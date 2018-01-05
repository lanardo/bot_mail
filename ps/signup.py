import requests
import json

from bs4 import BeautifulSoup as bs

from ps.captchaSolver import solveCaptcha
from ps.requestsManager import RequestsManager



class SignUp(RequestsManager):
    def __init__(self):
        RequestsManager.__init__(self)
        # self.session = self.initSession()
        self.loginUrl = ""
        self.signupUrl = ""
        # self.apiEndPoint = "https://accounts.api.playstation.com/api/v1/accounts/"
        self.apiEndPoint = "https://accounts.api.playstation.com/api/v1/"
        self.authApiUrl = "https://auth.api.sonyentertainmentnetwork.com/2.0/"
        # self.baseHeaders = {
        #                     "Connection": "keep-alive",
        #                     "Origin": "https://id.sonyentertainmentnetwork.com",
        #                     "Accept": "*/*",
        #                     "Accept-Encoding": "gzip, deflate, br",
        #                     "Accept-Language": "en-US,en;q=0.9"
        #                     }
        return None
    #
    def slaveClientId(self):
        url = "https://store.playstation.com/en-us/product/IP9101-NPIA90005_01-PSPLUS14DAYTRIAL"
        clientIdReq = self.makeRequest(url=url, method="GET")
        s1 = bs(clientIdReq.content, "html.parser")
        v1 = s1.find(id = "shoebox-config")
        v2 = json.loads(v1.text)
        clientId =  v2['overrides'][0]['auth']['authCode']['clientId']
        print(clientId)
        self.loginUrl = "https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/authorize?response_type=code&redirect_uri=https://store.playstation.com/en-us/product/IP9101-NPIA90005_01-PSPLUS14DAYTRIAL&request_locale=en_US&client_id={}&scope=kamaji:commerce_native,kamaji:commerce_container,kamaji:lists&prompt=login&state=returning&service_entity=urn:service-entity:psn&hidePageElements=SENLogo&disableLinks=SENLink&ui=pr".format(clientId)
        self.signupUrl = "https://id.sonyentertainmentnetwork.com/create_account/?entry=/create_account&tp_psn=true&state=returning&disableLinks=SENLink&ui=pr&client_id={}&hidePageElements=SENLogo&prompt=login&redirect_uri=https://store.playstation.com/en-us/product/IP9101-NPIA90005_01-PSPLUS14DAYTRIAL&request_locale=en_US&response_type=code&scope=kamaji:commerce_native,kamaji:commerce_container,kamaji:lists&service_entity=urn:service-entity:psn".format(clientId)
        return clientId
    #
    def checkPassword(self, PASSWORD):
        passwordData = { "password" : PASSWORD }
        passwordHeaders = self.headersOne()
        url = self.apiEndPoint + "accounts/passwords/"
        checkPasswordReq = self.makeRequest(url=url, headers=passwordHeaders, data=passwordData)
        if checkPasswordReq.status_code == 200:
            return True
        return False
    #
    def reserveOnlineId(self, ONLINE_ID):
        onlineIdsData = { "onlineId": ONLINE_ID, "reserveIfAvailable":True }
        onlineIdsHeaders = self.headersOne()
        url = self.apiEndPoint + "accounts/onlineIds/"
        onlineIdReq = self.makeRequest(url=url, headers=onlineIdsHeaders, data=onlineIdsData)
        if onlineIdReq.status_code == 201:      #201 = Created
            reservationId = onlineIdReq.json()["reservationId"]
            return reservationId
        return None
    #
    def loginThroughCaptcha(self, EMAIL, reCaptchaResponse):
        loginData = {
                        "grant_type" : "captcha",
                        "captcha_provider" : "google:recaptcha-v2",
                        "scope" : "user:account.create user:account.loginId.validate oauth:authenticate",
                        "valid_for" : EMAIL,
                        "client_id" : "7e309afa-8d09-40d2-8e24-5029642f2c3c",
                        "client_secret" : "8aCv07DXTHJ1T2nA",
                        "response_token" : reCaptchaResponse,
                    }
        loginHeaders = self.headersTwo()
        oauthUrl = self.authApiUrl + "oauth/token"
        loginReq = self.makeRequest(url=oauthUrl, headers=loginHeaders, data=loginData)
        if loginReq.status_code == 200:
            accessToken = loginReq.json()["access_token"]
            return accessToken     #Use for authoriztion , Bearer
        else:
            print(loginReq.text)
            print(loginReq.headers)
        return None
    #
    def loginId(self, accessToken, EMAIL):
        loginIdHeaders = self.headersOne()
        loginIdHeaders["Authorization"] = "Bearer " + accessToken
        url = self.apiEndPoint + "accounts/loginIds/" + EMAIL
        loginIdReq = self.makeRequest(url=url, method="GET", headers=loginIdHeaders)
        if loginIdReq.status_code == 204:
            print("Success")
            return True
        return None
    #
    def userDetails(self, accessToken, userDetailsData):
        #PASS userDetailsData
        userDetailsHeader = self.headersOne()
        userDetailsHeader["Authorization"] = "Bearer " + accessToken
        userDetailsHeader["X-ServiceEntity"] = "urn:service-entity:psn"
        url = self.apiEndPoint + "s2s/accounts/"
        loginIdReq = self.makeRequest(url=url, headers=userDetailsHeader, data=userDetailsData)
        if loginIdReq == 201:
            #Returns
            # {"uri":"/api/v1/s2s/accounts/02a29cbc-38f2-43df-8576-c9decd119456","accountId":"1252013032702886792"}
            return loginIdReq.json()
        return None
    #
    def getSsoCookie(self, accessToken, EMAIL, PASSWORD):
        ssoCookieData = {
                            "authentication_type":"password",
                            "username": EMAIL,
                            "password": PASSWORD,
                            "client_id":"7e309afa-8d09-40d2-8e24-5029642f2c3c"
                        }

        ssoCookieHeaders = self.headersTwo()
        ssoCookieHeaders["Content-Type"] = "application/json; charset=UTF-8"
        ssoCookieHeaders["Authorization"] = "Bearer " + accessToken
        url = self.authApiUrl + "ssocookie"
        ssoCookieReq = self.makeRequest(url=url, headers=ssoCookieHeaders, data=ssoCookieData)
        if ssoCookieReq.status_code == 200:
            npssoCookie = ssoCookieReq.json()
            print(npssoCookie)
            return npssoCookie
        return None
    #
    def loginThroughSsoCookie(self):
        loginDataSSO = {
            "grant_type" : "sso_cookie",
            "scope" : "user:account.email.create user:account.emailVerification.get kamaji:get_account_hash user:account.phone.create user:account.phone.main.update user:account.phone.masked.get user:account.notification.create",
            "client_id" : "7e309afa-8d09-40d2-8e24-5029642f2c3c",
            "client_secret" : "8aCv07DXTHJ1T2nA",
        }
        loginHeadersSSO = self.headersTwo()
        oauthUrl = self.authApiUrl + "oauth/token"
        loginSsoReq = self.makeRequest(url=oauthUrl, headers=loginHeadersSSO, data=loginDataSSO)
        if loginSsoReq.status_code == 200:
            newAccessToken = loginSsoReq.json()["access_token"]
            return newAccessToken     #Use for authorization , Bearer
        return None
    #
    def commerceApi(self, newAccessToken):
        commerceHeaders = self.headersOne()
        commerceHeaders["Host"] = "commerce.api.np.km.playstation.net"
        commerceHeaders["Authorization"] = "Bearer " + newAccessToken
        url = "https://commerce.api.np.km.playstation.net/commerce/api/v1/users/me/account/id"
        commerceApiReq = self.makeRequest(url=url, headers=commerceHeaders, method="GET")
        if commerceApiReq.status_code == 200 :
            print("account id")
            accountId = commerceApiReq.json()
            print(accountId)
            return accountId
        return None
    #
    def regcam(self, newAccessToken):
        regcamHeaders = self.headersOne()
        regcamHeaders["Host"] = "regcam.api.np.km.playstation.net"
        regcamHeaders["Authorization"] = "Bearer " + newAccessToken
        url = "https://regcam.api.np.km.playstation.net/regcam/api/v1/pdr/users/me/profile"
        regcamReq = self.makeRequest(url=url, headers=regcamHeaders, method="GET")
        return None
    #
    def checkEmailStatus(self, newAccessToken):
        #Verified/Unverified
        emailStatusHeaders = self.headersOne()
        emailStatusHeaders["Authorization"] = "Bearer " + newAccessToken
        url = self.apiEndPoint + "accounts/me/emailVerification/"
        emailStatusReq = self.makeRequest(url=url, headers=emailStatusHeaders, method="GET")
        if emailStatusReq.status_code == 200 :
            print("emailStatus")
            emailStatus = emailStatusReq.json()
            print(emailStatus)
            return emailStatus
        return None
    #
    def doSignUp(self, EMAIL, PASSWORD, ONLINE_ID, userDetailsData):
        self.slaveClientId()
        getSignUpReq = self.makeRequest(url=self.signupUrl, method="GET")
        self.checkPassword(PASSWORD)
        reservationId = self.reserveOnlineId(ONLINE_ID)
        userDetailsData["onlineIdReservation"] = reservationId
        #Solve Captcha Here
        reCaptchaResponse = solveCaptcha()
        accessToken = self.loginThroughCaptcha(EMAIL, reCaptchaResponse)
        self.loginId(accessToken, EMAIL)
        self.userDetails(accessToken, userDetailsData)
        self.getSsoCookie(accessToken, EMAIL, PASSWORD)
        newAccessToken = self.loginThroughSsoCookie()
        print(newAccessToken)
        self.commerceApi(newAccessToken)
        self.regcam(newAccessToken)
        self.commerceApi(newAccessToken)
        self.checkEmailStatus(newAccessToken)
        getReturnReq = self.makeRequest(url="https://account.sonyentertainmentnetwork.com/cam/account/profile/account-details.action", method="GET")
        return newAccessToken