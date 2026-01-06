import os
import json
import uuid
import base64
import html
from typing import Any

import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime, timezone

API_CHAT_URL = "http://localhost:8000/chat"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

from layout import init_layout, chat_bubble_user, chat_bubble_ai, ai_typing_animation

st.set_page_config(
    page_title="Vietnam Travel AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

def render_html(s: str):
    cleaned = "\n".join(line.lstrip(" \t") for line in s.splitlines()).strip()
    st.markdown(cleaned, unsafe_allow_html=True)

def esc(x: Any) -> str:
    return html.escape(str(x), quote=True)

@st.cache_data(show_spinner=False)
def img_to_b64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

def post_chat(query: str) -> str:
    try:
        res = requests.post(API_CHAT_URL, json={"query": query}, timeout=45)
        if not res.ok:
            return f"Backend error: HTTP {res.status_code}"
        data = res.json() if res.content else {}
        return data.get("answer") or "No response received from the API."
    except requests.exceptions.Timeout:
        return "Backend timeout. Please try again."
    except Exception:
        return "Unable to connect to the backend API."

def scroll_to_bottom():
    components.html(
        """
<script>
(function() {
  const doc = window.parent.document;
  const main = doc.querySelector('section.main');
  if (!main) return;
  main.scrollTo({ top: main.scrollHeight, behavior: 'smooth' });
})();
</script>
        """,
        height=0,
    )

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def export_conversation(messages: list[dict]) -> bytes:
    payload = {"exported_at_utc": utc_now(), "messages": messages}
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")

def bump_seed():
    st.session_state.quick_seed = int.from_bytes(os.urandom(4), "little")

def safe_index(options: list[str], value: str, fallback_idx: int = 0) -> int:
    return options.index(value) if value in options else fallback_idx

def norm_none(x: Any):
    if x is None:
        return None
    s = str(x).strip()
    if s.lower() in {"none", "null", ""}:
        return None
    return x

def ensure_state():
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending" not in st.session_state:
        st.session_state.pending = None
    if "last_user_query" not in st.session_state:
        st.session_state.last_user_query = None
    if "quick_seed" not in st.session_state:
        bump_seed()

    defaults = {
        "mode": "Explore",
        "cities": [],
        "days": None,
        "budget": None,
        "style": None,
        "companions": None,
        "season": None,
        "pace": None,
        "interests": [],
        "constraints": [],
        "language": "English",
        "detail": "Detailed",
        "extras": [],
    }

    if "profile" not in st.session_state or not isinstance(st.session_state.profile, dict):
        st.session_state.profile = defaults.copy()
        return

    for k, v in defaults.items():
        if k not in st.session_state.profile:
            st.session_state.profile[k] = v

    st.session_state.profile["mode"] = st.session_state.profile.get("mode") or "Explore"

    if not isinstance(st.session_state.profile.get("cities"), list):
        st.session_state.profile["cities"] = []
    if not isinstance(st.session_state.profile.get("interests"), list):
        st.session_state.profile["interests"] = []
    if not isinstance(st.session_state.profile.get("constraints"), list):
        st.session_state.profile["constraints"] = []
    if not isinstance(st.session_state.profile.get("extras"), list):
        st.session_state.profile["extras"] = []

    for k in ["days", "budget", "style", "companions", "season", "pace"]:
        st.session_state.profile[k] = norm_none(st.session_state.profile.get(k))

    if st.session_state.profile.get("language") not in {"English", "Vietnamese"}:
        st.session_state.profile["language"] = "English"

    if st.session_state.profile.get("detail") not in {"Concise", "Balanced", "Detailed"}:
        st.session_state.profile["detail"] = "Detailed"

def reset_profile_to_none():
    st.session_state.profile.update(
        {
            "mode": "Explore",
            "cities": [],
            "days": None,
            "budget": None,
            "style": None,
            "companions": None,
            "season": None,
            "pace": None,
            "interests": [],
            "constraints": [],
            "extras": [],
        }
    )

def build_system_context(p: dict) -> str:
    language = p.get("language") or "English"
    detail = p.get("detail") or "Detailed"
    extras = p.get("extras") or []
    mode = p.get("mode") or "Explore"

    base = [
        "You are Vietnam Travel AI.",
        "Be accurate, practical, and structured. Do not claim real-time access.",
        f"Output language: {language}.",
        f"Response detail level: {detail}.",
    ]

    if extras:
        base.append("If relevant, include: " + ", ".join(extras) + ".")

    trip_fields = {
        "Cities": ", ".join(p.get("cities") or []),
        "Trip length": (f'{p.get("days")} days' if p.get("days") is not None else None),
        "Budget": p.get("budget"),
        "Style": p.get("style"),
        "Pace": p.get("pace"),
        "Companions": p.get("companions"),
        "Season": p.get("season"),
        "Interests": (", ".join(p.get("interests") or []) if (p.get("interests") or []) else None),
        "Constraints": (", ".join(p.get("constraints") or []) if (p.get("constraints") or []) else None),
    }

    any_trip_signal = any(v for v in trip_fields.values())

    if mode == "Explore" and not any_trip_signal:
        base += [
            "Primary role: help the user learn about Vietnam (culture, history, etiquette, regions, food, language, geography, tourism context).",
            "Do NOT proactively create itineraries or budgets unless the user explicitly asks for planning.",
            "If the user asks to plan, first ask 1–3 essential clarifying questions, then provide a best-effort draft plan with assumptions.",
        ]
        return "\n".join(base) + "\n"

    base += [
        "Primary role: trip planning copilot when asked.",
        "If the user asks for an itinerary, produce a day-by-day plan with morning/afternoon/evening and practical transport + cost estimates.",
        "If important trip details are missing, make reasonable assumptions and list them clearly, or ask minimal clarifying questions.",
        "User trip profile (may be partial):",
    ]

    for k, v in trip_fields.items():
        if v:
            base.append(f"- {k}: {v}")

    return "\n".join(base) + "\n"

def enrich_query(user_query: str, profile: dict) -> str:
    return f"{build_system_context(profile)}User question:\n{user_query}"

def set_pending(prompt: str):
    st.session_state.pending = prompt
    st.rerun()

ensure_state()

avatar_ai = img_to_b64(os.path.join(BASE_DIR, "images/chatbot/chatbot_avatar.png"))
avatar_user = img_to_b64(os.path.join(BASE_DIR, "images/chatbot/user_avatar.png"))

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

.block-container { max-width: 1240px; padding-top: 1.05rem; padding-bottom: 2.1rem; }

section[data-testid="stSidebar"] {
  background: rgba(255,255,255,.62) !important;
  border-right: 1px solid rgba(15,23,42,.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

div[data-testid="stHorizontalBlock"] { overflow: visible !important; }
div[data-testid="stColumn"] { overflow: visible !important; }

div[data-testid="stColumn"]:has(#a11_right_rail_marker) {
  position: sticky;
  top: 16px;
  align-self: flex-start;
  height: fit-content;
}

div[data-testid="stVerticalBlock"]:has(#a11_right_rail_marker) {
  border-radius: 20px !important;
  border: 1px solid rgba(148,163,184,.30) !important;
  background: rgba(255,255,255,.52) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 14px 40px rgba(15,23,42,.08);
  padding: 12px 12px !important;
  max-height: calc(100vh - 32px);
  overflow: auto;
}

@media (max-width: 980px) {
  div[data-testid="stColumn"]:has(#a11_right_rail_marker) { position: static !important; top: auto !important; }
  div[data-testid="stVerticalBlock"]:has(#a11_right_rail_marker) { max-height: none !important; overflow: visible !important; }
}

.chat-hero {
  position: relative;
  border-radius: 22px;
  padding: 16px 16px 14px 16px;
  border: 1px solid rgba(148,163,184,.30);
  background: rgba(255,255,255,.55);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 16px 46px rgba(15,23,42,.10);
  overflow: hidden;
  margin-bottom: 12px;
}
.chat-hero:before{
  content:"";
  position:absolute; inset:-2px;
  background:
    radial-gradient(520px 260px at 18% 38%, rgba(46,196,182,.18), rgba(0,0,0,0) 60%),
    radial-gradient(520px 260px at 78% 22%, rgba(255,159,28,.14), rgba(0,0,0,0) 60%),
    radial-gradient(520px 260px at 72% 88%, rgba(231,29,54,.10), rgba(0,0,0,0) 60%);
  pointer-events:none;
}
.hero-inner{ position:relative; z-index:1; }
.chat-hero h1 {
  margin: 0;
  font-weight: 900;
  font-size: 30px;
  letter-spacing: -0.55px;
  text-align: center;
  color: rgba(15,23,42,.95);
}
.chat-hero p {
  margin: 7px 0 0 0;
  text-align: center;
  color: rgba(71,85,105,.92);
  font-size: 13.5px;
  line-height: 1.6;
}
.pills{
  margin-top: 10px;
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
  background: rgba(255,255,255,.60);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: rgba(30,41,59,.92);
}

.shell {
  border-radius: 20px;
  border: 1px solid rgba(148,163,184,.30);
  background: rgba(255,255,255,.56);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 14px 40px rgba(15,23,42,.08);
  padding: 12px 12px 6px 12px;
}

div[data-testid="stChatInput"] { margin-top: 10px; }
div[data-testid="stChatInput"] textarea {
  border-radius: 14px !important;
  border: 1px solid rgba(148,163,184,.35) !important;
  background: rgba(255,255,255,.68) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 10px 26px rgba(15,23,42,.08) !important;
}

.a11-rail-title h3 {
  margin: 0 0 6px 0 !important;
  font-size: 15.5px !important;
  font-weight: 900 !important;
  letter-spacing: -.2px !important;
  color: rgba(15,23,42,.92) !important;
}
.a11-rail-sub {
  margin: 0 0 10px 0;
  color: rgba(71,85,105,.92);
  font-size: 13px;
  line-height: 1.6;
}
.a11-rail-sec {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid rgba(148,163,184,.28);
}
.a11-rail-label {
  font-size: 11.5px;
  font-weight: 800;
  color: rgba(100,116,139,.95);
  text-transform: uppercase;
  letter-spacing: .12em;
  margin-bottom: 8px;
}

div[data-testid="stVerticalBlock"]:has(#a11_right_rail_marker) .stButton > button {
  width: 100%;
  border-radius: 14px !important;
  border: 1px solid rgba(148,163,184,.34) !important;
  background: rgba(255,255,255,.60) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 10px 24px rgba(15,23,42,.06) !important;
  color: rgba(15,23,42,.92) !important;
  font-weight: 750 !important;
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
div[data-testid="stVerticalBlock"]:has(#a11_right_rail_marker) .stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(15,23,42,.10) !important;
  border-color: rgba(46,196,182,.45) !important;
}
</style>
""")

init_layout()

with st.sidebar:
    st.subheader("Session")
    st.caption(f"ID: {st.session_state.user_id[:8]}")
    a, b = st.columns(2)
    with a:
        if st.button("New session", use_container_width=True):
            st.session_state.user_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.pending = None
            st.session_state.last_user_query = None
            bump_seed()
            st.rerun()
    with b:
        if st.button("Shuffle prompts", use_container_width=True):
            bump_seed()
            st.rerun()

    st.subheader("Assistant Mode")
    mode_opts = ["Explore", "Plan"]
    st.session_state.profile["mode"] = st.selectbox(
        "Mode",
        mode_opts,
        index=safe_index(mode_opts, st.session_state.profile.get("mode", "Explore"), 0),
        help="Explore: learn about Vietnam without auto-planning. Plan: use Trip Profile for itineraries and logistics.",
    )

    st.subheader("Trip Profile (optional)")
    if st.button("Reset Trip Profile to None", use_container_width=True):
        reset_profile_to_none()
        st.rerun()

    cities_master = [
        "Hanoi", "Ha Long", "Ninh Binh", "Sa Pa", "Hue", "Da Nang", "Hoi An",
        "Nha Trang", "Da Lat", "Ho Chi Minh City", "Mekong Delta", "Phu Quoc"
    ]
    st.session_state.profile["cities"] = st.multiselect(
        "Cities",
        cities_master,
        default=st.session_state.profile.get("cities", []),
    )

    day_options = ["None"] + [str(i) for i in range(1, 22)]
    current_days = "None" if st.session_state.profile.get("days") is None else str(int(st.session_state.profile["days"]))
    picked_days = st.selectbox("Days", day_options, index=safe_index(day_options, current_days, 0))
    st.session_state.profile["days"] = None if picked_days == "None" else int(picked_days)

    budget_opts = ["None", "low", "mid", "high"]
    picked_budget = st.selectbox(
        "Budget",
        budget_opts,
        index=safe_index(budget_opts, str(st.session_state.profile.get("budget") or "None"), 0),
    )
    st.session_state.profile["budget"] = None if picked_budget == "None" else picked_budget

    style_opts = ["None", "balanced", "foodie", "culture", "nature", "beach", "luxury"]
    picked_style = st.selectbox(
        "Style",
        style_opts,
        index=safe_index(style_opts, str(st.session_state.profile.get("style") or "None"), 0),
    )
    st.session_state.profile["style"] = None if picked_style == "None" else picked_style

    pace_opts = ["None", "slow", "balanced", "fast"]
    picked_pace = st.selectbox(
        "Pace",
        pace_opts,
        index=safe_index(pace_opts, str(st.session_state.profile.get("pace") or "None"), 0),
    )
    st.session_state.profile["pace"] = None if picked_pace == "None" else picked_pace

    companions_opts = ["None", "solo", "couple", "friends", "family"]
    picked_comp = st.selectbox(
        "Companions",
        companions_opts,
        index=safe_index(companions_opts, str(st.session_state.profile.get("companions") or "None"), 0),
    )
    st.session_state.profile["companions"] = None if picked_comp == "None" else picked_comp

    season_opts = ["None", "any", "spring", "summer", "autumn", "winter"]
    picked_season = st.selectbox(
        "Season",
        season_opts,
        index=safe_index(season_opts, str(st.session_state.profile.get("season") or "None"), 0),
    )
    st.session_state.profile["season"] = None if picked_season == "None" else picked_season

    interests = ["food", "culture", "nature", "beach", "history", "nightlife", "photography", "adventure", "shopping"]
    st.session_state.profile["interests"] = st.multiselect(
        "Interests",
        interests,
        default=st.session_state.profile.get("interests", []),
    )

    constraints = ["wheelchair-friendly", "kid-friendly", "no-motorbike", "no-seafood", "vegetarian", "halal"]
    st.session_state.profile["constraints"] = st.multiselect(
        "Constraints",
        constraints,
        default=st.session_state.profile.get("constraints", []),
    )

    st.subheader("Answer Settings")
    lang_opts = ["English", "Vietnamese"]
    st.session_state.profile["language"] = st.selectbox(
        "Language",
        lang_opts,
        index=safe_index(lang_opts, st.session_state.profile.get("language", "English"), 0),
    )

    detail_opts = ["Concise", "Balanced", "Detailed"]
    st.session_state.profile["detail"] = st.selectbox(
        "Detail",
        detail_opts,
        index=safe_index(detail_opts, st.session_state.profile.get("detail", "Detailed"), 2),
    )

    extras_opts = ["Local tips", "Scams to avoid", "Transport options", "Budget breakdown", "Best time to visit", "Local phrases"]
    st.session_state.profile["extras"] = st.multiselect(
        "Include",
        extras_opts,
        default=st.session_state.profile.get("extras", []),
    )

    st.subheader("Utilities")
    c1, c2 = st.columns(2)
    with c1:
        regen_disabled = st.session_state.last_user_query is None
        if st.button("Regenerate", use_container_width=True, disabled=regen_disabled):
            if st.session_state.messages and st.session_state.messages[-1].get("role") == "ai":
                st.session_state.messages = st.session_state.messages[:-1]
            st.session_state.pending = st.session_state.last_user_query
            st.rerun()
    with c2:
        if st.button("Clear chat", use_container_width=True, disabled=len(st.session_state.messages) == 0):
            st.session_state.messages = []
            st.session_state.pending = None
            st.session_state.last_user_query = None
            st.rerun()

    if len(st.session_state.messages) > 0:
        blob = export_conversation(st.session_state.messages)
        st.download_button(
            "Download chat (JSON)",
            data=blob,
            file_name=f"travel_ai_chat_{st.session_state.user_id[:8]}.json",
            mime="application/json",
            use_container_width=True,
        )

mode = st.session_state.profile.get("mode", "Explore")
cities_txt = ", ".join(st.session_state.profile["cities"]) if st.session_state.profile.get("cities") else "None"
days_txt = "None" if st.session_state.profile.get("days") is None else str(st.session_state.profile["days"])
budget_txt = st.session_state.profile.get("budget") or "None"
style_txt = st.session_state.profile.get("style") or "None"

render_html(f"""
<div class="chat-hero">
  <div class="hero-inner">
    <h1>🧭 Vietnam Travel AI</h1>
    <p>{'Explore Vietnam with culture-first answers (no auto planning).' if mode == 'Explore' else 'Plan trips with profile-aware itineraries and logistics.'}</p>
    <div class="pills">
      <span class="pill">Mode: <b>{esc(mode)}</b></span>
      <span class="pill">Cities: <b>{esc(cities_txt)}</b></span>
      <span class="pill">Days: <b>{esc(days_txt)}</b></span>
      <span class="pill">Budget: <b>{esc(budget_txt)}</b></span>
      <span class="pill">Style: <b>{esc(style_txt)}</b></span>
    </div>
  </div>
</div>
""")

left, right = st.columns([1.55, 1.0], gap="large")

with right:
    render_html('<div id="a11_right_rail_marker"></div>')
    render_html("""
<div class="a11-rail-title">
  <h3>Menu</h3>
  <div class="a11-rail-sub">Quick actions and prompt ideas. This panel stays with you while you scroll.</div>
</div>
""")

    if mode == "Explore" and not st.session_state.profile.get("cities") and st.session_state.profile.get("days") is None:
        render_html('<div class="a11-rail-sec"><div class="a11-rail-label">Quick actions</div></div>')
        qa1, qa2 = st.columns(2)
        with qa1:
            if st.button("🏯 Culture", use_container_width=True, key="qa_culture"):
                set_pending("Give me a concise overview of Vietnamese culture: values, family life, etiquette, and regional differences.")
        with qa2:
            if st.button("🍲 Food 101", use_container_width=True, key="qa_food101"):
                set_pending("Explain Vietnamese cuisine by region (North/Central/South) and what dishes best represent each.")
        qa3, qa4 = st.columns(2)
        with qa3:
            if st.button("🗣️ Language", use_container_width=True, key="qa_lang"):
                set_pending("Teach me useful Vietnamese phrases for travelers, with pronunciation tips and when to use them.")
        with qa4:
            if st.button("🧭 Destinations", use_container_width=True, key="qa_dest"):
                set_pending("What are the top destination regions in Vietnam and what is each best known for?")
        qa5, qa6 = st.columns(2)
        with qa5:
            if st.button("🎎 Festivals", use_container_width=True, key="qa_fest"):
                set_pending("What are Vietnam’s major festivals (Tet, Mid-Autumn, etc.) and what should a visitor know?")
        with qa6:
            if st.button("🧠 Do/Don't", use_container_width=True, key="qa_etiquette"):
                set_pending("List practical do’s and don’ts for foreigners in Vietnam: etiquette, tipping, bargaining, and common misunderstandings.")

        render_html('<div class="a11-rail-sec"><div class="a11-rail-label">Suggested prompts</div></div>')
        suggestions = [
            "Explain the cultural differences between Northern and Southern Vietnam.",
            "What is Vietnamese coffee culture and what should I try first?",
            "Give me a beginner guide to Vietnamese street food and how to order safely.",
            "Tell me about Vietnam’s history timeline in a way a traveler can understand.",
            "What are the most scenic landscapes in Vietnam and why are they special?",
            "What souvenirs are culturally meaningful (not just touristy)?",
            "Explain Vietnamese dining etiquette and table manners.",
            "How does religion and spirituality show up in everyday life in Vietnam?",
            "What should I know about Vietnamese family culture and social norms?",
            "Describe Hanoi vs Ho Chi Minh City vibes for first-time visitors.",
            "What are common scams in Vietnam and how do locals avoid them?",
            "Give me a regional overview: mountains, coast, delta, highlands.",
        ]
    else:
        cities = ", ".join(st.session_state.profile["cities"]) if st.session_state.profile.get("cities") else "Vietnam"
        days = st.session_state.profile.get("days") or 5

        render_html('<div class="a11-rail-sec"><div class="a11-rail-label">Quick actions</div></div>')
        qa1, qa2 = st.columns(2)
        with qa1:
            if st.button("🗺️ Itinerary", use_container_width=True, key="qa_itinerary"):
                set_pending(f"Build a {days}-day itinerary for {cities}. Include must-do spots, realistic transport, estimated costs, and booking tips.")
        with qa2:
            if st.button("💸 Budget", use_container_width=True, key="qa_budget"):
                set_pending(f"Estimate a {days}-day travel budget for {cities}. Break down accommodation, food, transport, activities, and buffer with low/mid/high ranges.")

        qa3, qa4 = st.columns(2)
        with qa3:
            if st.button("🍜 Food", use_container_width=True, key="qa_food"):
                set_pending(f"Create a practical food guide for {cities}. What to eat, what to order, where to find it, and common tourist pitfalls.")
        with qa4:
            if st.button("🚕 Transport", use_container_width=True, key="qa_transport"):
                set_pending(f"Give transport guidance for traveling around {cities}. Apps, typical prices, airport transfers, intercity options, and safety tips.")

        qa5, qa6 = st.columns(2)
        with qa5:
            if st.button("🛡️ Safety", use_container_width=True, key="qa_safety"):
                set_pending(f"Give a Vietnam travel safety checklist for {cities}. Include scams to avoid, money safety, taxi/app tips, and emergency steps.")
        with qa6:
            if st.button("✨ Hidden gems", use_container_width=True, key="qa_gems"):
                set_pending(f"Suggest hidden gems and less-crowded experiences for {cities}. Provide specific neighborhoods/areas and best times to go.")

        render_html('<div class="a11-rail-sec"><div class="a11-rail-label">Suggested prompts</div></div>')
        suggestions = [
            "Compare Da Nang vs Hoi An: where should I stay for beach + culture?",
            "What is a realistic 5-day Hanoi + Ha Long + Ninh Binh route with transport timings?",
            "Give a weather-aware packing list and what to buy locally in Vietnam.",
            "Create a day-by-day plan for Ho Chi Minh City focused on food and history.",
            "What are common scams and how to avoid them with specific examples?",
            "Build a motorbike-free Northern Vietnam itinerary (Sa Pa / Ha Giang alternatives).",
            "Where should I stay in Hanoi and why? Recommend areas by vibe and budget.",
            "Design a couples itinerary with romantic spots and calmer evenings.",
            "Best street foods to try first and what phrases to use when ordering.",
            "How to split time between Hue, Da Nang, and Hoi An in 4 days?",
            "Create a premium/luxury itinerary with hotels and curated experiences.",
            "What are good day trips from Hanoi with a tight schedule?",
        ]

    idx = st.session_state.quick_seed % len(suggestions)
    ordered = suggestions[idx:] + suggestions[:idx]

    sp1, sp2 = st.columns(2)
    with sp1:
        for i in [0, 2, 4, 6]:
            if i < len(ordered):
                if st.button(f"• {ordered[i]}", use_container_width=True, key=f"sp_{i}"):
                    set_pending(ordered[i])
    with sp2:
        for i in [1, 3, 5, 7]:
            if i < len(ordered):
                if st.button(f"• {ordered[i]}", use_container_width=True, key=f"sp_{i}"):
                    set_pending(ordered[i])

with left:
    render_html('<div class="shell">')
    for m in st.session_state.messages:
        if m.get("role") == "user":
            chat_bubble_user(m.get("content", ""), avatar_user)
        else:
            chat_bubble_ai(m.get("content", ""), avatar_ai)
    render_html("</div>")

def on_submit():
    st.session_state.pending = st.session_state.msg
    st.session_state.msg = ""

placeholder = "Ask about Vietnam: culture, history, food, etiquette, regions…"
if st.session_state.profile.get("mode") == "Plan" or st.session_state.profile.get("cities") or st.session_state.profile.get("days") is not None:
    placeholder = "Ask about Vietnam (or request an itinerary, routes, costs, logistics)…"

st.chat_input(
    placeholder,
    key="msg",
    on_submit=on_submit,
)

if st.session_state.pending:
    q = (st.session_state.pending or "").strip()
    st.session_state.pending = None
    if q:
        st.session_state.last_user_query = q
        st.session_state.messages.append({"role": "user", "content": q})
        chat_bubble_user(q, avatar_user)

        ai_typing_animation(avatar_ai)

        payload = enrich_query(q, st.session_state.profile)
        answer = post_chat(payload)

        st.session_state.messages.append({"role": "ai", "content": answer})
        scroll_to_bottom()
        st.rerun()

components.html("""
<script>
(function () {
  const parent = window.parent;
  const doc = parent.document;
  function supportsHas() {
    try { return CSS.supports("selector(:has(*))"); } catch(e) { return false; }
  }
  if (supportsHas()) return;

  function applyFallbackSticky() {
    const marker = doc.getElementById("a11_right_rail_marker");
    if (!marker) return false;
    const col = marker.closest('div[data-testid="stColumn"]');
    if (!col) return false;
    col.style.position = "sticky";
    col.style.top = "16px";
    col.style.alignSelf = "flex-start";
    return true;
  }

  let tries = 0;
  const timer = parent.setInterval(() => {
    tries += 1;
    const ok = applyFallbackSticky();
    if (ok || tries >= 80) parent.clearInterval(timer);
  }, 100);
})();
</script>
""", height=0)
