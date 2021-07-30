from modules.routerbox.routerbox import Routerbox
from modules.routerbox.routerboxDB import RouterboxBD
from modules.smartolt.smartolt import Smartolt

from flask import request
from flask_restful import Resource
import sys

sys.path.append('../')


class ConsultaCli(Resource):
    def post(self):
        json_dt = request.get_json(force=True)
        token = json_dt['token']
        clipar = json_dt['clipar']
        tipopar = json_dt['tipopar']

        rbx = Routerbox(token)
        cliente = rbx.ConsultaCli(tipopar, clipar)

        if cliente['status'] == 1:

            VencST = rbx.DocAbertos(cliente['Codigo'])

            docs = {}

            cnt_docs = len(VencST)

            docs['count'] = cnt_docs
            docs['count_venc'] = 0

            if cnt_docs != 0:
                docinfo = []
                for doc in VencST:
                    if doc['diffDT'] > 0:
                        docs['count_venc'] += 1

                    docinfo.append(doc)
                docs['docinfo'] = docinfo
            cliente['documentos'] = docs

            rbxdb = RouterboxBD('172.31.254.41', 'squid', '***root*fistel@kaua2020dbrbx')
            atendimentos = rbxdb.AtendimentoCliAberto(cliente['Codigo'])
            contratos = rbxdb.ConsultaContrato(cliente['Codigo'])
            contIDs = list(contratos.keys())[1:]

            cliente['contratos'] = contratos
            cliente['atendimentos'] = atendimentos

        return cliente


class DesbloqueioConfia(Resource):
    def post(self):
        json_dt = request.get_json(force=True)

        token = json_dt['token']
        cliid = json_dt['cliid']
        docid = json_dt['docid']
        contid = json_dt['contid']
        infodate = json_dt['infodate']

        rbx = Routerbox(token)
        rbxdb = RouterboxBD('172.31.254.41', 'squid', '***root*fistel@kaua2020dbrbx')

        cpDate = infodate.split('/')
        cpDate.reverse()
        cpDate = '-'.join(cpDate)

        pgdt = "Data de Pagamento: %s" % infodate

        infopag = rbx.InfoPag(cliid, cpDate, docid)

        tickets = rbxdb.AtendimentoCliAberto(cliid)
        ticketid = 0

        for tck in tickets:
            if tck != 'count':
                ticket = tickets[tck]
                if ticket['Assunto'].find(pgdt) != -1:
                    ticketid = int(ticket['Numero'])

        if infopag == 1:
            desbloqueio_st = rbx.DesbCont(cliid, contid)

            if desbloqueio_st == 1:
                msg = "Desbloqueio em confia realizado com sucesso."

            else:
                msg = "Infelizmente não foi possível efetivar o desbloqueio."

        else:
            msg = "Infelizmente não foi possível efetivar o informe de pagamento."

        return {'infopag_st': infopag, "ticketid": ticketid}


class AbreAtendimento(Resource):
    def post(self):
        json_dt = request.get_json(force=True)
        token = json_dt['token']
        clientID = int(json_dt['cliid'])
        assunto = json_dt['assunto']
        ocorrencia = json_dt['ocorrencia']

        if 'fluxoid' in json_dt:
            par = ['f', int(json_dt['fluxoid'])]

        if 'topicid' in json_dt:
            tipo = json_dt['tipo']
            par = ['t', int(json_dt['topicid']), tipo]

        rbx = Routerbox(token)
        ticketID = rbx.CriaAtenFluxo(clientID, par, assunto, ocorrencia)
        if ticketID == 0:
            return 0
        else:
            return {'Protocolo': ticketID, 'Assunto': assunto, 'Comentario': ocorrencia}


class IncluiOcorrencia(Resource):
    def post(self):
        json_dt = request.get_json(force=True)
        token = json_dt['token']
        ticketID = json_dt['ticketid']
        msg = json_dt['msg']

        rbx = Routerbox(token)
        ocurID = rbx.IncluiOcorrencia(ticketID, msg)

        return ocurID


class DocLinkPdf(Resource):
    def post(self):
        document = {}
        json_dt = request.get_json(force=True)
        token = json_dt['token']
        docid = int(json_dt['docid'])

        rbx = Routerbox(token)
        document["url"] = rbx.DocLinkPdf(docid)
        document["barcode"] = rbx.DocBarCode(docid)

        return document


class CriaCliMercado(Resource):
    def post(self):
        json_dt = request.get_json(force=True)
        token = json_dt['token']
        cpf = json_dt['cpf']
        endereco = json_dt['endereco']
        bairro = json_dt['bairro']
        telefone = json_dt['telefone']
        cep = json_dt['cep']
        nome = json_dt['nome']

        rbx = Routerbox(token)
        retDT = rbx.CriaCliMercado(cpf, endereco, bairro, cep, telefone, nome)

        return retDT
