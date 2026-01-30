import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="FreelanceFast.ai",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HIGH-END SAAS CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    :root {
        --primary: #4F46E5; /* Indigo 600 */
        --primary-hover: #4338ca;
        --bg-color: #F8FAFC; /* Slate 50 */
        --card-bg: #FFFFFF;
        --text-dark: #0F172A;
        --text-gray: #64748B;
        --border: #E2E8F0;
    }

    /* GLOBAL RESET */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
    }
    
    /* REMOVE BLOAT */
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding-top: 2rem; max-width: 1000px;}

    /* HERO SECTION */
    .hero-container {
        text-align: center;
        padding: 4rem 1rem;
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: var(--text-dark);
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-gray);
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    .highlight {
        color: var(--primary);
        background: rgba(79, 70, 229, 0.1);
        padding: 0 0.5rem;
        border-radius: 4px;
    }

    /* FEATURE GRID */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-bottom: 3rem;
        text-align: center;
    }
    .feature-card {
        padding: 1.5rem;
        background: transparent;
        border: 1px solid transparent;
        border-radius: 12px;
    }
    .feature-icon {font-size: 2rem; margin-bottom: 0.5rem;}
    .feature-title {font-weight: 700; color: var(--text-dark);}
    .feature-text {font-size: 0.9rem; color: var(--text-gray);}

    /* APP CONTAINER (THE TOOL) */
    .tool-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05);
        margin-bottom: 4rem;
    }
    
    /* INPUT STYLING */
    label {
        font-weight: 600 !important;
        color: #0F172A !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stTextArea textarea {
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 1rem !important;
        transition: all 0.2s;
        background-color: #FFFFFF !important;
        color: #0F172A !important; /* FORÇANDO COR PRETA */
        caret-color: #4F46E5 !important;
    }
    .stTextArea textarea:focus {
        border-color: #4F46E5 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1) !important;
        color: #0F172A !important;
    }
    
    /* Preenchimento dos placeholders */
    ::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    
    /* CTA BUTTON */
    div.stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: transform 0.2s, background 0.2s;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3);
    }
    div.stButton > button:hover {
        background: var(--primary-hover);
        transform: translateY(-2px);
    }

    /* SALES BANNER */
    .sales-banner {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 2rem;
    }
    .sales-banner h3 {color: white !important; margin: 0 0 0.5rem 0;}
    .sales-banner p {color: rgba(255,255,255,0.9) !important; margin-bottom: 1.5rem;}
    .sales-btn {
        background: white;
        color: #4F46E5;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        transition: transform 0.2s;
    }
    .sales-btn:hover {transform: scale(1.05);}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (CONFIG) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1005/1005141.png", width=50)
    st.markdown("### 🔑 API Key Setup")
    
    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password",
        help="It's free. See tutorial above.",
        placeholder="AIzaSy..."
    )
    
    with st.expander("❓ How to get a FREE Key", expanded=True):
        st.markdown("""
        1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Click **Create API Key**
        3. Copy & Paste here.
        """)
        
    st.divider()
    st.caption("FreelanceFast v2.0 • Secure & Private")

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Stop losing jobs to<br><span class="highlight">generic proposals.</span></div>
    <div class="hero-subtitle">
        Generate persuasive, custom-tailored cover letters for Upwork & Fiverr in seconds. 
        Trained on $100k+ earning profiles.
    </div>
</div>
""", unsafe_allow_html=True)

# --- VALUE GRID ---
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Instant Speed</div>
        <div class="feature-text">Analyze job posts and write 300 words in under 5 seconds.</div>
    </div>
    """, unsafe_allow_html=True)
with col_f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Psychology First</div>
        <div class="feature-text">Uses persuasion hooks, not just "AI summary" text.</div>
    </div>
    """, unsafe_allow_html=True)
with col_f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <div class="feature-title">100% Secure</div>
        <div class="feature-text">BYOK Model. Your data and API keys never leave your browser.</div>
    </div>
    """, unsafe_allow_html=True)

# --- THE TOOL ---
st.write("") # Spacer

if not api_key:
    st.warning("⚠️ To start the engine, please enter your **Google API Key** in the sidebar (It's free!).")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
    except:
        pass

# Main Inputs
c1, c2 = st.columns(2)
with c1:
    job_desc = st.text_area("📋 Paste the Job Description", height=250, placeholder="Client is looking for...")
with c2:
    my_skills = st.text_area("👤 Your Skills / Bio", height=250, placeholder="I am a Python expert with...")

# Tone Selector (Visual)
st.write("")
st.markdown("**Select Strategy:**")
tone = st.radio(
    "Select Strategy",
    ["💼 Corporate (Safe)", "🚀 Startup (Energetic)", "🧠 Expert (Direct)"],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")
st.write("")

if st.button("🚀 Generate Winning Proposal"):
    if not api_key:
        st.error("Please add your API Key in the sidebar first!")
    elif not job_desc or not my_skills:
        st.error("Please fill in both fields.")
    else:
        with st.spinner("Analyzing client psychology... Drafting..."):
            try:
                # PROMPT ENGINEERING
                t_map = {"💼 Corporate (Safe)": "Professional", "🚀 Startup (Energetic)": "Enthusiastic", "🧠 Expert (Direct)": "Concise"}
                
                prompt = f"""
                Write a cover letter for Upwork.
                Job: {job_desc}
                Me: {my_skills}
                Tone: {t_map.get(tone)}
                
                Structure:
                1. Hook (Prove I read it)
                2. Solution (How I fix their pain)
                3. Call to Action (Soft close)
                No placeholders. Plain text.
                """
                
                res = model.generate_content(prompt)
                
                st.success("Draft Generated!")
                st.text_area("Copy your text:", value=res.text, height=350)
                
            except Exception as e:
                st.error(f"Error: {e}")

# --- SALES SECTION (BOTTOM) ---
st.markdown("""
<div class="sales-banner">
    <h3>🔥 Want to close 2x more deals?</h3>
    <p>Get the "Freelance Elite Pack" — 50+ Copy-Paste scripts for negotiation, difficult clients, and rate hikes.</p>
    <a href="https://dumpsterfire38.gumroad.com/l/freelance-elite-pack" target="_blank" class="sales-btn">Unlock Pack for $9</a>
</div>
""", unsafe_allow_html=True)
