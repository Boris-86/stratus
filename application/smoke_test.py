import unittest
import requests

address = "localhost"
port = "5000"
SUCCESS = 200

class TestWebApplication(unittest.TestCase):
    def testApp(self):
        url = f"http://{address}:{port}"
        http_code = None  # Use None to clearly distinguish from 0

        try:
            response = requests.get(url)
            http_code = response.status_code
            print(f"Smoke Test: Web application at {url} is reachable [O.K].")
            print(f"[INFO] HTTP status code: {http_code}")
        except Exception as e:
            print(f"[X] Smoke Test: Web application at {url} is NOT reachable! [X]")
            print(f"[INFO] Exception: {e}")
            print(f"[INFO] HTTP status code: {http_code}")

        self.assertEqual(http_code, SUCCESS)

if __name__ == '__main__':
    unittest.main()