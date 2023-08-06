# Development environment initialization

for the [Daipe stack](https://docs.daipe.ai/)

### What it does

#### Local Computer

* Extends the [Pyfony dev environment initialization](https://github.com/pyfony/penvy)
* Downloads Hadoop's `winutils.exe` and puts it into the project's `.venv` directory (Windows only) 
* Downloads **Java 1.8** binaries and puts them into the `~/.databricks-connect-java` dir
* Creates the empty `~/.databricks-connect` file

#### Databricks Repos Environment

* Download and install poetry package manager
* Install dependencies from poetry.lock
* Set current working directory to project root
* Append src folder to sys path
* Set proper environment variables

**Usage**

```
%sh
pip install benvy==1.x.x
```

```
from benvy.databricks.repos import bootstrap

bootstrap.install()
```

```
from benvy.databricks.repos import bootstrap

bootstrap.setup_env()
```

```
# %install_master_package_whl
```
