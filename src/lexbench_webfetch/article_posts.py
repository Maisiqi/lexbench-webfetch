"""Pure post ownership and body verification against an independent observation."""
import hashlib
import json
import math
import re
from datetime import datetime
from urllib.parse import urljoin, urlsplit

import soupsieve

from .body_coverage import body_requirements, evaluate_body_requirements, tokens, compact_ngrams
from .dynamic_lists import _scoped_html, named_entry_identity, visible_html_text
from .reference_quality import is_html_document_or_fragment, markdown_links, visible_markdown_links


def validate_post_contract(contract):
    """Raise ValueError for malformed frozen post extraction contracts."""
    try:
        allowed = {'version', 'hosts', 'entry_path', 'html_record_selector',
                   'html_permalink_selector', 'html_author_selector', 'html_body_selector',
                   'html_quote_selector', 'quote_markers', 'required_ratio', 'max_reference_age_seconds',
                   'allow_empty_outer_with_quotes'}
        if not isinstance(contract, dict) or set(contract) - allowed:
            raise ValueError('unknown frozen post contract fields')
        if type(contract['version']) is not int or contract['version'] != 1 or not isinstance(contract['hosts'], list) or not contract['hosts']:
            raise ValueError('invalid version or hosts')
        if any(not isinstance(h, str) or not h or '/' in h for h in contract['hosts']):
            raise ValueError('invalid hosts')
        re.compile(contract['entry_path'])
        for key in ('html_record_selector', 'html_permalink_selector', 'html_author_selector', 'html_body_selector'):
            if not isinstance(contract[key], str) or not contract[key].strip():
                raise ValueError('empty selector')
            soupsieve.compile(contract[key])
        soupsieve.compile(contract.get('html_quote_selector', 'blockquote'))
        for key in ('required_ratio', 'max_reference_age_seconds'):
            v = contract[key]
            if type(v) not in (int, float) or not math.isfinite(v) or v <= 0:
                raise ValueError('invalid numeric bound')
        if contract['required_ratio'] > 1:
            raise ValueError('invalid ratio')
        if type(contract.get('allow_empty_outer_with_quotes', False)) is not bool:
            raise ValueError('invalid empty outer opt-in')
        markers = contract.get('quote_markers', [])
        if not isinstance(markers, list) or any(not isinstance(x, str) or not x.strip() for x in markers):
            raise ValueError('invalid quote markers')
    except (KeyError, TypeError, re.error, soupsieve.SelectorSyntaxError) as error:
        raise ValueError('invalid post contract') from error


def _identity(value, contract, base):
    destination = urljoin(base, value)
    p = urlsplit(destination)
    p.port  # Force validation; hostname alone accepts malformed port text.
    if (p.scheme not in {'http', 'https'} or p.hostname not in contract['hosts']
            or p.username or p.password or not re.fullmatch(contract['entry_path'], p.path.rstrip('/'))):
        raise ValueError('invalid post URL')
    return named_entry_identity(destination, contract)


def _utc(value):
    stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
        raise ValueError('UTC timestamp required')
    return stamp


def _part_contract(part):
    text = part['text']
    contract = body_requirements(text)
    if 'source_line_ranges' in part:
        lines, cursor, regions = text.splitlines(), 1, []
        ranges = part['source_line_ranges']
        if not isinstance(ranges, list) or not 1 <= len(ranges) <= 5:
            raise ValueError('invalid source ranges')
        for span in ranges:
            if (not isinstance(span, list) or len(span) != 2 or any(type(n) is not int for n in span)
                    or span[0] != cursor or not span[0] <= span[1] <= len(lines)):
                raise ValueError('ranges must partition the whole body part')
            region = body_requirements('\n'.join(lines[span[0]-1:span[1]]),
                                       structure_hint='whole_declared_component')['regions']
            if len(region) != 1:
                raise ValueError('empty source region')
            regions.append({**region[0], 'id': f'post-region-{len(regions)+1}'})
            cursor = span[1] + 1
        if cursor != len(lines)+1:
            raise ValueError('ranges omit the end')
        contract['regions'] = regions
    if any(not compact_ngrams(r['text'], 6) for r in contract['regions']):
        raise ValueError('body regions require six-character matching units')
    contract['minimum_region_passes'] = len(contract['regions'])
    contract['minimum_floor'] = contract['minimum_coverage']
    return contract


