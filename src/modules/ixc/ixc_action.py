from .ixc_utils import ixcreqs, data2PDF
import base64
import json
import os

class IXCAC(object):
    """
    IXCAC will 
    """

    ixc_domain = os.environ.get("IXC_DOMAIN")
    ixc_key = os.environ.get("IXC_KEY")

    def __init__(self):
        self.base_url = "https://{}/webservice/v1".format(self.ixc_domain)
        self.token = self. ixc_key.encode('utf-8')

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
    
    def newProtocol(self):
        self.req['endpoint'] = '/gerar_protocolo_atendimento'
        self.req['method'] = "GET"
        self.req['headers']['ixcsoft'] = "listar"

        data = ixcreqs(self.req)

        return data

    def openTicket(self, qdata):
        self.req['endpoint'] = "/su_ticket"
        self.req['method'] = "POST"

        """
        payload = {
	                "id_cliente": qdata['id_cliente'],
	                "id_contrato": qdata['id_contrato'],
	                "id_assunto": qdata['id_assunto'],
	                "titulo": qdata['titulo'],
	                "menssagem": qdata['menssagem'],
	                "prioridade": qdata['prioridade'],
	                "origem_endereco": qdata['origem_endereco'],
	                "su_status": qdata['su_status'],
	                "id_ticket_setor": qdata['setor']
                }
        """
        payload = qdata

        if 'protocolo' in qdata.keys():
            proto = qdata['protocolo']
        else:
            proto = self.newProtocol()
        
        payload['protocolo'] = proto

        data = ixcreqs(self.req, json.dumps(payload), output="json")
        
        return data

    def insertTicketInteration(self, qdata):
        self.req['endpoint'] = "/su_mensagens"
        self.req['method'] = "POST"

        payload = {
	                "id_cliente": qdata['id_cliente'],
	                "id_ticket": qdata['id_ticket'],
	                "menssagem": qdata['message'],
                    "operador": qdata['operador'],
	                "su_status": qdata['su_status'],
                    "status": qdata['status'],
                    "existe_pendencia_externa": qdata['pendendica']
                }

        data = ixcreqs(self.req, self.header_template, json.dumps(payload))

        return data
                    
    def getBillet(self, qdata):
        billet_data = {}
        payload = {                    
                    'juro': 'N',
                    'multa': 'N',
                    'atualiza_boleto': 'N'
                  }
        
        self.req['endpoint'] = '/get_boleto'
        self.req['method'] = "POST"
        self.req['headers']['ixcsoft'] = "listar"

        payload['boletos'] = qdata['documentid']
        payload['tipo_boleto'] = 'dados'

        data = ixcreqs(self.req, json.dumps(payload),output="json")

        billet_data.update({"bar_code": (data[0])['linha_digitavel']})

        if "type" in qdata:
            payload['tipo_boleto'] = 'arquivo'
            payload['base64'] = 'N'

            path = "/tmp/dataFiles/billets"
            
            data = ixcreqs(self.req, json.dumps(payload), output='file')
            proto = "http"
            #domain = "services.veloo.com.br:{}".format(os.environ.get("PORT"))
            domain = "services.veloo.com.br"
            endpoint = "datafiles"

            builded_file = data2PDF(data, qdata['documentid'], path)

            if builded_file is not False:
                url_billet = "{}://{}/{}/{}".format(proto,domain,endpoint,builded_file)
                billet_data.update({"url_billet": url_billet})
            else:
                billet_data.update({"url_billet": "url_fail"})

        return billet_data

    def unlockContract(self, qdata):
        self.req['endpoint'] = '/desbloqueio_confianca'
        self.req['method'] = "POST"

        payload = {'id': qdata}

        data = ixcreqs(self.req, json.dumps(payload), output="json")

        if data['codigo'] == "200":
            return {"codigo": data['codigo'], "prazo": data['dias'], "msg": data['mensagem']}
        else:
            return {"codigo": data['codigo'], "msg": data['mensagem']}