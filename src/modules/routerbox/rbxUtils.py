from datetime import datetime as dt


def CompararData(data):
    data = dt.strptime(data, "%Y-%m-%d")
    now = dt.now()

    if data < now:
        return 1
    else:
        return 0


def CalcVTime(data):
    data = dt.strptime(data, "%Y-%m-%d")
    now = dt.now()
    vDT = now - data
    return vDT.days


def RetFortics(docs):
    res = []

    for doc in docs['result']:
        Id = len(res)+1
        vDate = doc['due_date']
        docId = doc['id']
        diffDT = CalcVTime(vDate)

        if diffDT > 0:
            situacao = 'Vencido'
        else:
            situacao = 'A vencer'

        vDate = FormatarDataSaida(vDate)
        res.append({'id': Id, 'code': docId, 'date': vDate, 'diffDT': diffDT, 'situacao': situacao})

    return res


def DocLinkFormater(link):
    link = link['result']['banking_billet_link']
    LFormat = link.replace('\\', '')
    return LFormat


def FormatarDataSaida(dtStr):
    dt = dtStr.split("-")
    dt.reverse()
    nova_data = '/'.join(dt)
    return nova_data