def _reference_status(reference, context, contract, case_id, url):
    if reference is None:
        return 'missing'
    try:
        if (type(reference['version']) is not int or reference['version'] != 1 or reference['case_id'] != case_id or reference['url'] != url
                or reference['scope'] != 'initial_load_only'
                or not isinstance(reference['context_id'], str) or not reference['context_id']):
            return 'invalid'
        observed = _utc(reference['observed_at'])
        records, seen = reference['records'], set()
        if not isinstance(records, list) or not records:
            return 'invalid'
        for row in records:
            key = _identity(row['url'], contract, url)
            if key in seen or not isinstance(row['author'], str) or not tokens(row['author']):
                return 'invalid'
            seen.add(key)
            parts = row['body_parts']
            if (not isinstance(parts, list) or not parts or parts[0].get('kind') != 'post'
                    or any(p.get('kind') != 'quote' for p in parts[1:])):
                return 'invalid'
            for index, part in enumerate(parts):
                if (part['kind'] not in {'post', 'quote'} or part['complete_initial_text'] is not True
                        or not isinstance(part['text'], str)):
                    return 'invalid'
                if 'author' in part and (not isinstance(part['author'], str) or not tokens(part['author'])):
                    return 'invalid'
                if 'empty_outer_text' in part:
                    # This independent observation cannot excuse omitted prose or
                    # an empty quote. Every owned quote still needs attribution.
                    if (not contract.get('allow_empty_outer_with_quotes', False)
                            or part['empty_outer_text'] is not True or index != 0
                            or part['text'] != '' or 'source_line_ranges' in part or len(parts) < 2
                            or any(not isinstance(p.get('author'), str) or not tokens(p['author'])
                                   for p in parts[1:])):
                        return 'invalid'
                    continue
                if not tokens(part['text']):
                    return 'invalid'
                _part_contract(part)
        if not isinstance(context, dict) or context.get('id') != reference['context_id']:
            return 'context_mismatch'
        age = (_utc(context['started_at'])-observed).total_seconds()
        if age < 0:
            return 'context_mismatch'
        if age > contract['max_reference_age_seconds']:
            return 'stale'
    except (KeyError, TypeError, ValueError, AttributeError):
        return 'invalid'
    return 'verified'


def _owned_body_text(node, contract):
    surface = _scoped_html(str(node))
    # Field-node ownership alone does not exclude a nested card's text.
    for nested in list(surface.select(contract['html_record_selector'])):
        if nested.parent is not None:
            nested.decompose()
    return visible_html_text(str(surface))


def _is_post_html(content):
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


def _html_records(content, contract):
    soup, rows = _scoped_html(content), []
    # With scripting enabled, fallback markup is not displayed article text.
    for fallback in list(soup.select('noscript')):
        if fallback.parent is not None:
            fallback.decompose()
    selector = contract.get('html_quote_selector', 'blockquote')
    for card in soup.select(contract['html_record_selector']):
        def owned(node):
            return node.find_parent(lambda x: soupsieve.match(contract['html_record_selector'], x)) is card
        quotes = [x for x in card.select(selector) if owned(x)
                  and not x.find_parent(lambda p: p is not card and soupsieve.match(selector, p))]
        def outer(node):
            return owned(node) and not any(node is q or q in node.parents for q in quotes)
        fields = [[x for x in card.select(contract[key]) if outer(x)] for key in
                  ('html_permalink_selector', 'html_author_selector', 'html_body_selector')]
        if any(len(x) != 1 for x in fields):
            rows.append({})
            continue
        link, author, body = [x[0] for x in fields]
        quote_text = [_owned_body_text(x, contract) for x in quotes]
        quote_authors = [[a.get_text(' ', strip=True)
                          for a in x.select(contract['html_author_selector'])
                          if owned(a) and a.find_parent(
                              lambda p: soupsieve.match(selector, p)) is x]
                         for x in quotes]
        for quote in quotes:
            quote.extract()
        rows.append({'url': link.get('href', ''), 'author': author.get_text(' ', strip=True),
                     'post': _owned_body_text(body, contract), 'quote': quote_text,
                     'quote_authors': quote_authors})
    return rows


