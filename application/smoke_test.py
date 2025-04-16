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
import json
import os
#===============================================================================
#                           Constants & Variables
#===============================================================================
SUCCESS = 200
CONFIG_FILE = "test_config.json"
#===============================================================================
#                             Classes & Functions
#===============================================================================
class TestWebApplication(unittest.TestCase):
    def testApp(self):      

        if not os.path.exists(CONFIG_FILE):
            self.fail(f"[ERROR] Config file '{CONFIG_FILE}' not found.")
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        
        address = config.get("address")
        port = config.get("port")      
        
        url = f"http://{address}:{port}"
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