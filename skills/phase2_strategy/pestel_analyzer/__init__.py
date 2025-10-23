"""
PESTEL Analyzer Skill.

Analyzes the macro-environmental factors affecting the company using
the PESTEL framework (Political, Economic, Social, Technological,
Environmental, Legal).
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
    Execute PESTEL analysis.

    Analyzes 6 macro-environmental dimensions:
    1. Political - Government policies, regulations, stability
    2. Economic - Economic trends, cycles, conditions
    3. Social - Demographics, culture, values
    4. Technological - Innovation, disruption, tech trends
    5. Environmental - Sustainability, climate, resource issues
    6. Legal - Laws, regulations, compliance requirements

    Args:
        task: Task object with description
        context: Execution context (full Phase 1 context)
        config: BCOS configuration

    Returns:
        Dictionary with PESTEL analysis
    """
    logger.info("Executing PESTEL Analysis skill")

    company = context.get('company', config.get('company', {}))
    company_name = company.get('name', 'Unknown')
    industry = company.get('industry', 'Unknown')

    # Get Phase 1 context
    company_intel = context.get('company_intelligence', {})
    market_intel = context.get('market_intelligence', {})

    # Conduct PESTEL analysis
    pestel_analysis = _conduct_pestel_analysis(
        company_name=company_name,
        industry=industry,
        company_intel=company_intel,
        market_intel=market_intel,
        config=config
    )

    logger.info(f"PESTEL analysis completed for {company_name}")

    return pestel_analysis


