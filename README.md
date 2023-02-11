# blab Tools for Jupyter
Some Jupyter Tools, see `jupyter` directory

## Install
`pip install blab`

## Usage
Put this code in the first cell of your notebook:
```
# blab init
try:
    import blab
except ImportError as e:
    !pip install blab
startup_notebook = blab.blab_startup()
%run $startup_notebook  
```

## Features
* Finds a local folder named `libs` and integrates it into the Python path. Useful for your own private libraries.
* loads `autotime` (see https://github.com/cpcloud/ipython-autotime)
* loads `autoreload` 
* loads `ipytest`
* configures `%matplotlib inline`
* Tool: `run_notebooks`: Starts all notebooks in the directory in alphabetical order
* Tool: `search_notebooks`: Searches notebooks for occurrences of a string (wrapper for nbconvert)
* Tool: `raise Stop`: Ends the execution of a notebook and displays the elapsed time
* Tool: `bgc('orange')`: Sets the backbround color of a notebook cell (does not work in colab)



```python

```
