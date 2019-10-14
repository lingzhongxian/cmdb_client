# coding:utf-8
from lib.log import Logger
import json
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from conf import settings
import requests
import time
import hashlib
from src import plugins
from lib.serialize import Json


class BaseClient(object):
    def __init__(self):
        self.asset_api=settings.ASSET_API
        self.key=settings.KEY
        self.key_name=settings.AUTH_KEY_NAME

    def auth_key(self):
        """
        接口认证
        :return:
        """
        hash=hashlib.md5(self.key.encode("utf-8"))#加盐:在这个基础上再加密
        time_span=time.time()
        hash.update(bytes("%s|%f"%(self.key,time_span),encoding="utf-8"))
        encryption=hash.hexdigest()
        result="%s|%f"%(encryption,time_span)
        #
        return {self.key_name:result}

    def get_asset(self):
        pass

    def post_asset(self,msg,callback=None):
        """
        post方式向接口提交资产信息
        :param msg:
        :param callback:
        :return:
        """
        status=True
        try:
            headers={}
            headers.update(self.auth_key())
            response=requests.post(
                url=self.asset_api,
                headers=headers,
                json=msg
            )
        except Exception as e:
            response=e
            status=False
        if callback:
            callback(status,response)


    def process(self):
        pass

    def callback(self,status,response):
        """
        提交资产后的回调函数
        :param status:
        :param response:
        :return:
        """
        if not status:
            Logger().log(str(response),False)
            return
        ret=json.loads(response.text)
        if ret["code"]==1000:
            Logger().log(ret["message"],True)
        else:
            Logger().log(ret["message"],False)

    def send_data(self,data_dict):
        pass

    def get_host(self):
        pass
    def run(self,hostname):
        pass

class Agent(BaseClient):
    def __init__(self):
        self.cert_file_path=settings.CERT_FILE_PATH
        super(Agent,self).__init__()
    def load_local_cert(self):
        pass
    def write_local_cert(self,cert):
        pass
    def process(self):
        # 采集资产
        # from src.package import pack
        # data_dict = pack
        # hostname=self.file_host()
        # if hostname:
        #     data_dict["hostname"]=hostname
        # else:
        #     #获取当前主机名
        #     #写入nid文件
        #     data_dict["hostname"]="slave1"
        # 将资产数据发送到API(POST)
        # self.send_data(data_dict)
        # 获取指定主机名的资产信息
        # {"status":True,"message":None,"error":None,"data":{"disk":<lib.response.BaseResponse object at 0x0}}
        server_info = plugins.get_server_info()
        if not server_info.status:
            return
        local_cert = self.load_local_cert()
        if local_cert:
            if local_cert == server_info.data["hostname"]:
                pass
            else:
                server_info.data["hostname"] = local_cert
        else:
            self.write_local_cert(server_info.data["hostname"])
        # 序列化成字符串
        server_json = Json.dumps(server_info.data)
        # 发送到API
        self.post_asset(server_json, self.callback)
    def run(self,hostname):
        pass

class SSH(BaseClient):
    def process(self):
        # 采集资产
        from src.package import pack
        data_dict=pack
        # 将资产数据发送到API(POST)
        self.send_data(data_dict)


class Salt(BaseClient):
    def process(self):
        """
        根据主机名获取资产信息，将其发送到API
        :return:
        {
            "data":[{"hostname":"slave1"},{"hostname":"slave2"}],
            "error":null,
            "message":null,
            "status":true
        }
        """
        # # 采集资产
        # from src.package import pack
        # data_dict = pack
        # # 将资产数据发送到API(POST)
        # self.send_data(data_dict)


        task = self.get_asset()
        if not task["task"]:
            Logger().log(task["message"], False)

        # 创建线程池：最大可用线程10
        pool = ThreadPoolExecutor(10)
        for item in task["data"]:
            hostname = item["hostname"]
            pool.submit(self.run, hostname)
        pool.shutdown(wait=True)
    def run(self,hostname):
        # 获取指定主机名的资产信息
        # {"status":True,"message":None,"error":None,"data":{"disk":<lib.response.BaseResponse object at 0x0}}
        server_info = plugins.get_server_info(hostname)
        # 序列化成字符串
        server_json = Json.dumps(server_info.data)
        # 发送到API
        self.post_asset(server_json, self.callback)