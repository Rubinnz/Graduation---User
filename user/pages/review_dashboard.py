import re
import os
import html
import base64
from datetime import datetime, timezone

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import altair as alt

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Sentiment on Twitter About Traveling in Vietnam",
    layout="wide",
    page_icon="💬",
)

st.session_state.setdefault("_a11_token_twitter_dash", 0)
st.session_state["_a11_token_twitter_dash"] += 1
A11_TOKEN = st.session_state["_a11_token_twitter_dash"]

st.session_state.setdefault("_quick_seed", int.from_bytes(os.urandom(4), "little"))
st.session_state.setdefault("_last_fetch_utc", None)

def render_html(s: str):
    cleaned = "\n".join(line.lstrip(" \t") for line in s.splitlines()).strip()
    st.markdown(cleaned, unsafe_allow_html=True)

def esc(x) -> str:
    return html.escape(str(x), quote=True)

def detect_first_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None

def detect_text_column(df: pd.DataFrame) -> str | None:
    return detect_first_col(df, ["clean_tweet", "review_text", "vietnam_segment", "text", "content"])

def detect_time_column(df: pd.DataFrame) -> str | None:
    return detect_first_col(df, ["created_at", "createdAt", "timestamp", "time", "datetime", "date", "posted_at"])

def detect_user_column(df: pd.DataFrame) -> str | None:
    return detect_first_col(df, ["username", "user", "screen_name", "author", "user_name", "handle"])

def detect_id_column(df: pd.DataFrame) -> str | None:
    return detect_first_col(df, ["tweet_id", "id", "status_id", "post_id"])

def detect_lang_column(df: pd.DataFrame) -> str | None:
    return detect_first_col(df, ["lang", "language"])

def detect_engagement_cols(df: pd.DataFrame) -> dict:
    return {
        "likes": detect_first_col(df, ["like_count", "likes", "favorite_count", "favourites"]),
        "retweets": detect_first_col(df, ["retweet_count", "retweets", "repost_count"]),
        "replies": detect_first_col(df, ["reply_count", "replies"]),
        "quotes": detect_first_col(df, ["quote_count", "quotes"]),
    }

def normalize_sentiment(s) -> str:
    x = str(s).strip().lower()
    if x in {"pos", "positive", "positve"}:
        return "positive"
    if x in {"neu", "neutral"}:
        return "neutral"
    if x in {"neg", "negative"}:
        return "negative"
    return "other"

def to_dt(series: pd.Series) -> pd.Series:
    x = pd.to_datetime(series, errors="coerce", utc=True)
    if x.notna().any():
        return x
    return pd.to_datetime(series.astype(str), errors="coerce", utc=True)

def highlight(text: str, q: str) -> str:
    safe = esc(text)
    q = q.strip()
    if not q:
        return safe
    pat = re.compile(re.escape(q), re.IGNORECASE)
    return pat.sub(lambda m: f"<mark>{m.group(0)}</mark>", safe)

STOPWORDS = {
    "the","and","for","with","that","this","you","your","are","was","were","have","has","had","but","not","from","they","them",
    "what","when","where","why","how","about","into","out","over","under","just","like","very","really","more","most","less",
    "its","it's","im","i'm","ive","i've","we","our","us","me","my","mine","their","there","here","than","then","too","also",
    "in","on","at","to","of","a","an","is","it","as","be","by","or","if","so","do","did","does","can","could","should","would",
    "rt","via","amp","https","http","co","t","vn","vietnam"
}

def top_terms(texts: pd.Series, n: int = 20) -> pd.DataFrame:
    tokens = []
    for t in texts.dropna().astype(str).tolist():
        for w in re.findall(r"[a-zA-Z]{3,}", t.lower()):
            if w in STOPWORDS:
                continue
            tokens.append(w)
    if not tokens:
        return pd.DataFrame(columns=["term", "count"])
    s = pd.Series(tokens).value_counts().head(n).reset_index()
    s.columns = ["term", "count"]
    return s

@st.cache_data(show_spinner=False, ttl=120)
def fetch_reviews() -> pd.DataFrame:
    try:
        res = requests.get(f"{BACKEND_URL}/fetch/topics", timeout=15)
        if not res.ok:
            return pd.DataFrame()
        data = res.json().get("data", [])
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()

