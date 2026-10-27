"""Regenerate the definition inventory in data.md; no captures or provider runs."""
from collections import Counter
from pathlib import Path
import sys

from lexbench_webfetch import benchmark
from lexbench_webfetch.stable_tasks import SCHEMA_FIELDS

REVISION = 'review-550-20261023'
START, END = '<!-- distribution:start -->', '<!-- distribution:end -->'
# One checkpoint means one declared group/region/field, not one alternative string.
ROWS = {
    'facts': ('Required facts', 'metrics.py'),
    'fact_diagnostics': ('Diagnostic historical facts', 'metrics.py'),
    'markers': ('Required legacy marker groups', 'metrics.py'),
    'anchors': ('Required stable anchors', 'stable_tasks.py'),
    'anchor_diagnostics': ('Diagnostic stable anchors', 'stable_tasks.py'),
    'regions': ('Body regions', 'body_coverage.py'),
    'endings': ('Article endings', 'body_coverage.py'),
    'ordered_endings': ('Ordered article endings', 'body_coverage.py'),
    'patterns': ('Required text patterns', 'metrics.py'),
    'page_patterns': ('Required page patterns', 'stable_tasks.py'),
    'source_pairs': ('Fixed name/URL pairs', 'stable_tasks.py'),
    'named': ('Named-link collections', 'stable_tasks.py'),
    'typed': ('Typed record/table fields', 'stable_tasks.py'),
    'groups': ('Composite groups', 'composite_tasks.py'),
    'sections': ('Document sections', 'document_structure.py'),
    'definitions': ('Definition terms', 'document_structure.py'),
    'titles': ('Article title groups', 'article_title.py'),
    'comments': ('Comment contracts', 'article_comments.py'),
    'posts': ('Post contracts', 'article_posts.py'),
    'membership': ('Fixed source record hashes', 'stable_tasks.py'),
    'resources': ('Resource groups', 'resource_urls.py'),
    'files': ('File integrity contracts', 'file_acceptance.py'),
    'length': ('Body character floors', 'metrics.py'),
    'forbidden': ('Lexical exclusion terms', 'metrics.py'),
    'identity': ('Required page identity', 'scoring.py'),
    'legacy_lists': ('Legacy list contracts', 'dynamic_lists.py'),
}


def components(case):
    """Count configured executable checks, following score_attempt/task_passed gates."""
    if case.get('rule_review', {}).get('status') == 'unresolved':
        return Counter()
    c = case.get('acceptance_contract') or {}
    schema, kind = c.get('schema'), case.get('task_kind', 'body')
    body_gate = schema == 'body_text' or (not c and kind == 'body')
    r = Counter()
    r['facts' if body_gate else 'fact_diagnostics'] = len(case.get('required_facts', []))
    r['markers'] = int(body_gate and bool(case.get('expected_any')))
    r['anchors' if c.get('stable_text_role', 'required') != 'diagnostic'
      else 'anchor_diagnostics'] = len(c.get('stable_text_anchors', []))
    body = case.get('body_requirements') or {}
    r['regions'] = len(body.get('regions', []))
    r['endings'] = int(bool(body.get('ending') or body.get('ending_reference')))
    r['ordered_endings'] = int(body.get('version') == 5)
    r['patterns'] = len(case.get('required_patterns', []))
    r['page_patterns'] = len(c.get('page_patterns', []))
    r['source_pairs'] = len(c.get('source_record_pair_hashes', []))
    r['named'] = int(schema == 'named_link')
    if schema and schema not in ('named_link', 'body_text'):
        r['typed'] = len(c.get('table_columns', [])) if schema == 'table_row' else len(SCHEMA_FIELDS[schema]) + len(c.get('field_minimum_records', {}))
    groups = (case.get('composite_acceptance') or {}).get('groups', [])
    r['groups'] = len(groups)
    for group in groups:
        r['named'] += int(group['kind'] in ('named_link', 'linked_table'))
        r['typed'] += len(group.get('required_columns', [])) + len(group.get('required_fields', [])) + int(bool(group.get('group_caption')))
    document = case.get('document_structure') or {}
    r['definitions' if document.get('type') == 'definition' else 'sections'] = len(document.get('headings', []))
    source = case.get('source_benchmark') or {}
    for row, key in [('titles', 'title_contract'), ('comments', 'comment_contract'), ('posts', 'post_contract')]:
        r[row] = int(key in source)
    r['membership'] = len(c.get('source_membership', {}).get('record_hashes', []))
    r['resources'] = len(case.get('expected_resources', [])) if kind == 'resource' else 0
    r['files'] = int(kind == 'file')
    r['length'] = int(body_gate and case.get('min_content_chars', 0) > 0)
    r['forbidden'] = len(case.get('forbidden_any', []))
    r['identity'] = int(case.get('page_identity_required', False))
    r['legacy_lists'] = int(not c and source.get('mode') == 'dynamic_list_structure')
    return +r


def datasets():
    base, revised = {}, {}
    for row in benchmark.registry()['suites']:
        suite = row['id']
        data = benchmark.read(benchmark.suite(suite)[1] / 'tasks.json')
        base[suite] = data['cases']
        revised[suite] = benchmark.apply_annotation_revision(suite, data, REVISION)['cases']
    return base, revised


def summarize(cases):
    covered, points = Counter(), Counter()
    for case in cases:
        counts = components(case)
        covered.update(counts.keys())
        points.update(counts)
    return covered, points


def cell(count, denominator):
    return f'{count} ({100 * count / denominator:.1f}%)'


