import requests

class Envato:

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.s = requests.session()
        self.s.headers.update({
            'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
        })
        self.isLogged = False
        self.token = ""
        self.userData = {}
    
    def login(self):
        r = self.s.get("https://elements.envato.com/sign-in")
        data = {
            'username':self.username,
            'password':self.password,
            'language_code':'en',
            'to':'elements'
        }
        r = self.s.post("https://account.envato.com/api/sign_in",data=data)
        if r.json()['state'] == 'ok':
            # self.isLogged = True
            self.token = r.json()['token']
            print(self.token)
            _data = {
                'original_landing_page':'https://elements.envato.com/seppo-corporate-one-page-html-template',
                'token':self.token
            }
            r = self.s.post("https://elements.envato.com/api/v1/sign_in.json",json=_data)
            if r.status_code == 200:
                self.isLogged = True
                self.userData = r.json()
                print("============ENVATO LOGIN SUCCESS==========")
                print(f"Envato Username: {self.userData['data']['attributes']['ssoUser']['envatoUsername']}")
                print(f"Envato ID: {self.userData['data']['id']}")
                print(f"Envato Customer Type: {self.userData['data']['attributes']['marketingCustomerType']}")
            else:
                print(r.text)
        else:
            print(r.text)


if __name__ == "__main__":
    a = Envato("USERNAME",'PASSWORD')
    a.login()