from unittest import TestCase
from unittest.mock import patch
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from rest_client_framework.client import Client
from rest_client_framework.request import Request

class RequestTestCase(TestCase):
    # Borrowed from django.test.testcases.SimpleTestCase
    def assertURLEqual(self, first, second):
        def normalize(url):
            parsed = urlparse(url)
            query = sorted(parse_qsl(parsed.query))
            return urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                urlencode(query),
                parsed.fragment
            ))
        self.assertEqual(
            normalize(first),
            normalize(second),
            msg='URL {} != {}'.format(first, second)
        )

    @patch.object(Client, 'base_url', 'https://some.test.service/')
    def test_url_construction(self):
        """
        Tests the automatic joining of client base URLs to request URL paths.
        """
        client = Client()
        request = Request(client, 'foo')
        self.assertURLEqual(request.url, 'https://some.test.service/foo')
        # Omitting the trailing slash from a bare domain should be OK
        with patch.object(Client, 'base_url', 'https://some.test.service'):
            self.assertURLEqual(request.url, 'https://some.test.service/foo')
        # Relative URLs should be constructed as expected
        with patch.object(Client, 'base_url', 'https://some.test.service/api/'):
            self.assertURLEqual(request.url, 'https://some.test.service/api/foo')
            self.assertURLEqual(
                Request(client, '/foo').url, 'https://some.test.service/foo'
            )
        request.kwargs['bar'] = 'baz'
        self.assertURLEqual(request.url, 'https://some.test.service/foo?bar=baz')
        request.kwargs['abc'] = '123'
        self.assertURLEqual(request.url, 'https://some.test.service/foo?bar=baz&abc=123')
        # Extra slashes should be normalized away
        request = Request(client, '/some/api/method/', coffee_additive='Half & Half')
        self.assertURLEqual(
            request.url,
            'https://some.test.service/some/api/method/?coffee_additive=Half+%26+Half'
        )
        with patch.object(Client, 'base_url', 'https://some.test.service/api'):
            # This is a subtle thing, but the resolved URL path actually won't
            # begin with /api due to the fact that the base URL doesn't end
            # with a slash.
            self.assertURLEqual(
                request.url,
                'https://some.test.service/some/api/method/?coffee_additive=Half+%26+Half'
            )
        # URL paths containing colons should work
        request = Request(client, 'foo:bar')
        self.assertURLEqual(request.url, 'https://some.test.service/foo:bar')
        with patch.object(Client, 'base_url', 'https://some.test.service'):
            self.assertURLEqual(request.url, 'https://some.test.service/foo:bar')
        with patch.object(Client, 'base_url', 'https://some.test.service/baz'):
            self.assertURLEqual(request.url, 'https://some.test.service/foo:bar')
        request = Request(client, 'baz/foo:bar')
        self.assertURLEqual(request.url, 'https://some.test.service/baz/foo:bar')
        with patch.object(Client, 'base_url', 'https://some.test.service/baz/'):
            self.assertURLEqual(request.url, 'https://some.test.service/baz/baz/foo:bar')

    def test_signature(self):
        """
        Tests signature equality between two requests with equivalent arguments
        and/or payloads.
        """
        client = Client()
        request1 = Request(client, 'foo')
        request2 = Request(client, 'bar')
        # The signature doesn't take the path into account
        self.assertEqual(request1.signature, request2.signature)
        request1.kwargs = request2.kwargs = {'foo': 'bar', 'bar': 'baz'}
        self.assertEqual(request1.signature, request2.signature)
        request1.kwargs['baz'] = 'quux'
        self.assertNotEqual(request1.signature, request2.signature)
        # This has nothing to do with signature testing per se, but it's a
        # convenient place to assert that you can't instantiate a GET request
        # with a body.
        with self.assertRaises(ValueError):
            Request(client, 'foo', body={'foo': 'bar'})
        # Order of arguments shouldn't matter
        self.assertEqual(
            Request(client, 'foo', foo='bar', bar={'baz': 'quux', 'abc': 123}).signature,
            Request(client, 'foo', bar={'abc': 123, 'baz': 'quux'}, foo='bar').signature
        )
        request1 = Request(client, 'foo', method='POST', body={'foo': 'bar', 'bar': ['a', 'b', 12]})
        request2 = Request(client, 'foo', method='POST', body={'bar': ['a', 'b', 12], 'foo': 'bar'})
        self.assertEqual(request1.signature, request2.signature)
        # Order of sequences, however, does matter
        request2.body['bar'] = ['a', 12, 'b']
        self.assertNotEqual(request1.signature, request2.signature)
        # Both the GET parameters and the request body are taken into account
        request1 = Request(
            client,
            'foo',
            method='POST',
            body={'foo': 'bar', 'bar': ['a', 'b', 12]},
            param='value',
            param2='value2'
        )
        request2 = Request(
            client,
            'foo',
            method='POST',
            body={'foo': 'bar', 'bar': ['a', 'b', 12]},
            param2='value2',
            param='value'
        )
        self.assertEqual(request1.signature, request2.signature)
        request2.body['baz'] = 'quux'
        self.assertNotEqual(request1.signature, request2.signature)