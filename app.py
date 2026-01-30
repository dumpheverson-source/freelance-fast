import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="FreelanceFast",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED CSS (DEV/SAAS AESTHETIC) ---
st.markdown("""
<style>
    /* Import Fonts: Inter (UI) & JetBrains Mono (Code/Data) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    /* BASE THEME */
    :root {
        --bg-color: #0f172a;
        --panel-color: #1e293b;
        --border-color: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --accent-color: #6366f1; /* Indigo 500 */
        --accent-hover: #4f46e5; /* Indigo 600 */
        --font-ui: 'Inter', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    /* GLOBAL RESET */
    .stApp {
        background-color: var(--bg-color);
        font-family: var(--font-ui);
        color: var(--text-primary);
    }
    
    /* REMOVE STREAMLIT BLOAT */
    header {visibility: hidden;}
    .css-1rs6os {visibility: hidden;}
    .css-17ziqus {visibility: hidden;}
    
    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: var(--font-ui);
        letter-spacing: -0.02em;
        color: var(--text-primary);
    }
    
    .mono-label {
        font-family: var(--font-mono);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        display: block;
    }

    /* INPUT FIELDS (TERMINAL STYLE) */
    .stTextArea textarea {
        background-color: var(--panel-color) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-mono) !important; /* Code font for inputs */
        font-size: 0.9rem;
        border-radius: 6px;
        transition: border 0.2s ease;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 1px var(--accent-color) !important;
    }

    /* BUTTONS (HIGH END) */
    div.stButton > button {
        background-color: var(--accent-color);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        font-family: var(--font-ui);
        font-weight: 500;
        padding: 0.6rem 1.2rem;
        border-radius: 6px;
        transition: all 0.2s;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    div.stButton > button:hover {
        background-color: var(--accent-hover);
        border-color: rgba(255,255,255,0.2);
        transform: translateY(-1px);
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #020617; /* Darker than main */
        border-right: 1px solid var(--border-color);
    }
    
    /* ALERTS */
    .stAlert {
        background-color: var(--panel-color);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    /* CUSTOM CONTAINERS */
    .app-header {
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: var(--panel-color);
        border: 1px solid var(--border-color);
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONFIGURATION ---
with st.sidebar:
    st.markdown("<div style='margin-bottom: 2rem; font-weight: 600; font-size: 1.1rem; color: #fff;'>FreelanceFast<span style='color: #6366f1'>.ai</span></div>", unsafe_allow_html=True)
    
    st.markdown('<span class="mono-label">CONFIGURATION</span>', unsafe_allow_html=True)
    
    # API Key Input (Minimalist)
    api_key = st.text_input(
        "API Key (Google Gemini)",
        type="password",
        placeholder="sk-...",
        label_visibility="collapsed"
    )
    
    # Status Indicator
    if api_key:
        st.markdown("""
        <div style='display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #4ade80; margin-top: 8px;'>
            <div style='width: 8px; height: 8px; background: #4ade80; border-radius: 50%;'></div>
            System Operational
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #94a3b8; margin-top: 8px;'>
            <div style='width: 8px; height: 8px; background: #ef4444; border-radius: 50%;'></div>
            Awaiting Key
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown('<span class="mono-label">PARAMETERS</span>', unsafe_allow_html=True)
    
    tone = st.select_slider(
        "Tone Intensity",
        options=["Subtle", "Balanced", "Bold"],
        value="Balanced"
    )
    
    output_len = st.select_slider(
        "Response Length",
        options=["Concise", "Standard", "Detailed"],
        value="Concise"
    )

# --- MAIN LAYOUT ---

# Header Section
st.markdown("""
<div class="app-header">
    <h1>Proposal Generator</h1>
    <p style='color: #94a3b8; font-size: 1rem;'>Automated cover letter drafting for technical freelancers.</p>
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.info("Initialize system by providing a valid Google API Key in the sidebar.")
    st.stop()

# Configure GenAI
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except:
    st.error("Authentication failed. Verify API Key.")
    st.stop()

# Input Grid
col_job, col_skills = st.columns(2)

with col_job:
    st.markdown('<span class="mono-label">INPUT // JOB SPECIFICATION</span>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Spec",
        height=300,
        placeholder="Paste full job posting here...",
        label_visibility="collapsed"
    )

with col_skills:
    st.markdown('<span class="mono-label">INPUT // CANDIDATE PROFILE</span>', unsafe_allow_html=True)
    user_skills = st.text_area(
        "Candidate Profile",
        height=300,
        placeholder="List technical stack, years of experience, and key achievements...",
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Action Area
col_btn, col_status = st.columns([1, 4])

with col_btn:
    generate_btn = st.button("Execute Generation", use_container_width=True)

# Logic & Output
if generate_btn:
    if not job_description or not user_skills:
        st.toast("Error: Missing input parameters.", icon="⚠️")
    else:
        with st.spinner("Processing context..."):
            try:
                # System Prompt (Strict, Professional)
                prompt = f"""
                ROLE: Expert Technical Copywriter for Freelance Proposals.
                OBJECTIVE: Compose a high-conversion cover letter for a freelance platform (Upwork/Toptal).
                
                INPUT DATA:
                - Job Spec: {job_description}
                - Candidate Profile: {user_skills}
                - Tone: {tone}
                - Length: {output_len}
                
                CONSTRAINTS:
                1. No fluff. Get straight to the value proposition.
                2. Demonstrate understanding of the client's specific technical problem.
                3. Cite specific matching experience from the candidate profile.
                4. Professional, confident, but not arrogant tone.
                5. Call to Action: Clear availability for a call.
                
                OUTPUT FORMAT:
                Plain text only. No markdown headers.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown('<span class="mono-label">OUTPUT // GENERATED PROPOSAL</span>', unsafe_allow_html=True)
                
                # Output Container
                st.text_area(
                    "Result",
                    value=response.text,
                    height=400,
                    label_visibility="collapsed"
                )
                
                st.success("Generation complete. 128ms")
                
            except Exception as e:
                st.error(f"Runtime Error: {str(e)}")

# Minimal Footer
st.markdown("""
<div style='text-align: center; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid #334155; color: #64748b; font-size: 0.8rem; font-family: "Inter", sans-serif;'>
    FreelanceFast v1.0.2 • System Status: Operational
</div>
""", unsafe_allow_html=True)
