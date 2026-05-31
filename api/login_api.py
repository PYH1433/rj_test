from api.base_api import BaseApi
from utils.yaml_util import update_yaml


class LoginApi(BaseApi):
    def login(self, username, password):
        res = self.post("user/login", json={
            "userName": username,
            "password": password
        })
        if (
            res.status_code == 200
            and isinstance(res.json().get("data"), dict)
        ):
            token = res.json()["data"].get("token")
            if token:
                self._set_token(token)
                update_yaml("data.yaml", {"user_token_header": token})
        return res
