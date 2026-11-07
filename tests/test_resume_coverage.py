"""Regression checks for complete experience coverage with relevance-based emphasis."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from resume_coverage import validate_resume_source
from validate_resume import load_context


class ResumeCoverageTests(unittest.TestCase):
    def setUp(self):
        self.records, self.policy = load_context(ROOT)

    def entry(self, identifier):
        record = self.records[identifier]
        organization = record.get('organization') or record.get('source_label', 'Unattributed')
        role = record['role'].replace('&', r'\&')
        return '\\ResumeExperience{' + identifier + '}{' + organization + '}{' + role + '}{}{}'

    def document(self, without=()):
        entries = [self.entry(identifier) for identifier, record in self.records.items()
                   if record['verification_status'] in self.policy['experience_coverage']['eligible_statuses']
                   and identifier not in without]
        return '\\begin{document}\n' + '\n'.join(entries) + '\n\\end{document}'

    def check(self, source, exclusions=None):
        return validate_resume_source(source, self.records, self.policy, exclusions)

    def test_all_supported_roles_pass_and_uncertain_source_is_reported(self):
        errors, report = self.check(self.document())
        self.assertEqual([], errors)
        self.assertEqual(len(self.records), len(report))
        decisions = {item['id']: item['decision'] for item in report}
        self.assertEqual('included', decisions['experience-aselsan'])
        self.assertEqual('included', decisions['experience-content-creation'])
        self.assertEqual('deferred', decisions['experience-freelance-unattributed'])

    def test_annotation_resume_cannot_silently_omit_aselsan(self):
        errors, _ = self.check(self.document(without={'experience-aselsan'}))
        self.assertIn('E_COVERAGE: missing supported experience experience-aselsan', errors)

    def test_comment_and_preamble_entry_do_not_count(self):
        source = self.entry('experience-aselsan') + '\n' + self.document(without={'experience-aselsan'})
        source = source.replace('\\end{document}', '% ' + self.entry('experience-aselsan') + '\n\\end{document}')
        errors, _ = self.check(source)
        self.assertTrue(any('E_COVERAGE' in error and 'experience-aselsan' in error for error in errors))

    def test_new_supported_experience_automatically_becomes_required(self):
        records = deepcopy(self.records)
        records['experience-future'] = dict(kind='experience', organization='Future Company',
                                           role='Engineer', verification_status='source_supported')
        errors, _ = validate_resume_source(self.document(), records, self.policy)
        self.assertIn('E_COVERAGE: missing supported experience experience-future', errors)

    def test_mismatched_organization_cannot_satisfy_coverage(self):
        source = self.document().replace('{ASELSAN}', '{Different Company}')
        errors, _ = self.check(source)
        self.assertTrue(any('experience-aselsan displays the wrong organization' in error for error in errors))

    def test_duplicate_id_is_rejected(self):
        source = self.document().replace('\\end{document}', self.entry('experience-aselsan') + '\n\\end{document}')
        errors, _ = self.check(source)
        self.assertIn('E_ENTRY: duplicate experience ID experience-aselsan', errors)

    def test_uncertain_source_cannot_be_counted_as_another_job(self):
        source = self.document().replace('\\end{document}', self.entry('experience-freelance-unattributed') + '\n\\end{document}')
        errors, _ = self.check(source)
        self.assertTrue(any(error.startswith('E_ATTRIBUTION:') for error in errors))

    def test_explicit_owner_exclusion_is_reported(self):
        errors, report = self.check(self.document(without={'experience-aselsan'}),
                                    {'experience-aselsan': 'Owner explicitly requested AI roles only.'})
        self.assertEqual([], errors)
        row = next(item for item in report if item['id'] == 'experience-aselsan')
        self.assertEqual('excluded_by_owner', row['decision'])
        self.assertIn('Owner explicitly', row['reason'])

    def test_exclusion_without_owner_reason_is_rejected(self):
        errors, _ = self.check(self.document(without={'experience-aselsan'}), {'experience-aselsan': ''})
        self.assertTrue(any(error.startswith('E_EXCLUSION:') for error in errors))

    def test_unknown_id_is_rejected(self):
        source = self.document().replace('\\end{document}', '\\ResumeExperience{experience-unknown}{Unknown}{Role}{}{}\n\\end{document}')
        errors, _ = self.check(source)
        self.assertIn('E_ENTRY: unknown experience ID experience-unknown', errors)

    def test_nested_braces_and_escaped_ampersand_are_supported(self):
        source = self.document().replace('{ASELSAN}', '{\\textbf{ASELSAN}}')
        errors, _ = self.check(source)
        self.assertEqual([], errors)

    def test_blank_role_is_rejected(self):
        source = self.document().replace('{Process Design and Optimization Engineering Intern}', '{}')
        errors, _ = self.check(source)
        self.assertTrue(any('must display an organization and role' in error for error in errors))

    def test_malformed_entry_reports_error(self):
        source = self.document() + '\n'
        source = source.replace(self.entry('experience-aselsan'), '\\ResumeExperience{experience-aselsan}')
        errors, _ = self.check(source)
        self.assertTrue(any(error.startswith('E_ENTRY:') for error in errors))

    def test_examples_change_emphasis_while_preserving_coverage(self):
        expected_count = sum(record['verification_status'] in self.policy['experience_coverage']['eligible_statuses']
                             for record in self.records.values())
        for relative in ['cv/template.tex', 'cv/examples/ai-trainer.tex', 'cv/examples/backend-engineer.tex']:
            with self.subTest(relative=relative):
                errors, report = self.check((ROOT / relative).read_text())
                self.assertEqual([], errors)
                self.assertEqual(expected_count, sum(item['decision'] == 'included' for item in report))
        ai = (ROOT / 'cv/examples/ai-trainer.tex').read_text()
        backend = (ROOT / 'cv/examples/backend-engineer.tex').read_text()
        self.assertLess(ai.index('{experience-outlier}'), ai.index('{experience-aselsan}'))
        self.assertLess(backend.index('{experience-revloai}'), backend.index('{experience-outlier}'))

    def test_malformed_policy_reports_a_validation_error(self):
        policy = deepcopy(self.policy)
        policy['experience_coverage'] = None
        errors, _ = validate_resume_source(self.document(), self.records, policy)
        self.assertTrue(any(error.startswith('E_POLICY:') for error in errors))


if __name__ == '__main__':
    unittest.main()
