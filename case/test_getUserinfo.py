from jsonschema.validators import validate
import pytest
from utils.yaml_util import read_yaml
from utils.request_util import Request,host




class TestUserInfo:
    url = host + "user/getUserInfo?userId="
    schema = {
        "type": "object",
        "required": ["code", "errMsg","data"],
        "properties": {
                "code": {
                "type": "number"
                },
                "errMsg": {
                "type": ["string","null"]
                },
                "data": {
                "type": "object",
                "required": ["id","userName","githubUrl"],
                    "properties": {
                        "id": {
                        "type": "number"
                        },
                        "userName": {
                        "type": "string"
                        },
                        "githubUrl": {
                        "type": "string"
                        }
                    }
                }
        }
    }

    #未登录获取用户信息
    def test_userinfo_nologin(self):
        url = self.url + str(read_yaml("data.yaml", "user_id"))
        res = Request().get(url)
        assert res.status_code == 401

    #登录获取用户信息&正确的user_id
    def test_userinfo_login(self):
        url = self.url + str(read_yaml("data.yaml", "user_id"))
        token = read_yaml("data.yaml", "user_token_header")
        header = {
            "User-Token": token 
        }
        res = Request().get(url,headers=header)
        validate(res.json(),self.schema)
        assert res.json()["code"] == 200

    #登录获取用户信息&错误的user_id
    @pytest.mark.parametrize("user_id",["0","-1","a","","11111111111111111111"])
    def test_userinfo_login_fail(self,user_id):
        url = self.url + user_id
        token = read_yaml("data.yaml", "user_token_header")
        header = {
            "User-Token": token 
        }

        res = Request().get(url,headers=header)
        assert res.json()["code"] == -1
