
import streamlit as st
import plotly.graph_objects as go
from streamlit.components.v1 import html
from typing import List, Dict, Optional

# ========== CONSTANTS ==========
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

# ========== SETUP ==========
def setup_page():
    """Configure premium page settings"""
    st.set_page_config(
        page_title="STRESFORMANCE   TRACKER",
        page_icon="🧠💼",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Inject premium animations and effects
    html(f"""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/conflict.browser.min.js"></script>
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <script>
    function fireConfetti() {{
        confetti({{
            particleCount: 200,
            spread: 90,
            origin: {{ y: 0.6 }},
            colors: ['#8A2BE2', '#00CED1', '#FFD700', '#FF6347'],
            shapes: ['circle', 'square', 'star']
        }});
    }}
    </script>
    <style>
    :root {{
        --primary: #8A2BE2;
        --secondary: #00CED1;
        --accent: #FFD700;
        --text: #000000;
        --bg: #0A0A1A;
    }}
    </style>
    """, height=0)

    # Premium CSS styling
    st.markdown(f"""
    <style>
    body, .stApp {{
        font-family: 'Poppins', sans-serif;
        background: var(--bg);
        color: var(--text);
        background-image: radial-gradient(circle at 10% 20%, rgba(138, 43, 226, 0.1) 0%, rgba(0, 206, 209, 0.05) 90%);
    }}
    .custom-title{{
    font-size: 1.1rem;
    white-space:nowrap;
    overflow: hidden;
    text-overflow:ellipsis;
    width:100%;
    display:block;
    text-align:center;
    line-height:1.2;
    margin-bottom:0.3rem;
    }}

    
    h2 {{
        color: var(--secondary);
        font-weight: 600;
        font-size: 1.8rem;
        text-shadow: 0 0 8px rgba(0, 206, 209, 0.5);
        margin-top: 1.8rem;
        border-bottom: 2px solid var(--accent);
        padding-bottom: 0.5rem;
    }}
    .stRadio > div {{
        flex-direction: row;
        gap: 1.5rem;
    }}
    .stRadio > label {{
        font-size: 1.1rem;
        color: var(--text) !important;
    }}
    .stButton button {{
        background: linear-gradient(135deg, var(--primary), var(--secondary);
        color: black;
        font-weight: 600;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
        transition: all 0.3s ease;
    }}
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(138, 43, 226, 0.6);
    }}
    .stMarkdown p {{
        font-size: 1.1rem;
        line-height: 1.6;
        color: var(--text) !important;
    }}
    .stMetric {{
        background: rgba(10, 10, 30, 0.7);
        border-radius: 16px;
        padding: 1rem;
        border-left: 4px solid var(--accent);
    }}
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ========== CORE FUNCTIONS ==========
def trigger_confetti():
    """Triggers premium confetti animation"""
    html("<script>fireConfetti();</script>", height=0)

def calculate_mean(scores: List[int]) -> float:
    """Calculate mean score with safety checks"""
    return sum(scores) / len(scores) if scores else 0

def classify_stress_level(mean: float) -> str:
    """Classify stress with emoji indicators"""
    if mean < 1.5: return "🌊 Very Low - Excellent Resilience"
    elif mean < 2: return "🌤️ Low - Good Balance" 
    elif mean < 3: return "🌓 Moderate - Needs Attention"
    elif mean < 4: return "🌋 High - Significant Stress"
    return "🔥 Very High - Critical Levels"

def classify_performance_level(mean: float) -> str:
    """Classify performance with emoji indicators"""
    if mean < 1.5: return "🚀 Very High - Peak Performance"
    elif mean < 2: return "🏆 High - Strong Output"
    elif mean < 3: return "🔄 Moderate - Room for Improvement"
    elif mean < 4: return "⚠️ Low - Needs Support"
    return "😢 Very Low - Very Unproductive"

#Gauge
def plot_dynamic_gauge(value: float, title: str, is_stress: bool):
    """Create gauge with dynamic colors and glowing effects"""
    # Determine colors and effects based on value and meter type
    if is_stress:
        if value >= 4.5:  # Very High Stress
            number_color = "#FF0000"  # Bright red
            glow = "0 0 10px #FF0000, 0 0 20px #FF0000"
            bar_color = "#FF0000"
        elif value >= 4:  # High Stress
            number_color = "#FF4500"  # Orange-red
            glow = "0 0 5px #FF4500"
            bar_color = "#FF4500"
        elif value >= 3:  # Moderate Stress
            number_color = "#FFD700"  # Gold
            glow = "none"
            bar_color = "#FFD700"
        elif value >= 2:  # Low Stress
            number_color = "#90EE90"  # Light green
            glow = "none"
            bar_color = "#90EE90"
        else:  # Very Low Stress
            number_color = "#32CD32"  # Lime green
            glow = "0 0 10px #32CD32, 0 0 20px #32CD32"
            bar_color = "#32CD32"
    else:  # Performance meter (opposite colors)
        if value >= 4.5:  # Very High Performance
            number_color = "#32CD32"  # Lime green
            glow = "0 0 10px #32CD32, 0 0 20px #32CD32"
            bar_color = "#32CD32"
        elif value >= 4:  # High Performance
            number_color = "#90EE90"  # Light green
            glow = "none"
            bar_color = "#90EE90"
        elif value >= 3:  # Moderate Performance
            number_color = "#FFD700"  # Gold
            glow = "none"
            bar_color = "#FFD700"
        elif value >= 2:  # Low Performance
            number_color = "#FF4500"  # Orange-red
            glow = "none"
            bar_color = "#FF4500"
        else:  # Very Low Performance
            number_color = "#FF0000"  # Bright red
            glow = "0 0 10px #FF0000, 0 0 20px #FF0000"
            bar_color = "#FF0000"

    # Create custom number display with glow effect
    st.markdown(
        f'<div style="text-align: left; font-size: 2.5rem; font-weight: bold; '
        f'color: {number_color}; text-shadow: {glow}; margin: 10px 0;">'
        f'{value:.1f}</div>',
        unsafe_allow_html=True
    )

    # Create gauge figure
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': title,
            'font': {'size': 18, 'color': 'black', 'family': "Poppins"}
        },
        gauge={
            'axis': {
                'range': [1, 5],
                'tickvals': [1, 2, 3, 4, 5],
                'tickcolor': 'black',
                'tickfont': {'color': 'black', 'size': 12}
            },
            'bar': {'color': bar_color},
            'bgcolor': 'rgba(255,255,255,0.8)',
            'borderwidth': 1,
            'bordercolor': "gray",
            'steps': [
                {'range': [1, 2], 'color': '#A3E4D7' if is_stress else '#F5B7B1'},
                {'range': [2, 3], 'color': '#FAD7A0' if is_stress else '#FAD7A0'},
                {'range': [3, 4], 'color': '#F5B7B1' if is_stress else '#A3E4D7'},
                {'range': [4, 5], 'color': '#8B0000' if is_stress else '#27AE60'}
            ],
            'threshold': {
                'line': {'color': bar_color, 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(255,255,255,0.9)',
        font={'family': "Poppins", 'color': "black"}
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ========== PAGE COMPONENTS ==========
def show_header():
    """Premium app header with animation"""
    st.markdown("""
    <style>
    @keyframes pulseGlow {
        0% {
            text-shadow:
                0 0 5px #00d0ff,
                0 0 10px #00d0ff,
                0 0 20px #00d0ff,
                0 0 30px #00d0ff;
        }
        50% {
            text-shadow:
                0 0 2px #00aaff,
                0 0 4px #00aaff,
                0 0 8px #00aaff,
                0 0 12px #00aaff;
        }
        100% {
            text-shadow:
                0 0 5px #00d0ff,
                0 0 10px #00d0ff,
                0 0 20px #00d0ff,
                0 0 30px #00d0ff;
        }
    }

    .custom-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
        text-align: center;
        animation: pulseGlow 3s infinite ease-in-out;
        margin-bottom: 4rem;
    }
    </style>

    <div class="custom-title">STRESFORMANCE <br> TRACKER</div>
""", unsafe_allow_html=True)

def stress_assessment():
    """Premium stress assessment page"""
    show_header()
    st.markdown("""
    <h2 style="display: flex; align-items: center; gap: 0.5rem;">
        <lottie-player 
            src="https://assets1.lottiefiles.com/packages/lf20_gn0tojcq.json" 
            background="transparent" 
            speed="1" 
            style="width: 40px; height: 40px;"
            autoplay>
        </lottie-player>
        Your Stress Measure
    </h2>
    <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
        Rate how often you've experienced these feelings in the past month:
    </p>
    """, unsafe_allow_html=True)
    
    for i, question in enumerate(STRESS_QUESTIONS):
        st.session_state.stress_answers[i] = st.radio(
            question, 
            OPTIONS,
            key=f"stress_{i}",
            index=None,
            help="Select how frequently you've experienced this feeling"
        )
    
    if st.button("🚀 Continue to Performance Assessment", type="primary"):
        if None in st.session_state.stress_answers:
            st.warning("⚠️ Please answer all questions to proceed")
        else:
            st.session_state.page = 2
            st.rerun()

def performance_assessment():
    """Premium performance assessment page"""
    show_header()
    st.markdown("""
    <h2 style="display: flex; align-items: center; gap: 0.5rem;">
        <lottie-player 
            src="https://assets1.lottiefiles.com/packages/lf20_1a8dx7tj.json" 
            background="transparent" 
            speed="1" 
            style="width: 40px; height: 40px;"
            autoplay>
        </lottie-player>
        Your Performance Measure
    </h2>
    <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
        Rate how often these performance issues occurred in the past month:
    </p>
    """, unsafe_allow_html=True)
    
    for i, question in enumerate(PERFORMANCE_QUESTIONS):
        st.session_state.perf_answers[i] = st.radio(
            question,
            OPTIONS,
            key=f"perf_{i}",
            index=None,
            help="Select how frequently this performance issue occurred"
        )
    
    col1, col2 = st.columns([1, 2])
    col1.button("🔙 Back", on_click=lambda: st.session_state.update(page=1))
    
    if col2.button("📊 View My Results", type="primary"):
        if None in st.session_state.perf_answers:
            st.warning("⚠️ Please answer all questions to see your results")
        else:
            st.session_state.page = 3
            st.rerun()

def show_results():
    """Premium results dashboard"""
    trigger_confetti()
    show_header()
    
    # Process stress results
    stress_scores = [OPTION_SCORES[ans] for ans in st.session_state.stress_answers]
    stress_mean = calculate_mean(stress_scores)
    stress_class = classify_stress_level(stress_mean)
    
    # Process performance results
    perf_scores = [OPTION_SCORES[ans] for ans in st.session_state.perf_answers]
    perf_mean = calculate_mean(perf_scores)
    perf_class = classify_performance_level(perf_mean)
    
    # Results header with celebration
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2>Your Assessment Results</h2>
        <lottie-player 
            src="https://assets1.lottiefiles.com/packages/lf20_olc8tpeq.json" 
            background="transparent" 
            speed="1" 
            style="width: 200px; height: 200px; margin: -2rem auto;"
            autoplay>
        </lottie-player>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(10, 10, 30, 0.7); border-radius: 16px; padding: 1.5rem; 
                    border-left: 4px solid #EEDD62; margin-bottom: 2rem;">
            <h3 style="color: #EEDD62; display: flex; align-items: center; gap: 0.5rem;">
                🧠 Stress Analysis
            </h3>
            <div style="font-size: 1.2rem; margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Level:</span>
                    <span style="font-weight: 600;">{stress_class.split(' - ')[0]}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Score:</span>
                    <span style="font-weight: 600;">{stress_mean:.2f}/5.00</span>
                </div>
            </div>
            <p style="color: #00CED1; font-style: italic;">{stress_class.split(' - ')[1]}</p>
        </div>
        """, unsafe_allow_html=True)
        plot_gauge(stress_mean, [1, 5], "🧠 Stress Meter", "#8A2BE2")
    
    with col2:
        st.markdown(f"""
        <div style="background: rgba(10, 10, 30, 0.7); border-radius: 16px; padding: 1.5rem; 
                    border-left: 4px solid #00CED1; margin-bottom: 2rem;">
            <h3 style="color: #00CED1; display: flex; align-items: center; gap: 0.5rem;">
                💼 Performance Analysis
            </h3>
            <div style="font-size: 1.2rem; margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Level:</span>
                    <span style="font-weight: 600;">{perf_class.split(' - ')[0]}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Score:</span>
                    <span style="font-weight: 600;">{perf_mean:.2f}/5.00</span>
                </div>
            </div>
            <p style="color: #8A2BE2; font-style: italic;">{perf_class.split(' - ')[1]}</p>
        </div>
        """, unsafe_allow_html=True)
        plot_gauge(perf_mean, [1, 5], "💼 Performance Meter", "#00CED1")
    
    # Recommendations section
    st.markdown("""
    <div style="background: rgba(138, 43, 226, 0.1); border-radius: 16px; padding: 1.5rem; 
                border: 1px solid rgba(0, 206, 209, 0.3); margin-top: 2rem;">
        <h3 style="color: #FFD700; display: flex; align-items: center; gap: 0.5rem;">
            💎 Personalized Recommendations
        </h3>
        <div style="display: flex; align-items: center; gap: 1rem; margin: 1rem 0;">
            <lottie-player 
                src="https://assets1.lottiefiles.com/packages/lf20_7c8hosjy.json" 
                background="transparent" 
                speed="1" 
                style="width: 80px; height: 80px;"
                autoplay>
            </lottie-player>
            <div>
                <p style="font-size: 1.1rem;">Based on your assessment, we recommend:</p>
                <ul style="margin-top: 0.5rem;">
                    <li>🧘‍♂️ Daily mindfulness exercises</li>
                    <li>⏱️ Time management strategies</li>
                    <li>💤 Improved sleep hygiene</li>
                    <li>📅 Regular breaks during work</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Final action buttons
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;">
        <button style="
            background: linear-gradient(135deg, #8A2BE2, #4B0082);
            color: black;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 0 15px rgba(138, 43, 226, 0.7)'" 
        onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none'">
            📩 Download Full Report
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    st.button("🔄 Start New Assessment", 
              on_click=lambda: (
                  st.session_state.clear(),
                  st.session_state.update(page=1),
                  st.rerun()
              ),
              type="primary")

def plot_gauge(value: float, range: List[float], title: str, color: str):
    """Create premium gauge chart with animations"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': title,
            'font': {'size': 12, 'family': "Poppins", 'color': color}
        },
        gauge={
            'axis': {
                'range': range,
                'tickwidth': 1,
                'tickcolor': 'black',
                'tickfont': {'color': 'black'}
            },
            'bar': {'color': color},
            'bgcolor': 'rgba(10, 10, 30, 0.3)',
            'borderwidth': 2,
            'bordercolor': 'rgba(255, 255, 255, 0.2)',
            'steps': [
                {'range': [1, 2.5], 'color': 'rgba(0, 206, 209, 0.5)'},
                {'range': [2.5, 3.5], 'color': 'rgba(255, 215, 0, 0.5)'},
                {'range': [3.5, 5], 'color': 'rgba(138, 43, 226, 0.5)'}
            ],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
    title={
        'text': "STRESFORMANCE TRACKER",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20},
        'yanchor': 'top'
    },
    margin=dict(t=60)  # Add top margin for title
)

# ========== MAIN APP ==========
def main():
    """Premium application flow"""
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
