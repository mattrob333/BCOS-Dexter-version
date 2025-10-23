"""
Porter's Five Forces Analyzer Skill.

Analyzes industry attractiveness and competitive intensity using
Michael Porter's Five Forces framework.
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
    Execute Porter's Five Forces analysis.

    Analyzes five competitive forces:
    1. Threat of New Entrants
    2. Bargaining Power of Suppliers
    3. Bargaining Power of Buyers
    4. Threat of Substitute Products/Services
    5. Rivalry Among Existing Competitors

    Args:
        task: Task object with description
        context: Execution context (full Phase 1 context)
        config: BCOS configuration

    Returns:
        Dictionary with Porter's Five Forces analysis
    """
    logger.info("Executing Porter's Five Forces skill")

    company = context.get('company', config.get('company', {}))
    company_name = company.get('name', 'Unknown')
    industry = company.get('industry', 'Unknown')

    # Get Phase 1 context
    company_intel = context.get('company_intelligence', {})
    business_model = context.get('business_model_canvas', {})
    market_intel = context.get('market_intelligence', {})
    competitor_intel = context.get('competitor_intelligence', {})

    # Conduct Porter's Five Forces analysis
    five_forces_analysis = _analyze_five_forces(
        company_name=company_name,
        industry=industry,
        company_intel=company_intel,
        business_model=business_model,
        market_intel=market_intel,
        competitor_intel=competitor_intel,
        config=config
    )

    logger.info(f"Porter's Five Forces analysis completed for {industry}")

    return five_forces_analysis


