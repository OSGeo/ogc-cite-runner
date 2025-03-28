"""CLI Utilities for running CITE tests and parsing their results."""

from builtins import print as stdlib_print
import logging
import typing
from pathlib import Path

import click
import httpx
import pydantic
import typer

from . import (
    config,
    exceptions,
    models,
    teamengine_runner,
)

logger = logging.getLogger(__name__)
app = typer.Typer()


def _parse_pydantic_secret_str(value: str) -> pydantic.SecretStr:
    return pydantic.SecretStr(value)


_DEFAULT_OUTPUT_FORMAT = models.OutputFormat.MARKDOWN

_test_suite_identifier_argument = typing.Annotated[
    str, typer.Argument(help="Identifier of the test suite. Ex: ogcapi-features-1.0")
]
_teamengine_base_url_argument = typing.Annotated[
    str,
    typer.Argument(
        help="Base URL of teamengine service. Ex: http://localhost:8080/teamengine"
    ),
]
_teamengine_username_option = typing.Annotated[
    pydantic.SecretStr,
    typer.Option(
        help="Username for authenticating with teamengine",
        parser=_parse_pydantic_secret_str,
    ),
]
_teamengine_password_option = typing.Annotated[
    pydantic.SecretStr,
    typer.Option(
        help="Password for authenticating with teamengine",
        parser=_parse_pydantic_secret_str,
    ),
]


@app.callback()
def base_callback(
    ctx: typer.Context, debug: bool = False, network_timeout: int = 120
) -> None:
    context = config.get_context(
        debug=debug,
        network_timeout_seconds=network_timeout,
    )
    config.configure_logging(rich_console=context.rich_console, debug=debug)
    ctx.obj = context


@app.command("parse-result")
def parse_test_result(
    ctx: typer.Context,
    test_suite_result: typing.Annotated[
        Path,
        typer.Argument(
            exists=True, file_okay=True, dir_okay=False, help="Suite execution result"
        ),
    ],
    output_format: models.OutputFormat = _DEFAULT_OUTPUT_FORMAT,
    exit_with_error_on_suite_failed_result: bool = False,
    include_summary: bool = True,
    include_failed_detail: bool = True,
    include_skipped_detail: bool = True,
    include_passed_detail: bool = False,
):
    context: config.CiteRunnerContext = ctx.obj
    parsed = teamengine_runner.parse_test_suite_result(
        test_suite_result.read_text(), context.settings
    )
    serialized = teamengine_runner.serialize_suite_result(
        parsed,
        output_format,
        serialization_details=models.SerializationDetails(
            include_summary=include_summary,
            include_failed_detail=include_failed_detail,
            include_skipped_detail=include_skipped_detail,
            include_passed_detail=include_passed_detail,
        ),
        context=ctx.obj,
    )
    if output_format.print_pretty():
        context.rich_console.print(serialized)
    else:
        stdlib_print(serialized)
    raise typer.Exit(_get_exit_code(parsed, exit_with_error_on_suite_failed_result))


@app.command()
def execute_test_suite_from_github_actions(
    ctx: typer.Context,
    teamengine_base_url: _teamengine_base_url_argument,
    test_suite_identifier: _test_suite_identifier_argument,
    test_suite_input: typing.Annotated[
        list[str],
        typer.Argument(
            help=(
                "Space-separated list of inputs to be passed to teamengine. Each "
                "input must be formatted as key=value. Ex: "
                "iut=http://localhost:5000 noofcollections=-1"
            )
        ),
    ],
    teamengine_username: _teamengine_username_option = "ogctest",
    teamengine_password: _teamengine_password_option = "ogctest",
    exit_with_error_on_suite_failed_result: bool = False,
    output_format: models.OutputFormat = _DEFAULT_OUTPUT_FORMAT,
    include_summary: bool = True,
    include_failed_detail: bool = True,
    include_skipped_detail: bool = True,
    include_passed_detail: bool = False,
):
    """Execute a CITE test suite via github actions.

    This command presents a simpler interface to run the
    `execute-test-suite` command, making it easier to run as a github action.
    """
    suite_inputs = {}
    for raw_suite_input in test_suite_input:
        param_name, param_value = raw_suite_input.partition("=")[::2]
        param_values = suite_inputs.setdefault(param_name, [])
        param_values.append(param_value)
    parsed, serialized = _execute_test_suite(
        ctx.obj,
        teamengine_base_url=teamengine_base_url,
        test_suite_identifier=test_suite_identifier,
        teamengine_username=teamengine_username,
        teamengine_password=teamengine_password,
        test_suite_inputs=suite_inputs,
        output_format=output_format,
        serialization_details=models.SerializationDetails(
            include_summary=include_summary,
            include_failed_detail=include_failed_detail,
            include_skipped_detail=include_skipped_detail,
            include_passed_detail=include_passed_detail,
        ),
    )
    context: config.CiteRunnerContext = ctx.obj
    if output_format.print_pretty():
        context.rich_console.print(serialized)
    else:
        stdlib_print(serialized)
    raise typer.Exit(
        0
        if output_format == models.OutputFormat.RAW
        else _get_exit_code(parsed, exit_with_error_on_suite_failed_result)
    )


