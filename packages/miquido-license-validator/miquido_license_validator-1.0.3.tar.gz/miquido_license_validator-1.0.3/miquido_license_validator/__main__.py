import os
import sys
from miquido_license_validator import license_validator

ignore_unknown = os.getenv('IGNORE_UNKNOWN', False)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        eprint('Missing file argument')
        exit(1)

    result = license_validator.are_valid(sys.argv[1])

    if len(result['notok']) > 0:
        eprint('Not ok licenses found')
        eprint(result['notok'])
        exit(1)

    if not ignore_unknown and len(result['unknown']) > 0:
        eprint('Unknown licenses found')
        eprint(result['unknown'])
        exit(1)