def _markdown_records(content, contract, url):
    # A fenced reference or source dump is not a rendered article record.
    content = re.sub(r'(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*$', '', content)
    # HTML visibility projection drops empty lines. Preserve Markdown paragraph
    # boundaries across that projection so a blockquote cannot absorb a later
    # unquoted paragraph. Choose a marker absent from the answer itself.
    paragraph_marker = '\ue000post-paragraph-break\ue001'
    while paragraph_marker in content:
        paragraph_marker += '_'
    content = re.sub(r'\n[ \t]*\n', '\n'+paragraph_marker+'\n', content)
    content = visible_html_text(content, preserve_source_whitespace=True, preserve_links=True)
    content = content.replace(paragraph_marker, '')
    lines, headers = content.splitlines(), []
    for index, line in enumerate(lines):
        links = [link for link in markdown_links(line) if not link.is_image]
        if not links or line.lstrip().startswith('>'):
            continue
        if len(links) > 1:
            first, last = links[0], links[-1]
            prefix, suffix = line[:first.start].strip(), line[last.end:].strip()
            if (not re.match(r'^(?:#{1,6}|[-*+]|\d+[.)])(?:\s|$)', prefix)
                    or suffix.strip(' |—–-:*_')):
                continue
            author = visible_markdown_links(first.label)
            destination = 'about:invalid-post-heading'
            # A linked author profile may precede exactly one owning post
            # permalink. Other explicit linked headings still end the prior
            # record, but cannot supply a valid record of their own.
            if (len(links) == 2 and re.fullmatch(r'(?:#{1,6}|[-*+]|\d+[.)])', prefix)
                    and not line[first.end:last.start].strip(' |·—–-:*_')):
                try:
                    profile = urlsplit(urljoin(url, first.destination))
                    profile.port
                    if (profile.scheme in {'http', 'https'}
                            and profile.hostname in contract['hosts']
                            and not profile.username and not profile.password
                            and not re.fullmatch(contract['entry_path'], profile.path.rstrip('/'))):
                        _identity(last.destination, contract, url)
                        destination = last.destination
                except ValueError:
                    pass
            headers.append((index, destination, visible_markdown_links(line), author))
            continue
        link = links[0]
        prefix, suffix = line[:link.start].strip(), line[link.end:].strip()
        explicit_header = bool(re.match(r'^(?:#{1,6}|[-*+]|\d+[.)])(?:\s|$)', prefix))
        if suffix.strip(' |—–-:*_') or (prefix and not explicit_header):
            continue
        try:
            _identity(link.destination, contract, url)
        except ValueError:
            # An explicit linked post heading still ends the previous post,
            # even when its own URL is invalid. Ordinary inline links do not.
            if not explicit_header:
                continue
        header = visible_markdown_links(line)
        author = re.sub(r'^(?:#{1,6}|[-*+]|\d+[.)])(?:\s+|$)', '', prefix).strip()
        if not author:
            author = visible_markdown_links(link.label)
        if not prefix and index and lines[index-1].strip() and not lines[index-1].startswith('>'):
            author = visible_markdown_links(lines[index-1])
            header = author+'\n'+header
        headers.append((index, link.destination, header, author))
    rows = []
    markers = {x.casefold().rstrip(':：') for x in contract.get('quote_markers', [])}
    for n, (start, destination, header, author) in enumerate(headers):
        end = headers[n+1][0] if n+1 < len(headers) else len(lines)
        post, quotes, current = [], [], None
        quote_mode, paragraph_break = None, False
        for line in lines[start+1:end]:
            if line.strip().strip('*_').rstrip(':：').casefold() in markers:
                if current is not None:
                    quotes.append('\n'.join(current))
                current = []
                quote_mode, paragraph_break = 'marker', False
            elif line.lstrip().startswith('>'):
                if current is None:
                    current = []
                    quote_mode = 'blockquote'
                paragraph_break = False
                current.append(re.sub(r'^\s*>\s?', '', line))
            elif current is not None:
                if quote_mode == 'blockquote' and paragraph_break and line.strip():
                    # Lazy continuation belongs to the current paragraph; a
                    # new unquoted paragraph belongs to the owning outer post.
                    quotes.append('\n'.join(current))
                    current, quote_mode = None, None
                    post.append(line)
                else:
                    current.append(line)
                    if not line.strip():
                        paragraph_break = True
            else:
                post.append(line)
        if current is not None:
            quotes.append('\n'.join(current))
        rows.append({'url': destination, 'author_header': header, 'author': author,
                     'whole_post': visible_markdown_links('\n'.join(lines[start+1:end])),
                     'post': visible_markdown_links('\n'.join(post)),
                     'quote': [visible_markdown_links(x) for x in quotes],
                     'quote_authors': [[visible_markdown_links(next(
                         (line.strip() for line in x.splitlines() if line.strip()), ''))]
                                       for x in quotes],
                     'quote_bodies_after_author': [visible_markdown_links('\n'.join(
                         x.lstrip().splitlines()[1:])) for x in quotes]})
    return rows