def sample_by_seed(df: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    if df.empty:
        return df
    n = max(0, min(n, len(df)))
    if n == 0:
        return df.head(0)
    s = df.sample(frac=1.0, random_state=seed) if len(df) > 1 else df
    return s.head(n)

render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"]  {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif !important;
}

.stApp {
  background:
    radial-gradient(1000px 520px at 10% 5%, rgba(46,196,182,0.13), rgba(0,0,0,0) 60%),
    radial-gradient(900px 500px at 90% 8%, rgba(255,159,28,0.10), rgba(0,0,0,0) 60%),
    radial-gradient(800px 460px at 80% 95%, rgba(231,29,54,0.08), rgba(0,0,0,0) 55%),
    #ffffff;
}

.block-container { max-width: 1220px; padding-top: 1.1rem; padding-bottom: 2.2rem; }

.hr {
  height: 1px;
  background: linear-gradient(90deg, rgba(0,0,0,0), rgba(15,23,42,.12), rgba(0,0,0,0));
  margin: 18px 0 16px 0;
  border-radius: 999px;
}

.hero {
  position: relative;
  border-radius: 20px;
  padding: 18px 18px 16px 18px;
  border: 1px solid rgba(15,23,42,.10);
  background: rgba(255,255,255,.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 14px 36px rgba(15,23,42,.07);
  overflow:hidden;
}
.hero:before{
  content:"";
  position:absolute; inset:-2px;
  background:
    radial-gradient(520px 260px at 18% 40%, rgba(46,196,182,0.16), rgba(0,0,0,0) 60%),
    radial-gradient(520px 260px at 82% 22%, rgba(255,159,28,0.13), rgba(0,0,0,0) 60%);
  pointer-events:none;
}
.hero-inner{ position:relative; z-index:1; }
.hero h1{
  margin: 0;
  font-weight: 900;
  font-size: 34px;
  letter-spacing: -0.6px;
  text-align:center;
}
.hero p{
  margin: 8px auto 0 auto;
  text-align:center;
  font-size: 14.5px;
  color: rgba(100,116,139,.95);
  line-height: 1.65;
  max-width: 980px;
}
.hero-badges{
  display:flex; justify-content:center; gap:10px; flex-wrap:wrap;
  margin-top: 10px;
}
.pill{
  display:inline-flex; align-items:center; gap:8px;
  border: 1px solid rgba(15,23,42,.10);
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
  background: rgba(248,250,252,1);
  color: rgba(30,41,59,.92);
}

.panel {
  border-radius: 18px;
  border: 1px solid rgba(15,23,42,.10);
  background: rgba(255,255,255,.78);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 12px 30px rgba(15,23,42,.06);
  padding: 12px 12px;
}

.note {
  border-radius: 18px;
  border: 1px solid rgba(15,23,42,.10);
  background: rgba(248,250,252,1);
  padding: 12px 12px;
  color: rgba(51,65,85,.95);
}

.sample {
  border-radius: 18px;
  border: 1px solid rgba(15,23,42,.10);
  background: rgba(255,255,255,.86);
  box-shadow: 0 10px 26px rgba(15,23,42,.06);
  padding: 12px 12px;
  transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
}
.sample:hover{
  transform: translateY(-3px);
  box-shadow: 0 16px 40px rgba(15,23,42,.10);
  border-color: rgba(46,196,182,.30);
}
.sample .txt{
  font-size: 14px;
  color: rgba(15,23,42,.92);
  line-height: 1.65;
}
.sample .meta{
  margin-top: 8px;
  font-size: 12px;
  color: rgba(100,116,139,.95);
}
.badge {
  display:inline-flex; align-items:center;
  border: 1px solid rgba(15,23,42,.12);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  background: rgba(248,250,252,1);
  margin-right: 6px;
  margin-top: 6px;
}
mark{
  background: rgba(255, 159, 28, .22);
  padding: 0 3px;
  border-radius: 6px;
}

.section-title{
  font-weight: 900;
  font-size: 18px;
  margin: 8px 0 8px 0;
  letter-spacing: -.25px;
}
.section-sub{
  margin-top:-4px;
  color: rgba(100,116,139,.95);
  font-size: 13px;
}

.reveal { opacity: 1; transform: none; }
.js-reveal .reveal.a11-managed {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity .65s ease, transform .65s ease;
  will-change: opacity, transform;
}
.js-reveal .reveal.a11-managed.show { opacity: 1; transform: translateY(0); }

</style>
""")

render_html("""
<div class="hero">
  <div class="hero-inner">
    <h1>💬 Twitter Sentiment on Traveling in Vietnam</h1>
    <p>
      A compact review dashboard for topic sentiment, emotions, and representative snippets from English-language travel-related tweets.
      Data is social-media self-reporting for analytical/illustrative use.
    </p>
    <div class="hero-badges">
      <span class="pill">Sentiment • Emotion • Topics</span>
      <span class="pill">Filterable • Exportable</span>
      <span class="pill">Fast sampling • Scroll reveal</span>
    </div>
  </div>
</div>
<div class="hr"></div>
""")

with st.sidebar:
    st.subheader("Controls")
    colr1, colr2 = st.columns([1, 1])
    with colr1:
        if st.button("🔄 Refresh data", use_container_width=True):
            st.session_state["_quick_seed"] = int.from_bytes(os.urandom(4), "little")
            fetch_reviews.clear()
            st.rerun()
    with colr2:
        if st.button("🎲 Shuffle samples", use_container_width=True):
            st.session_state["_quick_seed"] = int.from_bytes(os.urandom(4), "little")
            st.rerun()

    st.caption("Filters apply to charts, snippets, samples, and the dataset.")

df = fetch_reviews()
if df.empty:
    st.warning("No travel-related tweets available (or backend returned empty data).")
    st.stop()

if st.session_state["_last_fetch_utc"] is None:
    st.session_state["_last_fetch_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

TEXT_COL = detect_text_column(df)
required_cols = {"sentiment", "topic_name", "emotion"}
if TEXT_COL is None or not required_cols.issubset(df.columns):
    st.error("Data is incomplete (missing text / sentiment / topic / emotion).")
    st.stop()

TIME_COL = detect_time_column(df)
USER_COL = detect_user_column(df)
ID_COL = detect_id_column(df)
LANG_COL = detect_lang_column(df)
ENG = detect_engagement_cols(df)

df = df.copy()
df["sentiment"] = df["sentiment"].apply(normalize_sentiment)
df["topic_name"] = df["topic_name"].fillna("Unknown").astype(str)
df["emotion"] = df["emotion"].fillna("Unknown").astype(str)
df[TEXT_COL] = df[TEXT_COL].fillna("").astype(str)

if TIME_COL is not None:
    df[TIME_COL] = to_dt(df[TIME_COL])

topics = sorted(df["topic_name"].dropna().unique().tolist())
emotions = sorted(df["emotion"].dropna().unique().tolist())
sentiments = ["positive", "neutral", "negative", "other"]

with st.container():
    filtA, filtB, filtC, filtD = st.columns([1.2, 1.2, 1.2, 1.4])
    with filtA:
        selected_topic = st.selectbox("Topic", ["All"] + topics, index=0)
    with filtB:
        selected_emotions = st.multiselect("Emotion", emotions, default=[])
    with filtC:
        selected_sentiments = st.multiselect("Sentiment", sentiments, default=["positive", "neutral", "negative"])
    with filtD:
        search_text = st.text_input("Search in tweet text", placeholder="e.g., food, Ha Long, traffic...")

    extra1, extra2, extra3, extra4 = st.columns([1.1, 1.1, 1.1, 1.1])
    with extra1:
        min_len = st.slider("Min text length", 0, 220, 0)
    with extra2:
        dedupe = st.toggle("Remove duplicates", value=True)
    with extra3:
        exclude_rt = st.toggle("Exclude RT", value=True)
    with extra4:
        max_rows = st.selectbox("Max rows", [500, 1000, 3000, 10000, "All"], index=2)

fdf = df.copy()

if selected_topic != "All":
    fdf = fdf[fdf["topic_name"] == selected_topic]

if selected_sentiments:
    fdf = fdf[fdf["sentiment"].isin(selected_sentiments)]
else:
    fdf = fdf.iloc[0:0]

if selected_emotions:
    fdf = fdf[fdf["emotion"].isin(selected_emotions)]

if search_text.strip():
    q = search_text.strip().lower()
    fdf = fdf[fdf[TEXT_COL].str.lower().str.contains(q, na=False)]

if min_len > 0:
    fdf = fdf[fdf[TEXT_COL].str.len() >= min_len]

if exclude_rt:
    fdf = fdf[~fdf[TEXT_COL].str.match(r"^\s*rt\s+@?", case=False, na=False)]

if dedupe:
    fdf = fdf.drop_duplicates(subset=[TEXT_COL])

if max_rows != "All":
    fdf = fdf.head(int(max_rows))

render_html('<div class="hr"></div>')

tab_overview, tab_explore, tab_snippets, tab_samples, tab_data = st.tabs(
    ["📌 Overview", "📊 Explore", "🪄 Snippets", "🧭 Samples", "📄 Data"]
)

with tab_overview:
    total = len(fdf)
    if total == 0:
        st.info("No rows match the current filters.")
        st.stop()

    pos_rate = round((fdf["sentiment"] == "positive").mean() * 100, 1)
    neu_rate = round((fdf["sentiment"] == "neutral").mean() * 100, 1)
    neg_rate = round((fdf["sentiment"] == "negative").mean() * 100, 1)
    net = round(pos_rate - neg_rate, 1)

    top_topic = fdf["topic_name"].value_counts().index[0] if not fdf["topic_name"].value_counts().empty else "N/A"
    top_emotion = fdf["emotion"].value_counts().index[0] if not fdf["emotion"].value_counts().empty else "N/A"

    uniq_topics = int(fdf["topic_name"].nunique())
    uniq_emotions = int(fdf["emotion"].nunique())
    uniq_users = int(fdf[USER_COL].nunique()) if USER_COL else None
    avg_len = int(round(fdf[TEXT_COL].str.len().mean(), 0)) if total else 0

    render_html('<div class="panel">')
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Tweets", f"{total:,}")
    k2.metric("😊 Positive", f"{pos_rate}%")
    k3.metric("😐 Neutral", f"{neu_rate}%")
    k4.metric("😟 Negative", f"{neg_rate}%")
    k5.metric("Net score", f"{net}")
    k6.metric("Avg length", f"{avg_len}")
    render_html("</div>")

    render_html(f"""
<div class="note">
  <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
    <div>
      <div style="font-weight:800; margin-bottom:6px;">At-a-glance</div>
      <div>
        <span class="badge">Top topic: <b>{esc(top_topic)}</b></span>
        <span class="badge">Top emotion: <b>{esc(top_emotion)}</b></span>
        <span class="badge">Topics: <b>{esc(uniq_topics)}</b></span>
        <span class="badge">Emotions: <b>{esc(uniq_emotions)}</b></span>
        {f'<span class="badge">Users: <b>{esc(uniq_users)}</b></span>' if uniq_users is not None else ''}
      </div>
    </div>
    <div style="text-align:right; color: rgba(100,116,139,.95); font-size:12px;">
      Last fetch: <b>{esc(st.session_state["_last_fetch_utc"])}</b>
    </div>
  </div>
</div>
""")

    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown('<div class="section-title">Sentiment distribution</div>', unsafe_allow_html=True)
        s_cnt = fdf["sentiment"].value_counts().reset_index()
        s_cnt.columns = ["sentiment", "count"]
        donut = (
            alt.Chart(s_cnt)
            .mark_arc(innerRadius=62)
            .encode(
                theta=alt.Theta("count:Q"),
                color=alt.Color("sentiment:N", legend=alt.Legend(title="Sentiment")),
                tooltip=["sentiment:N", "count:Q"],
            )
            .properties(height=320)
        )
        st.altair_chart(donut, use_container_width=True)

    with c2:
        st.markdown('<div class="section-title">Top topics</div>', unsafe_allow_html=True)
        t_cnt = fdf["topic_name"].value_counts().head(12).reset_index()
        t_cnt.columns = ["topic_name", "count"]
        bar = (
            alt.Chart(t_cnt)
            .mark_bar()
            .encode(
                x=alt.X("count:Q", title="Tweets"),
                y=alt.Y("topic_name:N", sort="-x", title="Topic"),
                tooltip=["topic_name:N", "count:Q"],
            )
            .properties(height=320)
        )
        st.altair_chart(bar, use_container_width=True)

    if TIME_COL is not None and pd.api.types.is_datetime64_any_dtype(fdf[TIME_COL]):
        tf = fdf.dropna(subset=[TIME_COL]).copy()
        if not tf.empty:
            st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Sentiment trend</div><div class="section-sub">Daily counts in the current filtered view</div>', unsafe_allow_html=True)
            tf["day"] = tf[TIME_COL].dt.floor("D")
            ts = tf.groupby(["day", "sentiment"]).size().reset_index(name="count")
            line = (
                alt.Chart(ts)
                .mark_line(point=True)
                .encode(
                    x=alt.X("day:T", title="Day"),
                    y=alt.Y("count:Q", title="Tweets"),
                    color=alt.Color("sentiment:N", title="Sentiment"),
                    tooltip=["day:T", "sentiment:N", "count:Q"],
                )
                .properties(height=280)
            )
            st.altair_chart(line, use_container_width=True)

with tab_explore:
    if len(fdf) == 0:
        st.info("No rows match the current filters.")
        st.stop()

    left, right = st.columns([1, 1])

    with left:
        st.markdown('<div class="section-title">Emotion distribution</div><div class="section-sub">Top 12 in the filtered view</div>', unsafe_allow_html=True)
        e_cnt = fdf["emotion"].value_counts().head(12).reset_index()
        e_cnt.columns = ["emotion", "count"]
        ebar = (
            alt.Chart(e_cnt)
            .mark_bar()
            .encode(
                x=alt.X("count:Q", title="Tweets"),
                y=alt.Y("emotion:N", sort="-x", title="Emotion"),
                tooltip=["emotion:N", "count:Q"],
            )
            .properties(height=360)
        )
        st.altair_chart(ebar, use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Topic × Sentiment</div><div class="section-sub">Heatmap over top topics</div>', unsafe_allow_html=True)
        pivot = (
            fdf.pivot_table(index="topic_name", columns="sentiment", values=TEXT_COL, aggfunc="count", fill_value=0)
            .reset_index()
        )
        long = pivot.melt(id_vars=["topic_name"], var_name="sentiment", value_name="count")
        top_topics = fdf["topic_name"].value_counts().head(14).index.tolist()
        long = long[long["topic_name"].isin(top_topics)]
        heat = (
            alt.Chart(long)
            .mark_rect()
            .encode(
                x=alt.X("sentiment:N", title="Sentiment"),
                y=alt.Y("topic_name:N", sort=top_topics, title="Topic"),
                color=alt.Color("count:Q", title="Count"),
                tooltip=["topic_name:N", "sentiment:N", "count:Q"],
            )
            .properties(height=360)
        )
        st.altair_chart(heat, use_container_width=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    k1, k2 = st.columns([1.2, 1.0])
    with k1:
        st.markdown('<div class="section-title">Top terms</div><div class="section-sub">Simple tokenization over tweet text</div>', unsafe_allow_html=True)
        terms = top_terms(fdf[TEXT_COL], n=22)
        if terms.empty:
            st.info("Not enough text to extract terms.")
        else:
            term_bar = (
                alt.Chart(terms)
                .mark_bar()
                .encode(
                    x=alt.X("count:Q", title="Occurrences"),
                    y=alt.Y("term:N", sort="-x", title="Term"),
                    tooltip=["term:N", "count:Q"],
                )
                .properties(height=360)
            )
            st.altair_chart(term_bar, use_container_width=True)

    with k2:
        st.markdown('<div class="section-title">Keyword lens</div><div class="section-sub">Sentiment split for a keyword</div>', unsafe_allow_html=True)
        kw = st.text_input("Keyword", value="", placeholder="e.g., food, taxi, beach, visa")
        if kw.strip():
            mask = fdf[TEXT_COL].str.contains(kw.strip(), case=False, na=False)
            kdf = fdf[mask]
            if kdf.empty:
                st.info("No matches for that keyword in the current filters.")
            else:
                kcnt = kdf["sentiment"].value_counts().reindex(sentiments, fill_value=0).reset_index()
                kcnt.columns = ["sentiment", "count"]
                kbar = (
                    alt.Chart(kcnt)
                    .mark_bar()
                    .encode(
                        x=alt.X("count:Q", title="Tweets"),
                        y=alt.Y("sentiment:N", sort=sentiments, title="Sentiment"),
                        tooltip=["sentiment:N", "count:Q"],
                    )
                    .properties(height=260)
                )
                st.altair_chart(kbar, use_container_width=True)
        else:
            st.info("Enter a keyword to analyze sentiment for matching tweets.")

with tab_snippets:
    if len(fdf) == 0:
        st.info("No rows match the current filters.")
        st.stop()

    st.markdown('<div class="section-title">What people say</div><div class="section-sub">Shuffle for new picks; search highlights are supported</div>', unsafe_allow_html=True)

    a, b, c = st.columns([1.0, 1.0, 1.0])
    with a:
        n_show = st.slider("Snippets to show", 4, 24, 10)
    with b:
        two_cols = st.toggle("Two columns", value=True)
    with c:
        show_full = st.toggle("Show full text", value=False)

    sample = sample_by_seed(fdf.reset_index(drop=True), n_show, st.session_state["_quick_seed"])

    cols = st.columns(2) if two_cols else [st.container()]
    for i, r in sample.iterrows():
        tgt = cols[i % 2] if two_cols else cols[0]
        with tgt:
            txt = str(r[TEXT_COL])
            content = txt if show_full else ((txt[:280] + "…") if len(txt) > 280 else txt)
            render_html(f"""
<div class="sample reveal" data-a11-token="{A11_TOKEN}">
  <div class="txt">“{highlight(content, search_text)}”</div>
  <div class="meta">
    <span class="badge">Topic: <b>{esc(r["topic_name"])}</b></span>
    <span class="badge">Sentiment: <b>{esc(r["sentiment"])}</b></span>
    <span class="badge">Emotion: <b>{esc(r["emotion"])}</b></span>
  </div>
</div>
""")

with tab_samples:
    if len(fdf) == 0:
        st.info("No rows match the current filters.")
        st.stop()

    st.markdown('<div class="section-title">Representative examples</div><div class="section-sub">Balanced sampling for quick review</div>', unsafe_allow_html=True)

    def pick(df0: pd.DataFrame, s: str, n: int):
        x = df0[df0["sentiment"] == s]
        if x.empty:
            return x
        seed = st.session_state["_quick_seed"] ^ (hash(s) & 0xFFFFFFFF)
        return sample_by_seed(x.reset_index(drop=True), n, seed)

    pcol, ncol, gcol = st.columns(3)
    pos_df = pick(fdf, "positive", 4)
    neu_df = pick(fdf, "neutral", 4)
    neg_df = pick(fdf, "negative", 4)

    def render_block(title: str, icon: str, xdf: pd.DataFrame):
        st.markdown(f"### {icon} {title}")
        if xdf.empty:
            render_html("<div style='color:rgba(100,116,139,.95);'>No matching tweets available.</div>")
            return
        for _, r in xdf.iterrows():
            txt = str(r[TEXT_COL])
            short = (txt[:320] + "…") if len(txt) > 320 else txt
            render_html(f"""
<div class="sample reveal" data-a11-token="{A11_TOKEN}">
  <div class="txt">“{highlight(short, search_text)}”</div>
  <div class="meta">
    <span class="badge">Topic: <b>{esc(r["topic_name"])}</b></span>
    <span class="badge">Emotion: <b>{esc(r["emotion"])}</b></span>
  </div>
</div>
""")
            with st.expander("Show full tweet"):
                st.write(txt)

    with pcol:
        render_block("Positive picks", "😊", pos_df)
    with ncol:
        render_block("Neutral picks", "😐", neu_df)
    with gcol:
        render_block("Negative picks", "😟", neg_df)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Auto insights</div>', unsafe_allow_html=True)

    topic_counts = fdf["topic_name"].value_counts()
    if not topic_counts.empty:
        top_topics = topic_counts.head(6).index.tolist()
        tmp = fdf[fdf["topic_name"].isin(top_topics)].copy()
        tmp["pos"] = (tmp["sentiment"] == "positive").astype(int)
        tmp["neg"] = (tmp["sentiment"] == "negative").astype(int)
        score = tmp.groupby("topic_name")[["pos", "neg"]].sum()
        score["net"] = score["pos"] - score["neg"]
        score = score.sort_values("net", ascending=False).reset_index()
        score["label"] = score["topic_name"].astype(str)

        score_long = score.melt(id_vars=["topic_name", "label"], value_vars=["pos", "neg"], var_name="kind", value_name="count")
        diverge = (
            alt.Chart(score_long)
            .mark_bar()
            .encode(
                x=alt.X("count:Q", title="Count"),
                y=alt.Y("label:N", sort=alt.SortField("topic_name", order="ascending"), title="Topic"),
                color=alt.Color("kind:N", title="Type"),
                tooltip=["topic_name:N", "kind:N", "count:Q"],
            )
            .properties(height=260)
        )
        st.altair_chart(diverge, use_container_width=True)
    else:
        st.info("Not enough data to generate topic insights.")

with tab_data:
    if len(fdf) == 0:
        st.info("No rows match the current filters.")
        st.stop()

    st.markdown('<div class="section-title">Dataset</div><div class="section-sub">Choose columns, preview, export</div>', unsafe_allow_html=True)

    base_cols = [c for c in [ID_COL, TIME_COL, USER_COL, LANG_COL, TEXT_COL, "sentiment", "topic_name", "emotion"] if c and c in fdf.columns]
    extra_cols = [c for c in fdf.columns if c not in base_cols]
    default_cols = base_cols[:]
    pick_cols = st.multiselect("Columns", base_cols + extra_cols, default=default_cols)

    view = fdf[pick_cols].reset_index(drop=True) if pick_cols else fdf.reset_index(drop=True)

    st.dataframe(view, use_container_width=True, height=440)

    csv = view.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered CSV",
        data=csv,
        file_name=f"twitter_vietnam_sentiment_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )

components.html(f"""
<script>
(function () {{
  const parent = window.parent;
  const doc = parent.document;
  const TOKEN = "{A11_TOKEN}";

  function getRoot() {{
    return doc.querySelector('.stApp') || doc.body;
  }}

  function inView(el) {{
    const r = el.getBoundingClientRect();
    const vh = parent.innerHeight || doc.documentElement.clientHeight || 800;
    return r.top < vh * 0.92 && r.bottom > 0;
  }}

  function bindRevealForToken() {{
    const root = getRoot();
    const els = Array.from(doc.querySelectorAll('.reveal[data-a11-token="' + TOKEN + '"]'));
    if (!els.length) return false;

    els.forEach(el => el.classList.add('a11-managed'));
    els.forEach(el => {{ if (inView(el)) el.classList.add('show'); }});
    root.classList.add('js-reveal');

    if (doc.__a11TwitterDashIO) {{
      try {{ doc.__a11TwitterDashIO.disconnect(); }} catch (e) {{}}
      doc.__a11TwitterDashIO = null;
    }}

    if (!('IntersectionObserver' in parent)) {{
      els.forEach(el => el.classList.add('show'));
      return true;
    }}

    const io = new parent.IntersectionObserver((entries) => {{
      entries.forEach(e => {{
        if (e.isIntersecting) e.target.classList.add('show');
      }});
    }}, {{ threshold: 0.12, rootMargin: "0px 0px -10% 0px" }});

    doc.__a11TwitterDashIO = io;
    els.forEach(el => io.observe(el));
    return true;
  }}

  let tries = 0;
  const timer = parent.setInterval(() => {{
    tries += 1;
    const ok = bindRevealForToken();
    if (ok || tries >= 80) parent.clearInterval(timer);
  }}, 100);
}})();
</script>
""", height=0)
