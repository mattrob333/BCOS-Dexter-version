"""
Market Intelligence Skill.

Researches the market landscape, trends, size, growth, and opportunities
for the target company's industry.
"""

from typing import Dict, Any
from anthropic import Anthropic
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.logger import setup_logger

logger = setup_logger(__name__)


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute market intelligence gathering.

    Analyzes:
    - Market size and growth
    - Key trends and drivers
    - Market segments
    - Opportunities and threats
    - Regulatory environment
    - Technology trends

    Args:
        task: Task object with description
        context: Execution context (including company intelligence)
        config: BCOS configuration

    Returns:
        Dictionary with market intelligence findings
    """
    logger.info("Executing Market Intelligence skill")

    company = context.get('company', config.get('company', {}))
    company_name = company.get('name', 'Unknown')
    industry = company.get('industry', 'Unknown')

    # Get company intelligence from Phase 1 context
    company_intel = context.get('company_intelligence', {})

    # Analyze market landscape
    market_analysis = _analyze_market_landscape(
        company_name=company_name,
        industry=industry,
        company_intel=company_intel,
        config=config
    )

    logger.info(f"Market intelligence gathered for {industry}")

    return market_analysis


def _analyze_market_landscape(
    company_name: str,
    industry: str,
    company_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze the market landscape for the company's industry.

    Args:
        company_name: Name of the company
        industry: Industry vertical
        company_intel: Company intelligence from previous Phase 1 task
        config: BCOS configuration

    Returns:
        Market intelligence analysis
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Extract relevant context
    business_description = company_intel.get('business_description', '')
    products_services = company_intel.get('products_services', [])
    target_customers = company_intel.get('target_customers', '')

    context_summary = f"""
Company: {company_name}
Industry: {industry}
Business Description: {business_description}
Products/Services: {', '.join(products_services) if isinstance(products_services, list) else products_services}
Target Customers: {target_customers}
"""

    prompt = f"""Conduct a comprehensive market intelligence analysis for this company's industry.

{context_summary}

Analyze the market landscape across these dimensions:

1. **Market Size & Growth**
   - Total Addressable Market (TAM)
   - Serviceable Addressable Market (SAM)
   - Serviceable Obtainable Market (SOM)
   - Historical growth rates
   - Projected growth (next 3-5 years)
   - Geographic breakdown

2. **Market Segments**
   - Major market segments
   - Segment sizes and growth rates
   - Segment characteristics
   - Which segments is the company targeting?

3. **Market Trends**
   - Technology trends shaping the market
   - Consumer/buyer behavior trends
   - Business model innovations
   - Emerging segments or categories

4. **Market Drivers**
   - What's driving market growth?
   - Macroeconomic factors
   - Technology enablers
   - Regulatory changes
   - Social/demographic shifts

5. **Market Challenges**
   - Headwinds facing the industry
   - Barriers to growth
   - Regulatory challenges
   - Technology challenges

6. **Opportunities**
   - Untapped market segments
   - Geographic expansion opportunities
   - Product/service opportunities
   - Partnership opportunities

7. **Competitive Dynamics**
   - Market concentration (fragmented vs consolidated)
   - Barriers to entry
   - Bargaining power dynamics
   - Threat of substitutes

8. **Future Outlook**
   - Where is the market heading?
   - Potential disruptions
   - Long-term structural changes

Return a detailed JSON object:

{{
  "market_size": {{
    "tam": {{"value": "...", "unit": "USD/units", "year": 2024}},
    "sam": {{"value": "...", "unit": "USD/units", "year": 2024}},
    "som": {{"value": "...", "unit": "USD/units", "year": 2024}},
    "growth_rate_cagr": "...%",
    "projected_size_2030": "...",
    "geographic_breakdown": {{
      "north_america": "...%",
      "europe": "...%",
      "asia_pacific": "...%",
      "other": "...%"
    }}
  }},
  "market_segments": [
    {{
      "segment_name": "...",
      "size": "...",
      "growth_rate": "...%",
      "characteristics": ["...", "..."],
      "company_plays_here": true/false
    }}
  ],
  "trends": [
    {{
      "trend": "...",
      "impact": "high/medium/low",
      "timeframe": "current/emerging/future",
      "description": "...",
      "implications_for_company": "..."
    }}
  ],
  "drivers": [
    {{
      "driver": "...",
      "category": "technology/economic/social/regulatory",
      "impact": "positive/negative",
      "description": "..."
    }}
  ],
  "challenges": [
    {{
      "challenge": "...",
      "severity": "high/medium/low",
      "affected_segments": ["...", "..."],
      "description": "..."
    }}
  ],
  "opportunities": [
    {{
      "opportunity": "...",
      "type": "segment/geography/product/partnership",
      "size": "...",
      "effort_required": "low/medium/high",
      "description": "...",
      "rationale": "..."
    }}
  ],
  "competitive_dynamics": {{
    "market_concentration": "fragmented/moderately-concentrated/highly-concentrated",
    "herfindahl_index_estimate": "...",
    "barriers_to_entry": "low/medium/high",
    "key_success_factors": ["...", "..."],
    "switching_costs": "low/medium/high"
  }},
  "future_outlook": {{
    "trajectory": "rapid-growth/steady-growth/mature/declining",
    "disruption_risk": "low/medium/high",
    "key_uncertainties": ["...", "..."],
    "potential_disruptors": ["...", "..."],
    "structural_changes": ["...", "..."]
  }},
  "insights": [
    "Key insight 1...",
    "Key insight 2...",
    "Key insight 3..."
  ],
  "data_sources": ["Industry knowledge", "Market research", "Analysis"],
  "confidence": "high/medium/low",
  "last_updated": "2024"
}}

Be specific with numbers where possible. Use your knowledge of this industry to provide detailed, actionable insights.
"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000,
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

        # Add metadata
        analysis['company_name'] = company_name
        analysis['industry'] = industry
        analysis['analysis_type'] = 'market_intelligence'
        analysis['source'] = 'llm_analysis'

        return analysis

    except Exception as e:
        logger.error(f"Error analyzing market landscape: {e}")
        return {
            'error': str(e),
            'company_name': company_name,
            'industry': industry,
            'analysis_type': 'market_intelligence',
            'confidence': 'low'
        }
