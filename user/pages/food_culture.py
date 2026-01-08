import streamlit as st
import streamlit.components.v1 as components
import sys, os
import base64
import html

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from utils.path_config import img

st.set_page_config(
    page_title="Vietnamese Cuisine",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Mỗi lần rerun tăng 1 token để JS biết "batch" hiện tại (tránh DOM reuse làm kẹt reveal)
st.session_state.setdefault("_a11_token_cuisine", 0)
st.session_state["_a11_token_cuisine"] += 1
A11_TOKEN = st.session_state["_a11_token_cuisine"]

def render_html(s: str):
    """
    Streamlit markdown can render indented lines as code blocks.
    Remove ALL leading whitespace per-line to guarantee clean HTML rendering.
    """
    lines = s.splitlines()
    cleaned = "\n".join(line.lstrip(" \t") for line in lines).strip()
    st.markdown(cleaned, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def img_to_base64(path: str) -> str:
    full_path = img(path)
    ext = os.path.splitext(full_path)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    try:
        with open(full_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/{ext};base64,{encoded}"
    except FileNotFoundError:
        # 1x1 transparent gif
        return "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="

def esc(x: str) -> str:
    return html.escape(x, quote=True)

foods = [
    ("Pho", "food/pho.jpg",
     "Vietnam’s most iconic dish, featuring a clear and aromatic broth with rice noodles and tender meat, commonly enjoyed as breakfast.",
     "Noodle soup • Classic"),
    ("Banh Mi", "food/banhmi.jpg",
     "A unique fusion of Vietnamese flavors and Western influences, known worldwide for its convenience and variety.",
     "Street food • Fusion"),
    ("Goi Cuon (Fresh Spring Rolls)", "food/goicuon.jpg",
     "A light and refreshing dish made with shrimp, pork, herbs, and rice noodles, reflecting a healthy eating philosophy.",
     "Fresh • Healthy"),
    ("Bun Cha", "food/buncha.jpg",
     "A Hanoi specialty consisting of grilled pork served with rice noodles and a sweet-sour dipping sauce.",
     "Hanoi • Grilled"),
    ("Cao Lau", "food/cao_lau.jpg",
     "A distinctive noodle dish from Hoi An, influenced by cultural exchanges and closely tied to the town’s trading history.",
     "Hoi An • Heritage"),
    ("Com Tam (Broken Rice)", "food/comtam.jpg",
     "A popular southern Vietnamese dish that reflects everyday life and creativity in traditional cuisine.",
     "Southern • Comfort"),
    ("Banh Xeo", "food/banhxeo.jpg",
     "A savory crispy pancake filled with shrimp and pork, typically enjoyed in family meals and local gatherings.",
     "Crispy • Savory"),
]

render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif !important;
}

.stApp {
  background:
    radial-gradient(900px 500px at 15% 8%, rgba(255, 159, 28, 0.18), rgba(0,0,0,0) 60%),
    radial-gradient(700px 420px at 88% 18%, rgba(46, 196, 182, 0.16), rgba(0,0,0,0) 55%),
    radial-gradient(700px 420px at 82% 92%, rgba(231, 29, 54, 0.10), rgba(0,0,0,0) 55%);
}

.block-container { padding-top: 3rem; padding-bottom: 3rem; max-width: 1180px; }

.a11-divider {
  height: 1px;
  background: linear-gradient(90deg, rgba(0,0,0,0), rgba(148,163,184,.55), rgba(0,0,0,0));
  margin: 22px 0 18px 0;
  border-radius: 999px;
}

/* Hero */
.hero {
  position: relative;
  border-radius: 22px;
  padding: 26px 24px;
  overflow: hidden;
  border: 1px solid rgba(148,163,184,.35);
  background: rgba(255,255,255,.55);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 18px 45px rgba(15,23,42,.12);
}
@media (prefers-color-scheme: dark) {
  .hero { background: rgba(2,6,23,.42); border-color: rgba(148,163,184,.22); box-shadow: 0 18px 45px rgba(0,0,0,.35); }
}
.hero::before{
  content:"";
  position:absolute; inset:-2px;
  background:
    radial-gradient(420px 240px at 18% 30%, rgba(255,159,28,.22), rgba(0,0,0,0) 60%),
    radial-gradient(420px 240px at 82% 18%, rgba(46,196,182,.16), rgba(0,0,0,0) 55%),
    radial-gradient(420px 240px at 70% 88%, rgba(231,29,54,.12), rgba(0,0,0,0) 55%);
  pointer-events:none;
}
.hero-inner{ position:relative; z-index:1; }
.hero-badge{
  display:inline-flex; align-items:center; gap:10px;
  padding: 7px 12px;
  border-radius: 999px;
  border: 1px solid rgba(148,163,184,.35);
  background: rgba(255,255,255,.75);
  font-weight: 600;
  font-size: 13px;
  letter-spacing: .2px;
}
@media (prefers-color-scheme: dark) {
  .hero-badge{ background: rgba(2,6,23,.55); border-color: rgba(148,163,184,.22); }
}
.hero-title{
  margin: 14px 0 8px 0;
  font-weight: 800;
  font-size: 44px;
  letter-spacing: -0.8px;
  line-height: 1.12;
  padding-bottom: 2px;
}

.hero-subtitle{
  margin: 0;
  font-size: 16.5px;
  color: rgba(71,85,105,.95);
  line-height: 1.7;
  max-width: 900px;
}
@media (prefers-color-scheme: dark) { .hero-subtitle{ color: rgba(226,232,240,.84); } }

/* Animations */
@keyframes floatIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.hero-anim { animation: floatIn .7s cubic-bezier(.22,.9,.25,1) both; }
.hero-anim.d2 { animation-delay: .08s; }
.hero-anim.d3 { animation-delay: .14s; }

/* Section */
.section-head{
  margin-top: 6px;
  display:flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
}
.section-title{
  font-weight: 800;
  font-size: 22px;
  margin: 0;
  letter-spacing: -.3px;
}
.section-note{
  font-size: 13px;
  color: rgba(100,116,139,.95);
  margin: 0;
}
@media (prefers-color-scheme: dark) { .section-note{ color: rgba(148,163,184,.90);} }

/* Grid cards */
.grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-top: 12px;
}
@media (max-width: 1180px) { .grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (max-width: 860px)  { .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 540px)  { .grid { grid-template-columns: 1fr; } }

.card {
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(148,163,184,.35);
  background: rgba(255,255,255,.62);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 10px 26px rgba(15,23,42,.10);
  transition: transform .32s cubic-bezier(.2,.9,.2,1), box-shadow .32s cubic-bezier(.2,.9,.2,1), border-color .32s;
}
@media (prefers-color-scheme: dark) {
  .card { background: rgba(2,6,23,.44); border-color: rgba(148,163,184,.22); box-shadow: 0 10px 26px rgba(0,0,0,.34); }
}
.card:hover{
  transform: translateY(-6px);
  box-shadow: 0 18px 44px rgba(15,23,42,.16);
  border-color: rgba(255,159,28,.55);
}

.card-img-wrap{ height: 170px; overflow:hidden; }
.card-img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.02);
  transition: transform .45s cubic-bezier(.2,.9,.2,1), filter .45s cubic-bezier(.2,.9,.2,1);
  filter: saturate(1.06) contrast(1.02);
}
.card:hover .card-img{ transform: scale(1.08); }

