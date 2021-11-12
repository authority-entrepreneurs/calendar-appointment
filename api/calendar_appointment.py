import json

import requests


class GoHighLevel:

    def __init__(self, cred_headers=None):
        self.cred_headers = {
            'Authorization': 'Bearer f0f13f30-3c7c-4ada-b280-4582344bfec0',
            'Content-Type': 'application/json'
        }
    
    def post_appointment(self, phone, apptDate):

        appointment_url = "https://rest.gohighlevel.com/v1/appointments/"
        payload = {
            "email":phone,
            "selectedSlot":apptDate,
            "selectedTimezone":"America/Bahia_Banderas",
            "calendarId":"ys6QHQsWSyd1NWs8zvJ6_1636724585481"
            }

        response = requests.request("POST", appointment_url, 
                                    headers=self.cred_headers, 
                                    data=json.dumps(payload))
        return response.json()

go_high = GoHighLevel()
