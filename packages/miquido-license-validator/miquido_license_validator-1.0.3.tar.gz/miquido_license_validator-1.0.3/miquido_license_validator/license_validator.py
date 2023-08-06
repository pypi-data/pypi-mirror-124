import json
import requests
from functools import reduce


def __reduce(ok_licences, notok_licenses):
    ignored_licenses = __get_ignored()

    def inner_reduce(res, x):
        if x.lower() in ignored_licenses:
            return res
        if x.lower() in ok_licences:
            res['ok'].append(x)
        elif x.lower() in notok_licenses:
            res['notok'].append(x)
        else:
            res['unknown'].append(x)
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

    licenses_names = list(map(lambda x: x['id'], licenses['licenses']))

    return reduce(__reduce(ok_licenses, notok_licenses), licenses_names, result)
