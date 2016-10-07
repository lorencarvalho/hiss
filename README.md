[<img src="https://img.shields.io/pypi/v/hiss_repl.svg">](https://pypi.python.org/pypi/hiss_repl)
[![Build
Status](https://travis-ci.org/sixninetynine/hiss.svg?branch=master)](https://travis-ci.org/sixninetynine/hiss)


# 🐍 hiss

A simple & stripped down python REPL based on iPython

* provides all the normal functionality of iPython with a simple dotfile based config
* unobtrusive default prompt
* autodetection of virtualenvs

#### installation

`pip install hiss_repl`

alternatively (if you are _cool_ 😎) use [pex](https://github.com/pantsbuild/pex):

get pex (if you don't already have it):

```
virtualenv pextmp
source pextmp/bin/activate
pip install pex
mkdir -p ~/bin
pex pex -c pex -o ~/bin/pex
rm -rf pextmp && deactivate
```

python2.7:

```
pex hiss_repl -c hiss -o ~/bin/hiss
```
python3:

```
pex hiss_repl -c hiss --python `which python3` --python-shebang `which python3` -o ~/bin/hiss3
```

#### configuration

simple ipython configs can be put into `~/.hiss` (or anywhere and specified on the cli with `hiss
-c /path/to/.hiss`

for example:

```
osx ~ ❯❯❯ cat ~/.hiss
[IPython]
InteractiveShell.confirm_exit = True
```

any string/boolean ipython config option can be used. pure python object support is not yet
available (so stuff like `TerminalInteractiveShell.prompts\_class = ClassicPrompts` doesn't work)

#### screenshots

![](https://www.dropbox.com/s/12djf1idmzjhaei/Screenshot%202016-10-06%2000.59.15.png?raw=true)

#### still a work in progress

very open to contribution! just fork and submit a PR

looking for help with:

* pygments support! seems like it can be done via the `pygments.styles` entry point
* adding magic `%hiss` commands for macro management

---

* Free software: MIT license
