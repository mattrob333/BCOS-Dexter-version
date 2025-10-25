"""
Value Chain Mapper Skill

Analyzes a company's value chain using Porter's Value Chain framework.
Maps primary and support activities, identifies optimization opportunities.
"""

import json
import logging
from typing import Any, Dict
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SKILL_METADATA = {
    "name": "value_chain_mapper",
    "description": "Analyzes company value chain using Porter's framework",
    "phase": "phase1",
    "dependencies": ["company_intelligence"],
    "outputs": ["value_chain_analysis"]
}


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute value chain mapping analysis.

    Analyzes both primary and support activities using Porter's Value Chain framework.

    Args:
        task: Task object with description and requirements
        context: Execution context with company intelligence and other phase 1 data
        config: Configuration including company details and API keys

    Returns:
        Dict containing comprehensive value chain analysis
    """
    logger.info(f"Executing Value Chain Mapper: {task.description if hasattr(task, 'description') else 'Value Chain Analysis'}")

    try:
        company_name = config.get("company", {}).get("name", "Unknown Company")
        company_website = config.get("company", {}).get("website", "")
        industry = config.get("company", {}).get("industry", "")

        # Get company intelligence from context
        company_intel = context.get("company_intelligence", {})
        business_model = context.get("business_model_canvas", {})

        # Perform value chain analysis
        analysis = _analyze_value_chain(
            company_name=company_name,
            industry=industry,
            company_intel=company_intel,
            business_model=business_model,
            config=config
        )

        logger.info("Value chain analysis completed successfully")
        return {
            "status": "success",
            "data": analysis,
            "metadata": {
                "company": company_name,
                "framework": "Porter's Value Chain",
                "skill": "value_chain_mapper"
            }
        }

    except Exception as e:
        logger.error(f"Error in value chain analysis: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "data": {}
        }


def _analyze_value_chain(
    company_name: str,
    industry: str,
    company_intel: Dict[str, Any],
    business_model: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze company value chain using Claude.

    Args:
        company_name: Company name
        industry: Industry sector
        company_intel: Company intelligence data from previous analysis
        business_model: Business model canvas data
        config: Configuration with API keys

    Returns:
        Comprehensive value chain analysis
    """

    # Prepare context from previous analyses
    context_summary = _prepare_context_summary(company_intel, business_model)

    analysis_prompt = f"""You are a McKinsey-level strategy consultant performing a Value Chain Analysis.

Company: {company_name}
Industry: {industry}

CONTEXT FROM PREVIOUS ANALYSES:
{context_summary}

Analyze this company's value chain using Porter's Value Chain framework. Provide a comprehensive analysis covering:

## PRIMARY ACTIVITIES

### 1. Inbound Logistics
- How the company receives, stores, and distributes inputs
- Key suppliers and procurement processes
- Inventory management approach
- Quality control systems
- Strengths and weaknesses
- Optimization opportunities

### 2. Operations
- Core production/service delivery processes
- Technology and systems used
- Quality management
- Capacity and scalability
- Operational efficiency level
- Cost drivers
- Strengths and weaknesses
- Optimization opportunities

### 3. Outbound Logistics
- How products/services are delivered to customers
- Distribution channels and networks
- Order fulfillment processes
- Warehousing and shipping
- Customer delivery experience
- Strengths and weaknesses
- Optimization opportunities

### 4. Marketing & Sales
- Marketing strategies and channels
- Sales processes and team structure
- Brand positioning
- Customer acquisition costs
- Lead generation effectiveness
- Sales conversion rates
- Strengths and weaknesses
- Optimization opportunities

### 5. Service
- Post-sale customer support
- Warranty and returns processes
- Customer success programs
- Technical support
- Customer retention initiatives
- Net Promoter Score indicators
- Strengths and weaknesses
- Optimization opportunities

## SUPPORT ACTIVITIES

### 6. Firm Infrastructure
- Management and organizational structure
- Planning and finance systems
- Legal and compliance
- Quality management systems
- Corporate culture
- Strengths and weaknesses
- Optimization opportunities

### 7. Human Resource Management
- Recruitment and hiring processes
- Training and development programs
- Compensation and benefits
- Employee retention
- Talent management
- Culture and engagement
- Strengths and weaknesses
- Optimization opportunities

### 8. Technology Development
- R&D activities and innovation capacity
- Technology stack and infrastructure
- Digital transformation initiatives
- Data and analytics capabilities
- IP and patents
- Innovation culture
- Strengths and weaknesses
- Optimization opportunities

### 9. Procurement
- Supplier relationships and management
- Purchasing processes
- Vendor negotiation strategies
- Supply chain resilience
- Cost management
- Strengths and weaknesses
- Optimization opportunities

## VALUE CHAIN INTEGRATION

### Activity Linkages
Analyze how activities connect and reinforce each other:
- Which activities are tightly integrated?
- Where are there gaps or friction points?
- How do primary and support activities interact?
- Which linkages create competitive advantage?

### Cost Analysis
- Where are the major costs concentrated?
- Which activities drive the most value?
- Are costs aligned with strategic priorities?
- Opportunities for cost reduction

### Differentiation Analysis
- Which activities contribute most to differentiation?
- Where does the company create unique value?
- How sustainable are these advantages?

## STRATEGIC RECOMMENDATIONS

### Quick Wins (0-6 months)
List 3-5 immediate optimization opportunities with:
- Specific activity to improve
- Expected impact
- Implementation difficulty
- Resource requirements

### Medium-term Improvements (6-18 months)
List 3-5 strategic initiatives with:
- Activities to transform
- Expected impact
- Dependencies
- Investment required

### Long-term Strategic Shifts (18+ months)
List 2-3 major value chain transformations with:
- Vision for the transformed activity
- Competitive advantage created
- Risk factors
- Success metrics

Provide your analysis in valid JSON format with this exact structure:
{{
    "primary_activities": {{
        "inbound_logistics": {{
            "description": "...",
            "key_processes": ["...", "..."],
            "strengths": ["...", "..."],
            "weaknesses": ["...", "..."],
            "optimization_opportunities": ["...", "..."]
        }},
        "operations": {{...}},
        "outbound_logistics": {{...}},
        "marketing_sales": {{...}},
        "service": {{...}}
    }},
    "support_activities": {{
        "firm_infrastructure": {{...}},
        "human_resources": {{...}},
        "technology_development": {{...}},
        "procurement": {{...}}
    }},
    "integration_analysis": {{
        "activity_linkages": [
            {{
                "activities": ["...", "..."],
                "relationship": "...",
                "strength": "strong|medium|weak",
                "strategic_impact": "..."
            }}
        ],
        "cost_structure": {{
            "major_cost_centers": ["...", "..."],
            "cost_efficiency_rating": "high|medium|low",
            "optimization_potential": "..."
        }},
        "differentiation_drivers": [
            {{
                "activity": "...",
                "contribution": "...",
                "sustainability": "high|medium|low"
            }}
        ]
    }},
    "strategic_recommendations": {{
        "quick_wins": [
            {{
                "activity": "...",
                "recommendation": "...",
                "expected_impact": "...",
                "difficulty": "low|medium|high",
                "resources_required": "..."
            }}
        ],
        "medium_term": [...],
        "long_term": [...]
    }},
    "executive_summary": {{
        "overall_assessment": "...",
        "key_strengths": ["...", "..."],
        "critical_gaps": ["...", "..."],
        "top_priorities": ["...", "..."]
    }}
}}"""

    # Call Claude API
    try:
        client = Anthropic(api_key=config.get("llm", {}).get("api_key"))

        response = client.messages.create(
            model=config.get("llm", {}).get("model", "claude-3-5-sonnet-20241022"),
            max_tokens=16000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": analysis_prompt
            }]
        )

        # Extract and parse JSON response
        response_text = response.content[0].text

        # Try to extract JSON from markdown code blocks if present
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()

        analysis = json.loads(response_text)
        return analysis

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {str(e)}")
        logger.debug(f"Response text: {response_text}")
        # Return structured error
        return {
            "error": "Failed to parse analysis",
            "raw_response": response_text[:500]
        }
    except Exception as e:
        logger.error(f"Error calling Claude API: {str(e)}")
        raise


