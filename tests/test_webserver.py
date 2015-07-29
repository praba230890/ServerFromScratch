"""
Before runnning this test, start the webserver first
"""

import unittest
import requests

from http import webserver

class TestServer(unittest.TestCase):
    def test_root(self):
        response = requests.get('http://127.0.0.1:8888')
        self.assertEqual(response.text, """This is index file
second line""")
    
    def test_by_file_name(self):
        response = requests.get('http://127.0.0.1:8888/index.html')
        self.assertEqual(response.text, """This is index file
second line""")
        
    def test_with_invalid_file(self):
        response = requests.get('http://127.0.0.1:8888/indml')
        self.assertEqual(response.text, "Invalid request")

if __name__ == "__main__":
    unittest.main()