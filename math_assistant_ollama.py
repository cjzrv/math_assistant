import json
import random
import requests

# 設定 Ollama API 參數
OLLAMA_API_URL = "http://localhost:11434/api/chat"  # ✅ Ollama API 預設端口
MODEL_NAME = "hf.co/bartowski/Mistral-Nemo-Instruct-2407-GGUF:Q4_K_M"  # ✅ 可以更換為你下載的模型，如 'llama3', 'gemma'

# 讀取標準 JSON 格式的 Ape210K 題庫
with open("ape210k_test.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 隨機選擇一道題目
def get_random_question(data):
    question = random.choice(data)
    return {
        "question": question["original_text"],
        "answer": question["ans"],
        "equation": question["equation"]
    }

# 使用 Ollama API 來處理對話（支援流式輸出）
def chat_with_ollama(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": True  # ✅ 啟用流式輸出
    }

    response = requests.post(OLLAMA_API_URL, json=payload, stream=True)

    print("\n📖 Ollama 回答：", end="", flush=True)
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                content = data["message"]["content"]
                print(content, end="", flush=True)
            except json.JSONDecodeError:
                continue  # ✅ 忽略無效的 JSON 行
    print("\n")  # ✅ 確保輸出換行

# 主程式
if __name__ == "__main__":
    print("\n🎓 歡迎來到小學生數學輔助系統！")
    print("🔹 你可以輸入你的答案，Ollama 會幫你檢查正確性。")
    print("🔹 如果有其他問題，也可以繼續提問！")
    print("🔹 按 `Ctrl+C` 或 `Ctrl+D` 退出程式。\n")

    try:
        while True:  # ✅ 允許多輪對話
            sample_question = get_random_question(data)
            print("\n📌 題目:", sample_question["question"])

            # 初始化對話上下文
            messages = [
                {"role": "system", "content": "你是一位小學數學老師，負責批改學生的答案並提供解釋。"},
                {"role": "user", "content": f"這是一道小學數學題目：{sample_question['question']}"},
            ]

            # 讓使用者輸入答案
            user_answer = input("✏️ 請輸入你的答案： ")

            # 加入學生的回答
            messages.append({"role": "user", "content": f"我的答案是：{user_answer}"})

            # 讓 Ollama 幫助判斷答案是否正確（流式輸出）
            messages.append({"role": "user", "content": f"這道題的正確答案是 {sample_question['answer']}。請判斷我的答案是否正確，並提供詳細解釋。"})

            chat_with_ollama(messages)  # ✅ 使用 Ollama API 回答問題

            # 允許使用者繼續提問，並維持上下文
            while True:
                follow_up = input("\n💡 你還有其他問題嗎？(輸入問題或按 Enter 讓我出新題目)： ").strip()
                if follow_up == "":
                    break  # 讓系統出下一道題目
                else:
                    messages.append({"role": "user", "content": follow_up})  # ✅ 保留對話上下文
                    chat_with_ollama(messages)  # ✅ 使用上下文回答

    except (KeyboardInterrupt, EOFError):
        print("\n📚 感謝使用學習系統，再見！👋")
