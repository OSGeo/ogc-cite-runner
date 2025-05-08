"""These tests are meant to be run in a GitHub Action environment.

These are written with the standard Python unittest framework in order to not require
the installation of additional dependencies.
"""

import argparse
import json
import sys
import unittest

_RAW_JSON_REPORT: bytes | None = None


class TestGithubAction(unittest.TestCase):
    def setUp(self):
        global _RAW_JSON_REPORT
        self.parsed_report = json.loads(_RAW_JSON_REPORT)

    def test_report_main_result(self):
        self.assertFalse(self.parsed_report["passed"])

    def test_report_num_failed(self):
        self.assertEqual(self.parsed_report["num_failed_tests"], 4)

    def test_report_num_skipped(self):
        self.assertEqual(self.parsed_report["num_skipped_tests"], 36)

    def test_report_num_passed(self):
        self.assertEqual(self.parsed_report["num_passed_tests"], 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "json_report", type=argparse.FileType("rb"), help="raw JSON report"
    )
    args = parser.parse_args()
    global RAW_JSON_REPORT
    _RAW_JSON_REPORT = args.json_report.read()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestGithubAction)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