.card-body{ padding: 12px 12px 14px 12px; }
.card-title{
  font-weight: 750;
  font-size: 15.5px;
  margin: 2px 0 6px 0;
  letter-spacing: -.2px;
}
.card-desc{
  margin: 0;
  font-size: 13.3px;
  line-height: 1.55;
  color: rgba(71,85,105,.95);
}
@media (prefers-color-scheme: dark) { .card-desc{ color: rgba(226,232,240,.82); } }

.tag{
  display:inline-flex; align-items:center;
  gap: 8px;
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(148,163,184,.35);
  background: rgba(255,255,255,.72);
  margin: 10px 0 0 0;
}
@media (prefers-color-scheme: dark) { .tag{ background: rgba(2,6,23,.52); border-color: rgba(148,163,184,.22); } }
.tag-dot{
  width: 7px; height: 7px; border-radius: 999px;
  background: rgba(255,159,28,.92);
  box-shadow: 0 0 0 4px rgba(255,159,28,.18);
}

/* Scroll reveal (progressive enhancement) */
.reveal { opacity: 1; transform: none; }

.js-reveal .reveal {
  opacity: 0;
  transform: translateY(14px);
  transition: opacity .70s cubic-bezier(.2,.9,.2,1), transform .70s cubic-bezier(.2,.9,.2,1);
  transition-delay: var(--delay, 0ms);
  will-change: opacity, transform;
}
.js-reveal .reveal.show { opacity: 1; transform: translateY(0); }

/* Region blocks */
.regions {
  display: grid;
  grid-template-columns: repeat(3, minmax(0,1fr));
  gap: 14px;
  margin-top: 12px;
}
@media (max-width: 860px) { .regions { grid-template-columns: 1fr; } }
.region {
  border-radius: 18px;
  padding: 14px 14px;
  border: 1px solid rgba(148,163,184,.35);
  background: rgba(255,255,255,.62);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 10px 26px rgba(15,23,42,.10);
}
@media (prefers-color-scheme: dark) {
  .region { background: rgba(2,6,23,.44); border-color: rgba(148,163,184,.22); box-shadow: 0 10px 26px rgba(0,0,0,.34); }
}
.region h4{ margin: 0 0 6px 0; font-size: 15px; letter-spacing: -.2px; }
.region p{ margin: 0; font-size: 13.3px; line-height: 1.6; color: rgba(71,85,105,.95); }
@media (prefers-color-scheme: dark) { .region p{ color: rgba(226,232,240,.82); } }

@media (prefers-reduced-motion: reduce) {
  .card, .card-img, .hero-anim { transition: none !important; animation: none !important; }
  .js-reveal .reveal { opacity: 1 !important; transform: none !important; transition: none !important; }
}
</style>
""")

hero_html = (
    '<div class="hero">'
    '<div class="hero-inner">'
    '<div class="hero-badge hero-anim">'
    '<span style="font-size:16px;">🍜</span>'
    '<span>Vietnamese Cuisine</span>'
    '<span style="opacity:.6;">|</span>'
    '<span style="opacity:.85;">Signature dishes & regional taste</span>'
    '</div>'
    '<div class="hero-title hero-anim d2">Vietnamese Cuisine</div>'
    '<p class="hero-subtitle hero-anim d3">'
    'Vietnamese cuisine is the result of a harmonious balance between fresh ingredients, '
    'traditional cooking techniques, and a philosophy of flavor harmony. Each dish reflects '
    'not only nutritional values but also the cultural identity and everyday life of different regions across Vietnam.'
    '</p>'
    '</div>'
    '</div>'
    '<div class="a11-divider"></div>'
)
render_html(hero_html)

left, right = st.columns([2, 1])
with left:
    q = st.text_input("Search dishes", placeholder="Type: Pho, Banh Mi, Bun Cha...")
with right:
    tags = sorted({f[3] for f in foods})
    tag_pick = st.selectbox("Filter by vibe", ["All"] + tags, index=0)

filtered = []
for t, p, d, vibe in foods:
    hay = (t + " " + d + " " + vibe).lower()
    if q and q.lower() not in hay:
        continue
    if tag_pick != "All" and vibe != tag_pick:
        continue
    filtered.append((t, p, d, vibe))

render_html("""
<div class="section-head">
  <h3 class="section-title">🍽️ Signature Dishes of Vietnam</h3>
  <p class="section-note">Hover to interact • Scroll to reveal</p>
