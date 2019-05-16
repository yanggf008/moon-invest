# coding: utf-8
import unittest
from tools.email_service import Email


class TestEmail(unittest.TestCase):
    def test_send_email(self):
        title = "Hello, this is the spot price"
        content = "this is the exact price of one cryptocurrency"
        Email.send(title, content)
