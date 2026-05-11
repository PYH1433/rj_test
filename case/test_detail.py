from jsonschema.validators import validate
import pytest
from utils.request_util import Request,host
from utils.yaml_util import read_yaml


class TestDetail:
    url = host + "blog/getBlogDetail?blogId=" 
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
        url = self.url + str(read_yaml("data.yaml", "blogId"))
        res = Request().get(url=self.url)
        assert res.status_code == 401

    #登录状态下访问
    def test_detail_login(self):
        url = self.url + str(read_yaml("data.yaml", "blogId"))
        # print(f"这是url{url}")
        token = read_yaml("data.yaml","user_token_header")
        header = {
            "User-Token":token
        }
        print(f"这是header:{header}")
        res = Request().get(url=url,headers=header)
        validate(instance=res.json(), schema=self.schema)
        assert res.status_code == 200

    #错误的blogId
    @pytest.mark.parametrize("blogId",["","-1","0","a","123456789"])
    def test_detail_fail(self,blogId):
        url = self.url + blogId
        token = read_yaml("data.yaml","user_token_header")
        header = {
            "User-Token":token
        }
        res = Request().get(url=self.url,headers=header)

        