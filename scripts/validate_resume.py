#!/usr/bin/env python3
"""Check a generated LaTeX resume against the current career experience registry."""
import argparse
from pathlib import Path
import sys

from resume_coverage import validate_resume_source
from validate import parse_data
from yaml import YAMLError


def load_context(root):
    root = Path(root).resolve()
    records = {}
    for item in parse_data(root / 'index.yaml')['records']:
        path = (root / item['path']).resolve()
        if root not in path.parents:
            raise ValueError('manifest record must be inside the repository')
        record = parse_data(path)
        if record.get('kind') == 'experience':
            records[record['id']] = record
    profile = parse_data(root / 'profile.yaml')
    if set(profile.get('experience_refs', [])) != set(records):
        raise ValueError('profile experience_refs must cover every indexed experience record')
    policy = parse_data(root / 'cv/generation-policy.yaml')
    return records, policy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('resume', type=Path)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--exclude', action='append', default=[], metavar='ID=OWNER_REQUEST_REASON',
                        help='Only for an explicit owner-requested omission; repeat per experience')
    args = parser.parse_args()
    exclusions = {}
    for value in args.exclude:
        identifier, separator, reason = value.partition('=')
        if not separator or not reason.strip() or identifier in exclusions:
            parser.error('--exclude needs a unique ID and a nonempty owner-request reason')
        exclusions[identifier] = reason
    try:
        records, policy = load_context(args.root)
        errors, report = validate_resume_source(args.resume.read_text(), records, policy, exclusions)
    except (OSError, ValueError, KeyError, TypeError, YAMLError) as exc:
        print(f'FAIL: {exc}')
        return 1
    for item in report:
        print(f'{item["id"]}: {item["decision"]} - {item["reason"]}')
    for error in errors:
        print(error)
    print('FAIL' if errors else 'PASS: all required experiences are covered')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
