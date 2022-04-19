import json
import re

from flask import Flask, abort, request
from flask.json import jsonify

from .calendar_appointment import GoHighLevel

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = request.args
            phone = data.get('phone')
            apptDate = data.get('apptDate').split('-0500')[0]+'-05:00'
            ghl_key = data.get('ghl_key')
            calendar_id = data.get('calendar_id')
            if ghl_key or calendar_id is None:
                return {
                "message":"Email not Received Successfully",
                "errors":"Ghl key or calendar id is None"
                } 
            gohigh_data = GoHighLevel(headers=ghl_key)
            response = gohigh_data.post_appointment(phone, apptDate, calendar_id)
            return {
                "response":response
            }
        except Exception as e:
            return {
                "message":"Email not Received Successfully",
                "errors":jsonify(e)
            }
    else:
        abort(400)

