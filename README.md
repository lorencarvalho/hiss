[<img src="https://img.shields.io/pypi/v/hiss_repl.svg">](https://pypi.python.org/pypi/hiss_repl)
[![Build
Status](https://travis-ci.org/sixninetynine/hiss.svg?branch=master)](https://travis-ci.org/sixninetynine/hiss)


# 🐍 hiss

A simple & stripped down python REPL based on iPython

* all your favorite iPython goodness with a simple dotfile based config!
* unobtrusive default prompt!
* auto-magically detect & activate virtualenvs!
* easy to theme using pygments styles!

#### installation

`pip install hiss_repl`

alternatively (if you are _cool_ 😎) use [pex](https://github.com/pantsbuild/pex):

`pex hiss_repl -c hiss -o ~/bin/hiss`

#### configuration

simple ipython config options can be put into `~/.hiss` (or anywhere so long as you specify the config path on the command line via `hiss -c /path/to/.hiss`

for example:

```
$ cat ~/.hiss
[IPython]
InteractiveShell.confirm_exit = True
```

Any string or boolean IPython option can be declared. Pure python object support is not yet
available (so things like `TerminalInteractiveShell.prompts_class = ClassicPrompts` doesn't work)

You can also customize the syntax highlighting using pygments styles!

Set your theme in your hiss config (see `pygments.styles.get_all_styles()` for a full list):

```
$ cat ~/.hiss
[IPython]
confirm_exit = True
extensions = ['autoreload']
exec_lines = ['%autoreload 2']

[hiss.themes]
theme = monokai
```

Alternatively, you can drop python files with pygments style classes into `~/.hiss_themes` (or wherever):

```
$ ls ~/.hiss_themes
zenburn.py  tomorrow.py

$ cat ~/.hiss
[IPython]
confirm_exit = True
extensions = ['autoreload']
exec_lines = ['%autoreload 2']

[hiss.themes]
theme = tomorrow:Tomorrow
path = ~/.hiss_themes # this is the default
```

#### screenshots

![](https://www.dropbox.com/s/12djf1idmzjhaei/Screenshot%202016-10-06%2000.59.15.png?raw=true)

#### still a work in progress

very open to contribution! just fork and submit a PR

looking for help with:

* adding magic `%hiss` commands for macro management
* less hacky pygments theming maybe?

#### development

```
$ pex setuptools -- ./setup.py venv
running venv
('Creating virtual environment in ', '/home/lcarvalh/src/hiss/venv/hiss')
New python executable in /home/lcarvalh/src/hiss/venv/hiss/bin/python
Installing setuptools............done.
Installing pip...............done.
Linking `activate` to top level of project.

To activate, simply run `source activate`.
$ . activate
(hiss)$ python setup.py develop
```

---

* Free software: MIT license
