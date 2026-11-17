import streamlit as st

APP_TITLE = "PIBOT – Raspberry Pi AI Assistant"
DEVELOPER_NAME = "Engr. Bilal Mehmood"

# Locked Model & Temperature Configuration
MODEL_NAME = "gpt-6-luna"
TEMPERATURE = 1.0


def get_api_key() -> str:
    """Retrieves the OpenAI API key exclusively from Streamlit Secrets."""
    try:
        return st.secrets["OPENAI_API_KEY"].strip()
    except (KeyError, FileNotFoundError):
        return ""


SUPPORTED_BOARDS = [
    "Raspberry Pi 5 (RP1 I/O Controller)",
    "Raspberry Pi 4 Model B (BCM2711)",
    "Both / Hardware-Agnostic",
]

LANGUAGES = [
    "Auto-Detect (English / Urdu)",
    "English",
    "Urdu (اردو)",
]

QUICK_PROMPTS = {
    "🔌 Ultrasonic Distance Sensor (HC-SR04)": (
        "Provide step-by-step wiring (including voltage divider for 5V ECHO to 3.3V GPIO) "
        "and complete Python code using gpiozero to read distance from an HC-SR04 sensor."
    ),
    "📷 Pi Camera AI Object Detection": (
        "Give me a complete project structure, requirements.txt, and Python code using "
        "picamera2 and OpenCV to capture frames and run real-time motion/object detection."
    ),
    "⚙️ L298N DC Motor Control": (
        "Show pinout wiring and Python code to control two DC motors (forward, reverse, "
        "PWM speed control) using an L298N motor driver."
    ),
    "🌡️ I2C BME280 Sensor + Troubleshooting": (
        "How do I enable I2C on Raspberry Pi OS, verify the sensor with i2cdetect, "
        "and read temperature, humidity, and pressure in Python?"
    ),
}
