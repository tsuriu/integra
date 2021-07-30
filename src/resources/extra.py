from flask import json, jsonify, request
from flask_restful import reqparse, abort, Resource
import werkzeug
import requests
import sys
import os

sys.path.append('../')

class GerImages(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        image_file.save("your_file_name.jpg")


class GetDtcOnubyPon(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('host', type=str)
        parser.add_argument('ref_onu', type=str)

        data = parser.parse_args()
        
        onu = os.popen("sshpass -pv3l00.2021 ssh veloonet@{} -oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes256-ctr 'show interface gpon {}' | grep Overhead".format(data['host'], data['ref_onu']))
        onu = (onu.read()).split()

        return int(onu[-2].replace('(',''))


class Mikrotik_PPPCnt(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('host', type=str)
        parser.add_argument('inf', type=str)

        data = parser.parse_args()

        service_name = os.popen("sshpass -pteuaro ssh gay@{} '/interface pppoe-server server print brief where interface={}'".format(data['host'],data['inf']))
        service_name = (((service_name.read()).splitlines())[2].split())[1]
        
        ppp_on_count = os.popen("sshpass -pteuaro ssh gay@{} '/interface pppoe-server print count-only where service={}'".format(data['host'], service_name))
        ppp_on_count = ppp_on_count.read()

        return int(ppp_on_count)


class SendTelegramNotify(Resource):
    def post(self):
        json_dt = request.get_json(force=True)

        token = json_dt['token']
        chat_id = json_dt['sendid']
        subject = json_dt['subject']
        sendMsg = json_dt['sendmsg']

        sendMsg = sendMsg.replace('/n','\n')

        text = "{} \n {}".format(subject,sendMsg)

        url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
        
        result = requests.get(url_req)
        
        return result.json()