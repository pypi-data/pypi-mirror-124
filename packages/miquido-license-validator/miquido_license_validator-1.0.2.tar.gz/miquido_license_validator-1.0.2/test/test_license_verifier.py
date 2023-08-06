import json
import unittest
from unittest import mock
from miquido_license_validator import license_validator


class MockResponse:
    def __init__(self, status_code, json_body: dict):
        self.json_body = json_body
        self.status_code = status_code

    def json(self):
        return self.json_body


def mocked_request(*args, **kwargs):
    with open('test/fixtures/licenses_reference.json', 'r') as file:
        res = file.read()
    return MockResponse(200, json.loads(res))


class LicenseVerifierTests(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_request)
    def test_license_verifier(self, mock):
        res = license_validator.are_valid('test/fixtures/gl-license-scanning-report.json')
        self.assertEqual(1, len(res['ok']))
        self.assertEqual(1, len(res['notok']))
        self.assertEqual(6, len(res['unknown']))
        self.assertEqual("MIT", res['ok'][0])
        self.assertEqual("bsd", res['notok'][0])
