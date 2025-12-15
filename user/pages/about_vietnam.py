import streamlit as st
from utils.path_config import img

st.markdown(
    """
    <h1 style="text-align:center; font-size:40px; margin-top:10px;">
        🇻🇳 Việt Nam — Đất nước và Con người
    </h1>
    <p style="text-align:center; font-size:18px; color:#bbbbbb; max-width:800px; margin:auto;">
        Việt Nam sở hữu văn hóa lâu đời, cảnh quan phong phú và con người hiền hòa.
        Đây là điểm đến nổi bật thu hút hàng triệu du khách mỗi năm.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.subheader("Các điểm đến nổi bật của Việt Nam")
st.write("Dưới đây là những địa danh được du khách yêu thích nhất:")

destinations = [
    ("Vịnh Hạ Long", "destinations/halong.jpg"),
    ("Phố cổ Hội An", "destinations/hoian.jpg"),
    ("Đà Nẵng", "destinations/danang.jpg"),
    ("Hà Giang Loop", "destinations/ha_giang_loop.jpg"),
    ("Phố Cổ Hà Nội", "destinations/hanoi_old_quarter.jpg"),
    ("TP. Hồ Chí Minh", "destinations/ho_chi_minh_city.jpg"),
    ("Cố đô Huế", "destinations/hue.jpg"),
    ("Nha Trang", "destinations/nhatrang.jpg"),
    ("Phú Quốc", "destinations/phuquoc.jpg"),
    ("Sa Pa", "destinations/sapa.jpg"),
]

for i in range(0, len(destinations), 4):
    row_items = destinations[i:i+4]
    cols = st.columns(4)

    for col, (title, path) in zip(cols, row_items):
        with col:
            st.image(img(path))
            st.markdown(
                f"<p style='text-align:center; font-weight:bold;'>{title}</p>",
                unsafe_allow_html=True
            )

st.markdown("---")

st.subheader("Vì sao du khách quốc tế yêu thích Việt Nam?")
st.write(
    """
- Con người thân thiện, hiếu khách  
- Ẩm thực đa dạng và giá cả hợp lý  
- Thiên nhiên phong phú: biển, núi, cao nguyên, sông nước  
- Nhiều di sản văn hóa & thiên nhiên của UNESCO  
- Chi phí du lịch phải chăng, an toàn, tiện lợi  
"""
)
