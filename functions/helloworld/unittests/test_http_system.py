from unittest import TestCase
import os
import requests


class TestHttpSystem(TestCase):
    def test_no_args(self):
        BASE_URL = os.getenv('BASE_URL', 'https://us-central1-xadrex-explorer.cloudfunctions.net/hello_http')
        assert BASE_URL is not None

        res = requests.get(f"{BASE_URL}/hello_http")

        self.assertEqual('Hello World!', res.text)
