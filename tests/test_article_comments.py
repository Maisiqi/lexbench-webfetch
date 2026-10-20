"""Initial comments must preserve attribution, multiplicity and reply ownership."""
from copy import deepcopy

import pytest

from lexbench_webfetch.article_comments import (qualify_article_comments, validate_comment_contract,
                                               verify_article_comments)


CONTRACT = {'version': 1, 'record_selector': '.comment', 'author_selector': '.author',
            'body_selector': '.text', 'section_markers': ['Comments', '评论'],
            'max_reference_age_seconds': 900}
BODY = 'The reviewer carefully compares the original text with the revised translation.'
REPLY = 'The second edition restores the missing paragraph and explains the editorial decision.'
CONTEXT = {'id': 'run-one', 'started_at': '2026-10-20T01:01:00Z'}
REFERENCE = {'version': 1, 'case_id': 'article', 'url': 'https://example.test/article',
             'scope': 'initial_load_only', 'observation_complete': True,
             'context_id': 'run-one', 'observed_at': '2026-10-20T01:00:00Z',
             'source_observation_counts': [2, 2], 'records': [
                 {'id': 'c1', 'author': 'Alice', 'text': BODY, 'parent_id': None,
                  'complete_initial_text': True},
                 {'id': 'c2', 'author': 'Bob', 'text': REPLY, 'parent_id': 'c1',
                  'complete_initial_text': True}]}


def check(content, reference=REFERENCE, context=CONTEXT):
    return verify_article_comments(content, CONTRACT, reference,
                                   case_id='article', url=REFERENCE['url'], reference_context=context)


def html(body=BODY, reply=REPLY):
    return ('<h1>Article</h1><div class="comment" id="c1"><span class="author">Alice</span>'
            '<div class="text">' + body + '<div class="comment" id="c2">'
            '<span class="author">Bob</span><div class="text">' + reply + '</div></div></div></div>')


def markdown(body=BODY, reply=REPLY):
    return '# Article\n\n## Comments\n\n### Alice\n\n' + body + '\n\n#### Bob\n\n' + reply


@pytest.mark.parametrize('content', [html(), markdown()])
def test_complete_owned_comments_pass(content):
    assert check(content)['article_comments_pass']
    assert check(content)['article_comment_confirmed_count'] == 2


@pytest.mark.parametrize('content', [html(body=''), html(reply=''),
                                     html(body='', reply=BODY + REPLY),
                                     markdown(body=''), markdown(reply=''),
                                     markdown().replace('#### Bob', '### Bob'),
                                     html().replace('>Bob<', '>Charlie<'),
                                     markdown().replace('### Alice', '### Charlie'),
                                     html().replace('id="c2"', 'id="wrong"'),
                                     '# Article\n' + BODY + '\n' + REPLY,
                                     '```html\n' + html() + '\n```',
                                     '<script>' + html() + '</script>',
                                     '<div hidden>' + html() + '</div>'])
def test_missing_swapped_hidden_or_unowned_comments_fail(content):
    assert not check(content)['article_comments_pass']


def test_simple_plain_author_records_do_not_need_synthetic_ids():
    ref = deepcopy(REFERENCE)
    ref['records'][1]['parent_id'] = None
    text = 'Article\n\nComments\n\nAlice:\n' + BODY + '\n\nBob:\n' + REPLY
    assert check(text, ref)['article_comments_pass']
    assert not check(text, REFERENCE)['article_comments_pass']


def test_repeated_comments_need_multiplicity():
    ref = deepcopy(REFERENCE)
    ref['records'][1].update(author='Alice', text=BODY, parent_id=None)
    text = '## Comments\n\n### Alice\n' + BODY
    assert not check(text, ref)['article_comments_pass']
    assert check(text + '\n\n### Alice\n' + BODY, ref)['article_comments_pass']


def test_deleted_placeholder_and_short_comment_are_real_content():
    ref = deepcopy(REFERENCE)
    ref['records'][0]['text'] = '[deleted]'
    ref['records'][1]['text'] = '好'
    assert check(markdown(body='[deleted]', reply='好'), ref)['article_comments_pass']
    assert not check(markdown(body='', reply='好'), ref)['article_comments_pass']


@pytest.mark.parametrize('change,status', [
    ({'case_id': 'other'}, 'invalid'), ({'url': 'https://other.test/'}, 'invalid'),
    ({'observation_complete': False}, 'invalid'), ({'scope': 'all_pages'}, 'invalid'),
    ({'source_observation_counts': [2, 3]}, 'invalid'),
    ({'observed_at': '2026-10-20T00:00:00Z'}, 'stale'),
    ({'observed_at': '2026-10-20T02:00:00Z'}, 'context_mismatch'),
])
def test_independent_reference_boundary(change, status):
    ref = deepcopy(REFERENCE)
    ref.update(change)
    result = check(html(), ref)
    assert result['article_comments_reference_status'] == status
    assert not result['article_comments_pass']
    assert result['article_comment_results'] == []


