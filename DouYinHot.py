#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
import os
from datetime import datetime

# 定义固定的根目录
root_dir = "/data"
# 确保目录存在，如果不存在则创建
if not os.path.exists(root_dir):
    os.makedirs(root_dir)

# 获取当前日期，用于生成文件名
current_date = datetime.now().strftime("%Y-%m-%d")
file_name = f"DouYinHot_{current_date}.txt"
file_path = os.path.join(root_dir, file_name)  # 生成完整的文件路径

url = 'https://api.gumengya.com/Api/DouYinHot'
params = {
    'format': 'json',
}

try:
    response = requests.get(url, params=params)
    # 检查请求是否成功 (HTTP 状态码 200)
    if response.status_code == 200:
        try:
            res = response.json()
            # 状态码 200 表示请求成功
            if res.get('code') == '200':
                output = "请求成功: %s\n" % json.dumps(res, ensure_ascii=False, indent=4)
            else:
                output = "请求失败: %s\n" % json.dumps(res, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            output = "解析结果异常: %s\n" % e
    else:
        output = "请求异常, 状态码: %d\n" % response.status_code
except requests.RequestException as e:
    output = "请求发生异常: %s\n" % e

# 将输出结果按天保存到文件
with open(file_path, 'a', encoding='utf-8') as f:
    f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(output)
    f.write("\n" + "="*50 + "\n")  # 分隔符，方便阅读

print(f"输出已保存到文件: {file_path}")
