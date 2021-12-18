import datetime

import Weather.api as api
import Weather.communication as communication
import Weather.parser as parser

def get_data():
    response_json = api.get_forecast_weather(exclude_list=["current","daily"])

    return response_json


def rain_hourly(response_json):
    minutely_list = parser.parse_weather(response_json, time_period="minutely")
    tmp_dict = {}

    if parser.will_it_rain_this_hour(minutely_list) is True:
        precipitation_breakdown = parser.when_will_it_rain_this_hour(minutely_list)
        message = []
        for i in range(len(precipitation_breakdown)):
            message.append(f"In the next {precipitation_breakdown.index[i]} minutes ({str(precipitation_breakdown['precipitation'][i])}mm).")
        
        tmp_dict[communication.communication_dict["title"]["rain_this_hour"]] = "\n".join(message)

        return tmp_dict
    
    else:
        return tmp_dict

    

def rain_daily(response_json):
    hourly_list = parser.parse_weather(response_json, time_period="hourly")
    precipitation_dict = parser.when_will_it_rain_today(hourly_list)
    tmp_dict = {}

    if len(precipitation_dict) > 0:
        message = []
        for i in precipitation_dict:
            rain_time = datetime.datetime.fromtimestamp(i).strftime("%H:%M")
            rain_message = f"{precipitation_dict[i]['description']} ({str(precipitation_dict[i]['precipitation'])}mm)"
            message.append(f"At {rain_time} there will be {rain_message}.")

        tmp_dict[communication.communication_dict["title"]["rain_today"]] = "\n".join(message)

        return tmp_dict
    
    else:
        return tmp_dict


## Controllers
def controller_rain():
    response_json = get_data()
    rain_hourly_dict = rain_hourly(response_json)
    rain_daily_dict = rain_daily(response_json)

    (rain_title, rain_message) = (None, None)

    if len(rain_hourly_dict) > 0:
        print(type(rain_hourly_dict), rain_hourly_dict)
        rain_title = list(rain_hourly_dict.keys())[0]
        rain_message = list(rain_hourly_dict.values())[0]

    if len(rain_daily_dict) > 0:
        if rain_title is not None:
            print(type(rain_daily_dict), rain_daily_dict)
            communication.communication_dict["title"]["rain_this_hour_and_today"]
            rain_message = rain_message + "\n" + list(rain_daily_dict.values())[0]
        else:
            rain_title = list(rain_daily_dict.keys())[0]
            rain_message = list(rain_daily_dict.values())[0]
    return rain_title, rain_message


if __name__ == '__main__':
    response_json = get_data()
    rain_hourly_dict = rain_hourly(response_json)
    rain_daily_dict = rain_daily(response_json)