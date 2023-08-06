from benvy.databricks.repos.config.BootstrapConfig import BootstrapConfig
from benvy.container.dicontainer import Container


class BootstrapSetupEnvConfig(BootstrapConfig):
    def get_setup_steps(self, container: Container):
        return [
            container.get_sys_path_appender(),
            container.get_project_root_dir_setter(),
            container.get_app_env_setter(),
            container.get_bootstrap_env_setter(),
        ]
