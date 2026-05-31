from api.base_api import BaseApi


class UserApi(BaseApi):
    def get_user_info(self, user_id, no_auth=False):
        return self.get("user/getUserInfo", params={"userId": user_id}, no_auth=no_auth)

    def get_author_info(self, blog_id, no_auth=False):
        return self.get("user/getAuthorInfo", params={"blogId": blog_id}, no_auth=no_auth)