def test_missing_context_and_missing_reference_are_unavailable():
    assert check(html(), None)['article_comments_reference_status'] == 'missing'
    assert check(html(), context=None)['article_comments_reference_status'] == 'context_mismatch'
    assert check(html(), context={'id': 'different', 'started_at': CONTEXT['started_at']})['article_comments_reference_status'] == 'context_mismatch'


def test_observed_zero_requires_complete_zero_observations():
    ref = deepcopy(REFERENCE)
    ref.update(records=[], source_observation_counts=[0, 0])
    assert check('# Article\nNo displayed comments.', ref)['article_comments_pass']
    assert not check(html(), ref)['article_comments_pass']
    ref['source_observation_counts'] = [1, 0]
    assert check('', ref)['article_comments_reference_status'] == 'invalid'


@pytest.mark.parametrize('bad', [
    {'max_reference_age_seconds': 901}, {'max_reference_age_seconds': float('inf')},
    {'record_selector': ''}, {'author_selector': '['}, {'section_markers': []},
    {'id_attribute': 'id]'}, {'version': True}, {'unknown': 'field'},
])
def test_invalid_contracts_are_rejected(bad):
    with pytest.raises(ValueError):
        validate_comment_contract({**CONTRACT, **bad})


def test_invalid_parent_duplicate_and_incomplete_reference_rejected():
    for mutate in ('parent', 'duplicate', 'incomplete'):
        ref = deepcopy(REFERENCE)
        if mutate == 'parent':
            ref['records'][1]['parent_id'] = 'missing'
        elif mutate == 'duplicate':
            ref['records'][1]['id'] = 'c1'
        else:
            ref['records'][0]['complete_initial_text'] = False
        assert check(html(), ref)['article_comments_reference_status'] == 'invalid'


def test_identical_parent_records_are_disambiguated_by_owned_replies():
    ref = deepcopy(REFERENCE)
    ref['records'].append({**ref['records'][0], 'id': 'c3'})
    ref['records'].append({**ref['records'][1], 'id': 'c4', 'text': BODY, 'parent_id': 'c3'})
    ref['source_observation_counts'] = [4, 4]
    text = ('## Comments\n### Alice\n' + BODY + '\n#### Bob\n' + BODY
            + '\n### Alice\n' + BODY + '\n#### Bob\n' + REPLY)
    assert check(text, ref)['article_comments_pass']


def test_symbol_only_comment_is_not_an_empty_comment():
    ref = deepcopy(REFERENCE)
    ref['records'][1]['text'] = '👍👍'
    assert check(markdown(reply='👍👍'), ref)['article_comments_pass']
    assert not check(markdown(reply=''), ref)['article_comments_pass']


def test_plain_bare_authors_use_separate_comment_paragraph_boundaries():
    ref = deepcopy(REFERENCE)
    ref['records'][1]['parent_id'] = None
    text = 'Article\n\nComments\n\nAlice\n' + BODY + '\n\nBob\n' + REPLY
    assert check(text, ref)['article_comments_pass']
    assert not check('Article\n\nAlice\n' + BODY + '\n\nBob\n' + REPLY, ref)['article_comments_pass']


def empty_parent_reference():
    ref = deepcopy(REFERENCE)
    ref['records'][0].update(text='', empty_body=True)
    return ref


@pytest.mark.parametrize('content', [
    html(body='<img alt="smiling face" src="emoji.png">'),
    markdown(body=''),
    markdown(body='![smiling face](emoji.png)'),
    markdown(body='[![smiling face](emoji.png)](https://example.test/image)'),
])
def test_explicit_image_only_parent_owns_nonempty_initial_replies(content):
    result = check(content, empty_parent_reference())
    assert result['article_comments_reference_status'] == 'verified'
    assert result['article_comments_pass']


def test_empty_parent_cannot_excuse_omitted_prose_or_invent_image_words():
    ref = empty_parent_reference()
    assert not check(html(body='Actual original prose.'), ref)['article_comments_pass']
    assert not check(markdown(body='smiling face'), ref)['article_comments_pass']
    ref['records'][0]['text'] = 'Original nonempty prose.'
    assert check(html(), ref)['article_comments_reference_status'] == 'invalid'
    ref['records'][0]['text'] = ' '
    assert check(html(), ref)['article_comments_reference_status'] == 'invalid'


