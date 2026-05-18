
from jsonschema.validators import validate
import re
import pytest
from utils.request_util import Request,host
from utils.yaml_util import *


@pytest.mark.order(1)
class TestLogin:
    url = host + "user/login"
    schema = {
        "type": "object",
        "required": ["code","errMsg","data"],
        "additionalProperties": False,
        "properties": {
            "code": {
            "type": "number"
            },
            "errMsg": {
            "type":["string", "null"]
            },
            "data": {
            "type": ["object", "null"],
            "required": [],
            "properties": {
                "id": {
                "type": "number"
                },
                "token": {
                "type": "string"
                }
            }
            }
        }
    }


    #异常登录
    @pytest.mark.parametrize("login",[
        #错误的账号和密码
        {
            "userName": "zhangsan1", 
            "password": "1234567",
            "errMsg": "用户不存在"
        },
        #错误的账号，正确的密码
        {
            "userName": "xxxxx", 
            "password": "123456",
            "errMsg": "用户不存在"
        },
        #正确的账号，错误的密码
         {
            "userName": "zhangsan", 
            "password": "1234567",
            "errMsg": "密码不正确"
        },
        #不存在的账号
         {
            "userName": "xxxxx", 
            "password": "xxxxx",
            "errMsg": "用户不存在"
        },
        #账号密码为空
         {
            "userName": "", 
            "password": "",
            "errMsg": ["参数不合法:用户名不能为空","参数不合法:密码不能为空"],
        },
        #输入过长的账号
         {
            "userName": "这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号这是一个很长的账号的账号",
            "password": "1234567",
            "errMsg": "参数不合法:用户名长度不能超过20",
        },
        #输入过长的密码
         {
            "userName": "zhangsan", 
            "password": "这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码这是一个很长的密码的密码",
            "errMsg": "参数不合法:用户名长度不能超过20",
        }
    ])
    def test_login_fail(self,login):
        data = {
            "userName": login["userName"], 
            "password": login["password"]
        }
        res = Request().post(url=self.url, json=data)
        validate(instance=res.json(), schema=self.schema)
        assert res.json()["code"] == -1
        assert res.json()["errMsg"] in login["errMsg"]

    #正常登录
    @pytest.mark.parametrize("login",[
        {"userName": "zhangsan", "password": "123456"},
        {"userName": "lisi", "password": "123456"}
    ])
    def test_login_success(self,login):
        data = {
            "userName": login["userName"], 
            "password": login["password"]
        }
        res = Request().post(url=self.url, json=data)
        validate(instance=res.json(), schema=self.schema)
        assert res.json()["code"] == 200
        assert re.match(r'\S{100,}',res.json()["data"]["token"])


        token = {
            "user_token_header" : res.json()["data"]["token"]
        }
        write_yaml("data.yaml", token)
