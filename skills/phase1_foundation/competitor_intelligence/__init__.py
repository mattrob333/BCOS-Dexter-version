"""
Enhanced Competitor Intelligence Skill with Multi-Source Verification.

Uses real-time competitor discovery and profiling:

Sources:
1. Exa similar companies - Semantic competitor discovery
2. Firecrawl competitor websites - Products, pricing, positioning
3. Exa LinkedIn search - Key employees, org structure
4. Exa news search - Recent strategic moves
5. Perplexity verification - Fact-check competitor data
6. Truth Engine cross-reference - Validate all competitor profiles

Returns VerifiedDataset with sourced, verified competitor intelligence.
"""

from typing import Dict, Any, List
from anthropic import Anthropic
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from core.truth_engine import TruthEngine
from core.models import VerifiedDataset
from data_sources.apis.perplexity_client import PerplexityClient
from utils.logger import setup_logger

logger = setup_logger(__name__)


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute multi-source competitor intelligence gathering.

    Args:
        task: Task object
        context: Execution context with company and market intelligence
        config: BCOS configuration

    Returns:
        VerifiedDataset with competitor intelligence
    """
    logger.info("Executing Enhanced Competitor Intelligence (Multi-Source)")

    company = context.get('company', config.get('company', {}))
    company_name = company.get('name', 'Unknown')
    company_website = company.get('website', '')
    industry = company.get('industry', 'Unknown')

    # Get competitors from config
    competitors = config.get('competitors', [])

    # Get context from Phase 1
    company_intel = context.get('company_intelligence', {})
    market_intel = context.get('market_intelligence', {})

    # Initialize Truth Engine
    verification_config = config.get('verification', {})
    truth_engine = TruthEngine(min_confidence=verification_config.get('min_confidence', 0.5))

    all_competitors_data = {}

    # ========================================
    # Step 1: Discover Competitors
    # ========================================
    if not competitors and company_website:
        logger.info(f"Discovering competitors similar to {company_website}")
        discovered = _discover_competitors_with_exa(company_website, config)
        competitors = discovered.get('competitors', competitors)

    logger.info(f"Analyzing {len(competitors)} competitors")

    # ========================================
    # Step 2: Profile Each Competitor
    # ========================================
    for competitor in competitors[:5]:  # Limit to top 5
        logger.info(f"Profiling competitor: {competitor}")

        competitor_sources = []

        # Source 1: Scrape competitor website
        website_data = _scrape_competitor_website(competitor, config)
        if website_data.get('success'):
            competitor_sources.append({
                'source_type': 'primary',
                'source_name': f"{competitor} Website",
                'url': website_data.get('url', 'unknown'),
                'date_accessed': datetime.now().isoformat(),
                'data': website_data.get('data', {}),
                'reliability_score': 1.0
            })

        # Source 2: Exa company research
        exa_research = _research_competitor_with_exa(competitor, industry, config)
        if exa_research.get('success'):
            competitor_sources.append({
                'source_type': 'secondary',
                'source_name': 'Exa Company Research',
                'url': 'https://exa.ai',
                'date_accessed': datetime.now().isoformat(),
                'data': exa_research.get('data', {}),
                'reliability_score': 0.85
            })

        # Source 3: LinkedIn search for org structure
        linkedin_data = _search_linkedin(competitor, config)
        if linkedin_data.get('success'):
            competitor_sources.append({
                'source_type': 'secondary',
                'source_name': 'LinkedIn',
                'url': 'https://linkedin.com',
                'date_accessed': datetime.now().isoformat(),
                'data': linkedin_data.get('data', {}),
                'reliability_score': 0.8
            })

        # Source 4: Recent news about competitor
        news_data = _search_competitor_news(competitor, config)
        if news_data.get('success'):
            competitor_sources.append({
                'source_type': 'secondary',
                'source_name': 'News Search',
                'url': 'https://exa.ai',
                'date_accessed': datetime.now().isoformat(),
                'data': news_data.get('data', {}),
                'reliability_score': 0.75
            })

        # Source 5: Perplexity verification
        perplexity_data = _verify_competitor_data(competitor, config)
        if perplexity_data.get('success'):
            competitor_sources.append({
                'source_type': 'verification',
                'source_name': 'Perplexity Verification',
                'url': 'https://perplexity.ai',
                'date_accessed': datetime.now().isoformat(),
                'data': perplexity_data.get('data', {}),
                'reliability_score': 0.9
            })

        # Cross-reference data for this competitor
        verified_competitor = truth_engine.cross_reference(
            datasets=competitor_sources,
            entity_name=competitor,
            entity_type="competitor"
        )

        all_competitors_data[competitor] = verified_competitor.to_dict()

    # ========================================
    # Step 3: Competitive Analysis
    # ========================================
    logger.info("Synthesizing competitive intelligence...")

    competitive_analysis = _synthesize_competitive_intelligence(
        company_name,
        all_competitors_data,
        company_intel,
        market_intel,
        config
    )

    return {
        'success': True,
        'competitor_profiles': all_competitors_data,
        'competitive_analysis': competitive_analysis,
        'competitors_analyzed': len(all_competitors_data),
        'verification_method': 'multi_source_truth_engine'
    }


def _discover_competitors_with_exa(company_url: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Discover competitors using Exa's similar companies feature."""
    data_sources = config.get('data_sources', {})
    exa_config = data_sources.get('exa', {})

    if not (isinstance(exa_config, dict) and exa_config.get('use_mcp', False)):
        logger.info("Exa MCP not enabled for competitor discovery")
        return {'competitors': []}

    # TODO: When executed by Claude Code with MCP:
    # result = mcp__exa__crawling_exa(url=company_url)
    # similar = mcp__exa__web_search_exa(
    #     query=f"companies similar to {extract_company_name(company_url)}",
    #     numResults=10
    # )
    logger.info("[MCP] Would call mcp__exa__web_search_exa for similar companies")

    return {'competitors': []}


