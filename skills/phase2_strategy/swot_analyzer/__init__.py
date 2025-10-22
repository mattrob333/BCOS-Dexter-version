"""
SWOT Analyzer Skill.

Conducts comprehensive SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis
based on Phase 1 foundation data.
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
    Execute SWOT analysis.

    Analyzes:
    - Strengths: Internal positive attributes
    - Weaknesses: Internal limitations
    - Opportunities: External favorable conditions
    - Threats: External challenges

    Args:
        task: Task object with description
        context: Execution context (full Phase 1 context)
        config: BCOS configuration

    Returns:
        Dictionary with SWOT analysis
    """
    logger.info("Executing SWOT Analysis skill")

    company = context.get('company', config.get('company', {}))
    company_name = company.get('name', 'Unknown')

    # Get Phase 1 context
    company_intel = context.get('company_intelligence', {})
    business_model = context.get('business_model_canvas', {})
    market_intel = context.get('market_intelligence', {})
    competitor_intel = context.get('competitor_intelligence', {})

    # Conduct SWOT analysis
    swot_analysis = _conduct_swot_analysis(
        company_name=company_name,
        company_intel=company_intel,
        business_model=business_model,
        market_intel=market_intel,
        competitor_intel=competitor_intel,
        config=config
    )

    logger.info(f"SWOT analysis completed for {company_name}")

    return swot_analysis


