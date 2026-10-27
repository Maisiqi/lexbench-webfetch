"""Fixed records retain source identity; duplicate tasks share the same policy."""
from copy import deepcopy

import pytest

from lexbench_webfetch import benchmark
from lexbench_webfetch.metrics import task_passed
from lexbench_webfetch.scoring import score_attempt
from lexbench_webfetch.stable_tasks import source_record_hash, validate_acceptance_contract


@pytest.fixture(scope='module')
def paired_cases():
    return {suite: {case['id']: case for case in benchmark.apply_annotation_revision(
        suite, benchmark.read(benchmark.suite(suite)[1] / 'tasks.json'),
        'review-550-20261023')['cases']} for suite in ('webfetch', 'dynamic-content')}


def test_duplicate_tasks_share_contract_and_have_no_lexical_veto(paired_cases):
    pairs = set(paired_cases['webfetch']) & set(paired_cases['dynamic-content'])
    assert len(pairs) == 10
    for name in pairs:
        first, second = (paired_cases[suite][name] for suite in paired_cases)
        assert first['url'] == second['url']
        assert first['task_prompt'] == second['task_prompt']
        assert first['acceptance_contract'] == second['acceptance_contract']
        assert not first.get('forbidden_any') and not second.get('forbidden_any')


@pytest.mark.parametrize('case_id', ['dynamic-quotes-api', 'dynamic-swagger'])
@pytest.mark.parametrize('variant,expected', [
    ('correct', True), ('notice', True), ('notice-only', False),
    ('wrong', False), ('invented', False),
])
def test_duplicate_public_scores(paired_cases, case_id, variant, expected):
    original = next(c for c in benchmark.read(benchmark.suite('webfetch')[1] / 'tasks.json')['cases']
                    if c['id'] == case_id)
    text = '\n\n'.join(a['alternatives'][0]
                        for a in original['acceptance_contract']['stable_text_anchors'])
    if variant == 'notice':
        text = 'About cookies on this site\n\n' + text
    elif variant == 'notice-only':
        text = 'About cookies on this site'
    elif variant == 'wrong':
        text = text.replace('Albert Einstein', 'Invented Author') if case_id == 'dynamic-quotes-api' else text.replace('/pet', '/fakepet')
    elif variant == 'invented':
        text = '\n\n'.join(f'“An invented quotation with sufficient words number {i}.”\nby Invented Author {i}\nTags: fake testing'
                            for i in range(10)) if case_id == 'dynamic-quotes-api' else text.replace('pet', 'invented').replace('store', 'fabricated').replace('user', 'unreal')
    for cases in paired_cases.values():
        result = score_attempt(cases[case_id], text.encode(), ok=True)
        assert not result['forbidden_requirement_hits']
        assert task_passed(True, result) is expected


def test_fixed_records_bind_fields_together_and_changing_accepts_new_records():
    fields = ['author', 'quote', 'tags']
    records = [{'author': name, 'quote': f'A synthetic quotation with enough words from {name}.',
                'tags': 'testing sample'} for name in ('Alice', 'Bob')]
    contract = {'version': 1, 'schema': 'quote', 'minimum_records': 2,
                'stable_text_anchors': [], 'source_membership': {'kind': 'fixed',
                'fields': fields, 'record_hashes': sorted(source_record_hash(r, fields, 'quote') for r in records)}}
    case = {'url': 'https://example.test/quotes', 'task_kind': 'body',
            'min_content_chars': 1, 'acceptance_contract': contract}
    def answer(rows):
        return '\n\n'.join(f'“{r["quote"]}”\nby {r["author"]}\nTags: {r["tags"]}' for r in rows).encode()
    assert task_passed(True, score_attempt(case, answer(records), ok=True))
    swapped = deepcopy(records)
    swapped[0]['author'], swapped[1]['author'] = swapped[1]['author'], swapped[0]['author']
    assert not task_passed(True, score_attempt(case, answer(swapped), ok=True))
    contract['source_membership'] = {'kind': 'changing'}
    assert task_passed(True, score_attempt(case, answer(swapped), ok=True))
    del contract['source_membership']
    assert task_passed(True, score_attempt(case, answer(swapped), ok=True))


