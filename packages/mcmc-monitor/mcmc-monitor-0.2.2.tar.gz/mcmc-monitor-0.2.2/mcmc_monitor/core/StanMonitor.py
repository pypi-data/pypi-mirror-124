from .monitor_stan_run import monitor_stan_run, finalize_monitor_stan_run
from .MCMCRun import MCMCRun
from typing import List, Union
import tempfile
import os
import shutil
import time

class StanMonitor():
    def __init__(self, *, label: str, parameter_names: List[str], output_dir: Union[str, None]=None, debugging: bool=False):
        self._label = label
        self._parameter_names = parameter_names
        self._output_dir = output_dir
        self._prefix = 'mcmc-monitor-'
        self._debugging = debugging

    def __enter__(self):
        if self._output_dir is None:
            dirpath = None
            self._output_dir = str(tempfile.mkdtemp(
                prefix=self._prefix, dir=dirpath))
            self._remove = True
        else:
            self._remove = False
        
        self._run = MCMCRun(label=self._label)
        
        # begin monitoring the output directory for this run
        figure = self._run.figurl()
        url = figure.url(label=self._label)
        print('========================================================')
        print(f'Monitoring stan run in directory: {self._output_dir}')
        print(f'URL: {url}')
        print('========================================================')
        monitor_stan_run(
            run=self._run,
            stan_output_dir=self._output_dir,
            parameter_names=self._parameter_names
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # allow monitoring to finish before removing directory
        print(f'Finalizing monitoring of stan run in directory: {self._output_dir}')
        try:
            finalize_monitor_stan_run(self._output_dir)
        except Exception as e:
            print(f'WARNING: problem finalizing stan run: {str(e)}')
        if self._remove and (not self._debugging):
            _rmdir_with_retries(self._output_dir, num_retries=5)

def _rmdir_with_retries(dirname: str, num_retries: int, delay_between_tries: float=1):
    for retry_num in range(1, num_retries + 1):
        if not os.path.exists(dirname):
            return
        try:
            shutil.rmtree(dirname)
            break
        except: # pragma: no cover
            if retry_num < num_retries:
                print('Retrying to remove directory: {}'.format(dirname))
                time.sleep(delay_between_tries)
            else:
                raise Exception('Unable to remove directory after {} tries: {}'.format(num_retries, dirname))