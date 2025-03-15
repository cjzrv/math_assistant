import json
import random
import requests

# 設定 LM Studio API 參數
LM_API_URL = "http://localhost:1234/v1/chat/completions"  # 確保 LM Studio 正在運行
MODEL_NAME = "mistral-nemo-instruct-2407"  # 請更換為你的模型名稱（如 'mistral-7b.Q4_K_M.gguf'）

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

# 呼叫 LM Studio API 讓 LLM 判斷答案是否正確（支援流式輸出）
def check_answer_with_llm(question, correct_answer, user_answer, chat_history):
    prompt = f"""
    這是一道小學數學題目：
    問題：{question}

    學生輸入的答案是：{user_answer}
    正確答案應該是：{correct_answer}

    你的任務：
    1. 判斷學生的答案是否與正確答案相同，允許不同的單位（如「1.4米」和「1.4」）。
    2. 忽略答案中文與數字的差異，如5與五份應視為相同。
    3. 若答案正確，請回應：「✅ 你的答案正確！」。
    4. 若答案錯誤，請回應：「❌ 你的答案錯誤，正確答案是 {correct_answer}。」，並解釋該題應如何解題。
    """

    messages = [
        {"role": "system", "content": "你是一位小學數學老師，負責批改學生的答案並提供解釋。"},
        {"role": "user", "content": prompt}
    ]
    messages.extend(chat_history)  # ✅ 保持上下文

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.2,
        "stream": True  # ✅ 啟用流式輸出
    }

    with requests.post(LM_API_URL, json=payload, stream=True) as response:
        print("\n📖 LLM 判斷結果：", end="", flush=True)
        llm_response = ""

        for line in response.iter_lines():
            if line:
                try:
                    line = line.decode("utf-8").replace("data: ", "").strip()
                    data = json.loads(line)
                    content = data["choices"][0]["delta"].get("content", "")
                    print(content, end="", flush=True)
                    llm_response += content
                except json.JSONDecodeError:
                    continue

        print("\n")
    
    # ✅ 將這次的對話記錄加入 chat_history
    chat_history.append({"role": "user", "content": user_answer})
    chat_history.append({"role": "assistant", "content": llm_response})

# 主程式
if __name__ == "__main__":
    print("\n🎓 歡迎來到小學生數學輔助系統！")
    print("🔹 你可以輸入你的答案，LLM 會幫你檢查正確性。")
    print("🔹 如果有其他問題，也可以繼續提問！")
    print("🔹 按 `Ctrl+C` 或 `Ctrl+D` 退出程式。\n")

    try:
        while True:  # ✅ 允許多輪對話
            sample_question = get_random_question(data)
            print("\n📌 題目:", sample_question["question"])

            chat_history = []  # ✅ 每道題目重置歷史紀錄

            # 讓使用者輸入答案
            user_answer = input("✏️ 請輸入你的答案： ")

            # 讓 LLM 幫助判斷答案是否正確（流式輸出）
            check_answer_with_llm(
                sample_question["question"],
                sample_question["answer"],
                user_answer,
                chat_history
            )

            # 允許使用者繼續提問，並保持上下文
            while True:
                follow_up = input("\n💡 你還有其他問題嗎？(輸入問題或按 Enter 讓我出新題目)： ").strip()
                if follow_up == "":
                    break  # 讓系統出下一道題目
                else:
                    # ✅ 將對話上下文加回 LLM，保持連貫性
                    chat_history.append({"role": "user", "content": follow_up})

                    payload = {
                        "model": MODEL_NAME,
                        "messages": [
                            {"role": "system", "content": "你是一位小學數學老師，專門幫助學生學習。"}
                        ] + chat_history,
                        "temperature": 0.7,
                        "stream": True  # ✅ 啟用流式輸出
                    }

                    with requests.post(LM_API_URL, json=payload, stream=True) as response:
                        print("\n📖 LLM 回答：", end="", flush=True)
                        llm_response = ""

                        for line in response.iter_lines():
                            if line:
                                try:
                                    line = line.decode("utf-8").replace("data: ", "").strip()
                                    data = json.loads(line)
                                    content = data["choices"][0]["delta"].get("content", "")
                                    print(content, end="", flush=True)
                                    llm_response += content
                                except json.JSONDecodeError:
                                    continue

                        print("\n")

                    # ✅ 把 LLM 的回答加回 chat_history
                    chat_history.append({"role": "assistant", "content": llm_response})

    except (KeyboardInterrupt, EOFError):
        print("\n📚 感謝使用學習系統，再見！👋")
