#!/usr/bin/env python3
"""Validate the public career data contract without external services."""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

from resume_coverage import policy_errors, validate_resume_source

try:
    import yaml
except ImportError:
    raise SystemExit('Install the development dependency: python3 -m pip install -r requirements-dev.txt')

STATUSES = {'source_supported', 'externally_verified', 'self_reported', 'needs_confirmation', 'not_provided'}
ID_PATTERN = re.compile(r'^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$')
PLACEHOLDER = re.compile(r'\b(?:TODO|TBD|TBC|REPLACE_ME|YOUR_[A-Z_]+)\b')
IGNORED_DIRS = {'.git', '.venv', '__pycache__', 'build', 'private', 'local', 'output', 'tmp', '.pytest_cache'}
TEXT_SUFFIXES = {'.md', '.yaml', '.yml', '.tex', '.py', '.txt'}
SECRET_PATTERNS = [re.compile(p) for p in (
    r'gh[pousr]_[A-Za-z0-9]{20,}', r'github_pat_[A-Za-z0-9_]{20,}',
    r'AKIA[0-9A-Z]{16}', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'(?i)(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*[\x22\x27]?[A-Za-z0-9_+/=-]{20,}',
)]
EMAIL_PATTERN = re.compile(r'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
PHONE_PATTERN = re.compile(r'(?<!\w)(?:\+?\d[ ().-]*){10,15}(?!\w)')


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of silently losing evidence."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise yaml.constructor.ConstructorError('mapping', node.start_mark, f'duplicate key: {key}', key_node.start_mark)
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def public_files(root):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and not any(part in IGNORED_DIRS for part in p.relative_to(root).parts)
                  and p.name != 'contact.local.tex')


