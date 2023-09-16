import requests
import json

import utils.variable_utils as variable_utils

CARBON_INTENSITY_ENDPOINT = "https://api.carbonintensity.org.uk"
COVID_INTENSITY_ENDPOINT = "https://api.coronavirus.data.gov.uk"

COVID_METRIC = "newCasesByPublishDate"

region_file = open("regions.json")
REGIONS = json.load(region_file)

def get_data(api):
    response = requests.get(f"{api}")
    if response.status_code == 200:
        return response.json()
    
def get_carbon_intensity_by_date(area_type, start_date_iso8601, end_date_iso8601, regionid):
    print(f"{CARBON_INTENSITY_ENDPOINT}/{area_type}/intensity/{start_date_iso8601}/{end_date_iso8601}/regionid/{regionid}")
    return get_data(f"{CARBON_INTENSITY_ENDPOINT}/{area_type}/intensity/{start_date_iso8601}/{end_date_iso8601}/regionid/{regionid}")

def get_covid_cases_by_date(date: str, regionid: str):
    date = variable_utils.convert_date_without_time(date)
    covid_cases_data = get_data(f"{COVID_INTENSITY_ENDPOINT}/generic/soa/region/{REGIONS[str(regionid)]['areaCode']}/{COVID_METRIC}?date={date}")
    if covid_cases_data:
        return covid_cases_data["payload"]["value"]
    return 0

def parsed_data_format(carbon_intensity_data):
    general_data_info = carbon_intensity_data
    single_data = carbon_intensity_data["data"]

    parsed_data = {
            "regionid": general_data_info["regionid"],
            "region": general_data_info["shortname"],
            "carbondata": [ 
                {
                    "from": entry["from"],
                    "to": entry["to"],
                    "carbonintensity": entry["intensity"],
                    "covidcases": (
                        get_covid_cases_by_date(entry["from"], general_data_info["regionid"])
                    )
                } 
                for entry in single_data ]
            }
    return parsed_data

def parsed_data(area_type, start_date_iso8601, end_date_iso8601, regionid):
    carbon_intensity_data = get_carbon_intensity_by_date(area_type, start_date_iso8601, end_date_iso8601, regionid)
    if carbon_intensity_data:
        if "data" in carbon_intensity_data and carbon_intensity_data["data"]["data"]:
            return parsed_data_format(carbon_intensity_data["data"])
        elif "error" in carbon_intensity_data: 
            return {"error": carbon_intensity_data["error"]["code"], "message" : "Failed to retrieve carbon data: " + carbon_intensity_data["error"]["message"]}
    return {"message": "No Data Found for Carbon Intensity. Please make sure date range is valid (<60 days or end date is after start date)"}