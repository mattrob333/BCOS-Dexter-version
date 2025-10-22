"""
Firecrawl client for deep website scraping.

Firecrawl provides intelligent web scraping with JavaScript rendering,
PDF extraction, and markdown conversion.
"""

from typing import Dict, Any, Optional, List
import os
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FirecrawlClient:
    """
    Client for Firecrawl API.

    Provides methods to:
    - Scrape single pages
    - Crawl entire websites
    - Extract structured data
    """

    def __init__(self, api_key: str = None):
        """
        Initialize Firecrawl client.

        Args:
            api_key: Firecrawl API key (defaults to FIRECRAWL_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')

        if not self.api_key:
            logger.warning("Firecrawl API key not set - scraping will be limited")

        # Try to import firecrawl
        try:
            from firecrawl import FirecrawlApp
            self.client = FirecrawlApp(api_key=self.api_key) if self.api_key else None
            self.available = True
        except ImportError:
            logger.warning("Firecrawl library not installed - install with: pip install firecrawl-py")
            self.client = None
            self.available = False

    def scrape_url(self, url: str, formats: List[str] = None) -> Dict[str, Any]:
        """
        Scrape a single URL.

        Args:
            url: URL to scrape
            formats: Desired output formats (markdown, html, rawHtml, screenshot, etc.)

        Returns:
            Scraped content dictionary
        """
        if not self.available or not self.client:
            logger.warning("Firecrawl not available - using fallback scraping")
            return self._fallback_scrape(url)

        try:
            logger.info(f"Scraping {url} with Firecrawl")

            # Default to markdown format
            if formats is None:
                formats = ['markdown', 'html']

            result = self.client.scrape_url(
                url,
                params={'formats': formats}
            )

            return {
                'success': True,
                'url': url,
                'content': result.get('markdown', result.get('html', '')),
                'metadata': result.get('metadata', {}),
                'source': 'firecrawl'
            }

        except Exception as e:
            logger.error(f"Firecrawl scraping error: {e}")
            return self._fallback_scrape(url)

    def crawl_website(
        self,
        url: str,
        max_pages: int = 10,
        include_patterns: List[str] = None
    ) -> Dict[str, Any]:
        """
        Crawl multiple pages of a website.

        Args:
            url: Starting URL
            max_pages: Maximum number of pages to crawl
            include_patterns: URL patterns to include (e.g., ['/blog/*', '/docs/*'])

        Returns:
            Dictionary with crawled pages
        """
        if not self.available or not self.client:
            logger.warning("Firecrawl not available - scraping single page only")
            return {'pages': [self._fallback_scrape(url)]}

        try:
            logger.info(f"Crawling {url} with Firecrawl (max {max_pages} pages)")

            params = {
                'limit': max_pages,
            }

            if include_patterns:
                params['includePaths'] = include_patterns

            result = self.client.crawl_url(url, params=params)

            pages = []
            for page in result.get('data', []):
                pages.append({
                    'url': page.get('url'),
                    'content': page.get('markdown', page.get('html', '')),
                    'metadata': page.get('metadata', {}),
                })

            return {
                'success': True,
                'base_url': url,
                'pages': pages,
                'total_pages': len(pages),
                'source': 'firecrawl'
            }

        except Exception as e:
            logger.error(f"Firecrawl crawling error: {e}")
            return {'pages': [self._fallback_scrape(url)]}

    def _fallback_scrape(self, url: str) -> Dict[str, Any]:
        """
        Fallback scraping using requests + BeautifulSoup.

        Used when Firecrawl is not available or fails.
        """
        try:
            import requests
            from bs4 import BeautifulSoup

            logger.info(f"Using fallback scraping for {url}")

            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; BCOS/1.0)'
            })
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for element in soup(['script', 'style', 'nav', 'footer']):
                element.decompose()

            # Get text content
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            # Get title
            title = soup.title.string if soup.title else 'No title'

            return {
                'success': True,
                'url': url,
                'content': text[:10000],  # Limit to 10k chars
                'metadata': {
                    'title': title,
                },
                'source': 'fallback'
            }

        except Exception as e:
            logger.error(f"Fallback scraping error: {e}")
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'source': 'fallback'
            }

    def is_available(self) -> bool:
        """Check if Firecrawl is available and configured."""
        return self.available and self.client is not None
