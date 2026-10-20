"""Check initial comment coverage, preserving legacy run-bound verification."""
from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from datetime import date, datetime
from functools import lru_cache

import soupsieve

from .article_posts import _is_post_html
from .body_coverage import body_requirements, evaluate_body_requirements, tokens
from .dynamic_lists import _scoped_html, visible_html_text
from .reference_quality import markdown_links, visible_markdown_links


def validate_comment_contract(contract):
    """Validate the frozen extraction contract without acquiring any source page."""
    if isinstance(contract, dict) and type(contract.get('version')) is int and contract['version'] == 2:
        return _validate_coverage_contract(contract)
    allowed = {'version', 'mode', 'record_selector', 'author_selector', 'body_selector',
               'id_attribute', 'parent_record_selector', 'section_markers',
               'max_reference_age_seconds'}
    try:
        if not isinstance(contract, dict) or set(contract) - allowed or type(contract['version']) is not int or contract['version'] != 1:
            raise ValueError('invalid comment contract')
        age = contract['max_reference_age_seconds']
        if type(age) not in (int, float) or not math.isfinite(age) or not 0 < age <= 900:
            raise ValueError('comment observations must be at most fifteen minutes old')
        if contract.get('mode') == 'observed_absent':
            if set(contract) != {'version', 'mode', 'max_reference_age_seconds'}:
                raise ValueError('absent comment layout must not invent extraction selectors')
            return
        if 'mode' in contract:
            raise ValueError('unknown comment contract mode')
        for key in ('record_selector', 'author_selector', 'body_selector'):
            if not isinstance(contract[key], str) or not contract[key].strip():
                raise ValueError('empty comment selector')
            soupsieve.compile(contract[key])
        if 'parent_record_selector' in contract:
            soupsieve.compile(contract['parent_record_selector'])
        if 'id_attribute' in contract and not re.fullmatch(r'[a-zA-Z_][\w:-]*', contract['id_attribute']):
            raise ValueError('invalid comment ID attribute')
        markers = contract['section_markers']
        if not isinstance(markers, list) or not markers or any(not isinstance(x, str) or not x.strip() for x in markers):
            raise ValueError('comment section markers required')
    except (KeyError, TypeError, re.error, soupsieve.SelectorSyntaxError) as error:
        raise ValueError('invalid comment contract') from error


def _validate_coverage_contract(contract):
    allowed = {'version', 'minimum_comments', 'record_selector', 'author_selector',
               'body_selector', 'section_markers', 'id_attribute'}
    if set(contract) - allowed or type(contract.get('minimum_comments')) is not int or contract['minimum_comments'] < 1:
        raise ValueError('comment coverage requires a positive minimum')
    # Reuse selector validation without admitting legacy runtime requirements.
    legacy = {key: value for key, value in contract.items() if key != 'minimum_comments'}
    legacy.update(version=1, max_reference_age_seconds=900)
    validate_comment_contract(legacy)


def _utc(value):
    stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
        raise ValueError('UTC timestamp required')
    return stamp


def _author_key(value):
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