def _conduct_pestel_analysis(
    company_name: str,
    industry: str,
    company_intel: Dict[str, Any],
    market_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Conduct PESTEL analysis of macro-environmental factors.

    Args:
        company_name: Name of the company
        industry: Industry vertical
        company_intel: Company intelligence from Phase 1
        market_intel: Market intelligence from Phase 1
        config: BCOS configuration

    Returns:
        Complete PESTEL analysis
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Extract context
    business_description = company_intel.get('business_description', '')
    products_services = company_intel.get('products_services', [])

    # Market context
    market_trends = market_intel.get('trends', [])
    market_drivers = market_intel.get('drivers', [])

    context_summary = f"""
Company: {company_name}
Industry: {industry}
Business: {business_description}
Products/Services: {', '.join(products_services) if isinstance(products_services, list) else products_services}

Market Context:
- Key Trends: {', '.join([t.get('trend', '') for t in market_trends[:3]]) if market_trends else 'N/A'}
- Market Drivers: {', '.join([d.get('driver', '') for d in market_drivers[:3]]) if market_drivers else 'N/A'}
"""

    prompt = f"""Conduct a comprehensive PESTEL analysis for this company.

{context_summary}

Analyze all 6 macro-environmental dimensions:

**POLITICAL Factors**
Government policies, regulations, trade restrictions, tax policy, political stability, lobbying, government spending

Analyze:
- Relevant government policies affecting the industry
- Regulatory environment (favorable/unfavorable)
- Political stability in key markets
- Trade policies and tariffs
- Government spending priorities
- Lobbying and political influence

**ECONOMIC Factors**
Economic growth, interest rates, exchange rates, inflation, unemployment, disposable income, economic cycles

Analyze:
- Overall economic conditions in key markets
- Interest rate environment
- Exchange rate fluctuations (for global companies)
- Inflation trends and impact
- Consumer spending patterns
- Economic outlook (growth/recession)

**SOCIAL Factors**
Demographics, cultural attitudes, lifestyle changes, education levels, population growth, age distribution, health consciousness

Analyze:
- Demographic trends affecting the business
- Cultural shifts and changing values
- Lifestyle and behavioral changes
- Education and skill levels
- Attitudes toward the company/industry
- Social movements relevant to the business

**TECHNOLOGICAL Factors**
R&D activity, automation, technology incentives, rate of technological change, innovation, digital transformation

Analyze:
- Technological disruptions in the industry
- Rate of innovation and change
- Automation opportunities/threats
- Digital transformation trends
- Emerging technologies
- R&D landscape

**ENVIRONMENTAL Factors**
Climate change, sustainability, resource scarcity, pollution, carbon footprint, renewable energy, waste management

Analyze:
- Environmental regulations affecting the business
- Sustainability requirements and expectations
- Climate change impacts
- Resource availability and scarcity
- Carbon/environmental footprint concerns
- Circular economy trends

**LEGAL Factors**
Consumer laws, employment laws, health & safety, data protection, antitrust, intellectual property, industry regulations

Analyze:
- Key legal/regulatory requirements
- Compliance burden
- Intellectual property landscape
- Data privacy and security regulations
- Employment and labor laws
- Industry-specific regulations

For each factor, provide:
- Current state and trends
- Impact on the company (positive/negative/neutral)
- Opportunities created
- Threats posed
- Strategic implications

Return a detailed JSON object:

{{
  "political": {{
    "factors": [
      {{
        "factor": "...",
        "description": "...",
        "impact": "positive/negative/neutral",
        "magnitude": "high/medium/low",
        "trend": "improving/stable/worsening",
        "geographic_scope": "global/regional/national/local"
      }}
    ],
    "opportunities": ["...", "..."],
    "threats": ["...", "..."],
    "overall_impact": "positive/negative/neutral",
    "strategic_implications": "..."
  }},
  "economic": {{
    "factors": [
      {{
        "factor": "...",
        "description": "...",
        "impact": "positive/negative/neutral",
        "magnitude": "high/medium/low",
        "trend": "improving/stable/worsening",
        "timeframe": "immediate/short-term/medium-term/long-term"
      }}
    ],
    "opportunities": ["...", "..."],
    "threats": ["...", "..."],
    "overall_impact": "positive/negative/neutral",
    "strategic_implications": "..."
  }},
  "social": {{
    "factors": [
      {{
        "factor": "...",
        "description": "...",
        "impact": "positive/negative/neutral",
        "magnitude": "high/medium/low",
        "trend": "improving/stable/worsening"
      }}
    ],
    "demographic_trends": ["...", "..."],
    "cultural_shifts": ["...", "..."],
    "opportunities": ["...", "..."],
    "threats": ["...", "..."],
    "overall_impact": "positive/negative/neutral",
    "strategic_implications": "..."
  }},
  "technological": {{
    "factors": [
      {{
        "factor": "...",
        "description": "...",
        "impact": "positive/negative/neutral",
        "magnitude": "high/medium/low",
        "maturity": "emerging/developing/mature",
        "adoption_rate": "slow/moderate/rapid"
      }}
    ],
    "disruptive_technologies": ["...", "..."],
    "innovation_areas": ["...", "..."],
    "opportunities": ["...", "..."],
    "threats": ["...", "..."],
    "overall_impact": "positive/negative/neutral",
    "strategic_implications": "..."
  }},
  "environmental": {{
    "factors": [
      {{
        "factor": "...",
        "description": "...",
        "impact": "positive/negative/neutral",
        "magnitude": "high/medium/low",
        "urgency": "immediate/short-term/long-term",
        "regulatory_pressure": "high/medium/low"
      }}
    ],
    "sustainability_requirements": ["...", "..."],
    "climate_risks": ["...", "..."],
    "opportunities": ["...", "..."],
    "threats": ["...", "..."],
    "overall_impact": "positive/negative/neutral",
    "strategic_implications": "..."
  }},
  "legal": {{
    "factors": [
      {{
        "factor": "...",
        "description": "...",
        "impact": "positive/negative/neutral",
        "magnitude": "high/medium/low",
        "compliance_burden": "high/medium/low",
        "enforcement_risk": "high/medium/low"
      }}
    ],
    "regulatory_changes": ["...", "..."],
    "compliance_requirements": ["...", "..."],
    "opportunities": ["...", "..."],
    "threats": ["...", "..."],
    "overall_impact": "positive/negative/neutral",
    "strategic_implications": "..."
  }},
  "summary": {{
    "most_favorable_dimension": "...",
    "most_challenging_dimension": "...",
    "top_opportunities": ["...", "...", "..."],
    "top_threats": ["...", "...", "..."],
    "overall_macro_environment": "favorable/neutral/unfavorable",
    "key_trends_to_monitor": ["...", "...", "..."]
  }},
  "strategic_recommendations": [
    {{
      "recommendation": "...",
      "dimension": "political/economic/social/technological/environmental/legal",
      "priority": "high/medium/low",
      "rationale": "..."
    }}
  ],
  "confidence": "high/medium/low"
}}

Be thorough and specific. Focus on factors most relevant to this company and industry.
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
        analysis['industry'] = industry
        analysis['framework'] = 'PESTEL Analysis'
        analysis['source'] = 'llm_analysis'

        return analysis

    except Exception as e:
        logger.error(f"Error conducting PESTEL analysis: {e}")
        return {
            'error': str(e),
            'company_name': company_name,
            'industry': industry,
            'framework': 'PESTEL Analysis',
            'confidence': 'low'
        }
