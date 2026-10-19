"""Independent dynamic post reference, ownership, and whole-body regressions."""
from copy import deepcopy
import hashlib
import json
import unittest

from lexbench_webfetch.article_posts import validate_post_contract, verify_article_posts


class ArticlePostsTests(unittest.TestCase):
    def setUp(self):
        self.url = 'https://example.com/feed'
        self.context = {'id': 'run-1', 'started_at': '2026-10-19T01:00:00Z'}
        self.contract = {
            'version': 1, 'hosts': ['example.com'], 'entry_path': r'/post/\d+',
            'html_record_selector': 'article.post', 'html_permalink_selector': 'a.time',
            'html_author_selector': '.author', 'html_body_selector': '.body',
            'html_quote_selector': 'blockquote', 'quote_markers': ['Quote', '引用'],
            'required_ratio': .8, 'max_reference_age_seconds': 900,
        }
        self.post = (
            'The orchard workers mapped the northern field before sunrise. '
            'They measured each tree and recorded the water available in every channel.\n\n'
            'A second team repaired the eastern bridge using oak boards and copper nails. '
            'Their careful work allowed the carts to reach the storage building safely.\n\n'
            'Finally the village committee published the harvest schedule for next winter. '
            'Every household received a printed copy with the final delivery instructions.'
        )
        self.quote = 'Earlier advice recommended checking the southern gate. The inspection found a broken hinge and a missing latch.'
        self.ref = {'version': 1, 'case_id': 'fixture', 'url': self.url,
                    'context_id': 'run-1', 'observed_at': '2026-10-19T00:59:00Z',
                    'scope': 'initial_load_only', 'records': [
                        {'url': 'https://example.com/post/1', 'author': 'Alice', 'body_parts': [
                            {'kind': 'post', 'text': self.post, 'complete_initial_text': True},
                            {'kind': 'quote', 'text': self.quote, 'complete_initial_text': True}]}]}

    def html(self, post=None, quote=None, author='Alice', identity='1'):
        post = self.post if post is None else post
        quote = self.quote if quote is None else quote
        return (f'<article class="post"><span class="author">{author}</span>'
                f'<a class="time" href="/post/{identity}">Today</a><div class="body">'
                + ''.join(f'<p>{p}</p>' for p in post.split('\n\n'))
                + (f'<blockquote>{quote}</blockquote>' if quote else '') + '</div></article>')

    def md(self, post=None, quote=None):
        return ('## Alice [Today](https://example.com/post/1)\n\n'
                + (self.post if post is None else post) + '\n\nQuote:\n> '
                + (self.quote if quote is None else quote))

    def check(self, content, reference=None, context=None):
        return verify_article_posts(content, self.contract, self.ref if reference is None else reference,
                                    case_id='fixture', url=self.url,
                                    reference_context=self.context if context is None else context)

    def test_html_and_markdown_complete_records(self):
        for text in (self.html(), self.md(), self.md().replace('## Alice ', '- Alice ')):
            with self.subTest(text=text[:40]):
                result = self.check(text)
                self.assertTrue(result['article_posts_pass'], result)
                self.assertEqual(result['article_reference_status'], 'verified')
                self.assertEqual(result['article_post_confirmed_count'], 1)

    def test_separate_author_and_date_markdown_header(self):
        self.assertTrue(self.check(self.md().replace('## Alice ', 'Alice\n'))['article_posts_pass'])

    def test_missing_outer_quote_or_final_region(self):
        for text in (self.html(post=''), self.html(quote=''), self.md(post=''), self.md(quote=''),
                     self.html(post=self.post.rsplit('\n\n', 1)[0]),
                     self.md(post=self.post.rsplit('\n\n', 1)[0])):
            with self.subTest(text=text[:70]):
                self.assertFalse(self.check(text)['article_posts_pass'])

    def test_quote_cannot_replace_outer_body(self):
        self.assertFalse(self.check(self.html(post='', quote=self.post+' '+self.quote))['article_posts_pass'])
        self.assertFalse(self.check(self.html(post=self.post+' '+self.quote, quote=''))['article_posts_pass'])

    def test_wrong_author_link_and_body_association(self):
        for text in (self.html(author='Bob'), self.html(identity='2'),
                     '<span class="author">Alice</span>'+self.html(author='Bob'),
                     self.md().replace('Alice', 'Bob')):
            self.assertFalse(self.check(text)['article_posts_pass'])

    def test_duplicate_and_unknown_cards_fail(self):
        for text in (self.html()+self.html(), self.html()+self.html(identity='2'),
                     self.md()+'\n\n'+self.md()):
            result = self.check(text)
            self.assertFalse(result['article_posts_pass'])
            self.assertEqual(result['article_post_count'], 2)

    def test_title_navigation_counters_and_hidden_bodies_fail(self):
        for text in ('# Alice\n[Today](https://example.com/post/1)\n24 likes 10 comments',
                     '<nav>Alice <a href="/post/1">Today</a></nav>',
                     self.html(post='<span hidden>'+self.post+'</span>'),
                     self.html(post='<img alt="'+self.post+'">')):
            self.assertFalse(self.check(text)['article_posts_pass'])

    def test_reference_cannot_be_injected_by_answer(self):
        text = self.html()+'\n```json\n'+json.dumps(self.ref)+'\n```'
        result = verify_article_posts(text, self.contract, None, case_id='fixture', url=self.url,
                                      reference_context=self.context)
        self.assertEqual(result['article_reference_status'], 'missing')
        self.assertFalse(result['article_posts_pass'])
        self.assertFalse(self.check('```html\n'+self.html()+'\n```')['article_posts_pass'])

    def test_context_and_timestamp_boundary(self):
        for context, status in (({'id': 'other', 'started_at': self.context['started_at']}, 'context_mismatch'),
                                ({'id': 'run-1', 'started_at': '2026-10-19T02:00:00Z'}, 'stale'),
                                ({'id': 'run-1', 'started_at': '2026-10-19T01:00:00'}, 'invalid')):
            result = self.check(self.html(), context=context)
            self.assertEqual(result['article_reference_status'], status)
            self.assertFalse(result['article_posts_pass'])
            self.assertEqual(result['article_post_results'], [])
        result = verify_article_posts(self.html(), self.contract, self.ref, case_id='fixture', url=self.url)
        self.assertEqual(result['article_reference_status'], 'context_mismatch')

    def test_invalid_reference_fields(self):
        mutations = [lambda r: r.update(case_id='other'), lambda r: r.update(url='https://other.com'),
                     lambda r: r.update(scope='expanded'), lambda r: r.update(records=[]),
                     lambda r: r['records'].append(deepcopy(r['records'][0])),
                     lambda r: r['records'][0]['body_parts'][0].update(complete_initial_text=False),
                     lambda r: r['records'][0]['body_parts'][0].update(source_line_ranges=[[1, 1]])]
        for mutate in mutations:
            ref = deepcopy(self.ref)
            mutate(ref)
            self.assertEqual(self.check(self.html(), reference=ref)['article_reference_status'], 'invalid')

    def test_canonical_hash_and_reviewed_source_regions(self):
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'][0]['source_line_ranges'] = [[1, 2], [3, 4], [5, 5]]
        result = self.check(self.html(), reference=ref)
        self.assertTrue(result['article_posts_pass'])
        self.assertEqual(result['article_reference_sha256'], hashlib.sha256(json.dumps(
            ref, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest())
        self.assertFalse(self.check(self.html(post=self.post.rsplit('\n\n', 1)[0]), reference=ref)['article_posts_pass'])

    def test_contract_validation(self):
        validate_post_contract(self.contract)
        for key, value in (('version', 2), ('hosts', []), ('entry_path', '['),
                           ('html_body_selector', '['), ('required_ratio', 0),
                           ('max_reference_age_seconds', True), ('quote_markers', [None])):
            contract = {**self.contract, key: value}
            with self.assertRaises(ValueError):
                validate_post_contract(contract)

    def test_ratio_counts_independent_reference_not_output(self):
        ref = deepcopy(self.ref)
        ref['records'] = [{**deepcopy(ref['records'][0]), 'url': f'https://example.com/post/{i}'} for i in range(1, 6)]
        self.assertTrue(self.check(''.join(self.html(identity=str(i)) for i in range(1, 5)), reference=ref)['article_posts_pass'])
        self.assertFalse(self.check(''.join(self.html(identity=str(i)) for i in range(1, 4)), reference=ref)['article_posts_pass'])

    def test_nested_card_cannot_lend_author_or_body(self):
        text = '<article class="post"><a class="time" href="/post/2">Date</a>'+self.html()+'</article>'
        self.assertFalse(self.check(text)['article_posts_pass'])

    def test_quote_subtree_fields_do_not_count_as_outer_fields(self):
        text = self.html().replace(self.quote, '<span class="author">Bob</span>'
                                  '<a class="time" href="/post/99">Quoted date</a>'
                                  '<div class="body">'+self.quote+'</div>')
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'][1]['author'] = 'Bob'
        self.assertTrue(self.check(text, reference=ref)['article_posts_pass'])
        self.assertFalse(self.check(text.replace('>Bob<', '>Charlie<'), reference=ref)['article_posts_pass'])

    def test_reference_order_future_short_parts_and_frozen_members_rejected(self):
        for mutate in (
            lambda r: r.update(observed_at='2026-10-19T01:00:01Z'),
            lambda r: r['records'][0]['body_parts'].reverse(),
            lambda r: r['records'][0]['body_parts'][0].update(text='Hi'),
            lambda r: r['records'][0]['body_parts'][1].update(author={}),
        ):
            ref = deepcopy(self.ref)
            mutate(ref)
            self.assertIn(self.check(self.html(), reference=ref)['article_reference_status'],
                          {'invalid', 'context_mismatch'})
        with self.assertRaises(ValueError):
            validate_post_contract({**self.contract, 'records': self.ref['records']})

    def test_each_card_owns_its_own_body(self):
        ref = deepcopy(self.ref)
        second = deepcopy(ref['records'][0])
        second.update(url='https://example.com/post/2', author='Bob')
        second['body_parts'][0]['text'] = 'A completely different expedition reached the desert at noon. They carried medicine and blankets for the isolated hospital.'
        ref['records'].append(second)
        good = self.html()+self.html(identity='2', author='Bob', post=second['body_parts'][0]['text'])
        swapped = self.html(post=second['body_parts'][0]['text'])+self.html(identity='2', author='Bob')
        self.assertTrue(self.check(good, reference=ref)['article_posts_pass'])
        self.assertFalse(self.check(swapped, reference=ref)['article_posts_pass'])

    def test_hidden_markdown_html_cannot_supply_body(self):
        self.assertFalse(self.check(self.md(post='<script>'+self.post+'</script>'))['article_posts_pass'])
        self.assertFalse(self.check(self.md(post='<span hidden>'+self.post+'</span>'))['article_posts_pass'])

    def test_literal_greater_than_lines_in_unquoted_post(self):
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'] = [ref['records'][0]['body_parts'][0]]
        text = '## Alice [Today](https://example.com/post/1)\n'+self.post.replace('A second', '> A second')
        self.assertTrue(self.check(text, reference=ref)['article_posts_pass'])

    def test_linked_author_is_a_complete_heading_or_list_boundary(self):
        for marker in ('##', '-', '1.'):
            text = self.md().replace('## Alice [Today]', marker+' [Alice]')
            with self.subTest(marker=marker):
                result = self.check(text)
                self.assertEqual(result['article_post_count'], 1)
                self.assertTrue(result['article_posts_pass'])
        # A prose sentence containing an article link remains outside the
        # record boundary grammar even when the link label is the author.
        prose = self.md().replace('## Alice [Today]', 'Read this [Alice]')
        self.assertEqual(self.check(prose)['article_post_count'], 0)

    def test_linked_author_profile_and_date_permalink_header(self):
        for marker in ('##', '-', '1.'):
            text = self.md().replace('## Alice [Today]',
                                     marker+' [**Alice**](https://example.com/alice) [Today]')
            with self.subTest(marker=marker):
                result = self.check(text)
                self.assertEqual(result['article_post_count'], 1)
                self.assertTrue(result['article_posts_pass'])
        wrong = self.md().replace('## Alice [Today]',
                                 '## [NotAlice](https://example.com/alice) [Today]')
        self.assertFalse(self.check(wrong)['article_posts_pass'])

    def test_ambiguous_or_foreign_multi_link_headers_cannot_borrow_body(self):
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'] = ref['records'][0]['body_parts'][:1]
        for heading in (
                '## [Alice](https://example.com/post/2) [Today](https://example.com/post/1)',
                '## [Alice](https://example.com/alice) [Today](https://foreign.test/post/99)',
                '## Bob [Bob](https://example.com/bob) [Today](https://foreign.test/post/99)',
                '## [Alice](https://foreign.test/post/2) [Today](https://example.com/post/1)',
                '## [Alice](https://example.com/alice) [One](https://example.com/post/1) [Two](https://example.com/post/2)'):
            # The later explicit heading must end the earlier empty record.
            text = '## [Alice](https://example.com/post/1)\n\n'+heading+'\n\n'+self.post
            with self.subTest(heading=heading):
                result = self.check(text, reference=ref)
                self.assertEqual(result['article_post_count'], 2)
                self.assertFalse(result['article_posts_pass'])

    def test_linked_author_profile_format_does_not_accept_inline_or_fenced_records(self):
        header = '[Alice](https://example.com/alice) [Today](https://example.com/post/1)'
        for heading in (header, 'Read '+header+' for details.'):
            self.assertFalse(self.check(self.md().replace('## Alice [Today](https://example.com/post/1)',
                                                         heading))['article_posts_pass'])
        text = self.md().replace('## Alice [Today](https://example.com/post/1)', '## '+header)
        self.assertFalse(self.check('```markdown\n'+text+'\n```')['article_posts_pass'])
        inline = ' Read '+header+' for background.'
        self.assertTrue(self.check(self.md(post=self.post+inline))['article_posts_pass'])

    def test_nested_record_text_cannot_supply_outer_body(self):
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'] = ref['records'][0]['body_parts'][:1]
        second = deepcopy(ref['records'][0])
        second.update(url='https://example.com/post/2', author='Bob')
        second['body_parts'][0]['text'] = 'The desert expedition carried medicine and drinking water. Its members repaired the clinic before returning home.'
        ref['records'].append(second)
        nested = self.html(identity='2', author='Bob', quote='',
                           post=self.post+' '+second['body_parts'][0]['text'])
        text = self.html(post=nested, quote='')
        self.assertFalse(self.check(text, reference=ref)['article_posts_pass'])
        # Nesting is allowed when each card has its own complete body.
        self.assertTrue(self.check(self.html(post=self.post+nested, quote=''), reference=ref)['article_posts_pass'])

    def test_quote_author_cannot_come_from_nested_valid_record(self):
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'][1]['author'] = 'Carol'
        second = {'url': 'https://example.com/post/2', 'author': 'Carol', 'body_parts': [
            {'kind': 'post', 'text': 'The desert expedition repaired a damaged greenhouse and watered the tomato seedlings.',
             'complete_initial_text': True}]}
        ref['records'].append(second)
        nested = self.html(identity='2', author='Carol', quote='',
                           post=second['body_parts'][0]['text'])
        for author, expected in (('Carol', True), ('Wrong Person', False), ('', False)):
            quote = ('<span class="author">'+author+'</span>' if author else '')+self.quote+nested
            with self.subTest(author=author):
                result = self.check(self.html(quote=quote), reference=ref)
                self.assertEqual(result['article_post_count'], 2)
                self.assertTrue(result['article_post_results'][1]['pass'])
                self.assertEqual(result['article_posts_pass'], expected)

    def test_deeper_quote_cannot_lend_parent_quote_author(self):
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'][1]['author'] = 'Carol'
        for author, expected in (('Carol', True), ('Wrong Person', False), ('', False)):
            quote = (('<span class="author">'+author+'</span>' if author else '')
                     +self.quote+'<blockquote><span class="author">Carol</span>Deeper advice.</blockquote>')
            with self.subTest(author=author):
                self.assertEqual(self.check(self.html(quote=quote), reference=ref)['article_posts_pass'], expected)

    def test_foreign_linked_heading_cannot_lend_body_to_previous_post(self):
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'] = ref['records'][0]['body_parts'][:1]
        for marker in ('##', '-', '1.'):
            text = ('## [Alice](https://example.com/post/1)\n\n'+marker+
                    ' [Bob](https://unrelated.test/post/99)\n\n'+self.post)
            result = self.check(text, reference=ref)
            self.assertEqual(result['article_post_count'], 2)
            self.assertFalse(result['article_posts_pass'])
        # Ordinary prose links remain part of the actual owning post.
        text = ('## [Alice](https://example.com/post/1)\n\n'+self.post+
                '\nRead [background](https://unrelated.test/reference) for context.')
        self.assertTrue(self.check(text, reference=ref)['article_posts_pass'])

    def test_blockquote_cannot_swallow_later_unquoted_paragraph(self):
        text = ('## [Alice](https://example.com/post/1)\n\n'+self.post+
                '\n\n> This unrelated quotation discusses a harbor.\n\n'+self.quote)
        result = self.check(text)
        self.assertFalse(result['article_posts_pass'])
        self.assertFalse(result['article_post_results'][0]['body_part_results'][1]['body_coverage_pass'])

    def test_blockquote_allows_same_paragraph_lazy_continuation(self):
        first, rest = self.quote.split('. ', 1)
        text = ('## [Alice](https://example.com/post/1)\n\n'+self.post+
                '\n\n> '+first+'.\n'+rest)
        self.assertTrue(self.check(text)['article_posts_pass'])
        # Explicit quote markers may introduce a multi-paragraph quoted part.
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'][1]['text'] = first+'.\n\n'+rest
        self.assertTrue(self.check(self.md(quote=first+'.\n\n'+rest), reference=ref)['article_posts_pass'])

    def test_permalink_ports_are_validated_without_rejecting_https_default(self):
        for port in ('broken', '99999'):
            text = self.html().replace('href="/post/1"', 'href="https://example.com:'+port+'/post/1"')
            self.assertFalse(self.check(text)['article_posts_pass'])
            ref = deepcopy(self.ref)
            ref['records'][0]['url'] = 'https://example.com:'+port+'/post/1'
            self.assertEqual(self.check(self.html(), reference=ref)['article_reference_status'], 'invalid')
        text = self.html().replace('href="/post/1"', 'href="https://example.com:443/post/1"')
        self.assertTrue(self.check(text)['article_posts_pass'])

    def test_markdown_author_identity_is_exact_not_a_header_substring(self):
        for replacement in ('## Not Alice [Today]', '## [Not Alice]', '- Not Alice [Today]'):
            text = self.md().replace('## Alice [Today]', replacement)
            result = self.check(text)
            self.assertFalse(result['article_posts_pass'])
            self.assertFalse(result['article_post_results'][0]['author_pass'])
        for replacement in ('## Alice [October 19]', '## [Alice]',
                            '- Alice [October 19]', 'Alice\n[October 19]'):
            self.assertTrue(self.check(self.md().replace('## Alice [Today]', replacement))['article_posts_pass'])

    def test_quote_author_is_exact_and_separate_from_quoted_body(self):
        ref = deepcopy(self.ref)
        ref['records'][0]['body_parts'][1]['author'] = 'Alice'
        for actual_author in ('Not Alice', 'Bob'):
            text = self.md(quote=actual_author+'\n'+self.quote+' Alice')
            result = self.check(text, reference=ref)
            self.assertFalse(result['article_posts_pass'])
            self.assertFalse(result['article_post_results'][0]['body_part_results'][1]['author_pass'])
        for text in (self.md(quote='Alice\n'+self.quote),
                     '## [Alice](https://example.com/post/1)\n\n'+self.post+
                     '\n\n> Alice\n> '+self.quote):
            self.assertTrue(self.check(text, reference=ref)['article_posts_pass'])
        missing = '## [Alice](https://example.com/post/1)\n\n'+self.post
        self.assertFalse(self.check(missing, reference=ref)['article_posts_pass'])
        # Attribution alone cannot supply the quoted body's matching units.
        ref['records'][0]['body_parts'][1].update(author='Alexandria', text='Alexandria')
        self.assertFalse(self.check(self.md(quote='Alexandria'), reference=ref)['article_posts_pass'])

    def test_complete_noncontent_prefixes_preserve_html_fragment_mode(self):
        prefixes = (
            '<noscript><style>body { overflow-y: scroll; }</style></noscript>',
            '<script>window.sample = 1;</script>',
            '<style>.post { color: black; }</style>',
            '<!-- captured body fragment -->',
            '<link rel="stylesheet" href="/style.css">',
            '<meta charset="utf-8" />',
            '<!-- prefix --><script>window.sample = 1;</script>'
            '<style>.post { color: black; }</style><link href="/x>a.css" />',
        )
        for prefix in prefixes:
            with self.subTest(prefix=prefix):
                self.assertTrue(self.check(prefix+'\n'+self.html())['article_posts_pass'])

    def test_noncontent_prefix_cannot_launder_fenced_or_inline_markdown_html(self):
        prefix = '<style>.post { color: black; }</style>\n'
        self.assertFalse(self.check(prefix+'```html\n'+self.html()+'\n```')['article_posts_pass'])
        self.assertFalse(self.check(prefix+'## Notes\nRead <a href="/post/1">Alice</a> below.\n'+self.post)['article_posts_pass'])
        self.assertTrue(self.check(prefix+self.md(post=self.post+' Inline <em>emphasis</em>.'))['article_posts_pass'])
        # A fallback record inside noscript must not become a displayed card.
        fallback = '<noscript>'+self.html()+'</noscript><main>No posts here.</main>'
        self.assertFalse(self.check(fallback)['article_posts_pass'])
