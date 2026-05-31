from jsonschema.validators import validate
import pytest
from api.blog_api import BlogApi


class TestAdd:
    schema = {
        "type": "object",
        "required": ["code","errMsg","data"],
        "properties": {
            "code": {
            "type": "number"
            },
            "errMsg": {
            "type": ["string","null"]
            },
            "data": {
            "type": ["boolean","null"]
            }
        }
    }
    #未登录访问
    def test_add_nologin(self):
        res = BlogApi().add_blog("1", "", "", no_auth=True)
        assert res.status_code == 401

    #登录访问
    @pytest.mark.parametrize("login",[
        #标题内容都不为空
        {
            "userId": "1",
            "title": "test1",
            "content": "##在这里写下一篇博客",
            "data": True
        },
        #标题为空
        {
            "userId": "1",
            "title": "",
            "content": "##在这里写下一篇博客",
            "data": None
        },
        #内容为空
        {
            "userId": "1",
            "title": "test1",
            "content": "",
            "data": None
        },
        #标题内容都为空
        {
            "userId": "1",
            "title": "",
            "content": "",
            "data": None
        }
    ])
    def test_add(self,login):
        res = BlogApi().add_blog(login["userId"], login["title"], login["content"])
        validate(instance=res.json(), schema=self.schema)
        assert res.json()["data"] == login["data"]
