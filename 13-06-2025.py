import streamlit as st
from streamlit.components.v1 import html

# --- Inject Lottie player and Confetti JS ---
st.components.v1.html("""
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<script>
function fireConfetti() {
    var duration = 2 * 1000;
    var animationEnd = Date.now() + duration;
    var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 1000 };
    function randomInRange(min, max) { return Math.random() * (max - min) + min; }
    var interval = setInterval(function() {
        var timeLeft = animationEnd - Date.now();
        if (timeLeft <= 0) { return clearInterval(interval); }
        var particleCount = 50 * (timeLeft / duration);
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.2, 0.8), y: Math.random() - 0.2 } }));
    }, 250);
}
</script>
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
""", height=0)

# --- CSS for game-like look ---
st.markdown("""
    <style>
    .giftbox-row {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 60px;
        margin-top: 2em;
        margin-bottom: 2em;
    }
    .giftbox-game {
        background: rgba(255,255,255,0.92);
        border-radius: 16px;
        padding: 1.5em 1em 1em 1em;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        text-align: center;
        width: 330px;
        min-height: 420px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        transition: all 0.5s ease;
    }
    .giftbox-game h3 {
        margin-bottom: 0.3em;
    }
    .open-animation {
        margin-top: -25px;
        margin-bottom: 0.5em;
        text-align: center;
    }
    .slot-label {
        font-size: 1.2em;
        font-weight: bold;
        color: #4f8bf9;
        margin-bottom: 0.7em;
    }
    .game-btn {
        margin-top: 1.3em;
        font-size: 1.1em !important;
        font-weight: bold !important;
        width: 85%;
        border-radius: 10px !important;
        background: linear-gradient(90deg,#ffb347,#ffcc33);
        color: #333 !important;
        border: none;
        box-shadow: 0 2px 8px rgba(255,200,0,0.15);
        transition: background 0.2s;
    }
    .game-btn:active {
        background: linear-gradient(90deg,#ffcc33,#ffb347);
    }
    </style>
""", unsafe_allow_html=True)

# --- Questions and logic ---
stress_questions = [
    "1. In the last 1-4 weeks, I found it hard to wind down.",
    "2. In the last 1-4 weeks, I tended to over-react to situations.",
    "3. In the last 1-4 weeks, I felt restless.",
    "4. In the last 1-4 weeks, I felt easily agitated.",
    "5. In the last 1-4 weeks, I felt difficult to relax."
]
performance_questions = [
    "6. During the past 1-4 weeks, how often was your performance lower than most workers at your workplace?",
    "7. During the past 1-4 weeks, how often did you do no work at times when you were supposed to be working?",
    "8. During the past 1-4 weeks, how often did you find yourself not working carefully as you should?",
    "9. During the past 1-4 weeks, how often was the quality of your work lower than it should be?",
    "10. During the past 1-4 weeks, how often do you not fully concentrate on your work?",
    "11. During the past 1-4 weeks, how often did health problems limit the kind or amount of work you could do?"
]
options = ["Very Rare", "Rare", "Moderate", "Frequent", "Very Frequent"]

def option_to_score(option):
    return {"Very Rare":1, "Rare":2, "Moderate":3, "Frequent":4, "Very Frequent":5}[option]

def classify_stress_level(mean):
    if mean < 1.5: return "Very Low"
    elif mean < 2: return "Low"
    elif mean < 3: return "Moderate"
    elif mean < 4: return "High"
    else: return "Very High"

def classify_performance_level(mean):
    if mean < 1.5: return "Very High"
    elif mean < 2: return "High"
    elif mean < 3: return "Moderate"
    elif mean < 4: return "Low"
    else: return "Very Low"

def trigger_confetti():
    html("<script>fireConfetti();</script>", height=0)

# --- State ---
if "page" not in st.session_state:
    st.session_state.page = 1
if "stress_answers" not in st.session_state:
    st.session_state.stress_answers = [None]*5
if "performance_answers" not in st.session_state:
    st.session_state.performance_answers = [None]*6
if "stress_opened" not in st.session_state:
    st.session_state.stress_opened = False
if "perf_opened" not in st.session_state:
    st.session_state.perf_opened = False

# --- PAGE 1 ---
if st.session_state.page == 1:
    st.title("Page 1: Stress Level Assessment")
    st.markdown("#### Please answer all stress questions below:")

    for i, q in enumerate(stress_questions):
        st.session_state.stress_answers[i] = st.radio(
            q, options, key=f"stress_q{i+1}", horizontal=True, index=None
        )
    if st.button("Next ➡️", type="primary"):
        if None in st.session_state.stress_answers:
            st.warning("Please answer all stress questions before proceeding.")
        else:
            st.session_state.page = 2
            st.rerun()

