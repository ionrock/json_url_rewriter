from json_url_rewriter import rewrite

class TestAccessByKey(object):

    def test_get_top_level_by_key(self):
        doc = {'foo': 'bar'}
        assert rewrite.get_by_key(doc, 'foo') == 'bar'

    def test_set_top_levelby_key(self):
        doc = {'foo': 'bar'}
        rewrite.set_by_key(doc, 'foo', 'baz')
        assert doc['foo'] == 'baz'

    def test_set_failure_is_noop(self):
        doc = {'foo': 'bar'}
        orig = doc.copy()
        rewrite.set_by_key(doc, 'not_exists', 'baz')
        assert doc == orig

    def test_nested_by_key(self):
        doc = {'foo': {'bar': {'baz': 'hello world'}}}
        assert rewrite.get_by_key(doc, 'foo.bar.baz') == 'hello world'


class TestURLRewriter(object):

    def setup(self):
        self.rewriter = rewrite.URLRewriter([], None, None)

    def test_noop(self):
        doc = {'foo': 'bar'}
        assert self.rewriter(doc) == doc

    def test_keys_search(self):
        doc = {'foo': 'bar'}

    def test_rewrite_regex_with_string(self):
        doc = {'self': 'http://foo.com/bar/'}
        rw = rewrite.URLRewriter(['self'], 'http', 'https')
        assert rw.rewrite(doc['self']) == 'https://foo.com/bar/'

    def test_rewrite_regex_with_func(self):
        doc = {'self': 'http://foo.com/bar/'}

        def replace(match):
            return match.group() + 's'

        rw = rewrite.URLRewriter(['self'], 'http', replace)
        assert rw.rewrite(doc['self']) == 'https://foo.com/bar/'
