"""Behavior checks for evidence, date, reference and privacy failures."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate import validate_repository


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__', 'build'))
        self.addCleanup(self.temp.cleanup)

    def errors(self):
        return validate_repository(self.root)[0]

    def change_yaml(self, relative, change):
        path = self.root / relative
        obj = yaml.safe_load(path.read_text())
        change(obj)
        path.write_text(yaml.safe_dump(obj, sort_keys=False))

    def change_record(self, relative, change):
        path = self.root / relative
        front, body = path.read_text()[4:].split('\n---\n', 1)
        obj = yaml.safe_load(front)
        change(obj)
        path.write_text('---\n' + yaml.safe_dump(obj, sort_keys=False) + '---\n' + body)

    def assert_code(self, code):
        self.assertTrue(any(e.startswith(code + ' ') for e in self.errors()), self.errors())

    def test_current_repository_passes(self):
        self.assertEqual([], self.errors())

    def test_duplicate_yaml_keys_are_rejected(self):
        path = self.root / 'profile.yaml'
        path.write_text(path.read_text() + '\nname: another value\n')
        self.assert_code('E_YAML')

    def test_missing_record_identifier_is_rejected(self):
        self.change_yaml('profile.yaml', lambda obj: obj.pop('id'))
        self.assert_code('E_ID')

    def test_duplicate_record_identifier_is_rejected(self):
        self.change_record('projects/saferoads.md', lambda obj: obj.update(id='project-slime-hunter'))
        self.assert_code('E_ID')

    def test_unresolved_skill_evidence_is_rejected(self):
        self.change_yaml('skills.yaml', lambda obj: obj['skills'][0]['evidence_refs'].append('claim-nonexistent'))
        self.assert_code('E_REFERENCE')

    def test_profile_cannot_hide_a_background_experience(self):
        self.change_yaml('profile.yaml', lambda obj: obj['experience_refs'].remove('experience-content-creation'))
        self.assert_code('E_COVERAGE')

    def test_repository_examples_cannot_omit_aselsan(self):
        path = self.root / 'cv/examples/ai-trainer.tex'
        path.write_text(path.read_text().replace('\\ResumeExperience{experience-aselsan}', '\\ResumeEntry'))
        self.assert_code('E_RESUME')

    def test_listed_skill_cannot_be_upgraded_without_task_evidence(self):
        self.change_yaml('skills.yaml', lambda obj: obj['skills'][0].update(verification_status='source_supported'))
        self.assert_code('E_EVIDENCE')

    def test_invalid_month_is_rejected(self):
        self.change_record('experience/aselsan.md', lambda obj: obj.update(start_date='2026-13'))
        self.assert_code('E_DATE')

    def test_reversed_dates_are_rejected(self):
        self.change_record('experience/aselsan.md', lambda obj: obj.update(start_date='2026-09'))
        self.assert_code('E_DATE')

    def test_confirmed_placeholder_is_rejected(self):
        self.change_record('experience/aselsan.md', lambda obj: obj['claims'][0].update(text='TODO confirm employer'))
        self.assert_code('E_PLACEHOLDER')

    def test_broken_local_link_is_rejected(self):
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n[Missing record](experience/does-not-exist.md)\n')
        self.assert_code('E_LINK')

    def test_personal_email_is_rejected_without_echoing_value(self):
        value = 'private-person' + '@' + 'example.test'
        (self.root / 'accidental.txt').write_text(value)
        errors = self.errors()
        self.assertTrue(any(e.startswith('E_PRIVACY ') for e in errors))
        self.assertFalse(any(value in e for e in errors))

    def test_private_source_artifacts_are_rejected(self):
        (self.root / 'accidental.pdf').write_bytes(b'%PDF-test')
        self.assert_code('E_PRIVACY')

    def test_remote_tex_input_is_rejected(self):
        with (self.root / 'cv/template.tex').open('a') as stream:
            stream.write('\n' + '\\input{' + 'https://example.test/untrusted.tex}\n')
        self.assert_code('E_TEX')


if __name__ == '__main__':
    unittest.main()
