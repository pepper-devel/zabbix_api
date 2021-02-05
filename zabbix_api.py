
from zabbix_api_collection import BaseZabbixAPI,UserLoginZabbixAPI,HostZabbixAPI

class ZabbixAPI():
    def __init__(self,server,user_id, password):
        self.server = server
        self.user_id = user_id
        self.password = password
        #トークン取得
        user_login = UserLoginZabbixAPI(server)
        self.token = user_login.get_auth_token(user_id,password)

        self.host = HostZabbixAPI(self.server,self.token)



if __name__=="__main__":
    SERVER = "http://internal-lss-dev-alb-ope-test-4-211112863.ap-northeast-1.elb.amazonaws.com/"
    file_name = "config.json"
    token = ""

    zabbix_api_client = ZabbixAPI(SERVER,"Admin","zabbix")

    print(zabbix_api_client.host.get([]))