def verify_article_posts(content, contract, reference, *, case_id, url, reference_context=None):
    """Verify bodies only after validating the independent reference boundary."""
    validate_post_contract(contract)
    status = _reference_status(reference, reference_context, contract, case_id, url)
    result = {'article_reference_status': status, 'article_reference_sha256': None,
              'article_posts_pass': False, 'article_post_results': [], 'article_post_count': 0,
              'article_post_confirmed_count': 0, 'article_post_reference_count': 0}
    if status != 'verified':
        return result
    result['article_reference_sha256'] = hashlib.sha256(json.dumps(
        reference, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    expected = {_identity(x['url'], contract, url): x for x in reference['records']}
    rows = (_html_records(content, contract) if _is_post_html(content)
            else _markdown_records(content, contract, url))
    seen, checks = set(), []
    for row in rows:
        check = {'url': row.get('url'), 'pass': False, 'body_part_results': []}
        try:
            key = _identity(row['url'], contract, url)
            if key in seen:
                check['reason'] = 'duplicate'
            elif key not in expected:
                check['reason'] = 'unknown'
            else:
                ref = expected[key]
                author, header = tokens(ref['author']), tokens(row.get('author', row.get('author_header', '')))
                author_pass = (header == author if 'author' in row else any(
                    header[i:i+len(author)] == author for i in range(len(header)-len(author)+1)))
                if len(ref['body_parts']) == 1 and 'whole_post' in row:
                    # Literal greater-than lines can be original post prose,
                    # rather than a quoted post, when no quote was observed.
                    row = {**row, 'post': row['whole_post'], 'quote': []}
                quote_index = 0
                for part in ref['body_parts']:
                    actual = row['post'] if part['kind'] == 'post' else (
                        row['quote'][quote_index] if quote_index < len(row['quote']) else '')
                    quote_author_pass = True
                    if part['kind'] == 'quote' and part.get('author'):
                        candidates = (row.get('quote_authors', [])[quote_index]
                                      if quote_index < len(row.get('quote_authors', [])) else [actual])
                        quote_author_pass = any(tokens(part['author']) == tokens(a) for a in candidates)
                        if 'author_header' in row:
                            # The explicit first quote line owns attribution;
                            # mentions in body prose cannot substitute for it.
                            actual = (row['quote_bodies_after_author'][quote_index]
                                      if quote_index < len(row['quote_bodies_after_author']) else '')
                    quote_index += part['kind'] == 'quote'
                    if part.get('empty_outer_text') is True:
                        coverage = {'body_coverage_pass': not actual.strip(), 'empty_outer_text': True}
                    else:
                        coverage = evaluate_body_requirements(actual, _part_contract(part))
                    check['body_part_results'].append({'kind': part['kind'], 'author_pass': quote_author_pass, **coverage})
                check['author_pass'] = author_pass
                check['pass'] = (author_pass and len(row['quote']) == quote_index
                                 and all(x['body_coverage_pass'] and x['author_pass'] for x in check['body_part_results']))
            seen.add(key)
        except (KeyError, ValueError):
            check['reason'] = 'invalid_record'
        checks.append(check)
    confirmed = sum(x['pass'] for x in checks)
    result.update(article_post_results=checks, article_post_count=len(rows),
                  article_post_reference_count=len(expected), article_post_confirmed_count=confirmed,
                  article_posts_pass=(bool(rows) and all(x['pass'] for x in checks)
                                      and confirmed >= math.ceil(len(expected)*contract['required_ratio'])))
    return result
