# ChatGuard - OpenAI Academy x NxtWave Buildathon Submission

## 1. Problem Statement
**Who is affected:** Enterprises, startups, and developers deploying AI chatbots in high-stakes industries (Finance, Healthcare, Customer Support).

**The Problem:**
As companies rush to deploy AI with **RAG (Retrieval-Augmented Generation)**, they are blindly trusting foundation models. However, adding custom data and System Prompts introduces new, invisible vulnerabilities.
- **Data Exfiltration:** Attackers can trick bots into revealing private RAG documents.
- **Jailbreaks:** Techniques like "Roleplay" (e.g., the 'PWF' attack) can bypass safety filters.
- **Reputational Risk:** A single toxic response can destroy user trust.

Currently, **Red Teaming** (security testing) is manual, slow, and costs $10k-$50k per audit. Developers need an automated way to "crash test" their AI before deployment.

## 2. Our Solution
**ChatGuard** is an **Automated Red Teaming Platform** that stress-tests AI chatbots before they go live.

**How it works:**
1.  **Universal Connectivity:** Users connect their chatbot via **API Key** (OpenAI/Anthropic) or **Webhook** (for RAG testing).
2.  **Attack Simulation:** The system launches a barrage of 20+ research-backed adversarial attacks (Prompt Injection, Social Engineering, Logic Bombs).
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
-   **AI Integration:** Unified Interface Pattern supporting OpenAI, Anthropic, HuggingFace, and Groq SDKs.

**Implementation Status:**
-   **Functional Prototype:** Live demo available showing end-to-end attack simulation.
-   **Scalability:** Stateless architecture allowing for infinite horizontal scaling.
-   **Visuals:** Custom CSS Cyberpunk UI with real-time attack visualization.

**Demo Highlights:**
-   **Real-time Attack:** Watch ChatGuard generate a "PWF (Playing with Fire)" jailbreak.
-   **Real-time Failure:** See the target model comply with the attack.
-   **Real-time Detection:** See the AI Judge flag the compliance instantly.

---
*Built with ❤️ by [Glenn Sharma] for the OpenAI Academy x NxtWave Buildathon.*
