import streamlit as st
from streamlit.components.v1 import html as st_html
import base64
import os
import html as pyhtml
from typing import Any

st.set_page_config(
    page_title="Vietnam Travel AI",
    layout="wide",
    page_icon="🇻🇳",
    initial_sidebar_state="expanded",
)

def esc(x: Any) -> str:
    return pyhtml.escape(str(x), quote=True)

def render_html(s: str):
    cleaned = "\n".join(line.lstrip(" \t") for line in s.splitlines()).strip()
    st.markdown(cleaned, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def img_to_data_uri(path: str) -> str:
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    mime = f"image/{ext}"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

st.session_state.setdefault("a11_landing_prompt", "")

image_paths = [
    "images/slider.jpg",
    "images/slider1.jpg",
    "images/slider2.jpg",
    "images/slider3.jpg",
]

data_uris = []
for p in image_paths:
    try:
        data_uris.append(img_to_data_uri(p))
    except Exception:
        pass

render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, .stApp {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif !important;
}

.stApp {
  background:
    radial-gradient(1100px 520px at 12% 6%, rgba(46,196,182,.16), rgba(0,0,0,0) 60%),
    radial-gradient(900px 520px at 88% 8%, rgba(255,159,28,.14), rgba(0,0,0,0) 60%),
    radial-gradient(900px 520px at 82% 94%, rgba(231,29,54,.10), rgba(0,0,0,0) 55%),
    linear-gradient(180deg, rgba(255,255,255,1), rgba(248,250,252,1)) !important;
}

.block-container { max-width: 1240px; padding-top: 3rem; padding-bottom: 2.1rem; }

.a11-hr {
  height: 1px;
  background: linear-gradient(90deg, rgba(0,0,0,0), rgba(148,163,184,.45), rgba(0,0,0,0));
  margin: 18px 0 16px 0;
  border-radius: 999px;
}

.glass {
  border-radius: 22px;
  border: 1px solid rgba(148,163,184,.30);
  background: rgba(255,255,255,.58);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 16px 46px rgba(15,23,42,.10);
}

.hero {
  position: relative;
  overflow: hidden;
  padding: 18px 18px 16px 18px;
}
.hero::before{
  content:"";
  position:absolute; inset:-2px;
  background:
    radial-gradient(720px 320px at 14% 34%, rgba(46,196,182,.18), rgba(0,0,0,0) 60%),
    radial-gradient(720px 320px at 82% 22%, rgba(255,159,28,.15), rgba(0,0,0,0) 60%),
    radial-gradient(720px 320px at 72% 92%, rgba(231,29,54,.10), rgba(0,0,0,0) 60%);
  pointer-events:none;
}
.hero-inner { position: relative; z-index: 1; text-align:center; }
.hero-title {
  font-size: 40px;
  font-weight: 900;
  letter-spacing: -0.9px;
  line-height: 1.12;
  margin: 6px 0 8px 0;
  color: rgba(15,23,42,.95);
  padding-bottom: 2px;
}

.hero-desc {
  font-size: 15.5px;
  color: rgba(71,85,105,.92);
  max-width: 960px;
  margin: 0 auto;
  line-height: 1.75;
}

.pills{
  margin-top: 12px;
  display:flex;
  justify-content:center;
  gap:10px;
  flex-wrap:wrap;
}
.pill{
  display:inline-flex;
  align-items:center;
  gap:8px;
  border: 1px solid rgba(148,163,184,.30);
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
  background: rgba(255,255,255,.62);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: rgba(30,41,59,.92);
}

.section-head {
  display:flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  margin: 0 0 10px 0;
}
.section-title {
  margin: 0;
  font-size: 18px;
  font-weight: 900;
  letter-spacing: -.3px;
  color: rgba(15,23,42,.92);
}
.section-note {
  margin: 0;
  font-size: 12.5px;
  color: rgba(100,116,139,.95);
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}
@media (max-width: 980px){ .stats{ grid-template-columns: repeat(2, minmax(0,1fr)); } }

.stat {
  border-radius: 16px;
  border: 1px solid rgba(148,163,184,.28);
  background: rgba(255,255,255,.52);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 12px 12px;
}
.stat .k { font-weight: 900; font-size: 14px; letter-spacing: -.2px; color: rgba(15,23,42,.92); }
.stat .v { margin-top: 4px; font-size: 12.5px; color: rgba(100,116,139,.95); line-height: 1.55; }

.grid4 {
  display: grid;
  grid-template-columns: repeat(4, minmax(0,1fr));
  gap: 12px;
}
@media (max-width: 1180px){ .grid4{ grid-template-columns: repeat(2, minmax(0,1fr)); } }
@media (max-width: 640px){ .grid4{ grid-template-columns: 1fr; } }

.card {
  border-radius: 18px;
  border: 1px solid rgba(148,163,184,.30);
  background: rgba(255,255,255,.56);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 12px 34px rgba(15,23,42,.08);
  padding: 16px 14px;
  min-height: 176px;
  transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}
.card:hover{
  transform: translateY(-4px);
  box-shadow: 0 18px 44px rgba(15,23,42,.12);
  border-color: rgba(46,196,182,.40);
}
.card .icon {
  width: 38px; height: 38px;
  border-radius: 14px;
  display:flex; align-items:center; justify-content:center;
  border: 1px solid rgba(148,163,184,.28);
  background: rgba(255,255,255,.62);
  font-size: 18px;
}
.card .t {
  margin-top: 10px;
  font-size: 15px;
  font-weight: 900;
  letter-spacing: -.2px;
  color: rgba(15,23,42,.92);
}
.card .d {
  margin-top: 6px;
  font-size: 13px;
  color: rgba(71,85,105,.92);
  line-height: 1.65;
}

.footer {
  text-align:center;
  font-size: 13px;
  color: rgba(100,116,139,.95);
  margin-top: 18px;
}
.footer b { color: rgba(15,23,42,.92); }

.stButton > button {
  border-radius: 14px !important;
  border: 1px solid rgba(148,163,184,.34) !important;
  background: rgba(255,255,255,.60) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 10px 24px rgba(15,23,42,.06) !important;
  color: rgba(15,23,42,.92) !important;
  font-weight: 800 !important;
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(15,23,42,.10) !important;
  border-color: rgba(46,196,182,.45) !important;
}

div[data-testid="stTextInput"] input {
  border-radius: 14px !important;
  border: 1px solid rgba(148,163,184,.34) !important;
  background: rgba(255,255,255,.68) !important;
  box-shadow: 0 10px 24px rgba(15,23,42,.06) !important;
}
</style>
""")

render_html("""
<div class="glass hero">
  <div class="hero-inner">
    <div class="hero-title">Vietnam Travel</div>
    <div class="hero-desc">
      A premium, AI-powered travel companion to help international travelers explore Vietnam - culture, cuisine, etiquette,
      destinations and practical planning - powered by review analytics and conversation - first guidance.
    </div>
    <div class="pills"> 
      <span class="pill">Explore-first (no forced itinerary)</span>
      <span class="pill">Planning when you ask</span>
      <span class="pill">Review analytics</span>
      <span class="pill">Fast chat</span>
    </div>
  </div>
</div>
""")

render_html('<div class="a11-hr"></div>')

# Single-column layout
render_html("""
<div class="glass" style="padding:12px 12px;">
  <div class="section-head">
    <h3 class="section-title">✨ What you can do here</h3>
    <p class="section-note">Culture - first discovery • Plan later</p>
  </div>
  <div class="stats">
    <div class="stat">
      <div class="k">Explore</div>
      <div class="v">Culture, etiquette, history, regions - learn before planning.</div>
    </div>
    <div class="stat">
      <div class="k">Plan</div>
      <div class="v">Routes, budgets, transport, safety - only when requested.</div>
    </div>
    <div class="stat">
      <div class="k">Analyze</div>
      <div class="v">Sentiment + topics from real reviews to understand pain points.</div>
    </div>
    <div class="stat">
      <div class="k">Chat</div>
      <div class="v">Structured answers with controllable depth.</div>
    </div>
  </div>
</div>
""")
render_html('<div class="a11-hr"></div>')

if data_uris:
    imgs_html = "\n".join(
        [f'<img src="{u}" class="a11-slide {"active" if i == 0 else ""}" alt="slide-{i}">' for i, u in enumerate(data_uris)]
    )
    dots_html = "\n".join(
        [f'<button class="a11-dot {"active" if i == 0 else ""}" data-i="{i}" aria-label="dot-{i}"></button>' for i in range(len(data_uris))]
    )
    slider_html = f"""
<div class="glass" style="padding:12px 12px;">
  <div class="section-head">
    <h3 class="section-title">📸 Vietnam highlights</h3>
  </div>

  <div class="a11-slider" id="a11_slider">
    {imgs_html}
    <div class="a11-overlay">
      <div class="a11-ot">Discover Vietnam</div>
      <div class="a11-os">Browse the vibe first - plan only when you’re ready.</div>
    </div>
    <div class="a11-dots">{dots_html}</div>
  </div>
</div>

<style>
.a11-slider {{
  position: relative;
  width: 100%;
  height: 380px;
  overflow: hidden;
  border-radius: 18px;
  border: 1px solid rgba(148,163,184,.30);
  background: rgba(255,255,255,.45);
}}
.a11-slide {{
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 900ms ease-in-out, transform 900ms ease-in-out;
  transform: scale(1.02);
}}
.a11-slide.active {{
  opacity: 1;
  transform: scale(1.00);
}}
.a11-overlay {{
  position:absolute;
  left: 14px;
  bottom: 14px;
  right: 14px;
  padding: 12px 12px;
  border-radius: 16px;
  border: 1px solid rgba(148,163,184,.30);
  background: rgba(255,255,255,.58);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}}
.a11-ot {{
  font-weight: 900;
  letter-spacing: -.2px;
  color: rgba(15,23,42,.92);
  font-size: 16px;
}}
.a11-os {{
  margin-top: 3px;
  font-size: 12.5px;
  color: rgba(71,85,105,.92);
  line-height: 1.5;
}}
.a11-dots {{
  position:absolute;
  top: 12px;
  right: 12px;
  display:flex;
  gap: 6px;
}}
.a11-dot {{
  width: 10px;
  height: 10px;
  border-radius: 999px;
  border: 1px solid rgba(148,163,184,.45);
  background: rgba(255,255,255,.55);
  cursor: pointer;
  transition: transform .18s ease, background .18s ease;
}}
.a11-dot.active {{
  background: rgba(46,196,182,.78);
  transform: scale(1.15);
  border-color: rgba(46,196,182,.78);
}}
</style>

<script>
(function () {{
  const root = document.getElementById("a11_slider");
  if (!root) return;

  const slides = Array.from(root.querySelectorAll(".a11-slide"));
  const dots = Array.from(root.querySelectorAll(".a11-dot"));
  if (!slides.length) return;

  let index = 0;
  let paused = false;

  function setActive(i) {{
    slides[index].classList.remove("active");
    dots[index]?.classList.remove("active");
    index = (i + slides.length) % slides.length;
    slides[index].classList.add("active");
    dots[index]?.classList.add("active");
  }}

  const timer = setInterval(() => {{
    if (paused) return;
    setActive(index + 1);
  }}, 3200);

  root.addEventListener("mouseenter", () => paused = true);
  root.addEventListener("mouseleave", () => paused = false);

  dots.forEach(d => {{
    d.addEventListener("click", () => {{
      const i = Number(d.getAttribute("data-i") || "0");
      setActive(i);
    }});
  }});
}})();
</script>
"""
    st_html(slider_html, height=460)
else:
    render_html("""
<div class="glass" style="padding:14px 14px;">
  <div class="section-head">
    <h3 class="section-title">📸 Vietnam highlights</h3>
    <p class="section-note">Missing images</p>
  </div>
  <div style="color:rgba(100,116,139,.95); font-size:13.5px; line-height:1.6;">
    Add images in <b>images/</b> (slider.jpg, slider1.jpg, slider2.jpg, slider3.jpg) to enable the carousel.
  </div>
</div>
""")

render_html('<div class="a11-hr"></div>')

render_html("""
<div class="section-head">
  <h3 class="section-title">🌟 Key Features</h3>
  <p class="section-note">Clean UX • Practical value</p>
</div>

<div class="grid4">
  <div class="card">
    <div class="icon">🌏</div>
    <div class="t">Discover Vietnam</div>
    <div class="d">Geography, regions, people and iconic destinations with traveler-friendly context.</div>
  </div>

  <div class="card">
    <div class="icon">🍜</div>
    <div class="t">Cuisine & Culture</div>
    <div class="d">Regional dishes, ordering tips, etiquette and authentic local experiences.</div>
  </div>

  <div class="card">
    <div class="icon">🤖</div>
    <div class="t">AI Travel Assistant</div>
    <div class="d">Ask naturally. Get structured answers. Plan only when you want to.</div>
  </div>

  <div class="card">
    <div class="icon">📊</div>
    <div class="t">Review Analytics</div>
    <div class="d">Sentiment + topics from real reviews to understand what travelers love or dislike.</div>
  </div>
</div>
""")

render_html("""
<div class="footer">
  Use the <b>left sidebar</b> to navigate across pages. This landing is designed to feel premium and travel-native.
</div>
""")

go = st.button("🚀 Start chatting with AI", use_container_width=True)

if go:
    st.switch_page("pages/chat.py")

