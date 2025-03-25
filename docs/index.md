# CITE Runner

A test runner for [OGC CITE].

This project contains both a github action and a standalone CLI application for
testing your OGC server implementation with the official OGC CITE test suites.

Key features:

- **Runs as a github action**: Can be integrated into existing CI workflows
- **Runs as a standalone CLI application**: Can be run as a standalone tool
- **Multiple output formats**: Can output test suite results as markdown, JSON or XML

[OGC CITE]: https://github.com/opengeospatial/cite/wiki


## Examples

Integrate into your CI as a github action:

```yaml
jobs:
  perform-cite-testing:
    runs-on: ubuntu-24.04
    steps:
      - name: test ogcapi-features compliancy
        uses: OSGEO/cite-runner@main
        with:
          test_suite_identifier: ogcapi-features-1.0
          test_session_arguments: >-
            iut=http://localhost:5001
            noofcollections=-1
```

Run the same test suite as a standalone CLI application:

```shell
cite-runner execute-test-suite \
    http://localhost:8080/teamengine \
    ogcapi-features-1.0 \
    --test-suite-input iut http://localhost:5001 \
    --test-suite-input noofcollections -1 \
    --output-format markdown
```
