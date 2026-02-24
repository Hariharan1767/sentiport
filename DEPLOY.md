# Deployment Guide

This guide covers how to deploy both the **SentiPort Main Application** and the **Research-Grade Stock Prediction System**.

## 1. Research-Grade Stock Predictor (Streamlit)

This is the interactive research dashboard built with Streamlit.

### Local Setup
1. **Navigate to the directory**:
   ```powershell
   cd research_stock_predictor
   ```

2. **Create a Virtual Environment**:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the `research_stock_predictor/` directory:
   ```env
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   FINNHUB_API_KEY=your_finnhub_key
   ```
   *Note: You can also enter these keys directly in the app sidebar.*

5. **Run the App**:
   ```powershell
   streamlit run app/main.py
   ```

---

## 2. SentiPort Main Application (Flask + React)

The core analysis application with a React frontend and Flask backend.

### Local Setup
1. **Backend**:
   ```powershell
   # Activation if using existing venv
   .venv\Scripts\activate
   python api_server.py
   ```

2. **Frontend**:
   ```powershell
   npm install
   npm run dev
   ```

---

## 3. Deployment via Docker

To deploy the entire environment (including the main app) in a containerized manner:

1. **Build the Image**:
   ```powershell
   docker build -t sentiport .
   ```

2. **Run the Container**:
   ```powershell
   docker run -p 5000:5000 -p 5173:5173 sentiport
   ```

---

## 🚀 Quick Launch (Windows)
I've included a `launch_research.bat` in the root directory for one-click startup of the research dashboard.
