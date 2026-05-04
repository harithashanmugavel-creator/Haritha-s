"""
Marketing Analytics AI - Synthetic Data Generator
Generates realistic banking marketing campaign datasets for AI-powered analytics solution.

Datasets Generated:
1. campaign_history (10K rows) - Historical campaign intelligence
2. campaign_content (20K rows) - SMS/Email/WhatsApp content for compliance/similarity
3. audience_exposure (50K rows) - Customer fatigue detection data
4. campaign_feedback (20K rows) - Customer complaints and sentiment
5. campaign_roi_metrics (5K rows) - ROI and performance metrics
6. campaign_qa_results (5K rows) - Multi-channel QA validation results
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Output directory
OUTPUT_DIR = "/root/marketing_analytics_ai/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# REFERENCE DATA - Realistic Banking Marketing Categories
# ============================================================================

PRODUCTS = [
    "Personal Loan", "Credit Card", "Savings Account", "Fixed Deposit",
    "Home Loan", "Car Loan", "Education Loan", "Gold Loan",
    "Health Insurance", "Life Insurance", "Mutual Fund", "Demat Account",
    "Business Loan", "Current Account", "NRI Account", "Senior Citizen FD",
    "Credit Card Upgrade", "EMI Card", "Forex Card", "Prepaid Card"
]

AUDIENCE_SEGMENTS = [
    "Salaried Millennials", "Salaried Gen-Z", "HNI Customers", "Mass Affluent",
    "Students", "SMB Owners", "Retired Professionals", "Self-Employed",
    "Government Employees", "IT Professionals", "Healthcare Workers",
    "First-Time Borrowers", "Existing Loan Customers", "Premium Card Holders",
    "Dormant Account Holders", "High-Value Transactors", "Low-Balance Customers",
    "NRI Customers", "Women Professionals", "Senior Citizens"
]

REGIONS = [
    "Mumbai", "Delhi NCR", "Bangalore", "Chennai", "Hyderabad",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Chandigarh", "Kochi", "Coimbatore", "Indore", "Nagpur",
    "North India", "South India", "West India", "East India", "Pan India"
]

CHANNELS = ["SMS", "Email", "WhatsApp", "Push Notification", "Call Center"]

CAMPAIGN_STATUSES = ["Completed", "Active", "Paused", "Scheduled", "Cancelled"]

TONES = ["Promotional", "Informational", "Urgent", "Personalized", "Festive", "Reminder", "Educational"]

CTA_OPTIONS = [
    "Apply Now", "Know More", "Claim Offer", "Activate Now", "Upgrade Today",
    "Get Started", "Check Eligibility", "Book Appointment", "Download App",
    "Call Us", "Visit Branch", "Limited Time Offer", "Enroll Now"
]

COMPLIANCE_RISKS = ["Low", "Medium", "High", "Critical"]

SENTIMENTS = ["Positive", "Neutral", "Negative", "Very Negative"]

ISSUE_CATEGORIES = [
    "Spam/Excessive Messages", "Irrelevant Offers", "Misleading Information",
    "Technical Issues", "Poor Timing", "Privacy Concerns", "Unsubscribe Failed",
    "Duplicate Messages", "Wrong Customer Details", "Aggressive Sales",
    "Unclear Terms", "Hidden Charges", "App Issues", "Service Delay"
]

SEVERITIES = ["Low", "Medium", "High", "Critical"]

QA_STATUSES = ["Pass", "Warning", "Fail"]

# ============================================================================
# MESSAGE TEMPLATES - Realistic Banking Marketing Content
# ============================================================================

PROMOTIONAL_TEMPLATES = {
    "Personal Loan": [
        "Get instant personal loans up to ₹50L at just {rate}% p.a.! No collateral needed. Apply now: {link}",
        "Pre-approved personal loan waiting for you! Up to ₹25L at attractive rates. Limited period offer.",
        "Festive personal loan at lowest EMI ever! Approval in 2 mins. Check eligibility now.",
        "Dear Customer, your pre-approved loan of ₹{amount}L is ready. Interest starting {rate}% p.a. Apply today!",
        "Need funds urgently? Get personal loan disbursed in 24 hours. No documentation hassle!",
    ],
    "Credit Card": [
        "Upgrade to our Premium Credit Card and get {reward}X reward points + airport lounge access!",
        "Exclusive: Your credit limit increased to ₹{limit}L! Enjoy more shopping freedom.",
        "Activate your new credit card and get ₹{cashback} cashback on first transaction!",
        "Credit Card bill payment due? Convert to easy EMI at 0% interest for 3 months.",
        "Flash Sale! Get {discount}% cashback on all online purchases this weekend!",
    ],
    "Savings Account": [
        "Open Zero Balance Savings Account online in 5 minutes! Earn up to {rate}% interest.",
        "Refer & Earn: Get ₹{amount} for every successful savings account referral!",
        "Senior Citizen Savings Account: Higher interest rates + priority banking services.",
        "Salary Account upgrade available! Enjoy premium benefits at no extra cost.",
    ],
    "Fixed Deposit": [
        "FD rates increased! Earn up to {rate}% p.a. on fixed deposits. Invest now!",
        "Senior Citizen FD: Extra {bonus}% interest rate. Lock in high returns today!",
        "Tax-saving FD under 80C: Save up to ₹46,800 in taxes. Start with ₹{min}.",
        "Flexi FD with premature withdrawal facility. Best rates guaranteed!",
    ],
    "Home Loan": [
        "Dream home within reach! Home loan at {rate}% p.a. + zero processing fee.",
        "Home loan balance transfer: Save up to ₹{savings}L on interest!",
        "Special home loan rates for women borrowers: {rate}% p.a. Apply today!",
        "Pre-approved home loan up to ₹{amount}Cr waiting for you. Check now!",
    ],
    "Insurance": [
        "Secure your family's future! Life insurance at ₹{premium}/day. Get covered now.",
        "Health insurance renewal due: Upgrade plan for better coverage at same premium!",
        "Term insurance with ₹1Cr cover at just ₹{premium}/month. No medical tests required!",
        "Critical illness cover: Protect against 40+ diseases. Premium starting ₹{premium}/month.",
    ],
    "Mutual Fund": [
        "Start SIP with just ₹500/month! Build wealth systematically. Invest now.",
        "Tax-saving ELSS funds: Save taxes + grow wealth. Invest before deadline!",
        "Your portfolio review is due. Book free consultation with our expert.",
        "NFO Alert: New fund launch with excellent growth potential. Invest early!",
    ],
    "Generic": [
        "Exclusive offer for our valued customers! {discount}% off on all products this festive season.",
        "Banking made easy! Download our app for seamless transactions & exclusive offers.",
        "Your account review is pending. Visit nearest branch for premium benefits.",
        "Congratulations! You're pre-approved for multiple products. Check eligibility now!",
    ]
}

COMPLAINT_TEMPLATES = [
    "Too many promotional SMS from your bank. Please stop sending these messages!",
    "I've already unsubscribed but still receiving marketing calls. Very frustrating!",
    "The offer mentioned in SMS is not applicable to my account. Misleading information!",
    "Received 5 promotional messages today alone. This is harassment!",
    "Your executive called me during office hours for loan offer. Very unprofessional!",
    "The interest rate in SMS was different from what your branch quoted. Cheating!",
    "I opted out of marketing communications but still getting WhatsApp promotions.",
    "The credit card offer was not as mentioned. Hidden charges everywhere!",
    "Your app showed pre-approved loan but branch rejected. False advertising!",
    "Loan processing fee was higher than mentioned in campaign. Please clarify!",
    "Multiple calls from different executives for same product. Poor coordination!",
    "Campaign said instant approval but waiting for 5 days now. False promise!",
    "The cashback promised in campaign never got credited. Follow up required.",
    "Email said exclusive offer but everyone got the same. Not really exclusive!",
    "Your push notification timing is terrible. Getting messages at midnight!",
    "The EMI calculator in campaign shows different amount than actual EMI.",
    "Promotional message language was different from my preference. Update records!",
    "I'm not interested in loans but keep getting loan offers. Wrong targeting!",
    "The offer expired but I still received promotional SMS for it. Waste of time!",
    "Your campaign mentioned free insurance but it had premium after first year.",
    "Credit limit mentioned in message doesn't match my actual approved limit.",
    "Keep getting duplicate messages on both SMS and WhatsApp. Very annoying!",
    "The special rate for existing customers was same as new customer rate. Disappointed!",
    "App crashed when I tried to avail the campaign offer. Losing trust!",
    "Your WhatsApp Business messages are too frequent. Considering blocking!",
]

POSITIVE_FEEDBACK_TEMPLATES = [
    "Great offer on personal loan! Applied and got approval within hours. Impressed!",
    "The credit card upgrade offer was excellent. Enjoying the new benefits!",
    "Timely SMS about FD rate increase helped me invest at the right time. Thanks!",
    "Your WhatsApp banking is very convenient. Love the quick response!",
    "The festive offer on home loan saved me a lot on processing fees. Happy customer!",
    "Campaign offer was exactly as mentioned. No hidden charges. Trustworthy!",
    "Received personalized offer matching my needs. Good targeting!",
    "The app notification for bill payment reminder was helpful. Avoided late fee!",
]

CAMPAIGN_NAME_TEMPLATES = [
    "{season} {product} Fest", "{product} Special Offer", "{audience} {product} Campaign",
    "Pre-Approved {product} Drive", "{region} {product} Push", "Instant {product} Promo",
    "{month} {product} Bonanza", "Premium {product} Upgrade", "{product} Flash Sale",
    "Exclusive {product} Deal", "{festival} {product} Offer", "{product} EMI Special",
    "{product} Zero Cost", "Limited Period {product}", "{audience} Exclusive {product}"
]

SEASONS = ["Summer", "Monsoon", "Festive", "Winter", "Year-End", "Q1", "Q2", "Q3", "Q4"]
MONTHS = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
FESTIVALS = ["Diwali", "Holi", "Navratri", "Dussehra", "Christmas", "New Year", 
             "Independence Day", "Republic Day", "Eid", "Onam", "Pongal", "Ugadi"]

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_campaign_id(index):
    return f"CMP{10001 + index}"

def generate_content_id(index):
    return f"CNT{90001 + index}"

def generate_exposure_id(index):
    return f"EXP{20001 + index}"

def generate_feedback_id(index):
    return f"FB{30001 + index}"

def generate_metric_id(index):
    return f"ROI{40001 + index}"

def generate_qa_id(index):
    return f"QA{50001 + index}"

def generate_campaign_name():
    template = random.choice(CAMPAIGN_NAME_TEMPLATES)
    return template.format(
        season=random.choice(SEASONS),
        product=random.choice(PRODUCTS),
        audience=random.choice(AUDIENCE_SEGMENTS).split()[0],
        region=random.choice(REGIONS[:10]),
        month=random.choice(MONTHS),
        festival=random.choice(FESTIVALS)
    )

def generate_marketing_content(product, channel):
    """Generate realistic marketing message based on product and channel."""
    # Get templates for the product category
    product_key = product if product in PROMOTIONAL_TEMPLATES else "Generic"
    for key in PROMOTIONAL_TEMPLATES.keys():
        if key in product:
            product_key = key
            break
    
    templates = PROMOTIONAL_TEMPLATES.get(product_key, PROMOTIONAL_TEMPLATES["Generic"])
    template = random.choice(templates)
    
    # Fill in template variables
    content = template.format(
        rate=round(random.uniform(8.5, 16.5), 1),
        link="bit.ly/bank-offer",
        amount=random.randint(5, 50),
        reward=random.randint(2, 10),
        limit=random.randint(1, 10),
        cashback=random.randint(200, 2000),
        discount=random.randint(5, 25),
        bonus=round(random.uniform(0.25, 0.75), 2),
        min=random.choice([5000, 10000, 15000]),
        savings=random.randint(2, 15),
        premium=random.randint(15, 100)
    )
    
    # Adjust length based on channel
    if channel == "SMS" and len(content) > 160:
        content = content[:157] + "..."
    
    return content

def generate_date_range(start_date, end_date):
    """Generate random date within range."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# ============================================================================
