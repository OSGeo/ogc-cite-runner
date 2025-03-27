import datetime as dt
import enum
from typing import Generator

import jinja2
import pydantic
from rich import Console

from src.cite_runner.config import CiteRunnerSettings


class OutputFormat(str, enum.Enum):
    JSON = "json"
    MARKDOWN = "markdown"
    RAW = "raw"


class ParseableOutputFormat(str, enum.Enum):
    JSON = "json"
    MARKDOWN = "markdown"


class TestStatus(enum.Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class SerializationDetails(pydantic.BaseModel):
    include_summary: bool
    include_failed_detail: bool
    include_skipped_detail: bool
    include_passed_detail: bool


class TestSuiteInput(pydantic.BaseModel):
    name: str
    value: str


class TestCaseResult(pydantic.BaseModel):
    identifier: str
    status: TestStatus
    detail: str | None
    name: str | None
    description: str | None


class ConformanceClassResult(pydantic.BaseModel):
    title: str
    description: str
    num_failed_tests: int
    num_passed_tests: int
    num_skipped_tests: int
    tests: list[TestCaseResult]

    def gen_failed_tests(self) -> Generator[TestCaseResult, None, None]:
        for test_case in self.tests:
            if test_case.status == TestStatus.FAILED:
                yield test_case

    def gen_skipped_tests(self) -> Generator[TestCaseResult, None, None]:
        for test_case in self.tests:
            if test_case.status == TestStatus.SKIPPED:
                yield test_case

    def gen_passed_tests(self) -> Generator[TestCaseResult, None, None]:
        for test_case in self.tests:
            if test_case.status == TestStatus.PASSED:
                yield test_case


class TestSuiteResult(pydantic.BaseModel):
    suite_identifier: str
    suite_title: str
    test_run_start: dt.datetime
    test_run_end: dt.datetime
    test_run_duration: dt.timedelta
    num_tests_total: int
    num_failed_tests: int
    num_skipped_tests: int
    num_passed_tests: int
    inputs: list[TestSuiteInput]
    conformance_class_results: list[ConformanceClassResult]
    passed: bool


class CiteRunnerContext(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    debug: bool = False
    jinja_environment: jinja2.Environment = jinja2.Environment()
    network_timeout_seconds: int = 20
    rich_console: Console
    settings: CiteRunnerSettings
