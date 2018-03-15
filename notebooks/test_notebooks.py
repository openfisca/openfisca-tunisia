# -*- coding: utf-8 -*-


'''
Checks notebook execution result.
Equal to this command + error management:
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=60 --output executed_notebook.ipynb demo.ipynb

For nbconvert information, see: http://nbconvert.readthedocs.io/en/latest/index.html
For jupyter configuration information, run: jupyter --path
'''

# Dependencies: nbformat, nbconvert, jupyter-client, ipykernel
import io
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError
import os

directory = os.path.dirname(os.path.realpath(__file__))
notebook_filename = os.path.join(directory, 'demo.ipynb')
run_path = directory
notebook_filename_out = os.path.join(directory, 'executed_notebook.ipynb')

with io.open(notebook_filename) as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python')
error = False
try:
    out = ep.preprocess(nb, {'metadata': {'path': run_path}})
except CellExecutionError:
    error = True
    out = None
    msg = 'Error executing the notebook "%s".\n\n' % notebook_filename
    msg += 'See notebook "%s" for the traceback.' % notebook_filename_out
    print(msg)
    raise
finally:
    with io.open(notebook_filename_out, mode='wt') as f:  # io.open avoids UnicodeEncodeError
        nbformat.write(nb, f)

if not error:
    os.remove(notebook_filename_out)
