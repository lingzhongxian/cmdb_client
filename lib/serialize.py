# coding:utf-8
import json
from datetime import datetime
from datetime import date
from json.encoder import JSONEncoder
from .response import BaseResponse

# class JsonEncoder(JSONEncoder):
#     def default(self,o):
#         if isinstance(o,BaseResponse):
#             return o.__dict__
#         return JSONEncoder.default(self,o)
#
# class Json(object):
#
#     @staticmethod
#     def dumps(response,ensure_ascii=True):
#         return default_json.dumps(response,ensure_ascii=ensure_ascii,cls=JsonEncoder)

class Json(json.JSONEncoder):
    def dumps(self,field):
        if isinstance(field,datetime):
            return field.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(field,date):
            return field.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self,field)
class Response(object):
    def __init__(self):
        self.status=True
        self.data="fssd"
data={
    "k1":123,
    "k2":datetime.now(),
    "k3":Response()
}
ds=json.dumps(data,cls=Json)
print(ds)