"""
Similar Campaign Finder
=======================

Feature 1: Semantic search for similar marketing campaigns using embeddings.
Feature 2: AI-powered targeting recommendations based on campaign analysis.

Workflow:
1. Load campaign data from multiple CSVs
2. Create combined text embeddings using Azure OpenAI text-embedding-3-small
3. Store embeddings in FAISS vector database
4. Perform semantic search to find similar campaigns
5. Generate AI recommendations for targeting

Usage:
    finder = SimilarCampaignFinder()
    finder.build_index()
    results = finder.search("Festival loan campaign for salaried users", top_k=5)
    recommendations = finder.get_targeting_recommendations(results, user_context)
"""

import os
import json
import pickle
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Try to import FAISS
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS not installed. Run: pip install faiss-cpu")

# Try to import OpenAI
try:
    from openai import AzureOpenAI, OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not installed. Run: pip install openai")


# System prompt for targeting recommendations
TARGETING_SYSTEM_PROMPT = """You are an expert marketing strategist AI. Analyze similar campaign data and provide actionable targeting recommendations.

Based on the campaign performance data, feedback, and user's targeting context, provide:

1. **RECOMMENDED AUDIENCES** - Which audience segments to target based on high ROI and positive feedback
2. **AUDIENCES TO AVOID** - Which segments showed poor performance or negative feedback (spam complaints, misleading content issues)
3. **OPTIMAL TIMING** - Best time periods, days, or seasons based on successful campaigns
4. **CHANNEL RECOMMENDATIONS** - Which channels performed best for similar campaigns
5. **KEY LEARNINGS** - What worked and what didn't in similar campaigns

Respond in JSON format:
{
    "recommended_audiences": [
        {"segment": "name", "reason": "why", "expected_roi": "estimate", "confidence": "high/medium/low"}
    ],
    "avoid_audiences": [
        {"segment": "name", "reason": "why", "risk": "description"}
    ],
    "timing_recommendations": {
        "best_months": ["month names"],
        "best_days": ["day names or patterns"],
        "duration_suggestion": "recommended campaign duration",
        "reasoning": "why this timing"
    },
    "channel_recommendations": [
        {"channel": "name", "performance": "metrics summary", "best_for": "use case"}
    ],
    "key_learnings": [
        {"insight": "learning", "action": "what to do"}
    ],
    "warnings": ["potential pitfalls to avoid"],
    "summary": "2-3 sentence overall recommendation"
}"""