# DATASET 1: campaign_history (10K rows)
# ============================================================================

def generate_campaign_history(n_rows=10000):
    print(f"Generating campaign_history ({n_rows} rows)...")
    
    data = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 4, 30)
    
    for i in range(n_rows):
        launch_date = generate_date_range(start_date, end_date)
        channel = random.choice(CHANNELS)
        product = random.choice(PRODUCTS)
        
        # Generate correlated metrics
        base_ctr = np.random.uniform(1.5, 12.0)
        # WhatsApp tends to perform better
        if channel == "WhatsApp":
            base_ctr *= 1.3
        elif channel == "SMS":
            base_ctr *= 0.85
        
        spend = random.randint(50000, 5000000)
        impressions = spend * random.randint(3, 15)
        clicks = int(impressions * base_ctr / 100)
        conversions = int(clicks * random.uniform(0.05, 0.25))
        
        revenue = conversions * random.randint(5000, 50000)
        roi = round((revenue - spend) / spend, 2) if spend > 0 else 0
        
        data.append({
            "campaign_id": generate_campaign_id(i),
            "campaign_name": generate_campaign_name(),
            "product": product,
            "audience_segment": random.choice(AUDIENCE_SEGMENTS),
            "region": random.choice(REGIONS),
            "channel": channel,
            "launch_date": launch_date.strftime("%Y-%m-%d"),
            "end_date": (launch_date + timedelta(days=random.randint(7, 90))).strftime("%Y-%m-%d"),
            "spend_amount": spend,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "ctr": round(base_ctr, 2),
            "conversion_rate": round(conversions / clicks * 100 if clicks > 0 else 0, 2),
            "revenue_generated": revenue,
            "roi": roi,
            "campaign_status": random.choice(CAMPAIGN_STATUSES),
            "campaign_objective": random.choice(["Acquisition", "Retention", "Upsell", "Cross-sell", "Re-engagement", "Brand Awareness"]),
            "target_audience_size": random.randint(10000, 5000000),
            "actual_reach": random.randint(5000, 3000000)
        })
    
    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}/campaign_history.csv", index=False)
    print(f"  Saved: {OUTPUT_DIR}/campaign_history.csv")
    return df

