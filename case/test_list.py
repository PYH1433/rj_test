import pytest
from jsonschema.validators import validate
from api.blog_api import BlogApi
from utils.yaml_util import update_yaml


@pytest.mark.order(2)
class TestList:
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
        res = BlogApi().get_list(no_auth=True)
        assert res.status_code == 401

    #登录状态请求list接口
    def test_list_login(self):
        res = BlogApi().get_list()
        validate(instance=res.json(), schema=self.schema)
        assert res.json()["code"] == 200

        update_yaml("data.yaml", {"blogId": res.json()["data"][0]["id"]})
