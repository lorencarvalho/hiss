[<img src="https://img.shields.io/pypi/v/hiss_repl.svg">](https://pypi.python.org/pypi/hiss_repl)


# 🐍 hiss

A simple & stripped down python REPL based on iPython

* provides all the normal functionality of iPython with a simple dotfile based config
* unobtrusive default prompt
* autodetection of virtualenvs

#### screenshots

![](https://www.dropbox.com/s/12djf1idmzjhaei/Screenshot%202016-10-06%2000.59.15.png?raw=true)

#### installation

`pip install hiss`

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

#### still a work in progress

very open to contribution! just fork and submit a PR

looking for help with:

* pygments support! seems like it can be done via the `pygments.styles` entry point
* adding magic `%hiss` commands for macro management

---

* Free software: MIT license
