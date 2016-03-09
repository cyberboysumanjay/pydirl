import unittest
import shutil
import tempfile
import os
from pydirl.app import create_app
from . import populate_directory


class PydirlSingleTestCase(unittest.TestCase):

    def setUp(self):
        self.tmpFolder = tempfile.mkdtemp(prefix='pydirl_test_')
        populate_directory(self.tmpFolder)
        self.root = os.path.join(self.tmpFolder, '1/1-1/1-1.txt')
        app = create_app({'DEBUG': True, 'ROOT': self.root})
        self.app = app.test_client()

    def tearDown(self):
        shutil.rmtree(self.tmpFolder)

    def test_redirect(self):
        rsp = self.app.get('/in/the/middle/of/nowhere')
        self.assertEqual(rsp.status_code, 302)

    def test_download(self):
        rsp = self.app.get(os.path.basename(self.root))
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.data, b'standard-content 1-1')
