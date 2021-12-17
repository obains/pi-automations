def parse_alerts(response_json):
	if response_json["alerts"] is not None:
		alerts_title = response_json["alerts"]["event"]
		alerts_desc = response_json["alerts"]["description"]
		return alerts_title, alerts_desc
	else:
		return None, None