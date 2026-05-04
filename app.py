"""
Similar Campaign Finder - Streamlit App
========================================

A Streamlit interface for the Similar Campaign Finder feature.
Search for similar marketing campaigns using semantic search.
Get AI-powered targeting recommendations based on campaign analysis.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from similar_campaign_finder import SimilarCampaignFinder

# Page configuration
st.set_page_config(
    page_title="Similar Campaign Finder",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    }
    .metric-positive { color: #28a745; font-weight: bold; }
    .metric-negative { color: #dc3545; font-weight: bold; }
    .similarity-badge {
        background-color: #1f77b4;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.8rem;
    }
    .recommendation-card {
        background-color: #e8f4fd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #28a745;
    }
    .warning-card {
        background-color: #fff3cd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #ffc107;
    }
    .avoid-card {
        background-color: #f8d7da;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_finder():
    """Load and cache the Similar Campaign Finder."""
    finder = SimilarCampaignFinder()
    finder.build_index()
    return finder


def display_recommendations(recommendations: dict):
    """Display AI-generated targeting recommendations."""
    st.markdown("## 🎯 AI Targeting Recommendations")
    
    if "error" in recommendations:
        st.error(f"Error: {recommendations['error']}")
        return
    
    # Summary
    if "summary" in recommendations:
        st.info(f"**Summary:** {recommendations['summary']}")
    
    col1, col2 = st.columns(2)
    
    # Recommended Audiences
    with col1:
        st.markdown("### ✅ Recommended Audiences")
        if recommendations.get("recommended_audiences"):
            for aud in recommendations["recommended_audiences"]:
                if isinstance(aud, dict):
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <strong>{aud.get('segment', 'N/A')}</strong><br>
                        <em>{aud.get('reason', '')}</em>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success(f"• {aud}")
        else:
            st.write("No specific recommendations available")
    
    # Audiences to Avoid
    with col2:
        st.markdown("### ⛔ Audiences to Avoid")
        if recommendations.get("avoid_audiences"):
            for aud in recommendations["avoid_audiences"]:
                if isinstance(aud, dict):
                    st.markdown(f"""
                    <div class="avoid-card">
                        <strong>{aud.get('segment', 'N/A')}</strong><br>
                        <em>{aud.get('reason', '')}</em>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"• {aud}")
        else:
            st.write("No audiences identified to avoid")
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    # Timing Recommendations
    with col3:
        st.markdown("### ⏰ Timing Recommendations")
        timing = recommendations.get("timing_recommendations", {})
        if isinstance(timing, dict):
            if timing.get("best_days"):
                st.write(f"**Best Days:** {timing['best_days']}")
            if timing.get("best_times"):
                st.write(f"**Best Times:** {timing['best_times']}")
            if timing.get("avoid_periods"):
                st.write(f"**Avoid:** {timing['avoid_periods']}")
            if timing.get("note"):
                st.info(timing["note"])
        else:
            st.write(str(timing))
    
    # Channel Recommendations
    with col4:
        st.markdown("### 📢 Channel Recommendations")
        if recommendations.get("channel_recommendations"):
            for ch in recommendations["channel_recommendations"]:
                if isinstance(ch, dict):
                    priority = ch.get('priority', 'medium')
                    icon = "🔥" if priority == "high" else ("📌" if priority == "medium" else "📎")
                    st.write(f"{icon} **{ch.get('channel', 'N/A')}** ({priority}) - {ch.get('reason', '')}")
                else:
                    st.write(f"• {ch}")
        else:
            st.write("No channel recommendations available")
    
    st.markdown("---")
    
    # Key Learnings
    st.markdown("### 💡 Key Learnings")
    learnings = recommendations.get("key_learnings", [])
    if learnings:
        for learning in learnings:
            st.info(f"• {learning}")
    else:
        st.write("No specific learnings identified")
    
    # Warnings
    if recommendations.get("warnings"):
        st.markdown("### ⚠️ Warnings")
        for warning in recommendations["warnings"]:
            st.warning(f"• {warning}")


