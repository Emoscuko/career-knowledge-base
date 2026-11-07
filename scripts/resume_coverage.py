"""Pure checks for complete experience coverage in a generated LaTeX resume."""
import re
import unicodedata


def policy_errors(policy):
    errors = []
    coverage = policy.get('experience_coverage', {})
    if not isinstance(coverage, dict):
        return ['E_POLICY: experience_coverage must be a mapping']
    statuses = coverage.get('eligible_statuses', [])
    if policy.get('applies_to') != 'resume' or coverage.get('mode') != 'all_supported_distinct':
        errors.append('E_POLICY: resume policy must retain all supported distinct experiences')
    if (not isinstance(statuses, list) or not statuses or not all(isinstance(value, str) for value in statuses)
            or not set(statuses) <= {'source_supported', 'externally_verified'}):
        errors.append('E_POLICY: eligible statuses must be source-supported or externally verified')
    if coverage.get('omission_requires_explicit_user_request') is not True:
        errors.append('E_POLICY: experience omissions require an explicit user request')
    validation = policy.get('validation', {})
    if not isinstance(validation, dict) or validation.get('experience_macro') != 'ResumeExperience':
        errors.append('E_POLICY: coverage validation requires the ResumeExperience macro')
    layout = policy.get('layout', {})
    if not isinstance(layout, dict) or layout.get('overflow') != 'allow_second_page_before_omitting_experience':
        errors.append('E_POLICY: page budget must preserve complete experience coverage')
    return errors


def _argument(text, offset):
    while offset < len(text) and text[offset].isspace():
        offset += 1
    if offset >= len(text) or text[offset] != '{':
        raise ValueError('ResumeExperience requires five braced arguments')
    start, depth = offset + 1, 1
    offset += 1
    while offset < len(text):
        if text[offset] == '\\':
            offset += 2
            continue
        if text[offset] == '{':
            depth += 1
        elif text[offset] == '}':
            depth -= 1
            if depth == 0:
                return text[start:offset], offset + 1
        offset += 1
    raise ValueError('unclosed ResumeExperience argument')


def _plain(text):
    text = re.sub(r'\\[A-Za-z]+\*?', '', text)
    text = unicodedata.normalize('NFKC', text).casefold()
    return ''.join(char for char in text if char.isalnum())


def validate_resume_source(source, experiences, policy, exclusions=None):
    """Return errors and a complete coverage report; exclusions map IDs to owner-request reasons.

    This checks literal entry IDs and displayed organization/role fields, not general TeX
    execution or factual prose. Compilation and PDF inspection remain separate checks.
    """
    errors = policy_errors(policy)
    if errors:
        return errors, []
    exclusions = exclusions or {}
    eligible = set(policy['experience_coverage']['eligible_statuses'])
    required = {identifier for identifier, record in experiences.items()
                if record.get('verification_status') in eligible}
    for identifier, reason in exclusions.items():
        if identifier not in required or not isinstance(reason, str) or not reason.strip():
            errors.append(f'E_EXCLUSION: {identifier} needs an eligible record and explicit owner-request reason')

    # Ignore comments and the preamble: a name or macro definition there is not an experience entry.
    source = re.sub(r'(?<!\\)%[^\n]*', '', source)
    if '\\begin{document}' not in source or '\\end{document}' not in source:
        errors.append('E_RESUME: complete document environment required')
    body = source.partition('\\begin{document}')[2].partition('\\end{document}')[0]
    included = set()
    for match in re.finditer(r'\\ResumeExperience\b', body):
        try:
            fields, offset = [], match.end()
            for _ in range(5):
                field, offset = _argument(body, offset)
                fields.append(field)
        except ValueError as exc:
            errors.append(f'E_ENTRY: {exc}')
            continue
        identifier, organization, role, _, _ = fields
        if identifier not in experiences:
            errors.append(f'E_ENTRY: unknown experience ID {identifier}')
            continue
        if identifier in included:
            errors.append(f'E_ENTRY: duplicate experience ID {identifier}')
        included.add(identifier)
        record = experiences[identifier]
        if record.get('verification_status') not in eligible:
            errors.append(f'E_ATTRIBUTION: {identifier} is not a supported distinct experience')
        if identifier in exclusions:
            errors.append(f'E_EXCLUSION: {identifier} is both included and excluded')
        if not _plain(organization) or not _plain(role):
            errors.append(f'E_ENTRY: {identifier} must display an organization and role')
        if record.get('organization') and _plain(organization) != _plain(record['organization']):
            errors.append(f'E_ENTRY: {identifier} displays the wrong organization')
    for identifier in sorted(required - included - set(exclusions)):
        errors.append(f'E_COVERAGE: missing supported experience {identifier}')
    report = []
    for identifier, record in experiences.items():
        if identifier in included:
            decision, reason = 'included', 'Displayed in an experience entry; relevance changes detail and order.'
        elif identifier in exclusions:
            decision, reason = 'excluded_by_owner', exclusions[identifier]
        else:
            decision = 'missing' if identifier in required else 'deferred'
            reason = ('Supported experience must be included.' if identifier in required else
                      'Record is not established as a supported distinct role; follow its review policy.')
        report.append({'id': identifier, 'decision': decision, 'reason': reason})
    return errors, report
