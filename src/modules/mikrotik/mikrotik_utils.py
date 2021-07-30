def parseSrv(data):

    pdata = data.splitlines()
    pdata = pdata[2:]

    return pdata[0].split()