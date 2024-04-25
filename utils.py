from dateutil import parser
import time
from datetime import datetime
import re


def location_helper(city_name):
    return city_name.lower().replace(" ", "%20").replace(",", "")

state_to_timezone_offset = {
    'AL': -6,
    'AK': -9,  # Most of Alaska is -9, but the Aleutian Islands are -10.
    'AZ': -7,  # Arizona does not observe DST except for the Navajo Nation.
    'AR': -6,
    'CA': -8,
    'CO': -7,
    'CT': -5,
    'DE': -5,
    'FL': -5,  # The Florida Panhandle is in Central Time, so -6.
    'GA': -5,
    'HI': -10,
    'ID': -7,  # Northern Idaho is -8.
    'IL': -6,
    'IN': -5,  # Some parts of Indiana are -6.
    'IA': -6,
    'KS': -6,  # Some parts of Kansas are -7.
    'KY': -5,  # Western parts of Kentucky are -6.
    'LA': -6,
    'ME': -5,
    'MD': -5,
    'MA': -5,
    'MI': -5,  # Some parts of the Upper Peninsula are -6.
    'MN': -6,
    'MS': -6,
    'MO': -6,
    'MT': -7,
    'NE': -6,  # Western Nebraska is -7.
    'NV': -8,
    'NH': -5,
    'NJ': -5,
    'NM': -7,
    'NY': -5,
    'NC': -5,
    'ND': -6,  # Southwestern parts of North Dakota are -7.
    'OH': -5,
    'OK': -6,
    'OR': -8,  # Eastern Oregon is -7.
    'PA': -5,
    'RI': -5,
    'SC': -5,
    'SD': -6,  # Western South Dakota is -7.
    'TN': -6,  # Eastern Tennessee is -5.
    'TX': -6,  # El Paso and parts of West Texas are -7.
    'UT': -7,
    'VT': -5,
    'VA': -5,
    'WA': -8,
    'WV': -5,
    'WI': -6,
    'WY': -7
}

def datetime_location_to_epoch(date_str, time_str, location):

    abbrev = re.search(r'^.*([A-Z]{2}),? \d{5}$', location)
    if abbrev is None:
        return None
    
    state = abbrev.group()

    unix_offset = state_to_timezone_offset.get(state, 0) * 60 * 60

    # Combine the date and time string
    combined_string = f"{date_str} {time_str}"

    # Define the format for parsing
    format_string = '%A %b %d, %Y %I:%M%p'

    # Parse the combined string into a datetime object
    datetime_object = datetime.strptime(combined_string, format_string)

    # Convert the datetime object into epoch time
    epoch_time = int(time.mktime(datetime_object.timetuple()))

    epoch_time += unix_offset
    
    return epoch_time

def stringtime_to_datetime(str):
    return parser.parser(str)