def _prepare_context_summary(company_intel: Dict[str, Any], business_model: Dict[str, Any]) -> str:
    """Prepare a concise summary of context from previous analyses."""

    summary_parts = []

    # Company intelligence summary
    if company_intel:
        summary_parts.append("COMPANY INTELLIGENCE:")
        if "business_overview" in company_intel:
            summary_parts.append(f"- Overview: {company_intel['business_overview'][:300]}...")
        if "products_services" in company_intel:
            summary_parts.append(f"- Products/Services: {', '.join(company_intel['products_services'][:3])}")
        if "target_market" in company_intel:
            summary_parts.append(f"- Target Market: {company_intel['target_market']}")

    # Business model summary
    if business_model:
        summary_parts.append("\nBUSINESS MODEL:")
        if "value_propositions" in business_model:
            vp = business_model["value_propositions"]
            if isinstance(vp, dict) and "core_value_propositions" in vp:
                summary_parts.append(f"- Value Props: {', '.join(vp['core_value_propositions'][:3])}")
        if "revenue_streams" in business_model:
            rs = business_model["revenue_streams"]
            if isinstance(rs, dict) and "streams" in rs:
                summary_parts.append(f"- Revenue Streams: {', '.join([s.get('type', '') for s in rs['streams'][:3]])}")

    return "\n".join(summary_parts) if summary_parts else "Limited context available - performing analysis based on industry best practices."
