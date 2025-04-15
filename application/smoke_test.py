import unittest
import requests

address = "localhost"
port = "5000"
SUCCESS = '200'

class TestWeatherProject(unittest.TestCase):

	def testApp(self):
		try:
			http_code = requests.get("${address}:${port}").status_code
			print("Remote Test: Site is O.K!")
		except Exception:
			print("Remote Test: S ite is NOT reachable!")
		return self.assertTrue(http_code == SUCCESS)

if __name__ == '__main__':
    unittest.main()
