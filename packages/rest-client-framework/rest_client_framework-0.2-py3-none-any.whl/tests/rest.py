from copy import copy, deepcopy
from datetime import datetime
from unittest import TestCase
from rest_client_framework.rest import (AttributeCollisionError,
    RestDefinitionError, RestObject as BaseRestObject)

class RestObject(BaseRestObject):
    """
    A subclass of the base abstract class that adds some features to aid in
    testing.
    """
    def _set_data(self, *args, **kwargs):
        set_attrs = super()._set_data(*args, **kwargs)
        self.set_attrs = copy(set_attrs)
        return set_attrs

class UtilityObject(RestObject):
    property_map = {
        'time': None,
        'day': None
    }

class AnotherUtilityObject(RestObject):
    property_map = {
        'pitch': None,
        'yaw': None
    }

class RestObjectTestCase(TestCase):
    """
    Tests the core behavior defined in ``rest_client_framework.rest.RestObject``.
    """
    def setUp(self):
        # Instantiation of any class derived from RestObject has side effects
        # on class properties not only of that class but also its ancestors;
        # therefore, this test defines all test classes dynamically.
        class Foo(RestObject):
            include_null_properties = ('someBadlyNamedProperty',)
            property_map = {
                RestObject.__readonly__: ['someOtherProperty'],
                RestObject.__types__: {
                    'some_property': bool,
                    'set_me_first': 'UtilityObject'
                },
                'someProperty': None,
                'someOtherProperty': None,
                'someBadlyNamedProperty': 'my_attribute_name',
                'container': {
                    RestObject.__order__: ['firstContainedProperty'],
                    'containedProperty': None,
                    'firstContainedProperty': 'set_me_first',
                    'container': {
                        RestObject.__readonly__: ['deepProperty'],
                        'deepProperty': None
                    }
                }
            }

        class Bar(Foo):
            property_map = {
                RestObject.__defaults__: {
                    'some_property': True,
                    'bar_attribute': 'hello'
                },
                RestObject.__order__: ['container', 'someOtherProperty'],
                RestObject.__types__: {
                    'deep_property': __name__ + '.AnotherUtilityObject'
                },
                'someOtherProperty': {
                    RestObject.__order__: ['secondMember', 'firstMember'],
                    RestObject.__readonly__: ['secondMember'],
                    'firstMember': None,
                    'secondMember': None
                },
                'somePropertyUniqueToThisClass': 'bar_attribute'
            }

            @property
            def second_member(self):
                return self._second_member

            @second_member.setter
            def second_member(self, val):
                self._second_member = val

        class Baz(RestObject):
            use_pythonic_attribute_names = False
            include_null_properties = ('someProperty', 'container.containedProperty')
            property_map = {
                RestObject.__types__: {
                    'containedProperty': int
                },
                RestObject.__readonly__: {'containedReadOnlyProperty'},
                'container': {
                    'containedProperty': None,
                    'containedReadOnlyProperty': None
                },
                'someProperty': None,
                'someRenamedProperty': 'pythonically_named_property'
            }

        self.Foo = Foo
        self.Bar = Bar
        self.Baz = Baz

    def test_setter_dispatch(self):
        """
        Tests the behavior around the instantiation of objects with attribute
        values passed via keyword arguments.
        """
        foo = self.Foo(
            someProperty=1,
            someBadlyNamedProperty='asdf',
            container={
                'containedProperty': 'some nested property value',
                'firstContainedProperty': {
                    'time': '2:00 PM',
                    'day': 'Halloween'
                }
            }
        )
        # The type map specifies this as a boolean property, so the 1 provided
        # should have been cast to True.
        self.assertIs(foo.some_property, True)
        self.assertEqual(foo.my_attribute_name, 'asdf')
        self.assertEqual(foo.contained_property, 'some nested property value')
        self.assertEqual(foo.set_me_first, UtilityObject(time='2:00 PM', day='Halloween'))
        # The members of the container should have been set in the order that
        # I declared.
        self.assertLess(
            foo.set_attrs.index('set_me_first'),
            foo.set_attrs.index('contained_property')
        )
        # The other attributes set as a result of instantation should be
        # present in this list in any order.
        self.assertEqual(
            set(foo.set_attrs),
            {'set_me_first', 'contained_property', 'some_property', 'my_attribute_name'}
        )
        # Even though no values were provided for other attributes, they
        # should exist.
        self.assertIsNone(foo.some_other_property)
        self.assertIsNone(foo.deep_property)
        foo = self.Foo(
            container={
                'firstContainedProperty': {
                    'time': 'midnight',
                    'day': 'Friday the 13th'
                },
                'container': {
                    'deepProperty': 100
                },
                'containedProperty': 'asdfasdf'
            },
            someProperty=[],
            someOtherProperty='qwerty',
            someUnusedValue='a890se7dasjt89wa37'
        )
        self.assertIs(foo.some_property, False)
        self.assertEqual(foo.some_other_property, 'qwerty')
        self.assertEqual(foo.set_me_first, UtilityObject(
            time='midnight', day='Friday the 13th'
        ))
        self.assertEqual(foo.deep_property, 100)
        self.assertEqual(foo.contained_property, 'asdfasdf')
        # The extraneous keyword argument we provided should have been
        # discarded silently.
        self.assertFalse(hasattr(foo, 'some_unused_value'))
        self.assertFalse(hasattr(foo, 'someUnusedValue'))
        # Even though we varied the order in which the nested properties were
        # specified in the arguments, the setter order should have been
        # respected.
        self.assertLess(
            foo.set_attrs.index('set_me_first'),
            foo.set_attrs.index('contained_property')
        )
        self.assertEqual(set(foo.set_attrs), {
            'set_me_first',
            'contained_property',
            'some_property',
            'some_other_property',
            'deep_property'
        })
        # When it's not possible to convert the data in the arguments to the
        # appropriate type, an error should be raised.
        with self.assertRaises(TypeError):
            self.Foo(container={
                'firstContainedProperty': 'asdf'
            })

    def test_inherited_setter_dispatch(self):
        """
        Tests the instantiation of an inherited object whose property map was
        merged with its parent.
        """
        # Whereas Foo.someOtherProperty is a scalar, Bar.someOtherProperty is
        # a container for a deeper node.
        bar = self.Bar(
            someOtherProperty={
                'firstMember': 123,
                'secondMember': 456
            },
            someBadlyNamedProperty='zxcvbnm',
            somePropertyUniqueToThisClass='goodbye',
            container={
                'containedProperty': 'Modestly clothed, did she trouble you',
                'firstContainedProperty': {
                    'time': '5:23 AM',
                    'day': 'January 1st'
                },
                'container': {
                    'deepProperty': {
                        'pitch': 3,
                        'yaw': 200
                    }
                }
            }
        )
        # This class specifies True as the default value of some_property,
        # unlike its parent.
        self.assertIs(bar.some_property, True)
        self.assertEqual(bar.first_member, 123)
        self.assertEqual(bar.second_member, 456)
        # This is also happening behind the scenes by virtue of the @property
        # decorator.
        self.assertEqual(bar._second_member, 456),
        self.assertEqual(bar.my_attribute_name, 'zxcvbnm')
        self.assertEqual(bar.contained_property, 'Modestly clothed, did she trouble you')
        self.assertEqual(bar.set_me_first, UtilityObject(
            time='5:23 AM', day='January 1st'
        ))
        self.assertEqual(bar.deep_property, AnotherUtilityObject(
            pitch=3, yaw=200
        ))
        self.assertEqual(bar.bar_attribute, 'goodbye')
        # This time, there were multiple interacting order declarations
        self.assertLess(
            bar.set_attrs.index('set_me_first'),
            bar.set_attrs.index('deep_property')
        )
        self.assertLess(
            bar.set_attrs.index('set_me_first'),
            bar.set_attrs.index('second_member')
        )
        self.assertLess(
            bar.set_attrs.index('second_member'),
            bar.set_attrs.index('first_member')
        )
        self.assertEqual(set(bar.set_attrs), {
            'first_member',
            'second_member',
            'my_attribute_name',
            'contained_property',
            'set_me_first',
            'deep_property',
            'some_property',
            'bar_attribute'
        })
        bar = self.Bar(someProperty=False)
        self.assertIs(bar.some_property, False)
        self.assertEqual(bar.bar_attribute, 'hello')
        self.assertEqual(set(bar.set_attrs), {'some_property', 'bar_attribute'})
        with self.assertRaises(TypeError):
            self.Bar(someOtherProperty=[])

    def test_non_pythonic_attribute_names(self):
        # Tests the use of REST attribute names verbatim rather than automatic
        # transformation to Python-style names.
        baz = self.Baz(someProperty=123, container={
            'containedProperty': '42',
            'containedReadOnlyProperty': 'baz'
        }, someRenamedProperty='abc')
        self.assertEqual(baz.someProperty, 123)
        # This should have been cast as an int
        self.assertEqual(baz.containedProperty, 42)
        self.assertEqual(baz.containedReadOnlyProperty, 'baz')
        # Just because the default attribute names are what they are doesn't
        # mean explicitly declared ones shouldn't be respected.
        self.assertEqual(baz.pythonically_named_property, 'abc')
        # It's illegal to subclass a concrete RestObject subclass and change
        # the attribute name preference.
        with self.assertRaises(RestDefinitionError):
            type('IllegalSubclass', (self.Baz,), {'use_pythonic_attribute_names': True})

    def test_rest_representation(self):
        """
        Tests behavior pertinent to the conversion of RestObject instances
        back to simple data structures.
        """
        data = {
            'someProperty': False,
            'someBadlyNamedProperty': 'Young alien types who step out and dare to declare',
            'container': {
                'firstContainedProperty': {
                    'day': 'Judgement Day',
                    'time': 'High noon'
                }
            }
        }
        foo = self.Foo(**data)
        self.assertEqual(foo.as_rest(), data)
        # someBadlyNamedProperty will be included in the output even if it was
        # missing from the input.
        del data['someBadlyNamedProperty']
        foo = self.Foo(**data)
        comparison = deepcopy(data)
        comparison['someBadlyNamedProperty'] = None
        self.assertEqual(foo.as_rest(), comparison)
        # Conversion to the REST representation should be done recursively for
        # contained objects.
        foo.set_me_first = UtilityObject(day='April 1st')
        comparison['container']['firstContainedProperty'] = {'day': 'April 1st'}
        self.assertEqual(foo.as_rest(), comparison)
        # It's possible to selectively omit certain properties from the REST
        # representation.
        del comparison['someProperty']
        del comparison['container']
        with foo.exclude_properties('someProperty', 'container.firstContainedProperty'):
            self.assertEqual(foo.as_rest(), comparison)
        # It's also possible to do this in a non-contextual way
        foo.set_excluded_properties('someProperty', 'container.firstContainedProperty')
        self.assertEqual(foo.as_rest(), comparison)
        # It's also possible to merge the two forms
        foo.set_excluded_properties('someProperty')
        with foo.exclude_properties('container.firstContainedProperty', merge_contexts=True):
            self.assertEqual(foo.as_rest(), comparison)
        # If merging is not chosen, the context takes precedence
        with foo.exclude_properties('container.firstContainedProperty'):
            self.assertIn('someProperty', foo.as_rest())
        # Some of this class' properties are marked as read-only, so they are
        # normally excluded from REST representations.
        data = {
            'someOtherProperty': 'asdf',
            'container': {
                'containedProperty': 12345,
                'container': {
                    'deepProperty': "Personally, I think I'm overdone."
                }
            },
            'someBadlyNamedProperty': 'foo'
        }
        foo = self.Foo(**data)
        comparison = deepcopy(data)
        del comparison['someOtherProperty']
        # The designation of deep_property as read-only should not only cause
        # it to be omitted, but also its entire container, since there will be
        # nothing left to put in it.
        del comparison['container']['container']
        # The formatted object will contain someProperty even though we didn't
        # provide a value, since its value will have been cast as a boolean.
        comparison['someProperty'] = False
        self.assertEqual(foo.as_rest(), comparison)
        # It's possible to opt into the inclusion of read-only properties via a
        # context.
        data['someProperty'] = False
        with foo.include_readonly():
            self.assertEqual(foo.as_rest(), data)
        # Subclasses should inherit any declarations their parents define
        # regarding read-only properties and null inclusions.
        data = {
            'somePropertyUniqueToThisClass': 'Starland Vocal Band?! They suck!',
            'someOtherProperty': {
                'firstMember': 'abc',
                'secondMember': 'def'
            },
            'someBadlyNamedProperty': 'You have selected: regicide!',
            'container': {
                'container': {
                    'deepProperty': {
                        'pitch': 200,
                        'yaw': 1000
                    }
                }
            }
        }
        comparison = deepcopy(data)
        del comparison['someOtherProperty']
        # This whole thing should be omitted
        del comparison['container']
        # This will be present by virtue of its default value
        comparison['someProperty'] = True
        bar = self.Bar(**data)
        self.assertEqual(bar.as_rest(), comparison)
        # If we set a value for some other property that's in the container,
        # it will allow it to be included, but without the inner container,
        # which contains the read-only property.
        bar.set_me_first = UtilityObject(day='Yak shaving day', time='Bedtime')
        comparison['container'] = {'firstContainedProperty': {
            'day': 'Yak shaving day',
            'time': 'Bedtime'
        }}
        self.assertEqual(bar.as_rest(), comparison)
        data['container']['firstContainedProperty'] = comparison['container']['firstContainedProperty']
        # Again, need to add this in because of the default value
        data['someProperty'] = True
        with bar.include_readonly():
            self.assertEqual(bar.as_rest(), data)
            bar.my_attribute_name = None
            data['someBadlyNamedProperty'] = None
            self.assertEqual(bar.as_rest(), data)
        # The inclusion of properties that are normally present even if null
        # can be bypassed.
        with bar.exclude_properties('someBadlyNamedProperty'):
            self.assertNotIn('someBadlyNamedProperty', bar.as_rest())
        # The wildcard specifies that all properties should always be included
        # in the output, even if they have no value (unless they're read-only).
        class Foo(self.Foo):
            include_null_properties = '*'
        foo = Foo()
        comparison = {
            'someProperty': False,
            'someBadlyNamedProperty': None,
            'container': {
                'containedProperty': None,
                'firstContainedProperty': None,
                'container': None
            }
        }
        self.assertEqual(foo.as_rest(), comparison)
        comparison['someOtherProperty'] = None
        comparison['container']['container'] = {'deepProperty': None}
        with foo.include_readonly():
            self.assertEqual(foo.as_rest(), comparison)
        data = {
            'someProperty': 'abc',
            'someRenamedProperty': ['foo', 'bar'],
            'container': {
                'containedReadOnlyProperty': 'Sucks to your assmar'
            }
        }
        comparison = deepcopy(data)
        comparison['container'] = {'containedProperty': None}
        baz = self.Baz(**data)
        self.assertEqual(baz.as_rest(), comparison)
        comparison['container']['containedReadOnlyProperty'] = 'Sucks to your assmar'
        with baz.include_readonly():
            self.assertEqual(baz.as_rest(), comparison)

    def test_type_handling(self):
        """
        Tests the raising of errors if data incompatible with an attribute's
        declared type is passed during instantiation or when set on an
        existing instance, as well as implicit typecasting.
        """
        with self.assertRaises(TypeError):
            self.Foo(someOtherProperty='asdf', container={
                'firstContainedProperty': 'asdf'
            })
        # The same thing should happen if we try to set the value after
        # instantiation.
        foo = self.Foo(someOtherProperty='asdf')
        with self.assertRaises(TypeError):
            foo.set_me_first = 'asdf'
        # However, either dict representations of the intended REST type or
        # instances of the type itself are OK.
        foo.set_me_first = {'day': 'Yesterday', 'time': '0800 hrs'}
        foo.set_me_first = UtilityObject(day='Tomorrow', time="25 o'clock")
        # This should be cast as a boolean automatically
        foo.some_property = ''
        self.assertIs(foo.some_property, False)
        bar = self.Bar()
        with self.assertRaises(TypeError):
            bar.deep_property = UtilityObject(day='Someday', time='Whenever')
        baz = self.Baz()
        baz.containedProperty = '100'
        self.assertEqual(baz.containedProperty, 100)
        with self.assertRaises(TypeError):
            baz.containedProperty = 'asdf'
        # It should be possible to define setter and getter methods to handle
        # custom types.
        class MyFancyType:
            def __init__(self, val):
                self.val = val

        class Foo(self.Foo):
            property_map = {
                # Here we're mapping the REST property name to the intended
                # Python type, which isn't preferred but should be respected.
                RestObject.__types__: {
                    'someBadlyNamedProperty': MyFancyType
                }
            }

            def set_myfancytype_attribute(self, name, val):
                setattr(self, name, MyFancyType(val))

            def get_myfancytype_attribute(self, name):
                return list(reversed(getattr(self, name).val))

        foo = Foo(someBadlyNamedProperty=['a', 'b', 'c', 'd', 'e'], container={
            'firstContainedProperty': UtilityObject(day='Smarch 13th', time='13:00')
        })
        self.assertEqual(foo.my_attribute_name, ['e', 'd', 'c', 'b', 'a'])
        self.assertEqual(foo.as_rest(), {
            'someProperty': False,
            'someBadlyNamedProperty': ['e', 'd', 'c', 'b', 'a'],
            'container': {
                'firstContainedProperty': {'day': 'Smarch 13th', 'time': '13:00'}
            }
        })

    def test_reverse_mapping(self):
        """
        Tests the ability to create a reverse map of attributes to dotted REST
        property paths.
        """
        self.assertEqual({k: str(v) for k, v in self.Baz._reversed_property_map.items()}, {
            'containedProperty': 'container.containedProperty',
            'containedReadOnlyProperty': 'container.containedReadOnlyProperty',
            'someProperty': 'someProperty',
            'pythonically_named_property': 'someRenamedProperty'
        })
        self.assertEqual({k: str(v) for k, v in self.Bar._reversed_property_map.items()}, {
            'bar_attribute': 'somePropertyUniqueToThisClass',
            'first_member': 'someOtherProperty.firstMember',
            'second_member': 'someOtherProperty.secondMember',
            'some_property': 'someProperty',
            'my_attribute_name': 'someBadlyNamedProperty',
            'contained_property': 'container.containedProperty',
            'set_me_first': 'container.firstContainedProperty',
            'deep_property': 'container.container.deepProperty'
        })
        self.assertEqual({k: str(v) for k, v in self.Foo._reversed_property_map.items()}, {
            'some_property': 'someProperty',
            'some_other_property': 'someOtherProperty',
            'my_attribute_name': 'someBadlyNamedProperty',
            'contained_property': 'container.containedProperty',
            'set_me_first': 'container.firstContainedProperty',
            'deep_property': 'container.container.deepProperty'
        })
        class Bar(self.Bar):
            property_map = {
                'someOtherPropertyUniqueToThisClass': {
                    'uniqueNestedProperty': None,
                    'anotherUniqueNestedProperty': {
                        'veryDeepProperty': None
                    }
                }
            }

        self.assertEqual({k: str(v) for k, v in Bar._reversed_property_map.items()}, {
            'bar_attribute': 'somePropertyUniqueToThisClass',
            'first_member': 'someOtherProperty.firstMember',
            'second_member': 'someOtherProperty.secondMember',
            'some_property': 'someProperty',
            'contained_property': 'container.containedProperty',
            'my_attribute_name': 'someBadlyNamedProperty',
            'set_me_first': 'container.firstContainedProperty',
            'deep_property': 'container.container.deepProperty',
            'unique_nested_property': 'someOtherPropertyUniqueToThisClass.uniqueNestedProperty',
            'very_deep_property': 'someOtherPropertyUniqueToThisClass.anotherUniqueNestedProperty.veryDeepProperty'
        })
        # The logic that builds the reverse property map should also ensure
        # that there aren't collisions resulting from multiple property paths
        # pointing to the same attribute name.
        with self.assertRaises(AttributeCollisionError):
            type('BadRestObject', (self.Bar,), {
                'property_map': {
                    'somePropertyUniqueToThisClass': {
                        'firstMember': None
                    }
                }
            })

    def test_include_null_property_resolution(self):
        """
        Tests the resolution of different ``include_null_properties`` values
        across an inheritance chain.
        """
        class Bar(self.Foo):
            include_null_properties = ('container.containedProperty',)

        # The REST form of an empty object should contain the null property
        # specified in the class definition, plus that of its parent. And it
        # will contain any properties that have default values, of course.
        expected = {
            'someProperty': False,
            'someBadlyNamedProperty': None,
            'container': {
                'containedProperty': None
            }
        }
        self.assertEqual(Bar().as_rest(), expected)
        # Longer inheritance chains should work as expected
        class Baz(Bar):
            include_null_properties = ('someOtherProperty', 'container.container.deepProperty')

        # Both of the properties specified above are read-only, so we only see
        # them in the appropriate context.
        baz = Baz()
        self.assertEqual(baz.as_rest(), expected)
        expected['someOtherProperty'] = None
        expected['container']['container'] = {'deepProperty': None}
        with baz.include_readonly():
            self.assertEqual(baz.as_rest(), expected)

    def test_property_order_merging(self):
        """
        Tests the merging of property orderings across an inheritance chain.
        """
        class Baz(self.Bar):
            property_map = {
                RestObject.__order__: ['somePropertyUniqueToThisClass']
            }

        # The order designations across this inheritance chain do not share any
        # property names in common, so the child specification gets appended
        # to the parent.
        self.assertEqual(Baz._resolved_property_map[RestObject.__order__], [
            'container',
            'someOtherProperty',
            'somePropertyUniqueToThisClass'
        ])
        obj = Baz(container={
            'containedProperty': 'foo'
        }, someOtherProperty={
            'firstMember': 123,
            'secondMember': 456
        }, somePropertyUniqueToThisClass='asdf')
        self.assertEqual(
            list(filter(lambda a: a in (
                'contained_property',
                'second_member',
                'first_member',
                'bar_attribute'
            ), obj.set_attrs)), [
                'contained_property',
                'second_member',
                'first_member',
                'bar_attribute'
            ]
        )
        # This time, the ordering should respect the preference that
        # somePropertyUniqueToThisClass comes before someOtherProperty.
        class Baz(self.Bar):
            property_map = {
                RestObject.__order__: ['somePropertyUniqueToThisClass', 'someOtherProperty']
            }

        self.assertEqual(Baz._resolved_property_map[RestObject.__order__], [
            'container',
            'somePropertyUniqueToThisClass',
            'someOtherProperty'
        ])
        obj = Baz(container={
            'containedProperty': 'foo'
        }, someOtherProperty={
            'firstMember': 123,
            'secondMember': 456
        }, somePropertyUniqueToThisClass='asdf')
        self.assertEqual(
            list(filter(lambda a: a in (
                'contained_property',
                'second_member',
                'first_member',
                'bar_attribute'
            ), obj.set_attrs)), [
                'contained_property',
                'bar_attribute',
                'second_member',
                'first_member'
            ]
        )
        # Using Python property names should work equivalently, and the use of
        # a tuple here should coexist with the list in the parent definition.
        class Baz(self.Bar):
            property_map = {
                RestObject.__order__: ('bar_attribute', 'container')
            }

        self.assertEqual(Baz._resolved_property_map[RestObject.__order__], [
            'somePropertyUniqueToThisClass',
            'container',
            'someOtherProperty'
        ])
        obj = Baz(container={
            'containedProperty': 'foo'
        }, someOtherProperty={
            'firstMember': 123,
            'secondMember': 456
        }, somePropertyUniqueToThisClass='asdf')
        self.assertEqual(
            list(filter(lambda a: a in (
                'contained_property',
                'second_member',
                'first_member',
                'bar_attribute'
            ), obj.set_attrs)), [
                'bar_attribute',
                'contained_property',
                'second_member',
                'first_member'
            ]
        )
        # somePropertyUniqueToThisClass/bar_attribute has a default, so if we
        # don't specify it in the constructor arguments, it should still be set
        # in the expected order.
        obj = Baz(container={
            'containedProperty': 'foo'
        }, someOtherProperty={
            'firstMember': 123,
            'secondMember': 456
        })
        self.assertEqual(obj.bar_attribute, 'hello')
        self.assertLess(
            obj.set_attrs.index('bar_attribute'),
            obj.set_attrs.index('contained_property')
        )
        # To complicate things, we'll subclass the preceding class, use a
        # different name for the property in the first position, and add a
        # couple new ones.
        class Quux(Baz):
            property_map = {
                RestObject.__order__: [
                    'somePropertyUniqueToThisClass',
                    'someOtherProperty',
                    'yet_another_property',
                    'stillAnotherProperty'
                ],
                'yetAnotherProperty': None,
                'stillAnotherProperty': None
            }
        self.assertEqual(Quux._resolved_property_map[RestObject.__order__], [
            'somePropertyUniqueToThisClass',
            'container',
            'someOtherProperty',
            'yetAnotherProperty',
            'stillAnotherProperty'
        ])
        obj = Quux(
            container={'containedProperty': 'foo'},
            someOtherProperty={
                'firstMember': 123,
                'secondMember': 456
            },
            somePropertyUniqueToThisClass='asdf',
            yetAnotherProperty=UtilityObject(),
            stillAnotherProperty=456
        )
        self.assertEqual(
            list(filter(lambda a: a in (
                'contained_property',
                'second_member',
                'first_member',
                'bar_attribute',
                'yet_another_property',
                'still_another_property'
            ), obj.set_attrs)), [
                'bar_attribute',
                'contained_property',
                'second_member',
                'first_member',
                'yet_another_property',
                'still_another_property'
            ]
        )
        # Attempts to declare an order that conflicts with an ancestor should
        # fail.
        with self.assertRaises(RestDefinitionError):
            class Quux(Baz):
                property_map = {
                    RestObject.__order__: ['container', 'somePropertyUniqueToThisClass']
                }

    def test_equality_comparison(self):
        """
        Tests whether equivalent ``RestObject`` instances compare as true.
        """
        data = {
            'someProperty': True,
            'someBadlyNamedProperty': 'foo',
            'container': {
                'firstContainedProperty': {
                    'time': 'noon',
                    'day': 'Friday'
                }
            }
        }
        obj1 = self.Foo(**data)
        obj2 = self.Foo(**data)
        self.assertEqual(obj1, obj2)
        # Comparisons directly to the REST data should work too
        self.assertEqual(obj1, data)
        self.assertEqual(data['container']['firstContainedProperty'], obj1.set_me_first)

    def test_datetime_handling(self):
        """
        Tests the automatic conversion of ``datetime.datetime`` instances to
        and from strings.
        """
        class Foo(self.Foo):
            datetime_formats = ('%Y-%m-%d', '%m/%d/%Y %I:%M%p')
            property_map = {
                RestObject.__types__: {
                    'someProperty': datetime
                }
            }

        # It should be possible to leave the attribute unset
        obj = Foo()
        self.assertIsNone(obj.some_property)
        obj = Foo(someProperty='10/8/2021 10:50pm')
        self.assertIsInstance(obj.some_property, datetime)
        # When rendering back to REST, the datetime should retain its original
        # format, although there will be certain differences due to things like
        # zero padding and capitalization.
        self.assertEqual(obj.as_rest()['someProperty'], '10/08/2021 10:50PM')
        # This is OK too
        obj = Foo(someProperty='2021-10-08')
        self.assertIsInstance(obj.some_property, datetime)
        self.assertEqual(obj.as_rest()['someProperty'], '2021-10-08')
        # So is setting the attribute after instantiation
        obj = Foo()
        obj.some_property = '2000-01-01'
        self.assertIsInstance(obj.some_property, datetime)
        self.assertEqual(obj.as_rest()['someProperty'], '2000-01-01')
        # If a datetime is set directly, the first format will be used as a
        # default to turn it to a string.
        obj.some_property = datetime(2021, 6, 1, 12, 59)
        self.assertEqual(obj.as_rest()['someProperty'], '2021-06-01')
        with self.assertRaises(ValueError):
            Foo(someProperty='asdf')
        with self.assertRaises(ValueError):
            Foo(someProperty='2021-06-01 23:59:00')