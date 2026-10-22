"""Language labels are frozen task data, not scorer-wide site onboarding."""
from copy import deepcopy
import pytest
from lexbench_webfetch.article_comments import validate_comment_contract, verify_article_comments
from lexbench_webfetch.article_posts import validate_post_contract, verify_article_posts
from lexbench_webfetch.article_text import validate_labels

C = {'version': 2, 'minimum_comments': 1, 'record_selector': '.comment',
     'author_selector': '.author', 'body_selector': '.body', 'section_markers': ['Comments'],
     'ignored_labels': ['返信'], 'unavailable_notices': ['非表示のコメント']}


def test_new_language_labels_are_task_local_and_whole_label_only():
    def check(text, contract):
        return verify_article_comments('<div class="comment"><span class="author">Reader</span><p class="body">'+text+'</p></div>', contract)['article_comments_pass']
    assert not check('返信', C)
    assert not check('非表示のコメント', C)
    assert check('返信について説明します。', C)
    assert check('Real response.', C)
    other = {**C, 'ignored_labels': [], 'unavailable_notices': []}
    assert check('返信', other)
    assert not check('', other)


@pytest.mark.parametrize('bad', [None, 'Reply', [1], [''], ['Reply', 'Reply']])
def test_invalid_declared_labels_fail_closed(bad):
    with pytest.raises(ValueError):
        validate_comment_contract({**C, 'ignored_labels': bad})


def test_post_labels_are_not_global_or_substring_filters():
    contract = {'version': 2, 'minimum_posts': 1, 'hosts': ['example.test'], 'entry_path': r'/p/\d+',
                'html_record_selector': 'article', 'html_permalink_selector': 'a',
                'html_author_selector': 'b', 'html_body_selector': 'p',
                'ignored_labels': ['返信'], 'unavailable_notices': ['非表示']}
    def check(body):
        html = '<article><a href="/p/1">Post</a><b>Author</b><p>'+body+'</p></article>'
        return verify_article_posts(html, contract, url='https://example.test/feed')['article_posts_pass']
    assert not check('返信')
    assert not check('非表示')
    assert check('返信について説明します。')
    assert not check('')


def test_changed_authoring_defaults_cannot_silently_recompile(tmp_path):
    import shutil
    from lexbench_webfetch.article_dataset import DEFINITIONS, compile_dataset
    for name in ['cohort.json', 'rules.json', 'labels.json']:
        shutil.copyfile(DEFINITIONS / name, tmp_path / name)
    with (tmp_path / 'labels.json').open('a') as stream:
        stream.write('\n')
    with pytest.raises(ValueError, match='Changed article label defaults'):
        compile_dataset(tmp_path, tmp_path)