class SimilarCampaignFinder:
    """
    Find similar marketing campaigns using semantic search.
    
    Uses Azure OpenAI embeddings and FAISS for fast similarity search.
    """
    
    # Embedding model configuration
    EMBEDDING_DIMENSION = 1536  # Dimension for text-embedding-3-small
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the Similar Campaign Finder.
        
        Args:
            data_dir: Directory containing campaign data CSVs
        """
        self.data_dir = Path(__file__).parent / data_dir
        self.index_path = Path(__file__).parent / "campaign_index.faiss"
        self.metadata_path = Path(__file__).parent / "campaign_metadata.pkl"
        
        # Get models from env
        self.embedding_model = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-small-gamma")
        self.llm_model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.4-gamma")
        
        # Initialize OpenAI clients
        self.client = self._init_openai_client()
        self.llm_client = self._init_llm_client()
        
        # Data storage
        self.campaigns_df: Optional[pd.DataFrame] = None
        self.content_df: Optional[pd.DataFrame] = None
        self.roi_df: Optional[pd.DataFrame] = None
        self.feedback_df: Optional[pd.DataFrame] = None
        self.combined_df: Optional[pd.DataFrame] = None
        
        # FAISS index
        self.index: Optional[faiss.IndexFlatIP] = None
        self.campaign_ids: List[str] = []
        
        logger.info(f"SimilarCampaignFinder initialized with data_dir: {self.data_dir}")
    
    def _init_openai_client(self):
        """Initialize Azure OpenAI or standard OpenAI client."""
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI not available. Running in mock mode.")
            return None
        
        # Try Azure OpenAI first
        azure_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if azure_key and azure_endpoint:
            try:
                client = AzureOpenAI(
                    api_key=azure_key,
                    api_version=os.getenv("AZURE_EMBEDDING_API_VERSION", "2024-12-01-preview"),
                    azure_endpoint=azure_endpoint
                )
                logger.info(f"Initialized Azure OpenAI client for embeddings (model: {self.embedding_model})")
                return client
            except Exception as e:
                logger.warning(f"Failed to initialize Azure OpenAI: {e}")
        
        # Fallback to standard OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                client = OpenAI(api_key=openai_key)
                logger.info("Initialized standard OpenAI client for embeddings")
                return client
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
        
        logger.warning("No OpenAI API key configured. Using mock embeddings.")
        return None
    
    def _init_llm_client(self):
        """Initialize Azure OpenAI client for LLM (GPT) operations."""
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI not available for LLM.")
            return None
        
        azure_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if azure_key and azure_endpoint:
            try:
                client = AzureOpenAI(
                    api_key=azure_key,
                    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
                    azure_endpoint=azure_endpoint
                )
                logger.info(f"Initialized Azure OpenAI LLM client (model: {self.llm_model})")
                return client
            except Exception as e:
                logger.warning(f"Failed to initialize LLM client: {e}")
        
        return None
    
    def load_data(self) -> pd.DataFrame:
        """
        Load and merge all campaign data from CSVs.
        
        Returns:
            Combined DataFrame with all campaign information
        """
        logger.info("Loading campaign data...")
        
        # Load campaign history
        self.campaigns_df = pd.read_csv(self.data_dir / "campaign_history.csv")
        logger.info(f"Loaded {len(self.campaigns_df)} campaigns from campaign_history.csv")
        
        # Load campaign content
        self.content_df = pd.read_csv(self.data_dir / "campaign_content.csv")
        logger.info(f"Loaded {len(self.content_df)} content items from campaign_content.csv")
        
        # Load ROI metrics
        self.roi_df = pd.read_csv(self.data_dir / "campaign_roi_metrics.csv")
        logger.info(f"Loaded {len(self.roi_df)} ROI records from campaign_roi_metrics.csv")
        
        # Load feedback
        self.feedback_df = pd.read_csv(self.data_dir / "campaign_feedback.csv")
        logger.info(f"Loaded {len(self.feedback_df)} feedback records from campaign_feedback.csv")
        
        # Merge content with campaigns (take first content per campaign)
        content_per_campaign = self.content_df.groupby('campaign_id').first().reset_index()
        self.combined_df = self.campaigns_df.merge(
            content_per_campaign[['campaign_id', 'content_text', 'tone', 'cta']],
            on='campaign_id',
            how='left'
        )
        
        # Merge ROI metrics (take latest per campaign)
        roi_latest = self.roi_df.sort_values('measurement_date').groupby('campaign_id').last().reset_index()
        self.combined_df = self.combined_df.merge(
            roi_latest[['campaign_id', 'roi_score', 'roas', 'cost_per_conversion']],
            on='campaign_id',
            how='left'
        )
        
        # Aggregate feedback per campaign
        feedback_agg = self.feedback_df.groupby('campaign_id').agg({
            'sentiment_score': 'mean',
            'feedback_text': lambda x: ' | '.join(x.head(3).tolist()),  # Top 3 feedback
            'severity': lambda x: (x == 'High').sum()  # Count of high severity issues
        }).reset_index()
        feedback_agg.columns = ['campaign_id', 'avg_sentiment', 'sample_feedback', 'high_severity_count']
        
        self.combined_df = self.combined_df.merge(feedback_agg, on='campaign_id', how='left')
        
        # Fill NaN content_text
        self.combined_df['content_text'] = self.combined_df['content_text'].fillna('')
        
        logger.info(f"Combined data: {len(self.combined_df)} campaigns with full context")
        
        return self.combined_df
    
    def create_combined_text(self, row: pd.Series) -> str:
        """
        Create combined text for embedding from campaign row.
        
        Format:
            campaign_name
            product
            audience_segment
            campaign_objective
            content_text
        
        Args:
            row: DataFrame row with campaign data
            
        Returns:
            Combined text string for embedding
        """
        combined = f"""
{row.get('campaign_name', '')}
{row.get('product', '')}
{row.get('audience_segment', '')}
{row.get('campaign_objective', '')}
{row.get('content_text', '')}
""".strip()
        
        return combined
    
    def get_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for text using Azure OpenAI.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        if not self.client:
            # Return mock embedding for testing
            logger.debug("Using mock embedding (no API client)")
            np.random.seed(hash(text) % (2**32))
            return np.random.randn(self.EMBEDDING_DIMENSION).astype('float32')
        
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            embedding = np.array(response.data[0].embedding, dtype='float32')
            return embedding
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            # Fallback to mock
            np.random.seed(hash(text) % (2**32))
            return np.random.randn(self.EMBEDDING_DIMENSION).astype('float32')
    
    def get_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> np.ndarray:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts per API call
            
        Returns:
            Array of embedding vectors
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
            
            if not self.client:
                # Mock embeddings
                for text in batch:
                    all_embeddings.append(self.get_embedding(text))
            else:
                try:
                    response = self.client.embeddings.create(
                        model=self.embedding_model,
                        input=batch
                    )
                    for item in response.data:
                        all_embeddings.append(np.array(item.embedding, dtype='float32'))
                except Exception as e:
                    logger.error(f"Batch embedding failed: {e}")
                    for text in batch:
                        all_embeddings.append(self.get_embedding(text))
        
        return np.array(all_embeddings)
    
    def build_index(self, force_rebuild: bool = False) -> None:
        """
        Build FAISS index from campaign embeddings.
        
        Args:
            force_rebuild: If True, rebuild index even if exists
        """
        if not FAISS_AVAILABLE:
            raise RuntimeError("FAISS is required. Install with: pip install faiss-cpu")
        
        # Check if index already exists
        if not force_rebuild and self.index_path.exists() and self.metadata_path.exists():
            logger.info("Loading existing index...")
            self.load_index()
            return
        
        logger.info("Building new FAISS index...")
        
        # Load data if not already loaded
        if self.combined_df is None:
            self.load_data()
        
        # Create combined texts
        logger.info("Creating combined texts for embedding...")
        combined_texts = self.combined_df.apply(self.create_combined_text, axis=1).tolist()
        self.campaign_ids = self.combined_df['campaign_id'].tolist()
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(combined_texts)} campaigns...")
        embeddings = self.get_embeddings_batch(combined_texts)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index (Inner Product = Cosine Similarity after normalization)
        self.index = faiss.IndexFlatIP(self.EMBEDDING_DIMENSION)
        self.index.add(embeddings)
        
        logger.info(f"FAISS index built with {self.index.ntotal} vectors")
        
        # Save index and metadata
        self.save_index()
    
    def save_index(self) -> None:
        """Save FAISS index and metadata to disk."""
        if self.index is None:
            logger.warning("No index to save")
            return
        
        faiss.write_index(self.index, str(self.index_path))
        
        metadata = {
            'campaign_ids': self.campaign_ids,
            'created_at': datetime.now().isoformat()
        }
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        
        logger.info(f"Index saved to {self.index_path}")
    
    def load_index(self) -> None:
        """Load FAISS index and metadata from disk."""
        if not FAISS_AVAILABLE:
            raise RuntimeError("FAISS is required")
        
        self.index = faiss.read_index(str(self.index_path))
        
        with open(self.metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        self.campaign_ids = metadata['campaign_ids']
        
        # Load data for results
        if self.combined_df is None:
            self.load_data()
        
        logger.info(f"Loaded index with {self.index.ntotal} vectors")
    
    def search(self, query: str, top_k: int = 5) -> pd.DataFrame:
        """
        Search for similar campaigns using semantic search.
        
        Args:
            query: Natural language query (e.g., "Festival loan campaign for salaried users")
            top_k: Number of similar campaigns to return
            
        Returns:
            DataFrame with similar campaigns and their metrics
        """
        if self.index is None:
            raise RuntimeError("Index not built. Call build_index() first.")
        
        logger.info(f"Searching for: '{query}'")
        
        # Generate query embedding
        query_embedding = self.get_embedding(query)
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Build results
        results = []
        for i, (idx, score) in enumerate(zip(indices[0], distances[0])):
            if idx < 0:  # FAISS returns -1 for empty slots
                continue
            
            campaign_id = self.campaign_ids[idx]
            campaign_data = self.combined_df[self.combined_df['campaign_id'] == campaign_id].iloc[0]
            
            # Generate feedback summary
            feedback_summary = self._generate_feedback_summary(campaign_id)
            
            results.append({
                'Rank': i + 1,
                'Campaign': campaign_data['campaign_name'],
                'Campaign_ID': campaign_id,
                'Product': campaign_data['product'],
                'Audience': campaign_data['audience_segment'],
                'Objective': campaign_data['campaign_objective'],
                'ROI': round(campaign_data.get('roi', campaign_data.get('roi_score', 0)), 2),
                'CTR': f"{campaign_data.get('ctr', 0):.1f}%",
                'Feedback': feedback_summary,
                'Similarity_Score': round(score * 100, 1),
                'Channel': campaign_data['channel'],
                'Status': campaign_data['campaign_status']
            })
        
        results_df = pd.DataFrame(results)
        
        return results_df
    
    def _generate_feedback_summary(self, campaign_id: str) -> str:
        """
        Generate a summary of feedback for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Short feedback summary string
        """
        if self.feedback_df is None:
            return "No feedback data"
        
        campaign_feedback = self.feedback_df[self.feedback_df['campaign_id'] == campaign_id]
        
        if campaign_feedback.empty:
            return "No feedback received"
        
        # Calculate sentiment distribution
        positive = len(campaign_feedback[campaign_feedback['sentiment'].isin(['Positive', 'Very Positive'])])
        negative = len(campaign_feedback[campaign_feedback['sentiment'].isin(['Negative', 'Very Negative'])])
        total = len(campaign_feedback)
        
        if positive > negative:
            sentiment = "Positive reception"
        elif negative > positive:
            sentiment = "Mixed/Negative feedback"
        else:
            sentiment = "Neutral feedback"
        
        # Check for spam complaints
        spam_complaints = len(campaign_feedback[campaign_feedback['issue_category'].str.contains('Spam', na=False)])
        
        if spam_complaints > 0:
            return f"{sentiment}, {spam_complaints} spam complaints"
        
        # Get top issue if negative
        if negative > 0:
            top_issue = campaign_feedback['issue_category'].mode()
            if len(top_issue) > 0:
                return f"{sentiment}: {top_issue.iloc[0]}"
        
        return sentiment
    
    def search_and_display(self, query: str, top_k: int = 5) -> None:
        """
        Search and display results in a formatted table.
        
        Args:
            query: Search query
            top_k: Number of results
        """
        print(f"\n{'='*80}")
        print(f"🔍 SIMILAR CAMPAIGN FINDER")
        print(f"{'='*80}")
        print(f"\nQuery: \"{query}\"\n")
        
        results = self.search(query, top_k)
        
        if results.empty:
            print("No similar campaigns found.")
            return
        
        # Display as formatted table
        print(f"{'Campaign':<40} {'ROI':<8} {'CTR':<8} {'Feedback':<30}")
        print("-" * 90)
        
        for _, row in results.iterrows():
            campaign_name = row['Campaign'][:38] + '..' if len(row['Campaign']) > 40 else row['Campaign']
            feedback = row['Feedback'][:28] + '..' if len(row['Feedback']) > 30 else row['Feedback']
            print(f"{campaign_name:<40} {row['ROI']:<8} {row['CTR']:<8} {feedback:<30}")
        
        print(f"\n{'='*80}\n")
        
        return results
    
    def get_targeting_recommendations(
        self, 
        results_df: pd.DataFrame, 
        user_context: Optional[Dict] = None
    ) -> Dict:
        """
        Generate AI-powered targeting recommendations based on similar campaigns.
        
        Args:
            results_df: DataFrame from search() with similar campaigns
            user_context: Optional dict with user's context (budget, region, goals, etc.)
            
        Returns:
            Dict with targeting recommendations including:
            - recommended_audiences: List of audience segments to target
            - avoid_audiences: Audiences to avoid based on negative feedback
            - timing_recommendations: Best timing for campaigns
            - channel_recommendations: Recommended channels
            - key_learnings: Insights from similar campaigns
            - warnings: Issues to watch out for
        """
        if self.llm_client is None:
            logger.warning("LLM client not available. Returning basic recommendations.")
            return self._get_fallback_recommendations(results_df)
        
        if results_df.empty:
            return {"error": "No campaigns to analyze", "recommendations": []}
        
        # Prepare campaign data for LLM
        campaign_summary = self._format_campaign_data_for_llm(results_df)
        
        # Analyze feedback patterns
        feedback_analysis = self._analyze_feedback_patterns(results_df)
        
        # Build user context string
        context_str = ""
        if user_context:
            context_str = f"""
