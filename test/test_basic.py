import unittest
import shutil
import tempfile
from pydirl.app import create_app
from . import populate_directory


class PydirlTestCase(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp(prefix='pydirl_test_')
        populate_directory(self.root)
        app = create_app({'ROOT': self.root})
        self.app = app.test_client()

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_root(self):
        rsp = self.app.get('/')
        self.assertEqual(rsp.status_code, 200)

    def test_download_root(self):
        rsp = self.app.get('/?dowload=true')
        self.assertEqual(rsp.status_code, 200)

    def test_download_2_level_file(self):
        rsp = self.app.get('/1/1-1/1-1.txt')
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.data, b'standard-content 1-1')

    def test_req_empty_folder(self):
        rsp = self.app.get('empty/')
        self.assertEqual(rsp.status_code, 200)

    def test_direct_on_folder(self):
        '''Redirect when an existing folder
           is requested without the trailing slash
        '''
        rsp = self.app.get('empty')
        self.assertEqual(rsp.status_code, 302)

    def test_not_redirect_on_folder(self):
        '''Not redirect when a not existing folder
           is requested without the trailing slash
        '''
        rsp = self.app.get('empty/notexists')
        self.assertEqual(rsp.status_code, 404)

    def test_req_notexisting_folder_depth_1(self):
        rsp = self.app.get('empty/notexists/')
        self.assertEqual(rsp.status_code, 404)

    def test_req_notexisting_folder_depth_3(self):
        rsp = self.app.get('empty/notexists/not2/not3/')
        self.assertEqual(rsp.status_code, 404)

    def test_req_notexisting_folder_with_existing_prefix(self):
        ''' Ask a path that as a prefix that match an existing file

            os.listdir in this case should raise OSError with ENOTDIR and not with the
            standard ENOENT
        '''
        rsp = self.app.get('/1/1-1/1-1.txt/asd/notexists1/notexists2/notexists3/')
        self.assertEqual(rsp.status_code, 404)
