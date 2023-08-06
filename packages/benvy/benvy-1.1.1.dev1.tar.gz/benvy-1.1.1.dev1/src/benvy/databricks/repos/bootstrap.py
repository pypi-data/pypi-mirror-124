from penvy.env.EnvInitRunner import EnvInitRunner
from benvy.container.dicontainer import Container
from benvy.databricks.repos.config.BootstrapInstallConfig import BootstrapInstallConfig
from benvy.databricks.repos.config.BootstrapSetupEnvConfig import BootstrapSetupEnvConfig
from benvy.databricks.detector import is_databricks_repo


def install():
    if not is_databricks_repo():
        return

    configs = [BootstrapInstallConfig()]
    runner = EnvInitRunner(configs, Container)  # noqa
    runner._skip_confirmation = lambda dummy: True
    runner.run()


def setup_env():
    if not is_databricks_repo():
        return

    configs = [BootstrapSetupEnvConfig()]
    runner = EnvInitRunner(configs, Container)  # noqa
    runner._skip_confirmation = lambda dummy: True
    runner.run()


if __name__ == "__main__":
    install()
    setup_env()
