import os

def ipynb_to_html(filename):
    """
    Jupyter notebook to html
    """
    cmd = """export PYTHONPATH=%(pythonpath)s && jupyter nbconvert --to notebook --inplace --execute %(ipynb)s --ExecutePreprocesser.timeout=1000 && jupyter nbconvert --to html %(ipynb)s """ % dict(ipynb=filename,
                                                                                                                                                                                                  pythonpath=os.environ['PYTHONPATH'])
    ou = os.system(cmd)


def execute_ipynb(filename):
    """
    Execute a jupyter notebook so that its results display when the notebook
    is opened. 
    """
    cmd = "export PYTHONPATH=%(pythonpath)s && jupyter nbconvert --to notebook --inplace --execute %(ipynb)s --ExecutePreprocesser.timeout=1000" % dict(ipynb=filename, pythonpath=os.environ['PYTHONPATH'])
    ou = os.system(cmd)
    if ou != 0:
        raise Exception("execute_ipynb failed")


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser('')
    parser.add_argument('input')
    parser.add_argument('--output', dest='output', default=None)
    parser.add_argument('--html', action='store_true', default=False)
    args = parser.parse_args()
    if args.output is None:
        output = args.input
        
    if args.html:
        ipynb_to_html(args.input)
    else:
        execute_ipynb(args.input)