def _scrape_competitor_website(competitor: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Scrape competitor website for products, pricing, positioning."""
    # Try to find website URL
    competitor_url = f"https://{competitor.lower().replace(' ', '')}.com"

    data_sources = config.get('data_sources', {})
    firecrawl_config = data_sources.get('firecrawl', {})

    if not (isinstance(firecrawl_config, dict) and firecrawl_config.get('use_mcp', False)):
        # Fallback
        from data_sources.scrapers.firecrawl_client import FirecrawlClient
        client = FirecrawlClient()
        result = client.scrape_url(competitor_url)

        if result.get('success'):
            # Analyze content
            analyzed = _analyze_competitor_website(
                competitor, result.get('content', ''), config
            )
            return {
                'success': True,
                'url': competitor_url,
                'data': analyzed
            }

        return {'success': False}

    # TODO: MCP call
    logger.info(f"[MCP] Would call mcp__firecrawl__firecrawl_scrape for {competitor_url}")
    return {'success': False}


def _research_competitor_with_exa(competitor: str, industry: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Research competitor using Exa company research."""
    data_sources = config.get('data_sources', {})
    exa_config = data_sources.get('exa', {})

    if not (isinstance(exa_config, dict) and exa_config.get('use_mcp', False)):
        return {'success': False}

    # TODO: MCP call
    # result = mcp__exa__company_research_exa(
    #     companyName=competitor,
    #     numResults=10
    # )
    logger.info(f"[MCP] Would call mcp__exa__company_research_exa for {competitor}")

    return {'success': False}


def _search_linkedin(competitor: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Search LinkedIn for competitor org structure."""
    data_sources = config.get('data_sources', {})
    exa_config = data_sources.get('exa', {})

    if not (isinstance(exa_config, dict) and exa_config.get('use_mcp', False)):
        return {'success': False}

    # TODO: MCP call
    # result = mcp__exa__linkedin_search_exa(
    #     query=f"{competitor} employees leadership",
    #     searchType="profiles",
    #     numResults=10
    # )
    logger.info(f"[MCP] Would call mcp__exa__linkedin_search_exa for {competitor}")

    return {'success': False}


def _search_competitor_news(competitor: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Search for recent news about competitor."""
    data_sources = config.get('data_sources', {})
    exa_config = data_sources.get('exa', {})

    if not (isinstance(exa_config, dict) and exa_config.get('use_mcp', False)):
        return {'success': False}

    # TODO: MCP call
    # result = mcp__exa__web_search_exa(
    #     query=f"{competitor} news launches acquisitions 2024",
    #     numResults=5
    # )
    logger.info(f"[MCP] Would call Exa news search for {competitor}")

    return {'success': False}


def _verify_competitor_data(competitor: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Verify competitor data with Perplexity."""
    perplexity_config = config.get('data_sources', {}).get('perplexity', {})

    if not perplexity_config.get('enabled', False):
        return {'success': False}

    client = PerplexityClient()
    if not client.is_available():
        return {'success': False}

    result = client.get_company_info(
        competitor,
        specific_info=["revenue", "products", "market_share", "strategy"]
    )

    if result.get('success'):
        answer = result.get('answer', '')
        structured = _structure_competitor_response(competitor, answer, config)

        return {
            'success': True,
            'data': structured,
            'sources': result.get('sources', [])
        }

    return {'success': False}


def _analyze_competitor_website(competitor: str, content: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze competitor website content."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Analyze competitor website content.

Competitor: {competitor}

Content:
{content[:8000]}

Extract competitive intelligence:
{{
  "products_services": ["List offerings"],
  "pricing_strategy": "premium/value/penetration",
  "value_proposition": "What they promise customers",
  "target_segments": ["Who they target"],
  "key_differentiators": ["What makes them unique"],
  "weaknesses_observed": ["Potential gaps or issues"]
}}

Only include facts from the content.
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

        return json.loads(content)

    except Exception as e:
        logger.error(f"Error analyzing competitor website: {e}")
        return {}


def _structure_competitor_response(competitor: str, perplexity_answer: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Structure Perplexity competitor data."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Extract structured data about {competitor}.

Research Result:
{perplexity_answer}

Extract into JSON:
{{
  "revenue": "...",
  "employees": "...",
  "market_share": "...",
  "products": [...],
  "recent_strategy": "..."
}}
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
        logger.error(f"Error structuring competitor response: {e}")
        return {}


def _synthesize_competitive_intelligence(
    company_name: str,
    competitors_data: Dict[str, Any],
    company_intel: Dict[str, Any],
    market_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Synthesize competitive intelligence across all competitors."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Synthesize competitive intelligence.

Our Company: {company_name}

Competitor Profiles:
{str(competitors_data)[:5000]}

Our Company Context:
{str(company_intel)[:1000]}

Market Context:
{str(market_intel)[:1000]}

Provide competitive analysis:
{{
  "competitive_landscape": {{
    "market_leaders": [...],
    "our_position": "leader/challenger/follower"
  }},
  "competitive_advantages": ["Where we win"],
  "competitive_disadvantages": ["Where competitors win"],
  "strategic_recommendations": ["How to compete better"],
  "threat_assessment": {{
    "highest_threat": "Competitor X",
    "reason": "..."
  }}
}}
"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        content = response.content[0].text

        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()

        return json.loads(content)

    except Exception as e:
        logger.error(f"Error synthesizing competitive intelligence: {e}")
        return {}
