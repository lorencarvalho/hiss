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

for additional themes, include the [themes package](https://github.com/sixninetynine/hiss-themes)

`pip install hiss_themes`

`pex hiss_repl hiss_themes -c hiss -o ~/bin/hiss`

*want more themes?* add them to the [themes package](https://github.com/sixninetynine/hiss-themes) !!

#### configuration

simple ipython config options can be put into `~/.hiss` (or anywhere so long as you specify the config path on the command line via `hiss -c /path/to/.hiss`. You can also customize the syntax highlighting using pygments styles (see `pygments.styles.get_all_styles()` for a full list, or install the `hiss_themes` package for additional themes)! 

for example:

```
$ cat ~/.hiss
# Hiss config options, set to defaults
theme = legacy # syntax color theme, can be any built-in pygments theme or ones added by the hiss_themes package
autoreload = False # enables or disables iPython's autoreload feature
confirm_exit = False # controls whether or not you want to be prompted when exiting
colors = Linux # prompt and traceback color schemes, http://ipython.readthedocs.io/en/stable/config/details.html?highlight=colors#terminal-colors
editor = vim # which editor to use for macros like %edit
xmode = Context # how exceptions are reported, can be 'Context'|'Plain'|'Verbose'
```

#### screenshots
_default settings_
![](https://www.dropbox.com/s/12djf1idmzjhaei/Screenshot%202016-10-06%2000.59.15.png?raw=true)
_with custom theme_
![](https://www.dropbox.com/s/kruj91cdvc4701y/Screenshot%202017-01-16%2013.10.17.png?raw=true)
_virtualenv detection_
![](https://www.dropbox.com/s/s07fy6rttz0i6j0/Screenshot%202017-01-16%2013.11.20.png?raw=true)
#### still a work in progress

very open to contribution! just fork and submit a PR

looking for help with:

* adding some additional magic commands for macro management?, convienence?

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
