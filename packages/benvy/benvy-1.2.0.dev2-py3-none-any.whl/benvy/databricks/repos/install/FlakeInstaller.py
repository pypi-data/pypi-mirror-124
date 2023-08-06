import os
import IPython
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.poetry.DependenciesLoader import DependenciesLoader


class FlakeInstaller(SetupStepInterface):
    def __init__(
        self,
        dependencies_loader: DependenciesLoader,
        logger: Logger,
    ):
        self._dependencies_loader = dependencies_loader
        self._logger = logger

    def run(self):
        self._logger.info("Installing flake8")

        dependencies = self._dependencies_loader.load_dev()

        if "flake8" not in dependencies:
            self._logger.warning("flake8 missing in dev dependencies, skipping flake8 installation")
            return

        if "pycodestyle-magic" not in dependencies:
            self._logger.warning("pycodestyle-magic missing in dev dependencies, skipping flake8 installation")
            return

        IPython.get_ipython().run_line_magic(
            "pip", f"install flake8=={dependencies['flake8']['version']} pycodestyle_magic=={dependencies['pycodestyle-magic']['version']}"
        )

    def get_description(self):
        return "Install flake8"

    def should_be_run(self) -> bool:
        return "DAIPE_BOOTSTRAPPED" not in os.environ
