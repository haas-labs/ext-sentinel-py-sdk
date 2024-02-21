# Virtual environment

Creation of virtual environments is done by executing the command venv:

```sh
python -m venv /path/to/new/virtual/environment
```

Running this command creates the target directory (creating any parent directories that don’t exist already) and places a `pyvenv.cfg` file in it with a `home` key pointing to the Python installation from which the command was run (a common name for the target directory is `.venv`). It also creates a `bin`  subdirectory containing a copy/symlink of the Python binary/binaries (as appropriate for the platform or arguments used at environment creation time). It also creates an (initially empty) `lib/pythonX.Y/site-packages` subdirectory. If an existing directory is specified, it will be re-used.

Once an environment has been created, you can activate it, e.g. by
sourcing an activate script in its bin directory. For example:

```sh
source .venv/bin/activate       # for bash/zsh shell
source .venv/bin/activate.fish  # for fish shell
```

## References

- [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)
