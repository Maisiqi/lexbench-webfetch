"""Explicit mutable-document section coverage, without frozen prose matching."""
from __future__ import annotations

import math
import re
import unicodedata


def _key(text):
    # Formatting and serializer line breaks may vary; word order may not.
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())


def validate_document_structure(contract):
    if not isinstance(contract, dict) or set(contract) - {
        'version', 'headings', 'minimum_heading_coverage', 'minimum_body_chars', 'type',
    }:
        raise ValueError('Invalid document_structure fields')
    if contract.get('version') != 1 or isinstance(contract.get('version'), bool):
        raise ValueError('Unsupported document_structure version')
    if 'type' in contract and contract['type'] != 'definition':
        raise ValueError('Unsupported document structure type')
    threshold = contract.get('minimum_heading_coverage')
    if (isinstance(threshold, bool) or not isinstance(threshold, (int, float))
            or not math.isfinite(threshold) or not 0 < threshold <= 1):
        raise ValueError('Invalid document heading coverage')
    minimum = contract.get('minimum_body_chars')
    if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 1:
        raise ValueError('Invalid document body character floor')
    headings = contract.get('headings')
    if not isinstance(headings, list) or not headings:
        raise ValueError('Document structure requires evidenced headings')
    ids, texts = set(), set()
    for heading in headings:
        if not isinstance(heading, dict) or set(heading) != {'id', 'text', 'level', 'body_required'}:
            raise ValueError('Invalid document heading fields')
        if (not isinstance(heading['id'], str) or not heading['id'].strip()
                or heading['id'] in ids or not isinstance(heading['text'], str)
                or not _key(heading['text']) or _key(heading['text']) in texts):
            raise ValueError('Document headings must have unique IDs and text')
        if (isinstance(heading['level'], bool) or not isinstance(heading['level'], int)
                or not 1 <= heading['level'] <= 6 or not isinstance(heading['body_required'], bool)):
            raise ValueError('Invalid document heading level or body requirement')
        if contract.get('type') == 'definition' and (heading['level'] != 1 or not heading['body_required']):
            raise ValueError('Definitions require a local description and level 1')
        ids.add(heading['id'])
        texts.add(_key(heading['text']))
    if not any(h['body_required'] for h in headings):
        raise ValueError('A document contract needs at least one substantive section')


def _html_events(content):
    from bs4 import Comment, NavigableString
    from .dynamic_lists import scoped_html
    # Accessibility-tree hiding is not visual hiding. Reuse the shared
    # explicit HTML/inline-style visibility rules, including closed details.
    soup = scoped_html(content)
    root = soup.select_one('main') or soup.select_one('article') or soup.body or soup
    for node in root.select('nav,header,footer,aside,[role="navigation"],.toc,#toc,.reference-toc'):
        node.decompose()
    # Lists containing only local section links are tables of contents. Other
    # lists and article-specific external reading links remain body content.
    for node in list(root.select('ul,ol')):
        if not node.parent:
            continue
        links = node.select('a[href]')
        if (links and all(str(a.get('href', '')).startswith('#') for a in links)
                and _key(node.get_text()) == _key(''.join(a.get_text() for a in links))):
            node.decompose()
    events = []
    consumed = set()
    for node in root.descendants:
        if getattr(node, 'name', None) in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            events.append((node.get_text(' ', strip=True), int(node.name[-1])))
            consumed.update(id(child) for child in node.descendants)
        elif (isinstance(node, NavigableString) and not isinstance(node, Comment)
              and id(node) not in consumed and node.strip()):
            events.append((str(node).strip(), None))
    return events


