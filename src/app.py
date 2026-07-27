import streamlit as st
import os

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="JSRS AI Assistant - BGI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# =========================================================
# FUNCTIONS
# =========================================================
def go_home():
    """
    Clears the chat history and pending question, returning to the welcome screen.
    """
    st.session_state.messages = []
    st.session_state.pending_question = None
    st.rerun()

def get_ai_response(prompt: str) -> str:
    """
    Generates AI response using Gemini API if GEMINI_API_KEY is available,
    otherwise returns a context-aware fallback response.
    """
    # Safely retrieve API Key from environment variables or Streamlit secrets
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = None
    
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            system_instruction = (
                "You are the official JSRS AI Assistant for Business Gateways International (BGI). "
                "Provide accurate, professional, and clear answers regarding the Joint Supplier Registration System (JSRS), "
                "supplier certification, registration requirements, profile updates, and oil & gas supplier gateways in Oman."
            )
            response = model.generate_content(f"{system_instruction}\n\nUser Question: {prompt}")
            return response.text
        except Exception as e:
            return f"Error communicating with AI service: {str(e)}"
    
    # Contextual knowledge base fallback response when no API key is provided
    prompt_lower = prompt.lower()
    if "jsrs" in prompt_lower and ("what" in prompt_lower or "is" in prompt_lower):
        return (
            "**Joint Supplier Registration System (JSRS)** is an industry-wide supplier certification and single-window "
            "registration system operated by Business Gateways International (BGI) in Oman. It connects suppliers with "
            "Operators (like PDO, OQ, Daleel Petroleum) and Contractors across key energy and economic sectors."
        )
    elif "register" in prompt_lower or "apply" in prompt_lower or "how to register" in prompt_lower:
        return (
            "**Steps to register on JSRS:**\n"
            "1. Visit the official Business Gateways portal.\n"
            "2. Fill out the online Supplier Registration application.\n"
            "3. Upload mandatory corporate documents (CR Certificate, Chamber of Commerce Membership, Tax ID).\n"
            "4. Pay the applicable registration fee and submit for verification by the BGI team."
        )
    elif "document" in prompt_lower or "requirement" in prompt_lower:
        return (
            "**Mandatory documents required for JSRS Registration:**\n"
            "- Commercial Registration (CR) Certificate\n"
            "- Chamber of Commerce Membership Certificate\n"
            "- Valid Tax Identification / VAT Certificate\n"
            "- Company Profile & Authorized Signatory Identification\n"
            "- Quality & HSE Policy Documents (if applicable)"
        )
    elif "update" in prompt_lower or "profile" in prompt_lower or "modify" in prompt_lower:
        return (
            "**Steps to update your JSRS Company Profile:**\n"
            "1. Log in to your official **JSRS Supplier Portal** account.\n"
            "2. Navigate to **'Company Profile Management'** from your dashboard.\n"
            "3. Select the section you wish to update (e.g., Contact Info, Products/Services, Financials, HSE/Certificates).\n"
            "4. Upload supporting documents if updating legal details or trade licenses.\n"
            "5. Click **'Submit for Verification'**. BGI team will review and approve your requested changes."
        )
    else:
        return (
            f"Thank you for your question regarding: **'{prompt}'**.\n\n"
            "The JSRS AI Assistant is here to assist with supplier registration, certification, "
            "and business gateways documentation. Please feel free to ask about registration steps, mandatory documents, or profile updates."
        )

def process_question(question_text: str):
    """
    Adds user question and appends AI response to session state.
    """
    st.session_state.messages.append({"role": "user", "content": question_text})
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Searching knowledge base..."):
            response = get_ai_response(question_text)
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# =========================================================
# HEADER
# =========================================================
st.markdown("<h1 style='text-align: center;'>Business Gateways International</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #0284c7;'>🤖 JSRS AI Assistant</h3>", unsafe_allow_html=True)
st.markdown("---")

# =========================================================
# BACK BUTTON (If in active chat session)
# =========================================================
if st.session_state.messages:
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("⬅️ Back to Home", use_container_width=True):
            go_home()

# Handle quick button selection
if st.session_state.pending_question:
    q = st.session_state.pending_question
    st.session_state.pending_question = None
    process_question(q)

# =========================================================
# MAIN CONTENT AREA
# =========================================================
if not st.session_state.messages:
    # WELCOME SCREEN
    st.markdown(
        """
        <div style='text-align: center; padding: 20px 0;'>
            <h2>Welcome to the JSRS Knowledge Assistant</h2>
            <p style='font-size: 1.1rem; color: #64748b;'>
                Your intelligent assistant for Joint Supplier Registration System inquiries, supplier certification guidance, and enterprise documentation.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("#### 💡 Quick Inquiry Topics")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("❓ What is JSRS and who operates it?", use_container_width=True):
            st.session_state.pending_question = "What is JSRS and who operates it?"
            st.rerun()
            
        if st.button("📋 What documents are required for registration?", use_container_width=True):
            st.session_state.pending_question = "What documents are required for registration?"
            st.rerun()

    with col_b:
        if st.button("🚀 How do I apply for JSRS Certification?", use_container_width=True):
            st.session_state.pending_question = "How do I apply for JSRS Certification?"
            st.rerun()
            
        if st.button("🔄 How do I update my company profile?", use_container_width=True):
            st.session_state.pending_question = "How do I update my company profile?"
            st.rerun()

else:
    # CHAT HISTORY SCREEN
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# =========================================================
# CHAT INPUT
# =========================================================
user_input = st.chat_input("Type your question here...")
if user_input:
    process_question(user_input)