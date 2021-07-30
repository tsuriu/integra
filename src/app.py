#!/usr/bin/env python3

import os, sys, ssl
from werkzeug import serving
from flask import Flask, send_file, send_from_directory, request, jsonify
from flask_restful import Api, reqparse
from flask_cors import CORS
from resources.ixc import OsCheckResource, clientCheckResource, unblockContractResource, billetFileResource
from resources.rocketchat import rcStatsResource
from resources.webhook import szHook
from resources.extra import GetDtcOnubyPon, SendTelegramNotify, Mikrotik_PPPCnt

sys.path.append('../')


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

api.add_resource(clientCheckResource, '/cpf_check')
api.add_resource(unblockContractResource, '/unblock')
api.add_resource(billetFileResource, '/doclink')
api.add_resource(OsCheckResource, '/oscheck')

api.add_resource(rcStatsResource, '/rc_stats')

api.add_resource(GetDtcOnubyPon, '/getonucnt')
api.add_resource(SendTelegramNotify, '/sendtelegram')

api.add_resource(Mikrotik_PPPCnt, '/cntpppoe')

api.add_resource(szHook, '/hook')

@app.route('/datafiles/<path:filename>', methods=['GET'])
def returnFile(filename):
    path = "/tmp/dataFiles/billets"

    return send_from_directory(directory=path, filename=filename)

  
if __name__ == '__main__':

    app.run(host="0.0.0.0", port=os.environ.get("PORT"), debug=os.environ.get("DEBUG"), threaded=True)