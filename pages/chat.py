"""
ChatGuard - Live Chat Debugger
A separate page for testing the AI connection directly.
"""
import streamlit as st
from utils import simple_chat, GROQ_AVAILABLE, AI_MODEL

st.set_page_config(
    page_title="ChatGuard | Live Chat",
    page_icon="💬",
    layout="wide"
)

# Apply same dark theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0f0c 0%, #0d1410 50%, #0a0f0c 100%);
        color: #e0e0e0;
    }
    .stChatMessage {
        background: rgba(10, 15, 12, 0.8) !important;
        border: 1px solid rgba(0, 255, 136, 0.2) !important;
        border-radius: 12px !important;
    }
    .stChatInput > div > div > input {
        background: rgba(10, 15, 12, 0.9) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
        color: #00ff88 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #00ff88; font-family: 'Space Grotesk', sans-serif;">💬 LIVE CHAT DEBUGGER</h1>
    <p style="color: #5a7d6f;">Direct Connection Test: Groq Llama-3.3-70b (High-Speed Inference)</p>
</div>
""", unsafe_allow_html=True)

# Status display
if GROQ_AVAILABLE:
    st.success(f"✅ Connected to Groq API | Model: `{AI_MODEL}`")
else:
    st.error("❌ Groq SDK not available. Please install it with `pip install groq`")

st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Say something to the AI..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... 🤔")
        
        # CALL THE NEW UTILS FUNCTION
        full_response = simple_chat(prompt)
        
        message_placeholder.markdown(full_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
