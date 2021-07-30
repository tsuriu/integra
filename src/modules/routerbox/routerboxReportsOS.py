from .odbc_mysql import mysqldb
from decimal import Decimal


class RouterboxBDReports(object):
    def __init__(self):
        self.host = "172.31.254.41"
        self.user = "squid"
        self.passwd = "***root*fistel@kaua2020dbrbx"
        self.schema = "isupergaus"

        self.rbxdb = mysqldb(self.host, self.user, self.passwd, self.schema)

    def repOS(self, groupid):
        result = {}

        qry_nocap = "SELECT Numero, Cliente, Usu_Abertura, Usu_Designado, Grupo_Designado, Fluxo, Topico, TRUNCATE(UNIX_TIMESTAMP(CONCAT(Data_AB, ' ',Hora_AB)),0) as Abertura, TRUNCATE(UNIX_TIMESTAMP(CONCAT(Data_BX, ' ',Hora_BX)),0) as BX, TRUNCATE(UNIX_TIMESTAMP(CONCAT(Data_Prox, ' ',Hora_Prox)),0) as Prox, UNIX_TIMESTAMP(Data_ATU) as ATU, UNIX_TIMESTAMP(SLAInicio) as SLAInicio, SLA, SLATipo, Duracao, Situacao, (select Foto from usuarios where usuario=Usu_Abertura) as FotoAbert, (select Foto from usuarios where usuario=Usu_Designado) as FotoDesig from Atendimentos where Situacao = 'A' and Grupo_Designado = {} ORDER BY Numero ASC;".format(groupid)
        qry_cap = "SELECT Numero, Cliente, Usu_Abertura, Usu_Designado, Grupo_Designado, Fluxo, Topico, TRUNCATE(UNIX_TIMESTAMP(CONCAT(Data_AB, ' ',Hora_AB)),0) as Abertura, TRUNCATE(UNIX_TIMESTAMP(CONCAT(Data_BX, ' ',Hora_BX)),0) as BX, TRUNCATE(UNIX_TIMESTAMP(CONCAT(Data_Prox, ' ',Hora_Prox)),0) as Prox, UNIX_TIMESTAMP(Data_ATU) as ATU, UNIX_TIMESTAMP(SLAInicio) as SLAInicio, SLA, SLATipo, Duracao, Situacao, (select Foto from usuarios where usuario=Usu_Abertura) as FotoAbert, (select Foto from usuarios where usuario=Usu_Designado) as FotoDesig from Atendimentos where Situacao != 'F' and Usu_Designado in (select usuario from usuarios where idgrupo={}) ORDER BY Numero ASC;".format(groupid)

        osNocap = self.rbxdb.fetchAll(qry_nocap)
        osCap = self.rbxdb.fetchAll(qry_cap)

        for data in [osNocap, osCap]:
            for dta in data['data']:
                for dt in list(dta.keys()):
                    if isinstance(dta[dt], Decimal):
                        dta[dt] = int(dta[dt])

        result['nocap'] = osNocap
        result['cap'] = osCap

        return result


if __name__ == '__main__':
    rbx = RouterboxBDReports()
    os = rbx.repOS(11)
