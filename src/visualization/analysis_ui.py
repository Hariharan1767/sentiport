
import streamlit as st
import pandas as pd

def apply_custom_theme():
    """
    Applies Matrix Green and Midnight Black custom CSS theme.
    """
    st.markdown("""
    <style>
    /* Matrix Green & Midnight Black Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0e0f 0%, #000000 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        font-family: 'Courier New', monospace;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00ff41 !important;
        font-size: 2rem !important;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #66ff99 !important;
    }
    
    /* Cards/Containers */
    .factor-card {
        background: rgba(0, 20, 15, 0.8);
        border: 2px solid #00ff41;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
    }
    
    .invest-decision {
        background: linear-gradient(135deg, #003300 0%, #001a00 100%);
        border: 3px solid #00ff41;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.5);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 30px rgba(0, 255, 65, 0.5); }
        50% { box-shadow: 0 0 50px rgba(0, 255, 65, 0.8); }
    }
    
    .avoid-decision {
        background: linear-gradient(135deg, #1a0000 0%, #0d0000 100%);
        border: 3px solid #ff4444;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(255, 68, 68, 0.5);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background-color: #00ff41;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #004d00 0%, #003300 100%);
        color: #00ff41;
        border: 2px solid #00ff41;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: #00ff41;
        color: #000000;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.8);
    }
    
    /* Text */
    p, li, span {
        color: #c0c0c0 !important;
    }
    
    .factor-description {
        color: #99ff99 !important;
        font-style: italic;
        margin: 10px 0;
    }
    
    .score-text {
        color: #00ff41 !important;
        font-weight: bold;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def render_factor_card(factor_name, result, description):
    """
    Renders a single factor analysis card.
    """
    score = result['score']
    max_score = result['max_score']
    details = result.get('details', [])
    
    percentage = (score / max_score * 100) if max_score > 0 else 0
    
    st.markdown(f"""
    <div class="factor-card">
        <h3>{factor_name}</h3>
        <p class="factor-description">{description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(percentage / 100)
    with col2:
        st.markdown(f'<p class="score-text">{score:.1f}/{max_score}</p>', unsafe_allow_html=True)
    
    if details:
        with st.expander("📋 Details"):
            for detail in details:
                st.markdown(f"• {detail}")
    
def render_decision(prediction):
    """
    Renders the investment decision with visual prominence.
    """
    decision = prediction['decision']
    confidence = prediction['confidence_score']
    
    if decision == "INVEST":
        css_class = "invest-decision"
        emoji = "🚀"
        text_color = "#00ff41"
    else:
        css_class = "avoid-decision"
        emoji = "⚠️"
        text_color = "#ff4444"
    
    st.markdown(f"""
    <div class="{css_class}">
        <h1 style="color: {text_color}; margin: 0;">{emoji} {decision} {emoji}</h1>
        <p style="color: {text_color}; font-size: 1.5rem; margin-top: 10px;">
            Confidence: {confidence:.1%}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_stock_analysis_page(orchestrator):
    """
    Main page for 9-factor stock analysis.
    """
    apply_custom_theme()
    
    st.markdown("<h1>🔍 Deep Stock Analysis (9-Factor Model)</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p>Comprehensive investment analysis based on Fundamentals, Valuation, Business Model, 
    Management, Industry Position, Technical Indicators, Risk Factors, Macro Environment, 
    and Growth Potential.</p>
    """, unsafe_allow_html=True)
    
    # Input
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker = st.text_input("Enter Stock Ticker", "AAPL", key="ticker_input").upper()
    with col2:
        st.write("")
        st.write("")
        analyze_btn = st.button("🔎 Analyze", use_container_width=True)
    
    if analyze_btn or st.session_state.get('last_analyzed'):
        if analyze_btn:
            st.session_state['last_analyzed'] = ticker
        
        ticker_to_analyze = st.session_state['last_analyzed']
        
        with st.spinner(f"🤖 Analyzing {ticker_to_analyze}..."):
            result = orchestrator.analyze_stock(ticker_to_analyze)
        
        if 'error' in result:
            st.error(result['error'])
            return
        
        # Company Info Header
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Company", result['company_name'])
        with col2:
            st.metric("Sector", result['sector'])
        with col3:
            st.metric("Price", f"${result['current_price']:.2f}" if isinstance(result['current_price'], (int, float)) else "N/A")
        with col4:
            mkt_cap = result['market_cap']
            if isinstance(mkt_cap, (int, float)):
                st.metric("Market Cap", f"${mkt_cap / 1e9:.1f}B")
            else:
                st.metric("Market Cap", "N/A")
        
        st.markdown("---")
        
        # Decision First (Most Important)
        render_decision(result['prediction'])
        
        st.markdown("---")
        st.markdown("<h2>📊 Factor Analysis Breakdown</h2>", unsafe_allow_html=True)
        
        # Render each factor
        analysis = result['analysis']
        descriptions = result['factor_descriptions']
        
        # Group factors logically
        st.markdown("### 💼 Business Health")
        render_factor_card(
            descriptions['fundamental']['name'],
            analysis['fundamental'],
            descriptions['fundamental']['description']
        )
        
        st.markdown("### 💰 Financial Metrics")
        col1, col2 = st.columns(2)
        with col1:
            render_factor_card(
                descriptions['valuation']['name'],
                analysis['valuation'],
                descriptions['valuation']['description']
            )
        with col2:
            render_factor_card(
                descriptions['growth']['name'],
                analysis['growth'],
                descriptions['growth']['description']
            )
        
        st.markdown("### 🏢 Qualitative Factors")
        col1, col2 = st.columns(2)
        with col1:
            render_factor_card(
                descriptions['business']['name'],
                analysis['business'],
                descriptions['business']['description']
            )
        with col2:
            render_factor_card(
                descriptions['management']['name'],
                analysis['management'],
                descriptions['management']['description']
            )
        
        st.markdown("### 📈 Market Analysis")
        col1, col2 = st.columns(2)
        with col1:
            render_factor_card(
                descriptions['technical']['name'],
                analysis['technical'],
                descriptions['technical']['description']
            )
        with col2:
            render_factor_card(
                descriptions['risk']['name'],
                analysis['risk'],
                descriptions['risk']['description']
            )
        
        # Summary Table
        st.markdown("---")
        st.markdown("<h2>📋 Score Summary</h2>", unsafe_allow_html=True)
        
        summary_data = []
        for key, factor_info in descriptions.items():
            if key in analysis:
                summary_data.append({
                    'Factor': factor_info['name'],
                    'Score': f"{analysis[key]['score']:.1f}",
                    'Max': f"{analysis[key]['max_score']:.1f}",
                    'Percentage': f"{(analysis[key]['score'] / analysis[key]['max_score'] * 100) if analysis[key]['max_score'] > 0 else 0:.0f}%"
                })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
