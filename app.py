import streamlit as st
import google.generativeai as genai
import os

# Configuração da Página
st.set_page_config(
    page_title="FreelanceFast.ai - Win More Jobs",
    page_icon="🚀",
    layout="centered"
)

# Estilo Customizado (CSS simples para deixar bonito)
st.markdown("""
<style>
    .stTextArea textarea {font-size: 16px !important;}
    .stButton button {width: 100%; background-color: #4CAF50; color: white; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Título e Subtítulo
st.title("🚀 FreelanceFast.ai")
st.markdown("### Generate winning cover letters in seconds.")
st.markdown("---")

# Barra Lateral - Configuração e API Key (SEGURANÇA MÁXIMA)
with st.sidebar:
    st.header("🔑 Settings")
    
    api_key = st.text_input(
        "Enter your Google API Key:",
        type="password",
        help="Get your free key at https://aistudio.google.com/app/apikey. Your key is NOT stored on our servers."
    )
    
    if not api_key:
        st.warning("⚠️ You need a Google API Key to use this app. It's free!")
        st.stop()
    
    st.success("API Key is ready! ✅")
    
    st.markdown("---")
    st.markdown("**Tips for better results:**")
    st.markdown("- Paste the full job description.")
    st.markdown("- Be honest about your skills.")
    st.markdown("- Review the generated text before sending.")

# Configurar o Modelo (Google Gemini)
try:
    genai.configure(api_key=api_key)
    # Usando Gemini 1.5 Pro (gratuito e inteligente) ou Flash (rápido)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
except Exception as e:
    st.error(f"Error configuring API: {e}")
    st.stop()

# Área Principal - Inputs do Usuário
col1, col2 = st.columns(2)

with col1:
    job_description = st.text_area(
        "📋 Job Description",
        height=300,
        placeholder="Paste the job description from Upwork, Fiverr, etc..."
    )

with col2:
    user_skills = st.text_area(
        "👤 Your Skills & Experience",
        height=300,
        placeholder="I am a Python developer with 5 years of experience in web scraping..."
    )

tone = st.selectbox(
    "🎭 Tone of Voice",
    ["Professional & Direct", "Enthusiastic & Eager", "Casual & Friendly", "Confident & Expert"]
)

# Botão de Geração
if st.button("✨ Generate Cover Letter"):
    if not job_description or not user_skills:
        st.error("Please fill in both the Job Description and Your Skills.")
    else:
        with st.spinner("Writing the perfect proposal for you..."):
            try:
                # O Prompt "Engenharia Reversa de RH"
                prompt = f"""
                You are an expert copywriter specializing in freelance proposals for Upwork.
                Your goal is to write a cover letter that gets the freelancer hired.
                
                **The Job:**
                {job_description}
                
                **The Freelancer:**
                {user_skills}
                
                **Instructions:**
                1. Tone: {tone}
                2. Start with a strong hook that shows you read the job description.
                3. Explain why the freelancer is the perfect fit based on their skills.
                4. Keep it concise (under 200 words if possible).
                5. End with a clear Call to Action (CTA) to schedule a call.
                6. Do NOT include placeholders like [Your Name] unless absolutely necessary.
                7. Output only the cover letter text.
                """
                
                response = model.generate_content(prompt)
                
                st.subheader("Your Cover Letter:")
                st.text_area("Copy and paste this:", value=response.text, height=400)
                st.balloons()
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
