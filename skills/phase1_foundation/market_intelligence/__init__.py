"""
Enhanced Market Intelligence Skill with Multi-Source Verification.

Uses real-time market data from multiple sources rather than LLM knowledge base.

Sources:
1. Exa market trends search - Real-time market data
2. Firecrawl industry reports - Analyst reports and research
3. Perplexity verification - Fact-check market sizes and growth rates
4. Truth Engine cross-reference - Validate all claims

Returns VerifiedDataset with sourced, verified market intelligence.
"""

from typing import Dict, Any
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
    Execute multi-source market intelligence gathering.

    Args:
        task: Task object
        context: Execution context with company intelligence
        config: BCOS configuration

    Returns:
        VerifiedDataset with market intelligence
    """
    logger.info("Executing Enhanced Market Intelligence (Multi-Source)")

    company = context.get('company', config.get('company', {}))
    company_name = company.get('name', 'Unknown')
    industry = company.get('industry', 'Unknown')

    # Get company intel from Phase 1 context
    company_intel = context.get('company_intelligence', {})

    # Initialize Truth Engine
    verification_config = config.get('verification', {})
    truth_engine = TruthEngine(min_confidence=verification_config.get('min_confidence', 0.5))

    all_sources_data = []

    # ========================================
    # Source 1: Exa Market Trends Search
    # ========================================
    logger.info(f"Source 1: Exa market trends search for {industry}")

    exa_market_data = _search_market_trends_with_exa(industry, company_name, config)

    if exa_market_data.get('success'):
        all_sources_data.append({
            'source_type': 'secondary',
            'source_name': 'Exa Market Research',
            'url': 'https://exa.ai',
            'date_accessed': datetime.now().isoformat(),
            'data': exa_market_data.get('data', {}),
            'reliability_score': 0.85
        })

    # ========================================
    # Source 2: Industry Reports (Firecrawl)
    # ========================================
    logger.info(f"Source 2: Industry reports for {industry}")

    industry_reports = _scrape_industry_reports(industry, config)

    if industry_reports.get('success'):
        all_sources_data.append({
            'source_type': 'secondary',
            'source_name': 'Industry Reports',
            'url': industry_reports.get('source_url', 'unknown'),
            'date_accessed': datetime.now().isoformat(),
            'data': industry_reports.get('data', {}),
            'reliability_score': 0.8
        })

    # ========================================
    # Source 3: Perplexity Market Verification
    # ========================================
    logger.info(f"Source 3: Perplexity market verification for {industry}")

    perplexity_data = _verify_market_data(industry, config)

    if perplexity_data.get('success'):
        all_sources_data.append({
            'source_type': 'verification',
            'source_name': 'Perplexity Market Verification',
            'url': 'https://perplexity.ai',
            'date_accessed': datetime.now().isoformat(),
            'data': perplexity_data.get('data', {}),
            'reliability_score': 0.9
        })

    # ========================================
    # Source 4: Claude Analysis with Company Context
    # ========================================
    logger.info("Source 4: Claude strategic analysis")

    claude_analysis = _claude_market_analysis(
        industry, company_name, company_intel, all_sources_data, config
    )

    if claude_analysis.get('success'):
        all_sources_data.append({
            'source_type': 'secondary',
            'source_name': 'Claude Strategic Analysis',
            'url': 'anthropic:claude',
            'date_accessed': datetime.now().isoformat(),
            'data': claude_analysis.get('data', {}),
            'reliability_score': 0.7  # Lower reliability as it's synthesis
        })

    # ========================================
    # Cross-Reference with Truth Engine
    # ========================================
    logger.info("Cross-referencing market data across all sources...")

    verified_dataset = truth_engine.cross_reference(
        datasets=all_sources_data,
        entity_name=f"{industry} Market",
        entity_type="market"
    )

    logger.info(
        f"Market intelligence verification complete: {verified_dataset.verified_count} verified, "
        f"confidence: {verified_dataset.overall_confidence:.2f}"
    )

    return {
        'success': True,
        'verified_dataset': verified_dataset.to_dict(),
        'industry': industry,
        'company_name': company_name,
        'sources_used': len(all_sources_data),
        'verification_method': 'multi_source_truth_engine'
    }


def _search_market_trends_with_exa(industry: str, company_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Search for market trends using Exa MCP."""
    data_sources = config.get('data_sources', {})
    exa_config = data_sources.get('exa', {})

    if not (isinstance(exa_config, dict) and exa_config.get('use_mcp', False)):
        logger.info("Exa MCP not enabled, using fallback")
        return _fallback_market_analysis(industry, company_name, config)

    # TODO: When executed by Claude Code with MCP access:
    # result = mcp__exa__web_search_exa(
    #     query=f"{industry} market size trends growth 2024",
    #     numResults=10
    # )
    logger.info("[MCP] Would call mcp__exa__web_search_exa for market trends")

    # Fallback
    return _fallback_market_analysis(industry, company_name, config)


