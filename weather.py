import requests

from utils import location_helper

weather_dot_com_api_key = "e1f10a1e78da46f5b10a1e78da96f525"

def get_icao_code(location):
    # https://api.weather.com/v3/location/search?apiKey=e1f10a1e78da46f5b10a1e78da96f525&language=en-US&query=kansas%20city&locationType=city%2Cairport%2CpostCode%2Cpws&format=json
    location = location_helper(location)
    url = f"https://api.weather.com/v3/location/search?apiKey={weather_dot_com_api_key}&language=en-US&query={location}&locationType=city%2Cairport%2CpostCode%2Cpws&format=json"
    try:
        output = requests.get(url, timeout=3)
        output.raise_for_status()  # Raises an exception for 4XX and 5XX status codes
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False, None

    if not output.ok:
        return False, None
    
    data = output.json()
    location = data.get('location')

    if location is None:
        return False, None
    
    icao_codes = location.get("icaoCode")

    if icao_codes is None:
        return False, None

    icao_code = icao_codes[0]

    return True, icao_code

def get_weather(icao_code, datetime):

    # date is YYYYMMDD format
    # time is unix time (gmt)

    # https://api.weather.com/v1/location/KMSY:9:US/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&startDate=20200102&endDate=20200102
    url = f"https://api.weather.com/v1/location/{icao_code}:9:US/observations/historical.json?apiKey={weather_dot_com_api_key}&units=e&startDate={date}&endDate={date}"
    try:
        output = requests.get(url, timeout=3)
        output.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False, None
    
    if not output.ok:
        return False, None
    
    data = output.json()

    observations = data.get('observations')
    if observations is None:
        return False, None
    
    weather = None
    for observation in observations:
        start_time = observation.get('valid_time_gmt')
        end_time = observation.get('expire_time_gmt')

        if time >= start_time and time <= end_time:
            weather = observation
            break
    
    if weather is None:
        return False, None
    
    temp = weather.get('temp')
    wspd = weather.get('wspd')
    precip = weather.get('precip_hrly')

    return True, (temp, wspd, precip)
