from .. import (
    config,
    models,
)


def to_markdown(
    parsed_result: models.TestSuiteResult,
    serialization_details: models.SerializationDetails,
    context: config.CiteRunnerContext,
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
    context: config.CiteRunnerContext,
) -> str:
    return parsed_result.model_dump_json(warnings="error")