@app.command()
def execute_test_suite(
    ctx: typer.Context,
    teamengine_base_url: _teamengine_base_url_argument,
    test_suite_identifier: _test_suite_identifier_argument,
    teamengine_username: _teamengine_username_option = "ogctest",
    teamengine_password: _teamengine_password_option = "ogctest",
    test_suite_input: typing.Annotated[
        typing.Optional[list[click.Tuple]],
        typer.Option(
            click_type=click.Tuple([str, str]),
            help=(
                "Input name and value separated by a space. "
                "Ex: --test-suite-input iut http://localhost:5000"
            ),
        ),
    ] = None,
    output_format: models.OutputFormat = _DEFAULT_OUTPUT_FORMAT,
    include_summary: bool = True,
    include_failed_detail: bool = True,
    include_skipped_detail: bool = True,
    include_passed_detail: bool = False,
    exit_with_error_on_suite_failed_result: bool = False,
):
    """Execute a CITE test suite."""
    suite_inputs = {}
    for param_name, param_value in test_suite_input:
        param_values = suite_inputs.setdefault(param_name, [])
        param_values.append(param_value)
    context: config.CiteRunnerContext = ctx.obj
    parsed, serialized = _execute_test_suite(
        context,
        teamengine_base_url=teamengine_base_url,
        test_suite_identifier=test_suite_identifier,
        teamengine_username=teamengine_username,
        teamengine_password=teamengine_password,
        test_suite_inputs=suite_inputs,
        output_format=output_format,
        serialization_details=models.SerializationDetails(
            include_summary=include_summary,
            include_failed_detail=include_failed_detail,
            include_skipped_detail=include_skipped_detail,
            include_passed_detail=include_passed_detail,
        ),
    )
    if output_format == models.OutputFormat.RAW:
        logger.debug("Outputting raw response, as returned by teamengine...")
    if output_format.print_pretty():
        context.rich_console.print(serialized)
    else:
        stdlib_print(serialized)
    raise typer.Exit(
        0
        if output_format == models.OutputFormat.RAW
        else _get_exit_code(parsed, exit_with_error_on_suite_failed_result)
    )


def _execute_test_suite(
    context: config.CiteRunnerContext,
    teamengine_base_url: str,
    test_suite_identifier: str,
    teamengine_username: pydantic.SecretStr,
    teamengine_password: pydantic.SecretStr,
    test_suite_inputs: dict[str, list[str]],
    output_format: models.OutputFormat,
    serialization_details: models.SerializationDetails,
) -> tuple[models.TestSuiteResult | None, str]:
    logger.debug(f"{locals()=}")
    client = httpx.Client(timeout=context.network_timeout_seconds)
    base_url = teamengine_base_url.strip("/")
    if teamengine_runner.wait_for_teamengine_to_be_ready(client, base_url):
        logger.debug(
            f"Asking teamengine to execute test suite {test_suite_identifier!r}..."
        )
        try:
            raw_result = teamengine_runner.execute_test_suite(
                client,
                base_url,
                test_suite_identifier,
                test_suite_arguments=test_suite_inputs,
                teamengine_username=teamengine_username,
                teamengine_password=teamengine_password,
            )
        except exceptions.CiteRunnerException:
            logger.exception("Unable to collect test suite execution results")
            raise SystemExit(1)
        else:
            parsed = None
            if output_format == models.OutputFormat.RAW:
                logger.debug("Outputting raw response, as returned by teamengine...")
                serialized = raw_result
            else:
                logger.debug("Parsing test suite execution results...")
                parsed = teamengine_runner.parse_test_suite_result(
                    raw_result, context.settings
                )
                serialized = teamengine_runner.serialize_suite_result(
                    parsed,
                    output_format,
                    serialization_details,
                    context,
                )
            return parsed, serialized
    else:
        logger.critical("teamengine service is not available")
        raise SystemExit(1)


def _get_exit_code(
    parsed: models.TestSuiteResult, exit_with_error_on_suite_failed_result: bool
) -> int:
    return 0 if parsed.passed else (1 if exit_with_error_on_suite_failed_result else 0)
