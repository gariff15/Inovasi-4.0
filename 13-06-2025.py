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
            'font': {'size': 16, 'family': "Poppins", 'color': color}
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
        'font': {'size': 24},
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
