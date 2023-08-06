import os
import IPython
from logging import Logger
from penvy.poetry.PyprojectLoader import PyprojectLoader
from penvy.poetry.DependenciesLoader import DependenciesLoader


class FlakeSetupper:
    def __init__(
        self,
        pyproject_loader: PyprojectLoader,
        dependencies_loader: DependenciesLoader,
        logger: Logger,
    ):
        self._pyproject_loader = pyproject_loader
        self._dependencies_loader = dependencies_loader
        self._logger = logger

    def run(self):
        self._logger.info("Setting up flake8")

        pyproject = self._pyproject_loader.load()
        dependencies = self._dependencies_loader.load_dev()

        flake8_cmd = pyproject.get("tool", {}).get("poe", {}).get("tasks", {}).get("flake8")

        if not flake8_cmd:
            self._logger.warning("flake8 command missing in pyproject.toml, skipping flake8 setup")
            return

        if "flake8" not in dependencies:
            self._logger.warning("flake8 missing in dev dependencies, skipping flake8 setup")
            return

        if "pycodestyle-magic" not in dependencies:
            self._logger.warning("pycodestyle-magic missing in dev dependencies, skipping flake8 setup")
            return

        flake8_options = str(flake8_cmd).split()
        flake8_options = " ".join([f"--{opt[2:].replace('=', ' ').replace('-', '_')}" for opt in flake8_options if opt.startswith("--")])

        IPython.get_ipython().run_line_magic("load_ext", "pycodestyle_magic")
        IPython.get_ipython().run_line_magic("flake8_on", flake8_options)

    def get_description(self):
        return "Setup flake8"

    def should_be_run(self) -> bool:
        return "DAIPE_BOOTSTRAPPED" not in os.environ
