import logging

import jinja2
import pydantic
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from rich.console import Console
from rich.logging import RichHandler

from . import models


class CiteRunnerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CITE_RUNNER__", env_nested_delimiter="__"
    )
    default_json_serializer: str = "cite_runner.serializers.simple.to_json"
    default_markdown_serializer: str = "cite_runner.serializers.simple.to_markdown"
    default_console_serializer: str = "cite_runner.serializers.console.to_console"
    default_parser: str = "cite_runner.parsers.earl.parse_test_suite_result"
    extra_templates_path: str | None = None

    # ogcapi_features_1_0_parser: str = (
    #     "cite_runner.teamengine_runner.parse_test_suite_result")
    # ogcapi_features_1_0_markdown_serializer: str = (
    #     "cite_runner.teamengine_runner.serialize_test_suite_result")
    simple_serializer_template: str = "test-suite-result.md"
    docs_url: str = "https://osgeo.github.io/cite-runner/"
    disclaimer: str = (
        "cite-runner is not affiliated with the OGC. Having a CITE test suite be declared as passed by cite-runner "
        "does not mean the implementation under test is OGC certified nor does it mean that it is guaranteed to pass "
        "the official CITE certification program."
    )


class CiteRunnerContext(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    debug: bool = False
    jinja_environment: jinja2.Environment = jinja2.Environment()
    network_timeout_seconds: int = 20
    result_console: Console
    status_console: Console
    settings: CiteRunnerSettings


def get_settings() -> CiteRunnerSettings:
    return CiteRunnerSettings()


def _get_jinja_environment(settings: CiteRunnerSettings) -> jinja2.Environment:
    loaders = [
        jinja2.PackageLoader("cite_runner", "templates"),
    ]
    if settings.extra_templates_path is not None:
        loaders.append(jinja2.FileSystemLoader(settings.extra_templates_path))
    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader(loaders),
        extensions=[
            "jinja2_humanize_extension.HumanizeExtension",
        ],
    )
    env.globals.update(
        {
            "TestStatus": models.TestStatus,
        }
    )
    return env


def configure_logging(rich_console: Console, debug: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        handlers=[RichHandler(console=rich_console, rich_tracebacks=True)],
    )
    logging.getLogger("httpcore").setLevel(logging.INFO if debug else logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.INFO if debug else logging.WARNING)


def get_context(
    debug: bool,
    network_timeout_seconds: int,
) -> CiteRunnerContext:
    settings = get_settings()
    return CiteRunnerContext(
        debug=debug,
        network_timeout_seconds=network_timeout_seconds,
        jinja_environment=_get_jinja_environment(settings),
        settings=settings,
        result_console=Console(),
        status_console=Console(stderr=True),
    )
