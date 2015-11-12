import json

from webtest import TestApp

from json_url_rewriter import middleware
from json_url_rewriter.rewrite import URLRewriter


DOC = {
    'self': 'http://foo.com/v1/bar/uuid'
}

def application(environ, sr):
    headers = [('Content-Type', 'application/json')]
    sr('200 OK', headers)
    return [json.dumps(DOC)]


class TestFunctionalMiddlware(object):

    def test_rewrite_with_tenant_id(self):
        rewriter = middleware.HeaderToPathPrefixRewriter(
            ['self'], 'http://foo.com',
            'X-Tenant-Id'
        )
        app = TestApp(middleware.RewriteMiddleware(application, rewriter))

        resp = app.get('/v2/zones', headers={'X-Tenant-Id': '12345'})

        assert resp.json['self'] == 'http://foo.com/12345/v1/bar/uuid'
