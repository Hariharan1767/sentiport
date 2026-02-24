import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from research_orchestrator import ResearchPipeline
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Multi-Modal Stock Prediction Research", layout="wide")

st.title("🧠 Multi-Modal Stock Prediction Research System")
st.markdown("""
This system evaluates the effectiveness of integrating **financial sentiment** (Qualitative) 
with **price history/technical indicators** (Quantitative) using a **Hybrid LSTM+Dense Deep Learning Architecture**.
""")

# Sidebar for Setup
with st.sidebar:
    st.header("⚙️ Configuration")
    av_api_key = st.text_input("Alpha Vantage API Key", value=os.getenv("ALPHA_VANTAGE_API_KEY", ""), type="password")
    fh_api_key = st.text_input("Finnhub API Key", value=os.getenv("FINNHUB_API_KEY", ""), type="password")
    
    ticker = st.text_input("Stock Ticker", value="AAPL")
    lookback = st.slider("Lookback Window (Days)", 7, 30, 14)
    run_button = st.button("🚀 Run Research Pipeline")

if run_button:
    if not av_api_key or not fh_api_key:
        st.error("Please provide both API keys in the sidebar.")
    else:
        with st.status("Initializing Research Pipeline...", expanded=True) as status:
            st.write("Fetching historical prices and indicators...")
            try:
                pipeline = ResearchPipeline(av_key=av_api_key, fh_key=fh_api_key)
                results = pipeline.run_experiment(ticker)
                
                status.update(label="Experiment Complete!", state="complete", expanded=False)
                
                # Metrics Display
                st.header(f"📊 Research Results: {ticker}")
                col1, col2, col3, col4 = st.columns(4)
                
                b = results['baseline']
                h = results['hybrid']
                
                col1.metric("Baseline RMSE", f"{b['rmse']:.4f}")
                col2.metric("Hybrid RMSE", f"{h['rmse']:.4f}", f"{((h['rmse']-b['rmse'])/b['rmse']):.1%}", delta_color="inverse")
                
                col3.metric("Baseline Dir. Accuracy", f"{b['directional_acc']:.2%}")
                col4.metric("Hybrid Dir. Accuracy", f"{h['directional_acc']:.2%}", f"{(h['directional_acc']-b['directional_acc']):.2%}")

                # Plots
                st.subheader("📈 Price vs Sentiment Interaction")
                df = results['data']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Close Price", yaxis="y1", line=dict(color="#00ff88")))
                fig.add_trace(go.Bar(x=df.index, y=df['daily_sentiment'], name="Sentiment Score", yaxis="y2", opacity=0.3, marker_color="#3b82f6"))
                
                fig.update_layout(
                    template="plotly_dark",
                    hovermode="x unified",
                    yaxis=dict(title="Stock Price ($)"),
                    yaxis2=dict(title="Sentiment Score (+1 to -1)", overlaying="y", side="right"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)

                # Statistical Interpretation
                st.subheader("📝 Statistical Interpretation")
                improvement = (h['directional_acc'] - b['directional_acc'])
                if improvement > 0:
                    st.success(f"Sentiment data **improved** directional accuracy by **{improvement:.2%}**.")
                else:
                    st.warning(f"Sentiment data **did not improve** directional accuracy in this specific window.")

            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
                st.info("Check if your Alpha Vantage key has reached its 5-calls/min limit.")

else:
    st.info("👈 Enter a ticker and run the experiment to see research findings.")

st.divider()
st.caption("Developed for Advanced Financial Deep Learning Research • Uses Only Free APIs")