def _analyze_five_forces(
    company_name: str,
    industry: str,
    company_intel: Dict[str, Any],
    business_model: Dict[str, Any],
    market_intel: Dict[str, Any],
    competitor_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze industry using Porter's Five Forces framework.

    Args:
        company_name: Name of the company
        industry: Industry vertical
        company_intel: Company intelligence from Phase 1
        business_model: Business Model Canvas from Phase 1
        market_intel: Market intelligence from Phase 1
        competitor_intel: Competitor intelligence from Phase 1
        config: BCOS configuration

    Returns:
        Complete Five Forces analysis
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Extract key context
    products_services = company_intel.get('products_services', [])
    business_model_type = company_intel.get('business_model', '')

    # Business model insights
    key_partners = business_model.get('key_partnerships', [])
    customer_segments = business_model.get('customer_segments', [])
    revenue_streams = business_model.get('revenue_streams', [])

    # Market context
    market_concentration = market_intel.get('competitive_dynamics', {}).get('market_concentration', 'Unknown')
    barriers_to_entry = market_intel.get('competitive_dynamics', {}).get('barriers_to_entry', 'Unknown')

    # Competitive context
    competitor_profiles = competitor_intel.get('competitor_profiles', [])
    num_competitors = len(competitor_profiles)

    context_summary = f"""
Company: {company_name}
Industry: {industry}
Products/Services: {', '.join(products_services) if isinstance(products_services, list) else products_services}
Business Model: {business_model_type}

Market Structure:
- Concentration: {market_concentration}
- Barriers to Entry: {barriers_to_entry}
- Number of Major Competitors: {num_competitors}

Customer Segments: {len(customer_segments)} identified
Key Partnerships: {len(key_partners)} identified
Revenue Streams: {len(revenue_streams)} identified
"""

    prompt = f"""Analyze this industry using Porter's Five Forces framework.

{context_summary}

Conduct a comprehensive Five Forces analysis:

**FORCE 1: THREAT OF NEW ENTRANTS**
How easy is it for new competitors to enter this market?

Analyze:
- Barriers to entry (capital requirements, economies of scale, technology, regulations, brand loyalty, network effects)
- Recent new entrants
- Ease of entry
- Time to competitive viability
- Deterrents that protect incumbents

**FORCE 2: BARGAINING POWER OF SUPPLIERS**
How much power do suppliers have over the industry?

Analyze:
- Number and concentration of suppliers
- Uniqueness of supplier offerings
- Switching costs
- Forward integration threat
- Importance of industry to suppliers
- Availability of substitutes for supplier products

**FORCE 3: BARGAINING POWER OF BUYERS**
How much power do customers have?

Analyze:
- Customer concentration vs firm concentration
- Customer price sensitivity
- Differentiation of products
- Switching costs for customers
- Backward integration threat
- Customer information availability

**FORCE 4: THREAT OF SUBSTITUTES**
How easily can customers find alternative products/services?

Analyze:
- Availability of substitutes
- Price-performance of substitutes
- Switching costs to substitutes
- Customer propensity to substitute
- Emerging substitute technologies

**FORCE 5: RIVALRY AMONG EXISTING COMPETITORS**
How intense is competition?

Analyze:
- Number and diversity of competitors
- Industry growth rate
- Fixed costs and capacity
- Product differentiation
- Brand loyalty
- Exit barriers
- Strategic stakes

For each force, provide:
- Intensity rating (Low/Medium/High)
- Trend (Increasing/Stable/Decreasing)
- Key factors driving the force
- Impact on industry attractiveness
- Implications for company strategy

Also provide:
- Overall industry attractiveness assessment
- Strategic recommendations

Return a detailed JSON object:

{{
  "threat_of_new_entrants": {{
    "intensity": "low/medium/high",
    "trend": "increasing/stable/decreasing",
    "factors": [
      {{
        "factor": "...",
        "impact": "increases/decreases threat",
        "description": "..."
      }}
    ],
    "barriers_to_entry": {{
      "capital_requirements": {{"level": "low/medium/high", "description": "..."}},
      "economies_of_scale": {{"level": "low/medium/high", "description": "..."}},
      "technology_complexity": {{"level": "low/medium/high", "description": "..."}},
      "regulatory_requirements": {{"level": "low/medium/high", "description": "..."}},
      "brand_loyalty": {{"level": "low/medium/high", "description": "..."}},
      "network_effects": {{"level": "low/medium/high", "description": "..."}},
      "access_to_distribution": {{"level": "low/medium/high", "description": "..."}}
    }},
    "recent_entrants": ["...", "..."],
    "impact_on_industry": "...",
    "strategic_implications": "..."
  }},
  "supplier_power": {{
    "intensity": "low/medium/high",
    "trend": "increasing/stable/decreasing",
    "factors": [
      {{
        "factor": "...",
        "impact": "increases/decreases power",
        "description": "..."
      }}
    ],
    "key_suppliers": ["...", "..."],
    "supplier_concentration": "fragmented/moderate/concentrated",
    "switching_costs": "low/medium/high",
    "forward_integration_threat": "low/medium/high",
    "impact_on_industry": "...",
    "strategic_implications": "..."
  }},
  "buyer_power": {{
    "intensity": "low/medium/high",
    "trend": "increasing/stable/decreasing",
    "factors": [
      {{
        "factor": "...",
        "impact": "increases/decreases power",
        "description": "..."
      }}
    ],
    "customer_concentration": "fragmented/moderate/concentrated",
    "price_sensitivity": "low/medium/high",
    "product_differentiation": "low/medium/high",
    "switching_costs": "low/medium/high",
    "backward_integration_threat": "low/medium/high",
    "impact_on_industry": "...",
    "strategic_implications": "..."
  }},
  "threat_of_substitutes": {{
    "intensity": "low/medium/high",
    "trend": "increasing/stable/decreasing",
    "substitutes": [
      {{
        "substitute": "...",
        "price_performance": "inferior/similar/superior",
        "switching_cost": "low/medium/high",
        "adoption_rate": "low/medium/high",
        "description": "..."
      }}
    ],
    "emerging_substitutes": ["...", "..."],
    "impact_on_industry": "...",
    "strategic_implications": "..."
  }},
  "competitive_rivalry": {{
    "intensity": "low/medium/high",
    "trend": "increasing/stable/decreasing",
    "factors": [
      {{
        "factor": "...",
        "impact": "increases/decreases rivalry",
        "description": "..."
      }}
    ],
    "number_of_competitors": "...",
    "market_growth_rate": "...",
    "industry_concentration": "fragmented/moderate/concentrated",
    "product_differentiation": "low/medium/high",
    "exit_barriers": "low/medium/high",
    "competitive_tactics": ["price competition", "innovation", "marketing", "..."],
    "impact_on_industry": "...",
    "strategic_implications": "..."
  }},
  "overall_assessment": {{
    "industry_attractiveness": "unattractive/moderately-attractive/highly-attractive",
    "attractiveness_score": 1-10,
    "strongest_force": "...",
    "weakest_force": "...",
    "key_dynamics": ["...", "...", "..."],
    "profit_potential": "low/medium/high",
    "strategic_positioning_opportunities": ["...", "..."]
  }},
  "strategic_recommendations": [
    {{
      "recommendation": "...",
      "force_addressed": "...",
      "rationale": "...",
      "priority": "high/medium/low"
    }}
  ],
  "confidence": "high/medium/low"
}}

Be thorough and specific. Use the context provided to make the analysis highly relevant to this company and industry.
"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=12000,
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
        analysis['framework'] = "Porter's Five Forces"
        analysis['source'] = 'llm_analysis'

        return analysis

    except Exception as e:
        logger.error(f"Error conducting Porter's Five Forces analysis: {e}")
        return {
            'error': str(e),
            'company_name': company_name,
            'industry': industry,
            'framework': "Porter's Five Forces",
            'confidence': 'low'
        }
