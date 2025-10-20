# OGC CITE Runner

{Cover slide}

A runner for OGC test suites

- Ricardo Garcia Silva <ricardo.garcia.silva@gmail.com>
- Tom Kralidis <tom.kralidis@somewhere.com>


---

# OGC CITE Runner

{Part 1 - Explain what OCR is and why it exists}

- OGC CITE Runner is a test runner for OGC CITE test suites
- It is a thin layer of automation over OGC TeamEngine
- Lowers effort required for running CITE tests
- Allows projects implementing OGC standards to have quick feedback on compliance
- Can be run as a standalone tool
- Available as a GitHub Action - also usable on other platforms


---

# OGC CITE

{what is OGC CITE}

- CITE - Compliance and Interoperability Testing & Evaluation
- Compliance and testing program operated by OGC
- Set of procedures for verifying compliance of an application to OGC standards
- An organization submits an application for CITE
- Compliant applications are granted an OGC Certification Trademark License, certifying that a specific version of a software application complies with an OGC standard
- A large part of the CITE procedure is demonstrating that the application passes OGC test suite for the standard being certified


---

# OGC Test Suites

- Official test suites which are used in the CITE procedure
- Published by OGC


---

# OGC TeamEngine

{what is TeamEngine and how to run CITE tests with it}

- Official OGC test runner
- Runs OGC test suites
- Has a web interface
- Official instance hosted by OGC at https://cite.opengeospatial.org/teamengine/
- Open source software
- Can also be run locally via native install or through docker


---

# OGC CITE Runner

- OGC CITE Runner is a thin layer over OGC TeamEngine
- Provides a CLI useful for automating the running of OGC test suites
- Outputs results in multiple formats
- Can be integrated into application CI pipelines
- Allows setting up quick feedback loop between development and possible compliance


---

# Quickstart

{Part 2 - Show how it can be used as a standalone tool}

Start a local instance of OGC TeamEngine:

```shell
docker run \
    --rm \
    --name teamengine \
    --add-host=host.docker.internal:host-gateway \
    --publish=9080:8080 \
    ogccite/teamengine-production:1.0-SNAPSHOT
```

Install OGC CITE Runner:

```shell
# install ogc-cite-runner
pipx install ogc-cite-runner

# or with pip
python3 -m venv .venv
source .venv/bin/activate
pip install ogc-cite-runner
```

Start your service under test, for example pygeoapi:

```shell
git clone https://github.com/geopython/pygeoapi.git
cd pygeoapi/tests/cite
docker compose up -d
```

Use OGC CITE Runner to test your implementation:

```shell
ogc-cite-runner execute-test-suite \
    http://localhost:9080/teamengine \
    ogcapi-features-1.0 \
    --test-suite-input iut http://host.docker.internal:5001
```

---

{Part 3 - Show how it can be used in github actions}

---

{Part 4- Go through the various options and output formats}

---

{Part 5 - Talk about future developments}
