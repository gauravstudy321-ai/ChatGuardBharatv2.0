# ChatGuard - OpenAI Academy x NxtWave Buildathon Submission

## 1. Problem Statement
**The Problem: Custom AI Chatbots break easily.**

Developers are building chatbots for specific jobs (like "Customer Support" or "Medical Advice") using models like GPT-4. They assume that if they write a rule like "Don't be rude," the AI will follow it.

**The Reality:**
It is surprisingly easy for users to bypass these rules using "Jailbreaks."
1.  **Roleplay Attacks:** A user can trick the bot by saying "Act as a movie character who ignores rules."
2.  **Bad Advice:** A breached bot might give harmful instructions or leak private instructions.
3.  **Manual Testing is Hard:** Currently, developers have to manually type in these attacks one by one to check if their bot is safe. This is slow and they often miss new types of tricks.

**The Need:** Developers need a tool that automatically tries these attacks and reports if the bot is safe or not.

## 2. Our Solution
**ChatGuard** is an **Automated Red Teaming Platform** that stress-tests AI chatbots before they go live.

**How it works:**
1.  **Universal Connectivity:** Users connect their chatbot via **API Key** (OpenAI/Anthropic) or **Webhook** (for RAG testing).
2.  **Attack Simulation:** The system launches a barrage of 45+ research-backed adversarial attacks across 12 categories (Prompt Injection, Social Engineering, Logic Bombs, etc.).
3.  **Simulation Layer:** We simulate the user's **System Prompt** intent to audit their specific safety instructions.
4.  **AI Judge Evaluation:** A secondary LLM acts as a "Security Auditor," semantically analyzing responses to catch subtle failures that regex misses.
5.  **Actionable Reporting:** Generates a pass/fail matrix and remediation advice.

**Unique Value:**
- **White Box Testing:** Users can test their raw System Prompts.
- **Black Box Testing:** Enterprise-grade Webhook testing for privacy preservation.
- **Cross-Provider:** Benchmarks GPT-4o vs. Claude vs. Llama side-by-side.

## 3. Use of OpenAI APIs
ChatGuard is architected as an **OpenAI-native tool**:

-   **OpenAI SDK Standard:** The entire backend uses the OpenAI SDK format for maximum compatibility.
-   **GPT-4o (Target Testing):** The system is optimized to audit GPT-4o's specific vulnerabilities (e.g., system prompt overriding).
-   **Future Integration - OpenAI Moderation API:** Roadmap includes integrating the Moderation endpoint as a "First Line of Defense" filter in our evaluation pipeline.
-   **Future Integration - GPT-4o as Judge:** The "Advanced Mode" is designed to plug in GPT-4o as the ultimate, high-reasoning security judge for complex enterprise audits.

## 4. Feasibility & Tech Stack
**Architecture:**
-   **Frontend:** Streamlit (Python-based reactive UI) for rapid visualization.
-   **Backend Logic:** Python modular architecture (`providers.py`, `utils.py`).
-   **Backend Logic:** Python modular architecture (`providers.py`, `utils.py`).
-   **User Management:** Secure auth system with SQLite history tracking.
-   **AI Integration:** Unified Interface Pattern supporting OpenAI, Anthropic, HuggingFace, and Groq SDKs.

**Implementation Status:**
-   **Functional Prototype:** Live demo available showing end-to-end attack simulation.
-   **Scalability:** Stateless architecture allowing for infinite horizontal scaling.
-   **Visuals:** Custom CSS Cyberpunk UI with real-time attack visualization.


**Demo Highlights:**
-   **Real-time Attack:** Watch ChatGuard generate a "PWF (Playing with Fire)" jailbreak.
-   **Real-time Failure:** See the target model comply with the attack.
-   **Real-time Detection:** See the AI Judge flag the compliance instantly.

## 5. Judging Criteria Checklist (100% Coverage)
We have addressed every requirement:

1.  **Deployment (25%):** Ready for Streamlit Cloud (Github-connected) or Docker.
2.  **AI Integration (25%):** Deep integration with OpenAI GPT-4o SDK and Groq (Llama-3).
3.  **Problem Relevance (10%):** Solves the urgent "Blind Trust" crisis in Enterprise AI.
4.  **UI/UX (10%):** Interactive "Cyberpunk" interface with real-time feedback.
5.  **Responsiveness (10%):** Mobile-friendly Streamlit layout.
6.  **Data Persistence (10%):** Users can **Track History** via personalized accounts and **Export Reports** (CSV/JSON).
7.  **Data Security (10%):** "Black Box Mode" ensures zero API key leakage, plus **Secure SHA-256 Auth**.

---
*Built with ❤️ by [Glenn Sharma] for the OpenAI Academy x NxtWave Buildathon.*
