import pytest
from jsonschema.validators import validate
from utils.request_util import Request,host
from utils.yaml_util import read_yaml, write_yaml


@pytest.mark.order(2)
class TestList:
    url = host + "blog/getList"
    schema = {
        "type": "object",
        "required": ["code","errMsg", "data"],
        "properties": {
            "code": {
            "type": "number"
            },
            "errMsg": {
            "type": ["string", "null"]
            },
            "data": {
            "type": ["array", "null"],
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id","title","content","userId","updateTime"],
                "properties": {
                "id": {
                    "type": "number"
                },
                "title": {
                    "type": "string"
                },
                "content": {
                    "type": "string"
                },
                "userId": {
                    "type": "number"
                },
                "updateTime": {
                    "type": "string"
                }
                }
            }
        }
    }
}

    #未登录状态请求list接口
    def test_list_nologin(self):
        res = Request().get(url =self.url)
        assert res.status_code == 401

    #登录状态请求list接口   
    def test_list_login(self):
        token = read_yaml("data.yaml","user_token_header")
        header = {
            "User-Token":token
        }
        print(f"header:{header}")
        res = Request().get(url =self.url,headers = header)
        validate(instance=res.json(), schema=self.schema)
        assert res.json()["code"] == 200

        blogId = {
            "blogId":res.json()["data"][0]["id"]
        }
        write_yaml("data.yaml",blogId)