def display_performance_analysis(analysis: dict):
    """Display campaign performance analysis - what worked vs what didn't."""
    st.markdown("### 📈 Campaign Performance Comparison")
    
    if "error" in analysis:
        st.error(f"Error: {analysis['error']}")
        return
    
    # Summary
    if "summary" in analysis:
        st.info(f"**Analysis Summary:** {analysis['summary']}")
    
    if "total_campaigns_analyzed" in analysis:
        st.caption(f"📊 Analyzed {analysis['total_campaigns_analyzed']} campaigns | Median ROI: {analysis.get('median_roi', 'N/A'):.1f}")
    
    st.markdown("---")
    
    # Two columns: Top Performers vs Underperformers
    col1, col2 = st.columns(2)
    
    # Top 3 Performers
    with col1:
        st.markdown("### ✅ Top 3 Best Performers")
        top_performers = analysis.get("top_performers", [])
        
        if top_performers:
            for i, perf in enumerate(top_performers[:3], 1):
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: #d4edda; border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 4px solid #28a745;">
                        <strong>#{i} {perf.get('campaign', 'N/A')}</strong><br>
                        <span style="color: #28a745; font-size: 1.2em;">ROI: {perf.get('roi', 'N/A')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Success reasons
                    if perf.get('success_reasons'):
                        st.markdown("**Why it worked:**")
                        for reason in perf['success_reasons']:
                            st.success(f"✓ {reason}")
                    
                    # Key strengths
                    if perf.get('key_strengths'):
                        st.markdown("**Key Strengths:**")
                        st.write(", ".join(perf['key_strengths']))
                    
                    st.markdown("---")
        else:
            st.write("No top performers data available")
    
    # Bottom 3 Underperformers
    with col2:
        st.markdown("### ❌ Top 3 Underperformers")
        underperformers = analysis.get("underperformers", [])
        
        if underperformers:
            for i, under in enumerate(underperformers[:3], 1):
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: #f8d7da; border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 4px solid #dc3545;">
                        <strong>#{i} {under.get('campaign', 'N/A')}</strong><br>
                        <span style="color: #dc3545; font-size: 1.2em;">ROI: {under.get('roi', 'N/A')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Failure reasons
                    if under.get('failure_reasons'):
                        st.markdown("**Why it didn't work:**")
                        for reason in under['failure_reasons']:
                            st.error(f"✗ {reason}")
                    
                    # Improvement suggestions
                    if under.get('improvement_suggestions'):
                        st.markdown("**How to improve:**")
                        for suggestion in under['improvement_suggestions']:
                            st.info(f"💡 {suggestion}")
                    
                    st.markdown("---")
        else:
            st.write("No underperformer data available")
    
    st.markdown("---")
    
    # Comparison Insights - The KEY difference
    st.markdown("### 🔄 Key Differences: Why Some Worked & Others Didn't")
    
    comparison_col1, comparison_col2 = st.columns(2)
    
    with comparison_col1:
        st.markdown("#### 🏆 Success Factors")
        success_factors = analysis.get("success_factors", [])
        if success_factors:
            for factor in success_factors:
                st.markdown(f"""
                <div style="background-color: #e8f5e9; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    ✅ {factor}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No success factors identified")
    
    with comparison_col2:
        st.markdown("#### ⚠️ Failure Factors")
        failure_factors = analysis.get("failure_factors", [])
        if failure_factors:
            for factor in failure_factors:
                st.markdown(f"""
                <div style="background-color: #ffebee; padding: 10px; border-radius: 5px; margin: 5px 0;">
                    ❌ {factor}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No failure factors identified")
    
    # Comparison Insights
    st.markdown("---")
    st.markdown("### 💡 Comparison Insights")
    comparison_insights = analysis.get("comparison_insights", [])
    if comparison_insights:
        for insight in comparison_insights:
            st.info(f"📌 {insight}")
    
    # Recommendations
    st.markdown("### 🎯 Recommendations for Your Campaign")
    recommendations = analysis.get("recommendations", [])
    if recommendations:
        for rec in recommendations:
            st.success(f"→ {rec}")


def display_campaign_comparison(comparison: dict):
    """Display the top 3 best vs top 3 worst campaigns comparison."""
    st.markdown("## 📊 Campaign Performance: Best vs Worst")
    
    if "error" in comparison:
        st.error(f"Error: {comparison['error']}")
        return
    
    # Summary
    if "summary" in comparison:
        st.info(f"**Analysis Summary:** {comparison['summary']}")
    
    # Show filters
    filters = comparison.get('filters_applied', [])
    total = comparison.get('total_campaigns_in_filter', 'N/A')
    st.caption(f"📊 Analyzed {total} campaigns | Filters: {', '.join(filters) if filters else 'None'}")
    
    st.markdown("---")
    
    # Two columns: Best vs Worst
    col1, col2 = st.columns(2)
    
    # Top 3 Best Performers
    with col1:
        st.markdown("### ✅ Top 3 Best Performers")
        top_performers = comparison.get("top_performers", [])
        
        for i, perf in enumerate(top_performers[:3], 1):
            st.markdown(f"""
            <div style="background-color: #d4edda; border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 5px solid #28a745;">
                <h4 style="margin: 0; color: #155724;">#{i} {perf.get('campaign', 'N/A')}</h4>
                <p style="font-size: 1.3em; color: #28a745; margin: 5px 0;"><strong>ROI: {perf.get('roi', 'N/A')}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Why it worked
            why_worked = perf.get('why_it_worked', [])
            if why_worked:
                st.markdown("**Why it worked:**")
                for reason in why_worked:
                    st.success(f"✓ {reason}")
            
            # Key success factors
            success_factors = perf.get('key_success_factors', [])
            if success_factors:
                st.caption(f"Key factors: {', '.join(str(f) for f in success_factors)}")
            
            st.markdown("")
    
    # Top 3 Worst Performers
    with col2:
        st.markdown("### ❌ Top 3 Underperformers")
        underperformers = comparison.get("underperformers", [])
        
        for i, under in enumerate(underperformers[:3], 1):
            st.markdown(f"""
            <div style="background-color: #f8d7da; border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 5px solid #dc3545;">
                <h4 style="margin: 0; color: #721c24;">#{i} {under.get('campaign', 'N/A')}</h4>
                <p style="font-size: 1.3em; color: #dc3545; margin: 5px 0;"><strong>ROI: {under.get('roi', 'N/A')}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Why it failed
            why_failed = under.get('why_it_failed', [])
            if why_failed:
                st.markdown("**Why it didn't work:**")
                for reason in why_failed:
                    st.error(f"✗ {reason}")
            
            # What went wrong
            what_wrong = under.get('what_went_wrong', [])
            if what_wrong:
                st.caption(f"Issues: {', '.join(str(w) for w in what_wrong)}")
            
            st.markdown("")
    
    st.markdown("---")
    
    # Key Differences
    st.markdown("### 🔄 Key Differences: Why Winners Won & Losers Lost")
    key_differences = comparison.get("key_differences", [])
    if key_differences:
        for i, diff in enumerate(key_differences, 1):
            st.markdown(f"""
            <div style="background-color: #fff3cd; border-radius: 8px; padding: 12px; margin: 8px 0; border-left: 4px solid #ffc107;">
                <strong>{i}.</strong> {diff}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Lessons Learned
    st.markdown("### 📚 Lessons Learned")
    lessons = comparison.get("lessons_learned", [])
    if lessons:
        for lesson in lessons:
            st.info(f"💡 {lesson}")
    
    # Recommendations
    st.markdown("### 🎯 Recommendations for Your New Campaign")
    recs = comparison.get("recommendations_for_new_campaign", [])
    if recs:
        for rec in recs:
            st.success(f"→ {rec}")


def display_content_suggestions(suggestions: dict):
    """Display AI-generated content suggestions."""
    st.markdown("## ✨ AI Content Suggestions")
    
    if "error" in suggestions:
        st.error(f"Error: {suggestions['error']}")
        if "suggestion" in suggestions:
            st.info(suggestions["suggestion"])
        return
    
    # Summary
    if "summary" in suggestions:
        st.success(f"**Strategy Summary:** {suggestions['summary']}")
    
    # Show analysis context
    region_text = suggestions.get('region', 'All Regions')
    campaigns_count = suggestions.get('campaigns_analyzed', 'N/A')
    filters = suggestions.get('filters_applied', [])
    
    st.caption(f"📍 Based on **{campaigns_count}** top-performing campaigns")
    if filters:
        st.caption(f"🔍 Filters: {', '.join(filters)}")
    
    st.markdown("---")
    
    # Suggested Content Examples
    st.markdown("### 📝 Suggested Content")
    suggested_content = suggestions.get("suggested_content", [])
    
    if suggested_content:
        for i, content in enumerate(suggested_content, 1):
            with st.expander(f"**Content Idea #{i}**: {content.get('headline', 'Sample Content')[:50]}...", expanded=(i == 1)):
                if content.get('headline'):
                    st.markdown(f"**Headline:** {content['headline']}")
                if content.get('body_copy'):
                    st.markdown("**Body Copy:**")
                    st.info(content['body_copy'])
                if content.get('why_it_works'):
                    st.caption(f"💡 {content['why_it_works']}")
    else:
        st.write("No content suggestions available")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # Tone Recommendations
    with col1:
        st.markdown("### 🎨 Tone Recommendations")
        tone = suggestions.get("tone_recommendations", {})
        if isinstance(tone, dict):
            if tone.get("primary_tone"):
                st.success(f"**Recommended Tone:** {tone['primary_tone']}")
            if tone.get("avoid_tones"):
                st.error(f"**Avoid:** {', '.join(tone['avoid_tones'])}")
            if tone.get("reasoning"):
                st.caption(tone['reasoning'])
        else:
            st.write(str(tone))
    
    # CTA Suggestions
    with col2:
        st.markdown("### 🔘 Call-to-Action Suggestions")
        ctas = suggestions.get("cta_suggestions", [])
        if ctas:
            for cta in ctas:
                if isinstance(cta, dict):
                    st.markdown(f"**→ {cta.get('cta_text', 'N/A')}**")
                    st.caption(f"  {cta.get('context', '')}")
                else:
                    st.write(f"• {cta}")
        else:
            st.write("No CTA suggestions available")
    
    st.markdown("---")
    
    # Content Tips
    st.markdown("### 💡 Content Tips")
    tips = suggestions.get("content_tips", [])
    if tips:
        for tip in tips:
            st.info(f"• {tip}")
    else:
        st.write("No specific tips available")


def main():
    # Header
    st.markdown('<p class="main-header">🔍 Similar Campaign Finder</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Find similar marketing campaigns and get AI-powered targeting recommendations</p>', unsafe_allow_html=True)
    
    # Sidebar for user context
    with st.sidebar:
        st.markdown("## 🎯 Your Campaign Context")
        st.markdown("*Provide context for better AI recommendations*")
        
        user_budget = st.text_input("💰 Budget", placeholder="e.g., $50,000")
        user_region = st.selectbox(
            "🌍 Target Region",
            ["All Regions", "Pan India", "North India", "South India", "East India", "West India",
             "Mumbai", "Delhi NCR", "Bangalore", "Chennai", "Kolkata", "Hyderabad", 
             "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kochi", "Coimbatore", "Indore", "Nagpur", "Chandigarh"]
        )
        user_goal = st.selectbox(
            "🎯 Campaign Goal",
            ["Any Goal", "Brand Awareness", "Acquisition", "Retention", 
             "Upsell", "Cross-sell", "Re-engagement"]
        )
        user_product = st.text_input("📦 Product/Service", placeholder="e.g., Personal Loan")
        user_timeline = st.text_input("📅 Timeline", placeholder="e.g., Q1 2025")
        
        st.markdown("---")
        
        # Content Suggestion Button
        st.markdown("### ✨ AI Content Suggestions")
        st.caption("Get content ideas based on successful campaigns in your region")
        
        suggest_content_btn = st.button(
            "📝 Suggest Content for My Campaign",
            type="primary",
            use_container_width=True,
            key="suggest_content"
        )
        
        st.markdown("---")
        
        # Performance Comparison Button
        st.markdown("### 📊 Campaign Performance")
        st.caption("See top 3 best & worst campaigns in your context")
        
        compare_performance_btn = st.button(
            "🔍 Compare Best vs Worst Campaigns",
            type="primary",
            use_container_width=True,
            key="compare_performance"
        )
        
        st.markdown("---")
        st.markdown("### 💬 Ask AI About Targeting")
        targeting_question = st.text_area(
            "Your question:",
            placeholder="e.g., Where should I target for festival campaigns?",
            height=100
        )
    
    # Load finder
    with st.spinner("Loading campaign index..."):
        finder = load_finder()
    
    st.success(f"✅ Loaded {finder.index.ntotal:,} campaigns | Model: `{finder.embedding_model}`")
    
    # Handle Content Suggestion Button
    if suggest_content_btn:
        with st.spinner("🧠 Analyzing successful campaigns and generating content suggestions..."):
            content_suggestions = finder.get_content_suggestions(
                region=user_region,
                product=user_product if user_product else None,
                goal=user_goal if user_goal != "Any Goal" else None
            )
            st.session_state['content_suggestions'] = content_suggestions
    
    # Display Content Suggestions if available
    if 'content_suggestions' in st.session_state:
        display_content_suggestions(st.session_state['content_suggestions'])
        if st.button("❌ Clear Content Suggestions", key="clear_content"):
            del st.session_state['content_suggestions']
            st.rerun()
    
    # Handle Performance Comparison Button
    if compare_performance_btn:
        with st.spinner("🧠 Analyzing campaign performance - finding best vs worst..."):
            perf_comparison = finder.get_performance_comparison(
                region=user_region,
                product=user_product if user_product else None,
                goal=user_goal if user_goal != "Any Goal" else None
            )
            st.session_state['perf_comparison'] = perf_comparison
    
    # Display Performance Comparison if available
    if 'perf_comparison' in st.session_state:
        display_campaign_comparison(st.session_state['perf_comparison'])
        if st.button("❌ Clear Performance Comparison", key="clear_comparison"):
            del st.session_state['perf_comparison']
            st.rerun()
    
    st.markdown("---")
    
    # Search input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "🎯 Enter your campaign query:",
            placeholder="e.g., Festival loan campaign for salaried users",
            help="Describe the type of campaign you're looking for"
        )
    
    with col2:
        top_k = st.selectbox("Results", [5, 10, 15, 20], index=0)
    
    # Example queries
    st.markdown("**Quick examples:**")
    example_cols = st.columns(4)
    examples = [
        "Festival loan campaign for salaried users",
        "Credit card upgrade for premium customers",
        "Health insurance for senior citizens",
        "Business loan for SMB owners"
    ]
    
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(example[:30] + "...", key=f"ex_{i}", use_container_width=True):
                query = example
                st.session_state['query'] = example
    
    # Check if query from button click
    if 'query' in st.session_state and not query:
        query = st.session_state['query']
    
    st.markdown("---")
    
    # Search and display results
    if query:
        with st.spinner(f"🔍 Searching for similar campaigns..."):
            results = finder.search(query, top_k=top_k)
        
        if results.empty:
            st.warning("No similar campaigns found. Try a different query.")
        else:
            st.markdown(f"### 📊 Top {len(results)} Similar Campaigns")
            st.markdown(f"Query: **\"{query}\"**")
            
            # Summary metrics
            metric_cols = st.columns(4)
            with metric_cols[0]:
                avg_roi = results['ROI'].mean()
                st.metric("Avg ROI", f"{avg_roi:.1f}")
            with metric_cols[1]:
                st.metric("Campaigns Found", len(results))
            with metric_cols[2]:
                top_similarity = results['Similarity_Score'].iloc[0]
                st.metric("Top Match Score", f"{top_similarity}%")
            with metric_cols[3]:
                channels = results['Channel'].nunique()
                st.metric("Unique Channels", channels)
            
            st.markdown("---")
            
            # Results table
            st.markdown("#### 📋 Results Table")
            
            # Format for display
            display_df = results[['Rank', 'Campaign', 'Product', 'Audience', 'ROI', 'CTR', 'Feedback', 'Similarity_Score', 'Channel', 'Status']].copy()
            display_df.columns = ['#', 'Campaign', 'Product', 'Audience', 'ROI', 'CTR', 'Feedback', 'Match %', 'Channel', 'Status']
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "#": st.column_config.NumberColumn(width="small"),
                    "Campaign": st.column_config.TextColumn(width="large"),
                    "ROI": st.column_config.NumberColumn(format="%.1f"),
                    "Match %": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.1f%%"),
                }
            )
            
            st.markdown("---")
            
            # Detailed cards
            st.markdown("#### 🎯 Detailed Results")
            
            for idx, row in results.iterrows():
                with st.expander(f"**{row['Rank']}. {row['Campaign']}** — Match: {row['Similarity_Score']}%", expanded=(row['Rank'] <= 3)):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**Campaign Details**")
                        st.markdown(f"- **ID:** {row['Campaign_ID']}")
                        st.markdown(f"- **Product:** {row['Product']}")
                        st.markdown(f"- **Audience:** {row['Audience']}")
                        st.markdown(f"- **Objective:** {row['Objective']}")
                    
                    with col2:
                        st.markdown("**Performance**")
                        roi_color = "green" if row['ROI'] > 500 else ("orange" if row['ROI'] > 100 else "red")
                        st.markdown(f"- **ROI:** :{roi_color}[{row['ROI']}]")
                        st.markdown(f"- **CTR:** {row['CTR']}")
                        st.markdown(f"- **Channel:** {row['Channel']}")
                        st.markdown(f"- **Status:** {row['Status']}")
                    
                    with col3:
                        st.markdown("**Feedback Summary**")
                        st.info(row['Feedback'])
            
            # Performance Analysis Section
            st.markdown("---")
            st.markdown("## 📊 Performance Analysis: What Worked vs What Didn't")
            
            perf_col1, perf_col2 = st.columns([2, 1])
            
            with perf_col1:
                if st.button("🔍 Analyze Campaign Performance", type="primary", use_container_width=True):
                    with st.spinner("🧠 Analyzing campaign performance..."):
                        perf_analysis = finder.analyze_campaign_performance(results)
                        st.session_state['perf_analysis'] = perf_analysis
            
            with perf_col2:
                st.caption("💡 Compare top performers vs underperformers")
            
            # Display Performance Analysis
            if 'perf_analysis' in st.session_state:
                display_performance_analysis(st.session_state['perf_analysis'])
                if st.button("❌ Clear Analysis", key="clear_perf"):
                    del st.session_state['perf_analysis']
                    st.rerun()
            
            # Download button
            st.markdown("---")
            csv = results.to_csv(index=False)
            st.download_button(
                "📥 Download Results as CSV",
                csv,
                f"similar_campaigns_{query[:20].replace(' ', '_')}.csv",
                "text/csv",
                use_container_width=True
            )
            
            # AI Recommendations Section
            st.markdown("---")
            st.markdown("## 🤖 AI-Powered Targeting Recommendations")
            
            # Build user context from sidebar inputs
            user_context = {}
            if user_budget:
                user_context['budget'] = user_budget
            if user_region != "All Regions":
                user_context['region'] = user_region
            if user_goal != "Any Goal":
                user_context['goal'] = user_goal
            if user_product:
                user_context['product'] = user_product
            if user_timeline:
                user_context['timeline'] = user_timeline
            
            # Show context if provided
            if user_context:
                st.info(f"📋 Using your context: {', '.join(f'{k}={v}' for k, v in user_context.items())}")
            
            rec_col1, rec_col2 = st.columns([2, 1])
            
            with rec_col1:
                if st.button("🎯 Get AI Targeting Recommendations", type="primary", use_container_width=True):
                    with st.spinner("🧠 Analyzing campaigns and generating recommendations..."):
                        recommendations = finder.get_targeting_recommendations(
                            results, 
                            user_context if user_context else None
                        )
                        st.session_state['recommendations'] = recommendations
            
            with rec_col2:
                st.caption("💡 AI analyzes similar campaigns and feedback to suggest optimal targeting")
            
            # Display recommendations if available
            if 'recommendations' in st.session_state:
                display_recommendations(st.session_state['recommendations'])
            
            # Interactive Q&A Section
            st.markdown("---")
            st.markdown("## 💬 Ask AI About Targeting")
            
            # Check if there's a question from sidebar
            if targeting_question:
                if st.button("🗣️ Ask This Question", use_container_width=True):
                    with st.spinner("🤔 Thinking..."):
                        answer = finder.ask_targeting_question(targeting_question, results)
                        st.session_state['qa_answer'] = answer
                        st.session_state['qa_question'] = targeting_question
            
            if 'qa_answer' in st.session_state:
                st.markdown(f"**Q:** {st.session_state.get('qa_question', 'Your question')}")
                st.markdown(f"**A:** {st.session_state['qa_answer']}")
            
            # Inline question input
            inline_question = st.text_input(
                "Or ask here:",
                placeholder="e.g., Which region has the best conversion rates?",
                key="inline_q"
            )
            if inline_question and st.button("Ask", key="ask_inline"):
                with st.spinner("🤔 Analyzing..."):
                    answer = finder.ask_targeting_question(inline_question, results)
                    st.markdown(f"**Answer:** {answer}")
    
    else:
        # Show placeholder
        st.info("👆 Enter a campaign description above to find similar campaigns from your database.")
        
        # Show some stats about the data
        st.markdown("### 📈 Campaign Database Stats")
        
        if finder.combined_df is not None:
            stat_cols = st.columns(4)
            with stat_cols[0]:
                st.metric("Total Campaigns", f"{len(finder.combined_df):,}")
            with stat_cols[1]:
                st.metric("Products", finder.combined_df['product'].nunique())
            with stat_cols[2]:
                st.metric("Audience Segments", finder.combined_df['audience_segment'].nunique())
            with stat_cols[3]:
                st.metric("Channels", finder.combined_df['channel'].nunique())
            
            # Sample campaigns
            st.markdown("#### 📋 Sample Campaigns")
            sample = finder.combined_df[['campaign_name', 'product', 'audience_segment', 'channel', 'roi']].head(10)
            sample.columns = ['Campaign', 'Product', 'Audience', 'Channel', 'ROI']
            st.dataframe(sample, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
