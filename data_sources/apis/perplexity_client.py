"""
Perplexity API Client for fact verification and web search.

Perplexity provides AI-powered search with source citations,
making it ideal for fact-checking and verification tasks.
"""

from typing import Dict, Any, List, Optional
import os
import requests
from datetime import datetime

from utils.logger import setup_logger

logger = setup_logger(__name__)


class PerplexityClient:
    """
    Client for Perplexity API.

    Provides methods to:
    - Search for information with source citations
    - Verify specific facts
    - Get recent news and developments
    """

    def __init__(self, api_key: str = None):
        """
        Initialize Perplexity client.

        Args:
            api_key: Perplexity API key (defaults to PERPLEXITY_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')

        if not self.api_key:
            logger.warning("Perplexity API key not set - verification features will be unavailable")
            self.available = False
            return

        self.base_url = "https://api.perplexity.ai"
        self.available = True
        logger.info("Perplexity client initialized successfully")

    def search(
        self,
        query: str,
        focus: str = "internet",  # "internet", "scholar", "writing", "wolfram", "youtube"
        num_results: int = 5
    ) -> Dict[str, Any]:
        """
        Search using Perplexity with source citations.

        Args:
            query: Search query
            focus: Search focus/mode
            num_results: Number of results to return

        Returns:
            Search results with sources and citations
        """
        if not self.available:
            logger.warning("Perplexity not available - skipping search")
            return {'success': False, 'error': 'Perplexity API not configured'}

        try:
            logger.info(f"Perplexity search: {query}")

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar-pro",  # Pro search model for complex queries (Feb 2025)
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a precise fact-checker. Provide accurate information with specific sources."
                        },
                        {
                            "role": "user",
                            "content": query
                        }
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.2,  # Low temperature for factual accuracy
                    "top_p": 0.9,
                    "search_mode": "web",  # Enable web search
                    "search_recency_filter": "month",  # Prefer recent results
                    "return_images": False,
                    "return_related_questions": False
                },
                timeout=30
            )

            # Check for errors before parsing
            if response.status_code != 200:
                error_body = response.text
                logger.error(f"Perplexity API error: {response.status_code}")
                logger.error(f"Response body: {error_body}")
                response.raise_for_status()

            data = response.json()

            # Extract answer and search results (citations returned by default)
            answer = data['choices'][0]['message']['content']

            # New API format uses 'search_results' field with title, url, date
            search_results = data.get('search_results', [])

            # Parse search results into structured format
            sources = []
            for result in search_results[:num_results]:
                sources.append({
                    'url': result.get('url', ''),
                    'title': result.get('title', ''),
                    'date': result.get('date', ''),
                    'source_type': 'verification',
                    'source_name': 'Perplexity Search',
                    'date_accessed': datetime.now().isoformat(),
                })

            return {
                'success': True,
                'query': query,
                'answer': answer,
                'sources': sources,
                'num_sources': len(sources),
                'source': 'perplexity'
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Perplexity API request error: {e}")
            return {
                'success': False,
                'error': str(e),
                'source': 'perplexity'
            }
        except Exception as e:
            logger.error(f"Perplexity search error: {e}")
            return {
                'success': False,
                'error': str(e),
                'source': 'perplexity'
            }

    def verify_fact(
        self,
        claim: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Verify a specific fact or claim.

        Args:
            claim: The fact to verify (e.g., "Stripe processes $1 trillion annually")
            context: Additional context (e.g., company name, industry)

        Returns:
            Verification result with confidence and sources
        """
        if not self.available:
            logger.warning("Perplexity not available - skipping verification")
            return {'success': False, 'error': 'Perplexity API not configured'}

        try:
            # Construct verification query
            query = f"Verify this fact: {claim}"
            if context:
                query += f" Context: {context}"
            query += " Is this accurate? Provide specific sources and verification."

            logger.info(f"Verifying fact: {claim}")

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar-pro",  # Pro search model (Feb 2025)
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a fact-checker. Verify claims with precision. State if verified, partially verified, or false. Always cite sources."
                        },
                        {
                            "role": "user",
                            "content": query
                        }
                    ],
                    "max_tokens": 1500,
                    "temperature": 0.1,  # Very low for fact-checking
                    "search_mode": "web",
                    "search_recency_filter": "month",
                    "return_images": False,
                    "return_related_questions": False
                },
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            answer = data['choices'][0]['message']['content']
            search_results = data.get('search_results', [])

            # Analyze verification result
            answer_lower = answer.lower()
            if any(word in answer_lower for word in ['verified', 'accurate', 'correct', 'true']):
                verified = True
                confidence = 0.85
            elif any(word in answer_lower for word in ['partially', 'mostly', 'generally']):
                verified = True
                confidence = 0.6
            elif any(word in answer_lower for word in ['false', 'incorrect', 'inaccurate', 'not verified']):
                verified = False
                confidence = 0.2
            else:
                verified = False
                confidence = 0.5

            sources = []
            for result in search_results:
                sources.append({
                    'url': result.get('url', ''),
                    'title': result.get('title', ''),
                    'date': result.get('date', ''),
                    'source_type': 'verification',
                    'source_name': 'Perplexity Fact Check',
                    'date_accessed': datetime.now().isoformat(),
                })

            return {
                'success': True,
                'claim': claim,
                'verified': verified,
                'confidence': confidence,
                'verification_result': answer,
                'sources': sources,
                'num_sources': len(sources),
                'source': 'perplexity'
            }

        except Exception as e:
            logger.error(f"Perplexity fact verification error: {e}")
            return {
                'success': False,
                'error': str(e),
                'source': 'perplexity'
            }

    def get_company_info(
        self,
        company_name: str,
        specific_info: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get company information with verification.

        Args:
            company_name: Name of the company
            specific_info: Specific pieces of information to retrieve
                          (e.g., ["revenue", "employees", "headquarters"])

        Returns:
            Company information with sources
        """
        if not self.available:
            return {'success': False, 'error': 'Perplexity API not configured'}

        if specific_info:
            info_list = ", ".join(specific_info)
            query = f"What are the current {info_list} for {company_name}? Provide specific, verifiable data with sources."
        else:
            query = f"Provide current verified information about {company_name}: business model, revenue, employees, products, headquarters, founded. Use recent sources."

        return self.search(query, num_results=5)

    def get_recent_news(
        self,
        topic: str,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Get recent news about a topic.

        Args:
            topic: Topic to search for (e.g., company name, industry)
            days_back: How many days back to search

        Returns:
            Recent news with sources
        """
        if not self.available:
            return {'success': False, 'error': 'Perplexity API not configured'}

        query = f"What are the latest news and developments about {topic} in the past {days_back} days? Provide specific sources."

        return self.search(query, num_results=10)

    def is_available(self) -> bool:
        """Check if Perplexity is available and configured."""
        return self.available
