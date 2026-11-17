import streamlit as st
from core.config import (
    APP_TITLE,
    DEVELOPER_NAME,
    MODEL_NAME,
    TEMPERATURE,
    SUPPORTED_BOARDS,
    LANGUAGES,
    QUICK_PROMPTS,
    get_api_key,
)
from core.prompts import build_system_prompt
from core.llm_client import PibotClient
from core.splash import render_splash_screen

# Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Trigger Animated Boot Splash Screen
render_splash_screen(duration=3.2)

# Custom Styling
st.markdown(
    """
    <style>
    .stChatMessage { border-radius: 10px; padding: 0.75rem; }
    .secure-badge {
        padding: 0.55rem 0.75rem;
        border-radius: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #10b981;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .dev-badge {
        font-size: 0.85rem;
        color: #9ca3af;
        border-top: 1px solid #374151;
        padding-top: 0.75rem;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load API Key Silently from Streamlit Secrets
api_key = get_api_key()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Assalam-o-Alaikum & Hello! I am **PIBOT**, your Raspberry Pi 4 & 5 AI Engineering Assistant.\n\n"
                "Ask me anything about **GPIO wiring, Python code, I2C/SPI/UART, sensors, motors, cameras, or Linux troubleshooting** "
                "in **English** or **Urdu (اردو)**."
            ),
        }
    ]

# Sidebar Configuration (No API credential fields rendered)
with st.sidebar:
    st.title("🍓 PIBOT Control Panel")
    st.caption("Raspberry Pi 4 & 5 Technical Expert")

    if api_key:
        st.markdown(
            '<div class="secure-badge">🔒 Credentials Secured via Streamlit Secrets</div>',
            unsafe_allow_html=True,
        )
    else:
        st.error("⚠️ Missing `OPENAI_API_KEY` in `.streamlit/secrets.toml`.")

    st.divider()
    st.subheader("Hardware & Language")

    selected_board = st.selectbox("Target Raspberry Pi", SUPPORTED_BOARDS, index=0)
    selected_lang = st.selectbox("Response Language", LANGUAGES, index=0)

    st.divider()
    st.subheader("Quick Project Starters")
    for label, prompt_text in QUICK_PROMPTS.items():
        if st.button(label, use_container_width=True):
            st.session_state.pending_prompt = prompt_text

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()
    with col2:
        if st.button("🔄 Boot Screen", use_container_width=True):
            st.session_state.splash_shown = False
            st.rerun()

    st.markdown(
        f'<div class="dev-badge"><b>Developed by:</b> {DEVELOPER_NAME}<br>'
        f'<b>Model:</b> {MODEL_NAME} | <b>Temp:</b> {TEMPERATURE}</div>',
        unsafe_allow_html=True,
    )

# Main Chat Header
st.title("🍓 PIBOT – Raspberry Pi AI Assistant")
st.caption(
    f"Hardware Mode: **{selected_board}** | Language: **{selected_lang}** | Developed by **{DEVELOPER_NAME}**"
)

# Render Chat History
for msg in st.session_state.messages:
    avatar = "🍓" if msg["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Handle Input
user_input = st.chat_input(
    "Describe your Raspberry Pi project, wiring question, or error (English / اردو)..."
)

if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    user_input = st.session_state.pop("pending_prompt")

if user_input:
    if not api_key:
        st.error("API credentials are not configured in Streamlit Secrets (`OPENAI_API_KEY`).")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    system_prompt = build_system_prompt(selected_board, selected_lang)
    client = PibotClient(api_key=api_key)

    with st.chat_message("assistant", avatar="🍓"):
        response_text = st.write_stream(
            client.stream_response(
                system_prompt=system_prompt,
                messages=st.session_state.messages,
            )
        )

    st.session_state.messages.append({"role": "assistant", "content": response_text})
