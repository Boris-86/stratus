import unittest
import requests

address = "localhost"
port = "5000"
SUCCESS = 200

class TestWebApplication(unittest.TestCase):
	def testApp(self):
		http_code = None
		url = f"{address}:{port}/"
		try:
			response = requests.get(url)
			http_code = response.status_code
			print("Remote Test: Web Site is O.K!")
		except Exception:
			print("Remote Test: Web Site ite is NOT reachable!")
		return self.assertEqual(http_code, SUCCESS)

if __name__ == '__main__':
    unittest.main()