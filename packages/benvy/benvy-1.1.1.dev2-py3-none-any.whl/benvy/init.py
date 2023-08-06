from penvy.PenvyConfig import PenvyConfig
from benvy.BenvyConfig import BenvyConfig
from benvy.databricks.repos.config.BootstrapConfig import BootstrapConfig
from penvy.env.EnvInitRunner import EnvInitRunner
from benvy.container.dicontainer import Container


def main():
    configs = [
        PenvyConfig(),
        BenvyConfig(),
        BootstrapConfig(),
    ]

    runner = EnvInitRunner(configs, Container)
    runner.run()


if __name__ == "__main__":
    main()
