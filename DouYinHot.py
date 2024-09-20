import os
import requests
import json
from datetime import datetime

# 获取钉钉机器人 Webhook access_token，从环境变量读取
access_token = os.getenv('DINGTALK_ACCESS_TOKEN')
if not access_token:
    raise ValueError("钉钉机器人 access_token 未设置")

dingtalk_webhook = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')

# 创建 data 目录，如果它不存在
output_dir = os.path.join(os.getcwd(), "data")
os.makedirs(output_dir, exist_ok=True)  # 直接创建目录，如果已存在则不报错

# 指定文件路径
output_file = os.path.join(output_dir, f"{current_date}.md")

# 请求数据
orig = 'DouYin'  # 如需改成抖音就填DouYin，以此类推
url = f'https://api.gumengya.com/Api/{orig}Hot?format=json'
resp = requests.get(url)

data = json.loads(resp.text)
news = ""

# 添加表格标题行
news += "| **Title** | **链接** |\n"
news += "| ----- | ---- |\n"

# 遍历所有新闻项，并生成表格内容
for item in data['data']:
    news += f"| {item['title']} | [链接]({item['url']}) |\n"

# 将结果保存到文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(news)

print(f"新闻已保存至: {output_file}")

# 读取文件内容
with open(output_file, 'r', encoding='utf-8') as f:
    file_content = f.read()

# 钉钉机器人发送消息
def send_to_dingtalk(content):
    headers = {
        "Content-Type": "application/json"
    }
    json_data = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"今日热点新闻 {current_date}",
            "text": content
        }
    }
    response = requests.post(dingtalk_webhook, headers=headers, json=json_data)
    if response.status_code == 200:
        print("消息已发送至钉钉")
    else:
        print(f"发送失败，状态码: {response.status_code}, 响应: {response.text}")

# 调用函数发送消息
send_to_dingtalk(file_content)
