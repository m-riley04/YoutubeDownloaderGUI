import webbrowser
from subprocess import Popen

def visit_website(url:str="https://google.com"):
    '''Opens a website from a given URL in the browser'''
    return webbrowser.open_new_tab(url)
    
def open_path(path:str):
    '''Opens a path in the File Explorer'''
    Popen(fr'explorer /open, "{path}"')