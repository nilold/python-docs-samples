from unittest import TestCase
from unittest.mock import Mock
from functions.helloworld.main import hello_http


class TestHttpUnit(TestCase):
    def test_print_name(self):
        name = 'Nilo'
        data = {'name': name}

        req = Mock(get_json=Mock(return_value=data), args=data)

        self.assertEqual('Hello {}!'.format(name), hello_http(req))

    def test_print_hello_world(self):
        data = {}

        req = Mock(get_json=Mock(return_value=data), args=data)

        self.assertEqual('Hello World!', hello_http(req))