def _reference_status(reference, context, contract, case_id, url, *,
                      allow_single_observation=False, allow_authoring_date=False):
    if reference is None:
        return 'missing'
    try:
        if (type(reference['version']) is not int or reference['version'] != 1
                or reference['case_id'] != case_id or reference['url'] != url
                or reference['scope'] != 'initial_load_only'
                or reference['observation_complete'] is not True
                or not isinstance(reference['context_id'], str) or not reference['context_id']):
            return 'invalid'
        records, counts = reference['records'], reference['source_observation_counts']
        if (not isinstance(records, list) or not isinstance(counts, list)
                or len(counts) < (1 if allow_single_observation else 2)
                or any(type(n) is not int or n < 0 for n in counts) or counts[-1] != len(records)):
            return 'invalid'
        evidence = reference.get('source_evidence')
        if allow_single_observation and len(counts) == 1:
            if not isinstance(evidence, list) or len(evidence) != 1:
                return 'invalid'
        if evidence is not None and (not isinstance(evidence, list) or not evidence
                or any(not isinstance(item, dict) or not isinstance(item.get('path'), str)
                       or not item['path'].strip() or not isinstance(item.get('sha256'), str)
                       or not re.fullmatch(r'[0-9a-f]{64}', item['sha256'])
                       or item.get('scope') != 'complete_initial_page' for item in evidence)):
            return 'invalid'
        seen = set()
        for row in records:
            if (not isinstance(row['id'], str) or not row['id'] or row['id'] in seen
                    or _author_key(row['author']) is None
                    or not isinstance(row['text'], str)
                    or (not row['text'].strip() and row.get('empty_body') is not True)
                    or ('empty_body' in row and (row['empty_body'] is not True or row['text'] != ''))
                    or row['complete_initial_text'] is not True
                    or row['parent_id'] is not None and row['parent_id'] not in seen):
                return 'invalid'
            if ('image_only' in row or 'source_media_count' in row) and (
                    row.get('image_only') is not True or row.get('empty_body') is not True
                    or row['text'] != '' or type(row.get('source_media_count')) is not int
                    or row['source_media_count'] < 1):
                return 'invalid'
            seen.add(row['id'])
        by_id = {row['id']: row for row in records}
        for row in records:
            if row.get('empty_body') is not True:
                continue
            # Independent rendered-media evidence can explain an image-only
            # leaf without inventing OCR prose. Otherwise an empty parent must
            # own at least one displayed descendant with ordinary text.
            if row.get('image_only') is True:
                continue
            descendant_text = False
            for child in records:
                parent = child['parent_id']
                while parent is not None:
                    if parent == row['id'] and child['text'].strip():
                        descendant_text = True
                        break
                    parent = by_id[parent]['parent_id']
                if descendant_text:
                    break
            if not descendant_text:
                return 'invalid'
        if not records and any(counts):
            return 'invalid'
        if allow_authoring_date and 'observed_at' not in reference:
            # Historical date-only evidence establishes authoring provenance,
            # never a clock value, freshness, or an execution context match.
            observed_on = reference.get('observed_on')
            if (not isinstance(observed_on, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', observed_on)
                    or date.fromisoformat(observed_on).isoformat() != observed_on or not evidence):
                return 'invalid'
        else:
            observed = _utc(reference['observed_at'])
            if not isinstance(context, dict) or context.get('id') != reference['context_id']:
                return 'context_mismatch'
            age = (_utc(context['started_at']) - observed).total_seconds()
            if age < 0:
                return 'context_mismatch'
            if age > contract['max_reference_age_seconds']:
                return 'stale'
        if contract.get('mode') == 'observed_absent' and records:
            # A newly appeared component requires reviewed extraction rules.
            # Its absence from an older definition can never excuse its text.
            return 'unsupported_layout'
    except (KeyError, ValueError, TypeError, AttributeError):
        return 'invalid'
    return 'verified'


def qualify_article_comments(contract, reference, *, case_id, url):
    """Review historical authoring evidence; never certify a future run.

    A single complete independent capture may qualify authoring only when its
    external source path and SHA-256 are declared. The compiler must verify
    those physical bytes. A real ISO observation date is sufficient for historical
    authoring when no exact timestamp exists; it creates no freshness claim.
    Runtime verification still requires two observations and exact UTC times.
    """
    validate_comment_contract(contract)
    qualification_contract = contract
    if contract['version'] == 2:
        qualification_contract = dict(contract, max_reference_age_seconds=900)
    if reference is None:
        status = 'missing'
    elif not isinstance(reference, dict):
        status = 'invalid'
    else:
        status = _reference_status(reference, {
            'id': reference.get('context_id'), 'started_at': reference.get('observed_at')},
            qualification_contract, case_id, url, allow_single_observation=True, allow_authoring_date=True)
    result = {'status': 'qualified' if status == 'verified' else status,
            'observation_count': len(reference.get('source_observation_counts', []))
            if isinstance(reference, dict) and isinstance(reference.get('source_observation_counts'), list) else 0,
            'comment_count': len(reference.get('records', []))
            if isinstance(reference, dict) and isinstance(reference.get('records'), list) else 0}
    if status == 'verified' and contract['version'] == 2:
        valid_count = len(_valid_coverage_records(reference['records']))
        result['valid_comment_count'] = valid_count
        if valid_count < contract['minimum_comments']:
            result['status'] = 'insufficient_comments'
    if status == 'verified' and 'observed_at' not in reference:
        result['observed_on'] = reference['observed_on']
    return result


def _comment_html(content):
    """Project native closed disclosure widgets without changing other suites."""
    soup = _scoped_html(content)
    for fallback in list(soup.select('noscript')):
        if fallback.parent is not None:
            fallback.decompose()
    for details in list(soup.select('details:not([open])')):
        if details.parent is None:
            continue
        # A closed details element renders only its first direct summary. A
        # nested open details cannot expose content through a closed ancestor.
        summary = details.find('summary', recursive=False)
        for child in list(details.contents):
            if child is not summary:
                child.extract()
    return soup


def _html_records(content, contract):
    soup = _comment_html(content)
    cards = soup.select(contract['record_selector'])
    rows = []
    for card in cards:
        def owner(node):
            return node.find_parent(lambda x: soupsieve.match(contract['record_selector'], x))
        fields = [[node for node in card.select(contract[key]) if owner(node) is card]
                  for key in ('author_selector', 'body_selector')]
        parent = card.find_parent(lambda x: soupsieve.match(
            contract.get('parent_record_selector', contract['record_selector']), x))
        parent_index = next((i for i, candidate in enumerate(cards) if candidate is parent),
                            -1 if parent is not None else None)
        row = {'parent': parent_index, 'source_id': card.get(contract.get('id_attribute', 'id'))}
        if any(len(nodes) != 1 for nodes in fields):
            rows.append(row)
            continue
        author, body = [nodes[0] for nodes in fields]
        copy = _comment_html(str(body))
        for nested in list(copy.select(contract['record_selector'])):
            if nested.parent is not None:
                nested.decompose()
        row.update(author=visible_html_text(str(author)), text=visible_html_text(str(copy)))
        rows.append(row)
    return rows


def _without_markdown_images(content):
    """Image alt labels are metadata, including images nested in normal links."""
    pieces, cursor = [], 0
    for link in markdown_links(content):
        if link.start < cursor:
            continue
        pieces.append(content[cursor:link.start])
        if not link.is_image:
            original = content[link.start:link.end]
            pieces.append(original.replace(link.label, _without_markdown_images(link.label), 1))
        cursor = link.end
    pieces.append(content[cursor:])
    return ''.join(pieces)


def _section_marker_tokens(line):
    """Ignore changing count decorations only on a comment section heading."""
    label = re.sub(r'^\s*#{1,6}\s+', '', line).strip().rstrip(':：')
    label = re.sub(r'^[0-9]+(?:\s*(?:条|则|件)\s*|\s+)', '', label)
    label = re.sub(r'\s*(?:\(\s*[0-9]+\s*(?:条|则|件)?\s*\)|（\s*[0-9]+\s*(?:条|则|件)?\s*）)\s*$', '', label)
    return tuple(tokens(label))


def _text_records(content, contract, authors):
    # Fences cannot create comment-section or author boundaries, but literal
    # code displayed inside an already owned comment remains required content.
    fence_marker = '\ue000comment-literal-code\ue001'
    while fence_marker in content:
        fence_marker += '_'
    fenced = {}
    def protect_fence(match):
        marker = fence_marker + str(len(fenced))
        fenced[marker] = match.group(0)
        return '\n' + marker + '\n'
    content = re.sub(r'(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*$', protect_fence, content)
    content = _without_markdown_images(content)
    paragraph_marker = '\ue000comment-paragraph-break\ue001'
    while paragraph_marker in content:
        paragraph_marker += '_'
    content = re.sub(r'\n[ \t]*\n', '\n' + paragraph_marker + '\n', content)
    content = visible_html_text(str(_comment_html(content)), preserve_source_whitespace=True, preserve_links=True)
    content = content.replace(paragraph_marker, '')
    lines = content.splitlines()
    markers = {tuple(tokens(x)) for x in contract['section_markers']}
    start = next((i + 1 for i, line in enumerate(lines)
                  if _section_marker_tokens(line) in markers), None)
    if start is None:
        return []
    rows, stack, current = [], [], None
    names = {_author_key(author): author for author in authors}
    for offset, line in enumerate(lines[start:]):
        if line.strip() in fenced:
            if current is not None:
                current['text'] += '\n' + fenced[line.strip()]
            continue
        pingback = re.fullmatch(r'\s*Pingback:\s+(.+?)\s*', line)
        if pingback:
            source = pingback[1]
            links = [link for link in markdown_links(source) if not link.is_image]
            label = visible_markdown_links(source)
            # WordPress renders pingbacks as one complete line. Its linked
            # source title owns identity; it is not a fabricated human author.
            # Plain serializers may retain that same line without its URL.
            if (_author_key(label) in names
                    and (not links or len(links) == 1 and source.strip() == source[links[0].start:links[0].end])):
                visible_line = visible_markdown_links(line).strip()
                if (current is not None and _author_key(current['author']) == _author_key(label)
                        and not current['text'].strip()):
                    # A faithful projection can retain both the linked source
                    # header and its complete displayed Pingback body line.
                    current['text'] = visible_line
                    continue
                rows.append({'author': label, 'text': visible_line,
                             'parent': None, 'source_id': None})
            stack, current = [], None
            continue
        heading = re.fullmatch(r'\s*(#{1,6})\s+(.+?)\s*', line)
        plain = re.fullmatch(r'([^\n:：]{1,120})[:：]\s*', line)
        bare = (names.get(_author_key(visible_markdown_links(line)))
                if line.strip() and not line.lstrip().startswith('@')
                and (offset == 0 or not lines[start + offset - 1].strip()) else None)
        if heading and _author_key(visible_markdown_links(heading[2])) not in names:
            heading = None
        if plain and (_author_key(visible_markdown_links(plain[1])) not in names
                      or plain[1].lstrip().startswith('@') and current is not None):
            plain = None
        if heading or plain or bare:
            level, author = (len(heading[1]), heading[2]) if heading else (2, plain[1] if plain else bare)
            while stack and stack[-1][0] >= level:
                stack.pop()
            current = {'author': visible_markdown_links(author), 'text': '',
                       'parent': stack[-1][1] if stack else None, 'source_id': None}
            rows.append(current)
            stack.append((level, len(rows) - 1))
        elif current is not None:
            current['text'] += '\n' + visible_markdown_links(line)
    return rows


# These are interface controls, not author identities or comment bodies. Match
# whole labels only: a real comment can discuss logging in or loading a page.
_COMMENT_CONTROLS = {'reply', 'replies', 'like', 'likes', 'share', 'report',
                     'load more', 'show more', 'read more', 'sign in', 'log in',
                     'login', 'register', 'leave a reply', 'add a comment',
                     '发表评论', '添加评论', '回复', '点赞', '登录', '注册',
                     '查看更多', '加载更多', '展开', '展开回复', '登录后评论'}
_COMMENT_PLACEHOLDERS = {'[内容不可见]', '[已删除]', '[deleted]', '[removed]',
                         'this comment has been hidden',
                         'this comment has been hidden (marked as spam)'}


def _coverage_label(value):
    return ' '.join(unicodedata.normalize('NFKC', value).split()).casefold().strip(':：')


def _valid_coverage_records(rows):
    valid, seen = [], set()
    for row in rows:
        author, body = row.get('author'), row.get('text')
        if (_author_key(author) is None or not isinstance(body, str)
                or _author_key(body) is None
                or _coverage_label(author) in _COMMENT_CONTROLS
                or _coverage_label(body) in _COMMENT_CONTROLS
                or _coverage_label(body) in _COMMENT_PLACEHOLDERS):
            continue
        # Preserve separately identified equal comments. Without source IDs,
        # repeated identical records provide no evidence of additional coverage.
        identity = ('id', row.get('source_id') or row.get('id')) if row.get('source_id') or row.get('id') else (
            'text', _author_key(author), _coverage_label(body))
        if identity not in seen:
            seen.add(identity)
            valid.append(row)
    return valid


def _comment_time_metadata(line):
    """Recognize standalone serializer timestamps, not date mentions in prose.

    Plain output consisting only of an author and date cannot distinguish a
    timestamp from a date-only comment. Native HTML body ownership remains the
    unambiguous representation for that unusual case.
    """
    stamp = visible_markdown_links(line).strip()
    return bool(re.fullmatch(
        r'(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}(?:[ T]\d{1,2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)?'
        r'|\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?'
        r'|\d+\s+(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?)\s+ago'
        r'|\d+\s*(?:秒|分钟|小时|天|周|个月|年)前|刚刚)', stamp, re.I))


def _coverage_text_records(content, contract):
    """Read explicit author/body formatting without a frozen author list.

    An unlabelled prose block cannot establish author attribution. Subheadings,
    linked/bold author lines and colon-labelled records are supported; ambiguous
    bare names are deliberately not guessed from arbitrary prose. Colon-style
    authors additionally require an explicit section heading: a plain navigation
    label mentioning comments must not turn article captions into authors.
    """
    # Code may be comment text, but cannot introduce fake record boundaries.
    fences = {}
    prefix = '\ue000coverage-fence'
    while prefix in content:
        prefix += '_'
    def protect(match):
        key = prefix + str(len(fences))
        fences[key] = match.group(0)
        return '\n' + key + '\n'
    content = re.sub(r'(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*$', protect, content)
    content = _without_markdown_images(content)
    paragraph_marker = prefix + 'paragraph'
    content = re.sub(r'\n[ \t]*\n', '\n' + paragraph_marker + '\n', content)
    content = visible_html_text(str(_comment_html(content)), preserve_source_whitespace=True, preserve_links=True)
    lines = content.replace(paragraph_marker, '').splitlines()
    markers = {_section_marker_tokens(x) for x in contract['section_markers']}
    start = next((i for i, line in enumerate(lines) if _section_marker_tokens(line) in markers), None)
    if start is None:
        return []
    section_heading = re.match(r'\s*(#{1,6})\s+', lines[start])
    section_level = len(section_heading[1]) if section_heading else 0
    rows, current = [], None
    heading_authors = False
    for offset, line in enumerate(lines[start + 1:], start + 1):
        previous_blank = not lines[offset - 1].strip()
        stripped = line.strip()
        if stripped in fences:
            if current is not None:
                current['text'] += '\n' + fences[stripped]
            continue
        heading = re.fullmatch(r'\s*(#{1,6})\s+(.+?)\s*', line)
        if heading and section_level and len(heading[1]) <= section_level:
            break
        if _coverage_label(visible_markdown_links(stripped)) in _COMMENT_CONTROLS:
            current = None
            continue
        if _section_marker_tokens(line) in markers:
            current = None
            continue
        pingback = re.fullmatch(r'\s*Pingback:\s+(.+?)\s*', line)
        if pingback:
            label = visible_markdown_links(pingback[1])
            rows.append({'author': label, 'text': visible_markdown_links(line).strip()})
            current = None
            continue
        links = [link for link in markdown_links(stripped) if not link.is_image]
        linked = len(links) == 1 and links[0].start == 0 and links[0].end == len(stripped)
        bold = re.fullmatch(r'\*\*(.+?)\*\*[:：]?', stripped)
        colon = re.fullmatch(r'([^\n:：]{1,120})[:：]\s*(.*)', stripped)
        # Colon records need a paragraph boundary; prose/code inside a comment
        # must not create new users merely by containing a colon.
        author, body = None, ''
        if heading:
            author = heading[2]
            heading_authors = True
        elif heading_authors:
            pass
        elif linked:
            author = links[0].label
        elif bold:
            author = bold[1]
        elif section_heading and colon and (current is None or previous_blank):
            author, body = colon[1], colon[2]
        elif section_heading and colon and not colon[2]:
            author = colon[1]
        if author is not None:
            current = {'author': visible_markdown_links(author), 'text': visible_markdown_links(body)}
            rows.append(current)
        elif current is not None and not _comment_time_metadata(line):
            current['text'] += '\n' + visible_markdown_links(line)
    return rows


def _verify_comment_coverage(content, contract):
    rows = (_html_records(content, contract) if _is_post_html(content)
            else _coverage_text_records(content, contract))
    valid = _valid_coverage_records(rows)
    return {'article_comments_mode': 'fixed_coverage',
            'article_comments_pass': len(valid) >= contract['minimum_comments'],
            'article_comment_count': len(valid),
            'article_comment_minimum': contract['minimum_comments']}


def _body_matches(actual, expected):
    # Short comments and deleted-message placeholders still carry real text.
    if not tokens(expected):
        return unicodedata.normalize('NFKC', actual).strip() == unicodedata.normalize('NFKC', expected).strip()
    if len(''.join(tokens(expected))) < 6:
        return tokens(actual) == tokens(expected)
    contract = body_requirements(expected, structure_hint='whole_declared_component')
    contract['minimum_region_passes'] = len(contract['regions'])
    contract['minimum_floor'] = contract['minimum_coverage']
    return evaluate_body_requirements(actual, contract)['body_coverage_pass']


def verify_article_comments(content, contract, reference, *, case_id, url, reference_context=None):
    """Apply fixed coverage, or the frozen legacy exact-reference contract."""
    validate_comment_contract(contract)
    if contract['version'] == 2:
        return _verify_comment_coverage(content, contract)
    status = _reference_status(reference, reference_context, contract, case_id, url)
    result = {'article_comments_reference_status': status, 'article_comments_reference_sha256': None,
              'article_comments_pass': False, 'article_comment_results': [],
              'article_comment_count': 0, 'article_comment_reference_count': 0,
              'article_comment_confirmed_count': 0}
    if status != 'verified':
        return result
    result['article_comments_reference_sha256'] = hashlib.sha256(json.dumps(
        reference, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    if contract.get('mode') == 'observed_absent':
        # A fresh independent observation certifies zero displayed comments;
        # marketing prose mentioning comments is not an invented component.
        result['article_comments_pass'] = True
        return result
    rows = _html_records(content, contract) if _is_post_html(content) else _text_records(content, contract, [row['author'] for row in reference['records']])
    expected = reference['records']
    # A source ID may be absent in plain output. Author plus independently owned
    # body and already matched parent establish identity without synthetic tags.
    row_authors = [_author_key(row.get('author')) for row in rows]
    ref_authors = [_author_key(ref['author']) for ref in expected]
    body_matches = lru_cache(maxsize=None)(_body_matches)
    possibilities = [{i for i, ref in enumerate(expected)
                      if row_authors[index] is not None and row_authors[index] == ref_authors[i]
                      and (not row.get('source_id') or row['source_id'] == ref['id'])
                      and body_matches(row.get('text', ''), ref['text'])}
                     for index, row in enumerate(rows)]
    # Match sibling sets as a bipartite graph. Memoized subtree compatibility
    # disambiguates identical parents through their replies without enumerating
    # factorial permutations when one late record is missing or different.
    expected_ids = {ref['id']: index for index, ref in enumerate(expected)}
    row_children, ref_children = {}, {}
    valid_tree = True
    for index, row in enumerate(rows):
        parent = row.get('parent')
        if parent is not None and (type(parent) is not int or not 0 <= parent < index):
            valid_tree = False
        row_children.setdefault(parent, []).append(index)
    for index, ref in enumerate(expected):
        parent = expected_ids.get(ref['parent_id']) if ref['parent_id'] is not None else None
        ref_children.setdefault(parent, []).append(index)
    child_pairs = {}
    def match_siblings(candidate_nodes, reference_nodes):
        if len(candidate_nodes) != len(reference_nodes):
            return None
        options = {node: [target for target in reference_nodes if compatible(node, target)]
                   for node in candidate_nodes}
        if any(not values for values in options.values()):
            return None
        matched_reference = {}
        def augment(node, visited):
            for target in options[node]:
                if target in visited:
                    continue
                visited.add(target)
                if target not in matched_reference or augment(matched_reference[target], visited):
                    matched_reference[target] = node
                    return True
            return False
        for node in sorted(candidate_nodes, key=lambda candidate: len(options[candidate])):
            if not augment(node, set()):
                return None
        return {node: target for target, node in matched_reference.items()}
    @lru_cache(maxsize=None)
    def compatible(node, target):
        if target not in possibilities[node]:
            return False
        pairs = match_siblings(row_children.get(node, []), ref_children.get(target, []))
        if pairs is None:
            return False
        child_pairs[node, target] = pairs
        return True
    roots = (match_siblings(row_children.get(None, []), ref_children.get(None, []))
             if valid_tree and len(rows) == len(expected) else None)
    mapping = {}
    if roots is not None:
        pending = list(roots.items())
        while pending:
            node, target = pending.pop()
            mapping[node] = expected[target]['id']
            pending.extend(child_pairs[node, target].items())
    matched = roots is not None and len(mapping) == len(rows)
    checks = [{'candidate_index': index, 'reference_id': mapping.get(index), 'pass': index in mapping}
              for index in range(len(rows))]
    used = set(mapping.values())
    result.update(article_comment_results=checks, article_comment_count=len(rows),
                  article_comment_reference_count=len(expected), article_comment_confirmed_count=len(used),
                  article_comments_pass=matched)
    return result
