from dateutil import parser

def location_helper(city_name):
    return city_name.lower().replace(" ", "%20").replace(",", "")

unix_offset = {
    "America/Los_Angeles": 8 * 60 * 60,
    "America/Boise": 7 * 60 * 60,
    "America/Denver": 7 * 60 * 60,
    "America/Phoenix": 7 * 60 * 60,
    "America/Chicago": 6 * 60 * 60,
    "America/Detroit": 5 * 60 * 60,
    "America/New_York": 5 * 60 * 60,
}

def stringtime_to_datetime(str):
    return parser.parser(str)