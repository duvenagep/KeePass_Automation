from urllib import request
import json, re, random,string
from secrets import USERNAME, PASSWORD


class PPS:
    def __init__(self, host='https://nlpps.sweco.se'):
        self.host = host
        self.token = None
        self.auth_header = None

    def get_token(self, user, passwd):
        url = f'{self.host}/oauth2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'grant_type=password&username={user}&password={passwd}'
        req = request.Request(url, data.encode(), headers)
        res = request.urlopen(req)
        self.token = json.loads(res.readlines()[0].decode())['access_token']
        self.auth_header = {'Authorization': f'Bearer {self.token}'}

    def get_root(self):
        url = f'{self.host}/api/v4/rest/credentialgroup/root'
        headers = {**self.auth_header, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
        req = request.Request(url, None, headers)
        res = request.urlopen(req).readlines()[0].decode().strip('"')
        return res

    def get_entry(self,entry_id):
        url = f'{self.host}/api/v4/rest/credentialgroup/{entry_id}'
        headers = {**self.auth_header, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
        req = request.Request(url, None, headers)
        res = request.urlopen(req).readlines()[0].decode().strip('"')
        return res

    def get_entry_ind(self,entry_id):
        url = f'{self.host}/api/v4/rest/credential/{entry_id}'
        headers = {**self.auth_header, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
        req = request.Request(url, None, headers)
        res = request.urlopen(req).readlines()[0].decode().strip('"')
        return res

    def get_password(self,entry_id):
        url = f'{self.host}/api/v4/rest/credential/{entry_id}/password'
        headers = {**self.auth_header, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
        req = request.Request(url, None, headers)
        res = request.urlopen(req).readlines()[0].decode().strip('"')
        return res

    def update_entry(self,data,entry_id):
        url = f'{self.host}/api/v4/rest/credential/{entry_id}'
        headers = {**self.auth_header, 'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
        req = request.Request(url, bytes(data.encode('utf-8')), headers, method="PUT")
        res = request.urlopen(req)
        return res

def get_SID(self,data):
    service_name = re.findall('SERVICE_NAME\s=\s\w+.\w+.\w+',data)[0].replace("SERVICE_NAME = ","")
    host = re.findall('HOST\s=\s\w+.\w+.\w+',data)[0].replace("HOST = ","")
    print(service_name,host)
    # print(f"sqlplus {username}/{password}@{host}:1521/{service_name}")


def new_password(length):
    random_source = string.ascii_letters + string.digits
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
 
    for i in range(length-3):
        password += random.choice(random_source)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password


 


if __name__ == "__main__":
    print("Hello world!")

    OBSURV_PUB_ID = '23e73774-86c1-42f0-bcb5-06e947d09752'
    OBSURV_INT_ID = '101ba6f7-04cd-47ef-a355-379b2f48efee'
    ORACLE = '437a8261-bfa4-4e34-8c35-795fcf827329'

    sessionPPS = PPS()
    sessionPPS.get_token(USERNAME,PASSWORD)

    obsurv_int = json.loads(sessionPPS.get_entry(OBSURV_INT_ID))
    obsurv_pub = json.loads(sessionPPS.get_entry(OBSURV_PUB_ID))
      
    acc_list = []
    for account_pub in obsurv_pub['Credentials']:
        password = sessionPPS.get_password(account_pub["Id"])

        for account_int in obsurv_int['Credentials']:
            if account_pub["Name"] in account_int["Name"]:
                _acc =  json.loads(sessionPPS.get_entry_ind(account_int["Id"]))
                name = _acc["Name"]

                data = {}
                data["Id"] = _acc["Id"]
                data["Name"] = _acc["Name"]
                data["GroupId"] = _acc["GroupId"]
                data["Username"] = _acc["Username"]
                data["Url"] = _acc["Url"]
                data["Notes"] = _acc["Notes"]
                data["Password"] = password

                update = json.dumps(data)

                sessionPPS.update_entry(update,_acc["Id"])
                print(f"Account {name} has been updated!")