User's Campaign Context:
- Budget: {user_context.get('budget', 'Not specified')}
- Target Region: {user_context.get('region', 'Not specified')}
- Campaign Goal: {user_context.get('goal', 'Not specified')}
- Product/Service: {user_context.get('product', 'Not specified')}
- Timeline: {user_context.get('timeline', 'Not specified')}
"""
        
        # Build prompt
        user_prompt = f"""
Analyze these similar campaigns and provide targeting recommendations:

{campaign_summary}

Feedback Analysis from Similar Campaigns:
{feedback_analysis}

{context_str}

Based on this data, provide specific, actionable targeting recommendations. Focus on:
1. Which audiences performed well and should be targeted
2. Which audiences had negative feedback and should be avoided
3. Best timing for campaigns based on historical performance
4. Channel preferences based on engagement metrics
5. Key warnings from negative feedback patterns

Return your analysis as valid JSON.
"""
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": TARGETING_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_completion_tokens=2000
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content
            
            # Extract JSON from response (handle potential markdown code blocks)
            json_match = response_text
            if "```json" in response_text:
                json_match = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                json_match = response_text.split("```")[1].split("```")[0]
            
            recommendations = json.loads(json_match.strip())
            logger.info("Successfully generated targeting recommendations")
            return recommendations
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            return {
                "error": "Failed to parse recommendations",
                "raw_response": response_text if 'response_text' in locals() else None,
                "fallback": self._get_fallback_recommendations(results_df)
            }
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return self._get_fallback_recommendations(results_df)
    
    def _format_campaign_data_for_llm(self, results_df: pd.DataFrame) -> str:
        """Format campaign results for LLM context."""
        campaign_lines = []
        
        for idx, row in results_df.iterrows():
            campaign_info = f"""
