# encoding: utf-8
from src.plugins.base import BasePlugin
from src.plugins.basic import BasicPlugin
from src.plugins.disk import DiskPlugin
from src.plugins.mem import MemoryPlugin
from src.plugins.nic import NicPlugin
from src.plugins.main_board import MainBoardPlugin
from conf import settings

def pack():
    # response={
    #     "disk":disk_info,
    #     "men":men_info,
    #     "nic":nic_info
    # }
    response={}
    for k,v in settings.PLUGINS.items():
        import importlib
        m_path,classname=v.rsplit(".",maxsplit=1)
        m=importlib.import_module(m_path)
        cls=getattr(m,classname)

        # 反射
        response[k]=cls().execute()
    return response

