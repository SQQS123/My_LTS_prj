import requests
import pandas as pd
import numpy as np
from openai import OpenAI

# 最好把ip写入一个配置文件里，这里以本地部署的ollama为例进行尝试(兼容openai接口)
MODEL_SERVER_IP = '127.0.0.1'
MODEL_SERVER_PORT = '11434'


MODEL_SERVER_URL = f"http://{MODEL_SERVER_IP}:{MODEL_SERVER_PORT}"

MODEL_LIST_URL = f"{MODEL_SERVER_URL}/v1/models"
CHAT_API_URL = f"{MODEL_SERVER_URL}/v1/chat/completions"
IMG_API_URL = f"{MODEL_SERVER_URL}/v1/images/generations"
AUDIO_API_URL = f"{MODEL_SERVER_URL}/v1/audio/transcriptions"

GLOBAL_Client = OpenAI(
    api_key="ollama",  # 替换为您的 DeepSeek API 密钥
    base_url=f"{MODEL_SERVER_URL}/v1",  # 与openai兼容的url，eg http://localhost:11434/v1
)

def enum_models() -> dict:
    models_map = {}
    try:
        data = requests.get(MODEL_LIST_URL,timeout=3)
        data.raise_for_status()
        if data:
            # 列举MODEL_SERVER_IP上存在的所有model
            print(f"### 以下是{MODEL_SERVER_IP}存在的model ###")
            # print(data.json())
            i = 0
            for item in data.json()['data']:
                models_map[i] = item['id']
                i+=1
                print(item['id'])
            # print(models_map)
            return models_map
    except Exception as e:
        print(f"访问 {MODEL_LIST_URL} 失败，原因：{e}")

# 聊天
def chat():
    while True:
        question = input('请输入您的问题:')
        response = GLOBAL_Client.chat.completions.create(
            model="qwen3:4b",  # 指定模型名称
            messages=[
                # {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            stream=True
        )
        # print(f"{ip}-{model_name}:")
        # print(dir(response))
        # 实现流式输出
        response_content = ""
        for chunk in response:
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    response_content=response_content + content
                    print(content, end="", flush=True)
        print()

# 图像生成
def img_gen():
    pass

if __name__ == "__main__":
    enum_models()
    # chat()