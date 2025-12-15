import streamlit as st
import requests

st.set_page_config(
    page_title="Vietnam Travel AI",
    layout="wide",
    page_icon="🇻🇳",
)

API_URL = "http://localhost:8000"

st.markdown(
    """
    <h1 style="
        text-align:center;
        font-size:42px;
        margin-top:15px;
        margin-bottom:5px;
        font-weight:700;
    ">
        🇻🇳 Vietnam Travel AI – User Portal
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        font-size:18px;
        color:#bbb;
        max-width:850px;
        margin-left:auto;
        margin-right:auto;
        line-height:1.6;
    ">
        Hệ thống AI hỗ trợ tư vấn du lịch Việt Nam, phân tích đánh giá của du khách quốc tế,
        gợi ý địa điểm, ẩm thực, văn hóa và thông tin hữu ích dựa trên dữ liệu thực tế.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.subheader("Các tính năng chính")

st.markdown(
    """
    - Giới thiệu về đất nước & con người Việt Nam  
    - Ẩm thực & văn hóa Việt Nam  
    - Chatbot AI tư vấn du lịch theo thời gian thực  
    - Dashboard phân tích đánh giá du lịch từ khách quốc tế  

    Sử dụng **sidebar bên trái** để điều hướng giữa các trang.
    """
)

# Nút chuyển sang chatbot nhanh
if st.button("Bắt đầu trò chuyện với AI 🤖", use_container_width=True):
    st.switch_page("pages/chat.py")
