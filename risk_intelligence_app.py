"""
AI Campaign Risk Intelligence Platform
=======================================

Predictive Marketing Operations Intelligence
- Predict campaign failures before launch
- Fatigue & Trust Risk Engine
- AI Campaign Simulation
- Smart Channel Recommendations
- Executive AI Summary

This is NOT a dashboard. This is PREDICTIVE INTELLIGENCE.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import json

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from campaign_risk_predictor import CampaignRiskPredictor
from similar_campaign_finder import SimilarCampaignFinder

# Page configuration
st.set_page_config(
    page_title="OptiGuard AI - Campaign Risk Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .risk-card-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
    }
    .risk-card-medium {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
    }
    .risk-card-low {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border-left: 4px solid #667eea;
    }
    .warning-banner {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .success-banner {
        background: #d4edda;
        border: 1px solid #28a745;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .insight-box {
        background: #e3f2fd;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border-left: 4px solid #2196f3;
    }
    .recommendation-box {
        background: #f3e5f5;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_risk_predictor():
    """Load and cache the Campaign Risk Predictor."""
    return CampaignRiskPredictor()


@st.cache_resource
def load_campaign_finder():
    """Load and cache the Similar Campaign Finder."""
    finder = SimilarCampaignFinder()
    finder.build_index()
    return finder


def render_risk_gauge(score: float, label: str, size: str = "large"):
    """Render a risk gauge visualization."""
    if score >= 70:
        color = "#ff6b6b"
        level = "HIGH"
    elif score >= 40:
        color = "#ffa726"
        level = "MEDIUM"
    else:
        color = "#66bb6a"
        level = "LOW"
    
    if size == "large":
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 3rem; font-weight: bold; color: {color};">{score}%</div>
            <div style="font-size: 1.2rem; color: {color}; font-weight: bold;">{level} RISK</div>
            <div style="font-size: 0.9rem; color: #666;">{label}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <div style="font-size: 1.8rem; font-weight: bold; color: {color};">{score}%</div>
            <div style="font-size: 0.8rem; color: {color};">{level}</div>
            <div style="font-size: 0.75rem; color: #666;">{label}</div>
        </div>
        """, unsafe_allow_html=True)


def render_recommendation_card(rec: dict):
    """Render a recommendation card."""
    priority_colors = {"HIGH": "#ff6b6b", "MEDIUM": "#ffa726", "LOW": "#66bb6a"}
    color = priority_colors.get(rec.get('priority', 'MEDIUM'), "#ffa726")
    
    st.markdown(f"""
    <div class="recommendation-box">
        <span style="color: {color}; font-weight: bold;">[{rec.get('priority', 'MEDIUM')}]</span>
        <strong>{rec.get('action', 'N/A')}</strong><br>
        <span style="color: #666;">{rec.get('details', '')}</span><br>
        <span style="color: #9c27b0; font-size: 0.85rem;">Impact: {rec.get('expected_impact', 'N/A')}</span>
    </div>
    """, unsafe_allow_html=True)


