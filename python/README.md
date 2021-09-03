
## Python environment
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) : pyenv plugin which manages python virtual environment.
- [pipenv](https://github.com/pypa/pipenv):  packaging tool for Python application and manages package dependencies and its sub-dependencies.
- [pyenv](https://github.com/pyenv/pyenv) : Simple Python Version Management: pyenv [Install](https://github.com/pyenv/pyenv#installation)

```
# Add to bash profile
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
# pyenv works by inserting a directory of shims at the front of your PATH. A shim is a small library that intercepts and changes calls to another library. Adding the following enables shims and autocompletion.
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
pyenv install -l
pyenv install 3.7.7
pyenv install 3.8.2
pyenv versions
# setting global version
pyenv global 3.7.7
pyenv version
# pyenv local creates or modifies .python-verion in the directory. For example, pyenv local 3.7.7 creates .python-verion with Python 3.7.7. pyenv local 3.8.2 modifies .python-verion to Python 3.8.2

```
## Creating virtual env
### way 1
```bash
python3 -m venv ~/projects/tools/cdpvenv

# Force reinstall pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
```

### using [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv#installation)
```bash
# add to bash profile
pyenv-virtualenv
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Create a virtualenv called py377 using Python 3.7.7
$ pyenv virtualenv 3.7.7 py377
# Create a virtualenv called py382 using Python 3.8.2
$ pyenv virtualenv 3.8.2 py382
# Create a virtualenv called jupy based on the global Python version
$ pyenv virtualenv jupy
```
Once you created different virtualenvs, you can set a local virtualenv for a directory. Here I am using the [Oh-My-Zsh built-in command](https://towardsdatascience.com/the-ultimate-guide-to-your-terminal-makeover-e11f9b87ac99) take.

```
$ take py377
# Set a local(direcotry) python environment to 377
$ pyenv local py377
(py377)$ cat .python-version
py377

# remove local virtual env
# remvoing .python-version will set the directory to the global Python version
$ rm .python-version

# deleting virtual env
pyenv uninstall my-virtual-env
pyenv virtualenv-delete my-virtual-env
```

### using [pipenv](https://github.com/pypa/pipenv#installation)

- create a new project using pyhton 3.7 `pipenv --python 3.7 install`
- It creates a virtualenv , also creates Pipfile and Pipfile.lock

- pipenv works with pyenv

```
$ pipenv --python 3.6
Warning: Python 3.6 was not found on your system…
Would you like us to install CPython 3.6.10 with pyenv? [Y/n]: Y
Installing CPython 3.6.10 with pyenv (this may take a few minutes)…
⠼ Installing python...
$ ls 
Pipfile
```

- install packages e.g. `pipenv install numpy`
- Installing all dependencies for a project (including dev): `pipenv install --dev`
- Create a lockfile containing pre-releases: `pipenv lock --pre`
- Show a graph of your installed dependencies: `pipenv graph`
- Check your installed dependencies for security vulnerabilities: `pipenv check`
- Install a local setup.py into your virtual environment/Pipfile: `pipenv install -e .`
- Removing environment `pipenv --rm`
- activate the project’s virtualenv by running `pipenv shell`, and deactivate by running `exit`
- Ignore Pipfile and use Pipfile.lock to install dependencies `pipenv install --ignore-pipfile`


## [pyflow](https://github.com/David-OConnor/pyflow)
- Pyflow streamlines working with Python projects and files. It's an easy-to-use CLI app with a minimalist API. Never worry about having the right version of Python or dependencies.

