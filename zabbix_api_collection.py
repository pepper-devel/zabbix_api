

import json
import urllib.request
from app_config_ctl import AppConfigController

#APIの基底クラス
class BaseZabbixAPI():

    def __init__(self,server):
        self.server = server

    # apicallメソッド
    def api_call(self,parameter):
        url = self.server + "/api_jsonrpc.php"
        try:
            request = urllib.request.Request(
                url=url,
                data=json.dumps(parameter).encode(),
                headers={"Content-Type": "application/json-rpc"}
            )

            with urllib.request.urlopen(request) as response:
                dictionary = json.loads(response.read())
                # print(dictionary)
                return dictionary["result"]
        except:
            raise
    

class UserLoginZabbixAPI(BaseZabbixAPI):
    def __init__(self,server):
        super().__init__(server)

    # 認証トークン取得メソッド
    def get_auth_token(self,user_id,password):
        request_json = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": user_id,
                "password": password
            },
            "id": 1,
            "auth": None
        }

        response = super().api_call(request_json)

        return response


class HostZabbixAPI(BaseZabbixAPI):
    def __init__(self,server,token=None,user_id=None,password=None):
        super().__init__(server)

        if token is not None:
            self.token = token
        elif user_id is not None and password is not None:
            user_login = UserLoginZabbixAPI(server)
            self.token = user_login.get_auth_token(user_id,password)
        else:
            raise Exception("No API access information")
    

    def get(self,host_name_list):
        request_json = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "filter": {
                    "host": host_name_list
                }
            },
            "auth": self.token,
            "id": 1
        }

        response = super().api_call(request_json)

        return response








# # apicallメソッド
# def api_call(server, parameter):
#     url = server + "/api_jsonrpc.php"
#     try:
#         request = urllib.request.Request(
#             url=url,
#             data=json.dumps(parameter).encode(),
#             headers={"Content-Type": "application/json-rpc"}
#         )

#         with urllib.request.urlopen(request) as response:
#             dictionary = json.loads(response.read())
#             # print(dictionary)
#             return dictionary["result"]
#     except:
#         raise

# # 認証トークン取得メソッド
# def get_auth_token(user_id, password, server=SERVER):
#     request_json = {
#         "jsonrpc": "2.0",
#         "method": "user.login",
#         "params": {
#             "user": user_id,
#             "password": password
#         },
#         "id": 1,
#         "auth": None
#     }

#     response = api_call(server, request_json)

#     return response


# def get_hostgroupid(hostgroup_name, server=SERVER):
#     request_json = {
#         "jsonrpc": "2.0",
#         "method": "hostgroup.get",
#         "params": {
#             "output": "extend",
#             "filter": {
#                 "name": [
#                     hostgroup_name
#                 ]
#             }
#         },
#         "auth": token,
#         "id": 1
#     }

#     response = api_call(server, request_json)

#     return response[0]["groupid"]


# def get_host_dtl(host_name, server=SERVER):
#     request_json = {
#         "jsonrpc": "2.0",
#         "method": "host.get",
#         "params": {
#             "filter": {
#                 "host": [host_name]
#             }
#         },
#         "auth": token,
#         "id": 1
#     }

#     response = api_call(server, request_json)

#     return response

# def create_host(hostgroup_id,host,name,proxy_hostid, server=SERVER):
#     request_json = {
#         "jsonrpc": "2.0",
#         "method": "host.create",
#         "params": {
#         'proxy_hostid': proxy_hostid,
#         'host': host,
#         'name' : name,
#         "interfaces":[
#             {
#                 "type": 1,
#                 "main": 1,
#                 "useip": 1,
#                 "ip": "127.0.0.1",
#                 "dns": "",
#                 "port": "10050"
#             }
#         ],
#         "groups": [
#             {
#                 "groupid": hostgroup_id
#             }
#         ]
#     },
#         "auth": token,
#         "id": 1
#     }

#     response = api_call(server, request_json)

#     return response

# #ホストの存在チェック
# def exist_host(host,server=SERVER):
#     dtl = get_host_dtl(host,server=server)
#     if dtl == []:
#         return False
#     else:
#         return True


# #存在しないホストを作成するメソッド
# def create_nonexistent_host(hostgroup_id,host,name,proxy_hostid,server=SERVER):

#     #ホストがある場合
#     if exist_host(host):
#         print(host + " already exists.")
#         return None 

#     #ホストがない場合
#     else:
#         response = create_host(hostgroup_id,host,name,proxy_hostid,server=server)
#         print(host + " is created. hostid :" + response["hostids"][0])
#         return response["hostids"][0]

# #itemの設定情報を取得するメソッド
# def get_item_info():
#     json_open = open("item_info_for_app_config.json", 'r')
#     return json.load(json_open)

# #itemを作成するメソッド
# # value_type：
# # 0-数値フロート。
# # 1-文字;
# # 2-ログ;
# # 3-数値の符号なし。
# # 4-テキスト。
# def create_item(host_id,key,name,value_type,server=SERVER):
#     request_json = {
#     "jsonrpc": "2.0",
#     "method": "item.create",
#     "params": {
#         "name": name,
#         "key_": key,
#         "hostid": host_id,
#         "type": 2,
#         "value_type": value_type,
#         "delay": "30s"
#     },
#     "auth": token,
#     "id": 1
# }

#     response = api_call(server, request_json)

#     return response

# #指定したホストグループにapp_configのホストとアイテムを作るメソッド
# def create_host_and_item_from_app_config(file_name,hostgroup_name):
#     # トークン取得
#     token = get_auth_token("Admin", "zabbix")

#     # ホストグループID取得
#     hostgroup_id = get_hostgroupid(hostgroup_name)

#     #プロキシサーバID
#     proxy_hostid = "10271"

#     acc_obj = AppConfigController(file_name)

#     host_item_dict = acc_obj.get_host_item_dict()

#     item_info = get_item_info()
#     print(item_info)
#     for host in host_item_dict:
#         host_id = create_nonexistent_host(hostgroup_id,host,host,proxy_hostid)
 
#         if host_id is None:
#             #ホストが作られなかったら何もしない
#             continue
#         else:
#             #ホストが作られたら紐づいたアイテムも作る
#             for item in host_item_dict[host]:
#                 if item in item_info:
#                     create_item(host_id,item,item,item_info[item])
#                 else:
#                     create_item(host_id,item,item,"4")

# if __name__ == "__main__":

#     # # トークン取得
#     token = get_auth_token("Admin", "zabbix")

#     # # ホストグループID取得
#     # hostgroup_id = get_hostgroupid("lambda-test2")

#     # #プロキシサーバID
#     # proxy_hostid = "10271"

#     # acc_obj = AppConfigController("app_config.json")

#     # #app_configからホストアイテム対応dictを取得
#     # host_item_dict = acc_obj.get_host_item_dict()

#     # #item作成情報取得
#     # item_info = get_item_info()

#     # print(get_host_dtl("lss-dev-ecscluster-lss-account"))
    


#     create_host_and_item_from_app_config("app_config_log.json","lambda-logs")
