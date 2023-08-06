from functools import reduce


def __reduce(res, x):
    for lic in x['licenses']:
        if lic not in res:
            res[lic] = []
        res[lic].append(x['name'])
    return res


def flatten_license_dependencies(dependencies):
    return reduce(__reduce, dependencies, {})