def _conduct_swot_analysis(
    company_name: str,
    company_intel: Dict[str, Any],
    business_model: Dict[str, Any],
    market_intel: Dict[str, Any],
    competitor_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Conduct comprehensive SWOT analysis using Phase 1 context.

    Args:
        company_name: Name of the company
        company_intel: Company intelligence from Phase 1
        business_model: Business Model Canvas from Phase 1
        market_intel: Market intelligence from Phase 1
        competitor_intel: Competitor intelligence from Phase 1
        config: BCOS configuration

    Returns:
        Complete SWOT analysis
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Extract key context
    value_proposition = company_intel.get('value_proposition', '')
    products_services = company_intel.get('products_services', [])

    # Business model insights
    revenue_streams = business_model.get('revenue_streams', [])
    key_resources = business_model.get('key_resources', {})
    cost_structure = business_model.get('cost_structure', {})

    # Market context
    market_trends = market_intel.get('trends', [])
    opportunities = market_intel.get('opportunities', [])
    challenges = market_intel.get('challenges', [])
    market_growth = market_intel.get('market_size', {}).get('growth_rate_cagr', 'Unknown')

    # Competitive context
    competitor_profiles = competitor_intel.get('competitor_profiles', [])
    our_position = competitor_intel.get('competitive_landscape', {}).get('our_position', 'Unknown')

    # Build rich context summary
    context_summary = f"""
Company: {company_name}
Value Proposition: {value_proposition}
Products/Services: {', '.join(products_services) if isinstance(products_services, list) else products_services}

Business Model:
- Revenue Streams: {len(revenue_streams)} identified
- Key Resources: {', '.join([k for k, v in key_resources.items() if v]) if key_resources else 'N/A'}
- Cost Model: {cost_structure.get('model', 'Unknown') if cost_structure else 'Unknown'}

Market Context:
- Market Growth Rate: {market_growth}
- Key Trends: {', '.join([t.get('trend', '') for t in market_trends[:3]]) if market_trends else 'N/A'}
- Market Opportunities: {len(opportunities)} identified
- Market Challenges: {len(challenges)} identified

Competitive Position:
- Our Position: {our_position}
- Competitors Analyzed: {len(competitor_profiles)}
"""

    prompt = f"""Conduct a comprehensive SWOT analysis for this company using all available context.

{context_summary}

Perform a detailed SWOT analysis:

**STRENGTHS (Internal Positive Attributes)**
What does the company do well?
- Core competencies
- Competitive advantages
- Strong resources and capabilities
- Successful track record
- Strong brand or reputation
- Proprietary technology or IP
- Talented team
- Financial strength

**WEAKNESSES (Internal Limitations)**
What can be improved?
- Gaps in capabilities
- Resource limitations
- Disadvantages vs competitors
- Operational inefficiencies
- Weak points in business model
- Brand vulnerabilities
- Financial constraints

**OPPORTUNITIES (External Favorable Conditions)**
What external factors could be exploited?
- Market growth areas
- Emerging trends to capitalize on
- Underserved segments
- Geographic expansion
- New product/service opportunities
- Strategic partnerships
- Regulatory changes that favor us
- Competitor weaknesses to exploit

**THREATS (External Challenges)**
What external factors pose risks?
- Competitive threats
- Market disruptions
- Regulatory risks
- Technology shifts
- Economic conditions
- Changing customer preferences
- Supplier/partner risks

Also provide:
- **TOWS Matrix**: Strategic initiatives matching strengths to opportunities, etc.
- **Prioritization**: Which items are most critical
- **Strategic Implications**: What this means for strategy

Return a detailed JSON object:

{{
  "strengths": [
    {{
      "strength": "...",
      "category": "product/brand/operations/financial/team/technology",
      "impact": "high/medium/low",
      "description": "...",
      "evidence": "...",
      "sustainability": "sustainable/at-risk"
    }}
  ],
  "weaknesses": [
    {{
      "weakness": "...",
      "category": "product/brand/operations/financial/team/technology",
      "severity": "high/medium/low",
      "description": "...",
      "evidence": "...",
      "addressability": "easy/moderate/difficult"
    }}
  ],
  "opportunities": [
    {{
      "opportunity": "...",
      "category": "market/product/partnership/geography/technology",
      "potential_impact": "high/medium/low",
      "description": "...",
      "timeframe": "immediate/short-term/medium-term/long-term",
      "requirements": "...",
      "attractiveness_score": 1-10
    }}
  ],
  "threats": [
    {{
      "threat": "...",
      "category": "competitive/market/regulatory/technology/economic",
      "severity": "high/medium/low",
      "description": "...",
      "probability": "high/medium/low",
      "timeframe": "immediate/short-term/medium-term/long-term",
      "mitigation_options": ["...", "..."]
    }}
  ],
  "tows_matrix": {{
    "so_strategies": [
      {{
        "strategy": "Use [strength] to pursue [opportunity]",
        "strength": "...",
        "opportunity": "...",
        "description": "...",
        "priority": "high/medium/low"
      }}
    ],
    "wo_strategies": [
      {{
        "strategy": "Overcome [weakness] to pursue [opportunity]",
        "weakness": "...",
        "opportunity": "...",
        "description": "...",
        "priority": "high/medium/low"
      }}
    ],
    "st_strategies": [
      {{
        "strategy": "Use [strength] to mitigate [threat]",
        "strength": "...",
        "threat": "...",
        "description": "...",
        "priority": "high/medium/low"
      }}
    ],
    "wt_strategies": [
      {{
        "strategy": "Minimize [weakness] to avoid [threat]",
        "weakness": "...",
        "threat": "...",
        "description": "...",
        "priority": "high/medium/low"
      }}
    ]
  }},
  "prioritization": {{
    "top_strengths": ["...", "...", "..."],
    "critical_weaknesses": ["...", "...", "..."],
    "best_opportunities": ["...", "...", "..."],
    "biggest_threats": ["...", "...", "..."]
  }},
  "strategic_implications": [
    "Implication 1...",
    "Implication 2...",
    "Implication 3..."
  ],
  "recommended_focus_areas": [
    {{
      "area": "...",
      "rationale": "...",
      "actions": ["...", "..."]
    }}
  ],
  "confidence": "high/medium/low"
}}

Be specific, insightful, and actionable. Use all available context to make the analysis rich and detailed.
"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
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
        analysis['framework'] = 'SWOT Analysis'
        analysis['source'] = 'llm_analysis'

        return analysis

    except Exception as e:
        logger.error(f"Error conducting SWOT analysis: {e}")
        return {
            'error': str(e),
            'company_name': company_name,
            'framework': 'SWOT Analysis',
            'confidence': 'low'
        }
