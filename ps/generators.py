# pip install uszipcode


from uszipcode import ZipcodeSearchEngine

import requests
import datetime
import random
import string
import json


class Generators(object):
    def __init__(self):
        self.locationGenerator = ZipcodeSearchEngine().all()       # Init only once, contains lots of data
        self.session = self.initSession()
        return None
    #
    def initSession(self):
        #Randomize User agent later
        session = requests.Session()
        session.headers['User-Agent'] =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        # print(session.headers)
        return session
    #
    def generateDOB(self):
        getDOB = requests.get("https://uinames.com/api/?ext").json()
        rawDOB = datetime.datetime.fromtimestamp(getDOB["birthday"]["raw"])
        #DOB should be greater than 18 years
        if rawDOB.year > 1995 :
            rawDOB = rawDOB.replace(year=1985)
        dob = rawDOB.strftime('%Y-%m-%d')
        return dob
    #
    def generateName(self):
        getName = requests.get("https://uinames.com/api/?region=united+states").json()
        # print(getName)
        return [getName["name"], getName["surname"]]
    #
    def generateLocationData(self):
        locationData = random.choice(self.locationGenerator)
        # print(locationData)
        return [locationData["State"], locationData["City"], locationData["Zipcode"]]
    #
    def generatePassword(self):
        # "Between 8 and 30 characters in length",
        # "Cannot use repeating characters (e.g. aaa64135, 111bcxjk)",
        # "Cannot contain your sign-in ID or the part of your email address before the \"@\"",
        # "Tips for Stronger Passwords",
        # "Passwords are case sensitive. Use a combination of uppercase and lowercase letters.",
        # "Do not use a word found in the dictionary",
        # "Use a mixture of letters, numbers, and special characters (e.g. h37@f3-2)",
        # "Use supported special characters (e.g. !, @, #, $, &)",
        # "Password cannot contain letters or numbers used three or more times in a row (e.g. 333 or BBB).",
        base_string = string.ascii_lowercase + string.digits + string.ascii_uppercase + "!@#$&"
        password = ""
        i = 0
        while len(password) < random.choice(range(12,20)):
            char = random.choice(base_string)
            # print(char)
            if char.upper() not in password.upper():
                password = password + char
            i += 1
            # print(i)
        # print(password)
        return password
    #
    def generateOnlineId(self):
        #prefix mzplus before each random string
        #minimum 3 letters long
        #the first letter should be a string
        base_string = string.ascii_lowercase + string.digits
        online_id = random.choice(string.ascii_lowercase)
        for i in range(random.choice(range(8,9))):
            online_id = online_id + random.choice(base_string)
        online_id = "mzplus_" + online_id
        if self.verifyOnlineId(online_id):
            return online_id
        else:
            print("Regenerating Online ID")
            return self.generateOnlineId()
    #
    def verifyOnlineId(self, online_id):
        print(online_id)
        onlineIdCheckData = { "onlineId": online_id, "reserveIfAvailable":False }
        onlineIdCheckHeaders = {"Content-Type": "application/json; charset=UTF-8"}
        url = "https://accounts.api.playstation.com/api/v1/accounts/onlineIds"
        check_online_id = self.session.post(url, data=json.dumps(onlineIdCheckData), headers=onlineIdCheckHeaders)
        print(check_online_id)
        print(check_online_id.url)
        # print(check_online_id.history)
        if check_online_id.status_code == 201:
            print("Online Id is available")
            return True
        elif check_online_id.status_code == 400:
            check_online_id_response = check_online_id.json()
            print(check_online_id_response)
            return False
        else:
            print(check_online_id.text)
        return False
    #
    def generate(self):
        # nada_obj = Nada()
        # nada_obj.checkEmails(ONLINE_ID)
        NAME = self.generateName()
        LD = self.generateLocationData()
        data = {
                "FIRST_NAME" : NAME[0],
                "LAST_NAME" : NAME[1],
                "DOB" : self.generateDOB(),
                "ONLINE_ID" : self.generateOnlineId(),
                "PASSWORD" : self.generatePassword(),
                "CITY" : LD[1],
                "POSTAL_CODE" : LD[2],
                "COUNTRY_SUB_DIVISION" : LD[0],
        }
        print(data)
        return data