def test_empty_parent_requires_explicit_observation_and_nonempty_descendant():
    ref = empty_parent_reference()
    del ref['records'][0]['empty_body']
    assert check(markdown(body=''), ref)['article_comments_reference_status'] == 'invalid'
    ref = empty_parent_reference()
    ref['records'] = ref['records'][:1]
    ref['source_observation_counts'] = [1, 1]
    assert check(markdown(body='', reply=''), ref)['article_comments_reference_status'] == 'invalid'
    ref = empty_parent_reference()
    ref['records'][1].update(text='', empty_body=True)
    assert check(markdown(body='', reply=''), ref)['article_comments_reference_status'] == 'invalid'


def test_visible_replies_without_their_empty_parent_fail():
    ref = empty_parent_reference()
    candidate = '<div class="comment" id="c2"><span class="author">Bob</span><div class="text">' + REPLY + '</div></div>'
    assert not check(candidate, ref)['article_comments_pass']
    assert not check('## Comments\n### Bob\n' + REPLY, ref)['article_comments_pass']


def test_empty_parent_may_own_nonempty_grandchild_through_empty_child():
    ref = empty_parent_reference()
    ref['records'][1].update(text='', empty_body=True)
    ref['records'].append({'id': 'c3', 'author': 'Carol', 'text': BODY,
                           'parent_id': 'c2', 'complete_initial_text': True})
    ref['source_observation_counts'] = [3, 3]
    text = '## Comments\n### Alice\n\n#### Bob\n\n##### Carol\n' + BODY
    assert check(text, ref)['article_comments_pass']



def zero_comment_reference():
    ref = deepcopy(REFERENCE)
    ref.update(records=[], source_observation_counts=[0, 0])
    return ref


@pytest.mark.parametrize('markup', [
    '<details class="open-all-comments"><summary>Show all comments</summary>' + html() + '</details>',
    '<details><details open>' + html() + '</details></details>',
])
def test_closed_details_do_not_expose_comments_for_initial_load(markup):
    zero = check(markup, zero_comment_reference())
    assert zero['article_comments_pass']
    assert zero['article_comment_count'] == 0
    assert not check(markup)['article_comments_pass']


def test_open_details_keep_all_owned_comments():
    assert check('<details open><summary>Comments</summary>' + html() + '</details>')['article_comments_pass']


def test_closed_details_inside_body_cannot_supply_missing_comment_prose():
    hidden = '<details><summary>Show more</summary>' + BODY + '</details>'
    assert not check(html(body=hidden))['article_comments_pass']
    assert check(html(body='<details open><summary>Show more</summary>' + BODY + '</details>'))['article_comments_pass']


def test_closed_details_summary_text_still_renders():
    body = '<details><summary>' + BODY + '</summary>Hidden extra prose.</details>'
    assert check(html(body=body))['article_comments_pass']
    hidden_summary = '<details><summary>Show more</summary><summary>' + BODY + '</summary></details>'
    assert not check(html(body=hidden_summary))['article_comments_pass']


def test_markdown_with_closed_html_details_cannot_supply_comment_records():
    markup = '# Article\n\n<details><summary>Show comments</summary>\n' + markdown() + '\n</details>'
    assert check(markup, zero_comment_reference())['article_comments_pass']
    assert not check(markup)['article_comments_pass']



ABSENT_CONTRACT = {'version': 1, 'mode': 'observed_absent', 'max_reference_age_seconds': 900}


def check_absent(content, reference, context=CONTEXT):
    return verify_article_comments(content, ABSENT_CONTRACT, reference,
                                   case_id='article', url=REFERENCE['url'], reference_context=context)


@pytest.mark.parametrize('content', [
    '# Article\nReaders can submit Comments through the contact form.',
    '<h1>Article</h1><p>Comments welcome by email.</p>',
    '# Comments\n## Contact us\nMarketing copy describing our product.',
])
def test_independently_absent_comment_component_needs_no_invented_selectors(content):
    validate_comment_contract(ABSENT_CONTRACT)
    result = check_absent(content, zero_comment_reference())
    assert result['article_comments_reference_status'] == 'verified'
    assert result['article_comments_pass']
    assert result['article_comment_results'] == []
    assert result['article_comment_count'] == 0
    assert result['article_comments_reference_sha256']


def test_newly_appeared_comments_require_new_reviewed_layout():
    for content in ('Article body alone.', html()):
        result = check_absent(content, REFERENCE)
        assert result['article_comments_reference_status'] == 'unsupported_layout'
        assert not result['article_comments_pass']
        assert result['article_comment_results'] == []


