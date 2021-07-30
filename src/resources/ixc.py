from flask import jsonify, request
from flask_restful import reqparse, abort, Resource
import sys

sys.path.append('../')

from modules.ixc.ixc_check import IXC
from modules.ixc.ixc_action import IXCAC
from modules.tools.http import http


class clientCheckResource(Resource):
    def post(self):
        json_dt = request.get_json(force=True)

        qdata = json_dt['cpf_cnpj']

        ixc = IXC()
        data = ixc.clientCheck(qdata)
        
        if data['status'] != '0':
            dataCont = ixc.contractCheck(data['id'])

            for cont in dataCont['continfo']:
                dataProd = ixc.productCheck(cont['id_vd_contrato'])
                dataPlan = ixc.planCheck(cont['id_vd_contrato'])

                cont.update({'produto': dataProd})
                cont.update({'plano': dataPlan})        

            data.update({'contratos': dataCont})

            dataFat = ixc.financialCheck(data['id'])

            data.update({'financeiro': dataFat})

        return data

class ticketOpenResource(Resource):
    def post(self):
        pass

class billetFileResource(Resource):
    def post(self):
        json_dt = request.get_json(force=True)

        ixc = IXCAC()
        data = ixc.getBillet(json_dt)

        return data

class unblockContractResource(Resource):
    def post(self):
        data = {}
        json_dt = request.get_json(force=True)

        id_client = json_dt['id_cliente']
        id_contract = json_dt['id_contrato']
        protocol = json_dt['protocolo']
        id_subject = json_dt['id_subject']

        payload_ticket = {
            "protocolo": protocol,
            "id_cliente": id_client,
	        "id_contrato": id_contract,
	        "id_assunto": id_subject,
	        "prioridade": "M",
	        "origem_endereco": "C",
	        "su_status": "N",
            "status": "T",
            "id_ticket_origem": "H",
	        "id_ticket_setor": "1"
            }
        
        ixchk = IXC()

        title = ixchk.subjectCheck(id_subject)

        ixc = IXCAC()

        contract = ixc.unlockContract(id_contract)

        data.update({"unlock_situation": contract})
        data.update({"protocolo": protocol})

        payload_ticket.update({"titulo": title['assunto']})
        payload_ticket.update({"menssagem": contract['msg']})

        ticket = ixc.openTicket(payload_ticket)
        ticket_status = ticket['type']

        if ticket_status != "error":
            ticket_id = ticket['id']
        else:
            ticket_id = "FAIL"

        data.update({"ticket": ticket_id})

        return data

class OsCheckResource(Resource):
    def post(self):
        json_dt = request.get_json(force=True)

        ixc = IXC()

        os = ixc.osCheck(json_dt)
        return os