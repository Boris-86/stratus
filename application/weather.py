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
import json
#===============================================================================
#                            Constants & Variables
#===============================================================================
API_KEY = 'VHGVWTTHTARHVPJLESFA9CYAV'
SUCCESS_CODE = 200
FANTASY_LANDS = ['on Mars', 'on Omicron Persei 8', 'on the Moon']
UNIT_GROUP = 'metric'
CONTENT_TYPE = 'json'
ELEMENTS = 'datetime,tempmax,tempmin,temp,humidity'
#===============================================================================
#                             Classes & Functions
#===============================================================================
def seven_days_forecast(city):
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
    baseurl = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next7days"
    params = {'unitGroup': UNIT_GROUP,
              'elements': ELEMENTS,
              'key': API_KEY,
              'contentType': CONTENT_TYPE }

    data = get(baseurl, params)
    status = data.status_code
    if status != SUCCESS_CODE:
        return {'status': status,
                'message': f"Sorry, We do not support cities {random.choice(FANTASY_LANDS)}. Yet"}
    content = json.loads(data.content)
    res_addr = content['resolvedAddress']
    curr_cond = content['currentConditions']
    days_list = [{attr: day[attr]
                  for attr in ['datetime', 'temp', 'tempmin', 'tempmax', 'humidity']}
                 for day in content['days']]
    for day in days_list:
        day['weekday'] = datetime.strptime(day['datetime'], '%Y-%m-%d').strftime('%A')
        day['datetime'] = "/".join(day['datetime'].split("-")[::-1])
    fdict = {'status': status, 'res_addr': res_addr, 'curr_cond': curr_cond, 'days': days_list}

    return fdict

#===============================================================================
#                                    MAIN
#===============================================================================
if __name__ == "__main__":
    print(seven_days_forecast('haifa'))
#===============================================================================
#                                 END OF FILE
#===============================================================================
