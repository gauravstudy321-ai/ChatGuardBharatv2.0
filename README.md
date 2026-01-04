# 🛡️ ChatGuard | Automated Red Teaming Platform

> **Automated Security & Reliability Testing for AI Chatbots**

![Status](https://img.shields.io/badge/Status-Functional_Prototype-00ff88?style=for-the-badge)
![Tech](https://img.shields.io/badge/Tech-Streamlit%20|%20OpenAI%20|%20Python-blue?style=for-the-badge)

## 🚨 The Problem
Adding **RAG (Retrieval Augmented Generation)** and custom **System Prompts** to LLMs introduces critical vulnerabilities. Attackers can trick chatbots into:
- Revealing private documents (Data Exfiltration)
- Ignoring safety guidelines (Jailbreaking)
- Generating toxic content

Manual "Red Teaming" (security testing) costs **$10k-$50k** and takes weeks.

## ⚡ The Solution
**ChatGuard** is a real-time security auditor that stress-tests your chatbot before deployment. It launches 45+ research-backed attacks across 12 categories and uses an **AI Judge** to verify safety.

### Key Features
- **🧪 Multi-Provider Support:** Test models from OpenAI, Anthropic, HuggingFace, and Groq.
- **🧠 AI Judge:** Uses Llama-3.3 (via Groq) to semantically analyze responses (regex is dead).
- **🎭 White-Box Mode:** Developers input their **API Key & System Prompt** for rapid logical testing (Local/Dev).
- **🔒 Black-Box Mode (Enterprise):** Companies use **Webhook Testing** to test deployed bots without sharing API keys.
- **📊 Real-time Dashboard:** Cyberpunk UI with live attack visualization and grading.
- **👤 User Accounts:** Secure login/signup system with history tracking.
- **💾 Scan History:** Save and compare past audit reports to track improvements.

## 🚀 Setup & Usage

### 1. Installation
```bash
git clone https://github.com/gauravstudy321-ai/chatguard.git
cd chatguard
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

### 3. Usage
1.  **Login/Signup:** Create an account to access your personalized dashboard.
2.  **Select Target:** Choose OpenAI, Anthropic, or Custom Webhook.
2.  **Configure:** Enter API Key and **System Prompt** (e.g., "You are a helpful assistant...").
3.  **Scan:** Click `INITIATE SCAN`. ChatGuard will verify your bot against known exploits.
4.  **Analyze:** Review the **Pass/Fail** matrix and detailed **AI Judge** reasoning.

## 🛠️ Tech Stack
-   **Frontend:** Streamlit
-   **Core Logic:** Python
-   **Database:** SQLite (Embedded User & Scan History Persistence)
-   **Integrations:** OpenAI SDK, Anthropic SDK, Groq SDK, HuggingFace
-   **Evaluation:** Llama-3.3-70b (via Groq)

---
*Built for the OpenAI Academy x NxtWave Buildathon.*
