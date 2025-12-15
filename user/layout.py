import streamlit as st

def init_layout():
    st.markdown("""
    <style>

    body {
        font-family: "Segoe UI", sans-serif;
        background-color: #0d0d0d;
        color: #f2f2f2;
    }

    .chat-row {
        display: flex;
        align-items: flex-start;
        margin-bottom: 16px;
    }

    .avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
    }

    .bubble-user {
        background: linear-gradient(135deg, #2ecc71, #1abc9c);
        padding: 12px 16px;
        border-radius: 14px;
        max-width: 70%;
        margin-left: auto;
        font-size: 16px;
        color: white;
    }

    .bubble-ai {
        background: linear-gradient(135deg, #34495e, #2c3e50);
        padding: 12px 16px;
        border-radius: 14px;
        max-width: 70%;
        margin-right: auto;
        font-size: 16px;
        color: white;
    }

    .typing {
        width: 60px;
        height: 20px;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-left: 50px;
    }

    .dot {
        width: 10px;
        height: 10px;
        background-color: #ccc;
        border-radius: 50%;
        animation: blink 1.4s infinite both;
    }

    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes blink {
        0% { opacity: 0.2; }
        20% { opacity: 1; }
        100% { opacity: 0.2; }
    }

    </style>
    """, unsafe_allow_html=True)


def chat_bubble_user(text, avatar):
    st.markdown(
        f"""
        <div class="chat-row" style="justify-content: flex-end;">
            <div class="bubble-user">{text}</div>
            <img class="avatar" src="data:image/png;base64,{avatar}">
        </div>
        """,
        unsafe_allow_html=True
    )


def chat_bubble_ai(text, avatar):
    st.markdown(
        f"""
        <div class="chat-row">
            <img class="avatar" src="data:image/png;base64,{avatar}">
            <div class="bubble-ai">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def ai_typing_animation(avatar):
    st.markdown(
        f"""
        <div class="chat-row">
            <img class="avatar" src="data:image/png;base64,{avatar}">
            <div class="typing">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
