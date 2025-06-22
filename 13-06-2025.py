def show_results():
    trigger_confetti()
    # Calculate means and classify levels
    stress_scores = [OPTION_SCORES[ans] for ans in st.session_state.stress_answers]
    stress_mean = calculate_mean(stress_scores)
    stress_level = classify_stress_level(stress_mean)
    
    perf_scores = [OPTION_SCORES[ans] for ans in st.session_state.perf_answers]
    perf_mean = calculate_mean(perf_scores)
    perf_level = classify_performance_level(perf_mean)

    # Normalize classification strings to exact keys used in pairing_map
    stress_level = stress_level.strip().title()
    perf_level = perf_level.strip().title()

    # 18-category pairing dictionary mapping (stress_level, perf_level) to recommendation
    pairing_map = {
        ("Very Low", "Very Low"): "NEEDS TRAINING",
        ("Very Low", "Low"): "NEEDS TRAINING",
        ("Very Low", "Moderate"): "NEEDS TRAINING",
        ("Very Low", "High"): "GOOD",
        ("Very Low", "Very High"): "EXCELLENT",
        ("Low", "Very Low"): "NEEDS TRAINING",
        ("Low", "Low"): "NEEDS TRAINING",
        ("Low", "Moderate"): "NEEDS TRAINING",
        ("Low", "High"): "GOOD",
        ("Low", "Very High"): "EXCELLENT",
        ("Moderate", "Very Low"): "NEEDS MONITORING AND TRAINING",
        ("Moderate", "Low"): "NEEDS MONITORING AND TRAINING",
        ("Moderate", "Moderate"): "NEEDS MONITORING AND TRAINING",
        ("High", "Very High"): "EXCELLENT BUT NEEDS COUNSELING",
        ("Very High", "Very Low"): "NEEDS COUNSELING AND TRAINING",
        ("Very High", "Low"): "NEEDS COUNSELING AND TRAINING",
        ("Very High", "Moderate"): "NEEDS COUNSELING AND TRAINING",
        ("Very High", "High"): "GOOD BUT NEEDS COUNSELING",
    }

    employer_action = pairing_map.get((stress_level, perf_level), "No recommendation available")

    # Display results header and animations
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

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="background: #f7f3ff; border-radius: 18px; padding: 1.5rem 1.2rem;
                    margin-bottom: 2rem; box-shadow: 0 3px 18px rgba(138, 43, 226, 0.13);
                    border-left: 5px solid #8A2BE2;">
            <h3 style="color: #8A2BE2;">🧠 Stress Analysis</h3>
            <div style="font-size: 1.2rem; margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Level:</span><span style="font-weight: 600;">{stress_level}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Score:</span><span style="font-weight: 600;">{stress_mean:.2f}/5.00</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        plot_dynamic_gauge(stress_mean, "🧠 Stress Meter", is_stress=True)

    with col2:
        st.markdown(f"""
        <div style="background: #fffbe5; border-radius: 18px; padding: 1.5rem 1.2rem;
                    margin-bottom: 2rem; box-shadow: 0 3px 18px rgba(255, 215, 0, 0.13);
                    border-left: 5px solid #FFD700;">
            <h3 style="color: #FFD700;">💼 Performance Analysis</h3>
            <div style="font-size: 1.2rem; margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Level:</span><span style="font-weight: 600;">{perf_level}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Score:</span><span style="font-weight: 600;">{perf_mean:.2f}/5.00</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        plot_dynamic_gauge(perf_mean, "💼 Performance Meter", is_stress=False)

    # Show Employer Action below results
    st.markdown(f"""
    <div style="background: #fffbe5; border-radius: 16px; padding: 1.2rem 1rem; margin: 1.5rem 0;
                border-left: 5px solid #FFD700; font-size: 1.18rem;">
        <b>Employer Action:</b> {employer_action}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col3, col4 = st.columns([1,1])
    with col3:
        if st.button("⬅️ Back to Performance Questions", key="back2"):
            st.session_state.page = 2
            st.experimental_rerun()
    with col4:
        if st.button("🔄 Restart", key="restart"):
            for k in ["stress_answers", "perf_answers"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state.page = 1
            st.experimental_rerun()

