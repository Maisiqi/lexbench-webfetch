"""Section titles require local returned body, not navigation or a word bag."""
from copy import deepcopy

import pytest

from lexbench_webfetch.document_structure import evaluate_document_structure, validate_document_structure
from lexbench_webfetch.metrics import task_passed
from lexbench_webfetch.scoring import score_attempt


def contract():
    return {'version': 1, 'minimum_heading_coverage': .8, 'minimum_body_chars': 50,
            'headings': [{'id': str(i), 'text': name, 'level': 2, 'body_required': True}
                         for i, name in enumerate(['Install', 'Usage', 'Errors', 'Examples', 'Reference'])]}


def body(count=5):
    return '\n\n'.join('## '+h['text']+'\nA useful paragraph describes this section.'
                       for h in contract()['headings'][:count])


@pytest.mark.parametrize('count,passed', [(5, True), (4, True), (3, False)])
def test_section_coverage(count, passed):
    assert evaluate_document_structure(body(count), contract())['document_structure_pass'] is passed


@pytest.mark.parametrize('text', [
    'Install\nUsage\nErrors\nExamples\nReference\n'+'Unrelated filler. '*20,
    '\n'.join(f'[{h["text"]}](#target)' for h in contract()['headings'])+'\n'+'Filler. '*30,
    'This sentence mentions Install, Usage, Errors, Examples and Reference. '*10,
    'Reference Examples Errors Usage Install\n'+'Filler. '*30,
    '```\n'+body()+'\n```',
])
def test_toc_sentence_word_bag_and_code_are_not_sections(text):
    assert not evaluate_document_structure(text, contract())['document_structure_pass']


@pytest.mark.parametrize('tag', ['nav', 'header', 'footer', 'aside'])
def test_html_navigation_cannot_supply_headings(tag):
    nav=''.join('<h2>'+h['text']+'</h2><p>Navigation copy</p>' for h in contract()['headings'])
    text=f'<{tag}>{nav}</{tag}><main><p>'+('Other text. '*30)+'</p></main>'
    assert not evaluate_document_structure(text, contract(), html_document=True)['document_structure_pass']


def test_html_paragraphs_containing_title_words_are_not_headings():
    text='<main>'+''.join('<p>'+h['text']+'</p><p>Substantial content.</p>' for h in contract()['headings'])+'</main>'
    assert not evaluate_document_structure(text, contract(), html_document=True)['document_structure_pass']


def test_html_real_heading_elements_and_nested_inline_text():
    text='<main>'+''.join('<h2><span>'+h['text']+'</span></h2><p>Substantial content.</p>' for h in contract()['headings'])+'</main>'
    assert evaluate_document_structure(text, contract(), html_document=True)['document_structure_pass']


def test_html_comments_cannot_supply_section_body():
    text='<main>'+''.join('<h2>'+h['text']+'</h2><!-- renderer state -->'
                         for h in contract()['headings'])+'</main>'
    measured=evaluate_document_structure(text,contract(),html_document=True)
    assert measured['document_body_chars'] == 0
    assert not measured['document_structure_pass']


def test_visually_present_aria_hidden_prose_supplies_section_body():
    text='<main>'+''.join('<h2>'+h['text']+'</h2><p aria-hidden="true">'
                         'Visible paragraph describing the section.</p>'
                         for h in contract()['headings'])+'</main>'
    assert evaluate_document_structure(text,contract(),html_document=True)['document_structure_pass']


@pytest.mark.parametrize('style', ['display:none', 'display: none !important',
                                  'visibility:hidden', 'opacity:0'])
def test_explicit_css_hidden_prose_cannot_supply_section_body(style):
    text='<main>'+''.join('<h2>'+h['text']+'</h2><p style="'+style+'">'
                         'Hidden paragraph describing the section.</p>'
                         for h in contract()['headings'])+'</main>'
    measured=evaluate_document_structure(text,contract(),html_document=True)
    assert measured['document_body_chars'] == 0
    assert not measured['document_structure_pass']


def test_changed_html_heading_depth_cannot_let_siblings_borrow_one_paragraph():
    text='<main>'+''.join(f'<h{i+1}>{h["text"]}</h{i+1}>'
                         for i,h in enumerate(contract()['headings']))+'<p>'+('Filler. '*30)+'</p></main>'
    assert not evaluate_document_structure(text,contract(),html_document=True)['document_structure_pass']


def test_source_declared_empty_heading_is_not_fabricated_prose():
    c=contract()
    c['headings'][-1]['body_required']=False
    assert evaluate_document_structure(body(3)+'\n## Reference', c)['document_structure_pass']
    assert not evaluate_document_structure(body(3)+'\n## Reference', contract())['document_structure_pass']


def test_multiline_heading_preserves_order_and_needs_body():
    c=contract()
    c['headings'][0]['text']='Install the client'
    text=body().replace('## Install', 'Install\nthe\nclient')
    assert evaluate_document_structure(text,c)['document_structure_pass']
    c['minimum_heading_coverage']=1
    assert not evaluate_document_structure(text.replace('Install\nthe\nclient','client\nthe\nInstall'),c)['document_structure_pass']


def test_child_prose_supports_parent_heading():
    c=contract()
    c['headings'][1]['level']=3
    text=body().replace('## Install\nA useful paragraph describes this section.', '## Install')
    assert evaluate_document_structure(text,c)['document_structure_pass']


def test_structure_is_optional_and_final_task_predicate_enforces_it():
    case={'url':'https://example.test/manual','expected_any':[],
          'acceptance_contract': {'version':1,'schema':'body_text','minimum_records':0,
                                  'stable_text_anchors':[{'id':'title','alternatives':['Install']}]}}
    text='Install\nUsage\nErrors\nExamples\nReference\n'+'Filler. '*20
    assert task_passed(True,score_attempt(case,text.encode(),ok=True))
    case['document_structure']=contract()
    m=score_attempt(case,text.encode(),ok=True)
    assert m['stable_task_pass']
    assert not m['content_pass']
    assert not task_passed(True,m)
    assert task_passed(True,score_attempt(case,body().encode(),ok=True))


@pytest.mark.parametrize('field,value', [('minimum_heading_coverage',True),('minimum_heading_coverage',float('nan')),
    ('minimum_heading_coverage',0),('minimum_heading_coverage',1.1),('minimum_body_chars',False),
    ('minimum_body_chars',0),('headings',[]),('version',True),('unknown',1)])
def test_invalid_contracts_fail_closed(field,value):
    c=contract();c[field]=value
    with pytest.raises(ValueError):validate_document_structure(c)


def test_all_empty_or_duplicate_headings_are_invalid():
    for c in [contract(),deepcopy(contract())]:
        if c['headings'][0]['body_required']:
            for h in c['headings']:h['body_required']=False
        with pytest.raises(ValueError):validate_document_structure(c)
    c=contract();c['headings'].append(deepcopy(c['headings'][0]))
    with pytest.raises(ValueError):validate_document_structure(c)