# ============================================================================
# DATASET 2: campaign_content (20K rows)
# ============================================================================

def generate_campaign_content(campaign_df, n_rows=20000):
    print(f"Generating campaign_content ({n_rows} rows)...")
    
    data = []
    campaign_ids = campaign_df["campaign_id"].tolist()
    campaign_products = dict(zip(campaign_df["campaign_id"], campaign_df["product"]))
    
    for i in range(n_rows):
        campaign_id = random.choice(campaign_ids)
        channel = random.choice(CHANNELS)
        product = campaign_products.get(campaign_id, random.choice(PRODUCTS))
        
        content_text = generate_marketing_content(product, channel)
        
        # Determine compliance risk based on content
        compliance_risk = "Low"
        risky_words = ["guaranteed", "100%", "instant approval", "no risk", "free forever", "unlimited"]
        if any(word in content_text.lower() for word in risky_words):
            compliance_risk = random.choice(["Medium", "High"])
        
        # More aggressive tones have higher compliance risk
        tone = random.choice(TONES)
        if tone in ["Urgent", "Promotional"] and compliance_risk == "Low":
            compliance_risk = random.choices(["Low", "Medium"], weights=[0.7, 0.3])[0]
        
        data.append({
            "content_id": generate_content_id(i),
            "campaign_id": campaign_id,
            "channel": channel,
            "content_text": content_text,
            "tone": tone,
            "cta": random.choice(CTA_OPTIONS),
            "compliance_risk": compliance_risk,
            "language": random.choices(
                ["English", "Hindi", "Tamil", "Telugu", "Marathi", "Bengali", "Kannada"],
                weights=[0.5, 0.25, 0.05, 0.05, 0.05, 0.05, 0.05]
            )[0],
            "character_count": len(content_text),
            "has_link": "bit.ly" in content_text or "link" in content_text.lower(),
            "has_offer_amount": "₹" in content_text,
            "created_date": generate_date_range(datetime(2023, 1, 1), datetime(2026, 4, 30)).strftime("%Y-%m-%d"),
            "version": random.randint(1, 5),
            "ab_variant": random.choice(["A", "B", "C", "Control"])
        })
    
    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}/campaign_content.csv", index=False)
    print(f"  Saved: {OUTPUT_DIR}/campaign_content.csv")
    return df