@pytest.mark.parametrize('change,status', [
    ({'case_id': 'different'}, 'invalid'),
    ({'source_observation_counts': [2, 0]}, 'invalid'),
    ({'observation_complete': False}, 'invalid'),
    ({'observed_at': '2026-10-20T00:00:00Z'}, 'stale'),
    ({'observed_at': '2026-10-20T02:00:00Z'}, 'context_mismatch'),
])
def test_absent_component_still_requires_current_complete_independent_observation(change, status):
    ref = zero_comment_reference()
    ref.update(change)
    result = check_absent('Article', ref)
    assert result['article_comments_reference_status'] == status
    assert not result['article_comments_pass']


def test_absent_component_never_passes_without_reference_or_run_context():
    assert check_absent('Article', None)['article_comments_reference_status'] == 'missing'
    assert check_absent('Article', zero_comment_reference(), None)['article_comments_reference_status'] == 'context_mismatch'
    assert check_absent('Article', zero_comment_reference(), {'id': 'other', 'started_at': CONTEXT['started_at']})['article_comments_reference_status'] == 'context_mismatch'


@pytest.mark.parametrize('contract', [
    {**ABSENT_CONTRACT, 'record_selector': '.invented-comments'},
    {**ABSENT_CONTRACT, 'section_markers': ['Comments']},
    {**ABSENT_CONTRACT, 'max_reference_age_seconds': 901},
    {**ABSENT_CONTRACT, 'max_reference_age_seconds': True},
    {**CONTRACT, 'mode': 'unknown'},
])
def test_absent_component_contract_is_narrow_and_validated(contract):
    with pytest.raises(ValueError):
        validate_comment_contract(contract)



@pytest.mark.parametrize('section', ['Top comments (189)', 'Top comments (0)',
                                     'Top comments (300)', '全部讨论（47）', '全部讨论（999）'])
def test_comment_section_ignores_only_its_changing_trailing_numeric_count(section):
    contract = {**CONTRACT, 'section_markers': ['Top comments', '全部讨论']}
    text = markdown().replace('Comments', section)
    result = verify_article_comments(text, contract, REFERENCE,
                                    case_id='article', url=REFERENCE['url'], reference_context=CONTEXT)
    assert result['article_comments_pass']


@pytest.mark.parametrize('section', ['Hot comments (189)', 'Top comments (many)',
                                     'All discussions（47）', 'Top comments (189) more'])
def test_count_normalization_cannot_match_unrelated_comment_section(section):
    contract = {**CONTRACT, 'section_markers': ['Top comments', '全部讨论']}
    text = markdown().replace('Comments', section)
    result = verify_article_comments(text, contract, REFERENCE,
                                    case_id='article', url=REFERENCE['url'], reference_context=CONTEXT)
    assert not result['article_comments_pass']


def test_count_normalization_does_not_change_author_or_short_comment_body():
    ref = deepcopy(REFERENCE)
    ref['records'][0]['author'] = 'Alice (189)'
    ref['records'][1]['text'] = '42 (9)'
    assert check(markdown().replace('Alice', 'Alice (189)').replace(REPLY, '42 (9)'), ref)['article_comments_pass']
    assert not check(markdown().replace(REPLY, '42'), ref)['article_comments_pass']


PINGBACK_SOURCE = 'Weekly writing links'
PINGBACK_TEXT = 'Pingback: ' + PINGBACK_SOURCE
PINGBACK_CONTRACT = {**CONTRACT, 'author_selector': 'a.url'}


def pingback_reference():
    ref = deepcopy(REFERENCE)
    ref['source_observation_counts'] = [1, 1]
    ref['records'] = [{'id': 'pingback-1', 'author': PINGBACK_SOURCE,
                       'text': PINGBACK_TEXT, 'parent_id': None, 'complete_initial_text': True}]
    return ref


def check_pingback(content):
    return verify_article_comments(content, PINGBACK_CONTRACT, pingback_reference(),
                                   case_id='article', url=REFERENCE['url'], reference_context=CONTEXT)


def pingback_html(author=PINGBACK_SOURCE, body=PINGBACK_TEXT):
    return ('<h1>Article</h1><div class="comment" id="pingback-1">'
            '<a class="url" href="https://source.test/post">' + author + '</a>'
            '<div class="text">' + body + '</div></div>')


@pytest.mark.parametrize('content', [
    pingback_html(),
    '<h1>Article</h1><div class="comment" id="pingback-1"><div class="text">Pingback: <a class="url" href="https://source.test/post">Weekly writing links</a></div></div>',
    '# Article\n\n## Comments\nPingback: [Weekly writing links](https://source.test/post)',
    'Article\n\nComments\nPingback: Weekly writing links',
])
def test_natural_pingback_lines_use_actual_linked_source_identity(content):
    assert check_pingback(content)['article_comments_pass']


