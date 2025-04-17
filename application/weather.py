#===============================================================================
# Boris Rozenman (c). 
# 
# Python Web Application Pipeline
# Deploy on local environment simulating a whole CI/CD
#===============================================================================

#===============================================================================
#                                 Libraries
#===============================================================================
from requests import get
from datetime import datetime
import random
#===============================================================================
#                            Constants & Variables
#===============================================================================
API_KEY = 'VHGVWTTHTARHVPJLESFA9CYAV'
SUCCESS_CODE = 200
FANTASY_LANDS = ['Mars', 'Omicron Persei 8', 'the Moon']
UNIT_GROUP = 'metric'
CONTENT_TYPE = 'json'
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
FORECAST_DAYS = 7
RESPONSE_ELEMENTS = ['datetime', 'tempmax', 'tempmin', 'temp', 'humidity']
PARAMS = {
    'unitGroup': UNIT_GROUP,
    'elements': ','.join(RESPONSE_ELEMENTS),
    'key': API_KEY,
    'contentType': CONTENT_TYPE
}
#===============================================================================
#                             Classes & Functions
#===============================================================================
def seven_days_forecast(city: str) -> dict:
    """
    Fetches a 7-day weather forecast for the specified city using the Visual Crossing API.
    Args:
        city (str): Name of the city to fetch forecast for.
    Returns:
        dict: A dictionary containing status, resolved address, current conditions,
              and a list of weather data for each of the next 7 days.
    """
    # Ensure a comma is added if there's no space (for cities like 'London, UK')
    if ' ' not in city:
        city += ','
    url = f"{BASE_URL}/{city}/next{FORECAST_DAYS}days"
    response = get(url, params=PARAMS)
    if response.status_code != SUCCESS_CODE:
        return {
            'status': response.status_code,
            'message': f"Sorry, we do not support cities on {random.choice(FANTASY_LANDS)}. Yet."
        }
    content = response.json()    
    res_addr = content['resolvedAddress']
    curr_cond = content['currentConditions']

    days_list = []
    for day in content['days']:
        day_info = {
            'datetime': "/".join(day['datetime'].split("-")[::-1]),
            'temp': day['temp'],
            'tempmin': day['tempmin'],
            'tempmax': day['tempmax'],
            'humidity': day['humidity'],
            'weekday': datetime.strptime(day['datetime'], '%Y-%m-%d').strftime('%A')
        }
        days_list.append(day_info)
    
    forecast_dict = {
        'status': response.status_code,
        'res_addr': res_addr,
        'curr_cond': curr_cond,
        'days': days_list
    }
    return forecast_dict

#===============================================================================
#                                    MAIN
#===============================================================================
if __name__ == "__main__":
    print(seven_days_forecast('haifa'))
#===============================================================================
#                                 END OF FILE
#===============================================================================