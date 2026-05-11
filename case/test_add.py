
from jsonschema.validators import validate
import pytest
from utils.yaml_util import read_yaml
from utils.request_util import Request,host




class TestAdd:
    url = host + "blog/addBlog"
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
    def test_add_noloogin(self):
        res = Request().post(url=self.url)
        assert res.status_code == 401




# {
# 	"userId": "1",
# 	"title": "111",
# 	"content": "##在这里写下一篇博客"
# }
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
    def test_login(self,login):
        token = read_yaml("data.yaml","user_token_header")
        header = {
            "User-Token":token
        }
        data = {
            "userId": login["userId"],
            "title": login["title"],
             "content": login["content"]
        }
        res = Request().post(url=self.url,json = data,headers=header)
        validate(instance=res.json(), schema=self.schema)
        assert res.json()["data"] == login["data"]




        