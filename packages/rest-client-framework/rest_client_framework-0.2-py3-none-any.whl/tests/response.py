from unittest import TestCase
from unittest.mock import patch, Mock
from rest_client_framework.client import Client
from rest_client_framework.request import Request
from rest_client_framework.response import (JsonRestResponse,
    JsonSequenceRestResponse, CachingJsonSequenceRestResponse)
from rest_client_framework.rest import RestObject
from .utils import get_mock_response

class TestClient(Client):
    base_url = 'https://some.test.service'

class Dingus(RestObject):
    property_map = {
        RestObject.__types__: {
            'birthday': 'Date'
        },
        'name': None,
        'occupation': None,
        'metaData': {
            'dob': 'birthday',
            'bestFriend': None
        }
    }

    def __init__(self, *args, **kwargs):
        self.args = args
        super().__init__(**kwargs)

class Date(RestObject):
    property_map = {
        'year': None,
        'month': None,
        'day': None
    }

class DingusResponseMixin:
    REST_CLASS = Dingus

class DingusResponse(DingusResponseMixin, JsonRestResponse):
    pass

class DingusSequenceResponseMixin(DingusResponseMixin):
    CONTAINER_PROPERTY = 'dinguses'

    def __init__(self, *args, **kwargs):
        self.get_series_call_count = 0
        super().__init__(*args, **kwargs)

    def get_series_from_response(self):
        self.get_series_call_count += 1
        return super().get_series_from_response()

class DingusSequenceResponse(DingusSequenceResponseMixin, JsonSequenceRestResponse):
    pass

class CachingDingusSequenceResponse(DingusSequenceResponseMixin, CachingJsonSequenceRestResponse):
    pass

class ResponseTestCase(TestCase):
    def test_single_response(self):
        """
        Tests the automatic instantiation of single REST objects from JSON
        responses.
        """
        client = TestClient()
        request = Request(client, 'test')
        response = DingusResponse(client, request, get_mock_response(request, content=b"""
{
    "name": "Steven Brule",
    "occupation": "Doctor",
    "metaData": {
        "dob": {
            "year": 1962,
            "month": 4,
            "day": 1
        },
        "bestFriend": "Denny"
    }
}
"""
))
        self.assertEqual(response.instance.name, 'Steven Brule')
        self.assertEqual(response.instance.occupation, 'Doctor')
        self.assertEqual(response.instance.birthday.year, 1962)
        self.assertEqual(response.instance.birthday.month, 4)
        self.assertEqual(response.instance.birthday.day, 1)
        self.assertEqual(response.instance.best_friend, 'Denny')
        # The response class can be configured to pass arbitrary positional
        # arguments to the REST object constructor.
        with patch.object(DingusResponse, 'get_instance_args', Mock(return_value=('foo',))):
            response = DingusResponse(client, request, get_mock_response(request, content=b"""
{
    "name": "Dorris Pringle-Brule Salahari",
    "occupation": "Mom",
    "metaData": {
        "dob": {
            "year": 1903,
            "month": 7,
            "day": 12
        },
        "bestFriend": "Mobin"
    },
    "foo": "bar"
}
"""
))
            self.assertEqual(response.instance.args, ('foo',))
            self.assertEqual(response.instance, Dingus(
                name='Dorris Pringle-Brule Salahari',
                occupation='Mom',
                metaData={
                    'dob': Date(year=1903, month=7, day=12),
                    'bestFriend': 'Mobin'
                }
            ))

    def test_series_response(self):
        """
        Tests the automatic instantiation of multiple REST objects from JSON
        responses.
        """
        client = TestClient()
        request = Request(client, 'test')
        response_content = b"""
{
    "dinguses": [{
        "name": "Steven Brule",
        "occupation": "Doctor",
        "metaData": {
            "dob": {
                "year": 1962,
                "month": 4,
                "day": 1
            },
            "bestFriend": "Denny"
        }
    }, {
        "name": "Dorris Pringle-Brule Salahari",
        "occupation": "Mom",
        "metaData": {
            "dob": {
                "year": 1903,
                "month": 7,
                "day": 12
            },
            "bestFriend": "Mobin"
        },
        "foo": "bar"
    }]
}
"""
        response = DingusSequenceResponse(
            client, request, get_mock_response(request, content=response_content)
        )
        self.assertTrue(all([isinstance(d, Dingus) for d in response]))
        self.assertEqual(response[1].birthday.month, 7)
        self.assertTrue(len(response), 2)
        # Each operation above should have called the instance's series getter
        self.assertEqual(response.get_series_call_count, 3)
        caching_response = CachingDingusSequenceResponse(
            client, request, get_mock_response(request, content=response_content)
        )
        # I'm intentionally performing this test with more assertions than
        # necessary in order to demonstrate that the caching takes place.
        self.assertEqual(len(caching_response), len(response))
        for i in range(len(caching_response)):
            self.assertEqual(caching_response[i], response[i])
        self.assertEqual(list(caching_response), list(response))
        self.assertEqual(caching_response.get_series_call_count, 1)
        # The caching can be deactivated contextually, which means that the
        # contents will differ if we alter the content of the underlying
        # response (and uncache the parsed JSON).
        caching_response.response._content = b"""
{
    "dinguses": [{
        "name": "Cindy Grunkerson",
        "occupation": "Fortune teller",
        "metaData": {
            "dob": {
                "month": 2,
                "year": 1974,
                "day": 28
            }
        }
    }, {
        "name": "Dr. Rongald Bringer",
        "occupation": "Card counter",
        "metaData": {
            "bestFriend": "Droug Grambler"
        }
    }, {
        "name": "Brob Barker",
        "occupation": "Pruppet man"
    }]
}
"""
        del caching_response.__dict__['json']
        with caching_response.no_cache():
            self.assertEqual(len(caching_response), 3)
            self.assertEqual(caching_response[2].occupation, 'Pruppet man')
        # Outside of that context, we're back to the old story
        self.assertEqual(list(caching_response), list(response))
        # This method should have been called twice more
        self.assertEqual(caching_response.get_series_call_count, 3)