def _text_events(content, headings, key_function=_key):
    # Markdown code contributes body content, but cannot declare section titles.
    lines, eligible = [], []
    fence = None
    for raw in content.splitlines():
        line = raw.strip()
        marker = re.match(r'^(`{3,}|~{3,})', line)
        if marker:
            char = marker[1][0]
            if fence is None:
                fence = char
            elif fence == char:
                fence = None
            continue
        if not line:
            continue
        if fence is None and re.fullmatch(r'(?:[-*+]\s*|\d+[.)]\s*)?\[[^]]+\]\(#[^)]*\)', line):
            continue
        level_match = re.match(r'^(#{1,6})\s+(.+?)(?:\s+#+)?$', line) if fence is None else None
        lines.append(level_match[2] if level_match else line)
        eligible.append((fence is None, len(level_match[1]) if level_match else None))
    declared = {key_function(h['text']): h for h in headings}
    prefixes = {key[:i] for key in declared for i in range(1, len(key) + 1)}
    events, index = [], 0
    while index < len(lines):
        available, explicit_level = eligible[index]
        if not available:
            events.append((lines[index], None))
            index += 1
            continue
        joined, match = '', None
        # Text serializers often split inline code/links within a heading.
        # Only complete adjacent lines, in source order, may form that heading.
        for end in range(index, min(index + 12, len(lines))):
            if not eligible[end][0] or (end > index and eligible[end][1] is not None):
                break
            joined += key_function(lines[end])
            if joined in declared:
                match = (end, declared[joined])
                break
            if joined not in prefixes:
                break
        if match:
            end, heading = match
            events.append((heading['text'], heading['level']))
            index = end + 1
        else:
            events.append((lines[index], explicit_level))
            index += 1
    return events



def _definition_key(text):
    # Preserve signature punctuation and argument order; tolerate inline-code
    # formatting and serializer whitespace, not bare API names.
    return re.sub(r'[\s`¶]', '', unicodedata.normalize('NFKC', text).casefold())


def _definition_html_events(content):
    from .dynamic_lists import scoped_html
    soup = scoped_html(content)
    root = soup.select_one('main') or soup.select_one('article') or soup.body or soup
    for node in root.select('nav,header,footer,aside,[role="navigation"],.toc,#toc,.reference-toc'):
        node.decompose()
    events = []
    for term in root.select('dt'):
        for anchor in term.select('.headerlink'):
            anchor.decompose()
        events.append((term.get_text('', strip=False).strip(), 1))
        description = term.find_next_sibling()
        # A term cannot borrow unrelated paragraphs or another term's dd.
        if description is not None and description.name == 'dd':
            events.append((description.get_text(' ', strip=True), None))
    return events

def evaluate_document_structure(content, contract, *, html_document=False):
    if not contract:
        return {}
    validate_document_structure(contract)
    definitions = contract.get('type') == 'definition'
    key_function = _definition_key if definitions else _key
    if definitions:
        events = (_definition_html_events(content) if html_document else
                  _text_events(content, contract['headings'], key_function))
    else:
        events = (_html_events(content) if html_document else
                  _text_events(content, contract['headings']))
    declared = {key_function(h['text']): h for h in contract['headings']}
    # Serializers may change heading levels. The declared source hierarchy
    # determines which subsequent text belongs to a registered section.
    events = [(text, declared[key_function(text)]['level']
               if level is not None and key_function(text) in declared else level)
              for text, level in events]
    supported = set()
    found = set()
    definition_body_indices = set()
    for index, (text, level) in enumerate(events):
        heading = declared.get(key_function(text)) if level is not None else None
        if heading is None:
            continue
        found.add(heading['id'])
        end = next((i for i in range(index + 1, len(events))
                    if events[i][1] is not None and events[i][1] <= level), len(events))
        if definitions:
            definition_body_indices.update(i for i in range(index + 1, end) if events[i][1] is None)
        has_body = any(event_level is None and bool(_key(value))
                       for value, event_level in events[index + 1:end])
        if has_body or not heading['body_required']:
            supported.add(heading['id'])
    body_chars = sum(len(text) for i, (text, level) in enumerate(events)
                     if level is None and (not definitions or i in definition_body_indices))
    coverage = len(supported) / len(declared)
    return {
        'document_structure_pass': (coverage >= contract['minimum_heading_coverage']
                                    and body_chars >= contract['minimum_body_chars']),
        'document_heading_coverage': coverage,
        'document_body_chars': body_chars,
        'document_minimum_body_chars': contract['minimum_body_chars'],
        'document_heading_results': [
            {'id': h['id'], 'present': h['id'] in found, 'pass': h['id'] in supported}
            for h in contract['headings']
        ],
    }