# ============================================================================
# DATASET 3: audience_exposure (50K rows)
# ============================================================================

def generate_audience_exposure(campaign_df, n_rows=50000):
    print(f"Generating audience_exposure ({n_rows} rows)...")
    
    data = []
    campaign_ids = campaign_df["campaign_id"].tolist()
    
    for i in range(n_rows):
        campaign_id = random.choice(campaign_ids)
        segment = random.choice(AUDIENCE_SEGMENTS)
        channel = random.choice(CHANNELS)
        
        exposure_count_7d = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            weights=[0.2, 0.25, 0.2, 0.15, 0.08, 0.05, 0.03, 0.02, 0.01, 0.01]
        )[0]
        
        exposure_count_30d = exposure_count_7d + random.randint(0, 15)
        
        # Fatigue score increases with exposure
        base_fatigue = exposure_count_7d * 0.1
        fatigue_score = min(1.0, base_fatigue + random.uniform(-0.1, 0.2))
        
        data.append({
            "exposure_id": generate_exposure_id(i),
            "customer_segment": segment,
            "campaign_id": campaign_id,
            "channel": channel,
            "exposure_date": generate_date_range(datetime(2023, 1, 1), datetime(2026, 4, 30)).strftime("%Y-%m-%d"),
            "exposure_count_last_7_days": exposure_count_7d,
            "exposure_count_last_30_days": exposure_count_30d,
            "fatigue_score": round(fatigue_score, 2),
            "opt_out_risk": round(fatigue_score * random.uniform(0.5, 1.2), 2),
            "engagement_rate": round(max(0, (1 - fatigue_score) * random.uniform(0.5, 1.0) * 15), 2),
            "last_interaction_days": random.randint(0, 90),
            "preferred_channel": random.choice(CHANNELS),
            "best_contact_time": random.choice(["Morning", "Afternoon", "Evening", "Night"]),
            "customer_lifetime_value_segment": random.choice(["High", "Medium", "Low"]),
            "churn_risk_score": round(random.uniform(0, 1), 2)
        })
    
    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}/audience_exposure.csv", index=False)
    print(f"  Saved: {OUTPUT_DIR}/audience_exposure.csv")
    return df

