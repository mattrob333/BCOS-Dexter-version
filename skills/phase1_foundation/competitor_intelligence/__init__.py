"""
Competitor Intelligence Skill.

Profiles key competitors, analyzes their strategies, strengths, weaknesses,
and positioning in the market.
"""

from typing import Dict, Any, List
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
    Execute competitor intelligence gathering.

    Analyzes:
    - Competitor profiles
    - Product/service comparison
    - Market positioning
    - Strengths and weaknesses
    - Strategic moves
    - Competitive advantages

    Args:
        task: Task object with description
        context: Execution context (including company and market intelligence)
        config: BCOS configuration

    Returns:
        Dictionary with competitor intelligence findings
    """
    logger.info("Executing Competitor Intelligence skill")

    company = context.get('company', config.get('company', {}))
    company_name = company.get('name', 'Unknown')
    industry = company.get('industry', 'Unknown')

    # Get list of competitors from config
    competitors = config.get('competitors', [])

    if not competitors:
        logger.warning("No competitors specified in config - will identify key competitors")

    # Get context from previous Phase 1 tasks
    company_intel = context.get('company_intelligence', {})
    market_intel = context.get('market_intelligence', {})

    # Analyze competitors
    competitor_analysis = _analyze_competitors(
        company_name=company_name,
        industry=industry,
        competitors=competitors,
        company_intel=company_intel,
        market_intel=market_intel,
        config=config
    )

    logger.info(f"Competitor intelligence gathered for {len(competitors)} competitors")

    return competitor_analysis


def _analyze_competitors(
    company_name: str,
    industry: str,
    competitors: List[str],
    company_intel: Dict[str, Any],
    market_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze competitors in detail.

    Args:
        company_name: Name of the company
        industry: Industry vertical
        competitors: List of competitor names
        company_intel: Company intelligence from Phase 1
        market_intel: Market intelligence from Phase 1
        config: BCOS configuration

    Returns:
        Comprehensive competitor analysis
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Extract relevant context
    business_description = company_intel.get('business_description', '')
    products_services = company_intel.get('products_services', [])
    value_proposition = company_intel.get('value_proposition', '')

    # Market context
    market_segments = market_intel.get('market_segments', [])
    market_trends = market_intel.get('trends', [])

    context_summary = f"""
Company: {company_name}
Industry: {industry}
Business Description: {business_description}
Products/Services: {', '.join(products_services) if isinstance(products_services, list) else products_services}
Value Proposition: {value_proposition}

Competitors to Analyze: {', '.join(competitors)}

Market Context:
- Key segments: {', '.join([s.get('segment_name', '') for s in market_segments[:3]]) if market_segments else 'N/A'}
- Key trends: {', '.join([t.get('trend', '') for t in market_trends[:3]]) if market_trends else 'N/A'}
"""

    prompt = f"""Conduct comprehensive competitor intelligence analysis.

{context_summary}

For each competitor, provide detailed analysis across these dimensions:

1. **Company Profile**
   - Company size (revenue, employees, funding)
   - Geographic presence
   - Target markets
   - Ownership structure (public, private, PE-backed)

2. **Products & Services**
   - Core offerings
   - Product portfolio breadth
   - Product differentiation
   - Pricing strategy

3. **Market Positioning**
   - Target customer segments
   - Value proposition
   - Brand positioning
   - Market share estimate

4. **Strengths**
   - Competitive advantages
   - What they do well
   - Key capabilities
   - Strategic assets

5. **Weaknesses**
   - Vulnerabilities
   - What they struggle with
   - Gaps in offering
   - Strategic liabilities

6. **Strategic Focus**
   - Current strategy
   - Recent moves (M&A, partnerships, product launches)
   - Investment priorities
   - Strategic direction

7. **Competitive Threat Level**
   - How much of a threat are they to our company?
   - In which segments do they compete?
   - How are they differentiated from us?

Also provide:
- Competitive positioning map
- Feature/capability comparison matrix
- Strategic group analysis

Return a detailed JSON object:

{{
  "competitor_profiles": [
    {{
      "name": "...",
      "profile": {{
        "revenue": "...",
        "employees": "...",
        "funding": "...",
        "headquarters": "...",
        "geographic_presence": ["...", "..."],
        "founded": "...",
        "ownership": "public/private/..."
      }},
      "products_services": {{
        "core_products": ["...", "..."],
        "portfolio_breadth": "narrow/moderate/wide",
        "differentiation": "...",
        "pricing_strategy": "premium/value/penetration",
        "pricing_model": "..."
      }},
      "market_positioning": {{
        "target_segments": ["...", "..."],
        "value_proposition": "...",
        "brand_position": "...",
        "market_share": "...%",
        "positioning_statement": "..."
      }},
      "strengths": [
        {{
          "strength": "...",
          "category": "product/brand/operations/financial",
          "impact": "high/medium/low",
          "description": "..."
        }}
      ],
      "weaknesses": [
        {{
          "weakness": "...",
          "category": "product/brand/operations/financial",
          "exploitability": "high/medium/low",
          "description": "..."
        }}
      ],
      "strategy": {{
        "current_focus": "...",
        "recent_moves": ["...", "..."],
        "investment_priorities": ["...", "..."],
        "strategic_direction": "..."
      }},
      "threat_assessment": {{
        "threat_level": "critical/high/medium/low",
        "overlapping_segments": ["...", "..."],
        "differentiation_vs_us": "...",
        "areas_of_direct_competition": ["...", "..."],
        "areas_where_we_win": ["...", "..."],
        "areas_where_they_win": ["...", "..."]
      }}
    }}
  ],
  "competitive_landscape": {{
    "market_leaders": ["...", "..."],
    "emerging_challengers": ["...", "..."],
    "niche_players": ["...", "..."],
    "our_position": "leader/challenger/follower/niche"
  }},
  "competitive_positioning_map": {{
    "axis_1": "price (low to high)",
    "axis_2": "feature breadth (narrow to wide)",
    "positions": [
      {{"company": "Our Company", "x": 7, "y": 8}},
      {{"company": "Competitor A", "x": 5, "y": 6}}
    ]
  }},
  "feature_comparison": {{
    "features": ["Feature 1", "Feature 2", "Feature 3"],
    "companies": {{
      "Our Company": [true, true, true],
      "Competitor A": [true, false, true]
    }}
  }},
  "strategic_groups": [
    {{
      "group_name": "Premium Full-Stack Providers",
      "members": ["...", "..."],
      "characteristics": ["...", "..."],
      "strategy": "..."
    }}
  ],
  "competitive_insights": [
    "Key insight 1...",
    "Key insight 2...",
    "Key insight 3..."
  ],
  "recommendations": [
    "Recommendation 1...",
    "Recommendation 2..."
  ],
  "confidence": "high/medium/low"
}}

Be thorough and specific. Focus on actionable competitive intelligence.
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
        analysis['analysis_type'] = 'competitor_intelligence'
        analysis['competitors_analyzed'] = len(competitors)
        analysis['source'] = 'llm_analysis'

        return analysis

    except Exception as e:
        logger.error(f"Error analyzing competitors: {e}")
        return {
            'error': str(e),
            'company_name': company_name,
            'industry': industry,
            'analysis_type': 'competitor_intelligence',
            'confidence': 'low'
        }