@pytest.mark.parametrize('content', [
    pingback_html(author='Different source'),
    pingback_html(body='Unrelated text about another topic.'),
    '# Article\n## Comments\nPingback: [Different source](https://source.test/other)',
    '# Article\n## Comments\nPingback: [Weekly writing links](https://source.test/post) unrelated tail',
    '# Article\n## Comments\nNo displayed pingback.',
    '# Article\nPingback: [Weekly writing links](https://source.test/post)',
    '# Article\n## Comments\nPingback: Weekly writing links\nPingback: Weekly writing links',
    '# Article\n## Comments\nTrackback: Weekly writing links',
])
def test_natural_pingback_missing_duplicate_wrong_source_or_unowned_text_fails(content):
    assert not check_pingback(content)['article_comments_pass']



def image_leaf_reference():
    ref = zero_comment_reference()
    ref['records'] = [
        {'id': '425798490', 'author': 'neng', 'parent_id': None, 'text': '',
         'complete_initial_text': True, 'empty_body': True, 'image_only': True, 'source_media_count': 1},
        {'id': '425815302', 'author': 'SHUANGer2021', 'parent_id': None, 'text': '',
         'complete_initial_text': True, 'empty_body': True, 'image_only': True, 'source_media_count': 2},
        {'id': '425791579', 'author': 'JimmyYen', 'parent_id': None, 'text': '',
         'complete_initial_text': True, 'empty_body': True, 'image_only': True, 'source_media_count': 1},
    ]
    ref['source_observation_counts'] = [3, 3]
    return ref


def image_leaf_html():
    return ''.join('<div class="comment" id="' + row['id'] + '"><span class="author">'
                   + row['author'] + '</span><div class="text"><img alt="smiling face" src="emoji.png"></div></div>'
                   for row in image_leaf_reference()['records'])


@pytest.mark.parametrize('content', [
    image_leaf_html(),
    '## Comments\n### neng\n![smiling face](emoji.png)\n### SHUANGer2021\n![smiling face](emoji.png)\n### JimmyYen\n![smiling face](emoji.png)',
    '## Comments\n### neng\n\n### SHUANGer2021\n\n### JimmyYen',
])
def test_independently_observed_image_only_leaves_preserve_authors_without_ocr(content):
    result = check(content, image_leaf_reference())
    assert result['article_comments_reference_status'] == 'verified'
    assert result['article_comments_pass']
    assert result['article_comment_confirmed_count'] == 3


@pytest.mark.parametrize('change', [
    {'image_only': False}, {'image_only': None}, {'source_media_count': 0},
    {'source_media_count': -1}, {'source_media_count': True}, {'source_media_count': 1.5},
    {'source_media_count': '1'}, {'empty_body': False}, {'text': 'Hidden original prose.'},
])
def test_image_only_leaf_cannot_forge_empty_or_media_evidence(change):
    ref = image_leaf_reference()
    ref['records'][0].update(change)
    assert check(image_leaf_html(), ref)['article_comments_reference_status'] == 'invalid'


@pytest.mark.parametrize('missing', ['image_only', 'source_media_count', 'empty_body'])
def test_image_only_leaf_requires_all_explicit_source_evidence(missing):
    ref = image_leaf_reference()
    del ref['records'][0][missing]
    assert check(image_leaf_html(), ref)['article_comments_reference_status'] == 'invalid'


def test_image_only_leaf_authorship_and_empty_owned_body_are_still_required():
    ref = image_leaf_reference()
    assert not check(image_leaf_html().replace('>neng<', '>someone else<'), ref)['article_comments_pass']
    assert not check(image_leaf_html().replace('<img alt="smiling face" src="emoji.png">', 'smiling face', 1), ref)['article_comments_pass']
    assert not check(image_leaf_html().split('</div></div>', 1)[1], ref)['article_comments_pass']



@pytest.mark.parametrize('author', ['????', '👍', '👩\u200d💻', '！！！'])
def test_literal_symbol_only_author_identity_is_valid_and_distinct(author):
    ref = deepcopy(REFERENCE)
    ref['records'][0]['author'] = author
    assert check(html().replace('>Alice<', '>' + author + '<'), ref)['article_comments_pass']
    assert check(markdown().replace('### Alice', '### ' + author), ref)['article_comments_pass']
    assert not check(html().replace('>Alice<', '>different person<'), ref)['article_comments_pass']
    assert not check(markdown().replace('### Alice', '### 😐'), ref)['article_comments_pass']


def test_symbol_author_punctuation_is_not_empty_token_identity():
    ref = deepcopy(REFERENCE)
    ref['records'][0]['author'] = '????'
    assert not check(html().replace('>Alice<', '>!!!!<'), ref)['article_comments_pass']
    assert not check(markdown().replace('### Alice', '### !!!!'), ref)['article_comments_pass']
    ref['records'][1]['parent_id'] = None
    plain = 'Comments\n\n????\n' + BODY + '\n\nBob\n' + REPLY
    assert check(plain, ref)['article_comments_pass']
    assert check(plain.replace('????\n', '????:\n'), ref)['article_comments_pass']
    assert not check(plain.replace('????', '!!!!'), ref)['article_comments_pass']


