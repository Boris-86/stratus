#===============================================================================
# Boris Rozenman (c). 
# 
# Python Web Application Pipeline
# Deploy on local environment simulating a whole CI/CD
#===============================================================================

#===============================================================================
#                                 Libraries
#===============================================================================
import unittest
import requests
#===============================================================================
#                           Constants & Variables
#===============================================================================
SUCCESS = 200
adress = "localhost"
port = "5000"

#===============================================================================
#                             Classes & Functions
#===============================================================================
class TestWebApplication(unittest.TestCase):
    def testApp(self):      
        url = f"http://{adress}:{port}"
        http_code = None  
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
#===============================================================================
#                                    MAIN
#===============================================================================
if __name__ == '__main__':
    unittest.main()
#===============================================================================
#                                 END OF FILE
#===============================================================================