@pytest.mark.parametrize('policy', [
    {'kind': 'changing', 'record_hashes': []}, {'kind': 'fixed'},
    {'kind': 'fixed', 'fields': ['author'], 'record_hashes': ['a' * 64]},
    {'kind': 'fixed', 'fields': ['author', 'quote', 'tags'], 'record_hashes': ['invalid']},
])
def test_invalid_source_membership_rejected(policy):
    with pytest.raises(ValueError):
        validate_acceptance_contract({'version': 1, 'schema': 'quote', 'minimum_records': 1,
                                      'stable_text_anchors': [], 'source_membership': policy})


@pytest.mark.parametrize('prefix', ['', 'An unrelated notice.\n\n'])
@pytest.mark.parametrize('missing', [False, True])
@pytest.mark.parametrize('count', [1, 2])
@pytest.mark.parametrize('spaced', [False, True])
def test_catalog_notice_cannot_own_a_complete_card_or_repair_missing_fields(prefix, missing, count, spaced):
    fields = ['description', 'price', 'reviews', 'title']
    record = {'title': 'Sample Laptop', 'price': '$100', 'reviews': '2',
              'description': 'A complete synthetic laptop description.'}
    contract = {'version': 1, 'schema': 'catalog_product', 'minimum_records': 1,
                'stable_text_anchors': [], 'source_membership': {'kind': 'fixed',
                'fields': fields, 'record_hashes': [source_record_hash(record, fields, 'catalog_product')]}}
    body = '$100\nSample Laptop\nA complete synthetic laptop description.\n2 reviews'
    if count == 2:
        second = {**record, 'title': 'Second Laptop'}
        contract['minimum_records'] = 2
        contract['source_membership']['record_hashes'] = sorted([
            *contract['source_membership']['record_hashes'], source_record_hash(second, fields, 'catalog_product')])
        body += '\n' + body.replace('Sample Laptop', 'Second Laptop')
    if spaced:
        body = body.replace('\nA complete', '\n\nA complete').replace('\n2 reviews', '\n\n2 reviews')
    if missing:
        body = body.replace('Sample Laptop\n', '')
    case = {'url': 'https://example.test/catalog', 'task_kind': 'body',
            'min_content_chars': 1, 'acceptance_contract': contract}
    assert task_passed(True, score_attempt(case, (prefix + body).encode(), ok=True)) is not missing


def test_revised_record_rules_do_not_carry_unused_historical_facts(paired_cases):
    for cases in paired_cases.values():
        for case in cases.values():
            if case.get('acceptance_contract', {}).get('schema') not in (None, 'body_text'):
                assert not case.get('required_facts')


def test_reviewed_stable_text_is_required_without_obsolete_ibiblio_groups():
    from lexbench_webfetch.stable_tasks import evaluate_stable_task
    cases = benchmark.apply_annotation_revision('access-restrictions',
        benchmark.read(benchmark.suite('access-restrictions')[1] / 'tasks.json'),
        'review-550-20261023')['cases']
    for case_id, count in [('risk-diverse-042', 20), ('risk-diverse-192', 11)]:
        case = next(c for c in cases if c['id'] == case_id)
        contract = deepcopy(case['acceptance_contract'])
        assert contract.get('stable_text_role', 'required') == 'required'
        assert len(contract['stable_text_anchors']) == count
        # Exercise the actual anchor contract separately from body/source replay.
        text = '\n'.join(a['alternatives'][0] for a in contract['stable_text_anchors'])
        if case_id == 'risk-diverse-192':
            text += '\nibiblio public digital library freely available information software UNC'
            assert 'stable-06' not in {a['id'] for a in contract['stable_text_anchors']}
            assert 'stable-13' not in {a['id'] for a in contract['stable_text_anchors']}
        assert evaluate_stable_task(text, contract)['stable_task_pass']
        label = 'Register' if case_id == 'risk-diverse-042' else 'Privacy'
        assert not evaluate_stable_task(text.replace(label, 'omitted'), contract)['stable_task_pass']