def render(base, revised):
    lines = [START, '### Sample composition', '',
             'Counting unit: registered case entry; percentages use the suite row total (combined row: 550).',
             'Delivery categories partition entries. Frozen baseline and selected revision have identical composition.', '',
             '| Suite | Total | Body | Structure | Resource discovery | File delivery | Unique URLs | Unique URL + prompt tasks |',
             '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    all_cases = sum(base.values(), [])
    for suite, cases in [*base.items(), ('Combined', all_cases)]:
        kinds = Counter(c.get('task_kind', 'body') for c in cases)
        label = suite
        if suite != 'Combined':
            directory = next(r['directory'] for r in benchmark.registry()['suites'] if r['id'] == suite)
            label = f'[{suite}](../src/lexbench_webfetch/definitions/{directory}/tasks.json)'
        values = [label, str(len(cases)), *(cell(kinds[k], len(cases)) for k in ('body', 'structure', 'resource', 'file')),
                  str(len({c['url'] for c in cases})), str(len({(c['url'], c.get('task_prompt', '')) for c in cases}))]
        lines.append('| ' + ' | '.join(values) + ' |')
    owners = {}
    for suite, cases in base.items():
        for c in cases:
            owners.setdefault((c['url'], c.get('task_prompt', '')), []).append(suite)
    repeated = [v for v in owners.values() if len(set(v)) > 1]
    lines += ['', f'Across suites: **{len(repeated)} exact URL + prompt identities**, represented by **{sum(map(len, repeated))} entries** '
              f'(**{sum(len(v)-1 for v in repeated)} repeated entries**). URL-only uniqueness does not establish task equivalence; '
              'different prompts on one URL remain different tasks. Equality uses stored strings, with no URL canonicalization.', '',
              '### Scoring component matrix', '',
              'Each cell is **covered cases (percentage of suite entries); declared checkpoints**. '
              'An arrow means **frozen baseline → selected revision**; unchanged cells appear once. '
              'Components overlap and must not be added into a total case count. '
              'A zero means no executable declaration in that component, not a measured failure.', '',
              '| Component | ' + ' | '.join(base) + ' | Combined |',
              '| --- | ' + ' | '.join(['---'] * (len(base)+1)) + ' |']
    before = {k: summarize(v) for k, v in base.items()}
    after = {k: summarize(v) for k, v in revised.items()}
    before['Combined'] = summarize(all_cases)
    after['Combined'] = summarize(sum(revised.values(), []))
    sizes = {**{k: len(v) for k, v in base.items()}, 'Combined': len(all_cases)}
    for key, (label, module) in ROWS.items():
        values = [f'[{label}](../src/lexbench_webfetch/{module})']
        for suite in sizes:
            pair = []
            for counts in (before[suite], after[suite]):
                pair.append(f'{cell(counts[0][key], sizes[suite])}; {counts[1][key]}')
            values.append(pair[0] if pair[0] == pair[1] else ' → '.join(pair))
        lines.append('| ' + ' | '.join(values) + ' |')
    lines += ['', '### Threshold changes', '',
              'Values are declared thresholds across all suites (absent values excluded); '
              'changed cases include additions/removals. For more than six values, show the range and distinct-value count. '
              'Nested composite-group quotas remain in the linked per-task definitions.', '',
              '| Declaration | Baseline values | Revised values | Changed cases |',
              '| --- | --- | --- | ---: |']
    paths = [('body_requirements', 'minimum_coverage'), ('body_requirements', 'minimum_floor'),
             ('body_requirements', 'minimum_region_passes'), ('body_requirements', 'version'),
             ('acceptance_contract', 'minimum_records'), ('acceptance_contract', 'maximum_records'),
             ('acceptance_contract', 'record_count_policy', 'required_ratio'),
             ('document_structure', 'minimum_heading_coverage'),
             ('document_structure', 'minimum_body_chars'), ('document_structure', 'minimum_section_chars')]
    def value(case, path):
        for key in path:
            case = case.get(key) if isinstance(case, dict) else None
        return case
    for path in paths:
        old = [value(c, path) for c in all_cases]
        new = [value(c, path) for c in sum(revised.values(), [])]
        def distribution(values):
            counts = Counter(v for v in values if v is not None)
            if not counts:
                return 'not declared'
            if len(counts) > 6:
                return f'{min(counts)}–{max(counts)} ({len(counts)} values; {sum(counts.values())} cases)'
            return ', '.join(f'{v}: {counts[v]} cases' for v in sorted(counts))
        lines.append('| `' + '.'.join(path) + '` | ' + distribution(old) + ' | ' +
                     distribution(new) + ' | ' + str(sum(a != b for a, b in zip(old, new))) + ' |')
    for edition, data in [('Baseline', base), ('Revision', revised)]:
        pending = [(s, c['id']) for s, cases in data.items() for c in cases if c.get('rule_review', {}).get('status') == 'unresolved']
        lines += ['', f'{edition} unavailable rule declarations: {len(pending)}' +
                  (': ' + ', '.join(f'`{s}/{c}`' for s, c in pending) if pending else '.')]
    lines += ['', END]
    return '\n'.join(lines)


def update(check=False):
    base, revised = datasets()
    path = Path(__file__).with_name('data.md')
    text = path.read_text()
    start, end = text.index(START), text.index(END) + len(END)
    generated = render(base, revised)
    if check:
        if text[start:end] != generated:
            raise SystemExit('Data distribution drift: run docs/data_distribution.py --write')
    else:
        path.write_text(text[:start] + generated + text[end:])


if __name__ == '__main__':
    if sys.argv[1:] not in (['--check'], ['--write']):
        raise SystemExit('Use --check or --write')
    update(check=sys.argv[1] == '--check')
