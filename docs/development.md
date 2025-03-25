# Development

After having cloned this repo, install the code with dev dependencies by running:

```shell
poetry install --with dev
```

Enable the pre-commit hooks by running

```shell
poetry run pre-commit install
```

Optionally, do a first run of pre-commit on all files, which will also initialize
pre-commit's hooks

```shell
poetry run pre-commit run --all-files
```
