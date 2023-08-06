from .MCMCRun import MCMCRun
import multiprocessing
import kachery_client as kc
import os
from typing import List

def monitor_stan_run(*, run: MCMCRun, stan_output_dir: str, parameter_names: List[str]):
    worker_process = multiprocessing.Process(target=_start_monitoring, args=(run, stan_output_dir, parameter_names))
    worker_process.start()

def finalize_monitor_stan_run(output_dir):
    fname = f'{output_dir}/finalize_stan_run'
    time.sleep(3)
    # Write a file. When it disappears, we know we are done.
    with open(fname, 'w') as f:
        f.write('Finalizing monitoring of stan run')
    # wait until file disappears
    while os.path.exists(fname):
        time.sleep(1)

import os
import time
from typing import Dict, List

class OutputCsvFile:
    def __init__(self, *, csv_path: str, run: MCMCRun, chain_id: int, parameter_names: List[str]):
        self._csv_path = csv_path
        self._parameter_names = parameter_names
        self._run = run
        self._chain_id = chain_id
        self._iter_num = 0
        self._file = open(self._csv_path, 'r')
        self._num_lines_processed = 0
        self._header_fields = None
        self._complete = False
    def cleanup(self):
        self._file.close()
    @property
    def csv_path(self):
        return self._csv_path
    @property
    def num_lines_processed(self):
        return self._num_lines_processed
    @property
    def complete(self):
        return self._complete
    def iterate(self):
        lines = self._file.readlines()
        if len(lines) > 0:
            self._process_lines(lines)
            self._num_lines_processed += len(lines)
    def _process_lines(self, lines: List[str]):
        for line in lines:
            if len(line) <= 5:
                self._complete = True
            elif line.startswith('#'):
                #comment
                pass
            else:
                vals = line.strip().split(',')
                if self._header_fields is None:
                    self._header_fields = vals
                else:
                    parameters = {
                        'chain_id': self._chain_id,
                        'iter_num': self._iter_num,
                        'timestamp': time.time()
                    }
                    for ii, k in enumerate(self._header_fields):
                        if ii < len(vals):
                            if (k in self._parameter_names):
                                parameters[k] = float(vals[ii])
                    self._iter_num = self._iter_num + 1
                    self._run.add_record(parameters)

def _chain_id_from_csv_file_name(path: str):
    # should end with '-<id>.csv'
    ind = path.rindex('-')
    return int(path[ind+1:].split('.')[0])

class OutputMonitor:
    def __init__(self, *, output_dir: str, run: MCMCRun, parameter_names: List[str]):
        self._output_dir = output_dir
        self._run = run
        self._parameter_names = parameter_names
        self._output_csv_files: Dict[str, OutputCsvFile] = {}
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        for fname, x in self._output_csv_files.items():
            x.cleanup()
    def start_iterating(self, interval=1):
        last_status_print = 0
        while True:
            something_incomplete = self.iterate()
            if something_incomplete:
                elapsed = time.time() - last_status_print
                if elapsed > 8:
                    self.print_status()
                    last_status_print = time.time()
            if not something_incomplete:
                if not os.path.exists(self._output_dir):
                    break
                fname0 = f'{self._output_dir}/finalize_stan_run'
                if os.path.exists(fname0):
                    os.unlink(fname0)
                    break
            time.sleep(interval)
        self.print_status()
        self._run.finalize()
        self.print_status()
    def print_status(self):
        total_lines_processed = sum([x.num_lines_processed for x in self._output_csv_files.values()])
        print(f'{total_lines_processed} lines processed in {len(self._output_csv_files.values())} files')
    def iterate(self):
        if not os.path.exists(self._output_dir):
            return
        for fname in os.listdir(self._output_dir):
            if fname.endswith('.csv'):
                if fname not in self._output_csv_files:
                    chain_id = _chain_id_from_csv_file_name(fname)
                    self._output_csv_files[fname] = OutputCsvFile(csv_path=f'{self._output_dir}/{fname}', run=self._run, chain_id=chain_id, parameter_names=self._parameter_names)
        something_incomplete = False
        for fname in list(self._output_csv_files.keys()):
            x = self._output_csv_files[fname]
            if os.path.exists(x.csv_path):
                x.iterate()
                if not x.complete:
                    something_incomplete = True
            else:
                print(f'Closing {fname}')
                x.cleanup()
                something_updated = True
                del self._output_csv_files[fname]
        return something_incomplete


def _start_monitoring(run: MCMCRun, output_dir: str, parameter_names: List[str]):
    # sys.stdout = open('debug_' + str(os.getpid()) + ".out", "a")
    # sys.stderr = open('debugerr_' + str(os.getpid()) + "_error.out", "a")
    with OutputMonitor(output_dir=output_dir, run=run, parameter_names=parameter_names) as m:
        m.start_iterating(0.1)