@pytest.mark.parametrize('author', ['', '   ', '\u200b', '\ufeff', '\u200c\u200d', '\u200b \ufeff\t', '\x00'])
def test_whitespace_or_only_invisible_characters_cannot_be_reference_author(author):
    ref = deepcopy(REFERENCE)
    ref['records'][0]['author'] = author
    assert check(html(), ref)['article_comments_reference_status'] == 'invalid'


def test_emoji_joiner_identity_is_not_silently_flattened():
    ref = deepcopy(REFERENCE)
    ref['records'][0]['author'] = '👩\u200d💻'
    assert check(html().replace('>Alice<', '>👩\u200d💻<'), ref)['article_comments_pass']
    assert not check(html().replace('>Alice<', '>👩💻<'), ref)['article_comments_pass']



def test_natural_comment_body_headings_do_not_become_invented_authors():
    candidate = markdown(body=BODY + '\n\n### Explanation\n\n' + BODY,
                         reply=REPLY + '\n\n##### Translation notes\n\n' + REPLY)
    assert check(candidate)['article_comments_pass']
    assert check(candidate)['article_comment_count'] == 2


def test_quoted_or_fenced_section_and_article_body_mentions_do_not_supply_comments():
    assert not check('> ' + markdown().replace('\n', '\n> '))['article_comments_pass']
    assert not check('```markdown\n' + markdown() + '\n```')['article_comments_pass']
    candidate = '# Article\nBob wrote: ' + REPLY + '\n\n## Comments\n### Alice\n' + BODY
    assert not check(candidate)['article_comments_pass']


def test_large_ambiguous_sibling_sets_use_cached_body_comparisons(monkeypatch):
    import lexbench_webfetch.article_comments as comments
    original, calls = comments._body_matches, []
    def counted(actual, expected):
        calls.append((actual, expected))
        return original(actual, expected)
    monkeypatch.setattr(comments, '_body_matches', counted)
    ref = deepcopy(REFERENCE)
    ref['records'] = [{'id': str(i), 'author': 'Same', 'text': 'same text',
                       'parent_id': None, 'complete_initial_text': True} for i in range(255)]
    ref['records'][-1]['text'] = 'different text'
    ref['source_observation_counts'] = [255, 255]
    candidate = '## Comments\n' + '\n\n'.join('### Same\nsame text' for _ in range(255))
    assert not check(candidate, ref)['article_comments_pass']
    assert len(calls) <= 4


def single_observation_reference():
    ref = deepcopy(REFERENCE)
    ref['source_observation_counts'] = [2]
    ref['source_evidence'] = [{'path': 'capture/complete-source.html', 'sha256': 'a' * 64,
                               'scope': 'complete_initial_page'}]
    return ref


def test_one_historical_complete_capture_can_qualify_authoring_but_never_runtime():
    ref = single_observation_reference()
    qualified = qualify_article_comments(CONTRACT, ref, case_id='article', url=REFERENCE['url'])
    assert qualified == {'status': 'qualified', 'observation_count': 1, 'comment_count': 2}
    runtime = check(markdown(), ref)
    assert runtime['article_comments_reference_status'] == 'invalid'
    assert not runtime['article_comments_pass']


@pytest.mark.parametrize('change', ['missing', 'empty', 'bad_sha', 'wrong_scope', 'no_path', 'multiple'])
def test_single_capture_authoring_requires_declared_complete_source_evidence(change):
    ref = single_observation_reference()
    if change == 'missing':
        del ref['source_evidence']
    elif change == 'empty':
        ref['source_evidence'] = []
    elif change == 'bad_sha':
        ref['source_evidence'][0]['sha256'] = 'not-a-digest'
    elif change == 'wrong_scope':
        ref['source_evidence'][0]['scope'] = 'viewport_only'
    elif change == 'no_path':
        ref['source_evidence'][0]['path'] = ' '
    else:
        ref['source_evidence'] *= 2
    assert qualify_article_comments(CONTRACT, ref, case_id='article', url=REFERENCE['url'])['status'] == 'invalid'


def test_two_source_qualification_and_runtime_requirements_remain_unchanged():
    qualified = qualify_article_comments(CONTRACT, REFERENCE, case_id='article', url=REFERENCE['url'])
    assert qualified == {'status': 'qualified', 'observation_count': 2, 'comment_count': 2}
    assert check(markdown())['article_comments_pass']
    ref = single_observation_reference()
    ref['case_id'] = 'different'
    assert qualify_article_comments(CONTRACT, ref, case_id='article', url=REFERENCE['url'])['status'] == 'invalid'



