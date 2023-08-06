import unittest

from miquido_license_validator import common

dependencies = [
    {
        "name": "PyYAML",
        "version": "5.4.1",
        "package_manager": "pip",
        "path": "requirements.txt",
        "licenses": [
            "LIC_1",
            "LIC_2"
        ]
    },
    {
        "name": "SecretStorage",
        "version": "3.3.1",
        "package_manager": "pip",
        "path": "requirements.txt",
        "licenses": [
            "LIC_1"
        ]
    },
    {
        "name": "cachetools",
        "version": "4.2.4",
        "package_manager": "pip",
        "path": "requirements.txt",
        "licenses": [
            "LIC_3"
        ]
    }
]


class LicenseDependencyFlattenTests(unittest.TestCase):
    def test_flatten(self):
        flatten = common.flatten_license_dependencies(dependencies)
        self.assertListEqual(['PyYAML', 'SecretStorage'], flatten['LIC_1'])
        self.assertListEqual(['PyYAML'], flatten['LIC_2'])
        self.assertListEqual(['cachetools'], flatten['LIC_3'])
