from unittest import TestCase
from rest_client_framework.datastructures import (BaseFrozenObject,
    FrozenSequence, FrozenMapping)

class TestObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class FrozenDatastructuresTestCase(TestCase):
    def setUp(self):
        self.list = [
            'foo',
            'bar',
            {
                'abc': 123,
                'def': 456,
            },
            7,
            [1, 2, 3],
            None,
            object(),
            ('a', 'b', ['foo', 'bar'])
        ]
        self.frozen_list = FrozenSequence(self.list)
        self.dict = {
            'foo': 'bar',
            'list': [1, 2, 3],
            'dict': {
                'a': 1,
                'b': 2
            },
            'object': object()
        }
        self.frozen_dict = FrozenMapping(self.dict)
        self.frozen_object = BaseFrozenObject(TestObject(
            foo='bar',
            list=[1, 2, 3],
            obj=object(),
            dict={
                'a': 1,
                'b': 2,
                'c': ('foo', 'bar', 'baz')
            }
        ))

    def test_member_access(self):
        """
        Tests access to frozen object members/attributes.
        """
        self.assertEqual(self.frozen_list[0], 'foo')
        self.assertIsNone(self.frozen_list[-3])
        self.assertIs(self.frozen_list[-2].__class__, object)
        self.assertEqual(self.frozen_list[-1][1], 'b')
        self.assertEqual(self.frozen_dict['foo'], 'bar')
        self.assertEqual(self.frozen_dict['list'][0], 1)
        self.assertEqual(self.frozen_dict['dict']['a'], 1)
        self.assertIs(self.frozen_dict['object'].__class__, object)
        self.assertEqual(self.frozen_object.foo, 'bar')
        self.assertEqual(self.frozen_object.list[2], 3)
        self.assertEqual(self.frozen_object.dict['c'][0], 'foo')
        self.assertIs(self.frozen_object.obj.__class__, object)
        # Eligible members of frozen objects should be automatically cast as
        # the appropriate frozen type.
        self.assertIsInstance(self.frozen_list[2], FrozenMapping)
        self.assertIsInstance(self.frozen_list[4], FrozenSequence)
        # Deep members too
        self.assertIsInstance(self.frozen_list[-1][-1], FrozenSequence)
        self.assertIsInstance(self.frozen_dict['list'], FrozenSequence)
        self.assertIsInstance(self.frozen_dict['dict'], FrozenMapping)
        self.assertIsInstance(self.frozen_object.list, FrozenSequence)
        self.assertIsInstance(self.frozen_object.dict, FrozenMapping)
        self.assertIsInstance(self.frozen_object.dict['c'], FrozenSequence)
        # Repeated access to the same frozen member should produce the same
        # instance.
        self.assertIs(self.frozen_list[2], self.frozen_list[2])
        self.assertIs(self.frozen_list[-1][-1], self.frozen_list[-1][-1])
        self.assertIs(self.frozen_dict['dict'], self.frozen_dict['dict'])
        self.assertIs(self.frozen_object.dict, self.frozen_object.dict)

    def test_equality(self):
        """
        Tests the comparison between frozen objects and their equivalent
        primitive types.
        """
        self.assertEqual(self.list, self.frozen_list)
        # The comparison should work both ways
        self.assertEqual(self.frozen_list, self.list)
        self.assertEqual(self.dict, self.frozen_dict)
        self.assertEqual(self.frozen_dict, self.dict)
        # And different but equivalent instances of the same types should
        # compare equally.
        self.assertEqual(self.frozen_list, FrozenSequence(self.list))
        self.assertEqual(self.frozen_dict, FrozenSequence(self.dict))