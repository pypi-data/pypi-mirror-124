import venv
import os
import entry_points_txt

import subprocess
from subprocess import CompletedProcess

from pathlib import Path

from typing import Sequence

from .exceptions import VEnvOutputError



class VEnv:
    """A Python virtual environment"""

    def __init__(self, path: str, **kwargs):
        self.path = Path(path)
        venv.create(self.path, **kwargs)


    # |--------------------
    # | TERMINAL COMMANDS

    def python(self, *args: Sequence[str]) -> CompletedProcess:
        """Run Python"""
        return subprocess.run(
            [self.path / 'bin' / 'python', *args],
            capture_output=True, text=True
        )

    def run_package(self, package_name: str, *args: Sequence[str]) -> CompletedProcess:
        """Run an installed Python package"""
        return self.python('-m', package_name, *args)

    def pip(self, *args: Sequence[str]) -> CompletedProcess:
        """Run PIP"""
        return self.run_package('pip', *args)


    # |-----------
    # | METADATA

    def installed_packages(self) -> list[str]:
        """Get installed packages"""

        # Get installed packages from `pip list`
        pkgs_string = self.pip('list').stdout
        packages = [line.split(maxsplit=1)  # "package_name  0.1.0"
                        for line in pkgs_string.splitlines()]

        # "Package" and "Version" headings are expected from a valid output
        if len(packages) < 1 or tuple(packages[0]) != ('Package', 'Version'):
            raise VEnvOutputError('`python -m pip list` did not return a valid list of packages')

        # Ignore the headings and divider and return the list
        return packages[2:]

    def entry_points(self) -> dict[dict[str, str]]:
        """Get entry points"""
        
        found = {}  # Found entry points

        # Go through all files in the `lib` directory
        for root, _, files in os.walk(self.path / 'lib', topdown=False):
            if 'entry_points.txt' not in files:
                continue

            # Open and parse every `entry_points.txt`
            with open(Path(root) / 'entry_points.txt', 'r') as f:
                for name, entries in entry_points_txt.load(f).items():
                    if name not in found:
                        found[name] = {}
                    
                    # Add entry points!
                    found[name].update(entries)

        return found