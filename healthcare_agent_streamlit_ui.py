import os
import time
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# ============================================================
# SentiMed — Premium Healthcare AI Dashboard (Streamlit)
# UI redesigned for Streamlit. CrewAI/Gemini consultation logic
# and specialist prompts are preserved from the original project.
# ============================================================

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="SentiMed | Health Overview",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "primary": "#174F50",
    "teal": "#2B9998",
    "teal_light": "#DDF4F1",
    "coral": "#F56B70",
    "orange": "#F6A85D",
    "ink": "#102B2B",
    "muted": "#728181",
    "canvas": "#F4F7F6",
    "white": "#FFFFFF",
    "border": "#E4ECEA",
}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --teal:#2B9998; --deep:#174F50; --ink:#102B2B; --muted:#728181; --canvas:#F4F7F6; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:var(--canvas); color:var(--ink); }
    .block-container { max-width:1500px; padding-top:1.25rem; padding-bottom:2.5rem; }
    [data-testid="stSidebar"] { background:#FFFFFF; border-right:1px solid #E4ECEA; }
    [data-testid="stSidebar"] .block-container { padding-top:1.4rem; }
    .brand { display:flex; align-items:center; gap:10px; font-family:Manrope,sans-serif; font-size:1.35rem; font-weight:800; color:#102B2B; margin-bottom:1.1rem; }
    .brand-mark { width:38px; height:38px; border:3px solid #2B9998; border-right-color:transparent; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#2B9998; font-size:20px; }
    .side-caption { font-size:.72rem; color:#93A3A1; text-transform:uppercase; letter-spacing:.13em; font-weight:700; margin:1.35rem 0 .6rem; }
    .profile-box { background:#F4F8F7; border:1px solid #E4ECEA; border-radius:16px; padding:14px; margin-top:1.4rem; }
    .eyebrow { color:#2B9998; font-weight:700; letter-spacing:.1em; text-transform:uppercase; font-size:.72rem; margin-bottom:.35rem; }
    .page-title { font-family:Manrope,sans-serif; font-size:clamp(2rem,3vw,3rem); line-height:1.12; font-weight:800; color:#102B2B; letter-spacing:-.055em; margin:.1rem 0 .35rem; }
    .subhead { color:#728181; font-size:.96rem; margin-bottom:1.2rem; }
    .panel { background:#FFFFFF; border:1px solid #E4ECEA; border-radius:22px; padding:20px 22px; box-shadow:0 7px 24px rgba(20,65,62,.035); margin-bottom:16px; }
    .panel-head { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:15px; }
    .panel-title { font-family:Manrope,sans-serif; font-size:1.05rem; font-weight:800; color:#102B2B; }
    .panel-note { font-size:.8rem; color:#9AA8A6; }
    .vital-card { background:#FFFFFF; border:1px solid #E4ECEA; border-radius:18px; padding:15px 15px 14px; min-height:130px; box-shadow:0 5px 18px rgba(20,65,62,.025); }
    .vital-icon { display:inline-flex; width:35px; height:35px; border-radius:50%; align-items:center; justify-content:center; background:#FFE9E8; color:#E95F65; font-size:1.1rem; margin-bottom:10px; }
    .vital-label { color:#728181; font-size:.8rem; font-weight:600; }
    .vital-value { color:#102B2B; font-family:Manrope,sans-serif; font-size:1.65rem; font-weight:800; letter-spacing:-.04em; line-height:1.25; }
    .status-good { color:#2B9998; font-size:.75rem; font-weight:700; margin-left:5px; }
    .report-tile { border-radius:15px; background:linear-gradient(140deg,#D7EBE8,#F7FAF9); min-height:128px; padding:13px; display:flex; flex-direction:column; justify-content:space-between; border:1px solid #E4ECEA; }
    .report-icon { font-size:1.25rem; color:#2B9998; }
    .report-date { color:#728181; font-size:.68rem; }
    .report-name { color:#102B2B; font-size:.86rem; font-weight:700; line-height:1.25; }
    .med-row { display:grid; grid-template-columns:82px 1fr; gap:12px; align-items:center; margin:13px 0; }
    .med-day { color:#8B9998; font-size:.76rem; }
    .med-track { height:38px; border-bottom:1px dashed #C9D5D3; display:flex; align-items:center; }
    .med-pill { display:inline-flex; align-items:center; gap:9px; background:#174F50; color:white; border-radius:30px; padding:7px 12px; font-size:.82rem; font-weight:600; max-width:100%; }
    .med-dose { background:#2B9998; border-radius:18px; padding:3px 8px; font-size:.72rem; white-space:nowrap; }
    .appt-card { background:#174F50; border-radius:17px; color:white; padding:16px; min-height:180px; height:100%; }
    .appt-date { font-size:.75rem; color:#D0E5E2; margin-bottom:15px; }
    .appt-title { font-size:.95rem; font-weight:700; line-height:1.35; min-height:44px; }
    .appt-doctor { font-size:.77rem; color:#D0E5E2; margin-top:14px; }
    .soft-chip { display:inline-block; background:#E1F5F1; color:#247F7D; border-radius:20px; padding:5px 10px; font-size:.75rem; font-weight:700; }
    .chat-bubble { border-radius:16px; padding:16px 18px; background:#F2F8F7; border:1px solid #DCEBE8; line-height:1.65; white-space:pre-wrap; }
    .disclaimer { border-left:4px solid #F6A85D; padding:10px 13px; background:#FFF8ED; color:#775B32; border-radius:8px; font-size:.82rem; }
    div.stButton > button { border-radius:12px; min-height:43px; font-weight:700; border:1px solid #D9E6E3; }
    div.stButton > button[kind="primary"] { background:#174F50; color:#FFFFFF; border:0; }
    div.stButton > button[kind="primary"]:hover { background:#226B6B; color:#FFFFFF; }
    div[data-testid="stMetric"] { background:#FFFFFF; border:1px solid #E4ECEA; padding:14px 16px; border-radius:16px; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid #E4ECEA; }
    .stTabs [data-baseweb="tab"] { border-radius:10px 10px 0 0; padding:10px 16px; }
    @media (max-width: 800px) {
      .block-container { padding-left:1rem; padding-right:1rem; }
      .panel { padding:15px; }
      .page-title { font-size:2rem; }
      .med-row { grid-template-columns:60px 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Session state ----------
defaults = {
    "page": "Overview",
    "specialist": "Medical Advisor",
    "query": "",
    "last_result": "",
    "last_specialist": "",
    "last_timestamp": "",
    "history": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

SPECIALISTS = [
    "Medical Advisor",
    "Symptom Analyzer",
    "Treatment Recommender",
    "Nutrition Specialist",
    "Mental Health Counselor",
    "Fitness Coach",
    "Disease Educator",
    "Preventive Medicine Expert",
    "Emergency Response Advisor",
]

AGENT_CONFIGS = {
    "Medical Advisor": {
        "role": "Medical Advisor",
        "goal": "Provide accurate medical information and comprehensive guidance",
        "backstory": """You are an experienced medical advisor with extensive knowledge of various medical conditions, symptoms, and treatments. You provide clear, evidence-based medical information while emphasizing the importance of consulting healthcare professionals for diagnosis and treatment.""",
    },
    "Symptom Analyzer": {
        "role": "Symptom Analyzer",
        "goal": "Analyze symptoms and suggest possible conditions",
        "backstory": """You are a symptom analysis expert trained to identify patterns in patient-reported symptoms. You provide possible explanations for symptoms, assess severity, and recommend when immediate medical attention is needed.""",
    },
    "Treatment Recommender": {
        "role": "Treatment Recommender",
        "goal": "Suggest evidence-based treatment options",
        "backstory": """You are a treatment specialist knowledgeable about various medical treatments, medications, and therapies. You provide comprehensive treatment information while emphasizing proper medical supervision.""",
    },
    "Nutrition Specialist": {
        "role": "Nutrition Specialist",
        "goal": "Provide dietary guidance and nutritional advice",
        "backstory": """You are a certified nutritionist with expertise in therapeutic nutrition and dietary management of diseases. You provide personalized nutritional guidance based on health conditions.""",
    },
    "Mental Health Counselor": {
        "role": "Mental Health Counselor",
        "goal": "Provide mental health support and coping strategies",
        "backstory": """You are a compassionate mental health counselor trained in psychology and therapeutic techniques. You provide emotional support, coping strategies, and guidance for mental health concerns.""",
    },
    "Fitness Coach": {
        "role": "Fitness Coach",
        "goal": "Provide exercise guidance and fitness recommendations",
        "backstory": """You are a certified fitness coach with expertise in exercise physiology and rehabilitation. You create safe, effective exercise recommendations tailored to individual health conditions.""",
    },
    "Disease Educator": {
        "role": "Disease Educator",
        "goal": "Educate about diseases, prevention, and management",
        "backstory": """You are a health educator specializing in disease information and prevention strategies. You explain complex medical concepts in clear language.""",
    },
    "Preventive Medicine Expert": {
        "role": "Preventive Medicine Expert",
        "goal": "Provide prevention strategies and wellness recommendations",
        "backstory": """You are a preventive medicine expert focused on disease prevention and health promotion. You provide actionable recommendations for maintaining health.""",
    },
    "Emergency Response Advisor": {
        "role": "Emergency Response Advisor",
        "goal": "Provide emergency guidance and critical response information",
        "backstory": """You are an emergency medicine advisor trained in crisis management. You provide immediate guidance for emergencies and identify when to call emergency services.""",
    },
}

def run_ai_consultation(query: str, specialist: str) -> tuple[str, bool]:
    """Preserves the original CrewAI/Gemini consultation approach and fallback."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    config = AGENT_CONFIGS.get(specialist, AGENT_CONFIGS["Medical Advisor"])
    if not API_KEY:
        return (
            "GOOGLE_API_KEY was not found in your .env file.\n\n"
            "Add GOOGLE_API_KEY=your_actual_key to .env, restart Streamlit, and try again.",
            False,
        )
    try:
        llm = LLM(model="gemini/gemini-2.5-flash", temperature=0.7, api_key=API_KEY)
        agent = Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=False,
            llm=llm,
        )
        task = Task(
            description=f"""
As a {specialist}, analyze the following health query and provide helpful guidance:

QUERY: {query}

INSTRUCTIONS:
1. Provide clear, accurate information
2. If symptoms are mentioned, explain possible conditions (not diagnoses)
3. Suggest when to seek medical attention
4. Provide practical recommendations
5. Always remind this is informational, not medical advice
6. Be compassionate and supportive

Provide a comprehensive, well-structured response.
""",
            agent=agent,
            expected_output="Comprehensive healthcare guidance",
        )
        crew = Crew(agents=[agent], tasks=[task], verbose=False)
        result = crew.kickoff()
        formatted = (
            f"### 🩺 {specialist}\n"
            f"**Consultation date:** {timestamp}\n\n"
            f"{result}\n\n"
            "---\n\n"
            "**Medical disclaimer**\n"
            "This guidance is informational only and not a substitute for professional "
            "medical advice. Always consult qualified healthcare professionals for "
            "diagnosis, treatment, and emergency situations."
        )
        return formatted, True
    except Exception as exc:
        # Retain the original friendly fallback behavior, clearly labelled as simulated.
        simulated = f"""### 🩺 {specialist} — Demo Response
**Consultation date:** {timestamp}

The live AI consultation could not complete (network or API error). This is a simulated sample response for interface testing, not a personalized assessment.

- Symptoms can have many causes; avoid assuming a diagnosis based on limited information.
- Seek urgent medical attention for sudden severe symptoms, breathing difficulty, chest pain, fainting, or rapidly worsening conditions.
- For ongoing or concerning symptoms, contact a qualified healthcare professional.

**Simulated response only.** Original error: {exc}

---
**Medical disclaimer:** This information is not a substitute for professional medical advice."""
        return simulated, False

def panel_header(title, note=""):
    st.markdown(
        f'<div class="panel-head"><div class="panel-title">{title}</div>'
        f'<div class="panel-note">{note}</div></div>',
        unsafe_allow_html=True,
    )

def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="brand"><span class="brand-mark">⌁</span><span>SentiMed</span></div>',
            unsafe_allow_html=True,
        )
        st.caption("MULTI-AGENT WELLNESS NETWORK")
        st.markdown('<div class="side-caption">Workspace</div>', unsafe_allow_html=True)
        pages = {
            "Overview": "▦  Overview",
            "Analytics": "▥  Analytics",
            "Appointments": "♧  Appointments",
            "AI Chat": "▤  AI Chat",
            "Calendar": "▣  Calendar",
        }
        for page, label in pages.items():
            if st.button(label, key=f"nav_{page}", use_container_width=True,
                         type="primary" if st.session_state.page == page else "secondary"):
                st.session_state.page = page
                st.rerun()
        st.markdown('<div class="side-caption">Health tools</div>', unsafe_allow_html=True)
        if st.button("♡  Health Assessment", use_container_width=True):
            st.session_state.page = "Health Assessment"
            st.rerun()
        if st.button("✦  Wellness Tips", use_container_width=True):
            st.session_state.page = "Wellness Tips"
            st.rerun()
        if st.button("♙  Specialists", use_container_width=True):
            st.session_state.page = "Specialists"
            st.rerun()
        if st.button("☷  Consultation History", use_container_width=True):
            st.session_state.page = "History"
            st.rerun()
        mode = "Demo mode" if not API_KEY else "AI connected"
        dot = "🟠" if not API_KEY else "🟢"
        st.markdown(
            f'<div class="profile-box"><b>◉  SentiMed status</b><br>'
            f'<span style="color:#728181;font-size:.82rem">{dot} {mode}</span><br><br>'
            f'<span style="font-size:.78rem;color:#728181">Designed by Satyajit Jagtap</span></div>',
            unsafe_allow_html=True,
        )

def page_header(eyebrow, title, subtitle):
    st.markdown(
        f'<div class="eyebrow">{eyebrow}</div><div class="page-title">{title}</div>'
        f'<div class="subhead">{subtitle}</div>',
        unsafe_allow_html=True,
    )

def render_vital(icon, label, value, status="Good"):
    st.markdown(
        f'<div class="vital-card"><div class="vital-icon">{icon}</div>'
        f'<div class="vital-label">{label}<span class="status-good">{status}</span></div>'
        f'<div class="vital-value">{value}</div></div>',
        unsafe_allow_html=True,
    )

def render_overview():
    page_header("YOUR WELLNESS AT A GLANCE", "Health Overview", "A calmer, clearer view of your healthcare journey.")
    left, right = st.columns([0.92, 1.65], gap="large")
    with left:
        st.markdown('<div class="panel"><div class="panel-head"><div class="panel-title">Your health snapshot</div><span class="soft-chip">Example data</span></div>', unsafe_allow_html=True)
        v1, v2 = st.columns(2, gap="small")
        with v1:
            render_vital("♥", "Blood Pressure", "112/75", "Good")
        with v2:
            render_vital("♡", "Heart Rate", "78 bpm", "Normal")
        v3, v4 = st.columns(2, gap="small")
        with v3:
            render_vital("◉", "Blood Oxygen", "98%", "Good")
        with v4:
            render_vital("✚", "Hemoglobin", "13.8 g/dL", "Example")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            '<div class="panel"><div class="panel-title">A note about your dashboard</div>'
            '<p style="color:#728181;font-size:.88rem;line-height:1.6;margin-bottom:0">'
            'The vital-sign values shown here are illustrative UI sample data, not readings from a connected device or medical record.</p></div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Your reports", "Powered by AI")
        reports = [
            ("🩺", "24 Apr 2026", "Monthly health report"),
            ("✦", "05 Oct 2026", "Wellness insights"),
            ("♡", "18 Sep 2026", "Heart health guide"),
            ("◉", "02 Sep 2026", "Blood report guide"),
        ]
        cols = st.columns(4, gap="small")
        for col, (icon, date, name) in zip(cols, reports):
            with col:
                st.markdown(
                    f'<div class="report-tile"><div class="report-icon">{icon}</div>'
                    f'<div><div class="report-date">{date}</div><div class="report-name">{name}</div></div></div>',
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Medication schedule", "Sample schedule")
        meds = [
            ("Mon 12", "💊  Metformin · 500 mg", "Morning"),
            ("Wed 14", "☀️  Vitamin D · 1000 IU", "Daily"),
            ("Fri 16", "💊  Medication reminder", "Evening"),
        ]
        for day, medicine, dose in meds:
            st.markdown(
                f'<div class="med-row"><div class="med-day">{day}</div><div class="med-track">'
                f'<span class="med-pill">{medicine}<span class="med-dose">{dose}</span></span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown('<div class="panel-note">Illustrative schedule only — no medication has been prescribed by this app.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Upcoming care", "Example appointments")
        appts = [
            ("24 Oct", "Annual check-up", "Dr. Meera Shah", "●"),
            ("31 Oct", "Nutrition review", "Wellness clinic", "✚"),
            ("02 Nov", "Video consultation", "Dr. Arjun Rao", "◉"),
        ]
        cols = st.columns(3, gap="small")
        for col, (date, title, doctor, icon) in zip(cols, appts):
            with col:
                st.markdown(
                    f'<div class="appt-card"><div class="appt-date">{icon} &nbsp; {date}</div>'
                    f'<div class="appt-title">{title}</div><div class="appt-doctor">♙ &nbsp; {doctor}</div></div>',
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

def render_consultation():
    page_header("PERSONALIZED AI SUPPORT", "AI Health Consultation", "Choose a specialist and describe what you would like help understanding.")
    left, right = st.columns([0.92, 1.08], gap="large")
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Start a consultation", "Private to this session")
        specialist = st.selectbox("Choose your specialist", SPECIALISTS,
                                  index=SPECIALISTS.index(st.session_state.specialist))
        st.session_state.specialist = specialist
        query = st.text_area(
            "Describe your health concern",
            value=st.session_state.query,
            height=210,
            placeholder="Share your question, symptoms, duration, and any relevant context...",
            help="Avoid entering identifying information such as your full name, address, or medical record number.",
        )
        st.session_state.query = query
        col1, col2 = st.columns([2, 1])
        with col1:
            submit = st.button("✦  Get AI Guidance", type="primary", use_container_width=True)
        with col2:
            clear = st.button("Clear", use_container_width=True)
        if clear:
            st.session_state.query = ""
            st.session_state.last_result = ""
            st.rerun()
        if submit:
            if not query.strip():
                st.warning("Please describe your health question before continuing.")
            else:
                with st.spinner(f"{specialist} is reviewing your question…"):
                    result, live = run_ai_consultation(query.strip(), specialist)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.last_result = result
                st.session_state.last_specialist = specialist
                st.session_state.last_timestamp = timestamp
                st.session_state.history.insert(0, {
                    "timestamp": timestamp,
                    "specialist": specialist,
                    "query": query.strip(),
                    "result": result,
                    "live": live,
                })
                if live:
                    st.success("Consultation completed.")
                elif API_KEY:
                    st.warning("A sample fallback response was returned because the live consultation failed.")
                else:
                    st.info("Demo mode: add GOOGLE_API_KEY to your .env file to enable live consultation.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            '<div class="disclaimer">For information and education only. This tool cannot diagnose conditions or replace a qualified clinician. For a medical emergency, contact local emergency services.</div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_header("Your guidance", "AI-generated response")
        if st.session_state.last_result:
            st.caption(f"{st.session_state.last_specialist} · {st.session_state.last_timestamp}")
            st.markdown(st.session_state.last_result)
        else:
            st.markdown(
                '<div class="chat-bubble"><b>Welcome to SentiMed</b><br><br>'
                'Your response will appear here after you submit a question. Choose a specialist to tailor the focus of the guidance.<br><br>'
                '<span style="color:#728181;font-size:.86rem">Helpful tip: Include how long you have experienced a symptom and whether it is getting better or worse.</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

def render_assessment():
    page_header("HEALTH TOOLS", "Health Assessment", "A structured checklist to help prepare for a conversation with a clinician.")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.info("This checklist does not calculate a diagnosis or assess medical risk.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Vital signs")
        st.checkbox("Blood pressure reading available")
        st.checkbox("Heart rate reading available")
        st.checkbox("Temperature reading available")
        st.checkbox("Oxygen saturation reading available")
        st.markdown("#### Current concerns")
        st.checkbox("I can describe when symptoms started")
        st.checkbox("I can describe severity and changes")
    with c2:
        st.markdown("#### Health background")
        st.checkbox("Current medicines and supplements listed")
        st.checkbox("Allergies and sensitivities listed")
        st.checkbox("Relevant medical history noted")
        st.markdown("#### Lifestyle")
        st.checkbox("Sleep and energy patterns considered")
        st.checkbox("Diet, hydration, and activity considered")
        st.checkbox("Stress and mood considered")
    notes = st.text_area("Notes to discuss with a healthcare professional", placeholder="Add any questions you want to remember…")
    if st.button("Prepare consultation notes", type="primary"):
        st.text_area("Your notes", value=notes or "No notes entered.", height=120)
    st.markdown("</div>", unsafe_allow_html=True)

def render_wellness():
    page_header("SMALL STEPS, BETTER HABITS", "Wellness & Prevention", "General wellness ideas to discuss with your healthcare professional.")
    tips = [
        ("🥗", "Nutrition", "Aim for varied meals with vegetables, fruit, whole grains, and suitable protein. Individual needs vary."),
        ("🚶", "Movement", "Choose physical activity that fits your ability and health. Build up gradually and seek advice if unsure."),
        ("🌙", "Sleep", "Keep a consistent sleep routine and make time to wind down before bed."),
        ("🧘", "Stress care", "Try paced breathing, short breaks, or supportive conversations when stress builds."),
        ("💧", "Hydration", "Drink fluids regularly, adjusting to your activity, climate, and any clinician-directed restrictions."),
        ("🩺", "Preventive care", "Keep recommended screenings and check-ups based on your age, history, and local guidance."),
        ("💚", "Mental wellbeing", "Stay connected with trusted people and seek professional support when you need it."),
        ("📚", "Stay informed", "Use reputable health sources and ask a qualified clinician about advice that conflicts.")
    ]
    cols = st.columns(2, gap="large")
    for i, (icon, title, description) in enumerate(tips):
        with cols[i % 2]:
            st.markdown(
                f'<div class="panel"><div style="font-size:1.5rem;margin-bottom:8px">{icon}</div>'
                f'<div class="panel-title">{title}</div><p style="color:#728181;line-height:1.6;margin-bottom:0">{description}</p></div>',
                unsafe_allow_html=True,
            )

def render_specialists():
    page_header("THE RIGHT FOCUS FOR YOUR QUESTION", "Healthcare Specialists", "Select a specialist in the AI Chat page to tailor the response focus.")
    descriptions = [
        ("Medical Advisor", "🏥", "General health information and practical next steps"),
        ("Symptom Analyzer", "⌕", "Organize symptom details and possible explanations"),
        ("Treatment Recommender", "✚", "Explain treatment options to discuss with a clinician"),
        ("Nutrition Specialist", "🥗", "General nutrition and dietary education"),
        ("Mental Health Counselor", "♡", "Supportive coping strategies and wellbeing resources"),
        ("Fitness Coach", "↗", "General movement and fitness guidance"),
        ("Disease Educator", "▤", "Understand conditions and common terminology"),
        ("Preventive Medicine Expert", "🛡", "Prevention and health-promotion information"),
        ("Emergency Response Advisor", "!", "Recognize urgent situations and seek emergency help"),
    ]
    cols = st.columns(3, gap="medium")
    for i, (name, icon, desc) in enumerate(descriptions):
        with cols[i % 3]:
            st.markdown(
                f'<div class="panel" style="min-height:155px"><div style="font-size:1.5rem;color:#2B9998">{icon}</div>'
                f'<div class="panel-title" style="margin-top:8px">{name}</div>'
                f'<p style="color:#728181;font-size:.86rem;line-height:1.5">{desc}</p></div>',
                unsafe_allow_html=True,
            )
            if st.button("Use specialist", key=f"use_{i}", use_container_width=True):
                st.session_state.specialist = name
                st.session_state.page = "AI Chat"
                st.rerun()

def render_history():
    page_header("YOUR RECENT SESSIONS", "Consultation History", "History is kept for the current browser session and is not permanently stored.")
    if not st.session_state.history:
        st.markdown('<div class="panel">No consultations yet. Open AI Chat to start your first consultation.</div>', unsafe_allow_html=True)
        return
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"{item['timestamp']}  ·  {item['specialist']}"):
            st.markdown("**Question**")
            st.write(item["query"])
            st.markdown("**Response**")
            st.markdown(item["result"])
    if st.button("Clear consultation history"):
        st.session_state.history = []
        st.session_state.last_result = ""
        st.rerun()

def render_analytics():
    page_header("YOUR ACTIVITY", "Analytics", "A simple summary of consultations in this active session.")
    total = len(st.session_state.history)
    st_cols = st.columns(3)
    st_cols[0].metric("Consultations", total)
    st_cols[1].metric("Specialists used", len(set(x["specialist"] for x in st.session_state.history)))
    st_cols[2].metric("Live AI responses", sum(1 for x in st.session_state.history if x["live"]))
    if st.session_state.history:
        counts = {}
        for item in st.session_state.history:
            counts[item["specialist"]] = counts.get(item["specialist"], 0) + 1
        st.bar_chart(counts)
    else:
        st.info("Your activity chart will appear after you complete a consultation.")

def render_appointments():
    page_header("PLAN YOUR NEXT STEP", "Appointments", "Sample appointment cards for the dashboard design.")
    st.info("These are illustrative examples only. This app does not book real medical appointments.")
    cols = st.columns(3, gap="large")
    for col, date, title, doctor in zip(
        cols,
        ["24 Oct", "31 Oct", "02 Nov"],
        ["Annual check-up", "Nutrition review", "Video consultation"],
        ["Dr. Meera Shah", "Wellness clinic", "Dr. Arjun Rao"],
    ):
        with col:
            st.markdown(
                f'<div class="appt-card"><div class="appt-date">● &nbsp; {date}</div>'
                f'<div class="appt-title">{title}</div><div class="appt-doctor">♙ &nbsp; {doctor}</div></div>',
                unsafe_allow_html=True,
            )

def render_calendar():
    page_header("YOUR SCHEDULE", "Calendar", "Example calendar view. No appointments are stored or booked by this demo.")
    today = datetime.now()
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader(today.strftime("%B %Y"))
    st.caption("Use this view as a UI starting point; connect a real calendar or scheduling backend if needed.")
    st.markdown("</div>", unsafe_allow_html=True)

render_sidebar()

# Top utility strip
top_l, top_r = st.columns([6, 1])
with top_l:
    st.caption("SENTIMED  /  MULTI-AGENT WELLNESS NETWORK")
with top_r:
    st.markdown(
        f'<div style="text-align:right;color:#2B9998;font-weight:700;padding-top:3px">'
        f'{"● AI ready" if API_KEY else "● Demo mode"}</div>',
        unsafe_allow_html=True,
    )

page = st.session_state.page
if page == "Overview":
    render_overview()
elif page == "AI Chat":
    render_consultation()
elif page == "Health Assessment":
    render_assessment()
elif page == "Wellness Tips":
    render_wellness()
elif page == "Specialists":
    render_specialists()
elif page == "History":
    render_history()
elif page == "Analytics":
    render_analytics()
elif page == "Appointments":
    render_appointments()
elif page == "Calendar":
    render_calendar()
else:
    render_overview()

st.markdown(
    '<div style="text-align:center;color:#9AA8A6;font-size:.76rem;padding:18px 0 4px">'
    'SentiMed · AI-powered health information · Not a substitute for professional medical care</div>',
    unsafe_allow_html=True,
)
