import requests
from utils.logger_utils import Logger

host = "http://47.108.157.13:8090/"

class Request:
    def __init__(self):
        self.logger =  Logger.getlog()
     # 发起 get 请求
    def get(self, url, **kwargs):
        self.logger.info('准备开始发起 get 请求,url:' + url)
        self.logger.info('接口信息是：{}'.format(kwargs))
        s = requests.get(url, **kwargs)
        self.logger.info('接口响应状态码：{}'.format(s.status_code))
        self.logger.info('接口响应内容是：{}'.format(s.text))
        return s

    # 发起post请求
    def post(self, url, **kwargs):
        self.logger.info('准备开始发起 post 请求,url:' + url)
        self.logger.info('接口信息是：{}'.format(kwargs))
        s = requests.post(url, **kwargs)
        self.logger.info('接口响应状态码：{}'.format(s.status_code))
        self.logger.info('接口响应内容是：{}'.format(s.text))
        return s
        
        
        

