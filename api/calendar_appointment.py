import json

import requests
from requests.api import put


class GoHighLevel:

    def __init__(self, cred_headers=None):
        self.cred_headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6InBUZ2RKQktqSXptRUtDUG93bGdCIiwiY29tcGFueV9pZCI6IjFJRzJRdmxFYUJPRndYcWtFYUk0IiwidmVyc2lvbiI6MSwiaWF0IjoxNjQzMzg1NzEyNDczLCJzdWIiOiJ0SXcwWGZkd3NycTZ4d2wwckxMcyJ9.QmpzOrgHHY6AnsAVcr2TE7WpbG2Udxp9mD7W-Xn21oQ',
            'Content-Type': 'application/json'
        }
    
    def get_contact_lookup(self, phone):

        contact_lookup = 'https://rest.gohighlevel.com/v1/contacts/lookup?phone={0}'.format(phone)
        response = requests.request("GET", contact_lookup, 
                                    headers=self.cred_headers)
        result = response.json().get('contacts')[0]
        contacts_id = result.get('id')
        tags = result.get('tags')
        return contacts_id, tags
     
    def put_contact_tags(self, contact_id, tags, apptDate):

        put_contact_endpoint = 'https://rest.gohighlevel.com/v1/contacts/{0}'.format(contact_id)
        if "outside_of_time_slot" not in tags:
            tags.append("outside_of_time_slot")
        payload = {
            "tags":tags,
            "customField":[
                {
                "id": "HPx3074jyCnmTheXupv6",
                "value": apptDate
                }
            ]
        }
        response = requests.request("PUT", put_contact_endpoint, 
                                    headers=self.cred_headers, 
                                    data=json.dumps(payload))
        return response.json()


    def post_appointment(self, phone, apptDate):

        appointment_url = "https://rest.gohighlevel.com/v1/appointments/"
        payload = {
            "phone":phone,
            "selectedSlot":apptDate,
            "selectedTimezone":"America/Chicago",
            "calendarId":"cwEMboMjvEUHA0bs6atY"
            }

        response = requests.request("POST", appointment_url, 
                                    headers=self.cred_headers, 
                                    data=json.dumps(payload))
        if response.json().get('selectedSlot') is None:
            return response.json()
        else:
            new_phone_format = '+1'+''.join(e for e in phone if e.isalnum())
            contact_ids, tags = self.get_contact_lookup(new_phone_format)
            put_response = self.put_contact_tags(contact_ids, tags, apptDate)
            return put_response

go_high = GoHighLevel()
