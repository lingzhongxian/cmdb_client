#coding:utf-8
class BaseResponse:
    def __init__(self):
        self.status=None
        self.message=None
        self.data=None
        self.error=None