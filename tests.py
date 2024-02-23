import unittest
import time
import os
from repositroy import PersistDataRepository, InMemoryRepository


class TestPersistDataRepository(unittest.TestCase):
    def setUp(self):
        self.store = PersistDataRepository('test_store.pkl')

    def tearDown(self):
        if os.path.exists('test_store.pkl'):
            os.remove('test_store.pkl')

    def test_set_on_duplicate_key(self):
        self.store.set("key", 'value')
        self.store.set('key', 'value1')
        self.assertEqual(self.store.get('key'), 'value1')

    def test_set_get(self):
        self.store.set('key1', 'value1')
        self.assertEqual(self.store.get('key1'), 'value1')

    def test_delete(self):
        self.store.set('key2', 'value2')
        self.store.delete('key2')
        self.assertIsNone(self.store.get('key2'))

    def test_expire(self):
        self.store.set('key3', 'value3')
        self.store.expire('key3', 1)
        self.assertEqual(self.store.get('key3'), 'value3')
        time.sleep(2)
        self.assertIsNone(self.store.get('key3'))

    def test_ttl(self):
        self.store.set('key4', 'value4')
        self.store.expire('key4', 2)
        time.sleep(1)
        self.assertIsNotNone(self.store.ttl('key4'), "Key Deleted Before Expire Time !")

    def test_persistence(self):
        self.store.set('key5', 'value5')
        self.store.expire('key5', 3)
        new_store = PersistDataRepository('test_store.pkl')
        self.assertEqual(new_store.get('key5'), 'value5')
        self.assertAlmostEqual(new_store.ttl('key5'), 3, delta=0.1)


class TestInMemoryRepository(unittest.TestCase):
    def setUp(self):
        self.store = InMemoryRepository()

    def test_set_get(self):
        self.store.set('key1', 'value1')
        self.assertEqual(self.store.get('key1'), 'value1')

    def test_get_non_existent_key(self):
        self.assertIsNone(self.store.get('non_existent_key'))

    def test_delete(self):
        self.store.set('key2', 'value2')
        self.store.delete('key2')
        self.assertIsNone(self.store.get('key2'))

    def test_expire(self):
        self.store.set('key3', 'value3', 2)
        time.sleep(3)  # Wait for the key to expire
        self.assertIsNone(self.store.get('key3'))

    def test_ttl(self):
        self.store.set('key4', 'value4', 5)
        time.sleep(3)
        self.assertIsNotNone(self.store.ttl('key4'), "Key Delete Before Expire Time")

    def test_set_on_duplicate_key(self):
        self.store.set("key", 'value')
        self.store.set('key', 'value1')
        self.assertEqual(self.store.get('key'), 'value1')


if __name__ == '__main__':
    unittest.main()
