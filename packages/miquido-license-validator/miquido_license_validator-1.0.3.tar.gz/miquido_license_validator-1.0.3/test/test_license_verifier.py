import json
import os
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
        self.assertEqual(2, len(res['notok']))
        self.assertEqual(5, len(res['unknown']))
        self.assertEqual("MIT", res['ok'][0])
        self.assertEqual("bsd", res['notok'][0])
        self.assertEqual("GNU", res['notok'][1])

    @mock.patch('requests.get', side_effect=mocked_request)
    def test_ignores(self, mock):
        with open('test/fixtures/ignorelist.txt', 'r') as f:
            ignores = f.read()
        with open('.licenseignore', 'w') as f:
            f.write(ignores)

        res = license_validator.are_valid('test/fixtures/gl-license-scanning-report.json')

        self.assertEqual(1, len(res['ok']))
        self.assertEqual(1, len(res['notok']))
        self.assertEqual(3, len(res['unknown']))
        self.assertEqual("MIT", res['ok'][0])
        self.assertEqual("GNU", res['notok'][0])

    @classmethod
    def setUpClass(cls) -> None:
        with open('.licenseignore', 'r') as f:
            cls.actual_ignore = f.read()

    @classmethod
    def tearDownClass(cls) -> None:
        with open('.licenseignore', 'w') as f:
            f.write(cls.actual_ignore)

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        try:
            os.remove(".licenseignore")
        except FileNotFoundError:
            pass