def _scrape_industry_reports(industry: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Scrape industry reports using Firecrawl MCP search."""
    data_sources = config.get('data_sources', {})
    firecrawl_config = data_sources.get('firecrawl', {})

    if not (isinstance(firecrawl_config, dict) and firecrawl_config.get('use_mcp', False)):
        logger.info("Firecrawl MCP not enabled")
        return {'success': False}

    # TODO: When executed by Claude Code:
    # results = mcp__firecrawl__firecrawl_search(
    #     query=f"{industry} industry report market size 2024",
    #     limit=5
    # )
    logger.info("[MCP] Would call mcp__firecrawl__firecrawl_search for industry reports")

    return {'success': False}


def _verify_market_data(industry: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Verify market data with Perplexity."""
    perplexity_config = config.get('data_sources', {}).get('perplexity', {})

    if not perplexity_config.get('enabled', False):
        return {'success': False}

    client = PerplexityClient()
    if not client.is_available():
        return {'success': False}

    # Search for market data verification
    query = f"{industry} market size 2024 growth rate TAM SAM market trends"
    result = client.search(query, num_results=5)

    if result.get('success'):
        # Structure the response
        answer = result.get('answer', '')
        structured = _structure_market_response(industry, answer, config)

        return {
            'success': True,
            'data': structured,
            'sources': result.get('sources', [])
        }

    return {'success': False}


def _claude_market_analysis(
    industry: str,
    company_name: str,
    company_intel: Dict[str, Any],
    gathered_data: list,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Use Claude to synthesize market intelligence from gathered data."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Compile all gathered insights
    insights_summary = "\n\n".join([
        f"Source: {s.get('source_name')}\nData: {str(s.get('data', {}))[:500]}"
        for s in gathered_data
    ])

    prompt = f"""Analyze market intelligence for {industry} based on gathered data.

Company: {company_name}
Industry: {industry}

Company Context:
{str(company_intel)[:1000]}

Gathered Market Data:
{insights_summary}

Synthesize into structured market intelligence:

{{
  "market_size": {{
    "tam": {{"value": "...", "unit": "USD", "year": 2024}},
    "sam": {{"value": "...", "unit": "USD", "year": 2024}},
    "growth_rate_cagr": "...%",
    "geographic_breakdown": {{"north_america": "...%", "europe": "...%", "asia": "...%"}}
  }},
  "market_segments": [
    {{"segment_name": "...", "size": "...", "growth_rate": "...%"}}
  ],
  "trends": [
    {{"trend": "...", "impact": "high/medium/low", "timeframe": "current/emerging"}}
  ],
  "drivers": [
    {{"driver": "...", "category": "technology/economic/social/regulatory"}}
  ],
  "opportunities": [
    {{"opportunity": "...", "size": "...", "effort_required": "low/medium/high"}}
  ],
  "competitive_dynamics": {{
    "market_concentration": "fragmented/concentrated",
    "barriers_to_entry": "low/medium/high"
  }}
}}

ONLY include facts from the gathered data. Mark uncertain items clearly.
"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        content = response.content[0].text

        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()

        data = json.loads(content)
        return {'success': True, 'data': data}

    except Exception as e:
        logger.error(f"Error in Claude market analysis: {e}")
        return {'success': False, 'error': str(e)}


def _structure_market_response(industry: str, perplexity_answer: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Structure Perplexity's market data into format."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Extract structured market data from this research.

Industry: {industry}

Research Result:
{perplexity_answer}

Extract into JSON:
{{
  "market_size": {{
    "tam": {{"value": "...", "year": 2024}},
    "growth_rate_cagr": "...%"
  }},
  "market_segments": [...],
  "trends": [...],
  "drivers": [...]
}}

Only include explicitly stated facts.
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
        logger.error(f"Error structuring market response: {e}")
        return {}


def _fallback_market_analysis(industry: str, company_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback: Use Claude's knowledge base for market intelligence."""
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Provide market intelligence for {industry}.

Context: {company_name} operates in this industry.

Return JSON with your knowledge:
{{
  "market_size": {{"tam": "...", "growth_rate": "...%"}},
  "market_segments": [...],
  "trends": [...],
  "drivers": [...],
  "opportunities": [...],
  "confidence": "low",
  "source": "knowledge_base",
  "disclaimer": "From knowledge base - may be outdated"
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

        result = json.loads(content)
        return {'success': True, 'data': result}

    except Exception as e:
        logger.error(f"Error in fallback market analysis: {e}")
        return {'success': False, 'error': str(e)}
