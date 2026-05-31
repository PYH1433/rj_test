import pytest
from jsonschema.validators import validate
from api.user_api import UserApi
from utils.yaml_util import read_yaml, update_yaml


@pytest.mark.order(3)
class TestAuthorInfo:
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
        res = UserApi().get_author_info(read_yaml("data.yaml", "blogId"), no_auth=True)
        assert res.status_code == 401

    #登录状态获取作者信息&正确的blogId
    def test_authorinfo_login(self):
        res = UserApi().get_author_info(read_yaml("data.yaml", "blogId"))
        validate(instance=res.json(), schema=self.schema)
        assert res.json()["code"] == 200
        update_yaml("data.yaml", {"user_id": res.json()["data"]["id"]})

    #登录状态获取作者信息&错误的blogId
    @pytest.mark.parametrize("blogId",["","0","0.1","-1","a","9999999"])
    def test_authorinfo_login_fail(self,blogId):
        res = UserApi().get_author_info(blogId)
        assert res.json()["code"] == -1
