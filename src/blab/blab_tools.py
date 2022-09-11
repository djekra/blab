
import warnings, datetime
import bpyth as bpy


#############################################################################################################
### run_notebooks
#############################################################################################################

# https://nbconvert.readthedocs.io/en/latest/execute_api.html
def run_notebooks( exclude=[], out_dir = 'nb_out/', mode='list', cell_timeout=None  ):
    '''
    Uses nbconvert to starts all notebooks in the directory in alphabetical order.
    * exclude: Strings that must not appear in the file name
    * out_dir: Output-directory
    * mode:    'list'  list only the files to run
               'run'   run the files and stop on error
               'force' run the files, ignoring errors
    * cell_timeout: None or seconds
    '''
    
    import os   
    
    # Create
    if not os.path.exists(out_dir):
        os.makedirs(out_dir) 
    
    # List Files
    notebooks = [ f for f in os.listdir('.') if os.path.isfile( os.path.join('.', f))]
    notebooks = [ d for d in notebooks if d.endswith('ipynb') ]
    notebooks = [s for s in notebooks if not any(x in s for x in exclude)]
    notebooks = sorted(notebooks)
    
    print('Trying to run this {} notebooks:'.format(len(notebooks)))
    for nbf in notebooks:
        print('         {:<40}'.format(nbf)) 
    print()
    if not mode in ['run','force']:
        print("Set mode='run' or mode='force' to run these notebooks.")
        return
    
    # Run
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
    ep = ExecutePreprocessor(timeout=cell_timeout)   

    for nbfile in notebooks:

        #print('Starting', nbfile, end=' ')
        print('Running: {:<40}'.format(nbfile), end=' ')

        # öffnen
        with open(nbfile, encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        # ausführen
        startzeit = datetime.datetime.now()
        try:
            ep.preprocess(nb)
        except CellExecutionError:
            msg = 'Error executing the notebook "%s"\n\n' % nbfile
            warnings.warn(msg)
            if mode != 'force':
                raise        
        finally:
            # Ergebnis abspeichern
            stopzeit = datetime.datetime.now()
            difference = stopzeit - startzeit
            print( '  ', bpy.human_readable_seconds(difference.seconds)   )
            with open( out_dir + nbfile, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)  
            
    # Ende for
    print('='*60, '\n\n')


    
    
#############################################################################################################
### search_code
#############################################################################################################    

def search_notebooks( query, radius=1, exclude=[]):
    '''
    Searches notebooks for occurrences of a string.
    Not only the code, but also all output is searched.
    The search is case sensitive.
    radius=1: In the whole workspace
    radius=0: In the current directory
    '''
    
    import glob
    def suche_intern(query,pattern):
        result = []
        for filepath in glob.iglob(pattern, recursive=True):
            with open(filepath) as file:
                try:
                    s = file.read()
                    if (s.find(query) > -1):
                        result.append(filepath)
                except:
                    pass
        return result
    # ende suche_intern
                
    result = []
    if (radius == 0):
        pattern = '*.ipynb'
    else:
        pattern = '../**/*.ipynb'
    result += suche_intern(query,pattern)
    
    result += ['----------------------------------']
    if (radius == 0):
        pattern = '*.py'
    else:
        pattern = '../**/*.py'
    result += suche_intern(query,pattern)
    
    result = [s for s in result if not any(x in s for x in exclude)]
    
    # Ausgabe
    if len(result) < 1:
        print('Nothing found')
    else:
        for r in result:
            print(r)
    #return result
    
    
    