"""
Business Model Canvas Skill.

Analyzes a company's business model using the Business Model Canvas framework.
The BMC breaks down business models into 9 key building blocks.
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
    Execute Business Model Canvas analysis.

    The BMC framework analyzes:
    1. Customer Segments - Who are the customers?
    2. Value Propositions - What value do we deliver?
    3. Channels - How do we reach customers?
    4. Customer Relationships - How do we interact with customers?
    5. Revenue Streams - How do we make money?
    6. Key Resources - What assets are required?
    7. Key Activities - What key things must we do?
    8. Key Partnerships - Who are our partners?
    9. Cost Structure - What are the main costs?

    Args:
        task: Task object with description
        context: Execution context (including company intelligence)
        config: BCOS configuration

    Returns:
        Dictionary with Business Model Canvas analysis
    """
    logger.info("Executing Business Model Canvas skill")

    company = context.get('company', config.get('company', {}))
    company_name = company.get('name', 'Unknown')

    # Get company intelligence from Phase 1 context
    company_intel = context.get('company_intelligence', {})

    # Build BMC using LLM with context
    bmc_analysis = _analyze_business_model_canvas(
        company_name=company_name,
        company_intel=company_intel,
        config=config
    )

    logger.info(f"Business Model Canvas completed for {company_name}")

    return bmc_analysis


def _analyze_business_model_canvas(
    company_name: str,
    company_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze company's business model using BMC framework.

    Args:
        company_name: Name of the company
        company_intel: Company intelligence from previous Phase 1 task
        config: BCOS configuration

    Returns:
        Complete Business Model Canvas analysis
    """
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    # Extract relevant context
    business_description = company_intel.get('business_description', '')
    products_services = company_intel.get('products_services', [])
    target_customers = company_intel.get('target_customers', '')
    value_proposition = company_intel.get('value_proposition', '')
    business_model = company_intel.get('business_model', '')
    industry = config.get('company', {}).get('industry', 'Unknown')

    # Build context summary
    context_summary = f"""
Company: {company_name}
Industry: {industry}
Business Description: {business_description}
Products/Services: {', '.join(products_services) if isinstance(products_services, list) else products_services}
Target Customers: {target_customers}
Value Proposition: {value_proposition}
Business Model: {business_model}
"""

    prompt = f"""Analyze this company's business model using the Business Model Canvas framework.

{context_summary}

Create a comprehensive Business Model Canvas analysis covering all 9 building blocks:

1. **Customer Segments**: Who are the different groups of customers? (e.g., mass market, niche, segmented, diversified, multi-sided)

2. **Value Propositions**: What value does the company deliver to each customer segment? What problems are solved? What needs are satisfied?

3. **Channels**: Through what channels does the company reach each customer segment? (awareness, evaluation, purchase, delivery, after-sales)

4. **Customer Relationships**: What type of relationships does the company establish with each segment? (personal, automated, self-service, communities, co-creation)

5. **Revenue Streams**: How does the company generate revenue from each segment? (asset sale, usage fee, subscription, lending/leasing, licensing, brokerage, advertising)

6. **Key Resources**: What key assets are required to make the business model work? (physical, intellectual, human, financial)

7. **Key Activities**: What key activities must the company perform? (production, problem-solving, platform/network)

8. **Key Partnerships**: Who are the key partners and suppliers? What do they provide?

9. **Cost Structure**: What are the most important costs? (cost-driven vs value-driven, fixed vs variable, economies of scale/scope)

Return a detailed JSON object:

{{
  "customer_segments": [
    {{
      "segment_name": "...",
      "description": "...",
      "characteristics": ["...", "..."],
      "size_estimate": "..."
    }}
  ],
  "value_propositions": [
    {{
      "for_segment": "...",
      "core_value": "...",
      "problems_solved": ["...", "..."],
      "needs_satisfied": ["...", "..."],
      "differentiation": "..."
    }}
  ],
  "channels": {{
    "awareness": ["...", "..."],
    "evaluation": ["...", "..."],
    "purchase": ["...", "..."],
    "delivery": ["...", "..."],
    "after_sales": ["...", "..."]
  }},
  "customer_relationships": [
    {{
      "segment": "...",
      "relationship_type": "...",
      "description": "...",
      "examples": ["...", "..."]
    }}
  ],
  "revenue_streams": [
    {{
      "stream_type": "...",
      "description": "...",
      "pricing_mechanism": "...",
      "contribution": "..."
    }}
  ],
  "key_resources": {{
    "physical": ["...", "..."],
    "intellectual": ["...", "..."],
    "human": ["...", "..."],
    "financial": ["...", "..."]
  }},
  "key_activities": [
    {{
      "activity": "...",
      "category": "production/problem-solving/platform",
      "importance": "critical/important/supporting",
      "description": "..."
    }}
  ],
  "key_partnerships": [
    {{
      "partner_type": "...",
      "partners": ["...", "..."],
      "motivation": "...",
      "what_they_provide": "..."
    }}
  ],
  "cost_structure": {{
    "model": "cost-driven/value-driven",
    "major_costs": [
      {{
        "cost_category": "...",
        "type": "fixed/variable",
        "description": "...",
        "significance": "..."
      }}
    ],
    "economies_of_scale": "...",
    "economies_of_scope": "..."
  }},
  "insights": [
    "Key insight 1...",
    "Key insight 2...",
    "Key insight 3..."
  ],
  "bmc_archetype": "unbundled/long-tail/multi-sided-platform/free/open",
  "confidence": "high/medium/low"
}}

Be specific, detailed, and insightful. Use your knowledge of the company and industry.
"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
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
        analysis['framework'] = 'Business Model Canvas'
        analysis['source'] = 'llm_analysis'

        return analysis

    except Exception as e:
        logger.error(f"Error analyzing Business Model Canvas: {e}")
        return {
            'error': str(e),
            'company_name': company_name,
            'framework': 'Business Model Canvas',
            'confidence': 'low'
        }
