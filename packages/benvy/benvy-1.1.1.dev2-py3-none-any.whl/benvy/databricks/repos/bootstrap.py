from benvy.databricks.repos.runner.BootstrapRunner import BootstrapRunner
from benvy.container.dicontainer import Container
from benvy.databricks.repos.config.BootstrapInstallConfig import BootstrapInstallConfig
from benvy.databricks.repos.config.BootstrapSetupEnvConfig import BootstrapSetupEnvConfig
from benvy.databricks.detector import is_databricks_repo


def install():
    if not is_databricks_repo():
        return

    configs = [BootstrapInstallConfig()]
    runner = BootstrapRunner(configs, Container)  # noqa
    runner.run()


def setup_env():
    if not is_databricks_repo():
        return

    configs = [BootstrapSetupEnvConfig()]
    runner = BootstrapRunner(configs, Container)  # noqa
    runner.run()


if __name__ == "__main__":
    install()
    setup_env()
