import datetime
import pandas as pd
from pandas import json_normalize

## General Parsers
def parse_alerts(response_json):
	try:
		alerts_title = response_json["alerts"]["event"]
		alerts_desc = response_json["alerts"]["description"]
		return alerts_title, alerts_desc
	except KeyError:
		return None, None


def parse_weather(response_json, time_period="hourly"):
    tmp_list = response_json[time_period]
    return tmp_list


def dt_limiter(response_list, cut_off="eod"):
    if cut_off == "eod":
        time_limit = datetime.datetime.today().replace(hour=0, minute= 0, second=0, microsecond=0) + datetime.timedelta(1)

    cleaned_list = []

    for x in response_list:
        if datetime.datetime.fromtimestamp(x["dt"]) < time_limit:
            cleaned_list.append(x)
    
    return cleaned_list


## Rain Parsers
def will_it_rain_this_hour(minutely_list):
    rain = False
    for x in minutely_list:
        if x["precipitation"] > 0:
            rain = True
    return rain


def when_will_it_rain_this_hour(minutely_list):
    df = json_normalize(minutely_list)
    df["dt"] = pd.to_datetime(df["dt"], unit="s")
    time_list = ["10", "10-20", "20-30", "30-40", "40-50", "50-60"]
    precipitation_breakdown = df.groupby(pd.cut(df["dt"], 6, labels=time_list))[["precipitation"]].sum()
    precipitation_df = precipitation_breakdown[precipitation_breakdown["precipitation"] > 0]
    
    return precipitation_df


def when_will_it_rain_today(hourly_list):
    def add_nested_dict(precipitation_dict, x, precipitation_amount, main_weather, description):
        precipitation_dict[x["dt"]] = {
            "precipitation": precipitation_amount,
            "main_weather": main_weather,
            "description": description
            }
    
    #hourly_list = dt_limiter(hourly_list)

    precipitation_dict = {}

    for x in hourly_list:
        main_weather = x["weather"][0]["main"]
        description = x["weather"][0]["description"]
        if (main_weather == "Rain")| (main_weather == "Drizzle") | (main_weather == "Thunderstorm"):
            precipitation_amount = x["rain"]["1h"]
            add_nested_dict(precipitation_dict, x, precipitation_amount, main_weather, description)
        elif main_weather == "Snow":
            precipitation_amount = x["snow"]
            add_nested_dict(precipitation_dict, x, precipitation_amount, main_weather, description)

    return precipitation_dict


if __name__ == '__main__':
    import api
    response_json = api.get_forecast_weather(exclude_list=["current","daily"])
    minutely_list = parse_weather(response_json, time_period="minutely")
    hourly_list = parse_weather(response_json, time_period="hourly")

    #print(minutely_list)
    #x = when_will_it_rain_this_hour(minutely_list)
    x = when_will_it_rain_today(hourly_list)
    print(x)
