import requests
from unittest import TestCase
from unittest.mock import patch, Mock
from rest_client_framework.client import NoOpTransport, Client as BaseClient
from rest_client_framework.exceptions import ServiceResponseError, MaximumAttemptsExceeded
from rest_client_framework.request import Request
from rest_client_framework.response import Response
from .utils import get_mock_response

class Client(BaseClient):
    """
    Special-case client class that repeats requests whose HTTP response code
    is 503.
    """
    def handle_response(self, request, response, *args, **kwargs):
        if response is not None and response.status_code == 503:
            return self.RETRY
        return super().handle_response(request, response, *args, **kwargs)

@patch.object(Client, 'create_transport', Mock(return_value=NoOpTransport()))
@patch.object(Client, 'get_logger', Mock())
@patch.object(Client, 'base_url', 'https://some.test.service/')
class ClientTestCase(TestCase):
    def test_response_handling(self):
        """
        Tests the basic response handling behavior.
        """
        client = Client()
        # When the response's status code isn't "ok" according to the requests
        # library, the default behavior should be to raise an error.
        request = Request(client, 'test')
        response = get_mock_response(request, status_code=400)
        with patch.object(NoOpTransport, 'request', Mock(return_value=response)):
            client.logger.reset_mock()
            with self.assertRaises(ServiceResponseError) as context:
                client.request(request)
            # The response attached to the exception should actually be the
            # response as returned by the transport's request() method. The
            # request won't be the same instance, as it will be a
            # FrozenRequest wrapper around the real request, but it should
            # compare as equal.
            self.assertEqual(context.exception.request, request)
            self.assertIs(context.exception.response, response)
            self.assertEqual(client.attempt_count, 1)
            # Even though this request failed, there should still have been a
            # debugging log call containing the detailed request data.
            mock_call = client.logger.log.call_args_list[1]
            self.assertEqual(mock_call[0][0], client.request_verbose_log_level)
            self.assertTrue(
                mock_call[0][1].startswith('Request trace')
            )
        response = get_mock_response(request, content=b'foo')
        with patch.object(NoOpTransport, 'request', Mock(return_value=response)):
            client.logger.reset_mock()
            rest_response = client.request(request)
            self.assertIsInstance(rest_response, Response)
            self.assertIs(rest_response.response, response)
            self.assertEqual(rest_response.request, request)
            client.logger.log.assert_any_call(
                client.response_log_level,
                'Got 3-byte response with code 200.'
            )
            self.assertEqual(client.attempt_count, 1)

    @patch.object(Client, 'prepare_for_retry', Mock())
    def test_automatic_request_repetition(self):
        """
        Tests the automatic repetition of requests.
        """
        client = Client()
        request = Request(client, 'test')
        responses = [get_mock_response(request, status_code=503) for i in range(client.max_attempts - 1)]
        responses.append(get_mock_response(request, status_code=200))
        with patch.object(NoOpTransport, 'request', Mock(side_effect=responses)):
            client.prepare_for_retry.reset_mock()
            rest_response = client.request(request)
            self.assertEqual(rest_response.request, request)
            self.assertIs(rest_response.response, responses[-1])
            self.assertEqual(client.attempt_count, len(responses))
            self.assertEqual(client.responses, responses)
            self.assertEqual(len(client.prepare_for_retry.call_args_list), len(responses) - 1)
        # This time, we'll exceed the maximum number of attempts before the
        # response appears.
        responses.insert(0, get_mock_response(request, status_code=503))
        with patch.object(NoOpTransport, 'request', Mock(side_effect=responses)):
            client.prepare_for_retry.reset_mock()
            with self.assertRaises(MaximumAttemptsExceeded) as context:
                client.request(request)
            self.assertEqual(context.exception.request, request)
            self.assertIs(context.exception.responses, client.responses)
            self.assertEqual(client.attempt_count, client.max_attempts)
            self.assertEqual(len(client.responses), client.max_attempts)
            self.assertEqual(len(client.prepare_for_retry.call_args_list), client.max_attempts)