import pymysql


class RouterboxBD(object):
    def __init__(self, host, user, pswd):
        self.host = host
        self.user = user
        self.pswd = pswd

        self.rbxdb = pymysql.connect(host=self.host, port=3306, user=self.user, passwd=self.pswd, db='isupergaus', cursorclass=pymysql.cursors.DictCursor)

        self.cur = self.rbxdb.cursor()

    def __del__(self):
        self.rbxdb.close()

    def AtendimentoCliAberto(self, cliid):
        AtRet = {}

        qry = "SELECT Numero,Assunto,Prioridade,TipoCli,Contrato,unix_timestamp(Data_AB) as Data_AB,unix_timestamp(Hora_AB) as Hora_AB,unix_timestamp(Data_ATU) as Data_ATU,Fluxo,Topico,Situacao FROM Atendimentos WHERE Situacao != 'F' AND Cliente = '{}';".format(cliid)

        self.cur.execute(qry)
        atendimentos = self.cur.fetchall()

        AtRet['count'] = len(atendimentos)

        for at in atendimentos:
            AtRet[at['Numero']] = at

        return AtRet

    def ClientePlanRefs(self, contid):
        plandata = {}
        qry = "SELECT Planos.Descricao AS descricao, Planos.Velocidade AS down, Planos.VelocidadeUP AS up FROM Clientes, Contratos, Planos  WHERE Clientes.Codigo = Contratos.Cliente AND Contratos.Plano = Planos.Codigo AND Clientes.Situacao REGEXP 'B|A' AND Contratos.Numero = {}".format(contid)

        self.cur.execute(qry)
        data = self.cur.fetchall()

        for dt in data:
            plandata = dt

        return plandata

    def ConsultaContrato(self, cliid):
        Contratos = {}

        qry = "SELECT Numero,Situacao FROM Contratos WHERE Situacao REGEXP 'B|A|I' AND Cliente = '{}';".format(cliid)

        self.cur.execute(qry)
        contratos = self.cur.fetchall()

        Contratos['count'] = len(contratos)
        continfo = []

        for cont in contratos:
            cont['Plano'] = self.ClientePlanRefs(cont['Numero'])
            continfo.append(cont)

        Contratos['continfo'] = continfo

        return Contratos

    def ConsultaContatos(self, cliid):

        return 0

    def ClientePPPoE(self, cliid, contid):

        qry = "select Usuario from ClientesUsuarios where MAC != ''  and Cliente={} and Contrato={};".format(cliid, contid)

        self.cur.execute(qry)
        ppp_user = self.cur.fetchone()

        return ppp_user

    def ClienteAuthData(self, ppp_user):
        userdata = {}
        qry = "select cliente as cliid,username,acctsessiontime,nasipaddress as nas,framedprotocol as proto,framedipaddress as ip,framedipv6address as ipv6 from radacct where username='{}';".format(ppp_user)

        self.cur.execute(qry)
        data = self.cur.fetchall()

        for dt in data:
            userdata['auth_data'] = dt

        return userdata
