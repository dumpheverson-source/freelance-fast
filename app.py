import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="FreelanceFast.ai",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://twitter.com/seutwitter',
        'Report a bug': "https://github.com/dumpheverson-source/freelance-fast/issues",
        'About': "FreelanceFast.ai helps you win more jobs on Upwork & Fiverr."
    }
)

# --- CUSTOM CSS (THE "HUMAN" TOUCH) ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Titles */
    h1 {
        font-weight: 700;
        color: #ffffff;
        font-size: 3rem !important;
        margin-bottom: 0.5rem;
    }
    h3 {
        font-weight: 600;
        color: #e0e0e0;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 900px;
    }

    /* Cards (Input Areas) */
    .stTextArea textarea {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 8px;
        color: #f0f0f0;
        padding: 10px;
    }
    .stTextArea textarea:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 1px #4CAF50;
    }

    /* The Generate Button */
    div.stButton > button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(76, 175, 80, 0.39);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(76, 175, 80, 0.23);
        background: linear-gradient(90deg, #45a049 0%, #4CAF50 100%);
        border: none;
        color: white;
    }
    div.stButton > button:active {
        transform: translateY(1px);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111;
        border-right: 1px solid #222;
    }
    
    /* Success/Warning Boxes */
    .stAlert {
        border-radius: 8px;
    }
    
    /* Custom Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #666;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
        border-top: 1px solid #222;
        z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (CONFIG) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=60) # Placeholder logo
    st.title("Settings")
    
    st.markdown("### 🔑 API Access")
    api_key = st.text_input(
        "Google API Key",
        type="password",
        placeholder="Paste your key here...",
        help="Your key is processed locally in memory. We never store it."
    )
    
    if not api_key:
        st.warning("👉 You need a free Google Gemini API key to start.")
        st.markdown("[Get a free key here](https://aistudio.google.com/app/apikey)", unsafe_allow_html=True)
    else:
        st.success("Connected & Secure 🔒")

    st.markdown("---")
    st.markdown("### 🎯 Pro Tips")
    st.info(
        "**1. Be Specific:** Paste the full job description.\n\n"
        "**2. Be Honest:** Don't invent skills you don't have.\n\n"
        "**3. Edit:** Always read before sending."
    )
    
    st.markdown("---")
    st.caption("Version 1.0.0 • Open Source")

# --- MAIN CONTENT ---

# Header
st.title("⚡ FreelanceFast.ai")
st.markdown("""
<div style='font-size: 1.2rem; color: #aaa; margin-bottom: 2rem;'>
    The unfair advantage for freelancers. Generate <b>highly persuasive</b> cover letters in seconds.
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.image("https://raw.githubusercontent.com/dumpheverson-source/freelance-fast/main/assets/banner_placeholder.png", caption="Add your API key in the sidebar to unlock 🔓") 
    st.stop()

# Configure Model
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except Exception as e:
    st.error(f"⚠️ Invalid API Key. Please check it and try again.")
    st.stop()

# Input Section (Two Columns)
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 1️⃣ The Job")
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="e.g. 'Looking for a Python developer to build a scraper...'"
    )

with col2:
    st.markdown("### 2️⃣ Your Edge")
    user_skills = st.text_area(
        "Paste your skills or resume summary",
        height=300,
        placeholder="e.g. 'Senior Python Dev with 5 years exp in Selenium, BS4...'"
    )

# Options
st.markdown("### 3️⃣ Fine-tuning")
tone_col, length_col = st.columns(2)
with tone_col:
    tone = st.selectbox(
        "Tone of Voice",
        ["Professional & Confident", "Casual & Friendly", "Direct & No-nonsense", "Enthusiastic & Eager"],
        index=0
    )
with length_col:
    length = st.radio(
        "Length",
        ["Short (Impactful)", "Medium (Standard)", "Long (Detailed)"],
        horizontal=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# Generate Button
if st.button("🚀 Write My Cover Letter"):
    if not job_description or not user_skills:
        st.error("⚠️ Please fill in both the Job Description and Your Skills.")
    else:
        with st.spinner("🧠 Analyzing job requirements... Drafting proposal..."):
            try:
                # Advanced Prompt Engineering
                prompt = f"""
                Act as a world-class copywriter for top-tier freelancers. Write a cover letter for Upwork/Freelancer.com.
                
                CONTEXT:
                - Job: {job_description}
                - My Skills: {user_skills}
                - Tone: {tone}
                - Length: {length}
                
                RULES:
                1. HOOK: Start with a custom hook that proves I read the job post. No generic "I am writing to apply..."
                2. VALUE: Focus on how I solve THEIR problem, not just listing my skills.
                3. PROOF: Mention relevant experience from my skills that matches their needs.
                4. CTA: End with a low-friction call to action (e.g., "Ready to chat?").
                5. FORMAT: Use short paragraphs. No walls of text.
                6. Do not use placeholders like [Your Name] unless strictly needed.
                
                OUTPUT:
                Just the cover letter text. No preamble.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("🎉 Your Draft is Ready")
                st.success("Copy the text below and tweak it if needed!")
                
                st.text_area("Final Result", value=response.text, height=450)
                
                # Feedback/Copy helpers
                st.caption("💡 Tip: Add a link to your portfolio before sending!")
                
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

# Footer
st.markdown("""
<div class="footer">
    Built for the hustle. FreelanceFast.ai © 2024
</div>
""", unsafe_allow_html=True)
