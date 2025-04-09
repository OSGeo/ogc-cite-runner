---
hide:
   - navigation
---

# Development

cite-runner is implemented in Python.

The standalone application depends on the following third-party projects:

- [typer] for CLI commands
- [pydantic] for models
- [jinja] for output format templates
- [httpx] for making network requests
- [lxml] for parsing teamengine responses
- [mkdocs] for documentation

### Brief implementation overview

cite-runner runs CITE tests suites by calling [teamengine's web API]. It
requests test suite results in the EARL (AKA the W3C Evaluation and Report
Language) format, which is XML-based.

After obtaining a test suite run result in EARL format, cite-runner parses it
into an instance of `models.TestSuiteResult`, its internal data structure.From
there, it is able to serialize it into either JSON or markdown.


### Setting up a development environment

In a brief nutshell:

1. Fork the cite-runner repository

2. Clone you fork to your local environment

3. Install [uv]

4. Use uv to install the cite-runner code locally. This will create a virtualenv and install all
   dependencies needed for development, including for working on docs:

    ```shell
    uv sync
    ```

5. Optionally (but strongly recommended) enable the [pre-commit] hooks
   provided by cite-runner:

    ```shell
    uv run pre-commit install
    ```

6. Stand up a docker container with a local teamengine instance:

    ```shell
    docker run \
        --rm \
        --name=teamengine \
        --network=host \
        ogccite/teamengine-production:1.0-SNAPSHOT
    ```

    You should now be able to use `http:localhost:8080/teamengine` in
    cite-runner

    !!! warning

        teamengine will try to run on your local port `8080`, which could
        potentially already be occupied by another application.

7. Work on the cite-runner code

8. You can run cite-runner via uv with:

    ```shell
    uv run cite-runner
    ```

8. If you want to work on documentation, you can start the mkdocs server with:

    ```shell
    uv run mkdocs serve
    ```


[httpx]: https://www.python-httpx.org/
[jinja]: https://jinja.palletsprojects.com/en/stable/
[lxml]: https://lxml.de/
[mkdocs]: https://www.mkdocs.org/
[pre-commit]: https://pre-commit.com/
[pydantic]: https://docs.pydantic.dev/latest/
[teamengine's web API]: https://opengeospatial.github.io/teamengine/users.html
[typer]: https://typer.tiangolo.com/
[uv]: https://docs.astral.sh/uv/
