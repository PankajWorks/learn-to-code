import urllib2 , hmac , base64
from hashlib import sha1
import hmac , requests
import json

class RestClient:
    User_Agent = 'ubuntu'
    host = ''
    Content_Type = 'Aplication/json'
    resourse = ''
    Date = ''
    headers = {}
    data = []
    status_code = ''
    url = ''
    text = ''
    responce = None
    username = ''
    password = ''

    def put_header(self,key,value):
        self.headers[key]=value


    def get(self,append_url='',params={},is_auth=False):
	    if is_auth:
        	self.responce = requests.get(self.host+self.resourse+append_url,headers=self.headers,params=params,auth=(self.username,self.password))
	    else:
        	self.responce = requests.get(self.host+self.resourse+append_url,headers=self.headers,params=params)

    def post(self,params={},append_url='',is_auth=False):
	    if is_auth:
        	self.responce = requests.post(self.host+self.resourse+append_url,data=params,headers=self.headers,auth=(self.username,self.password))
	    else:
        	self.responce = requests.post(self.host+self.resourse+append_url,data=params,headers=self.headers)


    def put(self,params={},append_url='',is_auth=False):
	    if is_auth:
        	self.responce = requests.put(self.host+self.resourse+append_url,data=params,headers=self.headers,auth=(self.username,self.password))
	    else:
        	self.responce = requests.put(self.host+self.resourse+append_url,data=params,headers=self.headers)



    def delete(self,append_url='',params={},is_auth=False):
	    if is_auth:
        	self.responce = requests.delete(self.host+self.resourse+append_url,params=params,headers=self.headers,auth=(self.username,self.password))
	    else:
        	self.responce = requests.delete(self.host+self.resourse+append_url,params=params,headers=self.headers)
