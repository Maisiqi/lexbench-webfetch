"""Shared article-only visible text and identity policy."""
import re
import unicodedata
from .dynamic_lists import scoped_html
from .body_coverage import tokens
from .reference_quality import is_html_document_or_fragment, markdown_links

def author_key(value):
    """Keep literal symbol-only identities instead of comparing empty tokens."""
    if not isinstance(value, str):
        return None
    value = unicodedata.normalize('NFKC', value)
    # Joiners matter in rendered names and emoji sequences. Other invisible
    # format/control characters cannot create a username by themselves.
    value = ''.join(char for char in value
                    if not unicodedata.category(char).startswith('C') or char in '\u200c\u200d')
    value = ' '.join(value.split())
    if not any(not char.isspace() and not unicodedata.category(char).startswith('C') for char in value):
        return None
    words = tokens(value)
    return ('tokens', value.startswith('@'), tuple(words)) if words else ('literal', value)

def article_html(content):
    """Apply shared visibility and remove article-only fallback text."""
    soup = scoped_html(content)
    for fallback in list(soup.select('noscript')):
        if fallback.parent is not None:
            fallback.decompose()
    return soup

def without_markdown_images(content):
    """Image alt labels are metadata, including images nested in normal links."""
    pieces, cursor = [], 0
    for link in markdown_links(content):
        if link.start < cursor:
            continue
        pieces.append(content[cursor:link.start])
        if not link.is_image:
            original = content[link.start:link.end]
            pieces.append(original.replace(link.label, without_markdown_images(link.label), 1))
        cursor = link.end
    pieces.append(content[cursor:])
    return ''.join(pieces)

def is_article_html(content):
    """Classify HTML after complete leading non-content blocks only."""
    remaining = content.lstrip()
    # Attributes may contain a greater-than sign inside quoted values.
    attributes = r"(?:[^>\"']|\"[^\"]*\"|'[^']*')*"
    while True:
        prefix = re.match(
            r'<!--.*?-->|<(noscript|style|script)\b' + attributes
            + r'>.*?</\1\s*>|<(?:meta|link)\b' + attributes + r'>',
            remaining, re.I | re.S,
        )
        if not prefix:
            return is_html_document_or_fragment(remaining)
        remaining = remaining[prefix.end():].lstrip()


# Article-specific whole-label policy; never applied as substring filtering.
ARTICLE_CONTROLS = {'show more', 'log in', 'report', '回复', '注册', '加载更多', '展开', 'sign in', 'share', 'read more', 'like', '点赞', 'load more', 'likes', '登录', 'replies', 'reply', '查看更多'}
COMMENT_CONTROLS = ARTICLE_CONTROLS | {'login', '展开回复', 'register', '发表评论', '登录后评论', '添加评论', 'leave a reply', 'add a comment'}
COMMENT_PLACEHOLDERS = {'[内容不可见]', '[已删除]', '[deleted]', '[removed]',
                         'this comment has been hidden',
                         'this comment has been hidden (marked as spam)'}


POST_CONTROLS = ARTICLE_CONTROLS | {'view', 'views', '昨天', '今天', 'permalink', '转发', 'bookmarks', 'repost', 'yesterday', 'reposts', 'today', '查看', '分享', '收藏', 'bookmark'}


def article_markdown(content):
    """Project cleaned HTML while retaining headings, links and ownership stops.

    This is used only when no reviewed native record containers remain. It is
    not a competing parser whose more permissive count can override native DOM
    ownership. Navigation and explicit related-content landmarks are excluded.
    """
    from bs4 import NavigableString, Tag
    soup = article_html(content)
    for node in list(soup.select('nav, aside, footer, [role="navigation"], [role="complementary"]')):
        if node.parent is not None:
            node.decompose()
    def render(node):
        if isinstance(node, NavigableString):
            return str(node)
        if not isinstance(node, Tag):
            return ''
        text = ''.join(render(child) for child in node.children)
        if node.name == 'img':
            return ''
        if node.name == 'a':
            return '[' + text.strip() + '](' + node.get('href', '') + ')'
        if node.name in ('strong', 'b'):
            return '**' + text.strip() + '**'
        if re.fullmatch(r'h[1-6]', node.name):
            return '\n\n' + '#' * int(node.name[1]) + ' ' + text.strip() + '\n\n'
        if node.name == 'blockquote':
            return '\n\n' + '\n'.join('> ' + line for line in text.strip().splitlines()) + '\n\n'
        if node.name == 'br':
            return '\n'
        if node.name in ('p', 'div', 'section', 'article', 'ul', 'ol', 'li'):
            return '\n\n' + text.strip() + '\n\n'
        return text
    return render(soup)
