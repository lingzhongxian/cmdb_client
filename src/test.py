# encoding: utf-8
#继承关系：self先执行子类，后执行父类
# class Bbh:
#     def server(self):
#         self.sz()
#         print("super server")
#     def sz(self):
#         # self.xiaowen()
#         print("super sz")
#
# class Mr(Bbh):
#     def sz(self):
#         print("sz")
#     # def server(self):
#     #     print("server")
#     def xiaowen(self):
#         # self.process_request()
#         print()
#
# class Yun:
#     def process_request(self):
#         print("yun")
#
# class Zzc(Yun,Mr):
#     pass
# obj=Zzc()
# obj.server()

# def funA(arg):
#     print("A")
#     arg()
#
# @funA
# def funB():
#     print("B")


# def hello(self,func):
#     self.name="Sam"
#     a=func
#     def greet():
#         return "Greet"
#     def welcome():
#         return "Welcome"
#     if self.name=="Sam":
#         return greet
#     else:
#         return welcome
# #
# # # @hello
# def var(self,name):
#     self.name=name
# #
# print(hello(var(name="Sam")))

# from concurrent.futures import ThreadPoolExecutor
# from concurrent.futures import ProcessPoolExecutor
# import time
#
# def task(arg):
#     print(arg)
#     time.sleep(1)
#
# pool=ThreadPoolExecutor(5)
#
# for i in range(1,51):
#     pool.submit(task,i)

import requests
host_data={
    "status":True,
    "data":{
    "hostname":"slave1",
    "disk":{"status":True,"data":""},
    "mem":{"status":True,"data":""},
    "nic":{"status":True,"data":""},
    "cpu":{"status":True,"data":""},
    "main_board":{"status":True,"data":""},
    },
}

response=requests.post(
    url="http://127.0.0.1:8000/asset/",
    json=host_data,
    headers={"authkey":"8kasoimnasodn8687asdfkmasdf"},
)
print(response.text)

# requests.get(url="http://127.0.0.1:8000/api/asset/?k1=123")
# requests.get(url="http://127.0.0.1:8000/api/asset/",params={"k1":"v1","k2":"v2"})