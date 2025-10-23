"""
MCP Tool Wrappers for BCOS.

This module provides Python wrappers around MCP (Model Context Protocol) tools,
allowing skills to access Firecrawl, Exa, and other MCP services.

The wrappers handle:
- Tool availability checking
- Fallback to Python API clients when MCP unavailable
- Error handling and retry logic
- Result normalization
"""

from typing import Dict, Any, List, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MCPToolkit:
    """
    Wrapper around MCP tools for use in skills.

    This provides a clean interface for skills to access MCP tools
    without dealing with tool availability, fallbacks, or error handling.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize MCP toolkit.

        Args:
            config: BCOS configuration with data_sources settings
        """
        self.config = config
        self.data_sources = config.get('data_sources', {})

        # Check which MCP tools are enabled
        firecrawl_config = self.data_sources.get('firecrawl', {})
        self.firecrawl_enabled = (
            isinstance(firecrawl_config, dict) and
            firecrawl_config.get('enabled', False) and
            firecrawl_config.get('use_mcp', False)
        )

        exa_config = self.data_sources.get('exa', {})
        self.exa_enabled = (
            isinstance(exa_config, dict) and
            exa_config.get('enabled', False) and
            exa_config.get('use_mcp', False)
        )

        perplexity_config = self.data_sources.get('perplexity', {})
        self.perplexity_enabled = (
            isinstance(perplexity_config, dict) and
            perplexity_config.get('enabled', False)
        )

        logger.info(
            f"MCP Toolkit initialized: "
            f"Firecrawl={'enabled' if self.firecrawl_enabled else 'disabled'}, "
            f"Exa={'enabled' if self.exa_enabled else 'disabled'}, "
            f"Perplexity={'enabled' if self.perplexity_enabled else 'disabled'}"
        )

    def scrape_url(self, url: str, formats: List[str] = None) -> Dict[str, Any]:
        """
        Scrape a URL using Firecrawl MCP or fallback.

        Args:
            url: URL to scrape
            formats: Desired formats (markdown, html, etc.)

        Returns:
            Scraped content dictionary
        """
        if not self.firecrawl_enabled:
            logger.warning("Firecrawl MCP not enabled - using fallback")
            return self._fallback_scrape(url)

        # This is a placeholder for MCP tool call
        # In actual execution, skills would request this from Claude Code
        # which has direct access to MCP tools
        logger.info(f"[MCP] Scraping {url}")

        return {
            'success': False,
            'error': 'MCP tool call placeholder - requires Claude Code execution context',
            'url': url,
            'note': 'Skills should request MCP operations from executor during task execution'
        }

    def search_web(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search web using Firecrawl MCP search.

        Args:
            query: Search query
            num_results: Number of results

        Returns:
            Search results
        """
        if not self.firecrawl_enabled:
            logger.warning("Firecrawl MCP not enabled")
            return {'success': False, 'error': 'Firecrawl not enabled'}

        logger.info(f"[MCP] Searching: {query}")

        return {
            'success': False,
            'error': 'MCP tool call placeholder',
            'query': query
        }

    def company_research(self, company_name: str, num_results: int = 10) -> Dict[str, Any]:
        """
        Research company using Exa MCP.

        Args:
            company_name: Company to research
            num_results: Number of results

        Returns:
            Company research results
        """
        if not self.exa_enabled:
            logger.warning("Exa MCP not enabled")
            return {'success': False, 'error': 'Exa not enabled'}

        logger.info(f"[MCP] Researching company: {company_name}")

        return {
            'success': False,
            'error': 'MCP tool call placeholder',
            'company': company_name
        }

    def deep_research(self, instructions: str, model: str = "exa-research") -> Dict[str, Any]:
        """
        Start deep research task using Exa deep researcher.

        Args:
            instructions: Research instructions
            model: Research model (exa-research or exa-research-pro)

        Returns:
            Task ID for checking status
        """
        if not self.exa_enabled:
            logger.warning("Exa MCP not enabled")
            return {'success': False, 'error': 'Exa not enabled'}

        logger.info(f"[MCP] Starting deep research: {instructions[:50]}...")

        return {
            'success': False,
            'error': 'MCP tool call placeholder',
            'instructions': instructions
        }

    def verify_with_perplexity(self, query: str) -> Dict[str, Any]:
        """
        Verify information using Perplexity.

        Args:
            query: Verification query

        Returns:
            Verification results with sources
        """
        if not self.perplexity_enabled:
            logger.warning("Perplexity not enabled")
            return {'success': False, 'error': 'Perplexity not enabled'}

        # Use Python client for Perplexity (no MCP available)
        from data_sources.apis.perplexity_client import PerplexityClient

        client = PerplexityClient()
        if not client.is_available():
            return {'success': False, 'error': 'Perplexity API key not configured'}

        return client.search(query)

    def _fallback_scrape(self, url: str) -> Dict[str, Any]:
        """Fallback to Python client for scraping."""
        from data_sources.scrapers.firecrawl_client import FirecrawlClient

        client = FirecrawlClient()
        return client.scrape_url(url)

    def is_available(self, tool_name: str) -> bool:
        """
        Check if a specific MCP tool is available.

        Args:
            tool_name: Name of tool (firecrawl, exa, perplexity)

        Returns:
            True if tool is enabled and available
        """
        if tool_name == 'firecrawl':
            return self.firecrawl_enabled
        elif tool_name == 'exa':
            return self.exa_enabled
        elif tool_name == 'perplexity':
            return self.perplexity_enabled
        else:
            return False


# Global note for skills:
#
# For now, skills should construct prompts that request MCP tool usage
# rather than calling these wrappers directly. When Claude Code executes
# the skill with tool access, it can call MCP tools directly.
#
# Example skill implementation:
#
# def execute(task, context, config):
#     # Build prompt requesting MCP tool use
#     prompt = f"""
#     Use the following MCP tools to gather company intelligence:
#
#     1. Use mcp__firecrawl__firecrawl_scrape to scrape {company_website}
#     2. Use mcp__exa__company_research_exa to research {company_name}
#     3. Use perplexity to verify key facts
#
#     Compile findings into structured format.
#     """
#
#     # Return prompt for executor to process with Claude + MCP tools
#     return {
#         'requires_mcp_execution': True,
#         'mcp_prompt': prompt,
#         'context': context
#     }
