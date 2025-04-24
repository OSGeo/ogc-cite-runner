---
hide:
   - navigation
---

# Development

cite-runner is implemented in Python.

The standalone application depends on the following third-party projects:

- [typer:material-open-in-new:]{: target="blank_" } for CLI commands
- [pydantic:material-open-in-new:]{: target="blank_" } for models
- [jinja:material-open-in-new:]{: target="blank_" } for output format templates
- [httpx:material-open-in-new:]{: target="blank_" } for making network requests
- [lxml:material-open-in-new:]{: target="blank_" } for parsing teamengine responses
- [mkdocs:material-open-in-new:]{: target="blank_" } for documentation

### Brief implementation overview

cite-runner runs CITE tests suites by calling [teamengine's web API:material-open-in-new:]{: target="blank_" }. It
requests test suite results in the EARL (AKA the W3C Evaluation and Report
Language) format, which is XML-based.

After obtaining a test suite run result in EARL format, cite-runner parses it
into an instance of `models.TestSuiteResult`, its internal data structure.From
there, it is able to serialize it into either JSON or markdown.


### Setting up a development environment

In a brief nutshell:

1. Fork the cite-runner repository

2. Clone your fork to your local environment

3. Install [uv:material-open-in-new:]{: target="blank_" }

4. Use uv to install the cite-runner code locally. This will create a virtualenv and install all
   dependencies needed for development, including for working on docs:

    ```shell
    uv sync
    ```

5. Optionally (but strongly recommended) enable the [pre-commit:material-open-in-new:]{: target="blank_" } hooks
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


## Release management

cite-runner releases are managed with a [GitHub actions workflow:material-open-in-new:]{: target="_blank" }, which is
set up to run whenever a new tag named `v*` is pushed to the repository. This workflow will:

- Call the CI workflow, which takes care of testing and building the application
- Create a GitHub release
- Publish the built application to PyPI

!!! note

    The release workflow is not fully automated, requiring the cite-runner maintainers to explicitly provide
    approval of new runs. This is intentional.



[GitHub actions workflow:material-open-in-new:]: https://github.com/OSGeo/cite-runner/blob/main/.github/workflows/release.yaml
[httpx:material-open-in-new:]: https://www.python-httpx.org/
[jinja:material-open-in-new:]: https://jinja.palletsprojects.com/en/stable/
[lxml:material-open-in-new:]: https://lxml.de/
[mkdocs:material-open-in-new:]: https://www.mkdocs.org/
[pre-commit:material-open-in-new:]: https://pre-commit.com/
[pydantic:material-open-in-new:]: https://docs.pydantic.dev/latest/
[teamengine's web API:material-open-in-new:]: https://opengeospatial.github.io/teamengine/users.html
[typer:material-open-in-new:]: https://typer.tiangolo.com/
[uv:material-open-in-new:]: https://docs.astral.sh/uv/
