import streamlit as st
from core.config import (
    APP_TITLE,
    DEVELOPER_NAME,
    DEFAULT_MODEL,
    API_KEY,
    SUPPORTED_BOARDS,
    LANGUAGES,
    QUICK_PROMPTS,
)
from core.prompts import build_system_prompt
from core.llm_client import PibotClient

# Page Configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .stChatMessage { border-radius: 10px; padding: 0.75rem; }
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

# Sidebar Configuration
with st.sidebar:
    st.title("🍓 PIBOT Control Panel")
    st.caption("Raspberry Pi 4 & 5 Technical Expert")

    api_key_input = st.text_input(
        "OpenAI API Key",
        value=API_KEY,
        type="password",
        help="Enter your OpenAI API key or configure OPENAI_API_KEY in .env",
    )

    model_name = st.text_input(
        "Model Name",
        value=DEFAULT_MODEL,
        help="Default: gpt-6-luna",
    )

    st.divider()
    st.subheader("Hardware & Language")

    selected_board = st.selectbox("Target Raspberry Pi", SUPPORTED_BOARDS, index=0)
    selected_lang = st.selectbox("Response Language", LANGUAGES, index=0)
    temperature = st.slider(
        "Creativity / Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.05,
        help="Lower values (0.1–0.3) yield more deterministic code and wiring instructions.",
    )

    st.divider()
    st.subheader("Quick Project Starters")
    for label, prompt_text in QUICK_PROMPTS.items():
        if st.button(label, use_container_width=True):
            st.session_state.pending_prompt = prompt_text

    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

    st.markdown(
        f'<div class="dev-badge"><b>Developer:</b> {DEVELOPER_NAME}<br>'
        f'<b>Engine:</b> {model_name}</div>',
        unsafe_allow_html=True,
    )

# Main Chat Header
st.title("🍓 PIBOT – Raspberry Pi AI Assistant")
st.caption(
    f"Hardware Mode: **{selected_board}** | Language: **{selected_lang}** | Developer: **{DEVELOPER_NAME}**"
)

# Render Chat History
for msg in st.session_state.messages:
    avatar = "🍓" if msg["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Handle Input (either from Chat Input or Quick Starter Button)
user_input = st.chat_input(
    "Describe your Raspberry Pi project, wiring question, or error (English / اردو)..."
)

if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    user_input = st.session_state.pop("pending_prompt")

if user_input:
    if not api_key_input:
        st.error("Please enter your OpenAI API Key in the sidebar or `.env` file to run PIBOT.")
        st.stop()

    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    # Generate and stream PIBOT response
    system_prompt = build_system_prompt(selected_board, selected_lang)
    client = PibotClient(api_key=api_key_input, model=model_name)

    with st.chat_message("assistant", avatar="🍓"):
        response_text = st.write_stream(
            client.stream_response(
                system_prompt=system_prompt,
                messages=st.session_state.messages,
                temperature=temperature,
            )
        )

    st.session_state.messages.append({"role": "assistant", "content": response_text})
