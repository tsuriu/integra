from requests import sessions
from rocketchat_API.rocketchat import RocketChat
import os

class RChat(object):
    """ 
    rocketchat
    """

    rc_url = os.environ.get("RC_URL")
    rc_username = os.environ.get("RC_USERNAME")
    rc_password = os.environ.get("RC_PASSWORD")

    def __init__(self):
        self.rc = RocketChat(self.rc_username, self.rc_password, server_url=self.rc_url, ssl_verify=False)

    def availability(self):
        res = self.rc.info.json()
        return res['success']

    def stats(self):
        res = self.rc.statistics().json()

        data = {}

        rc_stat_keys = ['version','totalUsers','activeUsers','activeGuests',
                        'nonActiveUsers','onlineUsers','awayUsers','busyUsers',
                        'totalConnectedUsers','offlineUsers','totalThreads',
                        'livechatEnabled','totalChannelMessages','totalPrivateGroupMessages',
                        'totalDirectMessages','totalMessages','totalLivechatMessages',
                        'instanceCount','oplogEnabled','mongoVersion','mongoStorageEngine',
                        'pushQueue','enterpriseReady','uploadsTotal','uploadsTotalSize',
                        'process']

        rc_stat_os_keys = ['uptime', 'totalmem', 'freemem']

        if 'success' in list(res.keys()):
            os_data = {}
            for key in rc_stat_keys:
                data[key] = res[key]
            
            for oskey in rc_stat_os_keys:
                os_data[oskey] = res['os'][oskey]
            
            data['os'] = os_data
            
        else:
            data = res
        
        return data