# --- PAGE 2 ---
elif st.session_state.page == 2:
    st.title("Page 2: Performance Level Assessment")
    st.markdown("#### Please answer all performance questions below:")

    for i, q in enumerate(performance_questions):
        st.session_state.performance_answers[i] = st.radio(
            q, options, key=f"perf_q{i+6}", horizontal=True, index=None
        )
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("⬅️ Back", key="back1"):
            st.session_state.page = 1
            st.rerun()
    with col2:
        if st.button("Next ➡️", key="next2", type="primary"):
            if None in st.session_state.performance_answers:
                st.warning("Please answer all performance questions before proceeding.")
            else:
                st.session_state.page = 3
                st.rerun()

# --- PAGE 3: Game-like Result Reveal ---
elif st.session_state.page == 3:
    st.title("🎰🎁 Results: Click to Reveal Your Surprise!")
    st.markdown("#### Click the box to reveal your result!")

    # Calculate results
    stress_scores = [option_to_score(a) for a in st.session_state.stress_answers]
    mean_stress = sum(stress_scores) / len(stress_scores)
    stress_class = classify_stress_level(mean_stress)

    perf_scores = [option_to_score(a) for a in st.session_state.performance_answers]
    mean_perf = sum(perf_scores) / len(perf_scores)
    perf_class = classify_performance_level(mean_perf)

    # Lottie Animations (use surprise/slot/gift box)
    giftbox_open = "https://lottie.host/1f6f3e5d-3e2d-4f5b-9e3d-4b5f3e5d3e2d/2h7l3j.json"
    slot_open = "https://lottie.host/294b684d-d6b4-4116-ab35-85ef566d4379/VkGHcqcMUI.json"

    # Layout for game-like boxes
    st.markdown('<div class="giftbox-row">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    # --- Stress Box ---
    with col1:
        st.markdown('<div class="giftbox-game">', unsafe_allow_html=True)
        st.markdown('<div class="slot-label">Stress Level</div>', unsafe_allow_html=True)
        if not st.session_state.stress_opened:
            html(f"""
            <div class="open-animation">
                <lottie-player src="{giftbox_open}" background="transparent" speed="1" style="width: 180px; height: 180px;" loop autoplay></lottie-player>
            </div>
            """, height=190)
            if st.button("🎁 Click to Reveal!", key="open_stress", help="Click to open the box and see your stress result!", use_container_width=True):
                st.session_state.stress_opened = True
                trigger_confetti()
                st.rerun()
        else:
            html(f"""
            <div class="open-animation
::contentReference[oaicite:12]{index=12}
             html(f"""
            <div class="open-animation">
                <lottie-player src="{giftbox_open}" background="transparent" speed="1" style="width: 180px; height: 180px;" autoplay></lottie-player>
            </div>
            """, height=200)
            st.subheader(f"Stress Level: {stress_class}")
            st.write(f"Mean Score: **{mean_stress:.2f}**")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Performance Box ---
    with col2:
        st.markdown('<div class="giftbox-game">', unsafe_allow_html=True)
        st.markdown('<div class="slot-label">Performance Level</div>', unsafe_allow_html=True)
        if not st.session_state.perf_opened:
            html(f"""
            <div class="open-animation">
                <lottie-player src="{slot_open}" background="transparent" speed="1" style="width: 180px; height: 180px;" loop autoplay></lottie-player>
            </div>
            """, height=190)
            if st.button("🎰 Click to Reveal!", key="open_perf", help="Click to open the slot and see your performance result!", use_container_width=True):
                st.session_state.perf_opened = True
                trigger_confetti()
                st.rerun()
        else:
            html(f"""
            <div class="open-animation">
                <lottie-player src="{slot_open}" background="transparent" speed="1" style="width: 180px; height: 180px;" autoplay></lottie-player>
            </div>
            """, height=200)
            st.subheader(f"Performance Level: {perf_class}")
            st.write(f"Mean Score: **{mean_perf:.2f}**")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Navigation Buttons ---
    col3, col4 = st.columns([1,1])
    with col3:
        if st.button("⬅️ Back to Questions", key="back2"):
            st.session_state.page = 2
            st.session_state.stress_opened = False
            st.session_state.perf_opened = False
            st.rerun()
    with col4:
        if st.button("🔄 Restart", key="restart"):
            for k in ["stress_answers", "performance_answers", "stress_opened", "perf_opened"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state.page = 1
            st.rerun()

