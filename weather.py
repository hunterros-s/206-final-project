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
        raise Exception(f"Error: {e}")

    if not output.ok:
        raise Exception(f"Output not okay: {output}")
    
    data = output.json()
    location = data.get('location')

    if location is None:
        raise Exception(f"Location is none: {data}")
    
    icao_codes = location.get("icaoCode")

    if icao_codes is None:
        raise Exception(f"Icao codes is none: {location}")

    icao_code = None

    for code in icao_codes:
        if code is None:
            continue
        icao_code = code
        break

    return icao_code

def get_from_icao_datetime_weather(icao_code, datetime):

    unix_time = int(datetime.timestamp())
    # Format datetime as YYYYMMDD string
    formatted_date = datetime.strftime("%Y%m%d")

    # print(unix_time, formatted_date)

    # date is YYYYMMDD format
    # time is unix time (gmt)

    # https://api.weather.com/v1/location/KMSY:9:US/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&startDate=20200102&endDate=20200102
    url = f"https://api.weather.com/v1/location/{icao_code}:9:US/observations/historical.json?apiKey={weather_dot_com_api_key}&units=e&startDate={formatted_date}&endDate={formatted_date}"
    try:
        output = requests.get(url, timeout=3)
        output.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error: {e}")
    
    if not output.ok:
        raise Exception(f"Output not okay: {output}")
    
    data = output.json()

    observations = data.get('observations')
    if observations is None:
        raise Exception(f"Observations invalid: {data}")
    
    weather = observations[0]
    for observation in observations[1:]:
        start_time = observation.get('valid_time_gmt')
        end_time = observation.get('expire_time_gmt')

        if start_time <= unix_time:
            weather = observation
            break
    
    if weather is None:
        raise Exception(f"Weather is invalid: {observations}")
    
    temp = weather.get('temp')
    wspd = weather.get('wspd')
    if wspd is None:
        wspd = 0
    wx_phrase = weather.get('wx_phrase')

    return (temp, wspd, wx_phrase)

def get_weather(location, datetime):
    try:
        icao = get_icao_code(location)
    except Exception as e:
        print(f"Exception: {e}")

    print(location, icao)
    
    return get_from_icao_datetime_weather(icao, datetime)
