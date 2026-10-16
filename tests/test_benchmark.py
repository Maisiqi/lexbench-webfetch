"""Input contracts: complete versions export; corrupt, partial or unsafe inputs fail."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from lexbench_webfetch import benchmark as bench


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    return bench.digest(path)


class PublicDefinitions(unittest.TestCase):
    def test_all_shipped_suites_are_consistent(self):
        rows = [bench.validate(row['id']) for row in bench.registry()['suites']]
        self.assertEqual(len(rows), 4)
        self.assertEqual(sum(row['case_count'] for row in rows), 450)

    def test_nested_reference_bodies_are_bound_without_being_distributed(self):
        body = 'Third-party reference paragraph. ' * 400
        source = 'Captured source lines. ' * 300
        case = {'id': 'article', 'body_requirements': {
            'regions': [{'id': 'main', 'text': body, 'source_text': source,
                         'min_coverage': 0.9}], 'min_region_coverage': 0.8}}
        public = bench.public_task(case)
        encoded = json.dumps(public)
        self.assertNotIn(body, encoded)
        self.assertNotIn(source, encoded)
        region = public['body_requirements']['regions'][0]
        self.assertEqual(region['text_binding'], {
            'sha256': hashlib.sha256(body.encode()).hexdigest(), 'chars': len(body)})
        self.assertEqual(region['min_coverage'], 0.9)
        self.assertEqual(public['body_requirements']['min_region_coverage'], 0.8)
        self.assertEqual(case['body_requirements']['regions'][0]['text'], body)

    def test_unknown_suite_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unknown suite'):
            bench.validate('not-a-suite')


class FrozenInputs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.suites = self.root / 'suites'
        self.source = self.root / 'source'
        suite = self.suites / 'synthetic'
        case = {'id': 'article', 'name': 'Article', 'url': 'https://example.test',
                'category': 'web', 'task_prompt': 'Return the article',
                'expected_any': ['unique fact'], 'ground_truth_main_content': 'unique fact'}
        data = {'id': 'test', 'name': 'Test', 'cases': [case]}
        sha = write(self.source / 'dataset.json', data)
        ref_sha = write(self.source / 'sources/article.json', {'reference': 'unique fact'})
        definition = hashlib.sha256(json.dumps(case, ensure_ascii=False, sort_keys=True,
                                               separators=(',', ':')).encode()).hexdigest()
        catalog_sha = write(suite / 'dataset-catalog.json', {
            'id': 'test', 'name': 'Test', 'case_count': 1, 'dataset_sha256': sha,
            'cases': [{'id': 'article', 'name': 'Article', 'url': 'https://example.test',
                       'definition_sha256': definition}]})
        write(suite / 'tasks.json', {'id': 'test', 'cases': [{k: v for k, v in case.items()
                                                          if k != 'ground_truth_main_content'}]})
        write(suite / 'source-inputs.json', {
            'schema_version': 2, 'kind': 'frozen_reference_inputs',
            'catalog_sha256': catalog_sha, 'dataset_sha256': sha, 'dataset': 'dataset.json',
            'files': {'dataset.json': sha}, 'trees': {'sources': {'article.json': ref_sha}}})
        self.bind_registry()
        self.patch = patch.object(bench, 'SUITES', self.suites)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def bind_registry(self):
        suite = self.suites / 'synthetic'
        write(self.suites / 'registry.json', {'schema_version': 1, 'suites': [{
            'id': 'synthetic', 'dataset_id': 'test', 'case_count': 1,
            'files': {p.name: bench.digest(p) for p in suite.iterdir()}}]})

    def test_complete_inputs_export_without_private_extras(self):
        (self.source / 'private.log').write_text('not public')
        output = self.root / 'export'
        result = bench.export('synthetic', self.source, output)
        self.assertEqual(result, output / 'dataset.json')
        self.assertEqual({p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()},
                         {'dataset.json', 'sources/article.json'})
        self.assertEqual(bench.verify_inputs('synthetic', output)['case_count'], 1)

    def test_existing_output_is_preserved(self):
        output = self.root / 'existing'
        output.mkdir()
        marker = output / 'saved'
        marker.write_text('evidence')
        with self.assertRaisesRegex(ValueError, 'new directory'):
            bench.export('synthetic', self.source, output)
        self.assertEqual(marker.read_text(), 'evidence')

    def test_missing_and_changed_inputs_fail_without_export(self):
        target = self.source / 'sources/article.json'
        original = target.read_bytes()
        for replacement in (None, b'changed'):
            with self.subTest(replacement=replacement):
                if replacement is None:
                    target.unlink()
                else:
                    target.write_bytes(replacement)
                with self.assertRaises((OSError, ValueError)):
                    bench.export('synthetic', self.source, self.root / 'output')
                self.assertFalse((self.root / 'output').exists())
                target.write_bytes(original)

    def test_symlinked_input_is_rejected(self):
        target = self.source / 'sources/article.json'
        outside = self.root / 'outside.json'
        target.rename(outside)
        target.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'Symlinked'):
            bench.verify_inputs('synthetic', self.source)

    def test_public_acceptance_cannot_differ_from_frozen_task(self):
        path = self.suites / 'synthetic/tasks.json'
        data = bench.read(path)
        data['cases'][0]['expected_any'] = ['easier requirement']
        write(path, data)
        self.bind_registry()
        with self.assertRaisesRegex(ValueError, 'Public task differs'):
            bench.verify_inputs('synthetic', self.source)

    def test_omitting_an_acceptance_requirement_is_rejected(self):
        path = self.suites / 'synthetic/tasks.json'
        data = bench.read(path)
        del data['cases'][0]['expected_any']
        write(path, data)
        self.bind_registry()
        with self.assertRaisesRegex(ValueError, 'Public task differs'):
            bench.verify_inputs('synthetic', self.source)

    def test_task_removal_and_reordering_are_rejected(self):
        path = self.suites / 'synthetic/tasks.json'
        write(path, {'id': 'test', 'cases': []})
        self.bind_registry()
        with self.assertRaisesRegex(ValueError, 'inventory'):
            bench.validate('synthetic')

    def test_changed_shipped_file_fails(self):
        (self.suites / 'synthetic/tasks.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Changed suite file'):
            bench.validate('synthetic')

    def test_escaping_paths_are_rejected(self):
        for value in ('../secret', '/absolute', 'sources/../../secret', 'sources\\secret'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                bench.bound_path(self.source, value)


if __name__ == '__main__':
    unittest.main()
