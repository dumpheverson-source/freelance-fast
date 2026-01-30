import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="FreelanceFast",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CLEAN SAAS CSS (Notion/Linear Style) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* BASE THEME */
    :root {
        --primary-color: #2563eb; /* Royal Blue */
        --bg-color: #ffffff;
        --text-color: #0f172a;
        --secondary-text: #64748b;
        --border-color: #e2e8f0;
    }

    /* GLOBAL RESET */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-color);
    }
    
    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* TYPOGRAPHY */
    h1 {
        font-weight: 700;
        letter-spacing: -0.02em;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    h3 {
        font-weight: 600;
        font-size: 1.1rem;
        margin-top: 1.5rem;
    }
    p {
        color: var(--secondary-text);
        line-height: 1.6;
    }

    /* INPUT FIELDS (CLEAN) */
    .stTextArea textarea {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px;
        padding: 12px;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: border-color 0.2s;
    }
    .stTextArea textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }

    /* BUTTONS (PRIMARY) */
    div.stButton > button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 6px 8px -2px rgba(37, 99, 235, 0.3);
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid var(--border-color);
    }

    /* INFO BOXES */
    .stAlert {
        background-color: #eff6ff;
        border: 1px solid #dbeafe;
        color: #1e40af;
        border-radius: 8px;
    }
    
    /* STEPS INDICATOR */
    .step-badge {
        background-color: #f1f5f9;
        color: #475569;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔑 Step 1: Get Access")
    
    # TUTORIAL DESTAQUE (CORREÇÃO)
    st.info("""
    **Need a Free Key?**
    1. [Click here to open Google AI](https://aistudio.google.com/app/apikey)
    2. Click blue button **"Create API Key"**
    3. Copy the code that starts with `AIza...`
    4. Paste it below 👇
    """)
    
    api_key = st.text_input(
        "Paste Key Here",
        type="password",
        help="Paste your free Gemini API key here.",
        placeholder="AIzaSy..."
    )
    
    if api_key:
        st.success("✅ Connected! You are ready.")

    st.markdown("---")
    st.markdown("### 💎 Step 2: Pro Level")
    st.warning("""
    **🔥 Want to earn more?**
    
    Don't just send a proposal. Send a **winning strategy**.
    
    Get our **"Freelance Elite Pack"**:
    - 50+ Templates for tough clients
    - Scripts to negotiate higher rates
    - "Copy/Paste" responses for interviews
    
    **[👉 Get the Pack for $9](https://dumpsterfire38.gumroad.com/l/freelance-elite-pack)**
    """)

# --- MAIN CONTENT ---
st.markdown("<div style='text-align: center; margin-bottom: 2rem;'>", unsafe_allow_html=True)
st.title("FreelanceFast")
st.markdown("Create winning proposals for Upwork & Fiverr in seconds.")
st.markdown("</div>", unsafe_allow_html=True)

# (Removido o bloqueio visual st.stop aqui)

# Configure AI (Lazy Loading)
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
    except:
        pass # Handle error later on button click

# STEP 1
st.markdown('<h3><span class="step-badge">1</span>The Job</h3>', unsafe_allow_html=True)
job_description = st.text_area(
    "Paste the client's job description here",
    height=200,
    placeholder="e.g. Looking for a graphic designer to create a logo for a coffee shop...",
    label_visibility="collapsed"
)

# STEP 2
st.markdown('<h3><span class="step-badge">2</span>Your Skills</h3>', unsafe_allow_html=True)
user_skills = st.text_area(
    "Paste your skills or brief bio",
    height=150,
    placeholder="e.g. 5 years experience in Adobe Illustrator, branding expert...",
    label_visibility="collapsed"
)

# STEP 3
col1, col2 = st.columns(2)
with col1:
    st.markdown('<h3><span class="step-badge">3</span>Tone</h3>', unsafe_allow_html=True)
    tone = st.selectbox(
        "Choose tone",
        ["Professional & Direct", "Friendly & Casual", "Confident & Expert"],
        label_visibility="collapsed"
    )
with col2:
    st.markdown('<h3><span class="step-badge">4</span>Length</h3>', unsafe_allow_html=True)
    length = st.selectbox(
        "Choose length",
        ["Short & Punchy", "Standard", "Detailed"],
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Write Proposal"):
    if not api_key:
        st.error("🔒 Please enter your Google API Key in the sidebar to generate results. It's free!")
        st.sidebar.markdown("### ⬅️ Enter Key Here")
    elif not job_description or not user_skills:
        st.error("Please fill in both the Job Description and Your Skills.")
    else:
        with st.spinner("Writing your proposal..."):
            try:
                prompt = f"""
                Write a freelance proposal for Upwork/Fiverr.
                
                CONTEXT:
                - Job: {job_description}
                - Me: {user_skills}
                - Tone: {tone}
                - Length: {length}
                
                RULES:
                1. Start with a hook that proves I read the job.
                2. Explain WHY I am the best fit.
                3. Mention specific skills I have.
                4. End with a question or call to action.
                5. Do NOT use placeholders like [Name].
                
                OUTPUT:
                Plain text only.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success("🎉 Proposal Ready!")
                st.text_area("Copy and paste this:", value=response.text, height=350)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 3rem;'>
    FreelanceFast © 2024 • Open Source
</div>
""", unsafe_allow_html=True)
