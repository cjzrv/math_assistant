# 🧮 AI Math Assistant Bot

This is an **AI-powered math assistant chatbot** that helps with:
- **Randomly selecting math problems** to test your skills (based on the Ape210K dataset 📚)
- **Checking your answers** and providing detailed explanations 🤖
- **Allowing follow-up questions**, keeping conversation context for a smooth learning experience 💬
- **Supporting multiple LLM options (Ollama, LM Studio, GPT-4o-mini)** for both **local and cloud-based AI** 🔥

[Chinese README](./README_CN.md)

---

## 🚀 Supported LLM Deployment Options
| LLM Deployment  | Works Offline | Requires API Key | How It Runs |
|---------------|--------------|--------------|--------------|
| **Ollama** 🖥️ | ✅ Yes | ❌ No | Runs locally using Ollama's LLM models |
| **LM Studio** 💻 | ✅ Yes | ❌ No | Requires LM Studio with API enabled at `http://localhost:1234` |
| **GPT-4o-mini** 🌐 | ❌ No | ✅ Yes | Uses OpenAI API for cloud-based LLM |

> **Choose the deployment option that fits your needs!**

---

## 🛠️ Installation & Setup
### **1️⃣ Choose an LLM Deployment Option**
Select either **Ollama (Local)**, **LM Studio (Local)**, or **GPT-4o-mini (Cloud-based)**.

---

### **2️⃣ Install Dependencies**
For **GPT-4o-mini**, install:
```bash
pip install requests openai
```
For **LM Studio**, install:
```bash
pip install requests
```

---

### **3️⃣ Download Math Dataset**
We use **Ape210K**, a large-scale math problem dataset:
```bash
wget -O ape210k_test.json "https://your-link-to-json-file.com/ape210k_cleaned.json"
```
Ensure `ape210k_test.json` is present in your project directory.

---

### **4️⃣ Run Different Versions**
#### ✅ **Ollama Local LLM**
1. **Install Ollama**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
   Windows users can download it from [Ollama's official website](https://ollama.com/).

2. **Download an LLM Model**
   ```bash
   ollama pull hf.co/bartowski/Mistral-Nemo-Instruct-2407-GGUF:Q4_K_M  # or use llama3, gemma
   ```

3. **Run the Ollama Version**
   ```bash
   python math_assistant_ollama.py
   ```

---

#### ✅ **LM Studio Local LLM**
1. **Download & Install [LM Studio](https://lmstudio.ai/)**
2. **Enable API in LM Studio**
   - Go to **Settings**
   - Enable **Local API Server**
   - Default API endpoint: `http://localhost:1234`
3. **Run the LM Studio Version**
   ```bash
   python math_assistant_lm_studio.py
   ```

---

#### ✅ **GPT-4o-mini (Cloud-Based OpenAI API)**
1. **Sign up for an OpenAI API key**
   - Register at [OpenAI API](https://platform.openai.com/signup/)
2. **Set your API key**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
3. **Run the GPT-4o-mini Version**
   ```bash
   python math_assistant_gpt4o.py
   ```

---

## 🖥️ Usage
Once the program is running, you will see:
```
🎓 Welcome to the AI Math Assistant Bot!
🔹 Enter your answer, and the AI will check its correctness.
🔹 Ask additional questions if needed!
🔹 Press `Ctrl+C` or `Ctrl+D` to exit.

📌 Problem: Jim is 1 meter and 2 decimeters tall. Tim's height is 8 decimeters less than twice Jim's height. What is their average height?
✏️ Enter your answer: 1.4 meters

📖 AI Response:
✅ Correct answer!

💡 Do you have any other questions? (Enter a question or press Enter for a new problem): How do you solve this?

📖 AI Response:
Step-by-step explanation...
(streaming output)
```
> 📌 **The AI will remember the conversation context and provide relevant responses!**

---

## 📜 License
This project is licensed under the **MIT License**, allowing free use and modification while crediting the original authors.

---

## ❤️ Acknowledgments
- [Ollama](https://ollama.com/) for local LLM execution
- [LM Studio](https://lmstudio.ai/) for local AI deployment
- [OpenAI](https://openai.com/) for GPT-4o-mini API support
- [Ape210K](https://github.com/Chenny0808/ape210k) for the open-source math dataset
- [Mistral AI](https://mistral.ai/) for open LLM models