Campaign {idx + 1}: {row.get('Campaign', 'N/A')}
- Similarity Score: {row.get('Similarity', 0):.2%}
- Audience: {row.get('Audience', 'N/A')}
- Region: {row.get('Region', 'N/A')}
- Channel: {row.get('Channel', 'N/A')}
- ROI: {row.get('ROI', 'N/A')}
- CTR: {row.get('CTR', 'N/A')}
- Conversions: {row.get('Conversions', 'N/A')}
- Spend: {row.get('Spend', 'N/A')}
- Content Tone: {row.get('Content_Tone', 'N/A')}
- Feedback Summary: {row.get('Feedback', 'N/A')}
"""
            campaign_lines.append(campaign_info)
        
        return "\n".join(campaign_lines)
    
    def _analyze_feedback_patterns(self, results_df: pd.DataFrame) -> str:
        """Analyze feedback patterns from similar campaigns."""
        if self.feedback_df is None:
            return "No feedback data available"
        
        # Get campaign IDs from results
        campaign_ids = []
        if self.combined_df is not None:
            for campaign_name in results_df.get('Campaign', []):
                matching = self.combined_df[self.combined_df['campaign_name'] == campaign_name]
                if not matching.empty:
                    campaign_ids.extend(matching['campaign_id'].tolist())
        
        if not campaign_ids:
            return "No matching campaign feedback found"
        
        # Filter feedback for these campaigns
        relevant_feedback = self.feedback_df[
            self.feedback_df['campaign_id'].isin(campaign_ids)
        ]
        
        if relevant_feedback.empty:
            return "No feedback data for similar campaigns"
        
        # Analyze patterns
        analysis_parts = []
        
        # Sentiment distribution
        sentiment_counts = relevant_feedback['sentiment'].value_counts()
        analysis_parts.append(f"Sentiment Distribution: {sentiment_counts.to_dict()}")
        
        # Common issues
        issue_counts = relevant_feedback['issue_category'].value_counts().head(5)
        if not issue_counts.empty:
            analysis_parts.append(f"Top Issues: {issue_counts.to_dict()}")
        
        # Spam complaints
        spam_count = len(relevant_feedback[
            relevant_feedback['issue_category'].str.contains('Spam', na=False, case=False)
        ])
        if spam_count > 0:
            analysis_parts.append(f"⚠️ Spam Complaints: {spam_count}")
        
        # Negative feedback details
        negative_feedback = relevant_feedback[
            relevant_feedback['sentiment'].isin(['Negative', 'Very Negative'])
        ]
        if not negative_feedback.empty:
            severe_issues = negative_feedback[negative_feedback['severity'].isin(['High', 'Critical'])]
            if not severe_issues.empty:
                analysis_parts.append(
                    f"⚠️ High/Critical Severity Issues: {len(severe_issues)} cases"
                )
                # Sample issues
                sample_issues = severe_issues['issue_category'].value_counts().head(3)
                analysis_parts.append(f"Most Common Severe Issues: {sample_issues.to_dict()}")
        
        # Average sentiment score
        if 'sentiment_score' in relevant_feedback.columns:
            avg_sentiment = relevant_feedback['sentiment_score'].mean()
            analysis_parts.append(f"Average Sentiment Score: {avg_sentiment:.2f}")
        
        return "\n".join(analysis_parts)
    
    def _get_fallback_recommendations(self, results_df: pd.DataFrame) -> Dict:
        """Generate basic recommendations without LLM."""
        recommendations = {
            "recommended_audiences": [],
            "avoid_audiences": [],
            "timing_recommendations": {"note": "LLM not available for detailed timing analysis"},
            "channel_recommendations": [],
            "key_learnings": [],
            "warnings": ["AI recommendations unavailable - showing basic analysis only"],
            "summary": "Basic analysis based on campaign metrics"
        }
        
        if results_df.empty:
            return recommendations
        
        # Extract unique audiences from successful campaigns (ROI > median)
        try:
            # Get high-performing audience segments
            if 'Audience' in results_df.columns:
                audiences = results_df['Audience'].dropna().unique().tolist()
                recommendations["recommended_audiences"] = [
                    {"segment": aud, "reason": "Found in similar campaigns"}
                    for aud in audiences[:5]
                ]
            
            # Get channels
            if 'Channel' in results_df.columns:
                channels = results_df['Channel'].dropna().unique().tolist()
                recommendations["channel_recommendations"] = [
                    {"channel": ch, "priority": "medium", "reason": "Used in similar campaigns"}
                    for ch in channels[:3]
                ]
            
            # Add key learnings from top campaigns
            top_campaigns = results_df.head(3)
            for _, row in top_campaigns.iterrows():
                learning = f"Campaign '{row.get('Campaign', 'Unknown')}' achieved {row.get('ROI', 'N/A')} ROI"
                recommendations["key_learnings"].append(learning)
                
        except Exception as e:
            logger.error(f"Error generating fallback recommendations: {e}")
        
        return recommendations
    
    def ask_targeting_question(self, question: str, results_df: pd.DataFrame) -> str:
        """
        Answer a specific targeting question based on campaign data.
        
        Args:
            question: User's question about targeting
            results_df: DataFrame from search() with similar campaigns
            
        Returns:
            AI-generated answer to the question
        """
        if self.llm_client is None:
            return "AI assistant not available. Please check your API configuration."
        
        campaign_summary = self._format_campaign_data_for_llm(results_df)
        feedback_analysis = self._analyze_feedback_patterns(results_df)
        
        prompt = f"""
