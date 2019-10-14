# encoding: utf-8
from lib.log import Logger
from conf import settings
class BasePlugin(object):
    def __init__(self,hostname=""):
        self.logger=Logger()
        self.mode_list=["Agent","SSH","Salt"]
        # if settings.MODE in mode_list:
        if hasattr(settings,"MODE"):
            self.mode=settings.MODE
        else:
            self.mode="Agent" #设置默认方式为：Agent
            # raise Exception("配置文件错误！")
        self.hostname=hostname
    def agent(self,cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def ssh(self,cmd):
        import paramiko
        private_key = paramiko.RSAKey.from_private_key_file(settings.SSH_PRIVATE_KEY)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=settings.SSH_PORT, username=settings.SSH_USER, pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result

    def salt(self,cmd):
        from salt import client
        local = client.LocalClient()
        result = local.cmd(self.hostname, 'cmd.run', [cmd])
        return result[self.hostname]

    def shell_cmd(self,cmd):
        if self.mode=="Agent":
            ret=self.agent(cmd)
        elif self.mode=="SSH":
            ret=self.ssh(cmd)
        else:
            ret=self.salt(cmd)
        return ret

    def exec_shell_cmd(self,cmd):
        if self.mode not in self.mode_list:
            raise Exception("settings.mode must be one of ['Agent', 'Salt', 'SSH']")
        func = getattr(self, self.mode)
        output = func(cmd)
        return output


    def execute(self):
        self.linux()
    def linux(self):
        raise Exception("..............")