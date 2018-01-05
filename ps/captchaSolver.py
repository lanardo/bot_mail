import requests
import time

dataSiteKey="6LdSoRkTAAAAAAhKr1g2Zy4cCtE4hrgwIBdMYhXL"
API_KEY = "6bb015504bbb633f9f2b78d15182105e"

captchaPageUrl = "https://id.sonyentertainmentnetwork.com/create_account/?entry=/create_account&tp_psn=true&state=returning&disableLinks=SENLink&ui=pr&client_id=f6c7057b-f688-4744-91c0-8179592371d2&hidePageElements=SENLogo&prompt=login&redirect_uri=https://store.playstation.com/en-us/product/IP9101-NPIA90005_01-PSPLUS14DAYTRIAL&request_locale=en_US&response_type=code&scope=kamaji:commerce_native,kamaji:commerce_container,kamaji:lists&service_entity=urn:service-entity:psn#/create_account/wizard/psn_profile?entry=/create_account"


def solveCaptcha():
    captchaSession = requests.Session()
    captchaPostUrl = "http://2captcha.com/in.php?key={}&json=1&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, dataSiteKey, captchaPageUrl)
    # print(captchaPostUrl)
    captchaId = {"status" : 0}
    while (captchaId["status"] != 1):
        print("refreshing captcha")
        captchaPostReq = captchaSession.get(captchaPostUrl)
        # print(captchaPostReq)
        # print(captchaPostReq.url)
        print(captchaPostReq.text)
        captchaId = captchaPostReq.json()
        print(captchaId)
        time.sleep(5)
    #{"status":1,"request":"03AO6mBfzL1pFJDkrITXPLpA20Dwe5znaWuNIgFPfFbUVS9sa3swJqhuJekWnfCqSgYp95ZL9QdYlMVj76sxmS2dDVaEdRCiz2wAOaZwzNJSMNO2Eg3XWT97fK83M9vlw72-qExGct0sZuZszwsBvI-nNXVu_jvJuSQt3juVjehVmNk9J7uFVjj53rm6RXblEsJtTOMkVjkYeCc2W-SP8kAPP8o9ijw2hgrv9nEEq43TgYzbvNv17aiIrMo2zgX-gEqP_K3SN4ZkHUyVYVSOO3yI1tM6NgJUTICbPDoUNo_1oBNOySPjNPT5nXUmO0hTki_6YA-Kyp9s_Ian2x7O0GRtD8AU4aoQcdvSSRmmfINp0oMIId1te6DmE"}
    captchaId = captchaPostReq.json()["request"]
    getResponse = {"status":0,"request":"CAPCHA_NOT_READY"}
    while (getResponse["status"] != 1):
        time.sleep(5)
        getResponse = captchaSession.get("http://2captcha.com/res.php?key={}&action=get&id={}&json=1".format(API_KEY, captchaId)).json()
        print("Getting response")
        print(getResponse)
    captchaResponse = getResponse["request"]
    print(captchaResponse)
    return captchaResponse


