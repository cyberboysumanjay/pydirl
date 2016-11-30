import unittest
import shutil
import tempfile
from zipfile import ZipFile
from pydirl.app import create_app
from . import populate_directory


class PydirlZippedTestCase(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp(prefix='pydirl_test_')
        populate_directory(self.root)

    def tearDown(self):
        shutil.rmtree(self.root)

    def get_zipped_root(self, regex=None):
        app = create_app({'ROOT': self.root, 'EXCLUDE': regex})
        tc = app.test_client()
        rsp = tc.get('/?download=True')
        self.assertTrue(rsp.is_streamed)
        # store the result byte stream in a temporary file
        tempF = tempfile.TemporaryFile()
        tempF.write(rsp.get_data())
        return tempF

    def test_zipped(self):
        zippedRoot = self.get_zipped_root()
        expected_entries = ['2/2-1/2-1.txt', '1/1-1/1-1.txt']
        zf = ZipFile(zippedRoot)
        self.assertTrue(zf.testzip() is None)
        for elem in expected_entries:
            self.assertTrue(elem in zf.namelist())
        self.assertEqual(len(expected_entries), len(zf.namelist()))
        zf.close()

    def test_zipped_excluded_file(self):
        zippedRoot = self.get_zipped_root('1-1.txt')
        expected_entries = ['2/2-1/2-1.txt']
        zf = ZipFile(zippedRoot)
        self.assertTrue(zf.testzip() is None)
        for elem in expected_entries:
            self.assertTrue(elem in zf.namelist())
        self.assertEqual(len(expected_entries), len(zf.namelist()))
        zf.close()

    def test_zipped_excluded_directory(self):
        zippedRoot = self.get_zipped_root('1/')
        expected_entries = ['2/2-1/2-1.txt']
        zf = ZipFile(zippedRoot)
        self.assertTrue(zf.testzip() is None)
        for elem in expected_entries:
            self.assertTrue(elem in zf.namelist())
        self.assertEqual(len(expected_entries), len(zf.namelist()))
        zf.close()
