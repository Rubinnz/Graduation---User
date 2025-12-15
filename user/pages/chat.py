import streamlit as st
import requests
import uuid
import base64
import os

API_CHAT_URL = "http://localhost:8000/chat"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

avatar_ai = img_to_b64(os.path.join(BASE_DIR, "images/chatbot/chatbot_avatar.png"))
avatar_user = img_to_b64(os.path.join(BASE_DIR, "images/chatbot/user_avatar.png"))

from layout import init_layout, chat_bubble_user, chat_bubble_ai, ai_typing_animation

st.set_page_config(page_title="Chatbot Du Lịch Việt Nam", layout="wide")
init_layout()

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending" not in st.session_state:
    st.session_state.pending = None

user_id = st.session_state.user_id

with st.sidebar:
    st.subheader("Cuộc hội thoại")
    st.write(f"Phiên hiện tại: {user_id[:8]}")
    if st.button("Tạo phiên mới"):
        st.session_state.user_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

st.markdown(
    "<h1 style='text-align:center; margin-bottom:20px;'>💬 Chatbot Du Lịch Việt Nam</h1>",
    unsafe_allow_html=True
)

for m in st.session_state.messages:
    if m["role"] == "user":
        chat_bubble_user(m["content"], avatar_user)
    else:
        chat_bubble_ai(m["content"], avatar_ai)

def on_submit():
    st.session_state.pending = st.session_state.msg
    st.session_state.msg = ""

st.chat_input("Nhập câu hỏi của bạn...", key="msg", on_submit=on_submit)

if st.session_state.pending:
    q = st.session_state.pending
    st.session_state.pending = None

    st.session_state.messages.append({"role": "user", "content": q})
    chat_bubble_user(q, avatar_user)

    ai_typing_animation(avatar_ai)

    try:
        res = requests.post(API_CHAT_URL, json={"query": q})
        answer = res.json().get("answer", "Không nhận được phản hồi từ API.")
    except:
        answer = "Không kết nối được backend API."

    st.session_state.messages.append({"role": "ai", "content": answer})
    st.rerun()