Based on the following similar campaign data and feedback analysis, please answer this question:

Question: {question}

Campaign Data:
{campaign_summary}

Feedback Analysis:
{feedback_analysis}

Please provide a specific, actionable answer based on the data above. Be concise but thorough.
"""
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert marketing strategist. Answer questions about campaign targeting based on historical campaign data and feedback. Be specific and actionable."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_completion_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return f"Sorry, I couldn't process your question. Error: {str(e)}"
    
    def analyze_campaign_performance(self, results_df: pd.DataFrame) -> Dict:
        """
        Analyze and compare campaign performance - what worked vs what didn't.
        
        Args:
            results_df: DataFrame from search() with similar campaigns
            
        Returns:
            Dict with performance analysis including:
            - top_performers: Best performing campaigns with reasons
            - underperformers: Campaigns that didn't perform well with reasons
            - comparison: Direct comparison insights
            - success_factors: What made top campaigns successful
            - failure_factors: What caused underperformance
        """
        if results_df.empty:
            return {"error": "No campaigns to analyze"}
        
        # Calculate performance metrics
        results_with_metrics = results_df.copy()
        
        # Get ROI as numeric
        results_with_metrics['ROI_numeric'] = pd.to_numeric(
            results_with_metrics['ROI'].astype(str).str.replace('%', ''), 
            errors='coerce'
        ).fillna(0)
        
        # Determine median ROI for classification
        median_roi = results_with_metrics['ROI_numeric'].median()
        
        # Classify campaigns
        top_performers = results_with_metrics[results_with_metrics['ROI_numeric'] >= median_roi].head(3)
        underperformers = results_with_metrics[results_with_metrics['ROI_numeric'] < median_roi].head(3)
        
        # Get detailed feedback for each
        top_feedback = self._get_detailed_feedback(top_performers)
        under_feedback = self._get_detailed_feedback(underperformers)
        
        # If no LLM, return basic analysis
        if self.llm_client is None:
            return self._get_basic_performance_analysis(top_performers, underperformers, top_feedback, under_feedback)
        
        # Prepare data for LLM analysis
        top_data = []
        for _, row in top_performers.iterrows():
            top_data.append({
                "campaign": row['Campaign'],
                "roi": row['ROI'],
                "ctr": row['CTR'],
                "audience": row['Audience'],
                "channel": row['Channel'],
                "feedback": row['Feedback'],
                "objective": row.get('Objective', 'N/A')
            })
        
        under_data = []
        for _, row in underperformers.iterrows():
            under_data.append({
                "campaign": row['Campaign'],
                "roi": row['ROI'],
                "ctr": row['CTR'],
                "audience": row['Audience'],
                "channel": row['Channel'],
                "feedback": row['Feedback'],
                "objective": row.get('Objective', 'N/A')
            })
        
        prompt = f"""
Analyze the performance of these similar marketing campaigns and provide insights on what worked vs what didn't.

TOP PERFORMING CAMPAIGNS (High ROI):
{json.dumps(top_data, indent=2)}

Feedback Details for Top Performers:
{json.dumps(top_feedback, indent=2)}

UNDERPERFORMING CAMPAIGNS (Lower ROI):
{json.dumps(under_data, indent=2)}

Feedback Details for Underperformers:
{json.dumps(under_feedback, indent=2)}

Median ROI: {median_roi:.1f}

