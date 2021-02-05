
from zabbix_api_collection import BaseZabbixAPI

class ZabbixAPI(BaseZabbixAPI):
    def __init__(self,server,user_id, password):
        super(server,user_id,password)
        #トークン取得
        self.token = self.get_auth_token()
    
    # 認証トークン取得メソッド
    def get_auth_token(self):
        request_json = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user_id,
                "password": self.password
            },
            "id": 1,
            "auth": None
        }

        response = self.api_call(request_json)

        return response


    def host


if __name__=="__main__":
    SERVER = "http://internal-lss-dev-alb-ope-test-4-211112863.ap-northeast-1.elb.amazonaws.com/"
    file_name = "config.json"
    token = ""

    tmp = BASE_ZabbixAPI(SERVER,"Admin","zabbix")

    print(tmp.token)
