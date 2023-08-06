# venvarium

## Installation

```sh
python -m pip install venvarium
```

### Example

```py
from venvarium import VEnv


# Create the virtual environment
ENV_PATH = 'myproject/myenv' 
venv = VEnv(ENV_PATH)

# Run Python, PIP, or any other package or program
venv.python('-c', 'print("hello, world!")')
venv.pip('install', '--upgrade', 'pip')
venv.run_package('flask')

# See all installed packages
pkgs = venv.installed_packages()
print(pkgs)

# Get the entry points
entry_points = venv.entry_points().get('my_entry_point')
print(entry_points)
```