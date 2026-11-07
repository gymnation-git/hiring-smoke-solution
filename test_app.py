import json
import threading
import unittest
import urllib.error
import urllib.request

import app


class SmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = app.server(port=0)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def call(self, method, path, body=None):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(self.base + path, data=data, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read())

    def test_echo_counts_characters(self):
        self.assertEqual(self.call("POST", "/echo", {"text": "häy"}), (200, {"text": "häy", "length": 3}))

    def test_sum(self):
        self.assertEqual(self.call("GET", "/sum?a=-5&b=7"), (200, {"sum": 2}))

    def test_validation(self):
        status, body = self.call("GET", "/sum?a=x&b=1")
        self.assertEqual((status, body["error"]["code"]), (422, "VALIDATION"))

    def test_upper(self):
        self.assertEqual(self.call("GET", "/upper?text=abc"), (200, {"text": "ABC"}))


if __name__ == "__main__":
    unittest.main()
