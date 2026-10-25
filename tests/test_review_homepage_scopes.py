"""Homepage product records must belong to the main content, with mutable routes."""
import html

import pytest

from lexbench_webfetch import benchmark
from lexbench_webfetch.metrics import task_passed
from lexbench_webfetch.scoring import score_attempt


@pytest.fixture(scope='module')
def cases():
    root = benchmark.suite('popular-sites')[1]
    data = benchmark.apply_annotation_revision(
        'popular-sites', benchmark.read(root / 'tasks.json'), 'review-550-20261023')
    return {c['id']: c for c in data['cases']}


@pytest.mark.parametrize('case_id,owner,prefix', [
    ('global-homepage-042-github-com', '<main>', '/features/'),
    ('global-homepage-046-zoom-us', '<main id="main">', '/en/products/'),
    ('china-homepage-075-volcengine-com', '<main class="page">', '/product/'),
    ('china-homepage-081-elsevier-com', '<main id="main-content">', '/products/'),
])
@pytest.mark.parametrize('format,location,expected', [
    ('html', 'body', True), ('html', 'navigation', False),
    ('markdown', 'body', True), ('markdown', 'footer', False),
    ('markdown', 'missing-boundary', False),
])
def test_new_products_need_body_ownership(cases, case_id, owner, prefix,
                                         format, location, expected):
    case = cases[case_id]
    contract = case['acceptance_contract']
    scope = contract['entry_scope']
    anchors = '\n'.join(a['alternatives'][0] for a in contract['stable_text_anchors'])
    entries = [(f'New feature {i}', f'https://{contract["hosts"][0]}{prefix}future-{i}')
               for i in range(contract['minimum_records'])]
    if format == 'html':
        records = ''.join(f'<a href="{url}">{title}</a>' for title, url in entries)
        content = owner + (records if location == 'body' else '<p>Empty body.</p>') + '</main>'
        content += '<nav>' + (records if location == 'navigation' else '') + '</nav>'
        content += '<footer>' + html.escape(anchors) + '</footer>'
    else:
        records = '\n'.join(f'[{title}]({url})' for title, url in entries)
        start, end = scope['start_pattern'][1:-1], scope['end_pattern'][1:-1]
        content = start + '\n' + (records if location == 'body' else 'Empty body.')
        if location != 'missing-boundary':
            content += '\n' + end
        content += '\n' + (records if location == 'footer' else '') + '\n' + anchors
    assert task_passed(True, score_attempt(case, content.encode(), ok=True)) is expected


@pytest.mark.parametrize('owner,label', [
    ('<main class="nav-main">', 'A product'),
    ('<main id="main">', 'Explore products'),
])
def test_zoom_navigation_main_and_generic_buttons_do_not_count(cases, owner, label):
    case = cases['global-homepage-046-zoom-us']
    contract = case['acceptance_contract']
    anchors = ' '.join(a['alternatives'][0] for a in contract['stable_text_anchors'])
    records = ''.join(f'<a href="https://www.zoom.com/en/products/future-{i}/">{label}</a>'
                      for i in range(contract['minimum_records']))
    answer = owner + records + '</main><footer>' + html.escape(anchors) + '</footer>'
    assert not task_passed(True, score_attempt(case, answer.encode(), ok=True))
