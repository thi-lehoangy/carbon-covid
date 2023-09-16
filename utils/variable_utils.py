from typing import List

from datetime import datetime, date, timedelta

TODAY_ISO8601 = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
TODAY_YYYY_MM_DD = datetime.now().strftime("%Y-%m-%d")
YESTERDAY_YYYY_MM_DD = (datetime.now() - timedelta(days = 1)).strftime("%Y-%m-%d")

def get_area_type(regionid: str):
    nationalid_set: set = ("1", "2", "6", "7", "15", "16", "17")
    area_type = "regional"
    if regionid in nationalid_set:
        area_type = "national"
    else: 
        area_type = "regional"
    return area_type

def convert_string_date_to_object(start_date: str, end_date: str) -> List[datetime]:
    start_y, start_m, start_d = start_date.split("-")
    end_y, end_m, end_d = end_date.split("-")
    start_date = date(int(start_y), int(start_m), int(start_d))
    end_date = date(int(end_y), int(end_m), int(end_d))

    iso8601_format = [start_date.strftime("%Y-%m-%dT%H:%M:%SZ"), end_date.strftime("%Y-%m-%dT%H:%M:%SZ")]
    iso_format = [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
    return [iso8601_format, iso_format]

def convert_date_without_time(date: str):
    parsed_start_time = datetime.strptime(date, "%Y-%m-%dT%H:%MZ")
    date = parsed_start_time.strftime("%Y-%m-%d")
    return date
