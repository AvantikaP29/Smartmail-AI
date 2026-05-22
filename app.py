import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure your free Gemini key (Reads GEMINI_API_KEY from your .env file)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartMail AI",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS (Updated to Dark/Midnight Theme) ─────────────────────────────────
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 720px; }

    /* App Dark Background Fix */
    .stApp { background-color: #0f111a !important; }

    /* Header card */
    .header-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        color: white;
        display: flex;
        align-items: center;
        gap: 1rem;
        border: 1px solid #1f293d;
    }

    .header-title {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .header-subtitle {
        font-size: 0.9rem;
        opacity: 0.7;
        margin: 0.25rem 0 0;
        font-weight: 300;
    }

    /* Section Label */
    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 0.75rem;
    }

    /* Streamlit text area override (Dark Background inputs) */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1.5px solid #1e293b !important;
        font-size: 0.9rem !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.6 !important;
        background: #161b26 !important;
        color: #f8fafc !important;
        transition: border-color 0.2s !important;
    }

    .stTextArea textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79,70,229,0.15) !important;
        background: #161b26 !important;
    }

    /* Tone selector alignment fix */
    .stButton > button {
        width: 100%;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
    }

    /* Primary Generate button custom gradient styling */
    div.stButton > button[key="generate_btn"] {
        background: linear-gradient(135deg, #4f46e5, #0f3460) !important;
        color: white !important;
        border: none !important;
    }

    div.stButton > button[key="generate_btn"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
    }

    /* Result header */
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #1e293b;
    }

    .result-label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94a3b8;
    }

    .tone-tag {
        background: #064e3b;
        color: #34d399;
        border: 1px solid #059669;
        border-radius: 100px;
        padding: 3px 10px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    /* Status messages */
    .stAlert { border-radius: 10px !important; }

    /* Footer */
    .footer-text {
        text-align: center;
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-card">
    <div style="font-size:2.8rem; line-height:1">📧</div>
    <div>
        <h1 class="header-title">SmartMail AI</h1>
        <p class="header-subtitle">Generate professional email replies in seconds</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tone Config ────────────────────────────────────────────────────────────────
TONES = {
    "Professional": {
        "emoji": "💼",
        "desc": "Polished and business-appropriate",
        "prompt_hint": "Use a professional, business-appropriate tone. Be clear, direct, and courteous."
    },
    "Friendly": {
        "emoji": "😊",
        "desc": "Warm and conversational",
        "prompt_hint": "Use a warm, friendly, and conversational tone. Sound approachable and personable."
    },
    "Formal": {
        "emoji": "🏛️",
        "desc": "Structured and official",
        "prompt_hint": "Use a highly formal tone with proper salutations and structured language suitable for official correspondence."
    },
    "Concise": {
        "emoji": "⚡",
        "desc": "Short and to the point",
        "prompt_hint": "Be extremely concise. Keep the reply to 3–5 sentences max. No fluff."
    },
    "Apologetic": {
        "emoji": "🙏",
        "desc": "Empathetic and sorry",
        "prompt_hint": "Use an apologetic and empathetic tone. Acknowledge any issues and express genuine regret."
    },
    "Assertive": {
        "emoji": "💪",
        "desc": "Confident and firm",
        "prompt_hint": "Use a confident, assertive tone. Be firm and clear without being rude."
    },
}

# ─── Session State ───────────────────────────────────────────────────────────────
if "selected_tone" not in st.session_state:
    st.session_state.selected_tone = "Professional"
if "generated_reply" not in st.session_state:
    st.session_state.generated_reply = ""

# ─── Input Section ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">📩 Email or Message</div>', unsafe_allow_html=True)
email_content = st.text_area(
    label="Email content",
    label_visibility="collapsed",
    placeholder="Paste the email or message you want to reply to here...",
    height=180,
    key="email_input"
)

# ─── Tone Selector ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:1rem">🎨 Reply Tone</div>', unsafe_allow_html=True)

cols = st.columns(3)
tone_keys = list(TONES.keys())
for i, tone in enumerate(tone_keys):
    with cols[i % 3]:
        is_selected = st.session_state.selected_tone == tone

        # Inject styled custom button via Streamlit button
        if st.button(
                f"{TONES[tone]['emoji']} {tone}",
                key=f"tone_{tone}",
                help=TONES[tone]["desc"],
                use_container_width=True
        ):
            st.session_state.selected_tone = tone
            st.session_state.generated_reply = ""
            st.rerun()

# Dynamic visual treatment for selected tone badge style
for tone in TONES.keys():
    if st.session_state.selected_tone == tone:
        st.markdown(f"""
        <style>
        div.stButton > button[key="tone_{tone}"] {{
            background: linear-gradient(135deg, #1a1a2e, #0f3460) !important;
            color: white !important;
            border: 2px solid #4f46e5 !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <style>
        div.stButton > button[key="tone_{tone}"] {{
            background: #161b26 !important;
            color: #cdd9e5 !important;
            border: 1.5px solid #1e293b !important;
        }}
        </style>
        """, unsafe_allow_html=True)

# Show selected tone description
active_tone = st.session_state.selected_tone
st.markdown(
    f'<p style="font-size:0.8rem; color:#94a3b8; margin:0.4rem 0 1rem;">'
    f'{TONES[active_tone]["emoji"]} <strong>{active_tone}</strong> — {TONES[active_tone]["desc"]}'
    f'</p>',
    unsafe_allow_html=True
)

# ─── Generate Button ─────────────────────────────────────────────────────────────
generate_clicked = st.button("✨  Generate Reply", key="generate_btn", use_container_width=True)

# ─── Generation Logic (Switched to Gemini API) ──────────────────────────────────
if generate_clicked:
    if not email_content.strip():
        st.warning("⚠️  Please paste an email or message before generating.")
    elif not os.getenv("GEMINI_API_KEY"):
        st.error("❌  GEMINI_API_KEY not found. Please add it to your .env file.")
    else:
        tone_info = TONES[st.session_state.selected_tone]
        prompt = f"""You are a professional email assistant.

Generate a reply to the email below. {tone_info['prompt_hint']}

Requirements:
- Write only the reply body (no subject line)
- Use proper greeting and sign-off
- Keep it well-structured and clear
- Match the requested tone throughout

Email to reply to:
\"\"\"
{email_content}
\"\"\"
"""
        with st.spinner("Composing your reply..."):
            try:
                # Initialize Gemini model
                model = genai.GenerativeModel(
                    "gemini-2.5-flash",
                    system_instruction="You are an expert email assistant. Write professional, contextually appropriate email replies."
                )

                # Request text generation
                response = model.generate_content(prompt)

                st.session_state.generated_reply = response.text.strip()

            except Exception as e:
                st.error(f"❌ Error generating reply: {str(e)}")

# ─── Result Display ──────────────────────────────────────────────────────────────
if st.session_state.generated_reply:
    tone_emoji = TONES[st.session_state.selected_tone]["emoji"]
    tone_name = st.session_state.selected_tone

    st.markdown("---")
    st.markdown(
        f'<div class="result-header">'
        f'  <span class="result-label">✅ Generated Reply</span>'
        f'  <span class="tone-tag">{tone_emoji} {tone_name}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.text_area(
        label="Reply output",
        label_visibility="collapsed",
        value=st.session_state.generated_reply,
        height=260,
        key="reply_output"
    )

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(
            '<p style="font-size:0.75rem;color:#64748b;margin:0.5rem 0 0;">'
            '💡 You can edit the reply above before copying.'
            '</p>',
            unsafe_allow_html=True
        )
    with col3:
        if st.button("🔄  Regenerate", use_container_width=True, key="regen_btn"):
            st.session_state.generated_reply = ""
            st.rerun()

# ─── Footer ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<p class="footer-text">SmartMail AI · Powered by Google Gemini · Built with Streamlit</p>',
    unsafe_allow_html=True
)