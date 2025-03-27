from rich.table import Table

from .. import models
from ..models import CiteRunnerContext


def to_markdown(
    parsed_result: models.TestSuiteResult,
    serialization_details: models.SerializationDetails,
    context: CiteRunnerContext,
) -> str:
    """Serialize parsed test suite results to markdown"""
    template = context.jinja_environment.get_template(
        context.settings.simple_serializer_template
    )
    return template.render(
        result=parsed_result,
        serialization_details=serialization_details,
    )


def to_json(
    parsed_result: models.TestSuiteResult,
    serialization_details: models.SerializationDetails,
    context: CiteRunnerContext,
) -> str:
    return parsed_result.model_dump_json(indent=2)


def to_terminal(
    parsed_result: models.TestSuiteResult,
    serialization_details: models.SerializationDetails,
    context: CiteRunnerContext,
) -> str:
    table = Table("Conformance classes")
    table.add_column("Title")
    table.add_column("Failed")
    table.add_column("Skipped")
    table.add_column("Passed")
    for conformance_class in parsed_result.conformance_class_results:
        table.add_row(
            conformance_class.title,
            conformance_class.num_failed_tests,
            conformance_class.num_skipped_tests,
            conformance_class.num_passed_tests,
        )
