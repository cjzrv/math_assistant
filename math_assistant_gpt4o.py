import json
import random
import openai
import os

# 設定 OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "Your API Key")  # ⚠️ 你可以直接在這裡填入 API Key
client = openai.OpenAI(api_key=OPENAI_API_KEY)

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

# 使用 OpenAI GPT-4o-mini 來處理對話
def chat_with_gpt(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        stream=True  # ✅ 啟用流式輸出
    )

    print("\n📖 GPT-4o-mini 回答：", end="", flush=True)
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")  # ✅ 確保輸出換行

# 主程式
if __name__ == "__main__":
    print("\n🎓 歡迎來到小學生數學輔助系統！")
    print("🔹 你可以輸入你的答案，GPT-4o-mini 會幫你檢查正確性。")
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

            # 讓 GPT-4o-mini 幫助判斷答案是否正確（流式輸出）
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages + [
                    {"role": "user", "content": f"這道題的正確答案是 {sample_question['answer']}。請判斷我的答案是否正確，並提供詳細解釋。"}
                ],
                temperature=0.2,
                stream=True
            )

            print("\n📖 GPT-4o-mini 判斷結果：", end="", flush=True)
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)
            print("\n")

            # 將 GPT-4o-mini 的回應加入對話上下文
            messages.append({"role": "assistant", "content": "GPT-4o-mini 判斷結果："})

            # 允許使用者繼續提問，並維持上下文
            while True:
                follow_up = input("\n💡 你還有其他問題嗎？(輸入問題或按 Enter 讓我出新題目)： ").strip()
                if follow_up == "":
                    break  # 讓系統出下一道題目
                else:
                    messages.append({"role": "user", "content": follow_up})  # ✅ 保留對話上下文
                    chat_with_gpt(messages)  # ✅ 使用上下文回答

    except (KeyboardInterrupt, EOFError):
        print("\n📚 感謝使用學習系統，再見！👋")
