import requests
import json
import os

# 读取标题txt文件
with open("D:\\1637.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    # lines = lines[9:]

# 定义接口地址
api_url = 'http://127.0.0.1:7861/chat/chat'
# 保存处理结果的文件夹
output_folder = "D:\\txt"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 处理每一行
for index, line in enumerate(lines):
    # 清理行末尾的换行符
    line = line.strip()

    # 构建请求体
    data = {
        "query": line + "。根据前面的文章标题扩写文章内容，字数1000字",
        "conversation_id": "",
        "history_len": -1,
        "history": [
        ],
        "stream": False,
        "model_name": "Qwen-1_8B-Chat",
        "temperature": 0.7,
        "max_tokens": 2048,
        "prompt_name": "default"
    }

    # 发送请求
    try:
        response = requests.post(api_url, json=data)
        print(response)
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        continue

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        continue

    # 尝试获取JSON响应
    try:
        for llm_line in response.iter_lines():
            if llm_line.strip():  # 如果行不为空
                if llm_line.startswith(b'data:'):  # 如果是数据行
                    data = llm_line[len(b'data:'):].strip()  # 去除"data:"前缀和空白字符
                    try:
                        result = json.loads(data.decode('utf-8'))  # 尝试解析JSON数据
                        # 在这里处理json_data
                        print(result)
                        # 保存结果
                        with open(f"{output_folder}/{line}.txt", "w", encoding="utf-8") as result_file:
                            result_file.write(result.get("text", ""))
                    except json.JSONDecodeError:
                        # 如果解析失败，说明可能是ping包或其他非JSON数据，可以忽略
                        pass
        # result = response.json()
    except json.JSONDecodeError:
        print(f"Error decoding JSON response for line {line}")
        continue



print("处理完成")
