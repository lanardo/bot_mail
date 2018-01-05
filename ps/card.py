import requests
import json

from bs4 import BeautifulSoup as bs
from ps.requestsManager import RequestsManager

{
                    "Connection": "keep-alive",
                    "Origin": "https://id.sonyentertainmentnetwork.com",
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9"
                    }

class Card(RequestsManager):
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
    def getToken(self, CC_NUMBER):
    # Referer: https://transact.playstation.com/payment-instruments/add-credit-card?clientId=14e55179-c84c-46a9-ae31-cc9fb53aa734&layout=flex&platformId=CHIHIRO&reportSuite=snestorescea-uat
        cardData = {
                        "ccnumber": str(CC_NUMBER)
                    }
        #
        print(CC_NUMBER)
        headers = self.baseHeaders.copy()
        headers["Host"] = "tokenization.api.playstation.com"
        headers["Access-Control-Request-Method"] = "GET"
        headers["Origin"] = "https://transact.playstation.com"
        headers["Access-Control-Request-Header"] = "content-type,x-platform"
        headers["Content-Type"] = "application/json"
        cardDataHeaders = headers
        #
        url = "https://tokenization.api.playstation.com/api/v1/cctoken"
        getTokenReq = self.makeRequest(url=url, headers=cardDataHeaders, data=cardData)
        print("getting token for cc")
        if getTokenReq.status_code == 200:
            token = getTokenReq.json()["token"]
            print(token)
            return token
        return []
    #
    def addCardDetails(self, accessToken, CC_NUMBER, CC_NAME, CC_EXPIRATION_YEAR, CC_EXPIRATION_MONTH, CC_CVV, CC_STREET, CC_CITY, CC_ZIPCODE, CC_STATE, CC_COUNTRY):
        # Referer: https://transact.playstation.com/payment-instruments/add-credit-card?clientId=14e55179-c84c-46a9-ae31-cc9fb53aa734&layout=flex&platformId=CHIHIRO&reportSuite=snestorescea-uat
        headers = self.baseHeaders.copy()
        headers["Host"] = "wallets.api.playstation.com"
        headers["Access-Control-Request-Method"] = "GET"
        headers["Origin"] = "https://transact.playstation.com"
        headers["X-Platform"] = "CHIHIRO"
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer" + accessToken #8bf93308-360e-41a4-a684-fd759e93a9c9
        addCardDetailsHeaders = headers
        addCardDetailsData = {
                                "instrumentId":None,
                                "paymentMethodId":"VISA",
                                "defaultPaymentInstrument":True,
                                "paymentMethodType":"CC",
                                "holderName": CC_NAME,
                                "cardNumber": CC_NUMBER,
                                "expirationYear": int(CC_EXPIRATION_YEAR),
                                "expirationMonth": int(CC_EXPIRATION_MONTH),
                                "securityCode": CC_CVV,
                                "billingAddress":
                                                {
                                                    "line1": CC_STREET,
                                                    "line2":"",
                                                    "line3":"",
                                                    "city": CC_CITY,
                                                    "provinceOrState": CC_STATE,
                                                    "zipOrPostalCode": CC_ZIPCODE,
                                                    "country": CC_COUNTRY
                                                }
                                }
        url = "https://wallets.api.playstation.com/api/v1/wallets/me/savedInstruments/creditCards"
        addCardDetailsReq = self.makeRequest(url=url, headers=addCardDetailsHeaders, data=addCardDetailsData)
        if addCardDetailsReq.status_code == 200:
            instrumentId = addCardDetailsReq.json()["common"]["instrumentId"]
            print(instrumentId)
            return addCardDetails
        return None
    #
    def patchCardDetails(self, accessToken, instrumentId):
        # Referer: https://transact.playstation.com/payment-instruments/add-credit-card?clientId=14e55179-c84c-46a9-ae31-cc9fb53aa734&layout=flex&platformId=CHIHIRO&reportSuite=snestorescea-uat
        headers = self.baseHeaders.copy()
        headers["Host"] = "wallets.api.playstation.com"
        headers["Access-Control-Request-Method"] = "GET"
        headers["Origin"] = "https://transact.playstation.com"
        headers["X-Platform"] = "CHIHIRO"
        headers["Content-Type"] = "application/json-patch+json"
        headers["Authorization"] = "Bearer" + accessToken #8bf93308-360e-41a4-a684-fd759e93a9c9
        patchCardDetailsHeaders = headers
        patchCardDetailsData = [{"op":"replace","path":"/creditCard/common/defaultPaymentInstrument","value":True}]
        url = "https://wallets.api.playstation.com/api/v1/wallets/me/savedInstruments/" + str(instrumentId)
        patchCardDetailsReq = self.makeRequest(url=url, headers=patchCardDetailsHeaders, data=patchCardDetailsData)
        if patchCardDetailsReq.status_code == 200:
            cardDetails = patchCardDetailsReq.json()
            return cardDetails
        return None
    #
    def cartDetails(self):
        # Referer: https://store.playstation.com/en-us/product/IP9101-NPIA90005_01-PSPLUS14DAYTRIAL?code=JQfoH7&state=returning
        headers = self.baseHeaders.copy()
        headers["Host"] = "store.playstation.com"
        headers["x-requested-by"] = "Chihiro-PSStore"
        cartDetailsHeaders = headers

        url = "https://store.playstation.com/kamaji/api/valkyrie_storefront/00_09_000/user/checkout/cart"
        cartDetailsReq = self.makeRequest(url=url, headers=cartDetailsHeaders, method="GET")
        if cartDetailsReq.status_code == 200:
            cardDetails = cartDetailsReq.json()
            return cardDetails
        return None
    #
    def buyNowPreview(self):
        # Referer: https://store.playstation.com/en-us/product/IP9101-NPIA90005_01-PSPLUS14DAYTRIAL?code=JQfoH7&state=returning
        headers = self.baseHeaders.copy()
        headers["Host"] = "store.playstation.com"
        headers["Origin"] = "https://store.playstation.com"
        headers["x-requested-by"] = "Chihiro-PSStore"
        headers["content-type"] = "application/x-www-form-urlencoded"
        buyNowPreviewHeaders = headers
        buyNowPreviewData = { "sku": "IP9101-NPIA90005_01-PSPLUS14DAYTRIAL-U005" }
        url = "https://store.playstation.com/kamaji/api/valkyrie_storefront/00_09_000/user/checkout/buynow/preview"
        buyNowPreviewReq = self.makeRequest(url=url, headers=buyNowPreviewHeaders, data=buyNowPreviewData)
        if buyNowPreviewReq.status_code == 200:
            cardDetails = buyNowPreviewReq.json()
            return cardDetails
        return None
    #
    def getProduct(self):
        headers = self.baseHeaders.copy()
        headers["Host"] = "store.playstation.com"
        getProductHeaders = headers
        url = "https://store.playstation.com/store/api/chihiro/00_09_000/container/US/en/19/IP9101-NPIA90005_01-PSPLUS14DAYTRIAL"
        cartDetailsReq = self.makeRequest(url=url, headers=getProductHeaders, method="GET")
        return None
    #
    def buyNow(self, instrumentId):
        # instrumentId = 1033975554
        # Referer: https://store.playstation.com/en-us/checkout/buy-now/IP9101-NPIA90005_01-PSPLUS14DAYTRIAL-U005
        headers = self.baseHeaders.copy()
        headers["Host"] = "store.playstation.com"
        headers["Origin"] = "https://store.playstation.com"
        headers["x-requested-by"] = "Chihiro-PSStore"
        headers["content-type"] = "application/x-www-form-urlencoded"
        buyNowPreviewHeaders = headers
        buyNowPreviewData = {
                                "sku": "IP9101-NPIA90005_01-PSPLUS14DAYTRIAL-U005",
                                "autoDeposit": "true",
                                "payment_id" : int(instrumentId)
                            }
        url = "https://store.playstation.com/kamaji/api/valkyrie_storefront/00_09_000/user/checkout/buynow"
        buyNowPreviewReq = self.makeRequest(url=url, headers=buyNowPreviewHeaders, data=buyNowPreviewData)
        if buyNowPreviewReq.status_code == 200:
            buyNow = buyNowPreviewReq.json()
            print(buyNow["header"]["success"])
            return buyNow
        return None
    #
    def removeCard(self):
        headers = self.baseHeaders.copy()
        headers["Host"] = "account.sonyentertainmentnetwork.com"
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        removeCardHeaders = headers
        url = "https://account.sonyentertainmentnetwork.com/liquid/cam/account/mywallet/view-wallet.action?displayNavigation=false"
        getWalletReq = self.makeRequest(url=url, headers=removeCardHeaders, method="GET")
        soup = bs(getWalletReq.content, "html.parser")
        struts_token = soup.find("input", {"name":"struts.token" })["value"]
        paymentInstrumentId = soup.find("input", {"name":"paymentInstrumentId" })["value"]
        print(struts_token, paymentInstrumentId)
        removeCardHeaders["Origin"] = "https://account.sonyentertainmentnetwork.com"
        removeCardHeaders["Content-Type"] = "application/x-www-form-urlencoded"
        removeCardData = {
                            "struts.token.name" : "struts.token",
                            "struts.token": str(struts_token),
                            "paymentInstrumentId" : str(paymentInstrumentId)
                        }

        url = "https://account.sonyentertainmentnetwork.com/liquid/cam/account/mywallet/remove-payment-instrument-flow.action"
        removeCardReq = self.makeRequest(url=url, headers=removeCardHeaders, data="removeCardData")
        if removeCardReq.status_code == 302:
            print("Card removed Successfully")
            return True
        return None
    #
    def cardinator(self, accessToken):
        print("Adding Card and subscribing now")
        print(accessToken)
        CC_NUMBER = "4941127281747846"
        CC_NAME = "Mazen Mashally"
        CC_EXPIRATION_YEAR = 2021
        CC_EXPIRATION_MONTH = 9
        CC_CVV = "178"
        CC_STREET = "los angeles"
        CC_CITY = "los angeles"
        CC_ZIPCODE = "90005"
        CC_STATE = "CA"
        CC_COUNTRY = "US"
        self.getToken(CC_NUMBER)
        instrumentId = self.addCardDetails(accessToken, CC_NUMBER, CC_NAME, CC_EXPIRATION_YEAR, CC_EXPIRATION_MONTH, CC_CVV, CC_STREET, CC_CITY, CC_ZIPCODE, CC_STATE, CC_COUNTRY)
        self.patchCardDetails(accessToken, instrumentId)
        self.cartDetails()
        self.buyNowPreview()
        self.getProduct()
        self.buyNow()
        self.removeCard()
        return None
