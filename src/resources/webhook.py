from modules.szchat.webhook import parseData

from flask import request
from flask_restful import Resource, reqparse

import sys
import json
import re

class szHook(Resource):
    def post(self):
        json_dt = request.get_json(force=True)
        #json_dt = parseData(request.form.to_dict())
        print(json.dumps(json_dt, indent=4, sort_keys=True))
        return json_dt