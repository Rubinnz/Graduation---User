import streamlit as st
import sys, os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from utils.path_config import img

st.markdown(
    """
    <h1 style="text-align:center; font-size:40px; margin-top:10px;">
        🍜 Ẩm Thực Việt Nam
    </h1>
    <p style="text-align:center; font-size:18px; color:#bbbbbb; max-width:800px; margin:auto;">
        Ẩm thực Việt Nam nổi tiếng với sự hòa quyện tinh tế giữa mặn – ngọt – chua – cay,
        mang lại hương vị độc đáo khó quên cho du khách trong và ngoài nước.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.subheader("Các món ăn tiêu biểu của Việt Nam")

foods = [
    ("Phở", "food/pho.jpg"),
    ("Bánh mì", "food/banhmi.jpg"),
    ("Gỏi cuốn", "food/goicuon.jpg"),
    ("Bún chả", "food/buncha.jpg"),
    ("Cao lầu", "food/cao_lau.jpg"),
    ("Cơm tấm", "food/comtam.jpg"),
    ("Bánh xèo", "food/banhxeo.jpg"),
]

# Grid 4 ảnh mỗi hàng
for i in range(0, len(foods), 4):
    row_items = foods[i:i+4]
    cols = st.columns(4)

    for col, (title, path) in zip(cols, row_items):
        with col:
            st.image(img(path))
            st.markdown(f"<p style='text-align:center; font-weight:bold;'>{title}</p>", unsafe_allow_html=True)

st.markdown("---")

st.subheader("Đặc trưng ẩm thực theo vùng miền")
st.write(
    """
- **Miền Bắc**: Hương vị thanh đạm, nhẹ nhàng  
- **Miền Trung**: Đậm đà, cay nồng, nhiều gia vị  
- **Miền Nam**: Vị ngọt, béo, phong phú nguyên liệu  
"""
)
