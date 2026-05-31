from jsonschema.validators import validate
import pytest
from api.blog_api import BlogApi
from utils.yaml_util import read_yaml


class TestDetail:
    schema = {
        "type": "object",
        "required": ["code","errMsg","data"],
        "properties": {
            "code": {
            "type": "number"
            },
            "errMsg": {
            "type": ["string", "null"]
            },
            "data": {
            "type": ["array", "null","object"],
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

    #未登录状态下访问
    def test_detail_nologin(self):
        res = BlogApi().get_detail(read_yaml("data.yaml", "blogId"), no_auth=True)
        assert res.status_code == 401

    #登录状态下访问
    def test_detail_login(self):
        blog_id = read_yaml("data.yaml", "blogId")
        res = BlogApi().get_detail(blog_id)
        validate(instance=res.json(), schema=self.schema)
        assert res.status_code == 200

    #错误的blogId
    @pytest.mark.parametrize("blogId",["","-1","0","a","123456789"])
    def test_detail_fail(self,blogId):
        res = BlogApi().get_detail(blogId)
