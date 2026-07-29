import sys
from pathlib import Path

import streamlit as st


# =========================================================
# IMPORT CENTRAL RAG PIPELINE
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIRECTORY = PROJECT_ROOT / "src"

if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from rag_pipeline import ask_question


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="JSRS AI Assistant",
    page_icon="🤖",
    layout="centered",
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# =========================================================
# SUGGESTED QUESTIONS
# =========================================================

SUGGESTED_QUESTIONS = {
    "📄 Registration & Certification":
        "How can I register and apply for JSRS certification?",

    "📂 Required Documents":
        "What documents are required for JSRS certification?",

    "💳 Fee Payment Support":
        "How can I make a JSRS fee payment or resolve a payment issue?",

    "🔄 Validity & Renewal":
        "What is the validity period and renewal process for JSRS certification?",

    "🏢 PDO Related Queries":
        "What information is available for PDO-related JSRS queries?",
}


# =========================================================
# STYLING  (Blue / White / Orange palette)
# =========================================================

st.markdown(
    """
<style>
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background-color: #F5F9FF;
    color: #14213D;
}

.block-container {
    max-width: 820px;
    padding-top: 2.5rem;
    padding-bottom: 6rem;
}

/* Header */

.company-name {
    text-align: center;
    color: #FF7A00;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
    letter-spacing: 0.3px;
}

.assistant-title {
    text-align: center;
    color: #0B4F9E;
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 40px;
}

/* Welcome */

.welcome-title {
    color: #0B4F9E;
    font-size: 25px;
    font-weight: 700;
    margin-bottom: 14px;
}

.welcome-text {
    color: #2C3E50;
    font-size: 16px;
    line-height: 1.75;
    margin-bottom: 24px;
}

/* Divider */

.custom-divider {
    border-top: 1px solid #D6E4F5;
    margin: 24px 0;
}

/* Topic buttons */

div.stButton > button {
    width: 100%;
    min-height: 54px;
    background-color: #FFFFFF;
    color: #14213D;
    border: 1px solid #E1EAF7;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    font-size: 16px;
    font-weight: 500;
    text-align: left;
    justify-content: flex-start;
    margin-bottom: 6px;
}

div.stButton > button::after {
    content: "→";
    margin-left: auto;
    font-size: 20px;
    color: #FF7A00;
}

div.stButton > button:hover {
    background-color: #EAF3FF;
    color: #0B4F9E;
    border-color: #0B4F9E;
}

/* Chat messages */

div[data-testid="stChatMessage"] {
    background-color: #FFFFFF;
    border: 1px solid #E1EAF7;
    border-radius: 12px;
    margin-bottom: 12px;
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] ul,
div[data-testid="stChatMessage"] ol,
div[data-testid="stChatMessage"] strong,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] div {
    color: #14213D !important;
}

/* Sources */

.source-title {
    margin-top: 14px;
    font-size: 14px;
    font-weight: 700;
    color: #FF7A00;
}

.source-item {
    background-color: #F5F9FF;
    border-left: 3px solid #FF7A00;
    border-radius: 6px;
    padding: 8px 10px;
    margin-top: 7px;
    color: #14213D;
    font-size: 14px;
}

/* Chat input container */

div[data-testid="stChatInput"] {
    background-color: #FFFFFF;
    border: 1px solid #0B4F9E;
    border-radius: 12px;
}

/* Bottom bar wrapping the chat input (fixes half-black/half-white background) */

div[data-testid="stBottom"],
div[data-testid="stBottomBlockContainer"],
.stChatFloatingInputContainer,
div[data-testid="stChatInput"] > div {
    background-color: #F5F9FF !important;
}

section[data-testid="stBottom"] > div,
div[data-testid="stBottom"] > div,
footer[data-testid="stBottom"] {
    background-color: #F5F9FF !important;
}

html, body {
    background-color: #F5F9FF !important;
}

/* Chat input text + placeholder (fixes invisible typed text) */

div[data-testid="stChatInput"] textarea {
    color: #14213D !important;
    background-color: #FFFFFF !important;
    caret-color: #0B4F9E !important;
    -webkit-text-fill-color: #14213D !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #8CA3C4 !important;
    opacity: 1 !important;
}

/* Chat input send button icon */

div[data-testid="stChatInput"] button svg {
    fill: #FF7A00 !important;
}

/* Spinner text */

.stSpinner > div {
    color: #0B4F9E !important;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1.5rem;
    }

    .assistant-title {
        font-size: 30px;
    }
}
</style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def display_sources(sources):
    if not sources:
        return

    unique_sources = []

    for source in sources:
        if source not in unique_sources:
            unique_sources.append(source)

    st.markdown(
        '<div class="source-title">📄 Sources</div>',
        unsafe_allow_html=True,
    )

    for source in unique_sources:
        st.markdown(
            f'<div class="source-item">{source}</div>',
            unsafe_allow_html=True,
        )

def go_home():
    """
    Clears the chat history and returns to the welcome screen.
    """
    st.session_state.messages = []
    st.session_state.pending_question = None
    st.rerun()


def process_question(question):
    question = question.strip()

    if not question:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    try:
        with st.spinner("Searching JSRS documents..."):
            result = ask_question(question, k=3)

        answer = result.get(
            "answer",
            "I could not generate an answer.",
        )

        sources = result.get("sources", [])

    except Exception as error:
        answer = (
            "The assistant could not process your question. "
            "Please check the backend configuration."
        )

        sources = []

        st.error(str(error))

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="company-name">
    Business Gateways International
</div>

<div class="assistant-title">
    🤖 JSRS AI Assistant
</div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# BACK TO HOME BUTTON
# =========================================================

if st.session_state.messages:
    if st.button("🏠 Home"):
        go_home()

# =========================================================
# WELCOME SCREEN
# =========================================================

if not st.session_state.messages:
    st.markdown(
        """
<div class="welcome-title">
    👋 Welcome!
</div>

<div class="welcome-text">
    I'm your AI assistant for the JSRS Portal.
    <br><br>
    I can help answer questions about JSRS processes,
    documentation, certification, renewals, fee payments
    and other supplier-related queries using the official
    JSRS knowledge base.
</div>

<div class="custom-divider"></div>
        """,
        unsafe_allow_html=True,
    )

    for index, (label, question) in enumerate(
        SUGGESTED_QUESTIONS.items()
    ):
        if st.button(
            label,
            key=f"topic_{index}",
            use_container_width=True,
        ):
            st.session_state.pending_question = question
            st.rerun()

    st.markdown(
        '<div class="custom-divider"></div>',
        unsafe_allow_html=True,
    )


# =========================================================
# DISPLAY CHAT
# =========================================================

for message in st.session_state.messages:
    role = message.get("role", "assistant")
    avatar = "👤" if role == "user" else "🤖"

    with st.chat_message(role, avatar=avatar):
        st.markdown(message.get("content", ""))

        if role == "assistant":
            display_sources(message.get("sources", []))


# =========================================================
# PROCESS TOPIC BUTTON
# =========================================================

if st.session_state.pending_question:
    selected_question = st.session_state.pending_question
    st.session_state.pending_question = None

    process_question(selected_question)
    st.rerun()


# =========================================================
# CHAT INPUT
# =========================================================

user_question = st.chat_input(
    "Ask anything about JSRS..."
)

if user_question:
    process_question(user_question)
    st.rerun()