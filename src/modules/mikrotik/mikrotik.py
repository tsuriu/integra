from ..tools.sshc import ssh
from .mikrotik_utils import *

class mkt:

    def __init__(self, host, usr, passwd):
        self.host = host
        self.usr = usr 
        self.passwd = passwd 
        self.session = ssh(self.host, self.usr, self.passwd)

    def onlinePPP(self, inf):
        s = self.session

        gOnCountCmd = '/interface pppoe-server print count-only where service="{}"'
        gServiceCmd = '/interface pppoe-server server print brief where interface="{}"'

        pppService = parseSrv(s.execute(gServiceCmd.format(inf)))
        pppOnCount = s.execute(gOnCountCmd.format(pppService[1]))

        return int(pppOnCount.rstrip())