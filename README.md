# Get Carbon Intensity and COVID Data by Region and Date

## Introduction
This project aims to ease the process of retrieving carbon intensity data and COVID data for a specific region and date. The current APIs from the official sites are hard to utilize due to specific requirements for date format, area code, and metrics

## Goals
- Given: Region and Dates  
- Returns: Carbon Intensity and COVID data  

## Developer Guide
`GET /get_carbon_intensity_and_covid_cases/regionid/{regionid}?start_date={start_date}&end_date={end_date}`
- Regions specified by `regionid`, mapped to `areaCode` in `regions.json`  
- Dates in format YYYY-MM-DD 
    - Default `start_date` is yesterday
    - Default `end_date` is today
- Metric for COVID data is `newCasesByPublishDate`

### Request Limits

- Cutoff date for carbon intensity: May 10th, 2018  
- Start date has to be before end date
- Range cannot be bigger than 60 days 

### Separation of Concerns
- `main.py`: API requests
- `data_utils.py`: get data from Carbon and COVID APIs and parse them
- `variable_utils.py`: validate variables for API requests
- `regions.json`: map regions supported by Carbon API to those of COVID API

### Sample Return Values:

```
{
  "regionid": 7,
  "region": "South Wales",
  "carbondata": [
    {
      "from": "2022-09-14T23:30Z",
      "to": "2022-09-15T00:00Z",
      "carbonintensity": {
        "forecast": 383,
        "index": "very high"
      },
      "covidcases": 0
    },
    {
      "from": "2022-09-15T00:00Z",
      "to": "2022-09-15T00:30Z",
      "carbonintensity": {
        "forecast": 382,
        "index": "very high"
      },
      "covidcases": 294
    },
    // ...more data
}
```



```
{
  "error": "400 Bad Request",
  "message": "Failed to retrieve carbon data: The start datetime should be less than the end datetime i.e. /intensity/2017-08-25T15:30Z/2017-08-27T17:00Z"
}
```

