"""
Clean Competitor Intelligence - Single Source (Perplexity)

Simple, reliable approach:
1. One Perplexity search per competitor
2. Clean parsing with error handling
3. Return structured data

No multi-source complexity, no Truth Engine conflicts.
"""

from typing import Dict, Any
from anthropic import Anthropic
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from data_sources.apis.perplexity_client import PerplexityClient
from utils.logger import setup_logger

logger = setup_logger(__name__)


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute clean, single-source competitor intelligence gathering.

    Uses only Perplexity for reliability and simplicity.
    """
    logger.info("Executing Clean Competitor Intelligence (Perplexity Only)")

    company = config.get('company', {})
    company_name = company.get('name', 'Unknown')
    industry = company.get('industry', 'Unknown')

    # Get competitors from config (top 4)
    competitors = config.get('competitors', [])[:4]

    if not competitors:
        logger.warning("No competitors specified in config")
        return {
            'success': False,
            'error': 'No competitors specified for analysis'
        }

    # Check if Perplexity is enabled
    perplexity_config = config.get('data_sources', {}).get('perplexity', {})
    if not perplexity_config.get('enabled', False):
        logger.error("Perplexity is not enabled in config")
        return {
            'success': False,
            'error': 'Perplexity is required but not enabled in config'
        }

    # Initialize Perplexity client
    client = PerplexityClient()
    if not client.is_available():
        logger.error("Perplexity API not configured")
        return {
            'success': False,
            'error': 'Perplexity API key not found in environment'
        }

    # Profile each competitor
    competitor_profiles = {}

    for competitor in competitors:
        logger.info(f"Profiling competitor: {competitor}")

        # Single comprehensive search query per competitor
        search_query = f"""Provide comprehensive competitive intelligence about {competitor} in the {industry} industry:

1. **Company Overview:**
   - What does {competitor} do? (clear description)
   - Main products or services offered
   - Target customers and market segments
   - Value proposition

2. **Business Scale:**
   - Annual revenue (latest available)
   - Number of employees
   - Market share (if known)
   - Geographic presence

3. **Competitive Position:**
   - Key strengths and advantages
   - Products/features that differentiate them
   - Pricing strategy (premium/value/penetration)
   - Recent strategic moves or launches

4. **Market Positioning:**
   - How they position themselves
   - Marketing messages/slogans
   - Target customer segments

For each fact, provide specific information with sources.
If not publicly available, state "Not publicly available".
"""

        try:
            result = client.search(query=search_query, num_results=10)

            if not result.get('success'):
                logger.error(f"Perplexity search failed for {competitor}: {result.get('error')}")
                competitor_profiles[competitor] = {
                    'error': f"Failed to gather data: {result.get('error')}"
                }
                continue

            answer = result.get('answer', '')
            sources = result.get('sources', [])

            logger.info(f"Perplexity returned answer with {len(sources)} sources for {competitor}")

            # Parse the answer into structured data
            structured_data = _parse_competitor_answer(competitor, answer)

            if not structured_data:
                logger.error(f"Failed to parse Perplexity answer for {competitor}")
                competitor_profiles[competitor] = {
                    'error': 'Failed to parse competitor data'
                }
                continue

            # Add metadata
            structured_data['_metadata'] = {
                'source': 'Perplexity',
                'source_urls': sources,
                'date_collected': datetime.now().isoformat(),
                'competitor_name': competitor
            }

            competitor_profiles[competitor] = structured_data
            logger.info(f"Successfully profiled {competitor}")

        except Exception as e:
            logger.error(f"Error profiling {competitor}: {e}", exc_info=True)
            competitor_profiles[competitor] = {
                'error': str(e)
            }

    # Synthesize competitive analysis
    logger.info("Synthesizing competitive intelligence...")
    competitive_analysis = _synthesize_competitive_analysis(
        company_name,
        industry,
        competitor_profiles
    )

    return {
        'success': True,
        'competitor_profiles': competitor_profiles,
        'competitive_analysis': competitive_analysis,
        'competitors_analyzed': len([p for p in competitor_profiles.values() if 'error' not in p]),
        'source': 'perplexity'
    }


def _parse_competitor_answer(competitor_name: str, answer: str) -> Dict[str, Any]:
    """
    Parse Perplexity answer into clean structured data.

    Uses Claude to extract JSON with robust error handling.
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Extract structured competitive intelligence about {competitor_name}.