def parse_data(path):
    text = path.read_text(encoding='utf-8')
    if path.suffix == '.md':
        if not text.startswith('---\n'):
            return None
        chunks = text.split('\n---\n', 1)
        if len(chunks) != 2:
            raise ValueError('Unterminated Markdown front matter')
        text = chunks[0][4:]
    value = yaml.load(text, Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError('Data document must contain a mapping')
    return value


def validate_repository(root, private_values=()):
    """Return (errors, warnings, counts); never print private values."""
    root = Path(root).resolve()
    errors, warnings, data, ids = [], [], {}, {}

    def error(code, path, message):
        errors.append(f'{code} {path}: {message}')

    def register(identifier, path):
        if not isinstance(identifier, str) or not ID_PATTERN.fullmatch(identifier):
            error('E_ID', path, 'missing or invalid identifier')
            return False
        elif identifier in ids:
            error('E_ID', path, f'duplicate identifier {identifier}')
            return False
        else:
            ids[identifier] = path
            return True

    files = public_files(root)
    for path in files:
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in {'.pdf', '.png', '.jpg', '.jpeg', '.docx', '.zip'}:
            error('E_PRIVACY', relative, 'binary evidence/output belongs outside the public source tree')
        if path.name == '.env' or path.name.startswith('.env.'):
            error('E_PRIVACY', relative, 'environment configuration must not be published')
        if path.suffix in {'.yaml', '.yml'} or (path.suffix == '.md' and path.read_text().startswith('---\n')):
            try:
                obj = parse_data(path)
                if not register(obj.get('id'), relative):
                    continue
                data[relative] = obj
                if obj.get('schema_version') != 1:
                    error('E_SCHEMA', relative, 'schema_version must be 1')
            except (ValueError, TypeError, yaml.YAMLError):
                error('E_YAML', relative, 'invalid YAML, duplicate key or malformed front matter')
        if path.suffix in TEXT_SUFFIXES or path.name == '.gitignore':
            text = path.read_text(encoding='utf-8')
            if any(pattern.search(text) for pattern in SECRET_PATTERNS):
                error('E_PRIVACY', relative, 'possible credential/private key; inspect locally')
            if any(not address.endswith('@users.noreply.github.com') for address in EMAIL_PATTERN.findall(text)):
                error('E_PRIVACY', relative, 'possible personal email; inspect locally')
            if PHONE_PATTERN.search(text):
                error('E_PRIVACY', relative, 'possible phone number; inspect locally')
            for value in private_values:
                if value and value.casefold() in text.casefold():
                    error('E_PRIVACY', relative, 'known private value found; value suppressed')
                    break

    for required in ['profile.yaml', 'skills.yaml', 'sources.yaml', 'index.yaml', 'DATA_REVIEW.md']:
        if required not in data:
            error('E_SCHEMA', required, 'required data file missing or unreadable')
    sources = data.get('sources.yaml', {})
    documents = {}
    locators = {}
    for doc in sources.get('documents', []):
        if not register(doc.get('id'), 'sources.yaml'):
            continue
        documents[doc.get('id')] = doc
        if not isinstance(doc.get('page_count'), int) or doc['page_count'] < 0:
            error('E_SOURCE', 'sources.yaml', 'source page_count must be a nonnegative integer')
        if not re.fullmatch(r'[a-f0-9]{64}', str(doc.get('sha256', ''))):
            error('E_SOURCE', 'sources.yaml', 'source must have an SHA-256 fingerprint')
    for locator in sources.get('locators', []):
        if not register(locator.get('id'), 'sources.yaml'):
            continue
        locators[locator.get('id')] = locator
        doc = documents.get(locator.get('source_id'))
        pages = locator.get('pages')
        if not doc or not isinstance(pages, list) or any(not isinstance(p, int) or p < 1 or p > doc.get('page_count', 0) for p in pages):
            error('E_SOURCE', 'sources.yaml', 'locator source/pages do not resolve')
        elif doc.get('page_count', 0) > 0 and not pages:
            error('E_SOURCE', 'sources.yaml', 'paginated source locator needs at least one page')
        if not locator.get('section'):
            error('E_SOURCE', 'sources.yaml', 'locator needs a descriptive section')

    review_items = data.get('DATA_REVIEW.md', {}).get('review_items', [])
    reviews = {}
    for item in review_items:
        if not register(item.get('id'), 'DATA_REVIEW.md'):
            continue
        reviews[item.get('id')] = item
        if item.get('status') not in {'open', 'resolved'} or not item.get('question') or not item.get('generation_policy'):
            error('E_REVIEW', 'DATA_REVIEW.md', 'review needs status, question and generation policy')
        if item.get('status') == 'resolved' and (not item.get('resolution') or not item.get('source_refs')):
            error('E_REVIEW', 'DATA_REVIEW.md', 'resolved item needs resolution and source evidence')

    claims = {}
    for path, obj in data.items():
        for claim in obj.get('claims', []):
            if not register(claim.get('id'), path):
                continue
            claims[claim.get('id')] = claim
            if not claim.get('text') or not claim.get('kind') or claim.get('verification_status') not in STATUSES:
                error('E_CLAIM', path, 'claim needs text, kind and valid evidence status')
            if not isinstance(claim.get('source_refs'), list) or not claim['source_refs']:
                error('E_EVIDENCE', path, 'each claim needs source evidence')
            if claim.get('verification_status') in {'source_supported', 'externally_verified'} and PLACEHOLDER.search(claim.get('text', '')):
                error('E_PLACEHOLDER', path, 'confirmed claim contains an unresolved placeholder')

    by_id = {obj['id']: obj for obj in data.values()}

    def refs(values, allowed, path, label):
        if not isinstance(values, list):
            error('E_REFERENCE', path, f'{label} must be a list')
            return
        for value in values:
            if value not in allowed:
                error('E_REFERENCE', path, f'unresolved {label}: {value}')

    def month(value, path, field):
        if value is None:
            return None
        try:
            if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}', value):
                raise ValueError()
            return datetime.strptime(value, '%Y-%m')
        except ValueError:
            error('E_DATE', path, f'{field} must be null or a real YYYY-MM string')
            return None

    def check_source_refs(value, path):
        if isinstance(value, dict):
            if 'source_refs' in value:
                refs(value['source_refs'], locators, path, 'source_refs')
            for nested in value.values():
                check_source_refs(nested, path)
        elif isinstance(value, list):
            for nested in value:
                check_source_refs(nested, path)

    for path, obj in data.items():
        check_source_refs(obj, path)
        if 'verification_status' in obj and obj['verification_status'] not in STATUSES:
            error('E_SCHEMA', path, 'invalid record verification_status')
        if obj.get('kind') in {'experience', 'project', 'education', 'languages', 'achievements', 'certifications'}:
            for field in ['verification_status', 'source_refs', 'claims']:
                if field not in obj:
                    error('E_SCHEMA', path, f'missing {field}')
        if obj.get('kind') == 'experience' and (not obj.get('role') or 'organization' not in obj):
            error('E_SCHEMA', path, 'experience needs role and nullable organization')
        if obj.get('kind') == 'project' and (not obj.get('name') or not obj.get('project_type')):
            error('E_SCHEMA', path, 'project needs name and type')
        if obj.get('kind') in {'experience', 'project', 'education'}:
            for field in ['start_date', 'end_date', 'date_status']:
                if field not in obj:
                    error('E_SCHEMA', path, f'missing {field}')
            if obj.get('date_status') not in {'source_supported', 'not_provided', 'partially_provided'}:
                error('E_DATE', path, 'invalid date_status')
        start = month(obj.get('start_date'), path, 'start_date')
        end = month(obj.get('end_date'), path, 'end_date')
        month(obj.get('expected_graduation'), path, 'expected_graduation')
        if start and end and start > end:
            error('E_DATE', path, 'start_date is after end_date')
        if obj.get('ongoing_as_of_source') is True:
            if obj.get('end_date') is not None or not obj.get('source_as_of'):
                error('E_DATE', path, 'ongoing role needs null end_date and a source snapshot')
            try:
                snapshot = datetime.strptime(obj['source_as_of'], '%Y-%m-%d')
                if start and start > snapshot:
                    error('E_DATE', path, 'role starts after its source snapshot')
            except (KeyError, TypeError, ValueError):
                error('E_DATE', path, 'invalid source_as_of date')
        for key in ['experience_refs', 'project_refs', 'background_refs', 'education_refs']:
            if key in obj:
                refs(obj[key], by_id, path, key)
        if 'review_refs' in obj:
            refs(obj['review_refs'], reviews, path, 'review_refs')
        for language in obj.get('languages', []):
            refs([language.get('claim_ref')], claims, path, 'claim_ref')
    for item in review_items:
        refs(item.get('record_refs', []), by_id, 'DATA_REVIEW.md', 'record_refs')

    experiences = {identifier: obj for identifier, obj in by_id.items() if obj.get('kind') == 'experience'}
    experience_refs = data.get('profile.yaml', {}).get('experience_refs', [])
    if (not isinstance(experience_refs, list) or set(experience_refs) != set(experiences)
            or len(experience_refs) != len(set(experience_refs))):
        error('E_COVERAGE', 'profile.yaml', 'experience_refs must list every experience record exactly once, including background activities')
    policy = data.get('cv/generation-policy.yaml', {})
    for message in policy_errors(policy):
        error('E_POLICY', 'cv/generation-policy.yaml', message)
    for resume in [root / 'cv/template.tex', *sorted((root / 'cv/examples').glob('*.tex'))]:
        if resume.is_file():
            coverage_errors, _ = validate_resume_source(resume.read_text(), experiences, policy)
            for message in coverage_errors:
                error('E_RESUME', resume.relative_to(root), message)

    inventory = data.get('skills.yaml', {})
    categories = {}
    for cat in inventory.get('categories', []):
        if not register(cat.get('id'), 'skills.yaml'):
            continue
        categories[cat.get('id')] = cat
        if not cat.get('name'):
            error('E_SKILL', 'skills.yaml', 'category needs a name')
    for skill in inventory.get('skills', []):
        if not register(skill.get('id'), 'skills.yaml'):
            continue
        for field in ['name', 'category', 'tags', 'evidence_refs', 'verification_status', 'evidence_type', 'related_experiences', 'related_projects', 'related_background']:
            if field not in skill:
                error('E_SKILL', 'skills.yaml', f'skill missing {field}')
        if skill.get('category') not in categories or not skill.get('name') or not skill.get('tags'):
            error('E_SKILL', 'skills.yaml', 'skill needs name, tags and a registered category')
        if skill.get('verification_status') not in STATUSES:
            error('E_SKILL', 'skills.yaml', 'invalid skill verification_status')
        refs(skill.get('evidence_refs', []), claims, 'skills.yaml', 'evidence_refs')
        if not skill.get('evidence_refs'):
            error('E_EVIDENCE', 'skills.yaml', 'skill needs supporting claims')
        if skill.get('verification_status') in {'source_supported', 'externally_verified'} and not any(claims.get(ref, {}).get('verification_status') in {'source_supported', 'externally_verified'} for ref in skill.get('evidence_refs', [])):
            error('E_EVIDENCE', 'skills.yaml', 'supported skill has only listed/uncertain evidence')
        for key, kinds in [('related_experiences', {'experience'}), ('related_projects', {'project'}), ('related_background', {'education', 'languages', 'achievements', 'certifications'})]:
            refs(skill.get(key, []), {i for i, obj in by_id.items() if obj.get('kind') in kinds}, 'skills.yaml', key)
        for field in ['years_experience', 'proficiency_score']:
            if field in skill:
                error('E_SKILL', 'skills.yaml', f'{field} needs a schema extension and direct evidence')
        if 'proficiency' in skill and not isinstance(skill['proficiency'], dict):
            error('E_SKILL', 'skills.yaml', 'proficiency needs structured source-backed metadata')

    manifest = data.get('index.yaml', {})
    expected = {obj['id']: path for path, obj in data.items() if path != 'index.yaml'}
    indexed = {}
    for item in manifest.get('records', []):
        if item.get('id') in indexed:
            error('E_INDEX', 'index.yaml', 'duplicate manifest record')
        indexed[item.get('id')] = item.get('path')
    if indexed != expected:
        error('E_INDEX', 'index.yaml', 'manifest must cover every canonical data record with the exact ID/path')
    for path in manifest.get('entry_points', []):
        if not (root / path).is_file():
            error('E_INDEX', 'index.yaml', 'entry point does not exist')

    external = set()
    for path in files:
        if path.suffix == '.md':
            for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', path.read_text()):
                target = target.strip('<>')
                parsed = urlsplit(target)
                if parsed.scheme in {'http', 'https'}:
                    external.add(target)
                elif parsed.scheme or target.startswith('#'):
                    continue
                elif not (path.parent / unquote(parsed.path)).resolve().is_file():
                    error('E_LINK', path.relative_to(root), f'missing Markdown target: {target}')
        if path.suffix == '.tex':
            text = path.read_text()
            if re.search(r'\\(?:write18|openout)\b|\\input\{https?://', text):
                error('E_TEX', path.relative_to(root), 'unsafe external command or remote TeX input')
            for target in re.findall(r'\\input\{(cv/[^}]+)\}', text):
                if not (root / target).is_file():
                    error('E_LINK', path.relative_to(root), 'missing local TeX input')
    counts = {'records': len(expected), 'claims': len(claims), 'skills': len(inventory.get('skills', [])), 'categories': len(categories), 'sources': len(documents), 'locators': len(locators), 'open_reviews': sum(i.get('status') == 'open' for i in review_items), 'public_files': len(files), 'external_urls': sorted(external)}
    return errors, warnings, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--private-values', type=Path, help='Local file outside repository; one private value per line; values never printed')
    parser.add_argument('--check-external-links', action='store_true', help='Optional network access checks; inaccessible URLs are warnings')
    args = parser.parse_args()
    private_values = args.private_values.read_text().splitlines() if args.private_values else ()
    errors, warnings, counts = validate_repository(args.root, private_values)
    if args.check_external_links:
        for url in counts['external_urls']:
            try:
                with urlopen(Request(url, method='HEAD', headers={'User-Agent': 'career-knowledge-base-validator/1'}), timeout=15) as response:
                    if response.status >= 400:
                        warnings.append(f'W_EXTERNAL inaccessible public URL: {url}')
            except Exception:
                warnings.append(f'W_EXTERNAL could not verify public URL: {url}')
    for item in errors + warnings:
        print(item)
    if errors:
        print(f'FAIL: {len(errors)} error(s), {len(warnings)} warning(s)')
        return 1
    visible = {k: v for k, v in counts.items() if k != 'external_urls'}
    print('PASS:', ', '.join(f'{key}={value}' for key, value in visible.items()))
    print(f'External access checks: {len(counts["external_urls"])} attempted' if args.check_external_links else 'External access checks: not requested')
    return 0


if __name__ == '__main__':
    sys.exit(main())
