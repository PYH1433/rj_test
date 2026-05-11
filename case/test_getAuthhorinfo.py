
import pytest
from jsonschema.validators import validate
from utils.request_util import Request,host
from utils.yaml_util import read_yaml, write_yaml



@pytest.mark.order(3)
class TestAuthorInfo:
    url = host + "user/getAuthorInfo?blogId="
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


    #未登录状态获取作者信息
    def test_authorinfo_nologin(self):
        url = self.url + str(read_yaml("data.yaml", "blogId"))
        res = Request().get(url=url)
        assert res.status_code == 401

    #登录状态获取作者信息&正确的blgId
    def test_authorinfo_login(self):
        url = self.url + str(read_yaml("data.yaml", "blogId"))
        token = read_yaml("data.yaml", "user_token_header")
        header = {
            "User-Token": token 
        }
        res = Request().get(url=url,headers=header)
        validate(instance=res.json(), schema=self.schema)
        assert res.json()["code"] == 200
        id = {
            "user_id": res.json()["data"]["id"]
        }
        #将用户id存入data.yaml
        write_yaml("data.yaml", id)

    #登录状态获取作者信息&错误的blgId
    @pytest.mark.parametrize("blogId",["","0","0.1","-1","a","9999999"])
    def test_authorinfo_login_fail(self,blogId):
        url = self.url + blogId
        token = read_yaml("data.yaml", "user_token_header")
        header = {
            "User-Token": token 
        }
        res = Request().get(url=url,headers=header)
        assert res.json()["code"] == -1




