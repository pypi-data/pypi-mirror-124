import json
import requests
from functools import reduce

from miquido_license_validator import common


def __reduce(ok_licences, notok_licenses, dependencies):
    ignored_licenses = __get_ignored()

    def inner_reduce(res, x):
        if x.lower() in ignored_licenses:
            return res
        elem = {'name': x, 'dependencies': dependencies[x]}
        if x.lower() in ok_licences:
            res['ok'].append(elem)
        elif x.lower() in notok_licenses:
            res['notok'].append(elem)
        else:
            res['unknown'].append(elem)
        return res

    return inner_reduce


def __get_ignored():
    try:
        with open('.licenseignore', 'r') as f:
            ignored_licenses = f.read().split('\n')

        return set(map(lambda x: x.lower(), ignored_licenses))

    except FileNotFoundError:
        return set()


def are_valid(license_file):
    with open(license_file, 'r') as f:
        licenses = json.loads(f.read())

    license_reference = requests.get('https://licenses.miquido.dev').json()
    ok_licenses = set(map(lambda x: x.lower(), license_reference['ok']))
    notok_licenses = set(map(lambda x: x.lower(), license_reference['notok']))
    result = {
        'ok': [],
        'notok': [],
        'unknown': []
    }

    dependencies = common.flatten_license_dependencies(licenses['dependencies'])

    licenses_names = list(map(lambda x: x['id'], licenses['licenses']))

    return reduce(__reduce(ok_licenses, notok_licenses, dependencies), licenses_names, result)
