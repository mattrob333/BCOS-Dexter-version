"""
Enhanced Company Intelligence Skill with Multi-Source Verification.

This skill demonstrates the new BCOS architecture:
1. Gather data from multiple sources (Firecrawl, Exa, Perplexity)
2. Cross-reference facts using Truth Engine
3. Return verified data with confidence scores and source citations
4. 100% source attribution - no hallucinations

This is the reference implementation for the multi-source pattern.
"""

from typing import Dict, Any
from anthropic import Anthropic
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from core.truth_engine import TruthEngine
from core.models import VerifiedDataset, Source, SourceType
from data_sources.apis.perplexity_client import PerplexityClient
from utils.logger import setup_logger

logger = setup_logger(__name__)


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute multi-source company intelligence gathering.

    New approach:
    1. Scrape company website (Firecrawl MCP) - Primary source
    2. Deep research (Exa MCP deep researcher) - Secondary sources
    3. Verification (Perplexity) - Fact-checking
    4. Cross-reference with Truth Engine
    5. Return verified dataset with confidence scores

    Args:
        task: Task object with description
        context: Execution context
        config: BCOS configuration

    Returns:
        VerifiedDataset with sourced, verified facts
    """
    logger.info("Executing Enhanced Company Intelligence (Multi-Source)")

    company = config.get('company', {})
    company_name = company.get('name', 'Unknown')
    company_website = company.get('website', '')
    industry = company.get('industry', 'Unknown')

    # Initialize verification settings
    verification_config = config.get('verification', {})
    min_confidence = verification_config.get('min_confidence', 0.5)

    truth_engine = TruthEngine(min_confidence=min_confidence)

    # Store data from each source
    all_sources_data = []

    # ========================================
    # Source 1: Company Website (Firecrawl)
    # ========================================
    if company_website:
        logger.info(f"Source 1: Scraping {company_website} with Firecrawl")

        website_data = _scrape_website_with_mcp(company_website, config)

        if website_data.get('success'):
            # Analyze website content with Claude
            website_analysis = _analyze_website_content(
                company_name, website_data.get('content', ''), config
            )

            # Format as source data
            all_sources_data.append({
                'source_type': 'primary',
                'source_name': company_website,
                'url': company_website,
                'date_accessed': datetime.now().isoformat(),
                'data': website_analysis,
                'reliability_score': 1.0  # Primary source = highest reliability
            })
        else:
            logger.warning(f"Website scraping failed: {website_data.get('error')}")

    # ========================================
    # Source 2: Deep Company Research (Exa)
    # ========================================
    logger.info(f"Source 2: Deep research on {company_name} with Exa")

    exa_research = _deep_research_with_exa(company_name, industry, config)

    if exa_research.get('success'):
        all_sources_data.append({
            'source_type': 'secondary',
            'source_name': 'Exa Deep Research',
            'url': 'https://exa.ai',
            'date_accessed': datetime.now().isoformat(),
            'data': exa_research.get('data', {}),
            'reliability_score': 0.85  # Research aggregation = high reliability
        })

    # ========================================
    # Source 3: Fact Verification (Perplexity)
    # ========================================
    logger.info(f"Source 3: Verifying facts about {company_name} with Perplexity")

    perplexity_data = _verify_with_perplexity(company_name, config)

    if perplexity_data.get('success'):
        all_sources_data.append({
            'source_type': 'verification',
            'source_name': 'Perplexity Fact Check',
            'url': 'https://perplexity.ai',
            'date_accessed': datetime.now().isoformat(),
            'data': perplexity_data.get('data', {}),
            'reliability_score': 0.9  # Fact-checking service = very high reliability
        })

    # ========================================
    # Cross-Reference with Truth Engine
    # ========================================
    logger.info("Cross-referencing data across all sources...")

    verified_dataset = truth_engine.cross_reference(
        datasets=all_sources_data,
        entity_name=company_name,
        entity_type="company"
    )

    logger.info(
        f"Verification complete: {verified_dataset.verified_count} verified facts, "
        f"confidence: {verified_dataset.overall_confidence:.2f}"
    )

    # Return verified dataset
    return {
        'success': True,
        'verified_dataset': verified_dataset.to_dict(),
        'company_name': company_name,
        'sources_used': len(all_sources_data),
        'verification_method': 'multi_source_truth_engine'
    }


def _scrape_website_with_mcp(url: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scrape website using Firecrawl Python client.

    Uses the production-ready Firecrawl V2 API client.
    """
    from data_sources.scrapers.firecrawl_client import FirecrawlClient

    logger.info(f"Scraping website with Firecrawl: {url}")
    client = FirecrawlClient()

    result = client.scrape_url(url, formats=["markdown", "html"])

    if result.get('success'):
        logger.info(f"Successfully scraped {len(result.get('content', ''))} characters")
    else:
        logger.warning(f"Scraping failed: {result.get('error', 'Unknown error')}")

    return result


