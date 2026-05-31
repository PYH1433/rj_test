import os
import yaml

# 获取项目根目录下的 data 文件夹路径
BASE_PATH = os.path.join(os.getcwd(), "data")
if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)  # 不存在就自动创建，避免报错


# 追加写入 yaml
def write_yaml(filename, data):
    file_path = os.path.join(BASE_PATH, filename)
    with open(file_path, encoding="utf-8", mode="a") as f:
        yaml.safe_dump(data, stream=f, allow_unicode=True, sort_keys=False)


# 读取 yaml
def read_yaml(filename, key):
    file_path = os.path.join(BASE_PATH, filename)
    with open(file_path, encoding="utf-8", mode="r") as f:
        data = yaml.safe_load(f)
        return data[key]


# 清空 yaml
def clear_yaml(filename):
    file_path = os.path.join(BASE_PATH, filename)
    with open(file_path, encoding="utf-8", mode="w") as f:
        f.truncate()


# 更新 yaml（读-改-写，避免重复 key）
def update_yaml(filename, data_dict):
    file_path = os.path.join(BASE_PATH, filename)
    existing = {}
    try:
        with open(file_path, encoding="utf-8", mode="r") as f:
            content = f.read().strip()
            if content:
                existing = yaml.safe_load(content) or {}
    except FileNotFoundError:
        pass
    existing.update(data_dict)
    with open(file_path, encoding="utf-8", mode="w") as f:
        yaml.safe_dump(existing, stream=f, allow_unicode=True, sort_keys=False)