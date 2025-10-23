"""
Clean Company Intelligence - Single Source (Perplexity)

Simple, reliable approach:
1. One comprehensive Perplexity search
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
    Execute clean, single-source company intelligence gathering.

    Uses only Perplexity for reliability and simplicity.
    """
    logger.info("Executing Clean Company Intelligence (Perplexity Only)")

    company = config.get('company', {})
    company_name = company.get('name', 'Unknown')
    company_website = company.get('website', '')
    industry = company.get('industry', 'Unknown')

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

    # Single comprehensive search query
    search_query = f"""Provide comprehensive business intelligence about {company_name} ({company_website}):

1. **Basic Facts:**
   - Year founded
   - Headquarters location (city, state/country)
   - Number of employees or team size
   - CEO and/or founder names
   - Annual revenue or funding amount

2. **Business Overview:**
   - What does the company do? (clear description)
   - Main products or services offered
   - Target customers and market segments
   - Value proposition (what makes them unique)

3. **Business Model:**
   - How they make money (revenue streams)
   - Pricing model if known
   - Key partnerships or channels

For each fact, provide specific, verifiable information with sources.
If a fact is not publicly available, explicitly state "Not publicly available".
"""

    logger.info(f"Searching Perplexity for comprehensive data on {company_name}")

    try:
        result = client.search(query=search_query, num_results=10)

        if not result.get('success'):
            logger.error(f"Perplexity search failed: {result.get('error')}")
            return {
                'success': False,
                'error': f"Perplexity search failed: {result.get('error')}"
            }

        answer = result.get('answer', '')
        sources = result.get('sources', [])

        logger.info(f"Perplexity returned answer with {len(sources)} sources")
        logger.info(f"Answer preview: {answer[:300]}...")

        # Parse the answer into structured data
        structured_data = _parse_perplexity_answer(company_name, answer)

        if not structured_data:
            logger.error("Failed to parse Perplexity answer")
            return {
                'success': False,
                'error': 'Failed to parse Perplexity answer into structured data'
            }

        # Add metadata
        structured_data['_metadata'] = {
            'source': 'Perplexity',
            'source_urls': sources,
            'date_collected': datetime.now().isoformat(),
            'company_name': company_name,
            'company_website': company_website
        }

        logger.info(f"Successfully collected data: {len(structured_data)} top-level fields")
        logger.info(f"Key facts found: {structured_data.get('key_facts', {})}")

        return {
            'success': True,
            'data': structured_data,
            'company_name': company_name,
            'source': 'perplexity',
            'sources': sources
        }

    except Exception as e:
        logger.error(f"Error in company intelligence: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def _parse_perplexity_answer(company_name: str, answer: str) -> Dict[str, Any]:
    """
    Parse Perplexity answer into clean structured data.

    Uses Claude to extract JSON with robust error handling.
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Extract structured data from this business intelligence about {company_name}.

IMPORTANT: Extract EVERY specific fact mentioned. Be thorough and precise.

Perplexity Answer:
{answer}

Extract into this EXACT JSON structure:
{{
  "business_description": "Clear 1-2 sentence description of what the company does",
  "products_services": ["List each product/service mentioned"],
  "target_customers": "Who are their customers",
  "value_proposition": "What makes them unique or valuable",
  "business_model": "How they make money",
  "key_facts": {{
    "founded": "YYYY (year only, or 'Unknown')",
    "headquarters": "City, State/Country (or 'Unknown')",
    "employees": "Number as string (e.g., '100', '500+', or 'Unknown')",
    "revenue": "Amount with timeframe (e.g., '$5M annual', or 'Unknown')",
    "funding": "Amount and stage (e.g., 'Series A $10M', or 'Unknown')",
    "ceo": "Name (or 'Unknown')",
    "founder": "Name(s) (or 'Unknown')"
  }}
}}

RULES:
1. Extract EVERY fact mentioned in the answer
2. Use exact quotes when possible
3. If a fact isn't mentioned, use "Unknown" - do NOT make up data
4. For key_facts, extract the most specific value available
5. Return ONLY valid JSON, no extra text

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

        if 'key_facts' not in data or not isinstance(data['key_facts'], dict):
            logger.warning("key_facts missing or not a dict, adding empty dict")
            data['key_facts'] = {}

        logger.info(f"Successfully parsed: {len(data)} fields, {len(data['key_facts'])} key facts")

        return data

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Content was: {content[:500]}...")
        return {}
    except Exception as e:
        logger.error(f"Error parsing Perplexity answer: {e}", exc_info=True)
        return {}
