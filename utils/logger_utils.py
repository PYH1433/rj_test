import logging
import os
import time

# 过滤器：只输出 INFO 级别日志
class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

# 过滤器：只输出 ERROR 级别日志
class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR

# 日志工具类（单例）
class Logger:
    logger = None

    @classmethod
    def getlog(cls):
        """
        将日志保存到指定路径
        按天分文件：总日志、info日志、error日志
        """
        if cls.logger is None:
            # 创建日志器
            cls.logger = logging.getLogger(__name__)
            cls.logger.setLevel(logging.DEBUG)
            cls.logger.handlers.clear()  # 避免重复添加handler

            # 日志目录
            LOG_PATH = "logs/"
            if not os.path.exists(LOG_PATH):
                os.mkdir(LOG_PATH)

            # 按天生成日志文件名
            now = time.strftime("%Y-%m-%d")
            log_name = os.path.join(LOG_PATH, f"{now}.log")          # 总日志
            info_log_name = os.path.join(LOG_PATH, f"{now}_info.log") # 仅info
            error_log_name = os.path.join(LOG_PATH, f"{now}_error.log") # 仅error

            # 1. 总日志 handler（记录 INFO 及以上）
            handler = logging.FileHandler(log_name, encoding="utf-8")
            handler.setLevel(logging.INFO)

            # 2. INFO 日志 handler（只记录 INFO）
            info_handler = logging.FileHandler(info_log_name, encoding="utf-8")
            info_handler.setLevel(logging.INFO)
            info_handler.addFilter(InfoFilter())

            # 3. ERROR 日志 handler（只记录 ERROR）
            error_handler = logging.FileHandler(error_log_name, encoding="utf-8")
            error_handler.setLevel(logging.ERROR)
            error_handler.addFilter(ErrorFilter())



            # ========== 新增：控制台输出 handler ==========
            console_handler = logging.StreamHandler()  # 控制台


            # 日志格式
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"
            )

            # 设置格式
            handler.setFormatter(formatter)
            info_handler.setFormatter(formatter)
            error_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # 添加 handler
            cls.logger.addHandler(handler)
            cls.logger.addHandler(info_handler)
            cls.logger.addHandler(error_handler)
            # cls.logger.addHandler(console_handler) 

        return cls.logger