# ============================================================================
# DATASET 4: campaign_feedback (20K rows)
# ============================================================================

def generate_campaign_feedback(campaign_df, n_rows=20000):
    print(f"Generating campaign_feedback ({n_rows} rows)...")
    
    data = []
    campaign_ids = campaign_df["campaign_id"].tolist()
    
    for i in range(n_rows):
        # 70% negative, 15% neutral, 15% positive (realistic for complaint data)
        sentiment_choice = random.choices(
            ["Negative", "Very Negative", "Neutral", "Positive"],
            weights=[0.45, 0.25, 0.15, 0.15]
        )[0]
        
        if sentiment_choice in ["Negative", "Very Negative"]:
            feedback_text = random.choice(COMPLAINT_TEMPLATES)
            issue_category = random.choice(ISSUE_CATEGORIES)
            severity = random.choices(
                SEVERITIES,
                weights=[0.2, 0.4, 0.3, 0.1] if sentiment_choice == "Negative" else [0.1, 0.2, 0.4, 0.3]
            )[0]
        elif sentiment_choice == "Positive":
            feedback_text = random.choice(POSITIVE_FEEDBACK_TEMPLATES)
            issue_category = "Appreciation"
            severity = "Low"
        else:
            feedback_text = "General inquiry about the campaign offer."
            issue_category = "General Inquiry"
            severity = "Low"
        
        data.append({
            "feedback_id": generate_feedback_id(i),
            "campaign_id": random.choice(campaign_ids),
            "feedback_text": feedback_text,
            "sentiment": sentiment_choice,
            "sentiment_score": round(
                random.uniform(-1, -0.3) if sentiment_choice == "Very Negative"
                else random.uniform(-0.3, 0) if sentiment_choice == "Negative"
                else random.uniform(0, 0.3) if sentiment_choice == "Neutral"
                else random.uniform(0.3, 1), 2
            ),
            "issue_category": issue_category,
            "severity": severity,
            "feedback_source": random.choice(["App Review", "Survey", "Call Center", "Email", "Social Media", "Chatbot", "Branch"]),
            "feedback_date": generate_date_range(datetime(2023, 1, 1), datetime(2026, 4, 30)).strftime("%Y-%m-%d"),
            "resolution_status": random.choice(["Open", "In Progress", "Resolved", "Escalated", "Closed"]),
            "response_time_hours": random.randint(1, 168) if random.random() > 0.2 else None,
            "customer_segment": random.choice(AUDIENCE_SEGMENTS),
            "channel_of_campaign": random.choice(CHANNELS),
            "repeat_complaint": random.choices([True, False], weights=[0.3, 0.7])[0],
            "escalation_required": severity in ["High", "Critical"]
        })
    
    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}/campaign_feedback.csv", index=False)
    print(f"  Saved: {OUTPUT_DIR}/campaign_feedback.csv")
    return df