def page_campaign_simulation():
    """AI Campaign Risk Simulation Page."""
    st.markdown('<p class="main-header">🎯 AI Campaign Risk Simulator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Predict campaign failure risks BEFORE launch</p>', unsafe_allow_html=True)
    
    predictor = load_risk_predictor()
    
    st.markdown("---")
    
    # Input Section
    st.markdown("### 📝 Enter Campaign Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        campaign_idea = st.text_area(
            "Campaign Idea / Description",
            placeholder="e.g., Diwali personal loan campaign with zero processing fee for salaried millennials",
            height=100
        )
        
        audience_segment = st.selectbox(
            "Target Audience",
            ["Salaried Millennials", "Self-Employed Professionals", "Salaried Gen-Z",
             "HNI Customers", "Senior Citizens", "Students", "NRI Customers",
             "Small Business Owners", "First-Time Borrowers", "Existing Customers"]
        )
        
        channel = st.selectbox(
            "Primary Channel",
            ["Email", "SMS", "WhatsApp", "Push Notification", "Social Media"]
        )
    
    with col2:
        product = st.selectbox(
            "Product / Service",
            ["Personal Loan", "Home Loan", "Credit Card", "Car Loan", "Business Loan",
             "Fixed Deposit", "Savings Account", "Insurance", "Mutual Fund", "Gold Loan"]
        )
        
        region = st.selectbox(
            "Target Region",
            ["Pan India", "North India", "South India", "East India", "West India",
             "Mumbai", "Delhi NCR", "Bangalore", "Chennai", "Kolkata", "Hyderabad"]
        )
        
        budget = st.number_input("Budget (₹)", min_value=10000, max_value=10000000, value=100000, step=10000)
        
        objective = st.selectbox(
            "Campaign Objective",
            ["Acquisition", "Retention", "Upsell", "Cross-sell", "Re-engagement", "Brand Awareness"]
        )
    
    st.markdown("---")
    
    # Predict Button
    if st.button("🔮 PREDICT CAMPAIGN RISK", type="primary", use_container_width=True):
        if not campaign_idea:
            st.warning("Please enter a campaign idea/description")
            return
        
        with st.spinner("🧠 AI is analyzing campaign risks..."):
            prediction = predictor.predict_campaign_risk(
                campaign_idea=campaign_idea,
                audience_segment=audience_segment,
                channel=channel,
                region=region,
                budget=budget,
                product=product,
                objective=objective
            )
            st.session_state['risk_prediction'] = prediction
    
    # Display Prediction Results
    if 'risk_prediction' in st.session_state:
        prediction = st.session_state['risk_prediction']
        
        st.markdown("---")
        st.markdown("## 📊 Campaign Risk Assessment")
        
        # Overall Risk Banner
        overall = prediction['overall_risk']
        if overall['level'] == "HIGH":
            st.markdown(f"""
            <div class="risk-card-high">
                <h2>⚠️ HIGH RISK CAMPAIGN</h2>
                <p>Overall Risk Score: <strong>{overall['score']}%</strong></p>
                <p>Recommendation: <strong>{overall['launch_recommendation']}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        elif overall['level'] == "MEDIUM":
            st.markdown(f"""
            <div class="risk-card-medium">
                <h2>⚡ MODERATE RISK CAMPAIGN</h2>
                <p>Overall Risk Score: <strong>{overall['score']}%</strong></p>
                <p>Recommendation: <strong>{overall['launch_recommendation']}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="risk-card-low">
                <h2>✅ LOW RISK CAMPAIGN</h2>
                <p>Overall Risk Score: <strong>{overall['score']}%</strong></p>
                <p>Recommendation: <strong>{overall['launch_recommendation']}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Risk Metrics Grid
        st.markdown("### 📈 Risk Breakdown")
        
        risk_cols = st.columns(4)
        
        with risk_cols[0]:
            render_risk_gauge(
                prediction['fatigue_risk']['score'],
                "Fatigue Risk",
                "small"
            )
            st.caption(prediction['fatigue_risk']['description'][:100])
        
        with risk_cols[1]:
            render_risk_gauge(
                prediction['opt_out_risk']['probability'],
                "Opt-Out Risk",
                "small"
            )
            st.caption(prediction['opt_out_risk']['description'])
        
        with risk_cols[2]:
            render_risk_gauge(
                prediction['complaint_risk']['probability'],
                "Complaint Risk",
                "small"
            )
            st.caption(prediction['complaint_risk']['description'][:100])
        
        with risk_cols[3]:
            render_risk_gauge(
                prediction['trust_risk']['score'],
                "Trust Risk",
                "small"
            )
            st.caption(prediction['trust_risk']['description'][:100])
        
        st.markdown("---")
        
        # ROI Prediction & Channel Safety
        st.markdown("### 💰 ROI & Channel Analysis")
        
        roi_col, channel_col = st.columns(2)
        
        with roi_col:
            st.markdown("#### Expected ROI")
            roi = prediction['roi_prediction']
            st.metric("Expected ROI", roi['expected_roi'], roi['roi_range'])
            
            health_color = "#66bb6a" if roi['health'] == "HEALTHY" else ("#ffa726" if roi['health'] == "MODERATE" else "#ff6b6b")
            st.markdown(f"ROI Health: <span style='color: {health_color}; font-weight: bold;'>{roi['health']}</span>", unsafe_allow_html=True)
            
            if roi.get('warning'):
                st.warning(roi['warning'])
            
            st.caption(f"Confidence: {roi['confidence']}")
        
        with channel_col:
            st.markdown("#### Channel Safety")
            channel_safety = prediction['channel_safety']
            
            safety_color = "#66bb6a" if channel_safety['score'] >= 70 else ("#ffa726" if channel_safety['score'] >= 50 else "#ff6b6b")
            st.markdown(f"""
            <div style="text-align: center; padding: 10px;">
                <div style="font-size: 2rem; font-weight: bold; color: {safety_color};">{channel_safety['score']}%</div>
                <div>Channel Safety Score</div>
            </div>
            """, unsafe_allow_html=True)
            
            if channel_safety['alternatives']:
                st.markdown("**Safer Alternatives:**")
                for alt in channel_safety['alternatives']:
                    st.write(f"→ {alt['channel']}: {alt['safety_score']}% ({alt['improvement']})")
        
        st.markdown("---")
        
        # Best Contact Time
        st.markdown("### ⏰ Optimal Timing")
        timing = prediction['best_contact_time']
        
        time_col1, time_col2 = st.columns(2)
        with time_col1:
            st.info(f"**Best Time:** {timing['recommended_time']}")
        with time_col2:
            st.info(f"**Best Days:** {timing['recommended_days']}")
        st.caption(timing['reasoning'])
        
        st.markdown("---")
        
        # AI Insights
        st.markdown("### 🧠 AI Risk Insights")
        insights = prediction.get('ai_insights', [])
        for insight in insights:
            st.markdown(f"""
            <div class="insight-box">
                {insight}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recommendations
        st.markdown("### 🎯 AI Recommendations")
        recommendations = prediction.get('recommendations', [])
        for rec in recommendations:
            render_recommendation_card(rec)
        
        # Confidence
        st.markdown("---")
        conf = prediction['prediction_confidence']
        st.caption(f"Prediction Confidence: {conf['level']} ({conf['percentage']}%) - {conf['reason']}")


def page_fatigue_risk_engine():
    """Fatigue & Trust Risk Engine Page."""
    st.markdown('<p class="main-header">⚡ Fatigue & Trust Risk Engine</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Monitor audience fatigue and customer trust erosion</p>', unsafe_allow_html=True)
    
    predictor = load_risk_predictor()
    
    st.markdown("---")
    
    # Audience Fatigue Analysis
    st.markdown("### 📊 Audience Fatigue Analysis")
    
    audience = st.selectbox(
        "Select Audience Segment",
        ["Salaried", "Self-Employed", "HNI", "Senior", "Student", "NRI", "Millennials", "Gen-Z"]
    )
    
    if st.button("🔍 Analyze Fatigue Risk", type="primary"):
        with st.spinner("Analyzing fatigue patterns..."):
            report = predictor.get_audience_fatigue_report(audience)
            st.session_state['fatigue_report'] = report
    
    if 'fatigue_report' in st.session_state:
        report = st.session_state['fatigue_report']
        
        if "error" in report:
            st.error(report['error'])
        else:
            # Fatigue Score Display
            col1, col2, col3 = st.columns(3)
            
            with col1:
                render_risk_gauge(report['fatigue_score'], "Fatigue Score")
            
            with col2:
                st.metric("Total Campaigns Received", report['total_campaigns_received'])
                st.metric("Average ROI", f"{report['average_roi']:.1f}")
            
            with col3:
                st.markdown("**Feedback Summary**")
                fb = report['feedback_summary']
                st.write(f"✅ Positive: {fb['positive']}")
                st.write(f"❌ Negative: {fb['negative']}")
            
            st.markdown("---")
            
            # Channel Breakdown
            st.markdown("#### Channel Exposure")
            channels = report.get('channels_breakdown', {})
            if channels:
                channel_df = pd.DataFrame(list(channels.items()), columns=['Channel', 'Campaigns'])
                st.bar_chart(channel_df.set_index('Channel'))
            
            # Recommendation
            st.markdown("---")
            st.markdown("#### 🎯 Recommendation")
            st.warning(report['recommendation'])
    
    st.markdown("---")
    
    # Early Warning Signals
    st.markdown("### 🚨 Early Warning Signals")
    
    if st.button("🔔 Get Early Warnings", type="secondary"):
        with st.spinner("Scanning for warning signals..."):
            warnings = predictor.get_early_warning_signals()
            st.session_state['early_warnings'] = warnings
    
    if 'early_warnings' in st.session_state:
        warnings = st.session_state['early_warnings']
        
        if not warnings:
            st.success("✅ No critical warnings detected")
        else:
            for warning in warnings:
                severity = warning.get('severity', 'MEDIUM')
                if severity == "HIGH":
                    st.error(f"🚨 **{warning.get('type', 'WARNING')}**: {warning.get('message', '')}")
                else:
                    st.warning(f"⚠️ **{warning.get('type', 'WARNING')}**: {warning.get('message', '')}")
                st.caption(f"Recommendation: {warning.get('recommendation', 'N/A')}")


def page_similar_campaigns():
    """Similar Campaign Intelligence Page."""
    st.markdown('<p class="main-header">🔍 Similar Campaign Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Find similar campaigns using semantic search</p>', unsafe_allow_html=True)
    
    finder = load_campaign_finder()
    
    st.markdown("---")
    
    # Search
    query = st.text_input(
        "Describe your campaign idea",
        placeholder="e.g., Festive personal loan campaign for young professionals"
    )
    
    top_k = st.slider("Number of results", 3, 15, 5)
    
    if st.button("🔍 Find Similar Campaigns", type="primary"):
        if query:
            with st.spinner("Searching..."):
                results = finder.search(query, top_k=top_k)
                st.session_state['search_results'] = results
    
    if 'search_results' in st.session_state:
        results = st.session_state['search_results']
        
        if results.empty:
            st.warning("No similar campaigns found")
        else:
            st.markdown(f"### Found {len(results)} Similar Campaigns")
            
            for _, row in results.iterrows():
                roi_color = "#66bb6a" if row['ROI'] > 400 else ("#ffa726" if row['ROI'] > 200 else "#ff6b6b")
                
                with st.expander(f"**{row['Rank']}. {row['Campaign']}** | ROI: {row['ROI']} | Match: {row['Similarity_Score']}%"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Product:** {row['Product']}")
                        st.write(f"**Audience:** {row['Audience']}")
                        st.write(f"**Channel:** {row['Channel']}")
                    
                    with col2:
                        st.write(f"**Objective:** {row['Objective']}")
                        st.write(f"**CTR:** {row['CTR']}")
                        st.write(f"**Feedback:** {row['Feedback']}")


def page_executive_summary():
    """Executive AI Summary Page."""
    st.markdown('<p class="main-header">📊 Executive AI Summary</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-generated operational intelligence for leadership</p>', unsafe_allow_html=True)
    
    predictor = load_risk_predictor()
    
    st.markdown("---")
    
    if st.button("🧠 Generate Executive Summary", type="primary", use_container_width=True):
        with st.spinner("AI is analyzing campaign operations..."):
            # Generate summary
            warnings = predictor.get_early_warning_signals()
            
            # Calculate overall health
            if predictor.campaigns_df is not None:
                avg_roi = predictor.campaigns_df['roi'].mean()
                total_campaigns = len(predictor.campaigns_df)
                
                st.session_state['exec_summary'] = {
                    'total_campaigns': total_campaigns,
                    'avg_roi': avg_roi,
                    'warnings': warnings,
                    'generated': True
                }
    
    if st.session_state.get('exec_summary', {}).get('generated'):
        summary = st.session_state['exec_summary']
        
        st.markdown("### 📈 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Campaigns", f"{summary['total_campaigns']:,}")
        with col2:
            st.metric("Average ROI", f"{summary['avg_roi']:.1f}")
        with col3:
            st.metric("Active Warnings", len(summary['warnings']))
        with col4:
            health = "GOOD" if len(summary['warnings']) < 3 else ("MODERATE" if len(summary['warnings']) < 6 else "NEEDS ATTENTION")
            st.metric("Operations Health", health)
        
        st.markdown("---")
        
        st.markdown("### 🚨 Priority Alerts")
        for warning in summary['warnings'][:5]:
            severity = warning.get('severity', 'MEDIUM')
            icon = "🔴" if severity == "HIGH" else "🟡"
            st.markdown(f"{icon} **{warning.get('type')}**: {warning.get('message')}")
        
        st.markdown("---")
        
        st.markdown("### 🎯 AI Recommendations")
        st.info("1. Focus on diversifying channel mix to reduce fatigue")
        st.info("2. Implement cooling periods for heavily targeted segments")
        st.info("3. Monitor complaint rates on SMS and Push channels")
        st.info("4. Consider WhatsApp + Email combination for better engagement")


def main():
    """Main application entry point."""
    
    # Sidebar Navigation
    st.sidebar.markdown("# 🛡️ OptiGuard AI")
    st.sidebar.markdown("### Campaign Risk Intelligence")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigate",
        [
            "🎯 Campaign Risk Simulator",
            "⚡ Fatigue & Trust Engine",
            "🔍 Similar Campaigns",
            "📊 Executive Summary"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "**OptiGuard AI** predicts campaign operational risks "
        "BEFORE launch, helping prevent:\n\n"
        "- Customer fatigue\n"
        "- Opt-out surges\n"
        "- Trust erosion\n"
        "- Campaign failures"
    )
    
    # Render selected page
    if page == "🎯 Campaign Risk Simulator":
        page_campaign_simulation()
    elif page == "⚡ Fatigue & Trust Engine":
        page_fatigue_risk_engine()
    elif page == "🔍 Similar Campaigns":
        page_similar_campaigns()
    elif page == "📊 Executive Summary":
        page_executive_summary()


if __name__ == "__main__":
    main()