Provide a detailed analysis in the following JSON format:
{{
    "top_performers": [
        {{
            "campaign": "Campaign name",
            "roi": "ROI value",
            "success_reasons": ["Reason 1", "Reason 2"],
            "key_strengths": ["Strength 1", "Strength 2"]
        }}
    ],
    "underperformers": [
        {{
            "campaign": "Campaign name",
            "roi": "ROI value",
            "failure_reasons": ["Reason 1", "Reason 2"],
            "improvement_suggestions": ["Suggestion 1", "Suggestion 2"]
        }}
    ],
    "comparison_insights": [
        "Key insight comparing top vs underperformers"
    ],
    "success_factors": [
        "Common factor that led to success"
    ],
    "failure_factors": [
        "Common factor that led to underperformance"
    ],
    "recommendations": [
        "Actionable recommendation based on analysis"
    ],
    "summary": "Brief summary of overall findings"
}}
"""
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert marketing analyst. Analyze campaign performance data and provide insights on what made campaigns successful or unsuccessful. Be specific and data-driven. Return valid JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_completion_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            
            # Extract JSON
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            analysis = json.loads(response_text.strip())
            analysis['median_roi'] = median_roi
            analysis['total_campaigns_analyzed'] = len(results_df)
            logger.info("Successfully generated performance analysis")
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse performance analysis: {e}")
            return self._get_basic_performance_analysis(top_performers, underperformers, top_feedback, under_feedback)
        except Exception as e:
            logger.error(f"Error generating performance analysis: {e}")
            return self._get_basic_performance_analysis(top_performers, underperformers, top_feedback, under_feedback)
    
    def _get_detailed_feedback(self, campaigns_df: pd.DataFrame) -> List[Dict]:
        """Get detailed feedback for campaigns."""
        feedback_details = []
        
        if self.feedback_df is None:
            return feedback_details
        
        for _, row in campaigns_df.iterrows():
            campaign_id = row.get('Campaign_ID')
            if not campaign_id:
                continue
            
            campaign_feedback = self.feedback_df[self.feedback_df['campaign_id'] == campaign_id]
            
            if campaign_feedback.empty:
                continue
            
            sentiment_dist = campaign_feedback['sentiment'].value_counts().to_dict()
            issues = campaign_feedback['issue_category'].value_counts().head(3).to_dict()
            avg_score = campaign_feedback['sentiment_score'].mean() if 'sentiment_score' in campaign_feedback else 0
            
            feedback_details.append({
                "campaign": row['Campaign'],
                "total_feedback": len(campaign_feedback),
                "sentiment_distribution": sentiment_dist,
                "top_issues": issues,
                "avg_sentiment_score": round(avg_score, 2)
            })
        
        return feedback_details
    
    def _get_basic_performance_analysis(
        self, 
        top_performers: pd.DataFrame, 
        underperformers: pd.DataFrame,
        top_feedback: List[Dict],
        under_feedback: List[Dict]
    ) -> Dict:
        """Generate basic performance analysis without LLM."""
        analysis = {
            "top_performers": [],
            "underperformers": [],
            "comparison_insights": ["AI analysis unavailable - showing basic metrics"],
            "success_factors": [],
            "failure_factors": [],
            "recommendations": ["Enable AI for detailed insights"],
            "summary": "Basic performance comparison based on ROI metrics"
        }
        
        for _, row in top_performers.iterrows():
            analysis["top_performers"].append({
                "campaign": row['Campaign'],
                "roi": row['ROI'],
                "success_reasons": [f"High ROI: {row['ROI']}", f"Feedback: {row['Feedback']}"],
                "key_strengths": [row['Channel'], row['Audience']]
            })
        
        for _, row in underperformers.iterrows():
            analysis["underperformers"].append({
                "campaign": row['Campaign'],
                "roi": row['ROI'],
                "failure_reasons": [f"Lower ROI: {row['ROI']}", f"Feedback: {row['Feedback']}"],
                "improvement_suggestions": ["Review targeting", "Optimize content"]
            })
        
        return analysis

    def get_performance_comparison(
        self,
        region: str = None,
        product: str = None,
        goal: str = None
    ) -> Dict:
        """
        Get top 3 best performing and top 3 underperforming campaigns based on context.
        
        Args:
            region: Target region filter
            product: Product/service filter
            goal: Campaign goal filter
            
        Returns:
            Dict with performance comparison including top 3 vs bottom 3
        """
        if self.combined_df is None:
            return {"error": "Data not loaded"}
        
        # Filter campaigns based on context
        filtered_df = self.combined_df.copy()
        filters_applied = []
        
        if region and region not in ["All Regions", ""]:
            temp = filtered_df[filtered_df['region'].str.contains(region, case=False, na=False)]
            if not temp.empty:
                filtered_df = temp
                filters_applied.append(f"region={region}")
        
        if product:
            temp = filtered_df[filtered_df['product'].str.contains(product, case=False, na=False)]
            if not temp.empty:
                filtered_df = temp
                filters_applied.append(f"product={product}")
        
        if goal and goal not in ["Any Goal", "Select...", ""]:
            temp = filtered_df[filtered_df['campaign_objective'].str.contains(goal, case=False, na=False)]
            if not temp.empty:
                filtered_df = temp
                filters_applied.append(f"goal={goal}")
        
        if filtered_df.empty:
            filtered_df = self.combined_df.copy()
            filters_applied = ["all campaigns (no filter match)"]
        
        # Get top 3 performers and bottom 3
        top_3 = filtered_df.nlargest(3, 'roi')
        bottom_3 = filtered_df.nsmallest(3, 'roi')
        
        # Get feedback for these campaigns
        top_feedback = self._get_campaign_feedback_details(top_3)
        bottom_feedback = self._get_campaign_feedback_details(bottom_3)
        
        # If no LLM, return basic analysis
        if self.llm_client is None:
            return self._get_basic_comparison(top_3, bottom_3, top_feedback, bottom_feedback, filters_applied)
        
        # Prepare data for LLM
        top_data = []
        for _, row in top_3.iterrows():
            campaign_id = row['campaign_id']
            feedback_info = top_feedback.get(campaign_id, {})
            top_data.append({
                "campaign": row['campaign_name'],
                "roi": round(row['roi'], 2),
                "audience": row['audience_segment'],
                "channel": row['channel'],
                "region": row['region'],
                "product": row['product'],
                "objective": row['campaign_objective'],
                "feedback_sentiment": feedback_info.get('sentiment_summary', 'N/A'),
                "feedback_issues": feedback_info.get('issues', [])
            })
        
        bottom_data = []
        for _, row in bottom_3.iterrows():
            campaign_id = row['campaign_id']
            feedback_info = bottom_feedback.get(campaign_id, {})
            bottom_data.append({
                "campaign": row['campaign_name'],
                "roi": round(row['roi'], 2),
                "audience": row['audience_segment'],
                "channel": row['channel'],
                "region": row['region'],
                "product": row['product'],
                "objective": row['campaign_objective'],
                "feedback_sentiment": feedback_info.get('sentiment_summary', 'N/A'),
                "feedback_issues": feedback_info.get('issues', [])
            })
        
        prompt = f"""
Analyze these campaigns and explain why some performed well and others didn't.

CONTEXT FILTERS: {', '.join(filters_applied) if filters_applied else 'None'}

TOP 3 BEST PERFORMING CAMPAIGNS:
{json.dumps(top_data, indent=2)}

BOTTOM 3 UNDERPERFORMING CAMPAIGNS:
{json.dumps(bottom_data, indent=2)}