def date_only_reference():
    ref = single_observation_reference()
    del ref['observed_at']
    ref['observed_on'] = '2026-10-19'
    return ref


def test_historical_date_only_provenance_qualifies_without_invented_timestamp():
    ref = date_only_reference()
    before = deepcopy(ref)
    result = qualify_article_comments(CONTRACT, ref, case_id='article', url=REFERENCE['url'])
    assert result == {'status': 'qualified', 'observation_count': 1, 'comment_count': 2,
                      'observed_on': '2026-10-19'}
    assert ref == before
    assert 'observed_at' not in ref
    assert check(markdown(), ref)['article_comments_reference_status'] == 'invalid'
    ref['source_observation_counts'] = [2, 2]
    assert check(markdown(), ref)['article_comments_reference_status'] == 'invalid'


@pytest.mark.parametrize('observed_on', [None, '', '2026-02-30', '2026-10-19T00:00:00Z',
                                       '2026-1-9', '20261019', 'not a date'])
def test_date_only_authoring_rejects_missing_or_invalid_observation_dates(observed_on):
    ref = date_only_reference()
    if observed_on is None:
        del ref['observed_on']
    else:
        ref['observed_on'] = observed_on
    result = qualify_article_comments(CONTRACT, ref, case_id='article', url=REFERENCE['url'])
    assert result['status'] == 'invalid'
    assert 'observed_on' not in result


def test_date_only_authoring_requires_bound_complete_source_and_does_not_hide_bad_timestamps():
    ref = date_only_reference()
    ref['source_observation_counts'] = [2, 2]
    del ref['source_evidence']
    assert qualify_article_comments(CONTRACT, ref, case_id='article', url=REFERENCE['url'])['status'] == 'invalid'
    ref = date_only_reference()
    ref['observed_at'] = 'invalid exact timestamp'
    assert qualify_article_comments(CONTRACT, ref, case_id='article', url=REFERENCE['url'])['status'] == 'invalid'



@pytest.mark.parametrize('reference', [REFERENCE, single_observation_reference(), date_only_reference()])
def test_absent_component_cannot_qualify_positive_historical_reference(reference):
    result = qualify_article_comments(ABSENT_CONTRACT, reference, case_id='article', url=REFERENCE['url'])
    assert result['status'] == 'unsupported_layout'
    assert result['comment_count'] == 2


def test_absent_component_qualifies_only_independently_observed_zero_records():
    ref = zero_comment_reference()
    assert qualify_article_comments(ABSENT_CONTRACT, ref, case_id='article', url=REFERENCE['url'])['status'] == 'qualified'
    ref = date_only_reference()
    ref.update(records=[], source_observation_counts=[0])
    result = qualify_article_comments(ABSENT_CONTRACT, ref, case_id='article', url=REFERENCE['url'])
    assert result == {'status': 'qualified', 'observation_count': 1, 'comment_count': 0,
                      'observed_on': '2026-10-19'}



@pytest.mark.parametrize('section,marker', [
    ('留言（255条）', '留言'), ('留言（69条）', '留言'),
    ('3 条评论', '评论'), ('413 Reader Comments', 'Reader Comments'),
])
def test_actual_initial_source_comment_count_labels_match_natural_plain_records(section, marker):
    contract = {**CONTRACT, 'section_markers': [marker]}
    candidate = markdown().replace('Comments', section)
    result = verify_article_comments(candidate, contract, REFERENCE,
                                    case_id='article', url=REFERENCE['url'], reference_context=CONTEXT)
    assert result['article_comments_pass']


@pytest.mark.parametrize('count', [0, 1, 69, 255, 9999])
@pytest.mark.parametrize('decoration,marker', [
    ('留言（{}条）', '留言'), ('留言 ({}则)', '留言'), ('留言（{}件）', '留言'),
    ('{} 条评论', '评论'), ('{}则 评论', '评论'), ('{}件评论', '评论'),
    ('{} Reader Comments', 'Reader Comments'),
])
def test_changing_count_units_do_not_change_comment_acceptance(count, decoration, marker):
    contract = {**CONTRACT, 'section_markers': [marker]}
    candidate = markdown().replace('Comments', decoration.format(count))
    result = verify_article_comments(candidate, contract, REFERENCE,
                                    case_id='article', url=REFERENCE['url'], reference_context=CONTEXT)
    assert result['article_comments_pass']


