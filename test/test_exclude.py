import unittest
import shutil
import tempfile
from pydirl.app import create_app
from . import populate_directory


class PydirlExcludeTestCase(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp(prefix='pydirl_test_')
        populate_directory(self.root)

    def tearDown(self):
        shutil.rmtree(self.root)

    def create_app_with_regex(self, regex):
        self.app = create_app({'ROOT': self.root, 'EXCLUDE': regex})
        self.app = self.app.test_client()

    def test_exclude_all(self):
        self.create_app_with_regex(r'.*')
        rsp = self.app.get('/1/1-1/1-1.txt')
        self.assertEqual(rsp.status_code, 404)
        rsp = self.app.get('/1/1-1')
        self.assertEqual(rsp.status_code, 404)
        rsp = self.app.get('/2/')
        self.assertEqual(rsp.status_code, 404)
        rsp = self.app.get('/empty/')
        self.assertEqual(rsp.status_code, 404)

    def test_exclude_file(self):
        self.create_app_with_regex(r'.*1-1.txt')
        rsp = self.app.get('/1/1-1/1-1.txt')
        self.assertEqual(rsp.status_code, 404)

    def test_exclude_file_and_directory(self):
        self.create_app_with_regex(r'.*1-1')
        rsp = self.app.get('/1/1-1')
        self.assertEqual(rsp.status_code, 404)
        rsp = self.app.get('/1/1-1/1-1.txt')
        self.assertEqual(rsp.status_code, 404)

    def test_exclude_directory(self):
        self.create_app_with_regex(r'.*1-1/')
        rsp = self.app.get('/1/1-1/')
        self.assertEqual(rsp.status_code, 404)
