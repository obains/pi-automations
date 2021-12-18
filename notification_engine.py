import datetime

import Weather.controller as weather
import Notifier.pushbot as notifier
import notification_times

if __name__ == '__main__':
    current_hour = datetime.datetime.now().hour

    if current_hour in notification_times.times_dict["controller_rain"]:
        body, title = weather.controller_rain()
        if (body, title ) == (None, None):
            notifier.create_push(body, title)

