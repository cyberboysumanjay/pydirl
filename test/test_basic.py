import unittest
from pydirl.app import create_app


class PydirlTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def test_root(self):
        rsp = self.app.get('/')
        self.assertEqual(rsp.status_code, 200)
