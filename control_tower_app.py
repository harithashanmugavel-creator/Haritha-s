"""
🛡️ OptiGuard AI - Marketing Operations Control Tower
=====================================================

AI Campaign Risk Intelligence Platform
Predicts campaign failures BEFORE launch.

NOT a dashboard. This is PREDICTIVE INTELLIGENCE.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import json
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from campaign_risk_predictor import CampaignRiskPredictor
from similar_campaign_finder import SimilarCampaignFinder

# Page configuration
st.set_page_config(
    page_title="OptiGuard AI - Control Tower",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise-grade CSS
st.markdown("""
<style>
    /* FORCE DARK THEME EVERYWHERE */
    .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
    header, .stApp > header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
        background-color: #1a1a2e !important;
    }
    
    /* Top header bar */
    [data-testid="stHeader"] {
        background: rgba(26, 26, 46, 0.95) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Deploy button and toolbar */
    [data-testid="stToolbar"] {
        background: transparent !important;
    }
    
    [data-testid="stToolbar"] button, [data-testid="stToolbar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Main container */
    .main .block-container {
        background: transparent !important;
    }
    
    /* SIDEBAR - Dark background and visible text */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1e1e2e 0%, #1a1a2e 100%) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(135deg, #1e1e2e 0%, #1a1a2e 100%) !important;
    }
    
    /* Sidebar ALL text - force white */
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #00d4ff !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #f472b6 !important;
    }
    
    /* Sidebar selectbox styling */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: #e2e8f0 !important;
    }
    
    /* Sidebar text area */
    [data-testid="stSidebar"] textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: #e2e8f0 !important;
    }
    
    /* GLOBAL TEXT VISIBILITY - Make all text white/visible */
    .stApp *, .main *, [data-testid="stAppViewContainer"] * {
        color: #e2e8f0 !important;
    }
    
    .stApp p, .stApp span, .stApp div, .stApp label, 
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #e2e8f0 !important;
    }
    
    /* Streamlit specific elements */
    .stMarkdown, .stMarkdown p, .stText, .stCaption {
        color: #e2e8f0 !important;
    }
    
    /* Tab labels */
    .stTabs [data-baseweb="tab-list"] button {
        color: #e2e8f0 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #00d4ff !important;
    }
    
    /* Selectbox and input labels */
    .stSelectbox label, .stTextArea label, .stTextInput label, .stNumberInput label {
        color: #00d4ff !important;
    }
    
    /* Metric labels */
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        color: #e2e8f0 !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff 0%, #7c3aed 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #94a3b8 !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin: 15px 0;
        color: #e2e8f0 !important;
    }
    
    .glass-card h2, .glass-card h3, .glass-card h4, .glass-card p, .glass-card li {
        color: #e2e8f0 !important;
    }
    
    /* Health Score Card */
    .health-score-card {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.3) 0%, rgba(0, 212, 255, 0.3) 100%);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        padding: 40px;
        text-align: center;
        margin: 20px 0;
    }
    
    .health-score {
        font-size: 5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .health-grade {
        font-size: 2rem;
        color: #00d4ff;
        margin-top: 10px;
    }
    
    /* Risk cards */
    .risk-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 10px 40px rgba(238, 90, 90, 0.3);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 10px 40px rgba(251, 140, 0, 0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 10px 40px rgba(67, 160, 71, 0.3);
    }
    
    /* Pipeline visualization */
    .pipeline-step {
        background: rgba(124, 58, 237, 0.2);
        border: 1px solid rgba(124, 58, 237, 0.5);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
        color: #e2e8f0 !important;
    }
    
    .pipeline-step div {
        color: #e2e8f0 !important;
    }
    
    .pipeline-arrow {
        color: #7c3aed;
        font-size: 1.5rem;
        text-align: center;
    }
    
    /* Factor breakdown */
    .factor-positive {
        background: linear-gradient(90deg, rgba(102, 187, 106, 0.2) 0%, transparent 100%);
        border-left: 4px solid #66bb6a;
        padding: 10px 15px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        color: #e2e8f0 !important;
    }
    
    .factor-negative {
        background: linear-gradient(90deg, rgba(255, 107, 107, 0.2) 0%, transparent 100%);
        border-left: 4px solid #ff6b6b;
        padding: 10px 15px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        color: #e2e8f0 !important;
    }
    
    .factor-positive div, .factor-negative div, .factor-positive span, .factor-negative span {
        color: #e2e8f0 !important;
    }
    
    /* AI Reasoning box */
    .ai-reasoning {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: #e2e8f0 !important;
    }
    
    .ai-reasoning h4, .ai-reasoning p {
        color: #e2e8f0 !important;
    }
    
    .ai-analyst {
        background: linear-gradient(135deg, rgba(244, 114, 182, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        border: 1px solid rgba(244, 114, 182, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: #e2e8f0 !important;
    }
    
    .ai-analyst h4, .ai-analyst p {
        color: #e2e8f0 !important;
    }
    
    /* Live signal */
    .live-signal {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #ff6b6b;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
        margin-right: 8px;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
    }
    
    /* Before/After comparison */
    .comparison-before {
        background: rgba(255, 107, 107, 0.2);
        border: 1px solid #ff6b6b;
        border-radius: 10px;
        padding: 15px;
        color: #e2e8f0 !important;
    }
    
    .comparison-before h5, .comparison-before p {
        color: #e2e8f0 !important;
    }
    
    .comparison-after {
        background: rgba(102, 187, 106, 0.2);
        border: 1px solid #66bb6a;
        border-radius: 10px;
        padding: 15px;
        color: #e2e8f0 !important;
    }
    
    .comparison-after h5, .comparison-after p {
        color: #e2e8f0 !important;
    }
    
    /* Executive card */
    .executive-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        color: #e2e8f0 !important;
    }
    
    .executive-card h2, .executive-card h3, .executive-card h4, .executive-card p, .executive-card div {
        color: #e2e8f0 !important;
    }
    
    .executive-card hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Evidence badge */
    .evidence-badge {
        background: rgba(0, 212, 255, 0.2);
        border: 1px solid rgba(0, 212, 255, 0.5);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.85rem;
        display: inline-block;
        margin: 5px;
        color: #e2e8f0 !important;
    }
    
    /* Health score card text */
    .health-score-card div {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_predictor():
    """Load and cache the Campaign Risk Predictor."""
    return CampaignRiskPredictor()


@st.cache_resource
def load_finder():
    """Load and cache the Similar Campaign Finder."""
    finder = SimilarCampaignFinder()
    finder.build_index()
    return finder


def render_contextual_chat(section_key: str, section_title: str, context: dict, predictor):
    """Render an inline contextual chat for a specific section."""
    chat_state_key = f"chat_{section_key}"
    
    if chat_state_key not in st.session_state:
        st.session_state[chat_state_key] = []
    
    with st.expander(f"💬 Ask AI about {section_title}", expanded=False):
        # Render past messages
        for msg in st.session_state[chat_state_key]:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
        
        user_input = st.chat_input(
            f"Ask about {section_title}...",
            key=f"input_{section_key}"
        )
        
        if user_input:
            st.session_state[chat_state_key].append({'role': 'user', 'content': user_input})
            with st.chat_message('user'):
                st.markdown(user_input)
            
            with st.chat_message('assistant'):
                with st.spinner("Thinking..."):
                    response = generate_chat_response(user_input, section_title, context, predictor)
                    st.markdown(response)
            
            st.session_state[chat_state_key].append({'role': 'assistant', 'content': response})


def generate_chat_response(question: str, section: str, context: dict, predictor) -> str:
    """Generate AI response using GPT with section context."""
    if predictor.llm_client is None:
        return "⚠️ AI chat is unavailable - LLM client not configured."
    
    context_str = json.dumps(context, indent=2, default=str)[:3000]
    
    system_prompt = f"""You are an expert marketing risk analyst helping a user understand their campaign analysis.

You are answering questions about the "{section}" section of their campaign risk report.

CONTEXT DATA FOR THIS SECTION:
{context_str}

Guidelines:
- Be concise (2-4 sentences typically)
- Reference specific numbers from the context
- Explain the "why" behind recommendations
- Use simple language, avoid jargon
- For scenario questions, explain likely impact
- Use bullet points for lists
- Be direct and actionable"""
    
    try:
        response = predictor.llm_client.chat.completions.create(
            model=predictor.llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.4,
            max_completion_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"


def render_ai_pipeline():
    """Render the AI Decision Pipeline visualization."""
    st.markdown("### 🔄 AI Decision Pipeline")
    
    pipeline_steps = [
        ("📝", "Campaign Brief Analysis", "Understanding your campaign intent"),
        ("🔍", "Embedding Similarity Search", "Finding similar historical campaigns"),
        ("📊", "Historical Pattern Retrieval", "Analyzing 10,000+ campaign records"),
        ("⚡", "Fatigue Pattern Analysis", "Detecting audience saturation signals"),
        ("🎯", "Risk Prediction Engine", "Calculating multi-factor risk scores"),
        ("🧠", "GPT Reasoning Engine", "Generating AI insights & recommendations")
    ]
    
    cols = st.columns(len(pipeline_steps))
    for i, (icon, title, desc) in enumerate(pipeline_steps):
        with cols[i]:
            st.markdown(f"""
            <div class="pipeline-step">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="font-weight: bold; margin: 10px 0;">{title}</div>
                <div style="font-size: 0.8rem; color: #94a3b8;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if i < len(pipeline_steps) - 1:
                st.markdown('<div class="pipeline-arrow">→</div>', unsafe_allow_html=True)


def render_health_score(health: dict):
    """Render the Campaign Health Score prominently."""
    score = health['overall_score']
    grade = health['grade']
    
    # Color based on score
    if score >= 80:
        color = "#66bb6a"
    elif score >= 65:
        color = "#00d4ff"
    elif score >= 50:
        color = "#ffa726"
    else:
        color = "#ff6b6b"
    
    st.markdown(f"""
    <div class="health-score-card">
        <div style="color: #94a3b8; font-size: 1rem; text-transform: uppercase; letter-spacing: 2px;">Campaign Health Score</div>
        <div class="health-score" style="background: linear-gradient(90deg, {color}, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{score}</div>
        <div style="font-size: 1.5rem;">/100</div>
        <div class="health-grade">Grade: {grade}</div>
        <div style="color: #94a3b8; margin-top: 15px;">{health['interpretation']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Subscores
    st.markdown("#### Health Subscores")
    sub_cols = st.columns(4)
    subscores = health['subscores']
    
    labels = [
        ("💰", "ROI Health", subscores['roi_health']),
        ("🤝", "Trust Health", subscores['trust_health']),
        ("⚡", "Fatigue Health", subscores['fatigue_health']),
        ("✅", "Compliance Health", subscores['compliance_health'])
    ]
    
    for i, (icon, label, score) in enumerate(labels):
        with sub_cols[i]:
            color = "#66bb6a" if score >= 70 else ("#ffa726" if score >= 50 else "#ff6b6b")
            st.markdown(f"""
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="font-size: 2rem; font-weight: bold; color: {color};">{score}</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)


def render_risk_factors(factors: list):
    """Render risk factor breakdown with impact percentages."""
    st.markdown("### 📊 Top Contributing Factors")
    st.caption(f"Analysis based on {len(factors)} risk factors identified from historical campaign patterns")
    
    if not factors:
        st.info("No significant risk factors identified for this campaign configuration.")
        return
    
    for factor in factors[:6]:
        impact_val = factor['impact_value']
        is_positive = impact_val < 0
        
        css_class = "factor-positive" if is_positive else "factor-negative"
        icon = "✅" if is_positive else "⚠️"
        
        st.markdown(f"""
        <div class="{css_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>{icon} <strong>{factor['factor']}</strong></span>
                <span style="font-size: 1.2rem; font-weight: bold; color: {'#66bb6a' if is_positive else '#ff6b6b'};">
                    {factor['impact']}
                </span>
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 5px;">
                📈 {factor['evidence']}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_similar_campaigns(finder, query: str):
    """Render similar campaigns from semantic search."""
    st.markdown("### 🔍 Similar Historical Campaigns")
    st.caption("Found using semantic embedding search across 10,000+ campaign records")
    
    results = finder.search(query, top_k=3)
    
    if results.empty:
        st.info("No similar campaigns found in historical data.")
        return
    
    st.success(f"✅ Found {len(results)} similar campaigns matching your campaign idea")
    
    for _, row in results.iterrows():
        roi = row.get('ROI', row.get('roi', 0))
        roi_color = "#66bb6a" if roi > 400 else ("#ffa726" if roi > 200 else "#ff6b6b")
        similarity = row.get('Similarity_Score', row.get('similarity_score', 0))
        campaign_name = row.get('Campaign', row.get('campaign_name', 'Unknown'))
        product = row.get('Product', row.get('product', 'N/A'))
        audience = row.get('Audience', row.get('audience_segment', 'N/A'))
        feedback = row.get('Feedback', row.get('feedback', 'No feedback available'))
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 1.1rem;">{campaign_name}</strong>
                    <div style="color: #94a3b8; font-size: 0.85rem;">{product} | {audience}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.5rem; font-weight: bold; color: {roi_color};">ROI: {roi:.0f}</div>
                    <div style="color: #00d4ff;">Similarity: {similarity:.0f}%</div>
                </div>
            </div>
            <div style="margin-top: 10px; padding: 10px; background: rgba(0,0,0,0.2); border-radius: 8px;">
                <strong>Feedback:</strong> {feedback}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_historical_baseline(historical: dict):
    """Step 1: Show historical complaint % + 4 risk metrics from similar past campaigns."""
    st.markdown("### 📊 Historical Analysis: Similar Past Campaigns")
    st.caption(f"Analyzed {historical.get('similar_count', 0)} similar campaigns matching your product + audience")
    
    # Top KPI row
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        st.markdown(f"""
        <div style="padding: 14px; background: rgba(255,107,107,0.1); border-radius: 10px; border-left: 4px solid #ff6b6b;">
            <div style="color: #94a3b8; font-size: 0.78rem; font-weight: 600;">COMPLAINTS RAISED</div>
            <div style="color: #ff6b6b; font-size: 1.8rem; font-weight: 700;">{historical.get('complaints_pct', 0):.1f}%</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">of feedback was negative</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_cols[1]:
        st.markdown(f"""
        <div style="padding: 14px; background: rgba(244,114,182,0.1); border-radius: 10px; border-left: 4px solid #f472b6;">
            <div style="color: #94a3b8; font-size: 0.78rem; font-weight: 600;">CANCELLED / PAUSED</div>
            <div style="color: #f472b6; font-size: 1.8rem; font-weight: 700;">{historical.get('cancelled_pct', 0):.1f}%</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">of similar campaigns shut down</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_cols[2]:
        st.markdown(f"""
        <div style="padding: 14px; background: rgba(0,212,255,0.1); border-radius: 10px; border-left: 4px solid #00d4ff;">
            <div style="color: #94a3b8; font-size: 0.78rem; font-weight: 600;">AVG HISTORICAL ROI</div>
            <div style="color: #00d4ff; font-size: 1.8rem; font-weight: 700;">{historical.get('avg_roi', 0):.0f}</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">across {historical.get('similar_count', 0)} campaigns</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 4 Risk metric breakdown
    st.markdown("#### 🚦 Categorized Historical Risk")
    risk_cols = st.columns(4)
    risk_data = [
        ("Fatigue Risk", historical.get('fatigue_risk', 0), "#ff6b6b", "🥱"),
        ("Opt-Out Risk", historical.get('opt_out_risk', 0), "#f472b6", "🚪"),
        ("Complaint Risk", historical.get('complaint_risk', 0), "#a78bfa", "📢"),
        ("Trust Risk", historical.get('trust_risk', 0), "#facc15", "🛡️"),
    ]
    for col, (label, val, color, icon) in zip(risk_cols, risk_data):
        with col:
            st.markdown(f"""
            <div style="padding: 12px; background: rgba(255,255,255,0.04); border-radius: 8px; border-top: 3px solid {color}; text-align: center;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="color: #94a3b8; font-size: 0.72rem; font-weight: 600; margin-top: 4px;">{label.upper()}</div>
                <div style="color: {color}; font-size: 1.4rem; font-weight: 700; margin-top: 2px;">{val:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    sample_ids = historical.get('sample_campaign_ids', [])
    if sample_ids:
        st.caption(f"📁 Sample campaigns analyzed: {', '.join(sample_ids)}")
    
    st.markdown("---")


def render_predicted_reductions(deltas: dict, historical: dict):
    """Step 3: Show before → after with % reductions for the 4 risk metrics."""
    st.markdown("#### 📉 Predicted Improvements (After AI Optimization)")
    st.caption("Risk reductions vs. historical baseline from similar past campaigns")
    
    metrics = [
        ("Fatigue Risk", deltas['fatigue'], "#ff6b6b"),
        ("Opt-Out Risk", deltas['opt_out'], "#f472b6"),
        ("Complaint Risk", deltas['complaint'], "#a78bfa"),
        ("Trust Risk", deltas['trust'], "#facc15"),
    ]
    
    cols = st.columns(4)
    for col, (label, d, color) in zip(cols, metrics):
        delta_pct = d['delta_pct']
        delta_color = "#66bb6a" if delta_pct < 0 else "#ff6b6b"
        sign = "" if delta_pct < 0 else "+"
        with col:
            st.markdown(f"""
            <div style="padding: 14px; background: rgba(255,255,255,0.04); border-radius: 10px; border-left: 4px solid {color};">
                <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 600;">{label.upper()}</div>
                <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 6px;">
                    <span style="color: #ff6b6b; font-size: 0.95rem; text-decoration: line-through;">{d['before']:.1f}%</span>
                    <span style="color: #94a3b8;">→</span>
                    <span style="color: #66bb6a; font-size: 1.2rem; font-weight: 700;">{d['after']:.1f}%</span>
                </div>
                <div style="color: {delta_color}; font-size: 1.3rem; font-weight: 700; margin-top: 6px;">{sign}{delta_pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)


def render_optimization_exec_summary(summary: str):
    """Step 4: One-paragraph executive summary explaining the WHY."""
    st.markdown("#### 📋 Executive Summary")
    st.markdown(f"""
    <div class="glass-card" style="background: linear-gradient(135deg, rgba(102,187,106,0.12), rgba(0,212,255,0.08)); border-left: 4px solid #66bb6a;">
        <div style="display: flex; gap: 14px; align-items: flex-start;">
            <div style="font-size: 2rem;">🎯</div>
            <div style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.55;">{summary}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_problem_resolution(scenario: dict, resolutions: list):
    """Show how the AI optimization solves a known industry pain point + complaints."""
    st.markdown("---")
    st.markdown("### 🎯 Problem Statement Resolution")
    st.caption("How this AI optimization solves a real banking marketing pain point")
    
    confidence = scenario.get('match_confidence', 0)
    
    # Matched scenario header card
    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid #00d4ff;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: #00d4ff; font-size: 0.8rem; font-weight: 600; letter-spacing: 1px;">MATCHED INDUSTRY SCENARIO</div>
                <div style="font-size: 1.3rem; color: #e2e8f0; margin-top: 4px; font-weight: 700;">{scenario['name']}</div>
            </div>
            <div style="text-align: right;">
                <div style="color: #94a3b8; font-size: 0.75rem;">MATCH CONFIDENCE</div>
                <div style="font-size: 1.5rem; color: #66bb6a; font-weight: bold;">{confidence}%</div>
            </div>
        </div>
        <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);">
            <div style="color: #ff6b6b; font-size: 0.85rem; font-weight: 600;">⚠️ ORIGINAL INDUSTRY COMPLAINT:</div>
            <div style="color: #e2e8f0; font-size: 0.95rem; margin-top: 4px; font-style: italic;">"{scenario['real_problem']}"</div>
        </div>
        <div style="margin-top: 10px;">
            <div style="color: #f472b6; font-size: 0.85rem; font-weight: 600;">😣 OPERATIONAL PAIN MARKETING TEAMS FACE:</div>
            <div style="color: #e2e8f0; font-size: 0.95rem; margin-top: 4px;">{scenario['operational_pain']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Side-by-side: Old Pain → New AI Resolution
    st.markdown("#### 🔄 Pain → AI Resolution Mapping")
    
    for res in resolutions:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown(f"""
            <div class="factor-negative" style="height: 100%;">
                <div style="color: #ff6b6b; font-size: 0.75rem; font-weight: 700;">❌ BEFORE (Pain Point)</div>
                <div style="color: #e2e8f0; font-size: 0.92rem; margin-top: 6px;">{res['complaint']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="factor-positive" style="height: 100%;">
                <div style="color: #66bb6a; font-size: 0.75rem; font-weight: 700;">{res['icon']} NOW SOLVED BY AI</div>
                <div style="color: #e2e8f0; font-size: 0.92rem; margin-top: 6px;">{res['ai_fix']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # AI capabilities applied
    st.markdown("#### ✅ AI Capabilities Applied To Your Campaign")
    cap_cols = st.columns(2)
    for idx, cap in enumerate(scenario.get('ai_solution', [])):
        with cap_cols[idx % 2]:
            st.markdown(f"""
            <div style="padding: 10px 14px; background: rgba(102,187,106,0.1); border-left: 3px solid #66bb6a; border-radius: 6px; margin: 5px 0;">
                <div style="color: #e2e8f0; font-size: 0.9rem;">✓ {cap}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Complaint proof / references
    proofs = scenario.get('complaint_proof', [])
    if proofs:
        with st.expander("📚 Real-World Complaints & Industry Sources That Validated This Problem"):
            for p in proofs:
                st.markdown(f"- 🔗 [{p['label']}]({p['url']})")
    
    # Final verdict banner
    st.markdown(f"""
    <div class="glass-card" style="background: linear-gradient(135deg, rgba(102,187,106,0.15), rgba(0,212,255,0.1)); border: 1px solid #66bb6a; margin-top: 15px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 2rem;">🛡️</div>
            <div>
                <div style="color: #66bb6a; font-weight: 700; font-size: 1.05rem;">RESOLUTION DELIVERED</div>
                <div style="color: #e2e8f0; font-size: 0.92rem; margin-top: 4px;">
                    Your "<strong>{scenario['name']}</strong>" campaign has been optimized to directly prevent the historical complaints raised against this exact scenario. 
                    Risk caught <strong>before launch</strong> — not after customer escalations.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_optimization(optimization: dict):
    """Render the before/after optimization comparison."""
    st.markdown("### 🔧 AI Campaign Optimizer")
    st.caption("AI-powered recommendations to reduce risk")
    
    # Messaging optimization
    st.markdown("#### 📝 Messaging Optimization")
    msg = optimization.get('optimized_messaging', {})
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="comparison-before">
            <h5>❌ Before</h5>
            <p style="font-style: italic;">"{msg.get('before', 'Original messaging')}"</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="comparison-after">
            <h5>✅ After</h5>
            <p style="font-style: italic;">"{msg.get('after', 'Optimized messaging')}"</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info(f"💡 {msg.get('change_explanation', 'Optimization applied')}")
    
    # Before/After Metrics Comparison
    st.markdown("#### 📊 Predicted Improvements")
    
    comparison = optimization.get('before_after_comparison', [])
    if comparison:
        comp_df = pd.DataFrame(comparison)
        
        for _, row in comp_df.iterrows():
            improvement = row.get('improvement', 'N/A')
            is_improvement = '-' in str(improvement) or '+' in str(improvement) and row['metric'] == 'Expected ROI'
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; 
                        background: rgba(255,255,255,0.05); border-radius: 8px; margin: 5px 0;">
                <span><strong>{row['metric']}</strong></span>
                <span>
                    <span style="color: #ff6b6b;">{row['before']}</span>
                    →
                    <span style="color: #66bb6a;">{row['after']}</span>
                    <span style="color: {'#66bb6a' if is_improvement else '#ff6b6b'}; font-weight: bold; margin-left: 10px;">
                        {improvement}
                    </span>
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # Additional optimizations
    st.markdown("#### 📢 Channel Strategy")
    channel = optimization.get('optimized_channel_strategy', {})
    st.success(f"**Primary:** {channel.get('primary_channel', 'Email')} | **Secondary:** {channel.get('secondary_channel', 'WhatsApp')}")
    st.caption(channel.get('rationale', ''))
    
    st.markdown("#### ⏰ Timing Optimization")
    timing = optimization.get('optimized_timing', {})
    
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: grid; grid-template-columns: 1fr; gap: 12px;">
            <div style="padding: 12px; background: rgba(0,212,255,0.08); border-left: 3px solid #00d4ff; border-radius: 6px;">
                <div style="color: #00d4ff; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">🔁 FREQUENCY</div>
                <div style="color: #e2e8f0; font-size: 1rem;">{timing.get('frequency', '1/week')}</div>
            </div>
            <div style="padding: 12px; background: rgba(124,58,237,0.08); border-left: 3px solid #7c3aed; border-radius: 6px;">
                <div style="color: #a78bfa; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">🕓 BEST TIME</div>
                <div style="color: #e2e8f0; font-size: 1rem;">{timing.get('timing', 'Evening')}</div>
            </div>
            <div style="padding: 12px; background: rgba(244,114,182,0.08); border-left: 3px solid #f472b6; border-radius: 6px;">
                <div style="color: #f472b6; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">⏳ COOLDOWN</div>
                <div style="color: #e2e8f0; font-size: 1rem;">{timing.get('cooldown', '7 days')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary
    st.markdown(f"""
    <div class="glass-card">
        <h4>📋 Optimization Summary</h4>
        <p>{optimization.get('optimization_summary', 'Optimization complete.')}</p>
    </div>
    """, unsafe_allow_html=True)


def render_audience_playbook(playbook: dict, campaign_meta: dict):
    """Render the personalized audience intelligence playbook."""
    st.markdown("### 🎯 Audience Intelligence & Reach Playbook")
    st.caption("Personalized strategy based on YOUR historical campaign data")
    
    ideal = playbook.get('ideal_profile', {})
    comparison = playbook.get('comparison', {})
    exclusions = playbook.get('exclusions', [])
    patterns = playbook.get('winning_patterns', {})
    reach = playbook.get('reach_plan', {})
    
    # ============ ROI UPLIFT BANNER ============
    uplift = comparison.get('roi_uplift_potential', 0)
    uplift_pct = comparison.get('roi_uplift_percentage', 0)
    your_roi = comparison.get('your_combo_avg_roi', 0)
    target_roi = comparison.get('recommended_avg_roi', 0)
    
    uplift_color = "#66bb6a" if uplift > 0 else "#ff6b6b"
    uplift_icon = "📈" if uplift > 0 else "⚠️"
    
    # Format uplift text with both absolute and percentage
    if your_roi > 0:
        uplift_text = f"Uplift: +{uplift:.0f} ROI ({uplift_pct:+.1f}%)"
    else:
        uplift_text = f"Uplift: +{uplift:.0f} ROI"
    
    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid {uplift_color};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: #94a3b8; font-size: 0.85rem;">YOUR CURRENT COMBO</div>
                <div style="font-size: 1.4rem; color: #ff6b6b;">ROI {your_roi:.0f}</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">{comparison.get('your_combo_count', 0)} similar campaigns | {comparison.get('your_combo_cancelled_pct', 0):.0f}% cancelled</div>
            </div>
            <div style="font-size: 2rem;">{uplift_icon}</div>
            <div style="text-align: right;">
                <div style="color: #94a3b8; font-size: 0.85rem;">RECOMMENDED COMBO</div>
                <div style="font-size: 1.4rem; color: #66bb6a;">ROI {target_roi:.0f}</div>
                <div style="color: {uplift_color}; font-weight: bold;">{uplift_text}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============ TWO COLUMNS: REACH & EXCLUDE ============
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### ✅ WHO TO REACH")
        st.markdown(f"""
        <div class="factor-positive">
            <div style="font-size: 1.05rem; font-weight: bold; color: #66bb6a;">{ideal.get('top_audience', 'N/A')}</div>
            <div style="color: #e2e8f0; font-size: 0.9rem; margin-top: 6px;">
                via <strong>{ideal.get('top_channel', 'N/A')}</strong> in <strong>{ideal.get('top_region', 'N/A')}</strong>
            </div>
            <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 8px;">
                📊 Based on top {ideal.get('sample_size', 0)} performers • Avg ROI: {ideal.get('avg_roi', 0):.0f} • Conv: {ideal.get('avg_conversion_rate', 0):.1f}%
            </div>
            <div style="color: #00d4ff; font-size: 0.8rem; margin-top: 6px;">
                🏆 Best example: <em>{ideal.get('example_campaign', 'N/A')}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("#### ❌ WHO TO AVOID (Past Mistakes)")
        if exclusions:
            for exc in exclusions[:2]:
                st.markdown(f"""
                <div class="factor-negative">
                    <div style="font-size: 0.95rem; font-weight: bold; color: #ff6b6b;">{exc['campaign_id']} • {exc['status']}</div>
                    <div style="color: #e2e8f0; font-size: 0.85rem; margin-top: 4px;">{exc['campaign_name']}</div>
                    <div style="color: #94a3b8; font-size: 0.78rem; margin-top: 6px;">
                        🔴 {exc['channel']} → {exc['region']} • ROI only {exc['roi']:.0f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No clear failures found for this audience — you have flexibility.")
    
    # ============ STEP-BY-STEP REACH PLAN ============
    st.markdown("#### 📜 Your 3-Phase Reach Plan")
    
    p1 = reach.get('phase_1', {})
    p2 = reach.get('phase_2', {})
    p3 = reach.get('phase_3', {})
    total = reach.get('total_addressable', 0)
    
    st.markdown(f"""
    <div class="glass-card">
        <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 10px;">
            👥 Total Addressable Audience: <strong style="color: #00d4ff;">{total:,}</strong>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
            <div style="padding: 12px; background: rgba(0,212,255,0.1); border-radius: 8px; border-top: 3px solid #00d4ff;">
                <div style="color: #00d4ff; font-weight: bold; font-size: 0.85rem;">DAY {p1.get('day', 1)} • PHASE 1</div>
                <div style="font-size: 1.3rem; color: #e2e8f0; margin: 6px 0;">📧 {p1.get('channel', 'Email')}</div>
                <div style="color: #66bb6a; font-weight: bold;">{p1.get('audience', 0):,} users</div>
                <div style="color: #94a3b8; font-size: 0.78rem; margin-top: 6px;">{p1.get('goal', '')}</div>
            </div>
            <div style="padding: 12px; background: rgba(124,58,237,0.1); border-radius: 8px; border-top: 3px solid #7c3aed;">
                <div style="color: #a78bfa; font-weight: bold; font-size: 0.85rem;">DAY {p2.get('day', 4)} • PHASE 2</div>
                <div style="font-size: 1.3rem; color: #e2e8f0; margin: 6px 0;">💬 {p2.get('channel', 'WhatsApp')}</div>
                <div style="color: #66bb6a; font-weight: bold;">{p2.get('audience', 0):,} users</div>
                <div style="color: #94a3b8; font-size: 0.78rem; margin-top: 6px;">{p2.get('goal', '')}</div>
            </div>
            <div style="padding: 12px; background: rgba(244,114,182,0.1); border-radius: 8px; border-top: 3px solid #f472b6;">
                <div style="color: #f472b6; font-weight: bold; font-size: 0.85rem;">DAY {p3.get('day', 7)} • PHASE 3</div>
                <div style="font-size: 1.3rem; color: #e2e8f0; margin: 6px 0;">📱 {p3.get('channel', 'SMS')}</div>
                <div style="color: #66bb6a; font-weight: bold;">{p3.get('audience', 0):,} users</div>
                <div style="color: #94a3b8; font-size: 0.78rem; margin-top: 6px;">{p3.get('goal', '')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============ WINNING PATTERNS QUICK CHIPS ============
    st.markdown("#### 🏆 Winning Patterns From Your Data")
    
    chip_cols = st.columns(3)
    with chip_cols[0]:
        chans = patterns.get('best_channels', {})
        chan_str = " • ".join([f"{k} ({v})" for k, v in list(chans.items())[:3]]) or "N/A"
        st.markdown(f"""
        <div style="padding: 10px; background: rgba(102,187,106,0.1); border-radius: 8px;">
            <div style="color: #66bb6a; font-size: 0.8rem; font-weight: bold;">TOP CHANNELS</div>
            <div style="color: #e2e8f0; font-size: 0.9rem; margin-top: 4px;">{chan_str}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with chip_cols[1]:
        regs = patterns.get('best_regions', {})
        reg_str = " • ".join([f"{k} ({v})" for k, v in list(regs.items())[:3]]) or "N/A"
        st.markdown(f"""
        <div style="padding: 10px; background: rgba(0,212,255,0.1); border-radius: 8px;">
            <div style="color: #00d4ff; font-size: 0.8rem; font-weight: bold;">TOP REGIONS</div>
            <div style="color: #e2e8f0; font-size: 0.9rem; margin-top: 4px;">{reg_str}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with chip_cols[2]:
        auds = patterns.get('best_audiences', {})
        aud_str = " • ".join([f"{k} ({v})" for k, v in list(auds.items())[:3]]) or "N/A"
        st.markdown(f"""
        <div style="padding: 10px; background: rgba(244,114,182,0.1); border-radius: 8px;">
            <div style="color: #f472b6; font-size: 0.8rem; font-weight: bold;">TOP AUDIENCES</div>
            <div style="color: #e2e8f0; font-size: 0.9rem; margin-top: 4px;">{aud_str}</div>
        </div>
        """, unsafe_allow_html=True)


def render_executive_summary(exec_summary: dict):
    """Render compact executive impact summary."""
    st.markdown("### 👔 Executive Summary")
    
    # Compact headline + recommendation
    recommendation = exec_summary.get('recommendation', 'CAUTION')
    if 'GO' in recommendation and 'NO' not in recommendation:
        rec_color = "#66bb6a"
    elif 'NO-GO' in recommendation or 'NO GO' in recommendation:
        rec_color = "#ff6b6b"
    else:
        rec_color = "#ffa726"
    
    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid {rec_color};">
        <div style="font-size: 1.2rem; font-weight: bold; color: #e2e8f0; margin-bottom: 10px;">
            {exec_summary.get('headline', 'Campaign Assessment')}
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 15px;">
            <div>
                <div style="color: #00d4ff; font-size: 0.8rem; font-weight: bold;">💰 BUSINESS</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">{exec_summary.get('business_impact', 'Analyzing...')}</div>
            </div>
            <div>
                <div style="color: #7c3aed; font-size: 0.8rem; font-weight: bold;">👥 CUSTOMER</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">{exec_summary.get('customer_impact', 'Analyzing...')}</div>
            </div>
            <div>
                <div style="color: #f472b6; font-size: 0.8rem; font-weight: bold;">🏢 BRAND</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">{exec_summary.get('brand_impact', 'Analyzing...')}</div>
            </div>
        </div>
        <div style="padding: 12px; background: rgba(0,0,0,0.3); border-radius: 8px;">
            <span style="color: {rec_color}; font-weight: bold;">📋 {recommendation}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_live_signals(signals: list):
    """Render live risk signals."""
    st.markdown("### 📡 Live Risk Signals")
    
    for signal in signals:
        severity = signal.get('severity', 'MEDIUM')
        if severity == "HIGH":
            icon = "🔴"
            color = "#ff6b6b"
        elif severity == "MEDIUM":
            icon = "🟡"
            color = "#ffa726"
        else:
            icon = "🟢"
            color = "#66bb6a"
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 12px; 
                    background: rgba(255,255,255,0.05); border-radius: 10px; margin: 8px 0;
                    border-left: 4px solid {color};">
            <span class="live-signal"></span>
            <div style="flex: 1;">
                <strong>{icon} {signal.get('type', 'ALERT')}</strong>: {signal.get('message', '')}
            </div>
            <div style="text-align: right; color: #94a3b8; font-size: 0.85rem;">
                {signal.get('timestamp', '')} | {signal.get('trend', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application."""
    
    # Header
    st.markdown('<p class="main-header">🛡️ OptiGuard AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Marketing Operations Control Tower | Predictive Campaign Intelligence</p>', unsafe_allow_html=True)
    
    # Load resources
    predictor = load_predictor()
    finder = load_finder()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Campaign Configuration")
        
        campaign_idea = st.text_area(
            "Campaign Idea",
            placeholder="e.g., Diwali personal loan with zero processing fee",
            height=80
        )
        
        audience = st.selectbox(
            "Target Audience",
            ["Salaried Millennials", "Self-Employed Professionals", "Salaried Gen-Z",
             "HNI Customers", "Senior Citizens", "Students", "NRI Customers",
             "Small Business Owners", "First-Time Borrowers"]
        )
        
        channel = st.selectbox(
            "Primary Channel",
            ["Email", "SMS", "WhatsApp", "Push Notification", "Social Media"]
        )
        
        secondary_channels = st.multiselect(
            "Additional Channels (Optional)",
            ["Email", "SMS", "WhatsApp", "Push Notification", "Social Media", "Call Center"],
            default=[],
            help="Select supporting channels for multi-channel campaigns"
        )
        
        product = st.selectbox(
            "Product",
            ["Personal Loan", "Home Loan", "Credit Card", "Car Loan", "Business Loan",
             "Education Loan", "Fixed Deposit", "Insurance", "Mutual Fund", "Gold Loan",
             "NRI Account", "Savings Account", "Demat Account"]
        )
        
        region = st.selectbox(
            "Region",
            ["Pan India", "North India", "South India", "East India", "West India",
             "Mumbai", "Delhi NCR", "Bangalore", "Chennai"]
        )
        
        st.markdown("#### 💰 Budget & Timeline")
        
        budget = st.number_input(
            "Campaign Budget (₹)",
            min_value=10000,
            max_value=100000000,
            value=500000,
            step=50000,
            help="Total campaign spend in INR"
        )
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            launch_date = st.date_input(
                "Launch Date",
                value=datetime.now().date()
            )
        with col_d2:
            end_date = st.date_input(
                "End Date",
                value=datetime.now().date() + timedelta(days=30)
            )
        
        campaign_duration = (end_date - launch_date).days
        if campaign_duration > 0:
            st.caption(f"📅 Duration: **{campaign_duration} days** | 💸 Daily Spend: **₹{budget/max(campaign_duration,1):,.0f}**")
        
        st.markdown("---")
        
        analyze_btn = st.button("🔮 PREDICT RISKS", type="primary", use_container_width=True)
        optimize_btn = st.button("⚡ OPTIMIZE CAMPAIGN", use_container_width=True)
    
    # Main content
    if analyze_btn and campaign_idea:
        with st.spinner("🧠 AI is analyzing your campaign..."):
            # Run prediction
            risks = predictor.predict_campaign_risk(
                campaign_idea=campaign_idea,
                audience_segment=audience,
                channel=channel,
                region=region,
                product=product
            )
            
            # Get additional data
            factors = predictor.get_risk_factor_breakdown(audience, channel, product, region)
            
            health = predictor.calculate_campaign_health_score(risks)
            exec_summary = predictor.get_executive_impact_summary(campaign_idea, risks)
            playbook = predictor.get_audience_playbook(product, channel, audience, region)
            
            # Store in session
            st.session_state['risks'] = risks
            st.session_state['factors'] = factors
            st.session_state['health'] = health
            st.session_state['exec_summary'] = exec_summary
            st.session_state['playbook'] = playbook
            st.session_state['campaign_idea'] = campaign_idea
            st.session_state['campaign_meta'] = {
                'audience': audience,
                'channel': channel,
                'secondary_channels': secondary_channels,
                'product': product,
                'region': region,
                'budget': budget,
                'launch_date': str(launch_date),
                'end_date': str(end_date),
                'duration_days': campaign_duration
            }
    
    # Display results
    if 'risks' in st.session_state:
        # Health Score - BIG and prominent
        render_health_score(st.session_state['health'])
        render_contextual_chat(
            'health',
            'Campaign Health Score',
            {
                'health': st.session_state['health'],
                'campaign_meta': st.session_state.get('campaign_meta', {})
            },
            predictor
        )
        
        st.markdown("---")
        
        # Top Contributing Factors (full width)
        render_risk_factors(st.session_state['factors'])
        render_contextual_chat(
            'factors',
            'Risk Factors',
            {
                'factors': st.session_state['factors'],
                'campaign_idea': st.session_state['campaign_idea'],
                'campaign_meta': st.session_state.get('campaign_meta', {})
            },
            predictor
        )
        
        st.markdown("---")
        
        # Audience Intelligence & Reach Playbook
        render_audience_playbook(
            st.session_state['playbook'],
            st.session_state.get('campaign_meta', {})
        )
        render_contextual_chat(
            'playbook',
            'Audience Playbook',
            st.session_state['playbook'],
            predictor
        )
        
        st.markdown("---")
        
        # Similar Historical Campaigns (full width, below factors)
        render_similar_campaigns(finder, st.session_state['campaign_idea'])
        render_contextual_chat(
            'similar',
            'Similar Campaigns',
            {
                'campaign_idea': st.session_state['campaign_idea'],
                'similar_campaigns': finder.search(
                    st.session_state['campaign_idea'], top_k=3
                ).to_dict('records')
            },
            predictor
        )
        
        st.markdown("---")
        
        # Executive Summary
        render_executive_summary(st.session_state['exec_summary'])
        render_contextual_chat(
            'exec',
            'Executive Summary',
            st.session_state['exec_summary'],
            predictor
        )
        
        st.markdown("---")
        
        # Optimization Section
        if optimize_btn or 'optimization' in st.session_state:
            if optimize_btn:
                with st.spinner("⚡ AI is analyzing historical complaints, transforming messaging & calculating risk reductions..."):
                    # 1. Historical analysis from similar past campaigns
                    historical = predictor.get_historical_risk_breakdown(product, audience)
                    st.session_state['historical_risk'] = historical
                    
                    # 2. AI messaging transformation + optimization
                    optimization = predictor.optimize_campaign(
                        st.session_state['campaign_idea'],
                        audience, channel,
                        st.session_state['risks']
                    )
                    st.session_state['optimization'] = optimization
                    
                    # 3. Compute before/after deltas
                    deltas = predictor.calculate_optimization_deltas(historical, optimization)
                    st.session_state['opt_deltas'] = deltas
                    
                    # 4. Executive summary explaining the WHY
                    opt_exec = predictor.generate_optimization_executive_summary(
                        st.session_state['campaign_idea'], historical, deltas, optimization
                    )
                    st.session_state['opt_exec_summary'] = opt_exec
                    
                    # Match to known problem statement & build resolution mapping
                    matched_scenario = predictor.match_problem_statement(
                        st.session_state['campaign_idea'],
                        audience, product, channel
                    )
                    st.session_state['matched_scenario'] = matched_scenario
                    if matched_scenario:
                        st.session_state['resolutions'] = predictor.map_solution_to_complaint(
                            matched_scenario, optimization, st.session_state['risks']
                        )
            
            if 'optimization' in st.session_state:
                # Step 1: Historical baseline
                render_historical_baseline(st.session_state['historical_risk'])
                
                # Step 2 & 3: Optimization (messaging + before/after deltas)
                render_optimization(st.session_state['optimization'])
                render_predicted_reductions(
                    st.session_state['opt_deltas'],
                    st.session_state['historical_risk']
                )
                
                # Step 4: Executive summary
                render_optimization_exec_summary(st.session_state['opt_exec_summary'])
    
    else:
        # Landing state
        st.markdown("---")
        
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h2>🚀 Enter Your Campaign Details</h2>
            <p style="color: #94a3b8;">
                Configure your campaign in the sidebar and click <strong>PREDICT RISKS</strong> to see:
            </p>
            <ul style="text-align: left; max-width: 500px; margin: 0 auto; color: #94a3b8;">
                <li>Campaign Health Score (0-100)</li>
                <li>Risk Factor Breakdown with Impact %</li>
                <li>AI Reasoning & Evidence</li>
                <li>Similar Historical Campaigns</li>
                <li>Executive Impact Summary</li>
                <li>AI Campaign Optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
