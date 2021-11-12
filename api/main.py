import json
import re

from flask import Flask, abort, request
from flask.json import jsonify

from .calendar_appointment import go_high

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = request.args
            phone = data.get('phone')
            apptDate = data.get('apptDate').split('-0600')[0]+'-06:00'
            response = go_high.post_appointment(phone, apptDate)
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

