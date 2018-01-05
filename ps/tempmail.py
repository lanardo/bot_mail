# 1b4af3fe@emailo.pro
import requests
import random
import datetime
from lxml import html

class TempMail(object):
    def __init__(self):
        self.change_email_url = "https://temp-mail.org/en/option/change/"
        self.check_email_url = "https://temp-mail.org/en/option/check/?_=" # + timestamp 1511800684943
        # self.custom_name = str(custom_name)
        self.session = self.initSession()
        self.domain = self.availableDomains()
        return None
    #
    def initSession(self):
        session = requests.Session()
        session.headers['User-Agent'] =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        print(session.headers['User-Agent'])
        return session
    #
    def extractCsrfToken(self):
        extract_token = self.session.get(self.change_email_url)
        tree = html.fromstring(extract_token.content)
        csrf_token = tree.xpath('//input[@type="hidden" and @name="csrf"]')[0].value
        # <input type="hidden" name="csrf" value="de0d10eae1f7250593aecef707069143" style="display:none;">
        return csrf_token
    #
    def availableDomains(self):
        get_domains = self.session.get(self.change_email_url)
        tree = html.fromstring(get_domains.content)
        domains_selector = tree.xpath('//select[@name="domain" and @id="domain"]')[0].getchildren()
        domains = [i.text for i in domains_selector]
        domain = random.choice(domains)
        return domain
    #
    def changeEmail(self, custom_name):
        # "domain": "%40zhorachu.com"
        change_email_data = {
                            "csrf": self.extractCsrfToken(),
                            "mail": custom_name,
                            "domain": self.domain,
        }
        print(change_email_data)
        change_email = self.session.post(self.change_email_url, data = change_email_data)
        print(change_email)
        print(change_email.url)
        print(change_email.history)
        tree = html.fromstring(change_email.content)
        temp_email = tree.xpath('//div[@class="yourmail"]//input[@id="mail"]')[0].value
        print(temp_email)
        return temp_email
    #
    def generateTimestamp(self):
        return str(int(datetime.datetime.now().timestamp())*1000)
    #
    def checkEmail(self):
        check_email = self.session.get(self.check_email_url + self.generateTimestamp())
        # print(check_email.content)
        print(check_email.url)
        print(check_email)
        tree = html.fromstring(check_email.content)
        new_emails = tree.xpath('//table[@id="mails"]//td//a[@class="title-subject"]')
        if new_emails != []:
            emails_urls = [i.attrib["href"] for i in new_emails]
            self.parseEmail(emails_urls)
        return new_emails
    #
    def parseEmail(self, urls):
        for url in urls:
            getEmailReq = self.session.get(url)
            tree = html.fromstring(getEmailReq.content)
            # https://account.sonyentertainmentnetwork.com/liquid/cam/account/email/validate-email.action?service-entity=np&token=NDNmYjNlMzQtMjUwfh%2F1mS12ezBYei9vF4g3SnPqWRyGMrnyS4USUC8O9e4S9YcIaCyDpHSpqFxRFKWwvSVyGqdygCFisQbDboMkK4TWxGWf%2FiXQNZpTgBadytk%3D&request_locale=en_US
            verification_url = tree.xpath('//a[contains(text(),"Verify Now")]')[0].attrib["href"]
            if  "validate-email.action" in verification_url:
                print("Verifying Account")
                print(verification_url)
                verifying = self.session.get(verification_url)
                print(verifying)
                print(verifying.url)
                print(verifying.history)
                return True
        return None



