import requests
import json


class RequestsManager(object):
    def __init__(self):
        self.session = self.initSession()
        self.baseHeaders = {
                    "Connection": "keep-alive",
                    "Origin": "https://id.sonyentertainmentnetwork.com",
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9"
                    }
        return None
    #
    def initSession(self):
        #Randomize User agent later
        session = requests.Session()
        session.headers['User-Agent'] =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        # print(session.headers)
        return session
    #
    def makeRequest(self, url, method="POST", headers=None, data=None):
        if method == "POST":
            if headers:
                ct0 = headers.get("Content-Type")
                ct1 = headers.get("content-type")
                if ct0:
                    if ("application/json" in ct0):
                        print("Converting DATA to JSON")
                        data = json.dumps(data)
                elif ct1:
                    if ("application/json" in ct1):
                        print("Converting DATA to JSON")
                        data = json.dumps(data)
            req = self.session.post(url, headers=headers, data=data)
        elif method == "GET":
            req = self.session.get(url, headers=headers)
        elif method == "OPTIONS":
            req = self.session.options(url, headers=headers)
        print(req)
        # print(req.url)
        # print(req.history)
        if req.status_code == 400:
            print("error\n\n")
            print(req.text.encode())
        return req
    #
    def headersOne(self):
        #These headers are used for normal post requests
        #POST data type JSON
        #Host is accounts.api.playstation.com
        headers = self.baseHeaders.copy()
        headers["Host"] = "accounts.api.playstation.com"
        headers["Content-Type"] = "application/json; charset=UTF-8"
        return headers
    #
    def headersTwo(self):
        #These headers are used for login post requests
        #POST data is application/x-www-form-urlencoded
        #Host is auth.api.sonyentertainmentnetwork.com
        headers = self.baseHeaders.copy()
        headers["Host"] = "auth.api.sonyentertainmentnetwork.com"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        return headers
