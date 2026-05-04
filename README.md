<div align="center">

# 🛡️ OptiGuard AI

### AI-Powered Marketing Campaign Intelligence & Risk Prediction Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4-0078D4.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Predict campaign failures before they happen. Optimize marketing ROI with AI.**

[Problem Statement](#-strategic-problem-statement) • [Architecture](#-optiguard-architecture) • [Features](#-key-features--outputs) • [Flow Diagram](#-system-flow-diagram)

</div>

---

## 🚨 Strategic Problem Statement

### Voice of the Customer

> *"Repeated calls from HDFC bank... registered for DND since more than 3 years... harassing for personal loan offers."*
> 
> **Escalation:** Public grievance platform (Day 5 of campaign)

> *"It's Diwali week. A salaried customer receives 14 loan SMSes, 6 WhatsApp messages, and 3 calls in 4 days. By Day 5, he files a formal complaint."*

### Real-World Campaign Failures

| Scenario | Complaints / Impact | Operational Pain Point |
|----------|---------------------|------------------------|
| **Diwali Rush** | 8,500+ TRAI DND Filings | **Fatigue:** Cross-channel silos hitting same user 5x/week. No unified view of targeting overlap |
| **Senior Insurance** | 4,300+ Ombudsman Cases | **Trust Risk:** Compliance disconnect; misleading jargon causing friction and elderly mis-selling |
| **NRI Wealth** | 1,200+ Opt-out Reports | **Relevance:** Blanket targeting leading to brand blindness. Poor offshore channel strategy |
| **SME Loans** | 2,100+ Ignored Leads | **Timing:** Inability to detect low cash-flow cycles. Wasted spend on high-friction windows |
| **Gen-Z Credit** | 3,400+ Ethics Audits | **Tone:** Disconnect between traditional ads and digital-first values. "Hidden Fee" alerts |

### The Cost of Inaction

<div align="center">

| ₹7.2 Cr | 48,000 | 30-40% |
|:-------:|:------:|:------:|
| **ANNUAL OVERHEAD** | **ANALYST HOURS/YR** | **OPT-OUT RISK** |

</div>

### 🎯 THE MISSION

> **To prevent these 20,000+ registered grievances through an AI "Copilot" layer that simulates campaign risk before the first SMS is deployed.**

---

## 🏗️ OptiGuard Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    USER LAYER                                            │
│                     Marketing Operations Team & Stakeholders                             │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │  Compliance Officer │  │  CMO / Marketing    │  │  Campaign Manager   │              │
│  │                     │  │       Lead          │  │                     │              │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                                          │
│                              Streamlit Web Apps                                          │
│  ┌──────────────────────────────────┐  ┌──────────────────────────────────────────────┐ │
│  │     OptiGuard AI Solution        │  │           Control Tower UI                   │ │
│  │   risk_intelligence_app.py       │  │        control_tower_app.py                  │ │
│  │   • Gauges & Simulations         │  │   • Monitoring & Oversight                   │ │
│  └──────────────────────────────────┘  └──────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────┐                                                   │
│  │    Similar Campaign Finder       │                                                   │
│  │          app.py                  │                                                   │
│  │   • Search + Content Suggest     │                                                   │
│  └──────────────────────────────────┘                                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER - REASONING ENGINE                                 │
│  ┌────────────────────────────────────┐  ┌────────────────────────────────────────────┐ │
│  │      Marketing Intelligence        │  │        Similar Campaign Finder             │ │
│  │      (CampaignRiskPredictor)       │  │        (SimilarCampaignFinder)             │ │
│  │  ✓ Campaign Health Score           │  │  ✓ Semantic Search                         │ │
│  │  ✓ Risk Factors Analysis           │  │  ✓ Compare Campaigns                       │ │
│  │  ✓ Audience Playbook               │  │  ✓ AI Recommendations                      │ │
│  │  ✓ Executive Summary               │  │  ✓ Content Suggestions                     │ │
│  │  ✓ Contextual Chat                 │  │  ✓ Intent Mapping                          │ │
│  └────────────────────────────────────┘  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              AI INFRASTRUCTURE                                           │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│  │       VECTOR STORAGE            │  │              AI MODELS                       │   │
│  │  FAISS / metadata_idx           │  │  GPT-Class LLM (RAG)                        │   │
│  │  campaign_index.faiss           │  │  text-embedding-3-small                     │   │
│  └─────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         APP CORE                                                  │   │
│  │               Contextual Router & Orchestrator Hub                                │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER (.CSV)                                           │
│                         110K+ rows of synthetic banking data                             │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐                │
│  │campaign_qa    │ │campaign_roi   │ │campaign       │ │audience       │                │
│  │_results.csv   │ │_metrics.csv   │ │_feedback.csv  │ │_exposure.csv  │                │
│  │   5K rows     │ │   5K rows     │ │   20K rows    │ │   50K rows    │                │
│  └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘                │
│  ┌───────────────┐ ┌───────────────┐                                                    │
│  │campaign       │ │campaign       │                                                    │
│  │_content.csv   │ │_history.csv   │                                                    │
│  │   20K rows    │ │   10K rows    │                                                    │
│  └───────────────┘ └───────────────┘                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 System Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    DATA LAYER                                                 │
│                            110K+ rows of synthetic banking data                               │
│                                                                                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│  │campaign_qa  │ │campaign_roi │ │campaign     │ │audience     │ │campaign     │ │campaign ││
│  │_results.csv │ │_metrics.csv │ │_feedback.csv│ │_exposure.csv│ │_content.csv │ │_history ││
│  │  5K rows    │ │  5K rows    │ │  20K rows   │ │  50K rows   │ │  20K rows   │ │ 10K rows││
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └────┬────┘│
└─────────┼───────────────┼───────────────┼───────────────┼───────────────┼─────────────┼─────┘
          │               │               │               │               │             │
          └───────────────┴───────────────┴───────┬───────┴───────────────┴─────────────┘
                                                  │
                                                  ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                              INTELLIGENCE LAYER - Core Engines                                │
│                                                                                               │
│  ┌─────────────────────────────────────┐    ┌─────────────────────────────────────────────┐  │
│  │       CampaignRiskPredictor         │    │           SimilarCampaignFinder             │  │
│  │  • Health Score (0-100)             │    │  • Semantic Search                          │  │
│  │  • Risk Factor Breakdown            │    │  • Content Suggestions                      │  │
│  │  • Audience Playbook                │    │  • Best vs Worst Compare                    │  │
│  │  • Executive Summary                │    │  • Targeting Recommender                    │  │
│  │  • Contextual Chat                  │    │                                             │  │
│  └──────────────────┬──────────────────┘    └─────────────────────┬───────────────────────┘  │
└─────────────────────┼─────────────────────────────────────────────┼──────────────────────────┘
                      │                                             │
                      │         ┌───────────────────────────────────┘
                      │         │           Ingest + Embed
                      ▼         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AI / ML SERVICES                                            │
│                                                                                               │
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────────────────────┐  │
│  │     text-embedding-3-small      │    │              RAG Orchestrator                   │  │
│  │       (Vector Embedding)        │───▶│        (Retrieve → Augment → Generate)          │  │
│  └─────────────────────────────────┘    └──────────────────────┬──────────────────────────┘  │
│                                                                │                              │
│                                                                ▼                              │
│                                         ┌─────────────────────────────────────────────────┐  │
│                                         │              GPT-class LLM                      │  │
│                                         │  (Insights, Compliance, Summarization, Chat)    │  │
│                                         └─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                              VECTOR & MEMORY STORE                                            │
│                                                                                               │
│               ┌─────────────────────────────┐    ┌─────────────────────────────┐             │
│               │        FAISS Index          │    │      Metadata Pickle        │             │
│               │   campaign_index.faiss      │    │   campaign_metadata.pkl     │             │
│               │      10K+ Campaigns         │    │                             │             │
│               └─────────────────────────────┘    └─────────────────────────────┘             │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  OUTPUTS DELIVERED                                            │
│                                                                                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │  Campaign    │ │    Risk      │ │  Predicted   │ │ Channel &    │ │  Compliance  │        │
│  │Health Score  │ │   Factors    │ │ Reductions   │ │  Audience    │ │    Flags     │        │
│  │ 0-100 gauge  │ │Fatigue+Trust │ │ Opt-out ↓    │ │  Playbook    │ │ Safer Wording│        │
│  │              │ │Channel+Tone  │ │ Complaints ↓ │ │              │ │              │        │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘        │
│  ┌──────────────┐                                                                            │
│  │  Executive   │                                                                            │
│  │  Narrative   │                                                                            │
│  │ + Live Signals│                                                                           │
│  └──────────────┘                                                                            │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Features & Outputs

### 1. 🏥 Campaign Health Score

**What it does:** Generates a real-time health score (0-100) for any campaign configuration before launch.

**How it works:**
- Analyzes historical performance data across similar campaigns
- Evaluates audience fatigue levels from exposure data
- Cross-references complaint patterns and feedback sentiment
- Produces a composite risk-adjusted health score

**Output:**
```
┌─────────────────────────────────────────┐
│         CAMPAIGN HEALTH SCORE           │
│                                         │
│              ┌───────┐                  │
│              │  72   │ ← Score Gauge    │
│              └───────┘                  │
│           MODERATE RISK                 │
│                                         │
│  ✓ Audience: Salaried Millennials       │
│  ✓ Channel: SMS + WhatsApp              │
│  ✓ Product: Personal Loan               │
│  ⚠ Fatigue Risk: 34%                    │
└─────────────────────────────────────────┘
```

---

### 2. ⚠️ Risk Factor Breakdown

**What it does:** Breaks down campaign risk into four critical dimensions with percentage scores.

**Risk Dimensions:**
| Factor | Description | Trigger Examples |
|--------|-------------|------------------|
| **Fatigue Risk** | Customer over-communication likelihood | 5+ messages/week to same segment |
| **Trust Risk** | Brand trust erosion probability | Misleading offers, jargon overload |
| **Channel Risk** | Channel-audience mismatch | SMS to Gen-Z, Email to elderly |
| **Tone Risk** | Message tone inconsistency | Aggressive CTAs, hidden fees |

**Output:**
```
┌─────────────────────────────────────────┐
│          RISK FACTOR BREAKDOWN          │
│                                         │
│  Fatigue Risk    ████████░░░░  68%  🔴  │
│  Trust Risk      ██████░░░░░░  45%  🟡  │
│  Channel Risk    ████░░░░░░░░  32%  🟢  │
│  Tone Risk       ███░░░░░░░░░  28%  🟢  │
│                                         │
│  ⚠ PRIMARY CONCERN: Fatigue Risk        │
│  Segment received 4 campaigns this week │
└─────────────────────────────────────────┘
```

---

### 3. 📉 Predicted Reductions

**What it does:** Predicts potential negative outcomes if campaign launches without optimization.

**Predictions Include:**
- **Opt-out Probability:** Likelihood of customers unsubscribing
- **Complaint Likelihood:** Expected complaint volume increase
- **Engagement Drop:** Predicted CTR/conversion decline

**Output:**
```
┌─────────────────────────────────────────┐
│        PREDICTED REDUCTIONS             │
│        (If launched as-is)              │
│                                         │
│  📉 Opt-out Risk:     +23% ↑            │
│  📉 Complaints:       +180 expected     │
│  📉 Engagement:       -15% CTR          │
│  📉 Trust Score:      -8 points         │
│                                         │
│  💰 PROJECTED LOSS: ₹4.2L wasted spend  │
└─────────────────────────────────────────┘
```

---

### 4. 📋 Channel & Audience Playbook

**What it does:** AI-generated recommendations for optimal targeting strategy.

**Recommendations:**
- ✅ **Recommended Audiences:** High-ROI segments with reasons
- ⛔ **Audiences to Avoid:** Fatigued or low-performing segments
- 📢 **Best Channels:** Channel-segment match recommendations
- ⏰ **Optimal Timing:** Best days/times based on historical data

**Output:**
```
┌─────────────────────────────────────────┐
│      CHANNEL & AUDIENCE PLAYBOOK        │
│                                         │
│  ✅ RECOMMENDED:                        │
│  • HNI Customers (Email) - 3.2x ROI     │
│  • Salaried 30-40 (WhatsApp) - 2.8x ROI │
│                                         │
│  ⛔ AVOID:                              │
│  • Senior Citizens (SMS) - High fatigue │
│  • Students (Call) - 89% rejection      │
│                                         │
│  ⏰ BEST TIMING:                        │
│  • Weekdays: 10AM-12PM, 6PM-8PM         │
│  • Avoid: Mondays, Festival weeks       │
└─────────────────────────────────────────┘
```

---

### 5. 🛡️ Compliance Flags & Safer Wording

**What it does:** Scans campaign content for compliance risks and suggests safer alternatives.

**Checks Performed:**
- TRAI DND compliance
- RBI advertising guidelines
- Misleading claim detection
- Disclaimer presence
- Hidden fee warnings

**Output:**
```
┌─────────────────────────────────────────┐
│         COMPLIANCE FLAGS                │
│                                         │
│  🔴 CRITICAL: "Guaranteed approval"     │
│     → Suggest: "Subject to eligibility" │
│                                         │
│  🟡 WARNING: Missing interest rate      │
│     → Suggest: Add "T&C apply" + rate   │
│                                         │
│  🟡 WARNING: Aggressive CTA             │
│     → "ACT NOW!" → "Learn more"         │
│                                         │
│  ✅ PASS: DND compliance check          │
│  ✅ PASS: Contact info present          │
└─────────────────────────────────────────┘
```

---

### 6. 📝 Executive Narrative

**What it does:** GPT-generated executive summary with actionable insights for leadership.

**Includes:**
- Campaign risk summary in plain English
- Key recommendations prioritized by impact
- Comparison with similar historical campaigns
- Go/No-Go recommendation with confidence level

**Output:**
```
┌─────────────────────────────────────────────────────────────┐
│                  EXECUTIVE NARRATIVE                         │
│                                                              │
│  "This Personal Loan campaign targeting Salaried            │
│  Millennials via SMS shows MODERATE RISK (Health: 72/100).  │
│                                                              │
│  PRIMARY CONCERN: The target segment has received 4         │
│  campaigns in the past 7 days, pushing fatigue risk to 68%. │
│                                                              │
│  RECOMMENDATION: Delay launch by 5 days OR switch to        │
│  WhatsApp channel which shows 23% higher engagement for     │
│  this segment with lower fatigue.                           │
│                                                              │
│  Similar campaigns in Q3 2025 saw 2.1x better ROI when      │
│  launched mid-week with 7-day cooling period."              │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  🟡 CONDITIONAL GO - Address fatigue before launch  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

### 7. 🔍 Similar Campaign Finder (Semantic Search)

**What it does:** Uses vector embeddings to find historically similar campaigns for learning.

**Search Capabilities:**
- Natural language campaign description input
- Semantic similarity matching using FAISS
- Returns top-K similar campaigns with ROI data
- Shows what worked vs what failed

**Output:**
```
┌─────────────────────────────────────────────────────────────┐
│           SIMILAR CAMPAIGNS FOUND (Top 5)                    │
│                                                              │
│  1. Diwali Personal Loan 2025 (92% match)                   │
│     ROI: 2.4x | CTR: 3.2% | Complaints: 12                  │
│     ✅ SUCCESS - Used WhatsApp + 10-day gap                 │
│                                                              │
│  2. Festival Season Loan Push 2024 (87% match)              │
│     ROI: 0.8x | CTR: 1.1% | Complaints: 234                 │
│     ❌ FAILED - SMS spam, no cooling period                 │
│                                                              │
│  3. Q4 Credit Campaign 2025 (84% match)                     │
│     ROI: 1.9x | CTR: 2.8% | Complaints: 28                  │
│     ✅ SUCCESS - Segmented by income band                   │
│                                                              │
│  💡 KEY LEARNING: 7-day gap between campaigns = 2x ROI      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Azure OpenAI API access (for AI features)

### Installation

```bash
# Clone the repository
git clone https://github.com/harithashanmugavel-creator/Haritha-s.git
cd Haritha-s

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

### Running the Application

```bash
# Main Campaign Finder App
streamlit run app.py

# Risk Intelligence Dashboard
streamlit run risk_intelligence_app.py

# Control Tower (Full Platform)
streamlit run control_tower_app.py
```

---

## 📊 Datasets

The platform uses 6 synthetic datasets representing real banking marketing operations:

| Dataset | Records | Purpose |
|---------|---------|---------|
| `campaign_history.csv` | 10,000 | Historical campaign performance & ROI |
| `campaign_content.csv` | 20,000 | SMS/Email/WhatsApp message content |
| `audience_exposure.csv` | 50,000 | Customer fatigue & exposure tracking |
| `campaign_feedback.csv` | 20,000 | Customer complaints & sentiment |
| `campaign_roi_metrics.csv` | 5,000 | Detailed ROI & conversion metrics |
| `campaign_qa_results.csv` | 5,000 | Multi-channel QA validation results |

<details>
<summary><b>📋 Click to see detailed schema</b></summary>

#### campaign_history.csv
Campaign metadata including product, audience segment, channel, spend, impressions, clicks, conversions, CTR, ROI, and status.

#### campaign_content.csv  
Message content with tone analysis, CTA, compliance risk level, language, and A/B variant tracking.

#### audience_exposure.csv
Customer-level exposure tracking with fatigue scores, opt-out risk, engagement rates, and preferred channels.

#### campaign_feedback.csv
Customer feedback with sentiment analysis, issue categories, severity levels, and resolution tracking.

#### campaign_roi_metrics.csv
Granular performance metrics: CPC, CPA, ROAS, CAC, LTV, and benchmark comparisons.

#### campaign_qa_results.csv
QA validation results: tone consistency, CTA alignment, compliance status, and approval tracking.

</details>

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit 1.32+ |
| **LLM** | Azure OpenAI GPT-4 |
| **Embeddings** | text-embedding-3-small |
| **Vector Search** | FAISS |
| **Data Processing** | Pandas, NumPy |
| **Language** | Python 3.10+ |

---

## 📈 Business Impact

### Before OptiGuard AI
- 20-30 analyst hours per campaign review
- 48,000 analyst hours/year total
- ₹7.2 crore annual operational cost
- Reactive problem discovery

### After OptiGuard AI
- **50-70%** reduction in manual effort
- **₹4.3 crore** annual savings
- **5-10%** improvement in conversion rates
- **Predictive** risk identification

---

## 📁 Project Structure

```
marketing_analytics_ai/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
│
├── app.py                       # Similar Campaign Finder UI
├── risk_intelligence_app.py     # Risk Intelligence Dashboard
├── control_tower_app.py         # Full Control Tower Platform
│
├── similar_campaign_finder.py   # Semantic search & recommendations
├── campaign_risk_predictor.py   # Risk prediction engine
├── generate_datasets.py         # Synthetic data generation
│
└── data/                        # Dataset directory
    ├── campaign_history.csv
    ├── campaign_content.csv
    ├── audience_exposure.csv
    ├── campaign_feedback.csv
    ├── campaign_roi_metrics.csv
    └── campaign_qa_results.csv
```

---

## 🔧 Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Required environment variables:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-gpt-deployment
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-small
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**OptiGuard AI** - Built for the Hackathon Competition 2026

---

<div align="center">
<b>⭐ Star this repo if you find it useful!</b>
</div>
