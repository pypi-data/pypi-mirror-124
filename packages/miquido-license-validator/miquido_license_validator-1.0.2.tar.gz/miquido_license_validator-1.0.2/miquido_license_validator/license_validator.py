import json
import requests
from functools import reduce


def __reduce(ok_licences, notok_licenses):
    def inner_reduce(res, x):
        if x.lower() in ok_licences:
            res['ok'].append(x)
        elif x.lower() in notok_licenses:
            res['notok'].append(x)
        else:
            res['unknown'].append(x)
        return res
    return inner_reduce


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
