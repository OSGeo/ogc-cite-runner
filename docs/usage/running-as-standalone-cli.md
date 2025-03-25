# Running locally or on other CI platforms

This action's code can also be installed locally:

- Install [poetry](https://python-poetry.org/docs/)
- Clone this repository:

  ```shell
  git clone https://github.com/OSGeo/cite-runner.git
  ```
- Install the code:

  ```shell
  cd cite-runner
  poetry install
  ```

- Start your service to be tested. Let's assume it is already running on `http://localhost:5000`

- Run the teamengine docker image locally:

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
