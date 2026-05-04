<div align="center">

# 🛡️ OptiGuard AI

### AI-Powered Marketing Campaign Intelligence & Risk Prediction Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4-0078D4.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Predict campaign failures before they happen. Optimize marketing ROI with AI.**

[Features](#-key-features) • [Demo](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-datasets)

</div>

---

## 📋 Problem Statement

Marketing operations teams at banks manage **hundreds of campaigns** across SMS, Email, WhatsApp, Push Notifications, and Call Center channels. They face critical challenges:

| Challenge | Impact |
|-----------|--------|
| 🔄 Fragmented campaign intelligence | Duplicated efforts, inconsistent messaging |
| 😫 Customer fatigue from repeated targeting | Opt-outs, complaints, brand damage |
| ⏱️ Manual compliance reviews | 20-30 analyst hours per campaign |
| 📉 Delayed ROI analysis | Missed optimization opportunities |
| 🚫 No predictive risk assessment | Campaign failures discovered post-launch |

**Annual Cost:** ₹7.2 crore in operational inefficiency (48,000+ analyst hours/year)

---

## 💡 Solution Overview

**OptiGuard AI** is a predictive marketing intelligence platform that:

- 🎯 **Predicts campaign risks** before launch using ML + LLM analysis
- 🔍 **Finds similar campaigns** via semantic search for learnings
- 📊 **Analyzes ROI patterns** to recommend optimal strategies  
- ⚠️ **Detects customer fatigue** to prevent over-communication
- ✅ **Validates compliance** for multi-channel messaging
- 🤖 **Generates AI insights** for executive decision-making

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Azure OpenAI API access (for AI features)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/marketing-analytics-ai.git
cd marketing-analytics-ai

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

## 🎯 Key Features

### 1. Similar Campaign Finder
Semantic search to find historical campaigns similar to your idea, with ROI insights and engagement metrics.

### 2. Campaign Risk Predictor
ML-powered risk assessment that predicts:
- Customer fatigue probability
- Opt-out risk
- Complaint likelihood
- Trust erosion risk

### 3. AI Targeting Recommendations
LLM-generated insights on:
- Best audiences to target
- Audiences to avoid
- Optimal timing windows
- Channel recommendations

### 4. Multi-Channel QA Validator
Automated consistency checks across SMS, Email, and WhatsApp messaging.

### 5. Compliance Checker
Flags risky wording, missing disclaimers, and regulatory issues.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Campaign   │  │    Risk     │  │   Control Tower     │  │
│  │   Finder    │  │ Intelligence│  │    (Full Suite)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    AI/ML Engine Layer                        │
│  ┌─────────────────┐       ┌─────────────────────────────┐  │
│  │ FAISS Vector DB │       │    Azure OpenAI (GPT-4)     │  │
│  │ (Semantic Search)│       │ - Embeddings (text-embed-3) │  │
│  └─────────────────┘       │ - LLM (Risk Analysis)       │  │
│                            └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer (CSV)                        │
│  campaign_history │ campaign_content │ audience_exposure    │
│  campaign_feedback │ campaign_roi_metrics │ campaign_qa     │
└─────────────────────────────────────────────────────────────┘
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