Provide detailed analysis in this JSON format:
{{
    "top_performers": [
        {{
            "campaign": "name",
            "roi": value,
            "why_it_worked": ["reason 1", "reason 2", "reason 3"],
            "key_success_factors": ["factor 1", "factor 2"]
        }}
    ],
    "underperformers": [
        {{
            "campaign": "name",
            "roi": value,
            "why_it_failed": ["reason 1", "reason 2", "reason 3"],
            "what_went_wrong": ["issue 1", "issue 2"]
        }}
    ],
    "key_differences": [
        "Main difference 1 between winners and losers",
        "Main difference 2",
        "Main difference 3"
    ],
    "lessons_learned": [
        "Lesson 1 from this comparison",
        "Lesson 2"
    ],
    "recommendations_for_new_campaign": [
        "Based on analysis, do this",
        "Avoid this"
    ],
    "summary": "Brief summary explaining the performance gap"
}}
"""
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert marketing analyst. Analyze campaign performance and provide specific, data-driven insights on why campaigns succeeded or failed. Return valid JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_completion_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            analysis = json.loads(response_text.strip())
            analysis['filters_applied'] = filters_applied
            analysis['total_campaigns_in_filter'] = len(filtered_df)
            logger.info(f"Generated performance comparison with filters: {filters_applied}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error generating performance comparison: {e}")
            return self._get_basic_comparison(top_3, bottom_3, top_feedback, bottom_feedback, filters_applied)
    
    def _get_campaign_feedback_details(self, campaigns_df: pd.DataFrame) -> Dict:
        """Get feedback details for a set of campaigns."""
        feedback_details = {}
        
        if self.feedback_df is None:
            return feedback_details
        
        for _, row in campaigns_df.iterrows():
            campaign_id = row['campaign_id']
            campaign_feedback = self.feedback_df[self.feedback_df['campaign_id'] == campaign_id]
            
            if campaign_feedback.empty:
                feedback_details[campaign_id] = {"sentiment_summary": "No feedback", "issues": []}
                continue
            
            # Sentiment summary
            sentiment_counts = campaign_feedback['sentiment'].value_counts()
            positive = sentiment_counts.get('Positive', 0) + sentiment_counts.get('Very Positive', 0)
            negative = sentiment_counts.get('Negative', 0) + sentiment_counts.get('Very Negative', 0)
            
            if positive > negative:
                sentiment = "Mostly Positive"
            elif negative > positive:
                sentiment = "Mostly Negative"
            else:
                sentiment = "Mixed"
            
            # Top issues
            issues = campaign_feedback['issue_category'].value_counts().head(3).index.tolist()
            
            feedback_details[campaign_id] = {
                "sentiment_summary": sentiment,
                "positive_count": int(positive),
                "negative_count": int(negative),
                "issues": issues
            }
        
        return feedback_details
    
    def _get_basic_comparison(
        self,
        top_3: pd.DataFrame,
        bottom_3: pd.DataFrame,
        top_feedback: Dict,
        bottom_feedback: Dict,
        filters_applied: List[str]
    ) -> Dict:
        """Generate basic comparison without LLM."""
        analysis = {
            "top_performers": [],
            "underperformers": [],
            "key_differences": ["AI analysis unavailable - showing basic metrics"],
            "lessons_learned": ["Higher ROI correlates with positive feedback"],
            "recommendations_for_new_campaign": ["Focus on successful patterns from top performers"],
            "summary": "Basic comparison based on ROI metrics",
            "filters_applied": filters_applied,
            "total_campaigns_in_filter": len(top_3) + len(bottom_3)
        }
        
        for _, row in top_3.iterrows():
            campaign_id = row['campaign_id']
            feedback = top_feedback.get(campaign_id, {})
            analysis["top_performers"].append({
                "campaign": row['campaign_name'],
                "roi": round(row['roi'], 2),
                "why_it_worked": [
                    f"High ROI: {row['roi']:.1f}",
                    f"Channel: {row['channel']}",
                    f"Feedback: {feedback.get('sentiment_summary', 'N/A')}"
                ],
                "key_success_factors": [row['audience_segment'], row['channel']]
            })
        
        for _, row in bottom_3.iterrows():
            campaign_id = row['campaign_id']
            feedback = bottom_feedback.get(campaign_id, {})
            analysis["underperformers"].append({
                "campaign": row['campaign_name'],
                "roi": round(row['roi'], 2),
                "why_it_failed": [
                    f"Low ROI: {row['roi']:.1f}",
                    f"Channel: {row['channel']}",
                    f"Feedback: {feedback.get('sentiment_summary', 'N/A')}"
                ],
                "what_went_wrong": feedback.get('issues', ['Unknown'])[:2]
            })
        
        return analysis

    def get_content_suggestions(
        self, 
        region: str, 
        product: str = None,
        goal: str = None
    ) -> Dict:
        """
        Suggest content based on successful campaigns in the specified region.
        
        Args:
            region: Target region to analyze
            product: Optional product/service filter
            goal: Optional campaign goal filter
            
        Returns:
            Dict with content suggestions including:
            - suggested_content: List of content examples that worked well
            - tone_recommendations: What tone resonated with the audience
            - cta_suggestions: Effective call-to-actions
            - content_tips: Specific tips based on feedback
        """
        if self.combined_df is None or self.content_df is None:
            return {"error": "Data not loaded"}
        
        # Filter campaigns by region and optionally product/goal
        region_campaigns = self.combined_df.copy()
        filters_applied = []
        
        if region and region not in ["All Regions", ""]:
            filtered = region_campaigns[
                region_campaigns['region'].str.contains(region, case=False, na=False)
            ]
            if not filtered.empty:
                region_campaigns = filtered
                filters_applied.append(f"region={region}")
        
        if product:
            filtered = region_campaigns[
                region_campaigns['product'].str.contains(product, case=False, na=False)
            ]
            if not filtered.empty:
                region_campaigns = filtered
                filters_applied.append(f"product={product}")
        
        if goal and goal not in ["Select...", "Any Goal", ""]:
            filtered = region_campaigns[
                region_campaigns['campaign_objective'].str.contains(goal, case=False, na=False)
            ]
            if not filtered.empty:
                region_campaigns = filtered
                filters_applied.append(f"goal={goal}")
        
        # If still empty after all filters, use all campaigns (best performers)
        if region_campaigns.empty:
            logger.warning(f"No campaigns matched filters, using top performers from all campaigns")
            region_campaigns = self.combined_df.copy()
            filters_applied = ["all campaigns (no exact filter match)"]
        
        # Get top performing campaigns (by ROI)
        top_campaigns = region_campaigns.nlargest(20, 'roi')
        top_campaign_ids = top_campaigns['campaign_id'].tolist()
        
        # Get content for these campaigns
        top_content = self.content_df[
            self.content_df['campaign_id'].isin(top_campaign_ids)
        ]
        
        # Analyze feedback for these campaigns
        positive_feedback = pd.DataFrame()
        if self.feedback_df is not None:
            campaign_feedback = self.feedback_df[
                self.feedback_df['campaign_id'].isin(top_campaign_ids)
            ]
            positive_feedback = campaign_feedback[
                campaign_feedback['sentiment'].isin(['Positive', 'Very Positive'])
            ]
        
        # If no LLM, return basic analysis
        if self.llm_client is None:
            return self._get_basic_content_suggestions(top_content, top_campaigns)
        
        # Prepare content examples for LLM
        content_examples = []
        for _, row in top_content.head(10).iterrows():
            content_examples.append({
                "text": row.get('content_text', 'N/A')[:200],
                "tone": row.get('tone', 'N/A'),
                "cta": row.get('cta', 'N/A')
            })
        
        # Prepare campaign performance context
        campaign_context = []
        for _, row in top_campaigns.head(5).iterrows():
            campaign_context.append({
                "name": row.get('campaign_name', 'N/A'),
                "roi": row.get('roi', 0),
                "audience": row.get('audience_segment', 'N/A'),
                "channel": row.get('channel', 'N/A'),
                "region": row.get('region', 'N/A'),
                "product": row.get('product', 'N/A')
            })
        
        filter_desc = ', '.join(filters_applied) if filters_applied else "all top-performing campaigns"
        
        prompt = f"""
