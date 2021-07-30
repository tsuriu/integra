import json
import re
from datetime import date, datetime

import requests

from .rbxUtils import DocLinkFormater, RetFortics


class Routerbox:

    root_url = "https://rbx.squidtelecom.com.br"

    def __init__(self, token):
        self.token = token
        self.headers = {
            'content-type': "application/json",
            'authentication_key': self.token
            }

    def ConsultaCli(self, tipo, data):
        endpoint = "/routerbox/ws/rbx_server_json.php"
        url = self.root_url+endpoint

        parametro = ""

        if tipo == "cnpj_cnpf":
            data = ''.join(re.findall('\d+', data))
            parametro = "CNPJ_CNPF='{}'".format(data)
        if tipo == "cod":
            parametro = "Codigo='{}'".format(data)

        payload = {
            "ConsultaClientes": {
                "Autenticacao": {
                    "ChaveIntegracao": self.token
                },
                "Filtro": parametro
            }
        }

        result = requests.post(url, data=json.dumps(payload))
        result = result.json()

        clientDT = {}

        if result['status'] != 1:
            clientDT['status'] = 0
        else:
            result = (result['result'])[0]

            keys = ["Codigo", "Tipo", "CNPJ_CNPF", "Nome", "Grupo", "Situacao"]
            clientDT['status'] = 1

            for key in keys:
                clientDT[key] = result[key]

            addrKeys = ["Endereco", "Numero", "Complemento", "Bairro", "Cidade"]

            endereco = {}

            for addK in addrKeys:
                endereco[addK] = result[addK]

            clientDT['endereco'] = endereco

        return clientDT

    def ContratoBloq(self, cliid):
        endpoint = "/routerbox/ws/rbx_server_json.php"
        url = self.root_url+endpoint
        payload = {
            "ConsultaContratosBloqueados": {
                "Autenticacao": {
                    "ChaveIntegracao": self.token
                }
            }
        }

        result = requests.post(url, data=json.dumps(payload))
        result = (result.json())['result']

        contIDs = []
        for cont in result:
            cli = cont['Cliente_Codigo']
            if cliid == int(cli):
                contIDs.append(cont['Contrato_Numero'])
        return contIDs

    def DocAbertos(self, clientID):
        endpoint = "/routerbox/ws_json/ws_json.php"
        url = self.root_url+endpoint
        payload = {
            "get_unpaid_document":
            {
                "customer_id": int(clientID),
                "account_number": 3
            }
        }

        result = requests.post(url, headers=self.headers, data=json.dumps(payload))
        docs = result.json()
        docs = RetFortics(docs)

        if len(docs) > 0:
            res = docs[:3]
        else:
            res = []

        return res

    def DocLinkPdf(self, docid):
        endpoint = "/routerbox/ws_json/ws_json.php"
        url = self.root_url+endpoint

        payload = {
            "get_banking_billet":
            {
                "document_id": docid
            }
        }

        result = requests.post(url, headers=self.headers, data=json.dumps(payload))
        link = DocLinkFormater(result.json())

        if (result.json())['status'] == 1:
            res = link
        else:
            res = 0

        return res

    def DocBarCode(self, docid):
        endpoint = "/routerbox/ws_json/ws_json.php"
        url = self.root_url+endpoint

        payload = {
            "get_barcode":
            {
                "banking_billet_id": int(docid),
                "send_barcode": False
            }
        }

        result = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if (result.json())['status'] == 1:
            res = (result.json())['result']
            res = re.sub('[^A-Za-z0-9]+', '', res)
        else:
            res = 0

        return res

    def InfoPag(self, clientID, infoDate, docID):
        endpoint = "/routerbox/ws_json/ws_json.php"
        url = self.root_url+endpoint

        payload = {
            "send_payment_notification":
            {
                "document_id": docID,
                "payment_date": infoDate,
                "customer_id": clientID
            }
        }

        result = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return (result.json())['status']


    def DesbCont(self, clientID, contratoID):
        endpoint = "/routerbox/ws_json/ws_json.php"
        url = self.root_url+endpoint
        payload = {
            "contract_unblock":
            {
                "customer_id": int(clientID),
                "contract_id": int(contratoID)
            }
        }
        result = requests.post(url, headers=self.headers, data=json.dumps(payload))
        result = result.json()

        status = result['status']
        return status


    def CriaAtenFluxo(self, clientID, par, assunto, comment=None):
        endpoint = "/routerbox/ws/rbx_server_json.php"
        url = self.root_url+endpoint

        data = (date.today()).strftime("%Y-%m-%d")
        hora = (datetime.now()).strftime("%H:%M:%S")

        payload = {
            "AtendimentoCadastro": {
                "Autenticacao": {
                    "ChaveIntegracao": self.token
                },
                "DadosAtendimento": {
                    "Data_Abertura": data,
                    "Hora_Abertura": hora,
                    "Iniciativa": "C",
                    "Modo": "C",
                    "TipoCliente": "C",
                    "Cliente": clientID,
                    "Assunto": assunto
                }
            }
        }

        if par[0] == 'f':
            payload['AtendimentoCadastro']['DadosAtendimento']['Fluxo'] = par[1]
        if par[0] == 't':
            payload['AtendimentoCadastro']['DadosAtendimento']['Topico'] = par[1]
            payload['AtendimentoCadastro']['DadosAtendimento']['Tipo'] = par[2]
        if comment is not None:
            payload['AtendimentoCadastro']['DadosAtendimento']['Ocorrencia'] = comment

        result = requests.post(url, data=json.dumps(payload))
        result = result.json()

        if result['status'] == 1:
            return result['result']['NumeroAtendimento']
        else:
            return 0

    def CriaCliMercado(self, cpf, endereco, bairro, cep, telefone, nome):
        endpoint = "/routerbox/ws/rbx_server_json.php"
        url = self.root_url+endpoint

        payload = {
            "MercadoCadastro": {
                    "Autenticacao": {
                        "ChaveIntegracao": self.token
                    },
                "DadosMercado": {
                    "CPF": ''.join(re.findall('\d+', cpf)),
                    "TipoPessoa": "F",
                    "Endereco": endereco,
                    "Bairro": bairro,
                    "TelCelular": telefone,
                    "CEP": cep,
                    "Nome": nome,
                    "CodMunicipio": 2707701,
                    "UF": "AL",
                    "TipoConta": "POS"
                    }
                }
            }

        result = requests.post(url, data=json.dumps(payload))
        return result.json()

    def IncluiOcorrencia(self, atendID, msg):
        endpoint = "/routerbox/ws_json/ws_json.php"
        url = self.root_url+endpoint
        payload = {
            "ticket_occurrence_insert":
            {
                "ticket_id": int(atendID),
                "description": str(msg)
            }
        }

        print("comment", payload)

        result = requests.post(url, headers=self.headers, data=json.dumps(payload))

        return result.json()

    def EncerrarAtendimento(self, atendID, causeID, solucao, user):
        endpoint = "/routerbox/ws/rbx_server_json.php"
        url = self.root_url+endpoint
        payload = {
            "ticket_finish":
            {
                "ticket_id": atendID,
                "cause_id": causeID,
                "solution": solucao,
                "user": user
                }
            }

        result = requests.post(url, data=json.dumps(payload))
        result = result.json()

        return result
