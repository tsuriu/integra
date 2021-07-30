from datetime import datetime
from .ixc_utils import ixcreqs, cpfFormater
import time
import base64
import json
import operator
import random
import os


class IXC(object):
    """
    ixc will keep in contact with IXC server.
    """

    ixc_domain = os.environ.get("IXC_DOMAIN")
    ixc_key = os.environ.get("IXC_KEY")

    def __init__(self):
        self.base_url = "https://{}/webservice/v1".format(self.ixc_domain)
        self.token = self.ixc_key.encode('utf-8')

        self.header_template = {
            'ixcsoft': '',
            'Authorization': 'Basic {}'.format(base64.b64encode(self.token).decode('utf-8')),
            'Content-Type': 'application/json'
            }

        self.req = {
                    'base_url': self.base_url,
                    'token': self.token,
                    'headers': self.header_template
                    }
                    
        self.payload = {
                        'page': '1',
                        'rp': '1',
                        'sortorder': 'desc'
                       }

    def clientCheck(self, qdata):
        self.req['endpoint'] = "/cliente"
        self.req['method'] = "POST"
        self.req['headers']['ixcsoft'] = "listar"

        self.payload['qtype'] = "cnpj_cpf"
        self.payload['query'] = cpfFormater(str(qdata)) 
        self.payload['oper'] = "="

        ixc_client_keys = ['id', 'tipo_pessoa', 'cnpj_cpf', 'razao', 'ativo', 'id_condominio','endereco', 'numero', 'complemento', 'bairro']

        data_temp = ixcreqs(self.req, json.dumps(self.payload), output="json")
        data = {}
        
        data['status'] = data_temp['total']

        if data['status'] != '0':

            for dt in data_temp['registros']:
                kList = dt.keys()
                for key in kList:
                    if key in ixc_client_keys:
                        idx = ixc_client_keys.index(key)
                        nkey = ixc_client_keys[idx]

                        data[nkey] = dt[key]
                
        return data

    def contractCheck(self, qdata):
        self.req['endpoint'] = '/cliente_contrato'
        self.req['method'] = 'POST'
        self.req['headers']['ixcsoft'] = 'listar'

        self.payload['qtype'] = 'cliente_contrato.id_cliente'
        self.payload['query'] = qdata 
        self.payload['oper'] = '='
        self.payload['rp'] = '666'

        ixc_contract_keys = ['id', 'status', 'status_internet', 'status_velocidade', 'id_vd_contrato', 'data_ativacao', 'data_cancelamento']

        data_temp = ixcreqs(self.req, json.dumps(self.payload), output="json")
        data = {}
        continfo = []

        for dt in data_temp['registros']:
            contST = dt['status']
            tdata = {}
            if contST == "A":
                for k in ixc_contract_keys:
                    tdata.update({k:dt[k]})
                    

                continfo.append(tdata)

        data['continfo'] = continfo
        data['count'] = len(data['continfo'])

        return data

    def productCheck(self, qdata):
        self.req['endpoint'] = '/produtos'
        self.req['method'] = 'POST'
        self.req['headers']['ixcsoft'] = "listar"

        self.payload['qtype'] = "produtos.id"
        self.payload['query'] = qdata
        self.payload['oper'] = "="

        data_temp = ixcreqs(self.req, json.dumps(self.payload), output="json")
        data = {}

        ixc_product_keys = ['id', 'ativo', 'descricao', 'preco_base']

        for dt in data_temp['registros']:
            kList = dt.keys()
            for key in kList:
                if key in ixc_product_keys:
                    data.update({key: dt[key]})

        return data


    def loginCheck(self, qdata):

        pass
    

    def planCheck(self, qdata):
        self.req['endpoint'] = '/radgrupos'
        self.req['method'] = 'POST'
        self.req['headers']['ixcsoft'] = 'listar'

        self.payload['qtype'] = 'radgrupos.id'
        self.payload['query'] = qdata 
        self.payload['oper'] = '='

        data_temp = ixcreqs(self.req, json.dumps(self.payload), output="json")
        data = {}

        ixc_plan_keys = ['id', 'id_produto', 'download', 'upload', 'valor_produto']

        for dt in data_temp['registros']:
            kList = dt.keys()
            for key in kList:
                if key in ixc_plan_keys:
                    data.update({key: dt[key]})

        return data

    def financialCheck(self, qdata):
        self.req['endpoint'] = '/fn_areceber'
        self.req['method'] = 'POST'
        self.req['headers']['ixcsoft'] = 'listar'

        self.payload['qtype'] = 'fn_areceber.id_cliente'
        self.payload['query'] = qdata
        self.payload['oper'] = '='
        self.payload['rp'] = '2000'

        data_temp = ixcreqs(self.req, json.dumps(self.payload), output="json")
        data = {}
        documents = []
        lastpay = {}
        vdate = ""

        ixc_fat_keys = ['id', 'id_contrato', 'status', 'liberado', 'boleto', 'pagamento_data', 'pagamento_valor', 'data_emissao', 'data_vencimento', 'documento', 'valor', 'valor_aberto', 'valor_cancelado', 'valor_recebido']

        for dt in data_temp['registros']:
            tdata = {}
            docST = dt['status']
            
            if (dt['pagamento_data'] != "") and (len(list(lastpay.keys())) == 0):
                vdate = dt['data_vencimento']

                for k in ixc_fat_keys:
                    if "data" in k:
                        Y,M,D = (dt[k]).split("-")
                        ndate2 = "{}/{}/{}".format(D,M,Y)
                        lastpay.update({k:ndate2})
                    else:
                        lastpay.update({k:dt[k]})

                
                vdate = (vdate.split("-"))[-1]

            if docST not in ["R", "C"]:
                for k in ixc_fat_keys:
                    if "data_" in k:
                        Y,M,D = (dt[k]).split("-")
                        ndate = "{}/{}/{}".format(D,M,Y)

                        if "vencimento" in k:
                            diffDate = (datetime.now() - datetime.strptime(dt[k], "%Y-%m-%d"))
                            if diffDate.days > 0:
                                tdata.update({'situacao': 'Vencido'})
                            if diffDate.days < 0:
                                tdata.update({'situacao': 'A Vencer'})
                        
                        tdata.update({k:ndate})
                    else:
                        tdata.update({k:dt[k]})

                documents.append(tdata)
        
        documents.reverse()
        
        data['count'] = len(documents)
        if data['count'] != 0:
            for doc in documents:
                doc['docorder'] = documents.index(doc) + 1
            data['docinfo'] = documents
        
        data['lastpaid'] = lastpay
        data['vdate'] = vdate
        
        return data

    def subjectCheck(self, qdata):
        self.req['endpoint'] = '/su_oss_assunto'
        self.req['method'] = 'POST'
        self.req['headers']['ixcsoft'] = "listar"

        self.payload['qtype'] = "su_oss_assunto.id"
        self.payload['query'] = qdata
        self.payload['oper'] = "="

        data_temp = ixcreqs(self.req, json.dumps(self.payload), output="json")
        data = {}

        if data_temp['registros']:
            data['status'] = "SUCCESS"
            data['id'] = (data_temp['registros'][0])['id']
            data['assunto'] = (data_temp['registros'][0])['assunto']

        else: 
            data['status'] = "FAIL"           
        
        return data

    def osCheck(self,qdata):
        self.req['endpoint'] = '/su_oss_chamado'
        self.req['method'] = 'POST'
        self.req['headers']['ixcsoft'] = "listar"

        self.payload['qtype'] = "su_oss_chamado.{}".format(qdata['seekkey'])
        self.payload['query'] = qdata['seekpar']
        self.payload['oper'] = "="
        self.payload['rp'] = '666'

        ixc_os_keys = ["id","data_hora_analise", "data_hora_encaminhado", "data_hora_assumido", "data_hora_execucao", "data_abertura", "setor", "tipo", "status", "id_atendente", "mensagem", "protocolo", "data_fechamento"]

        data_temp = ixcreqs(self.req, json.dumps(self.payload), output="json")
        data = {}

        if data_temp['registros']:
            for dt in data_temp['registros']:
                for k in list(dt.keys()):
                    if k not in ixc_os_keys:
                        del dt[k]

                for k in list(dt.keys()):        
                    if 'data_' in k and dt[k] not in ['0000-00-00 00:00:00',""]:
                        d = datetime.strptime(dt[k], '%Y-%m-%d %H:%M:%S')
                        clock_key = k.replace('data','clock')
                        dt[clock_key] = int(time.mktime(d.timetuple()))

                        age_key = k.replace('data','age')
                        dt[age_key] = int(time.mktime((datetime.now()).timetuple())) - dt[clock_key]

                        data['registros'] = data_temp['registros']

        return data