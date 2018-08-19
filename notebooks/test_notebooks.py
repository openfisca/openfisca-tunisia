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
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
import sys
import os
import logging
import traceback


log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


def is_notebook(file_path):
  return file_path[-6:] == ".ipynb"


def run(notebook_path):
    directory = os.path.dirname(notebook_path)
    run_path = directory
    notebook_filename = os.path.basename(notebook_path)
    notebook_filename_out = os.path.join(directory, 'executed_' + notebook_filename)

    with io.open(notebook_path) as f:
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
        log.error(msg)
        raise
    finally:
        with io.open(notebook_filename_out, mode='wt') as f:  # io.open avoids UnicodeEncodeError
            nbformat.write(nb, f)

    if not error:
        os.remove(notebook_filename_out)


if __name__ == "__main__":
  try:
    target = sys.argv[1]

    if os.path.isdir(target):
      for file in os.listdir(target):
        if is_notebook(file):
          log.debug("> " + file)
          run(os.path.join(target, file))
    else:
        if not is_notebook(target):
            raise Exception(u"Expected an .ipynb file. Got: {}".format(target))
        run(target)

  except BaseException as e:
    if len(sys.argv) == 1:
      log.error(u"Missing a directory or a notebook to test.")
      log.warn(u"USAGE : python test_notebooks.py target")
      log.warn(u"        where 'target' is a directory containing .ipynb file OR an .ipynb file to test.")
    else:
      if e.strerror:
        log.debug(str(e.__class__.__name__)+ ': ' + e.message)
        log.error(traceback.format_exc())
      else:
        log.error(traceback.format_exc())
    # raise e
