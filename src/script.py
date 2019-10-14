# encoding: utf-8
#采集资产：三种不同的形式
from .plugins.base import BasePlugin

from conf import settings
from src import client


# obj=DiskPlugin()
# result=obj.execute()

# obj=BasePlugin()
# obj.execute()


def run():
    if settings.MODE == 'Agent':
        client.Agent().process()
    elif settings.MODE == 'SSH':
        client.SSH().process()
    elif settings.MODE == 'Salt':
        client.Salt().process()
    else:
        raise Exception('请配置资产采集模式，如：Agent、SSH、salt')
