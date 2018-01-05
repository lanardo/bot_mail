from ps.generators import Generators
from ps.signup import SignUp

# from nada import Nada
from ps.tempmail import TempMail
from ps.card import Card

import json
import time
import threading


card_handler = Card()
generatorHandler = Generators()
# nada_handler = Nada()
# nada_handler.checkEmails(ONLINE_ID)

temp_mail_handler = TempMail()


def single_signup():
    signup_handler = SignUp()
    with open("userDataSample.json", "r") as loadUserDataSample:
        userDetailsData = json.load(loadUserDataSample)
    #
    data = generatorHandler.generate()
    DOB = data.get("DOB")
    PASSWORD = data.get("PASSWORD")
    FIRST_NAME = data.get("FIRST_NAME")
    LAST_NAME = data.get("LAST_NAME")
    COUNTRY_SUB_DIVISION = data.get("COUNTRY_SUB_DIVISION")   
    CITY = data.get("CITY")
    POSTAL_CODE = data.get("POSTAL_CODE")
    ONLINE_ID = data.get("ONLINE_ID")    
    EMAIL = ONLINE_ID + temp_mail_handler.domain
    print(EMAIL)
    userDetailsData["communicationName"]["first"] = FIRST_NAME 
    userDetailsData["communicationName"]["last"] = LAST_NAME 
    userDetailsData["addresses"][0]["city"] = CITY
    userDetailsData["addresses"][0]["countrySubdivision"] = COUNTRY_SUB_DIVISION
    userDetailsData["addresses"][0]["postalCode"] = POSTAL_CODE
    userDetailsData["emailAddresses"][0]["address"] = EMAIL
    userDetailsData["dateOfBirth"] = DOB
    userDetailsData["onlineId"] = ONLINE_ID
    userDetailsData["signinId"] = EMAIL
    userDetailsData["password"] = PASSWORD
    temp_mail_handler.changeEmail(ONLINE_ID)
    #
    a = signup_handler.doSignUp(EMAIL, PASSWORD, ONLINE_ID, userDetailsData)
    time.sleep(5)
    if temp_mail_handler.checkEmail():
        signup_handler.checkEmailStatus(a)
        with open("VERIFIED_ACCOUNTS.txt","a+") as save_out:
            save_out.write("EMAIL : " + str(EMAIL) + "\tPASSWORD :" + str(PASSWORD) + "\n")
        card_handler.cardinator(a)
    return [EMAIL, PASSWORD]


single_signup()


for i in range(10):
    print("\n\n\n\n")
    print("Signing Up Account : " + str(i))
    try:
        data = single_signup()
        print("Finished Signing up, credentials below")
        print(data[0], data[1])
    except Exception as e:
        print(e)

