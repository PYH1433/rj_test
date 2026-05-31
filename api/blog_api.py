from api.base_api import BaseApi


class BlogApi(BaseApi):
    def get_list(self, no_auth=False):
        return self.get("blog/getList", no_auth=no_auth)

    def get_detail(self, blog_id, no_auth=False):
        return self.get("blog/getBlogDetail", params={"blogId": blog_id}, no_auth=no_auth)

    def add_blog(self, user_id, title, content, no_auth=False):
        return self.post("blog/addBlog", json={
            "userId": user_id,
            "title": title,
            "content": content
        }, no_auth=no_auth)
