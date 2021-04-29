import json

def request_data(json_request: str):
	data = json.load(json_request)
	
	if data is None:
		return
	
	