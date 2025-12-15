import streamlit as st
import pandas as pd
import altair as alt
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data")

def data(path):
    return os.path.join(DATA_DIR, path)

st.title("📊 Dashboard Đánh Giá Du Lịch Việt Nam")
st.write("Dữ liệu được phân tích từ các bài đánh giá du khách quốc tế.")

df_sentiment = pd.read_csv(data("sentiment_result.csv"))
df_emotion = pd.read_csv(data("emotion_result.csv"))
df_topic = pd.read_csv(data("topic_result.csv"))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Phân bố Sentiment")
    chart = alt.Chart(df_sentiment).mark_bar().encode(
        x='sentiment',
        y='count()',
        color='sentiment'
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.subheader("Phân bố Emotion")
    chart2 = alt.Chart(df_emotion).mark_bar().encode(
        x='emotion',
        y='count()',
        color='emotion'
    )
    st.altair_chart(chart2, use_container_width=True)

st.subheader("Top Topics")
topic_count = df_topic["topic"].value_counts().reset_index()
topic_count.columns = ["topic", "count"]

st.bar_chart(topic_count, x="topic", y="count")
