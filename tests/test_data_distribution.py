"""The reader-facing inventory must agree with the registered definitions."""
import runpy
from pathlib import Path


MODULE = runpy.run_path(str(Path(__file__).parents[1] / 'docs/data_distribution.py'))


def test_distribution_totals_and_documentation_drift():
    base, revised = MODULE['datasets']()
    assert [len(v) for v in base.values()] == [150, 100, 100, 100, 100]
    assert sum(map(len, base.values())) == 550
    for suite in base:
        assert [(c['id'], c['url'], c['task_prompt'], c.get('task_kind', 'body')) for c in base[suite]] == [
            (c['id'], c['url'], c['task_prompt'], c.get('task_kind', 'body')) for c in revised[suite]]
    all_cases = sum(base.values(), [])
    assert len({c['url'] for c in all_cases}) == 535
    assert len({(c['url'], c['task_prompt']) for c in all_cases}) == 540
    doc = (Path(__file__).parents[1] / 'docs/data.md').read_text()
    actual = doc[doc.index(MODULE['START']):doc.index(MODULE['END']) + len(MODULE['END'])]
    assert actual == MODULE['render'](base, revised)


def test_counts_distinguish_optional_anchors_unavailable_and_field_groups():
    count = MODULE['components']
    case = {'acceptance_contract': {'schema': 'body_text', 'stable_text_role': 'diagnostic',
                                   'stable_text_anchors': [{'alternatives': ['A', 'B']}]},
            'body_requirements': {'version': 5, 'regions': [{}, {}], 'ending': {'text': 'end'}}}
    result = count(case)
    assert result['anchor_diagnostics'] == 1 and result['anchors'] == 0
    assert result['regions'] == 2 and result['ordered_endings'] == 1
    case['rule_review'] = {'status': 'unresolved'}
    assert not count(case)
    result = count({'composite_acceptance': {'groups': [{'kind': 'linked_table',
        'required_columns': [{}, {}], 'required_fields': [{}], 'group_caption': {'field': {}}}]}})
    assert result['named'] == 1 and result['typed'] == 4 and result['groups'] == 1
