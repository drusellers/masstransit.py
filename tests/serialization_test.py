from masstransit.serializer import Serializer
import unittest

class TestSerializationObject:
    def __init__(self):
        self.name = "dru"
        self.age = 2

class TestSerializationHierarchyObject:
    def __init__(self):
        self.boss = "rob"
        self.obj = TestSerializationObject()

class TestSerialization(unittest.TestCase):
    def test_dictionary(self):
        s = Serializer()
        d = {'greeting': 'hi mom'}
        encoded = s.serialize(d)
        self.assertEqual('{"greeting": "hi mom"}', encoded)

    def test_dictionary_with_object(self):
        s = Serializer()
        d = {'msg': TestSerializationObject()}
        encoded = s.serialize(d)
        self.assertEqual('{"msg": {"age": 2, "name": "dru"}}', encoded)

    def test_serialization(self):
        s = Serializer()
        d = TestSerializationObject()
        encoded = s.serialize(d)
        #print encoded
        self.assertEqual('{"age": 2, "name": "dru"}', encoded)

    def test_deserialization(self):
        s = Serializer()
        data = '{"age": 2, "name": "dru"}'
        obj = s.deserialize(data)
        self.assertEqual(2, obj.age)
        self.assertEqual("dru", obj.name)

    def test_serialization_hierarchy(self):
        s = Serializer()
        d = TestSerializationHierarchyObject()
        encoded = s.serialize(d)
        #print encoded
        self.assertEqual('{"obj": {"age": 2, "name": "dru"}, "boss": "rob"}', encoded)

    def test_deserialization_hierarchy(self):
        s = Serializer()
        data = '{"obj": {"age": 2, "name": "dru"}, "boss": "rob"}'
        obj = s.deserialize(data)
        self.assertEqual('rob',obj.boss)
        self.assertEqual(2, obj.obj.age)
        self.assertEqual("dru", obj.obj.name)