# ============================================================================
# DATASET 5: campaign_roi_metrics (5K rows)
# ============================================================================

def generate_campaign_roi_metrics(campaign_df, n_rows=5000):
    print(f"Generating campaign_roi_metrics ({n_rows} rows)...")
    
    # Use subset of campaigns for detailed ROI metrics
    selected_campaigns = campaign_df.sample(min(n_rows, len(campaign_df)), replace=n_rows > len(campaign_df))
    
    data = []
    for i, (_, campaign) in enumerate(selected_campaigns.iterrows()):
        impressions = campaign["impressions"]
        clicks = campaign["clicks"]
        conversions = campaign["conversions"]
        spend = campaign["spend_amount"]
        revenue = campaign["revenue_generated"]
        
        # Add some variation
        impressions = int(impressions * random.uniform(0.9, 1.1))
        
        data.append({
            "metric_id": generate_metric_id(i),
            "campaign_id": campaign["campaign_id"],
            "measurement_date": generate_date_range(datetime(2023, 1, 1), datetime(2026, 4, 30)).strftime("%Y-%m-%d"),
            "impressions": impressions,
            "unique_impressions": int(impressions * random.uniform(0.6, 0.9)),
            "clicks": clicks,
            "unique_clicks": int(clicks * random.uniform(0.7, 0.95)),
            "conversions": conversions,
            "conversion_value": conversions * random.randint(5000, 50000),
            "acquisition_cost": spend,
            "cost_per_click": round(spend / clicks if clicks > 0 else 0, 2),
            "cost_per_conversion": round(spend / conversions if conversions > 0 else 0, 2),
            "revenue_generated": revenue,
            "profit": revenue - spend,
            "roi_score": round((revenue - spend) / spend * 100 if spend > 0 else 0, 2),
            "roas": round(revenue / spend if spend > 0 else 0, 2),
            "customer_acquisition_cost": round(spend / conversions if conversions > 0 else 0, 2),
            "lifetime_value_generated": conversions * random.randint(50000, 500000),
            "attribution_model": random.choice(["Last Click", "First Click", "Linear", "Time Decay", "Position Based"]),
            "benchmark_roi": round(random.uniform(1.5, 5.0), 2),
            "performance_vs_benchmark": random.choice(["Above", "At", "Below"])
        })
    
    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}/campaign_roi_metrics.csv", index=False)
    print(f"  Saved: {OUTPUT_DIR}/campaign_roi_metrics.csv")
    return df