@pytest.mark.parametrize('section', [
    '2026-10-19 Reader Comments', 'Reader Comments (2026-10-19)',
    'Reader Comments（2026年10月19日）', '413 Other Comments',
    '3 条回复', '留言（69篇）', '留言（69条） additional text',
])
def test_count_heading_normalization_does_not_strip_dates_or_match_unrelated_sections(section):
    contract = {**CONTRACT, 'section_markers': ['Reader Comments', '评论', '留言']}
    candidate = markdown().replace('Comments', section)
    result = verify_article_comments(candidate, contract, REFERENCE,
                                    case_id='article', url=REFERENCE['url'], reference_context=CONTEXT)
    assert not result['article_comments_pass']


def test_count_unit_normalization_is_not_applied_to_author_or_body():
    ref = deepcopy(REFERENCE)
    ref['records'][0]['author'] = '3 条评论'
    ref['records'][1]['text'] = '42（9条）'
    candidate = markdown().replace('### Alice', '### 3 条评论').replace(REPLY, '42（9条）')
    assert check(candidate, ref)['article_comments_pass']
    assert not check(candidate.replace('### 3 条评论', '### 评论'), ref)['article_comments_pass']
    assert not check(candidate.replace('42（9条）', '42'), ref)['article_comments_pass']



@pytest.mark.parametrize('mention', ['@Bob', '@Bob:', '@Alice', '@Alice:'])
def test_body_mentions_do_not_become_plain_author_records(mention):
    ref = deepcopy(REFERENCE)
    ref['records'][0]['text'] = BODY + '\n' + mention + '\n' + BODY
    candidate = markdown(body=ref['records'][0]['text'])
    assert check(candidate, ref)['article_comments_pass']
    assert check(candidate, ref)['article_comment_count'] == 2


def test_nested_body_mention_retains_reply_ownership():
    ref = deepcopy(REFERENCE)
    ref['records'][1]['text'] = '@Alice\n' + REPLY
    candidate = markdown(reply=ref['records'][1]['text'])
    assert check(candidate, ref)['article_comments_pass']
    assert not check(candidate.replace('#### Bob', '### Bob'), ref)['article_comments_pass']


def test_literal_at_prefixed_author_requires_real_header_and_keeps_identity():
    ref = deepcopy(REFERENCE)
    ref['records'][0]['author'] = '@Alice'
    assert check(markdown().replace('### Alice', '### @Alice'), ref)['article_comments_pass']
    assert not check(markdown(), ref)['article_comments_pass']
    assert not check(markdown().replace('### Alice', '@Alice'), ref)['article_comments_pass']
    assert not check(markdown().replace('### Alice', '@Alice:'), REFERENCE)['article_comments_pass']


def test_pingback_linked_source_header_and_visible_body_form_one_record():
    candidate = ('## Comments\n\n### [Weekly writing links](https://source.test/post)'
                 '\n\nPingback: Weekly writing links')
    result = check_pingback(candidate)
    assert result['article_comments_pass']
    assert result['article_comment_count'] == 1
    assert not check_pingback(candidate + '\nPingback: Weekly writing links')['article_comments_pass']


def test_six_nested_comment_levels_can_use_valid_h1_through_h6_headers():
    ref = deepcopy(REFERENCE)
    ref['records'] = [{'id': str(i), 'author': 'Author' + str(i), 'text': 'Reply text number ' + str(i),
                       'parent_id': str(i - 1) if i else None, 'complete_initial_text': True}
                      for i in range(6)]
    ref['source_observation_counts'] = [6, 6]
    candidate = 'Comments\n\n' + '\n\n'.join('#' * (i + 1) + ' Author' + str(i)
                                                          + '\nReply text number ' + str(i) for i in range(6))
    assert check(candidate, ref)['article_comments_pass']
    flattened = candidate.replace('###### Author5', '# Author5')
    assert not check(flattened, ref)['article_comments_pass']



def test_displayed_comment_code_is_owned_content_not_a_new_author_or_section():
    code = ('Before the example.\n```css\njustify-content: flex-start | flex-end | center | '
            'space-between | space-around | space-evenly;\n```\nAfter the example.')
    ref = deepcopy(REFERENCE)
    ref['records'][0]['text'] = code
    candidate = markdown(body=code)
    assert check(candidate, ref)['article_comments_pass']
    assert check(candidate, ref)['article_comment_count'] == 2
    assert not check(markdown(body='Before the example. After the example.'), ref)['article_comments_pass']


def test_literal_code_author_names_cannot_split_owned_comment_body():
    code = BODY + '\n```\n## Comments\n### Bob\n' + REPLY + '\n```'
    ref = deepcopy(REFERENCE)
    ref['records'][0]['text'] = code
    candidate = markdown(body=code)
    assert check(candidate, ref)['article_comments_pass']
    assert check(candidate, ref)['article_comment_count'] == 2
    # A whole fenced page still supplies no independent section or author card.
    assert not check('```markdown\n' + markdown() + '\n```')['article_comments_pass']
