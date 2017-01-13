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

for additional themes, include the themes package

`pip install hiss_themes`
`pex hiss_repl hiss_themes -c hiss -o ~/bin/hiss`

#### configuration

simple ipython config options can be put into `~/.hiss` (or anywhere so long as you specify the config path on the command line via `hiss -c /path/to/.hiss`

for example:

```
$ cat ~/.hiss
confirm_exit = false
autoreload = true
```
You can also customize the syntax highlighting using pygments styles!

Set your theme in your hiss config (see `pygments.styles.get_all_styles()` for a full list):

```
$ cat ~/.hiss
confirm_exit = false
autoreload = true
theme = monokai
```
#### screenshots

![](https://www.dropbox.com/s/12djf1idmzjhaei/Screenshot%202016-10-06%2000.59.15.png?raw=true)

#### still a work in progress

very open to contribution! just fork and submit a PR

looking for help with:

* adding some magic `%hiss` commands for macro management, convienence
* ~less hacky pygments theming maybe?~

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
