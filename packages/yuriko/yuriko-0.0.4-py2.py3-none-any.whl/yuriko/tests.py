import tempfile
from unittest import TestCase

from yuriko.manager import NotesManager


class NotesManagerTestCase(TestCase):

    PASSWORD = '0' * 16

    def test_manager(self):
        with tempfile.NamedTemporaryFile(suffix='test') as tf:
            manager = NotesManager(path=tf.name, password=self.PASSWORD)
            with self.assertRaises(KeyError):
                manager.search(prefix='t')
            manager.init()
            matches = manager.search(prefix='t')
            self.assertEqual(matches, [])
            manager.edit(key='mykey', value='100')
            matches = manager.search(prefix='my')
            self.assertEqual(matches, ['mykey'])
            self.assertEqual(manager.get('mykey'), '100')

            manager = NotesManager(path=tf.name, password=self.PASSWORD)
            manager.edit('mykey', '101')
            self.assertEqual(manager.get('mykey'), '101')
            manager.delete('mykey')
            self.assertEqual(manager.get('mykey'), '')
