"""
Company Intelligence Skill.

Gathers basic company information from website and public sources.
"""

from typing import Dict, Any
from anthropic import Anthropic
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from data_sources.scrapers.firecrawl_client import FirecrawlClient
from utils.logger import setup_logger

logger = setup_logger(__name__)


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute company intelligence gathering.

    Args:
        task: Task object with description
        context: Execution context
        config: BCOS configuration

    Returns:
        Dictionary with company intelligence findings
    """
    logger.info("Executing Company Intelligence skill")

    company = config.get('company', {})
    company_name = company.get('name', 'Unknown')
    company_website = company.get('website', '')

    # Initialize data sources
    firecrawl = FirecrawlClient()

    findings = {
        'company_name': company_name,
        'website': company_website,
        'industry': company.get('industry', 'Unknown'),
    }

    # Step 1: Scrape company website
    if company_website:
        logger.info(f"Scraping {company_website}")
        scrape_result = firecrawl.scrape_url(company_website)

        if scrape_result.get('success'):
            website_content = scrape_result.get('content', '')
            findings['website_content'] = website_content[:5000]  # First 5k chars
            findings['website_metadata'] = scrape_result.get('metadata', {})

            # Step 2: Use LLM to analyze website content
            analysis = _analyze_website_content(
                company_name=company_name,
                website_content=website_content,
                config=config
            )

            findings.update(analysis)
        else:
            logger.warning(f"Website scraping failed: {scrape_result.get('error')}")
            findings['scraping_error'] = scrape_result.get('error')

            # Fallback: Use LLM knowledge
            analysis = _fallback_company_knowledge(company_name, config)
            findings.update(analysis)
    else:
        logger.warning("No website provided - using LLM knowledge only")
        analysis = _fallback_company_knowledge(company_name, config)
        findings.update(analysis)

    logger.info(f"Company intelligence gathered for {company_name}")

    return findings


def _analyze_website_content(
    company_name: str,
    website_content: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Use LLM to analyze scraped website content.

    Args:
        company_name: Name of the company
        website_content: Scraped website text
        config: BCOS configuration

    Returns:
        Analyzed company intelligence
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Analyze this company website content and extract key business intelligence.

Company: {company_name}

Website Content:
{website_content[:8000]}

Extract and structure the following information:
1. Business description - What does this company do?
2. Products/Services - Main offerings
3. Target customers - Who are their customers?
4. Value proposition - What makes them unique?
5. Key facts - Revenue, team size, founding year, headquarters, etc. (if mentioned)
6. Business model - How do they make money?

Return a JSON object with your findings:
{{
  "business_description": "...",
  "products_services": ["...", "..."],
  "target_customers": "...",
  "value_proposition": "...",
  "key_facts": {{
    "founded": "...",
    "headquarters": "...",
    "team_size": "...",
    "revenue": "..."
  }},
  "business_model": "...",
  "confidence": "high/medium/low"
}}

Be specific and extract concrete details from the content.
"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        content = response.content[0].text

        # Extract JSON
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()

        analysis = json.loads(content)
        return analysis

    except Exception as e:
        logger.error(f"Error analyzing website content: {e}")
        return {
            'error': str(e),
            'confidence': 'low'
        }


def _fallback_company_knowledge(company_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fallback: Use LLM's knowledge base when website scraping fails.

    Args:
        company_name: Name of the company
        config: BCOS configuration

    Returns:
        Company intelligence from LLM knowledge
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    industry = config.get('company', {}).get('industry', 'Unknown')

    prompt = f"""Provide business intelligence about this company using your knowledge base.

Company: {company_name}
Industry: {industry}

Provide the following information (note if you're uncertain):
1. Business description
2. Main products/services
3. Target customers
4. Value proposition
5. Key facts (founding year, headquarters, etc.)
6. Business model

Return a JSON object:
{{
  "business_description": "...",
  "products_services": ["...", "..."],
  "target_customers": "...",
  "value_proposition": "...",
  "key_facts": {{
    "founded": "...",
    "headquarters": "...",
    "team_size": "...",
    "revenue": "..."
  }},
  "business_model": "...",
  "confidence": "medium/low",
  "source": "knowledge_base",
  "disclaimer": "Information from knowledge base - may be outdated"
}}

Be honest about confidence and acknowledge if information may be outdated.
"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        content = response.content[0].text

        # Extract JSON
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].split('```')[0].strip()

        analysis = json.loads(content)
        return analysis

    except Exception as e:
        logger.error(f"Error in fallback company knowledge: {e}")
        return {
            'error': str(e),
            'confidence': 'low'
        }
