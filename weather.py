import requests

weather_dot_com_api_key = "e1f10a1e78da46f5b10a1e78da96f525"
headers = {
  "Accept": "application/json, text/plain, */*",
  "Referer": "https://www.wunderground.com/",
  "Sec-Ch-Ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
  "Sec-Ch-Ua-Mobile": "?0",
  "Sec-Ch-Ua-Platform": "\"Windows\"",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

def city_name_to_api(city_name):
    return city_name.lower().replace(" ", "%20")

def get_icao_code(city_name):
    # https://api.weather.com/v3/location/search?apiKey=e1f10a1e78da46f5b10a1e78da96f525&language=en-US&query=kansas%20city&locationType=city%2Cairport%2CpostCode%2Cpws&format=json
    city_name = city_name_to_api(city_name)
    print(city_name)
    url = f"https://api.weather.com/v3/location/search?apiKey={weather_dot_com_api_key}&language=en-US&query={city_name}&locationType=city%2Cairport%2CpostCode%2Cpws&format=json"
    print(url)
    try:
        output = requests.get(url, timeout=3)
        output.raise_for_status()  # Raises an exception for 4XX and 5XX status codes
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    if not output.ok:
        return False, None
    
    data = output.json()
    location = data.get('location')

    if location is None:
        return None
    
    icao_codes = location.get("icaoCode")

    if icao_codes is None:
        return False, None

    icao_code = icao_codes[0]

    print(output.text)

    return True, icao_code

def get_weather_metadata(latitude, longitude):
    # https://api.weather.com/v1/location/KARG:9:US/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&startDate=20170415&endDate=20170415
    points = f"https://api.weather.gov/points/{latitude},{longitude}"
    output = requests.get(url=points, headers={"email":"hlross@umich.edu"})

    if output.ok:
        return True, output.text
    else:
        return False, output.text