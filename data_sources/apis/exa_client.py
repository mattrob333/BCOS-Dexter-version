"""
Exa API client for semantic search and company research.

Exa provides neural search for finding high-quality, relevant web content
about companies, markets, and industries.
"""

from typing import Dict, Any, Optional, List
import os
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ExaClient:
    """
    Client for Exa API.

    Provides methods to:
    - Search for company information
    - Find similar companies
    - Get recent news and content
    - Semantic search for market intelligence
    """

    def __init__(self, api_key: str = None):
        """
        Initialize Exa client.

        Args:
            api_key: Exa API key (defaults to EXA_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('EXA_API_KEY')

        if not self.api_key:
            logger.warning("Exa API key not set - semantic search will be unavailable")
            self.available = False
            self.client = None
            return

        # Try to import exa_py
        try:
            from exa_py import Exa
            self.client = Exa(api_key=self.api_key)
            self.available = True
            logger.info("Exa client initialized successfully")
        except ImportError:
            logger.warning("exa_py library not installed - install with: pip install exa_py")
            self.client = None
            self.available = False

    def search_company_info(
        self,
        company_name: str,
        num_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for information about a company.

        Args:
            company_name: Name of the company
            num_results: Number of results to return

        Returns:
            Search results with URLs and content
        """
        if not self.available or not self.client:
            logger.warning("Exa not available - skipping company info search")
            return {'success': False, 'error': 'Exa not available'}

        try:
            query = f"{company_name} company overview products business model"

            logger.info(f"Searching Exa for: {query}")

            results = self.client.search_and_contents(
                query,
                num_results=num_results,
                text=True,
                highlights=True
            )

            parsed_results = []
            for result in results.results:
                parsed_results.append({
                    'url': result.url,
                    'title': result.title,
                    'text': result.text[:2000] if result.text else '',  # First 2k chars
                    'highlights': result.highlights if hasattr(result, 'highlights') else [],
                    'published_date': result.published_date if hasattr(result, 'published_date') else None,
                    'score': result.score if hasattr(result, 'score') else None
                })

            return {
                'success': True,
                'query': query,
                'results': parsed_results,
                'num_results': len(parsed_results),
                'source': 'exa'
            }

        except Exception as e:
            logger.error(f"Exa search error: {e}")
            return {
                'success': False,
                'error': str(e),
                'source': 'exa'
            }

    def search_market_trends(
        self,
        industry: str,
        num_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for market trends and industry insights.

        Args:
            industry: Industry/market to research
            num_results: Number of results to return

        Returns:
            Search results about market trends
        """
        if not self.available or not self.client:
            logger.warning("Exa not available - skipping market trends search")
            return {'success': False, 'error': 'Exa not available'}

        try:
            query = f"{industry} market trends growth opportunities analysis 2024"

            logger.info(f"Searching Exa for market trends: {query}")

            results = self.client.search_and_contents(
                query,
                num_results=num_results,
                text=True,
                use_autoprompt=True  # Let Exa optimize the query
            )

            parsed_results = []
            for result in results.results:
                parsed_results.append({
                    'url': result.url,
                    'title': result.title,
                    'text': result.text[:2000] if result.text else '',
                    'published_date': result.published_date if hasattr(result, 'published_date') else None,
                })

            return {
                'success': True,
                'query': query,
                'results': parsed_results,
                'num_results': len(parsed_results),
                'source': 'exa'
            }

        except Exception as e:
            logger.error(f"Exa market trends search error: {e}")
            return {
                'success': False,
                'error': str(e),
                'source': 'exa'
            }

    def find_similar_companies(
        self,
        company_url: str,
        num_results: int = 10
    ) -> Dict[str, Any]:
        """
        Find companies similar to the given company.

        Args:
            company_url: URL of the company website
            num_results: Number of similar companies to find

        Returns:
            Similar companies based on content similarity
        """
        if not self.available or not self.client:
            logger.warning("Exa not available - skipping similar companies search")
            return {'success': False, 'error': 'Exa not available'}

        try:
            logger.info(f"Finding similar companies to: {company_url}")

            results = self.client.find_similar(
                url=company_url,
                num_results=num_results
            )

            parsed_results = []
            for result in results.results:
                parsed_results.append({
                    'url': result.url,
                    'title': result.title,
                    'score': result.score if hasattr(result, 'score') else None
                })

            return {
                'success': True,
                'base_url': company_url,
                'similar_companies': parsed_results,
                'num_results': len(parsed_results),
                'source': 'exa'
            }

        except Exception as e:
            logger.error(f"Exa similar companies search error: {e}")
            return {
                'success': False,
                'error': str(e),
                'source': 'exa'
            }

    def search_news(
        self,
        company_name: str,
        days_back: int = 30,
        num_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search for recent news about a company.

        Args:
            company_name: Name of the company
            days_back: How many days back to search
            num_results: Number of news articles to return

        Returns:
            Recent news articles about the company
        """
        if not self.available or not self.client:
            logger.warning("Exa not available - skipping news search")
            return {'success': False, 'error': 'Exa not available'}

        try:
            from datetime import datetime, timedelta

            start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

            query = f"{company_name} news"

            logger.info(f"Searching Exa for recent news: {query}")

            results = self.client.search_and_contents(
                query,
                num_results=num_results,
                text=True,
                start_published_date=start_date
            )

            parsed_results = []
            for result in results.results:
                parsed_results.append({
                    'url': result.url,
                    'title': result.title,
                    'text': result.text[:1000] if result.text else '',
                    'published_date': result.published_date if hasattr(result, 'published_date') else None,
                })

            return {
                'success': True,
                'query': query,
                'date_range': f"Last {days_back} days",
                'results': parsed_results,
                'num_results': len(parsed_results),
                'source': 'exa'
            }

        except Exception as e:
            logger.error(f"Exa news search error: {e}")
            return {
                'success': False,
                'error': str(e),
                'source': 'exa'
            }

    def is_available(self) -> bool:
        """Check if Exa is available and configured."""
        return self.available and self.client is not None