IMPORTANT: Extract EVERY specific fact mentioned. Be thorough and precise.

Perplexity Answer:
{answer}

Extract into this EXACT JSON structure:
{{
  "company_description": "Clear 1-2 sentence description",
  "products_services": ["List each product/service mentioned"],
  "target_customers": "Who are their customers",
  "value_proposition": "What makes them unique",
  "business_facts": {{
    "revenue": "Amount with timeframe (e.g., '$500M annual', or 'Unknown')",
    "employees": "Number as string (e.g., '1000', '500+', or 'Unknown')",
    "market_share": "Percentage or description (or 'Unknown')",
    "geography": "Markets served (or 'Unknown')"
  }},
  "competitive_strengths": ["List key advantages"],
  "pricing_strategy": "premium/value/penetration (or 'Unknown')",
  "positioning": "How they position themselves in market",
  "recent_moves": ["Recent strategic initiatives, launches, or news"]
}}

RULES:
1. Extract EVERY fact mentioned in the answer
2. Use exact quotes when possible
3. If a fact isn't mentioned, use "Unknown" - do NOT make up data
4. Return ONLY valid JSON, no extra text

Extract now:"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text

        # Extract JSON from markdown code blocks if present
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()

        # Parse JSON
        data = json.loads(content)

        # Validate structure
        if not isinstance(data, dict):
            logger.error(f"Parsed data is not a dict: {type(data)}")
            return {}

        logger.info(f"Successfully parsed competitor data: {len(data)} fields")

        return data

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Content was: {content[:500]}...")
        return {}
    except Exception as e:
        logger.error(f"Error parsing competitor answer: {e}", exc_info=True)
        return {}


def _synthesize_competitive_analysis(
    company_name: str,
    industry: str,
    competitor_profiles: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Synthesize competitive analysis across all competitor profiles.

    Uses Claude to generate strategic insights.
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Filter out failed profiles
    valid_profiles = {k: v for k, v in competitor_profiles.items() if 'error' not in v}

    if not valid_profiles:
        logger.warning("No valid competitor profiles to synthesize")
        return {
            'error': 'No competitor data available for analysis'
        }

    prompt = f"""Synthesize competitive intelligence for {company_name} in the {industry} industry.

Competitor Profiles:
{json.dumps(valid_profiles, indent=2)[:6000]}

Provide strategic competitive analysis in this JSON structure:
{{
  "competitive_landscape": {{
    "total_competitors_analyzed": {len(valid_profiles)},
    "market_positioning": "Description of overall competitive landscape",
    "key_players": ["List competitors by market position"]
  }},
  "common_strengths": ["Strengths most competitors share"],
  "common_weaknesses": ["Potential gaps across competitors"],
  "differentiation_opportunities": ["Where {company_name} could differentiate"],
  "competitive_threats": [
    {{
      "competitor": "Name",
      "threat_level": "high/medium/low",
      "reason": "Why they're a threat"
    }}
  ],
  "strategic_recommendations": [
    "Specific actionable recommendations for competing effectively"
  ]
}}

RULES:
1. Be specific and actionable
2. Base insights on actual competitor data
3. Focus on strategic implications for {company_name}
4. Return ONLY valid JSON

Synthesize now:"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text

        # Extract JSON from markdown code blocks if present
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()

        # Parse JSON
        data = json.loads(content)

        logger.info("Successfully synthesized competitive analysis")

        return data

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in synthesis: {e}")
        logger.error(f"Content was: {content[:500]}...")
        return {'error': 'Failed to parse competitive analysis'}
    except Exception as e:
        logger.error(f"Error synthesizing competitive analysis: {e}", exc_info=True)
        return {'error': str(e)}
