import json

from mock import Mock
from webtest import TestApp

from json_url_rewriter import middleware


class TestMiddlware(object):
    doc = {'hello': {'foo': 'bar'}}

    def middleware(self, *args):
        return middleware.RewriteMiddleware(*args)

    def resp(self, doc):
        return json.dumps(doc, indent=2).split('\n')

    def test_json_loading(self):
        mw = self.middleware(None, None)
        assert mw.json(self.resp(self.doc)) == self.doc

    def test_rewriter(self):
        resp = self.resp(self.doc)
        rewriter = Mock(return_value=self.doc)
        mw = self.middleware(None, rewriter)
        doc = mw.json(resp)

        result = mw.rewrite(resp, {})
        rewriter.assert_called_with(doc, {})

        # Noop rewriter
        assert result == json.dumps(doc)

    def test_middleware(self):
        def app(environ, sr):
            headers = [('Content-Type', 'application/json')]
            sr('200 OK', headers)
            return self.resp(self.doc)

        result = {'hello': 'world'}
        app = TestApp(self.middleware(app, lambda x, environ: result))
        resp = app.get('/')
        assert resp.json == result


class TestHeaderToPathPrefixRewriter(object):

    def test_regex(self):
        pass
