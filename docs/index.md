---
title: cite-runner
hide:
  - navigation
---
<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>

<figure markdown="span">
  ![cite-runner-logo](assets/cite-runner-logo.svg)
</figure>

A test runner for [OGC CITE].

Key features:

- **Runs as a github action**: Can be integrated into existing CI workflows
- **Runs as a standalone CLI application**: Can be run as a standalone tool
- **Multiple output formats**: Can output test suite results as straight to the terminal, in markdown,
  JSON or XML

This project aims to simplify the running of OGC CITE tests suites so that
server implementations of OGC standards may ensure their compliance with them
more frequently.

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
    --test-suite-input noofcollections -1
```


## License

cite-runner is published under an [MIT license].


[MIT license]: https://github.com/OSGeo/cite-runner/blob/main/LICENSE
