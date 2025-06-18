import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html
from typing import List, Dict, Optional

# ====== CONSTANTS ======
STRESS_QUESTIONS = [
    "🧠 1. In the last 1-4 weeks, I found it hard to wind down.",
    "⚡ 2. In the last 1-4 weeks, I tended to over-react to situations.",
    "🌀 3. In the last 1-4 weeks, I felt restless.",
    "🔥 4. In the last 1-4 weeks, I felt easily agitated.",
    "🌪️ 5. In the last 1-4 weeks, I felt difficult to relax."
]

PERFORMANCE_QUESTIONS = [
    "📉 6. During the past 1-4 weeks, how often was your performance lower than most workers?",
    "⏸️ 7. During the past 1-4 weeks, how often did you do no work when you should?",
    "⚠️ 8. During the past 1-4 weeks, how often did you not work carefully?",
    "🔍 9. During the past 1-4 weeks, how often was your work quality low?",
    "🧩 10. During the past 1-4 weeks, how often did you not fully concentrate?",
    "🏥 11. During the past 1-4 weeks, how often did health problems limit your work?"
]

OPTIONS = ["🌟 Very Rare", "✨ Rare", "💫 Moderate", "⚡ Frequent", "🔥 Very Frequent"]
OPTION_SCORES = {
    "🌟 Very Rare": 1, 
    "✨ Rare": 2, 
    "💫 Moderate": 3, 
    "⚡ Frequent": 4, 
    "🔥 Very Frequent": 5
}

# ====== COLOR THEME ======
COLOR_THEME = {
    "primary": "#6A5ACD",        # Soft purple (reduced saturation)
    "secondary": "#48D1CC",      # Gentle teal
    "accent": "#FFD700",         # Warm gold
    "text": "#2C3E50",           # Dark blue-gray (easy on eyes)
    "bg": "#F5F7FA",             # Very light gray background
    "success": "#27AE60",        # Calm green
    "warning": "#F39C12",        # Muted orange
    "danger": "#E74C3C",         # Soft red
    "info": "#3498DB"            # Friendly blue
}

# ====== UTILITIES ======
def trigger_confetti():
    """Triggers subtle confetti celebration"""
    html("<script>fireConfetti();</script>", height=0)

def calculate_mean(scores: List[int]) -> float:
    """Calculate mean score with safety checks"""
    return sum(scores) / len(scores) if scores else 0

def classify_stress_level(mean: float) -> str:
    """Classify stress with comforting descriptions"""
    if mean < 1.5: return "🌊 Very Low - You're managing stress beautifully"
    elif mean < 2: return "🌤️ Low - Good balance overall" 
    elif mean < 3: return "🌓 Moderate - Time for some self-care"
    elif mean < 4: return "🌋 High - Let's explore ways to relax"
    return "🔥 Very High - Your well-being needs attention"

def classify_performance_level(mean: float) -> str:
    """Classify performance with encouraging language"""
    if mean < 1.5: return "🚀 Excellent - You're performing at your best"
    elif mean < 2: return "🏆 Strong - Consistent quality work"
    elif mean < 3: return "🔄 Good - With room for growth"
    elif mean < 4: return "⚠️ Challenged - Let's identify support"
    return "🛑 Struggling - Your needs deserve focus"

