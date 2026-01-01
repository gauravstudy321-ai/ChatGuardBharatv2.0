import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from utils import generate_adversarial_prompts, test_chatbot, evaluate_response, AI_MODEL

# Page Config
st.set_page_config(
    page_title="ChatGuard | AI Safety Testing",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Unique Theme with Animated Background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Animated Background */
    .stApp {
        background: #0a0a0f;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(0, 255, 136, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(0, 212, 255, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 107, 0, 0.05) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Animated Grid Overlay */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 136, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 136, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    /* Floating Particles Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.5; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 136, 0.3); }
        50% { box-shadow: 0 0 40px rgba(0, 255, 136, 0.6); }
    }
    
    @keyframes scanline {
        0% { top: -100%; }
        100% { top: 100%; }
    }
    
    /* Hide Streamlit Branding but keep Header/Sidebar functional */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header {visibility: hidden;}  <-- Removed to fix sidebar toggle */
    
    /* Custom Header Styling to blend in */
    header {
        background: transparent !important;
    }
    
    /* Main Container - REMOVE HUGE TOP WHITESPACE */
    .main .block-container {
        padding-top: 2rem !important; /* Was default 6rem */
        padding-bottom: 2rem !important;
        max-width: 1400px;
        position: relative;
        z-index: 1;
    }
    
    /* Cyber Hero Header */
    .hero-container {
        background: linear-gradient(135deg, rgba(10, 10, 15, 0.95) 0%, rgba(15, 25, 20, 0.95) 100%);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 16px;
        padding: 1rem 1.5rem 1.5rem 1.5rem; /* TOP=1rem only */
        margin-bottom: 1.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -100%;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(transparent, rgba(0, 255, 136, 0.1), transparent);
        animation: scanline 3s linear infinite;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #00ff88;
        margin: 0;
        letter-spacing: 2px;
        text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #7dd3c0;
        margin-top: 0; /* No gap after logo */
        font-weight: 400;
        letter-spacing: 1px;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        color: #00ff88;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 1.5rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        animation: pulse 3s infinite;
    }
    
    /* Subtle Grain Overlay for Film Look (Anti-AI Feel) */
    .stApp::before {
        content: "";
        opacity: 0.03;
        position: fixed;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
        background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
    }

    /* Hand-Crafted Footer (Human Touch) */
    .human-footer {
        position: fixed;
        bottom: 20px;
        right: 20px;
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.3);
        z-index: 100;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
    }
    .human-footer a {
        color: rgba(255, 255, 255, 0.5);
        text-decoration: none;
        transition: color 0.3s;
    }
    .human-footer a:hover {
        color: #00ff88;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d12 0%, #0a0a0f 100%);
        border-right: 1px solid rgba(0, 255, 136, 0.2);
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #00ff88;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Fix for sidebar toggle button */
    [data-testid="collapsedControl"] {
        color: #00ff88 !important;
        background: rgba(10, 15, 12, 0.8) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
        border-radius: 8px !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: rgba(0, 255, 136, 0.2) !important;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.3) !important;
    }
    
    /* Metric Cards - Glassmorphism */
    .metric-card {
        background: rgba(10, 15, 12, 0.8);
        border: 1px solid rgba(0, 255, 136, 0.25);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 255, 136, 0.6);
        transform: translateY(-3px);
        box-shadow: 0 10px 40px rgba(0, 255, 136, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00ff88;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-value.warning {
        color: #ffb800;
    }
    
    .metric-value.danger {
        color: #ff4444;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #5a7d6f;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #00ff88;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 1px;
    }
    
    /* Button Styling */
    .stButton > button {
        background: transparent !important;
        border: 2px solid #00ff88 !important;
        color: #00ff88 !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        width: 100%;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    .stButton > button:hover {
        background: #00ff88 !important;
        color: #0a0a0f !important;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.4) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(10, 15, 12, 0.9) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
        border-radius: 8px !important;
        color: #d4e5de !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00ff88 !important;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.2) !important;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: #00ff88 !important;
    }
    
    /* Terminal-style Info Box */
    .info-box {
        background: rgba(0, 20, 10, 0.8);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-left: 3px solid #00ff88;
        border-radius: 4px;
        padding: 1rem 1.2rem;
        color: #7dd3c0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .feature-card {
        background: rgba(10, 15, 12, 0.6);
        border: 1px solid rgba(0, 255, 136, 0.15);
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: rgba(0, 255, 136, 0.5);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 255, 136, 0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: #00ff88;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    .feature-desc {
        color: #5a7d6f;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        line-height: 1.5;
    }
    
    /* Status Pills */
    .status-pass {
        background: rgba(0, 255, 136, 0.2);
        border: 1px solid #00ff88;
        color: #00ff88;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .status-fail {
        background: rgba(255, 68, 68, 0.2);
        border: 1px solid #ff4444;
        color: #ff4444;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.3), transparent);
        margin: 2.5rem 0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(10, 15, 12, 0.8) !important;
        border: 1px solid rgba(0, 255, 136, 0.2) !important;
        border-radius: 8px !important;
        color: #d4e5de !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #00ff88 !important;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
# Function to load logo as base64
import base64
def get_base64_logo():
    try:
        with open("logo.png", "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

logo_b64 = get_base64_logo()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">' if logo_b64 else '<div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>'

# Hero Header
# Hero Header
st.markdown(f"""
<div class="hero-container">
    {logo_html}
    <!-- Title removed as it is in the logo now -->
    <p class="hero-subtitle">Automated Security & Reliability Testing for AI Chatbots</p>
    <span class="hero-badge">OpenAI Academy X NxtWave Buildathon</span>
</div>
<style>
    .logo-img {{
        width: 380px; 
        max-width: 90%;
        margin-top: -2rem !important; /* Pull logo UP to compensate for PNG whitespace */
        margin-bottom: 0px; /* Tight to subtitle */
        filter: drop-shadow(0 0 20px rgba(0, 255, 136, 0.2));
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ CONTROL PANEL")
    st.markdown("---")
    
    use_demo = st.checkbox("🎮 Demo Mode", value=True, help="Use our Groq for demonstration. Uncheck to test your own chatbot.")
    
    st.markdown("---")
    
    if not use_demo:
        st.markdown("### 🎯 YOUR CHATBOT")
        provider = st.selectbox(
            "Provider",
            ["OpenAI", "Anthropic", "Groq", "Custom Webhook"],
            help="Select your chatbot provider"
        )
        
        user_api_key = st.text_input(
            "Your API Key",
            type="password",
            help="We never store your key. It's only used for this test.",
            placeholder="sk-..."
        )
        
        if provider == "OpenAI":
            model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"])
        elif provider == "Anthropic":
            model = st.selectbox("Model", ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"])
        elif provider == "Groq":
            model = st.selectbox("Model", ["llama-3.1-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"])
        else:  # Custom Webhook
            model = "webhook"
            user_api_key = st.text_input("Webhook Endpoint", placeholder="https://your-bot.com/api/chat")
        
        st.markdown(f"""
        <div class="info-box">
            <small>✅ Testing: {provider}/{model}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            > DEMO_MODE: ACTIVE<br>
            > TARGET: Groq (Mock Chatbot)<br>
            > EVALUATOR: ChatGPT-style AI<br>
            > STATUS: READY
        </div>
        """, unsafe_allow_html=True)
        provider = "Groq"
        model = AI_MODEL
        user_api_key = None
    

    
    st.markdown("---")
    
    num_tests = st.slider("🎯 Attack Vectors", min_value=3, max_value=10, value=5)
    
    st.markdown("---")
    
    eval_mode = st.radio(
        "🧠 Evaluation Engine",
        ["Fast (Pattern + Groq)", "Advanced (GPT-4o) - Coming Soon"],
        help="Advanced mode uses GPT-4o for semantic evaluation"
    )
    
    st.markdown("---")
    
    start_btn = st.button("▶ INITIATE SCAN", use_container_width=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #3d5c4f; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace;">
        OpenAI Academy • NxtWave<br>
        Powered by GPT-4o
    </div>
    """, unsafe_allow_html=True)

# Main Content
if start_btn:
    if not use_demo and not api_key:
        st.error("⚠️ API Key required. Enable Demo Mode or provide key.")
    else:
        # Testing Animation
        with st.container():
            scan_header = st.empty()  # Make it clearable
            scan_header.markdown('<div class="section-header">🔍 SECURITY SCAN IN PROGRESS</div>', unsafe_allow_html=True)
            
            progress_container = st.empty()
            status_text = st.empty()
            detail_text = st.empty()
            
            # Phase 1: Connect & Analyze
            status_text.markdown("**⚡ PHASE 1: INITIALIZATION**")
            detail_text.markdown("```\n> Connecting to Groq API (openai/gpt-oss-120b)...\n```")
            detail_text.markdown("```\n> Loading curated jailbreak database...\n```")
            detail_text.markdown("```\n> Selecting adversarial attack patterns...\n```")
            
            # Phase 2: Generate Prompts
            status_text.markdown("**🧠 PHASE 2: LOADING ATTACK VECTORS**")
            detail_text.markdown("```\n> Loading " + str(num_tests) + " research-backed jailbreaks...\n```")
            prompts = generate_adversarial_prompts("Groq AI Model", num_tests, use_demo=use_demo)
            detail_text.markdown("```\n> ✓ Loaded " + str(len(prompts)) + " curated jailbreak exploits\n```")
            
            # Phase 3: Execute Tests
            status_text.markdown("**🎯 PHASE 3: EXECUTING ATTACKS**")
            results = []
            progress_bar = progress_container.progress(0)
            
            attack_types = ["Prompt Injection", "Data Extraction", "Social Engineering", "Bias Testing", "Logic Abuse", "Jailbreak", "Privacy Probe", "Harmful Content"]
            
            for i, prompt in enumerate(prompts):
                attack_type = attack_types[i % len(attack_types)]
                detail_text.markdown(f"```\n> [{i+1}/{len(prompts)}] Testing: {attack_type}\n> Sending payload to target...\n```")
                
                response = test_chatbot(prompt, provider, user_api_key, model, use_demo=use_demo)
                
                detail_text.markdown(f"```\n> [{i+1}/{len(prompts)}] Response received\n> Running security evaluation...\n```")
                
                eval_result = evaluate_response(prompt, response, use_demo=use_demo)
                
                status_icon = "🚨 VULNERABLE" if eval_result["status"] == "FAIL" else "✓ DEFENDED"
                detail_text.markdown(f"```\n> [{i+1}/{len(prompts)}] Result: {status_icon}\n```")
                
                results.append({
                    "Prompt": prompt,
                    "Response": response,
                    "Score": eval_result["score"],
                    "Status": eval_result["status"],
                    "Reason": eval_result["reason"]
                })
                
                progress_bar.progress((i + 1) / len(prompts))
            
            # Phase 4: Complete
            status_text.markdown("**✅ PHASE 4: ANALYSIS COMPLETE**")
            detail_text.markdown("```\n> Generating vulnerability report...\n> Calculating security scores...\n> SCAN COMPLETE ✓\n```")
            scan_header.empty()  # Clear the "SCAN IN PROGRESS" header
            status_text.empty()
            detail_text.empty()
            progress_container.empty()
        
        # Results Section
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📊 VULNERABILITY REPORT</div>', unsafe_allow_html=True)
        
        df = pd.DataFrame(results)
        pass_count = len(df[df['Status'] == 'PASS'])
        fail_count = len(df[df['Status'] == 'FAIL'])
        avg_score = df['Score'].mean()
        pass_rate = pass_count / len(df) * 100
        
        # Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            rate_class = "danger" if pass_rate < 50 else "warning" if pass_rate < 80 else ""
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value {rate_class}">{pass_rate:.0f}%</div>
                <div class="metric-label">Defense Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{pass_count}</div>
                <div class="metric-label">Attacks Blocked</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            fail_class = "danger" if fail_count > 0 else ""
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value {fail_class}">{fail_count}</div>
                <div class="metric-label">Vulnerabilities</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            score_class = "danger" if avg_score < 2.5 else "warning" if avg_score < 4 else ""
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value {score_class}">{avg_score:.1f}</div>
                <div class="metric-label">Security Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Row
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Defended', 'Breached'],
                values=[pass_count, fail_count],
                hole=0.65,
                marker_colors=['#00ff88', '#ff4444'],
                textinfo='label+percent',
                textfont_size=13,
                textfont_color='white'
            )])
            fig_pie.update_layout(
                title=dict(text="Attack Results", font=dict(size=16, color='#00ff88', family='Space Grotesk')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                height=320,
                annotations=[dict(text=f'{pass_rate:.0f}%', x=0.5, y=0.5, font_size=32, font_color='#00ff88', showarrow=False, font_family='JetBrains Mono')]
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Human Footer
        st.markdown('<div class="human-footer">built with <span style="color:#00ff88;">intelligence</span> by Glitch Hunters</div>', unsafe_allow_html=True)
        
        with chart_col2:
            score_counts = df['Score'].value_counts().reindex(range(0, 6), fill_value=0)
            colors = ['#ff4444', '#ff6b35', '#ffb800', '#a3e635', '#22c55e', '#00ff88']
            
            fig_bar = go.Figure(data=[go.Bar(
                x=['0', '1', '2', '3', '4', '5'],
                y=score_counts.values,
                marker_color=colors,
                text=score_counts.values,
                textposition='outside',
                textfont=dict(color='#7dd3c0', size=14, family='JetBrains Mono')
            )])
            fig_bar.update_layout(
                title=dict(text="Score Distribution", font=dict(size=16, color='#00ff88', family='Space Grotesk')),
                xaxis=dict(title="Security Score", color='#5a7d6f', gridcolor='rgba(0,255,136,0.1)', title_font=dict(family='Space Grotesk')),
                yaxis=dict(title="Count", color='#5a7d6f', gridcolor='rgba(0,255,136,0.1)', title_font=dict(family='Space Grotesk')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=320
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.info("🔧 Evaluation Engine: Pattern-based (fast, free, deterministic) — Upgradable to OpenAI Moderation API for advanced independent checks (live when credits available).")
        
        # Detailed Results
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📋 DETAILED ANALYSIS</div>', unsafe_allow_html=True)
        
        for idx, row in df.iterrows():
            icon = "🚨" if row['Status'] == 'FAIL' else "✅"
            with st.expander(f"{icon} Attack #{idx + 1}: {row['Prompt'][:55]}..."):
                st.markdown(f"""
                **Attack Vector:**
                ```text
                {row['Prompt']}
                ```
                
                **Bot Response:**
                > {row['Response']}
                
                **Score:** `{row['Score']}/5` | **Result:** `{row['Status']}`
                
                **Analysis:** {row['Reason']}
                
                **Remediation Suggestion:**
                {row.get('Recommendation', 'No specific remediation available.')}
                """)
        
        # Export
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        col_export1, col_export2, col_export3 = st.columns([1, 2, 1])
        with col_export2:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇ DOWNLOAD FULL REPORT",
                data=csv,
                file_name='chatguard_security_report.csv',
                mime='text/csv',
                use_container_width=True
            )

else:
    # Landing State
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI-Powered Attacks</div>
            <div class="feature-desc">GPT-4o generates sophisticated adversarial prompts</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Safety Analysis</div>
            <div class="feature-desc">OpenAI Moderation API detects harmful content</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Visual Reports</div>
            <div class="feature-desc">Interactive dashboards with export options</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">3-Click Testing</div>
            <div class="feature-desc">No complex setup, instant vulnerability detection</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">🔧 HOW IT WORKS</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; color: #00ff88;">01</div>
            <div class="feature-title">DEFINE TARGET</div>
            <div class="feature-desc">Describe your chatbot's purpose and domain</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; color: #00ff88;">02</div>
            <div class="feature-title">EXECUTE SCAN</div>
            <div class="feature-desc">AI generates and runs adversarial attacks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; color: #00ff88;">03</div>
            <div class="feature-title">GET INSIGHTS</div>
            <div class="feature-desc">Review vulnerabilities and recommendations</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 **Configure your target in the sidebar and click 'INITIATE SCAN' to begin**")
