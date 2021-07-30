from flask import request
from flask_restful import Resource
import sys

sys.path.append('../')
from modules.mikrotik.mikrotik import mkt

class ResourceMikrotik_PPPCnt(Resource):
    def post(self):
        json_dt = request.get_json(force=True)

        host = json_dt['host']
        interface = json_dt['inf']
        sshusr = json_dt['user']
        sshpwd = json_dt['passwd']

        print(host,interface,sshusr,sshpwd)

        MKT = mkt(host, sshusr, sshpwd)
        cntppp = MKT.onlinePPP(interface)

        return cntppp