# ============================================================================
# DATASET 6: campaign_qa_results (5K rows)
# ============================================================================

def generate_campaign_qa_results(campaign_df, n_rows=5000):
    print(f"Generating campaign_qa_results ({n_rows} rows)...")
    
    data = []
    campaign_ids = campaign_df["campaign_id"].tolist()
    
    mismatch_reasons = [
        "Aggressive wording detected",
        "CTA differs across channels",
        "Offer amount inconsistent",
        "Disclaimer missing",
        "Interest rate not compliant",
        "Terms and conditions unclear",
        "Expiry date mismatch",
        "Product name variation",
        "Contact information different",
        "Brand guidelines violation",
        "Regulatory language missing",
        "Font/formatting issues",
        None  # No issues
    ]
    
    for i in range(n_rows):
        # Generate correlated QA results
        base_quality = random.random()
        
        tone_consistency = "Pass" if base_quality > 0.3 else random.choice(["Warning", "Fail"])
        cta_alignment = "Pass" if base_quality > 0.25 else random.choice(["Warning", "Fail"])
        compliance_status = "Pass" if base_quality > 0.35 else random.choice(["Warning", "Fail"])
        
        has_issues = tone_consistency != "Pass" or cta_alignment != "Pass" or compliance_status != "Pass"
        
        data.append({
            "qa_id": generate_qa_id(i),
            "campaign_id": random.choice(campaign_ids),
            "qa_date": generate_date_range(datetime(2023, 1, 1), datetime(2026, 4, 30)).strftime("%Y-%m-%d"),
            "tone_consistency": tone_consistency,
            "cta_alignment": cta_alignment,
            "compliance_status": compliance_status,
            "brand_guidelines_check": "Pass" if base_quality > 0.2 else random.choice(["Warning", "Fail"]),
            "disclaimer_present": random.choices([True, False], weights=[0.85, 0.15])[0],
            "regulatory_compliance": "Pass" if base_quality > 0.4 else random.choice(["Warning", "Fail"]),
            "mismatch_reason": random.choice(mismatch_reasons[:-1]) if has_issues else None,
            "overall_qa_score": round(base_quality * 100, 1),
            "channels_reviewed": random.randint(2, 5),
            "issues_found": random.randint(0, 5) if has_issues else 0,
            "critical_issues": random.randint(0, 2) if compliance_status == "Fail" else 0,
            "reviewer_notes": "Needs revision" if compliance_status == "Fail" else "Approved" if compliance_status == "Pass" else "Minor fixes required",
            "approval_status": "Rejected" if compliance_status == "Fail" else "Approved" if base_quality > 0.5 else "Conditional",
            "revision_count": random.randint(0, 3),
            "time_to_approve_hours": random.randint(2, 72)
        })
    
    df = pd.DataFrame(data)
    df.to_csv(f"{OUTPUT_DIR}/campaign_qa_results.csv", index=False)
    print(f"  Saved: {OUTPUT_DIR}/campaign_qa_results.csv")
    return df

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 70)
    print("Marketing Analytics AI - Synthetic Data Generator")
    print("=" * 70)
    print()
    
    # Generate all datasets
    campaign_df = generate_campaign_history(10000)
    print()
    
    generate_campaign_content(campaign_df, 20000)
    print()
    
    generate_audience_exposure(campaign_df, 50000)
    print()
    
    generate_campaign_feedback(campaign_df, 20000)
    print()
    
    generate_campaign_roi_metrics(campaign_df, 5000)
    print()
    
    generate_campaign_qa_results(campaign_df, 5000)
    print()
    
    print("=" * 70)
    print("Data generation complete!")
    print(f"All files saved to: {OUTPUT_DIR}")
    print("=" * 70)
    
    # Summary
    print("\nDataset Summary:")
    print("-" * 50)
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith('.csv'):
            df = pd.read_csv(f"{OUTPUT_DIR}/{file}")
            print(f"  {file}: {len(df):,} rows, {len(df.columns)} columns")

if __name__ == "__main__":
    main()
