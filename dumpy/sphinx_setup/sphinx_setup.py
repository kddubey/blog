"""
This is an extremely janky script which prepares everything needed to run `make html`.
If modules are added, refactored, etc. then delete the docs dir and run this script.
I also wanted to document this process somewhere in case I need it for a new project.
"""
# fmt: off
import os
from pathlib import Path
import subprocess

REPO_NAME = 'cappr'
PACKAGE_NAME = 'cappr'
PROJECT_NAME = 'CAPPr'
AUTHOR_NAME = 'kddubey'
VERSION = '1.0'
PACKAGE_DESC = r'''
Perform zero-shot text classification based on the following idea: for a given prompt 
and completion text pair, what's the probability that the completion comes after the 
prompt? Hence the name:

   | **C**\ompletion
   | **A**\fter
   | **P**\rompt
   | **Pr**\obability

The method is fleshed out in my `question on CrossValidated`_.

.. _question on CrossValidated: https://stats.stackexchange.com/q/601159/337906
'''

## can set this to pass (indented!)
CONF_SETUP_FUNC_BODY = '''
    pass
'''.lstrip('\n')
CONF_LINK_CODE_RESOLVE = (r'''
def linkcode_resolve(domain, info):
    import importlib
    import inspect
''' +
f'''
    code_url = "https://github.com/kddubey/{REPO_NAME}/blob/main"
''' +
r'''
    ## ty https://github.com/readthedocs/sphinx-autoapi/issues/202#issuecomment-907582382
    if domain != 'py':
        return
    if not info['module']:
        return

    mod = importlib.import_module(info["module"])

    if "." in info["fullname"]:
        objname, attrname = info["fullname"].split(".")
        obj = getattr(mod, objname)
        try:
            # object is a method of a class
            obj = getattr(obj, attrname)
        except AttributeError:
            # object is an attribute of a class
            return None
    else:
        obj = getattr(mod, info["fullname"])

    ## Unwrap the object to get the correct source file in case that is wrapped by a
    ## decorator
    obj = inspect.unwrap(obj)

    try:
        file = inspect.getsourcefile(obj)
        lines = inspect.getsourcelines(obj)
    except TypeError:
        # e.g. object is a typing.Union
        return None
    file = os.path.relpath(file, os.path.abspath(".."))
    start, end = lines[1], lines[1] + len(lines[0]) - 1

    file = file.lstrip('../')
    return f"{code_url}/{file}#L{start}-L{end}"
''')


assert os.curdir == REPO_NAME, "Put this script in the same directory as the repo"

os.mkdir('docs')
os.chdir('docs')


## Meowww
subprocess.run(['sphinx-quickstart', '-q', '--sep',
                '-p', PROJECT_NAME,
                '-a', AUTHOR_NAME,
                '-v', VERSION])
os.chdir('..')
subprocess.run(['sphinx-apidoc', '-M', '-e',
                '-o', os.path.join('docs', 'source'),
                REPO_NAME])


## Clean rsts: the Submodule and Subpackage headers are not useful, and neither are
## the module or package descriptors
## ty https://stackoverflow.com/a/67549866/18758987
src_dir = Path('docs', 'source')
for file in src_dir.iterdir():
    if not str(file).endswith(".rst"):
        continue

    with open(file, "r") as f:
        lines = f.read()

    junk_strs = ["Submodules\n----------", "Subpackages\n-----------"]

    for junk in junk_strs:
        lines = lines.replace(junk, "")

    lines = lines.replace(" module\n=", "\n")
    lines = lines.replace(" package\n=", "\n")

    with open(file, "w") as f:
        f.write(lines)


## Write docs/source/_static/css/custom.css to seperate arguments in a doc's function
## signature on different lines
## big ty to https://github.com/sphinx-doc/sphinx/issues/1514#issuecomment-742703082
css_str = r'''/* Newlines (\a) and spaces (\20) before each parameter */
.sig-param::before {
    content: "\a\20\20\20\20\20\20\20\20";
    white-space: pre;
}

/* Newline after the last parameter (so the closing bracket is on a new line) */
dt em.sig-param:last-of-type::after {
    content: "\a";
    white-space: pre;
}

/* To have blue background of width of the block (instead of width of content) */
dl.class > dt:first-of-type {
    display: block !important;
}

'''
os.makedirs(os.path.join('docs', 'source', '_static', 'css'))
custom_css = os.path.join('docs', 'source', '_static', 'css', 'custom.css')
with open(custom_css, 'w') as f:
    f.write(css_str)


## Re-write conf.py
import_str = '''import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "src")))

'''
extensions_str = 'extensions = ["sphinx.ext.linkcode", "sphinx.ext.napoleon", "sphinx.ext.autosectionlabel", ""sphinx_togglebutton""]'
html_theme_str = 'html_theme = "pydata_sphinx_theme"'
html_css_files_str = 'html_css_files = [os.path.join("css", "custom.css")]'
html_context_str = 'html_context = {"display_github": True, "github_user": "kddubey", "github_repo": "%s", "github_version": "main", "doc_path": "docs/source", "default_mode": "light"}' % REPO_NAME
setup_str = f'''
def setup(self):
{CONF_SETUP_FUNC_BODY}
'''

conf_py = os.path.join('docs', 'source', 'conf.py')
## prepend import
with open(conf_py, 'r') as contents:
    save = contents.read()
with open(conf_py, 'w') as contents:
    contents.write(import_str)
with open(conf_py, 'a') as contents:
    contents.write(save)

with open(conf_py, 'r') as f:
    lines = f.readlines()

## replace extensions, html_theme
lines_new = []
for line in lines:
    if line.startswith('extensions ='):
        lines_new.append(extensions_str)
    elif line.startswith('html_theme ='):
        lines_new.append(html_theme_str)
        lines_new.append('\n')
    else:
        lines_new.append(line)

## append html_css_files, setup
lines_new.append('\n')
lines_new.append(html_css_files_str)
lines_new.append('\n')
lines_new.append(html_context_str)
lines_new.append('\n')
lines_new.append(setup_str)
lines_new.append('\n')
lines_new.append(CONF_LINK_CODE_RESOLVE)

## overwrite
with open(conf_py, 'w') as f:
    f.writelines(lines_new)


## Re-write index.rst
index_rst = os.path.join('docs', 'source', 'index.rst')
with open(index_rst, 'r') as f:
    lines = f.readlines()

_package_rst_name = f'   {PACKAGE_NAME}' ## 3 spaces, not 4!
lines.insert(12, _package_rst_name)

with open(index_rst, 'w') as f:
    f.writelines(lines)
## now for the PACKAGE_DESC
with open(index_rst, 'r') as f:
    lines = f.readlines()

lines_before = []
found_it = False
lines_after = []
for line in lines:
    if not found_it:
        lines_before.append(line)
        if line.startswith('==='):
            found_it = True
    else:
        lines_after.append(line)

with open(index_rst, 'w') as f:
    lines = f.writelines(lines_before + [PACKAGE_DESC] + lines_after)

## Remove dangling modules.rst, and empty source/build dir
os.remove(os.path.join('docs', 'source', 'modules.rst'))