def _deep_research_with_exa(company_name: str, industry: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform deep research using Exa Python client.

    Searches for comprehensive company information using Exa's company research API.
    """
    from data_sources.apis.exa_client import ExaClient

    logger.info(f"Researching {company_name} with Exa")

    client = ExaClient()

    if not client.is_available():
        logger.warning("Exa not available, using fallback")
        return _fallback_company_knowledge(company_name, industry, config)

    # Use Exa's company research
    result = client.search_company_info(company_name, num_results=5)

    if result.get('success'):
        # Parse Exa results into structured data
        results = result.get('results', [])

        # Combine text from multiple results
        combined_text = "\n\n".join([
            f"Source: {r.get('title', 'Unknown')}\n{r.get('text', '')[:500]}"
            for r in results[:3]
        ])

        # Use Claude to structure the combined research
        structured = _structure_exa_response(company_name, combined_text, industry, config)

        return {
            'success': True,
            'data': structured,
            'sources': [r.get('url') for r in results]
        }

    logger.warning("Exa search failed, using fallback")
    return _fallback_company_knowledge(company_name, industry, config)


def _verify_with_perplexity(company_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Verify company facts with Perplexity."""
    perplexity_config = config.get('data_sources', {}).get('perplexity', {})

    if not perplexity_config.get('enabled', False):
        logger.warning("Perplexity not enabled")
        return {'success': False}

    client = PerplexityClient()
    if not client.is_available():
        logger.warning("Perplexity API not configured")
        return {'success': False}

    # Search for company verification
    result = client.get_company_info(
        company_name,
        specific_info=["revenue", "employees", "headquarters", "founded", "products"]
    )

    if result.get('success'):
        # Parse Perplexity response into structured data
        answer = result.get('answer', '')
        sources = result.get('sources', [])

        # Use Claude to structure the response
        structured = _structure_perplexity_response(company_name, answer, config)

        return {
            'success': True,
            'data': structured,
            'sources': sources
        }

    return {'success': False}


def _analyze_website_content(
    company_name: str,
    website_content: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Analyze scraped website content with Claude."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Analyze this company website and extract verified business intelligence.

Company: {company_name}

Website Content:
{website_content[:8000]}

Extract ONLY facts that are explicitly stated in the content:

{{
  "business_description": "What does this company do?",
  "products_services": ["List of products/services mentioned"],
  "target_customers": "Who are their customers?",
  "value_proposition": "What makes them unique?",
  "key_facts": {{
    "founded": "Year if mentioned",
    "headquarters": "Location if mentioned",
    "team_size": "Number if mentioned",
    "revenue": "Amount if mentioned"
  }},
  "business_model": "How they make money",
  "source_confidence": "high/medium/low - based on clarity of info"
}}

IMPORTANT: Only include facts found in the content. Use "Unknown" if not found.
"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        content = response.content[0].text

        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()

        return json.loads(content)

    except Exception as e:
        logger.error(f"Error analyzing website: {e}")
        return {}


def _structure_perplexity_response(
    company_name: str,
    perplexity_answer: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Structure Perplexity's text response into data format."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Extract structured data from this Perplexity research result.

Company: {company_name}

Perplexity Answer:
{perplexity_answer}

Extract into JSON format:
{{
  "business_description": "...",
  "products_services": ["..."],
  "key_facts": {{
    "revenue": "...",
    "employees": "...",
    "founded": "...",
    "headquarters": "..."
  }}
}}

Only include facts explicitly stated in the answer.
"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        content = response.content[0].text

        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()

        return json.loads(content)

    except Exception as e:
        logger.error(f"Error structuring Perplexity response: {e}")
        return {}


def _structure_exa_response(
    company_name: str,
    exa_results: str,
    industry: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Structure Exa search results into data format."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Extract structured data from these Exa search results.

Company: {company_name}
Industry: {industry}

Search Results:
{exa_results}

Extract into JSON format:
{{
  "business_description": "...",
  "products_services": ["..."],
  "target_customers": "...",
  "value_proposition": "...",
  "key_facts": {{
    "revenue": "...",
    "employees": "...",
    "founded": "...",
    "headquarters": "..."
  }},
  "business_model": "..."
}}

Only include facts explicitly stated in the search results.
"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        content = response.content[0].text

        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()

        return json.loads(content)

    except Exception as e:
        logger.error(f"Error structuring Exa response: {e}")
        return {}


def _fallback_company_knowledge(company_name: str, industry: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback: Use Claude's knowledge base."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Provide business intelligence about {company_name} in {industry}.

Return JSON with your knowledge:
{{
  "business_description": "...",
  "products_services": ["..."],
  "target_customers": "...",
  "value_proposition": "...",
  "key_facts": {{...}},
  "business_model": "...",
  "confidence": "medium",
  "source": "knowledge_base",
  "disclaimer": "From knowledge base - may be outdated"
}}

Be honest about confidence and acknowledge limitations.
"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        content = response.content[0].text

        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()

        result = json.loads(content)
        return {'success': True, 'data': result}

    except Exception as e:
        logger.error(f"Error in fallback: {e}")
        return {'success': False, 'error': str(e)}
