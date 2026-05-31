from jsonschema.validators import validate
import pytest
from utils.yaml_util import read_yaml
from api.user_api import UserApi


class TestUserInfo:
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
        res = UserApi().get_user_info(read_yaml("data.yaml", "user_id"), no_auth=True)
        assert res.status_code == 401

    #登录获取用户信息&正确的user_id
    def test_userinfo_login(self):
        res = UserApi().get_user_info(read_yaml("data.yaml", "user_id"))
        validate(res.json(),self.schema)
        assert res.json()["code"] == 200

    #登录获取用户信息&错误的user_id
    @pytest.mark.parametrize("user_id",["0","-1","a","","11111111111111111111"])
    def test_userinfo_login_fail(self,user_id):
        res = UserApi().get_user_info(user_id)
        assert res.json()["code"] == -1
