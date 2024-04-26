from dateutil import parser
import time
from datetime import datetime
import re


def location_helper(city_name):
    return city_name.lower().replace(" ", "%20").replace(",", "")

def ISO_8601_to_datetime(ISO_8601_str):
    # Convert ISO 8601 string to datetime object
    dt_object = datetime.fromisoformat(ISO_8601_str.replace("Z", "+00:00"))

    return dt_object