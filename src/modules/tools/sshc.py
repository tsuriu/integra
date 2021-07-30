from paramiko import client

class ssh:
    client = None

    def __init__(self, host, user, passwd):
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(host,username=user,password=passwd,look_for_keys=False)

    def execute(self, cmd):
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(cmd)
            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(4096)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(4096)
                        alldata += prevdata
                        
                        return str(alldata,"utf8")
        else:
            return "Error SendCommand"

    def getFile(self,rmtfl,lcfl):
        if(self.client):
            sftp = self.client.open_sftp()
            sftp.get(rmtfl,lcfl)