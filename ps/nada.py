import requests
import random
from lxml import html

class Nada(object):
    def __init__(self):
        self.session = self.initSession()
        self.domain = self.selectAvailableDomain()
        # self.domain = "getnada.com"
        return None
    #
    def initSession(self):
        headers = {
            "Host": "app.getnada.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Referer": "https://app.getnada.com/inbox/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }
        session = requests.Session()
        session.headers = headers
        print(session.headers['User-Agent'])
        return session
    #
    def selectAvailableDomain(self):
        get_domains = self.session.get("https://app.getnada.com/api/v1/domains").json()
        domains = [i["name"] for i in get_domains]
        print(domains)
        # domains.remove("nada.ltd")
        # print(domains)
        return random.choice(domains)
    #
    def checkEmails(self, custom_name):
        print(self.domain)
        email_req = self.session.get("https://app.getnada.com/api/v1/inboxes/{}@{}".format(custom_name, self.domain))
        print(email_req.url)
        print(email_req)
        all_emails = email_req.json()
        for each_email in all_emails:
            print(each_email)
            if "PlayStation" in each_email['f']:
                if "Account registration confirmation" in each_email['s']:
                    print("valid email")
                    mail_uid = each_email["uid"]
                    print(mail_uid)
                    #Retreive message
                    get_email = self.session.get("https://app.getnada.com/api/v1/messages/{}".format(mail_uid)).json()
                    email_tree = html.fromstring(get_email["html"])
                    confirmation_email_url = email_tree.xpath('//a[contains(text(), "Verify Now")]')[0].attrib.get('href')
                    return confirmation_email_url
        return []



# nada_obj = Nada()
# nada_obj.checkEmails("test")


