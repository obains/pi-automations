import datetime

import api
import communication
import parser

def get_data():
    response_json = api.get_forecast_weather(exclude_list=["current","daily"])

    return response_json


def rain_hourly(response_json):
    minutely_list = parser.parse_weather(response_json, time_period="minutely")
    if parser.will_it_rain_this_hour(minutely_list) is True:
        precipitation_breakdown = parser.when_will_it_rain_this_hour(minutely_list)
        message = []
        for i in range(len(precipitation_breakdown)):
            message.append(f"In the next {precipitation_breakdown.index[i]} minutes ({str(precipitation_breakdown['precipitation'][i])}mm).")

        return communication.communication_dict["title"]["rain_this_hour"], "\n".join(message)
    
    else:
        return None, None

    

def rain_daily(response_json):
    hourly_list = parser.parse_weather(response_json, time_period="hourly")
    precipitation_dict = parser.when_will_it_rain_today(hourly_list)

    if len(precipitation_dict) > 0:
        message = []
        for i in precipitation_dict:
            rain_time = datetime.datetime.fromtimestamp(i).strftime("%H:%M")
            rain_message = f"{precipitation_dict[i]['description']} ({str(precipitation_dict[i]['precipitation'])}mm)"
            message.append(f"At {rain_time} there will be {rain_message}.")

        return communication.communication_dict["title"]["rain_today"], "\n".join(message)
    
    else:
        return None, None


if __name__ == '__main__':
    response_json = get_data()
    title_rain_hourly, message_rain_hourly = rain_hourly(response_json)
    title_rain_daily, message_rain_daily = rain_daily(response_json)