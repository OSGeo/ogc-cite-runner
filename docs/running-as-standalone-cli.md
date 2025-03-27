---
hide:
  - navigation
---

# Running as a standalone application


## Installation

!!! note

    cite-runner will likely be available on the Python Package Index in the
    near future. That is not the case yet.

In order to use cite-runner locally you will need to have [git] and [poetry]
installed. Once these are installed, cite-runner can be installed by cloning
this repository and using poetry to install it:

```shell
git clone https://github.com/OSGeo/cite-runner.git
cd cite-runner
poetry install
```

You can verify the installation by running

```shell
poetry run cite-runner --help
```

##### Starting a local teamengine instance

cite-runner is a [teamengine] runner. the OGC application used for running
test suites. As such


### Usage

cite-runner is executed by calling the `cite-runner` command with a sub-command
and suitable arguments. For example:

```shell
poetry run cite-runner execute-test-suite \
    http://localhost:8080/teamengine \
    ogcapi-features-1.0 \
    --test-suite-input iut http://localhost:5000 \
    --test-suite-input noofcollections -1
```


##### Sub-commands

3. Start your service to be tested. Let's assume it is already running on `http://localhost:5000`

4. Run the teamengine docker image locally:

  ```shell
  docker run \
    --rm \
    --name teamengine \
    --network=host \
    ogccite/teamengine-production:1.0-SNAPSHOT
  ```

- Run the action code with

  ```shell
  poetry run cite-runner --help
  ```

There are additional commands and options which can be used when running locally, which allow controlling the output
format and how the inputs are supplied. Read the online

[git]: https://git-scm.com/
[poetry]: https://python-poetry.org/
[teamengine]:
