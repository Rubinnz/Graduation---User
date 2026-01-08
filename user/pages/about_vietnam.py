import streamlit as st
import streamlit.components.v1 as components
from utils.path_config import img
import base64
import os
import html

st.set_page_config(
    page_title="Vietnam — Land & People",
    page_icon="🇻🇳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def render_html(s: str):
    """
    Streamlit markdown can turn indented lines into code blocks.
    This removes ALL leading whitespace per-line to guarantee clean HTML rendering.
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

destinations = [
    ("Ha Long Bay", "destinations/halong.jpg",
     "A UNESCO World Natural Heritage site, famous for its thousands of limestone islands rising from emerald waters.",
     "UNESCO • Nature"),
    ("Hoi An Ancient Town", "destinations/hoian.jpg",
     "A well-preserved historic town reflecting a unique blend of Vietnamese, Chinese, and Western architectural influences.",
     "Heritage • Culture"),
    ("Da Nang", "destinations/danang.jpg",
     "A modern coastal city known for its beautiful beaches, iconic bridges, and central role in central Vietnam tourism.",
     "Coastal • Modern"),
    ("Ha Giang Loop", "destinations/ha_giang_loop.jpg",
     "A legendary mountain route offering breathtaking landscapes and rich ethnic minority cultures in northern Vietnam.",
     "Adventure • Highlands"),
    ("Hanoi Old Quarter", "destinations/hanoi.jpg",
     "A historic district over 1,000 years old, capturing the traditional lifestyle and cultural identity of Vietnam’s capital.",
     "Historic • Citylife"),
    ("Ho Chi Minh City", "destinations/ho_chi_minh_city.jpg",
     "Vietnam’s largest economic hub, characterized by its dynamic urban life and historical significance.",
     "Metropolis • Energy"),
    ("Hue Imperial City", "destinations/hue.jpg",
     "The former imperial capital of the Nguyen Dynasty, featuring royal architecture and refined court culture.",
     "Imperial • UNESCO"),
    ("Nha Trang", "destinations/nhatrang.jpg",
     "A popular beach destination known for its long coastline, pleasant climate, and resort activities.",
     "Beach • Resorts"),
    ("Phu Quoc Island", "destinations/phuquoc.jpg",
     "Often referred to as Vietnam’s ‘Pearl Island’, famous for pristine beaches and a rich marine ecosystem.",
     "Island • Relax"),
    ("Sa Pa", "destinations/sapa.jpg",
     "A highland town renowned for terraced rice fields, cool climate, and diverse ethnic cultures.",
     "Terraces • Cool air"),
]

render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif !important;
}

.stApp {
  background:
    radial-gradient(900px 500px at 15% 8%, rgba(46, 196, 182, 0.22), rgba(0,0,0,0) 60%),
    radial-gradient(700px 420px at 88% 18%, rgba(255, 159, 28, 0.18), rgba(0,0,0,0) 55%),
    radial-gradient(700px 420px at 82% 92%, rgba(231, 29, 54, 0.12), rgba(0,0,0,0) 55%);
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
    radial-gradient(380px 210px at 18% 30%, rgba(46,196,182,.26), rgba(0,0,0,0) 60%),
    radial-gradient(420px 240px at 82% 18%, rgba(255,159,28,.20), rgba(0,0,0,0) 55%),
    radial-gradient(420px 240px at 70% 88%, rgba(231,29,54,.14), rgba(0,0,0,0) 55%);
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
  max-width: 860px;
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

/* Grid */
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
  border-color: rgba(46,196,182,.55);
}

.card-img-wrap{ height: 170px; overflow:hidden; }
.card-img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.02);
  transition: transform .45s cubic-bezier(.2,.9,.2,1), filter .45s cubic-bezier(.2,.9,.2,1);
  filter: saturate(1.05) contrast(1.02);
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
  background: rgba(46,196,182,.92);
  box-shadow: 0 0 0 4px rgba(46,196,182,.18);
}

/* Reveal (FIX: progressive enhancement)
   - Mặc định luôn HIỂN THỊ để tránh trường hợp JS chưa kịp init => "không thấy data"
   - Khi JS bật chế độ reveal (add class .js-reveal), mới áp dụng ẩn + animate
*/
.reveal { opacity: 1; transform: none; }

.js-reveal .reveal {
  opacity: 0;
  transform: translateY(14px);
  transition: opacity .70s cubic-bezier(.2,.9,.2,1), transform .70s cubic-bezier(.2,.9,.2,1);
  transition-delay: var(--delay, 0ms);
  will-change: opacity, transform;
}
.js-reveal .reveal.show { opacity: 1; transform: translateY(0); }

/* Benefits */
.benefits {
  display: grid;
  grid-template-columns: repeat(3, minmax(0,1fr));
  gap: 14px;
  margin-top: 12px;
}
@media (max-width: 860px) { .benefits { grid-template-columns: 1fr; } }
.benefit {
  border-radius: 18px;
  padding: 14px 14px;
  border: 1px solid rgba(148,163,184,.35);
  background: rgba(255,255,255,.62);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 10px 26px rgba(15,23,42,.10);
}
@media (prefers-color-scheme: dark) {
  .benefit { background: rgba(2,6,23,.44); border-color: rgba(148,163,184,.22); box-shadow: 0 10px 26px rgba(0,0,0,.34); }
}
.benefit h4{ margin: 0 0 6px 0; font-size: 15px; letter-spacing: -.2px; }
.benefit p{ margin: 0; font-size: 13.3px; line-height: 1.6; color: rgba(71,85,105,.95); }
@media (prefers-color-scheme: dark) { .benefit p{ color: rgba(226,232,240,.82); } }

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
    '<span style="font-size:16px;">🇻🇳</span>'
    '<span>Vietnam • Land & People</span>'
    '<span style="opacity:.6;">|</span>'
    '<span style="opacity:.85;">Curated highlights</span>'
    '</div>'
    '<div class="hero-title hero-anim d2">Vietnam — Land &amp; People</div>'
    '<p class="hero-subtitle hero-anim d3">'
    'Vietnam is a Southeast Asian country known for its rich history, distinctive cultural identity, '
    'and diverse natural landscapes. The harmonious blend of tradition and modern life has made Vietnam '
    'an increasingly attractive destination for international travelers.'
    '</p>'
    '</div>'
    '</div>'
    '<div class="a11-divider"></div>'
)
render_html(hero_html)

left, right = st.columns([2, 1])
with left:
    q = st.text_input("Search destinations", placeholder="Type: Ha Long, Sa Pa, Hue...")
with right:
    tags = sorted({d[3] for d in destinations})
    tag_pick = st.selectbox("Filter by vibe", ["All"] + tags, index=0)

filtered = []
for t, p, d, vibe in destinations:
    if q and q.lower() not in (t + " " + d + " " + vibe).lower():
        continue
    if tag_pick != "All" and vibe != tag_pick:
        continue
    filtered.append((t, p, d, vibe))

render_html("""
<div class="section-head">
  <h3 class="section-title">🌏 Iconic Destinations in Vietnam</h3>
  <p class="section-note">Hover to interact • Scroll to reveal</p>
</div>
""")

if not filtered:
    st.info("No destinations matched your search/filter.")
else:
    cards = ['<div class="grid">']
    for idx, (title, path, desc, vibe) in enumerate(filtered):
        img_b64 = img_to_base64(path)
        cards.append(
            f'<article class="card reveal" style="--delay:{min(idx*60, 360)}ms">'
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

render_html("""
<div class="section-head">
  <h3 class="section-title">✨ Why Do International Travelers Choose Vietnam?</h3>
  <p class="section-note">Culture • Food • Landscape • Value</p>
</div>

<div class="benefits">
  <div class="benefit reveal" style="--delay:0ms">
    <h4>People & Culture</h4>
    <p>Friendly, welcoming people with a strong cultural identity, and a compelling blend of tradition and modern life.</p>
  </div>

  <div class="benefit reveal" style="--delay:80ms">
    <h4>Culinary Diversity</h4>
    <p>A diverse and affordable culinary scene across regions, from street food to refined local specialties.</p>
  </div>

  <div class="benefit reveal" style="--delay:160ms">
    <h4>Nature & Value</h4>
    <p>Beaches, mountains, highlands, river deltas, plus reasonable travel costs and continuously improving infrastructure.</p>
  </div>
</div>
""")

components.html("""
<script>
(function () {
  const parent = window.parent;
  const doc = parent.document;

  function getRoot() {
    return doc.querySelector('.stApp') || doc.body;
  }

  function initRevealBatch() {
    const root = getRoot();
    root.classList.add('js-reveal');

    const els = doc.querySelectorAll('.reveal:not([data-a11-observed])');
    if (!els.length) return false;

    // Nếu parent window không có IntersectionObserver thì show luôn
    if (!('IntersectionObserver' in parent)) {
      els.forEach(el => {
        el.classList.add('show');
        el.setAttribute('data-a11-observed', '1');
      });
      return true;
    }

    const io = new parent.IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('show');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -10% 0px" });

    els.forEach(el => {
      el.setAttribute('data-a11-observed', '1');
      io.observe(el);
    });

    return true;
  }

  // Poll vài giây để tránh trường hợp script chạy trước khi Streamlit render xong HTML
  let tries = 0;
  const timer = parent.setInterval(() => {
    tries += 1;
    initRevealBatch();

    // Dừng sau ~4s (40 * 100ms), đủ để DOM ổn định trên đa số môi trường
    if (tries >= 40) parent.clearInterval(timer);
  }, 100);
})();
</script>
""", height=0)
