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


# Frozen v2-input compatibility defaults. New authored contracts declare labels.
# Never expand these lists to onboard a site; labels belong to its input contract.
ARTICLE_CONTROLS = frozenset({'load more', 'read more', '登录', 'log in', '点赞', 'sign in', 'likes', 'replies', 'report', 'reply', '回复', 'show more', '加载更多', '展开', '查看更多', 'like', 'share', '注册'})
COMMENT_CONTROLS = frozenset({'read more', '登录', '加载更多', '添加评论', 'like', 'share', 'register', 'report', 'show more', 'sign in', '注册', '点赞', 'leave a reply', 'likes', '登录后评论', 'reply', '查看更多', 'load more', 'log in', 'replies', '回复', 'login', 'add a comment', '展开', '展开回复', '发表评论'})
COMMENT_PLACEHOLDERS = frozenset({'this comment has been hidden (marked as spam)', '[内容不可见]', '[deleted]', 'this comment has been hidden', '[removed]', '[已删除]'})


POST_CONTROLS = frozenset({'read more', '登录', '加载更多', '转发', '分享', 'like', '查看', 'share', 'report', 'show more', 'sign in', '收藏', '注册', '点赞', 'bookmarks', 'likes', 'reply', '今天', '查看更多', 'views', 'yesterday', 'load more', 'log in', 'replies', 'reposts', 'repost', 'today', 'view', '回复', '昨天', '展开', 'bookmark', 'permalink'})


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
        if node.name == 'pre':
            literal = node.get_text()
            longest = max((len(run) for run in re.findall(r'`+', literal)), default=0)
            fence = '`' * max(3, longest + 1)
            return '\n\n' + fence + '\n' + literal + '\n' + fence + '\n\n'
        if node.name == 'code':
            # Inline literal syntax must not create a record or section boundary.
            literal = node.get_text().replace('\n', ' ')
            return '`' + literal.replace('`', '\\`') + '`'
        if node.name == 'tr':
            cells = [render(child).replace('\n', ' ').strip()
                     for child in node.children if isinstance(child, Tag)
                     and child.name in ('td', 'th')]
            return '\n| ' + ' | '.join(cells) + ' |\n'
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


def validate_labels(contract):
    """Reject malformed task-declared labels rather than silently widening scope."""
    for field in ('ignored_labels', 'unavailable_notices'):
        if field in contract:
            labels = contract[field]
            if (not isinstance(labels, list) or any(not isinstance(label, str)
                    or not label.strip() for label in labels) or len(set(labels)) != len(labels)):
                raise ValueError('Invalid task-declared ' + field)


def declared_labels(contract, field, legacy):
    """Use an explicit task list, including an explicit empty list, verbatim."""
    return frozenset(' '.join(unicodedata.normalize('NFKC', label).split()).casefold().strip(':：')
                     for label in contract.get(field, legacy))
