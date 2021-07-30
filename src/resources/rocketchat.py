from flask import request
from flask_restful import reqparse, abort, Resource
import sys

sys.path.append('../')

from modules.rocketchat.rchat import RChat

class rcStatsResource(Resource):
    def get(self):

        rc = RChat()
        return rc.stats()