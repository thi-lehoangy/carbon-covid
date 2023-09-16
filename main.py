from fastapi import FastAPI

import utils.variable_utils as variable_utils
import utils.data_utils as data_utils

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/carbon_intensity_and_covid_cases/regionid/{regionid}")
async def get_info(regionid: int, start_date: str = variable_utils.YESTERDAY_YYYY_MM_DD, end_date: str = variable_utils.TODAY_YYYY_MM_DD):
    iso8601_format, _ = variable_utils.convert_string_date_to_object(start_date, end_date)
    start_date_iso8601, end_date_iso8601 = iso8601_format

    area_type = variable_utils.get_area_type(regionid)
    parsed_carbon_intensity_data = data_utils.parsed_data(area_type, start_date_iso8601, end_date_iso8601, regionid)

    return parsed_carbon_intensity_data