Analyze the following successful campaign content and provide content suggestions for a new campaign.

Filters Applied: {filter_desc}

Top Performing Campaigns:
{json.dumps(campaign_context, indent=2)}

Content Examples from Successful Campaigns:
{json.dumps(content_examples, indent=2)}

Target Region: {region if region and region != "All Regions" else "Pan India (all regions)"}
{f"Product Focus: {product}" if product else ""}
{f"Campaign Goal: {goal}" if goal and goal not in ['Any Goal', 'Select...'] else ""}

Positive Feedback Count: {len(positive_feedback)}

Based on this data, provide content suggestions in the following JSON format:
{{
    "suggested_content": [
        {{
            "headline": "Example headline text",
            "body_copy": "Example body copy that worked well",
            "why_it_works": "Brief explanation"
        }}
    ],
    "tone_recommendations": {{
        "primary_tone": "The tone that works best",
        "avoid_tones": ["Tones to avoid"],
        "reasoning": "Why this tone works for this region"
    }},
    "cta_suggestions": [
        {{
            "cta_text": "Example CTA",
            "context": "When to use this CTA"
        }}
    ],
    "content_tips": [
        "Specific tip based on what worked"
    ],
    "summary": "Brief summary of content strategy for this region"
}}
"""
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert marketing content strategist. Analyze successful campaign content and provide actionable content suggestions. Return valid JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_completion_tokens=1500
            )
            
            response_text = response.choices[0].message.content
            
            # Extract JSON
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            suggestions = json.loads(response_text.strip())
            suggestions['region'] = region if region and region != "All Regions" else "All Regions"
            suggestions['campaigns_analyzed'] = len(top_campaigns)
            suggestions['filters_applied'] = filters_applied if filters_applied else ["Top performers from all campaigns"]
            logger.info(f"Generated content suggestions with filters: {filters_applied}")
            return suggestions
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse content suggestions: {e}")
            result = self._get_basic_content_suggestions(top_content, top_campaigns)
            result['filters_applied'] = filters_applied if filters_applied else ["Top performers"]
            return result
        except Exception as e:
            logger.error(f"Error generating content suggestions: {e}")
            result = self._get_basic_content_suggestions(top_content, top_campaigns)
            result['filters_applied'] = filters_applied if filters_applied else ["Top performers"]
            return result
    
    def _get_basic_content_suggestions(self, content_df: pd.DataFrame, campaigns_df: pd.DataFrame) -> Dict:
        """Generate basic content suggestions without LLM."""
        suggestions = {
            "suggested_content": [],
            "tone_recommendations": {"primary_tone": "Professional", "reasoning": "Based on data analysis"},
            "cta_suggestions": [],
            "content_tips": ["AI suggestions unavailable - showing sample content from top campaigns"],
            "summary": "Sample content from highest performing campaigns"
        }
        
        # Get sample content
        if not content_df.empty:
            for _, row in content_df.head(3).iterrows():
                suggestions["suggested_content"].append({
                    "headline": row.get('content_text', 'N/A')[:100],
                    "body_copy": row.get('content_text', 'N/A'),
                    "why_it_works": f"From campaign with {row.get('tone', 'N/A')} tone"
                })
            
            # Get popular tones
            tone_counts = content_df['tone'].value_counts()
            if not tone_counts.empty:
                suggestions["tone_recommendations"]["primary_tone"] = tone_counts.index[0]
            
            # Get popular CTAs
            cta_counts = content_df['cta'].value_counts().head(3)
            for cta in cta_counts.index:
                suggestions["cta_suggestions"].append({
                    "cta_text": cta,
                    "context": "Frequently used in successful campaigns"
                })
        
        return suggestions


def main():
    """Main entry point for testing the Similar Campaign Finder."""
    print("\n" + "="*60)
    print("  SIMILAR CAMPAIGN FINDER - Marketing Analytics AI")
    print("="*60 + "\n")
    
    # Initialize finder
    finder = SimilarCampaignFinder()
    
    # Build index (will load from cache if exists)
    print("[1/3] Building/Loading campaign index...")
    finder.build_index()
    
    # Example searches
    test_queries = [
        "Festival loan campaign for salaried users",
        "Credit card upgrade for premium customers",
        "Health insurance for senior citizens",
        "Business loan for SMB owners"
    ]
    
    print("\n[2/3] Running example searches...\n")
    
    for query in test_queries:
        results = finder.search_and_display(query, top_k=5)
    
    print("[3/3] Done!\n")
    
    # Interactive mode
    print("Enter your own queries (type 'quit' to exit):\n")
    while True:
        query = input("🔍 Search query: ").strip()
        if query.lower() in ['quit', 'exit', 'q']:
            break
        if query:
            finder.search_and_display(query, top_k=5)


if __name__ == "__main__":
    main()