</div>
""")

if not filtered:
    st.info("No dishes matched your search/filter.")
else:
    cards = ['<div class="grid">']
    for idx, (title, path, desc, vibe) in enumerate(filtered):
        img_b64 = img_to_base64(path)
        cards.append(
            f'<article class="card reveal" data-a11-token="{A11_TOKEN}" style="--delay:{min(idx*60, 360)}ms">'
            f'<div class="card-img-wrap"><img class="card-img" src="{img_b64}" alt="{esc(title)}" loading="lazy"/></div>'
            f'<div class="card-body">'
            f'<div class="card-title">{esc(title)}</div>'
            f'<p class="card-desc">{esc(desc)}</p>'
            f'<div class="tag"><span class="tag-dot"></span><span>{esc(vibe)}</span></div>'
            f'</div></article>'
        )
    cards.append("</div>")
    render_html("\n".join(cards))

render_html('<div class="a11-divider"></div>')

render_html(f"""
<div class="section-head">
  <h3 class="section-title">🌍 Regional Characteristics of Vietnamese Cuisine</h3>
  <p class="section-note">North • Central • South</p>
</div>

<div class="regions">
  <div class="region reveal" data-a11-token="{A11_TOKEN}" style="--delay:0ms">
    <h4>Northern Vietnam</h4>
    <p>Light and balanced flavors, emphasizing subtlety and harmony.</p>
  </div>
  <div class="region reveal" data-a11-token="{A11_TOKEN}" style="--delay:80ms">
    <h4>Central Vietnam</h4>
    <p>Bold, spicy, and richly seasoned dishes shaped by harsh natural conditions.</p>
  </div>
  <div class="region reveal" data-a11-token="{A11_TOKEN}" style="--delay:160ms">
    <h4>Southern Vietnam</h4>
    <p>Sweeter and richer flavors with abundant ingredients influenced by river-based culture.</p>
  </div>
</div>
""")

# JS: bind reveal cho đúng batch hiện tại (TOKEN), tránh DOM reuse khi đổi filter
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

    // Chỉ xử lý đúng batch hiện tại
    const els = Array.from(doc.querySelectorAll('.reveal[data-a11-token="' + TOKEN + '"]'));
    if (!els.length) return false;

    // Reset marker (Streamlit có thể reuse DOM)
    els.forEach(el => {{
      el.removeAttribute('data-a11-observed');
    }});

    // Prime: những item đang ở viewport thì show trước
    els.forEach(el => {{
      if (inView(el)) el.classList.add('show');
    }});

    // Bật chế độ reveal
    root.classList.add('js-reveal');

    // Dọn observer cũ (nếu có) để không bị state kẹt khi đổi filter
    if (doc.__a11CuisineIO) {{
      try {{ doc.__a11CuisineIO.disconnect(); }} catch (e) {{}}
      doc.__a11CuisineIO = null;
    }}

    // Fallback: nếu không có IntersectionObserver thì show tất cả
    if (!('IntersectionObserver' in parent)) {{
      els.forEach(el => el.classList.add('show'));
      return true;
    }}

    const io = new parent.IntersectionObserver((entries) => {{
      entries.forEach(e => {{
        if (e.isIntersecting) {{
          e.target.classList.add('show');
          // Không unobserve để tránh trường hợp DOM reuse làm mất theo dõi
        }}
      }});
    }}, {{ threshold: 0.12, rootMargin: "0px 0px -10% 0px" }});

    doc.__a11CuisineIO = io;

    els.forEach(el => {{
      io.observe(el);
    }});

    return true;
  }}

  // Poll để đợi Streamlit render xong DOM sau khi đổi filter/search
  let tries = 0;
  const timer = parent.setInterval(() => {{
    tries += 1;
    const ok = bindRevealForToken();
    if (ok || tries >= 80) parent.clearInterval(timer); // ~8s
  }}, 100);
}})();
</script>
""", height=0)
