import os
import requests
from dotenv import load_dotenv

# 如果需要從 .env 檔案載入，請確保 .env 包含 HF_ACCESS_TOKEN
# HF_ACCESS_TOKEN=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
load_dotenv()

# 使用 Hugging Face Access Token
HF_ACCESS_TOKEN = os.getenv("HF_ACCESS_TOKEN", "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")
MODEL_NAME = "gpt2"

# Hugging Face Inference API URL
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

# 設置請求的標頭
HEADERS = {"Authorization": f"Bearer {HF_ACCESS_TOKEN}"}

def query_huggingface_api(payload):
    try:
        # 發送 POST 請求到 Inference API
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # 檢查是否有錯誤
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def main():
    # 測試訊息
    input_text = "Hello, how can I assist you today?"
    payload = {"inputs": input_text}

    # 查詢 Hugging Face API
    print("Querying Hugging Face API...")
    result = query_huggingface_api(payload)

    # 處理返回的資料
    if result:
        # 檢查回應是否是 list 格式
        if isinstance(result, list):
            # 取得第一個結果
            print(f"Model response: {result[0].get('generated_text', 'No response received')}")
        else:
            print(f"Model response: {result.get('generated_text', 'No response received')}")

if __name__ == "__main__":
    main()
