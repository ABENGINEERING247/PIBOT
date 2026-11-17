import time
import streamlit as st
from core.config import DEVELOPER_NAME


def render_splash_screen(duration: float = 3.2) -> None:
    """Displays a full-screen animated hardware boot splash screen on initial load."""
    if st.session_state.get("splash_shown", False):
        return

    splash_placeholder = st.empty()

    with splash_placeholder.container():
        st.markdown(
            f"""
            <style>
            /* Hide default Streamlit chrome during boot animation */
            header[data-testid="stHeader"],
            section[data-testid="stSidebar"] {{
                display: none !important;
            }}

            .pibot-splash-overlay {{
                position: fixed;
                inset: 0;
                z-index: 999999;
                background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: #f8fafc;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                text-align: center;
                padding: 2rem;
            }}

            /* Animated Circuit Ring + Core Emblem */
            .pibot-loader-ring {{
                position: relative;
                width: 110px;
                height: 110px;
                border-radius: 50%;
                border: 3px solid rgba(16, 185, 129, 0.15);
                border-top: 3px solid #10b981;
                border-right: 3px solid #ec4899;
                animation: spinRing 1.4s linear infinite;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1.75rem;
                box-shadow: 0 0 30px rgba(16, 185, 129, 0.25);
            }}

            .pibot-core-icon {{
                font-size: 2.8rem;
                animation: pulseCore 1.6s ease-in-out infinite, counterSpin 1.4s linear infinite;
            }}

            /* Title & Subtitle Animations */
            .pibot-title {{
                font-size: 3.4rem;
                font-weight: 800;
                letter-spacing: 0.22em;
                margin: 0;
                background: linear-gradient(90deg, #10b981, #34d399, #f43f5e);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: fadeSlideUp 0.8s ease-out forwards;
            }}

            .pibot-subtitle {{
                font-size: 1.05rem;
                color: #94a3b8;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin-top: 0.4rem;
                margin-bottom: 2rem;
                animation: fadeSlideUp 1s ease-out forwards;
            }}

            /* Progress Bar */
            .pibot-progress-track {{
                width: min(360px, 80vw);
                height: 6px;
                background: rgba(255, 255, 255, 0.08);
                border-radius: 999px;
                overflow: hidden;
                margin-bottom: 1rem;
            }}

            .pibot-progress-fill {{
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, #10b981, #ec4899);
                border-radius: 999px;
                animation: loadFill {duration}s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }}

            .pibot-boot-status {{
                font-family: monospace;
                font-size: 0.85rem;
                color: #34d399;
                margin-bottom: 2.5rem;
                animation: blinkText 1.2s infinite;
            }}

            /* Developer Credit Badge */
            .pibot-dev-credit {{
                padding: 0.65rem 1.4rem;
                border: 1px solid rgba(16, 185, 129, 0.35);
                background: rgba(16, 185, 129, 0.08);
                border-radius: 999px;
                font-size: 0.95rem;
                color: #e2e8f0;
                letter-spacing: 0.04em;
                animation: fadeSlideUp 1.2s ease-out forwards;
            }}

            .pibot-dev-credit span {{
                color: #10b981;
                font-weight: 700;
            }}

            @keyframes spinRing {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}

            @keyframes counterSpin {{
                0% {{ transform: rotate(360deg); }}
                100% {{ transform: rotate(0deg); }}
            }}

            @keyframes pulseCore {{
                0%, 100% {{ transform: scale(0.95); filter: drop-shadow(0 0 6px rgba(244, 63, 94, 0.5)); }}
                50% {{ transform: scale(1.08); filter: drop-shadow(0 0 16px rgba(16, 185, 129, 0.8)); }}
            }}

            @keyframes loadFill {{
                0% {{ width: 0%; }}
                45% {{ width: 62%; }}
                80% {{ width: 88%; }}
                100% {{ width: 100%; }}
            }}

            @keyframes fadeSlideUp {{
                0% {{ opacity: 0; transform: translateY(14px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}

            @keyframes blinkText {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.45; }}
            }}
            </style>

            <div class="pibot-splash-overlay">
                <div class="pibot-loader-ring">
                    <div class="pibot-core-icon">🍓</div>
                </div>
                <h1 class="pibot-title">PIBOT</h1>
                <div class="pibot-subtitle">Raspberry Pi 4 &amp; 5 AI Engineering Assistant</div>
                <div class="pibot-progress-track">
                    <div class="pibot-progress-fill"></div>
                </div>
                <div class="pibot-boot-status">[BOOT] Initializing GPIO / I2C / SPI Subsystems &amp; GPT-6 Luna...</div>
                <div class="pibot-dev-credit">
                    Developed by <span>{DEVELOPER_NAME}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        time.sleep(duration)

    st.session_state.splash_shown = True
    splash_placeholder.empty()
    st.rerun()