# ====== PAGE SETUP ======
def setup_page():
    """Configure comforting visual environment"""
    st.set_page_config(
        page_title="STRESFORMANCE TRACKER",
        page_icon="🧠💼",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Inject calming animations and fonts
    html(f"""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <script>
    function fireConfetti() {{
        confetti({{
            particleCount: 100,
            spread: 70,
            origin: {{ y: 0.6 }},
            colors: ['{COLOR_THEME["primary"]}', '{COLOR_THEME["secondary"]}'],
            ticks: 100
        }});
    }}
    </script>
    <style>
    :root {{
        --primary: {COLOR_THEME["primary"]};
        --secondary: {COLOR_THEME["secondary"]};
        --accent: {COLOR_THEME["accent"]};
        --text: {COLOR_THEME["text"]};
        --bg: {COLOR_THEME["bg"]};
    }}
    </style>
    """, height=0)

    # Comfort-focused CSS
    st.markdown(f"""
    <style>
    body, .stApp {{
        font-family: 'Poppins', sans-serif;
        background: var(--bg);
        color: var(--text);
        line-height: 1.6;
    }}
    h1 {{
        color: var(--primary);
        font-weight: 600;
        font-size: 2.2rem;
        margin-bottom: 1rem;
    }}
    h2 {{
        color: var(--secondary);
        font-weight: 500;
        font-size: 1.6rem;
        margin-top: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }}
    .stRadio > div {{
        flex-direction: row;
        gap: 1rem;
    }}
    .stRadio > label {{
        font-size: 1rem;
        color: var(--text) !important;
    }}
    .stButton button {{
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        font-weight: 500;
        border: none;
        padding: 0.7rem 1.3rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }}
    .stButton button:hover {{
        transform: translateY(-1px);
        opacity: 0.9;
    }}
    .stMarkdown p {{
        font-size: 1rem;
        color: var(--text) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ====== GAUGE DESIGN ======
def plot_comfort_gauge(value: float, title: str, color: str):
    """Create stress-free gauge visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': title,
            'font': {'size': 16, 'color': color, 'family': "Poppins"}
        },
        gauge={
            'axis': {
                'range': [1, 5],
                'tickvals': [1, 2, 3, 4, 5],
                'tickcolor': 'black',
                'tickfont': {'color': 'black', 'size': 12},
                'linecolor': 'black'
            },
            'bar': {'color': color},
            'bgcolor': 'rgba(255,255,255,0.8)',
            'borderwidth': 1,
            'bordercolor': "gray",
            'steps': [
                {'range': [1, 2], 'color': '#A3E4D7'},  # Calm green
                {'range': [2, 3], 'color': '#FAD7A0'},  # Soft orange
                {'range': [3, 5], 'color': '#F5B7B1'}   # Gentle red
            ],
            'threshold': {
                'line': {'color': color, 'width': 3},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        margin=dict(l=30, r=30, t=50, b=20),
        paper_bgcolor='rgba(255,255,255,0.9)',
        font={'family': "Poppins", 'color': "black"}
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ====== PAGE COMPONENTS ======
def show_header():
    """Welcoming app header"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <lottie-player 
            src="https://assets1.lottiefiles.com/packages/lf20_gn0tojcq.json" 
            background="transparent" 
            speed="1" 
            style="width: 100px; height: 100px; margin: 0 auto;"
            autoplay>
        </lottie-player>
        <h1>STRESFORMANCE TRACKER</h1>
        <p style="color: #7F8C8D;">Your personal well-being and performance companion</p>
    </div>
    """, unsafe_allow_html=True)

def stress_assessment():
    """Comfortable stress assessment interface"""
    show_header()
    st.markdown("""
    <h2>Your Stress Measure</h2>
    <p style="color: #555;">
        Let's understand how you've been feeling recently...
    </p>
    """, unsafe_allow_html=True)
    
    for i, question in enumerate(STRESS_QUESTIONS):
        st.session_state.stress_answers[i] = st.radio(
            question, 
            OPTIONS,
            key=f"stress_{i}",
            index=None
        )
    
    if st.button("Continue to Performance", type="primary"):
        if None in st.session_state.stress_answers:
            st.warning("Please complete all questions to continue")
        else:
            st.session_state.page = 2
            st.rerun()

def performance_assessment():
    """Encouraging performance assessment"""
    show_header()
    st.markdown("""
    <h2>Your Performance Measure</h2>
    <p style="color: #555;">
        Now let's reflect on your work experiences...
    </p>
    """, unsafe_allow_html=True)
    
    for i, question in enumerate(PERFORMANCE_QUESTIONS):
        st.session_state.perf_answers[i] = st.radio(
            question,
            OPTIONS,
            key=f"perf_{i}",
            index=None
        )
    
    col1, col2 = st.columns([1, 2])
    col1.button("Back", on_click=lambda: st.session_state.update(page=1))
    
    if col2.button("View Results", type="primary"):
        if None in st.session_state.perf_answers:
            st.warning("Please complete all questions to see results")
        else:
            st.session_state.page = 3
            st.rerun()

def show_results():
    """Supportive results presentation"""
    trigger_confetti()
    show_header()
    
    # Calculate results
    stress_scores = [OPTION_SCORES[ans] for ans in st.session_state.stress_answers]
    stress_mean = calculate_mean(stress_scores)
    stress_class = classify_stress_level(stress_mean)
    
    perf_scores = [OPTION_SCORES[ans] for ans in st.session_state.perf_answers]
    perf_mean = calculate_mean(perf_scores)
    perf_class = classify_performance_level(perf_mean)
    
    # Results display
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h2>Your Results</h2>
        <p style="color: #555;">Here's what we discovered...</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: white; border-radius: 10px; padding: 1.2rem; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1.5rem;">
            <h3 style="color: {COLOR_THEME['primary']};">🧠 Stress Level</h3>
            <p style="font-size: 1.8rem; font-weight: 600; color: {COLOR_THEME['primary']}; 
               margin: 0.5rem 0;">{stress_mean:.1f}/5.0</p>
            <p style="color: #555;">{stress_class}</p>
        </div>
        """, unsafe_allow_html=True)
        plot_comfort_gauge(stress_mean, "Stress Meter", COLOR_THEME["primary"])
    
    with col2:
        st.markdown(f"""
        <div style="background: white; border-radius: 10px; padding: 1.2rem; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1.5rem;">
            <h3 style="color: {COLOR_THEME['secondary']};">💼 Performance Level</h3>
            <p style="font-size: 1.8rem; font-weight: 600; color: {COLOR_THEME['secondary']}; 
               margin: 0.5rem 0;">{perf_mean:.1f}/5.0</p>
            <p style="color: #555;">{perf_class}</p>
        </div>
        """, unsafe_allow_html=True)
        plot_comfort_gauge(perf_mean, "Performance Meter", COLOR_THEME["secondary"])
    
    # Supportive recommendations
    st.markdown("""
    <div style="background: white; border-radius: 10px; padding: 1.2rem; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-top: 1.5rem;">
        <h3 style="color: #333;">📝 Personalized Suggestions</h3>
        <ul style="color: #555;">
            <li>Practice 5-minute breathing exercises daily</li>
            <li>Schedule regular short breaks during work</li>
            <li>Maintain a consistent sleep routine</li>
            <li>Celebrate small accomplishments</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.button("Start New Assessment", 
              on_click=lambda: (
                  st.session_state.clear(),
                  st.session_state.update(page=1),
                  st.rerun()
              ),
              type="primary")

# ====== MAIN APP ======
def main():
    """Run the comforting assessment app"""
    setup_page()
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = 1
    if "stress_answers" not in st.session_state:
        st.session_state.stress_answers = [None] * len(STRESS_QUESTIONS)
    if "perf_answers" not in st.session_state:
        st.session_state.perf_answers = [None] * len(PERFORMANCE_QUESTIONS)
    
    # Page routing
    if st.session_state.page == 1:
        stress_assessment()
    elif st.session_state.page == 2:
        performance_assessment()
    elif st.session_state.page == 3:
        show_results()

if __name__ == "__main__":
    main()
