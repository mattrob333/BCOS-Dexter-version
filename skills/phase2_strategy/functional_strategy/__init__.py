"""
Functional Strategy Skill

Develops strategic recommendations for each business function:
Sales, Marketing, Product, Operations, Finance, HR, IT/Technology.
"""

import json
import logging
from typing import Any, Dict
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SKILL_METADATA = {
    "name": "functional_strategy",
    "description": "Develop strategies for each business function",
    "phase": "phase2",
    "dependencies": ["value_chain_analysis", "org_structure_analysis"],
    "outputs": ["functional_strategy_analysis"]
}


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute functional strategy analysis for all departments."""
    logger.info(f"Executing Functional Strategy Analysis: {task.description if hasattr(task, 'description') else 'Functional Strategy'}")

    try:
        company_name = config.get("company", {}).get("name", "Unknown Company")
        industry = config.get("company", {}).get("industry", "")

        # Get all relevant context
        value_chain = context.get("value_chain_analysis", {})
        org_structure = context.get("org_structure_analysis", {})
        swot = context.get("swot_analysis", {})

        analysis = _develop_functional_strategies(
            company_name=company_name,
            industry=industry,
            value_chain=value_chain,
            org_structure=org_structure,
            swot=swot,
            config=config
        )

        logger.info("Functional strategy analysis completed")
        return {
            "status": "success",
            "data": analysis,
            "metadata": {
                "company": company_name,
                "analysis_type": "Functional Strategy",
                "skill": "functional_strategy"
            }
        }

    except Exception as e:
        logger.error(f"Error in functional strategy analysis: {str(e)}")
        return {"status": "error", "error": str(e), "data": {}}


def _develop_functional_strategies(
    company_name: str,
    industry: str,
    value_chain: Dict[str, Any],
    org_structure: Dict[str, Any],
    swot: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Develop functional strategies using Claude."""

    context_summary = _prepare_context_summary(value_chain, org_structure, swot)

    analysis_prompt = f"""You are a McKinsey functional strategy expert developing department-level strategies.

Company: {company_name}
Industry: {industry}

CONTEXT:
{context_summary}

## YOUR TASK

Develop comprehensive strategies for each major business function. For EACH function below, provide:

1. Current State Assessment
2. Strategic Objectives (aligned with company strategy)
3. Key Initiatives (3-5 concrete projects)
4. Success Metrics (KPIs)
5. Resource Requirements
6. Timeline and Milestones
7. Quick Wins (0-6 months)
8. Risks and Dependencies

## FUNCTIONS TO ANALYZE:

### 1. SALES STRATEGY

**Current State:**
- Sales model (inside, field, channel, etc.)
- Team size and structure
- Sales process maturity
- Current performance
- Key challenges

**Strategic Objectives:**
- Revenue growth targets
- Market expansion
- Customer acquisition
- Deal velocity improvement

**Key Initiatives:**
- Sales process optimization
- Team expansion/reorganization
- Territory management
- Sales enablement
- CRM/tools optimization
- Compensation redesign

**Success Metrics:**
- Revenue growth
- Win rate
- Average deal size
- Sales cycle length
- CAC
- Quota attainment

### 2. MARKETING STRATEGY

**Current State:**
- Marketing channels and mix
- Brand position
- Lead generation
- Content strategy
- Marketing technology stack

**Strategic Objectives:**
- Brand awareness
- Lead generation
- Customer engagement
- Market positioning

**Key Initiatives:**
- Digital marketing programs
- Content marketing
- Product marketing
- Brand campaigns
- Marketing automation
- Analyst relations

**Success Metrics:**
- Brand awareness
- Lead volume and quality
- MQL/SQL conversion
- CAC
- Marketing ROI
- Pipeline contribution

### 3. PRODUCT/ENGINEERING STRATEGY

**Current State:**
- Product portfolio
- Development process
- R&D investment
- Innovation capability
- Technical debt

**Strategic Objectives:**
- Product roadmap priorities
- Innovation goals
- Technical excellence
- Time to market

**Key Initiatives:**
- Product development projects
- Platform investments
- Architecture improvements
- Development process optimization
- Quality improvements

**Success Metrics:**
- Release velocity
- Product adoption
- Feature usage
- Technical debt reduction
- Customer satisfaction
- NPS

### 4. OPERATIONS STRATEGY

**Current State:**
- Operational processes
- Efficiency levels
- Quality metrics
- Technology enablement
- Capacity utilization

**Strategic Objectives:**
- Operational excellence
- Scalability
- Cost optimization
- Quality improvement

**Key Initiatives:**
- Process automation
- Quality management
- Capacity expansion
- Supply chain optimization
- Vendor management

**Success Metrics:**
- Operational efficiency
- Cost per unit
- Quality metrics
- On-time delivery
- Capacity utilization
- Error rates

### 5. FINANCE STRATEGY

**Current State:**
- Financial health
- FP&A maturity
- Reporting capabilities
- Cost structure
- Capital structure

**Strategic Objectives:**
- Financial sustainability
- Strategic planning capability
- Cost management
- Capital efficiency

**Key Initiatives:**
- FP&A process improvement
- Cost optimization
- Pricing strategy
- Cash flow management
- Financial systems

**Success Metrics:**
- Revenue growth
- Profitability margins
- Cash flow
- Budget accuracy
- Days sales outstanding
- Burn rate (if applicable)

### 6. HUMAN RESOURCES STRATEGY

**Current State:**
- Talent quality and gaps
- Culture and engagement
- HR processes
- Compensation philosophy
- Learning & development

**Strategic Objectives:**
- Talent acquisition
- Employee development
- Culture building
- Retention improvement

**Key Initiatives:**
- Recruitment strategy
- L&D programs
- Performance management
- Compensation redesign
- Culture initiatives
- Diversity & inclusion

**Success Metrics:**
- Employee satisfaction
- Retention rate
- Time to hire
- Quality of hire
- Training completion
- Diversity metrics

### 7. IT/TECHNOLOGY STRATEGY

**Current State:**
- Technology stack
- IT infrastructure
- Security posture
- Digital maturity
- Tech debt

**Strategic Objectives:**
- Digital transformation
- Security and compliance
- Technology enablement
- Data strategy

**Key Initiatives:**
- Infrastructure modernization
- Security improvements
- Data platform
- Application rationalization
- Cloud migration
- Automation

**Success Metrics:**
- System uptime
- Security incidents
- IT costs as % revenue
- Project delivery
- User satisfaction
- Automation level

### 8. CROSS-FUNCTIONAL ALIGNMENT

Analyze how functions must work together:
- Critical dependencies
- Integration points
- Shared objectives
- Collaboration needs
- Communication protocols

Provide analysis in valid JSON:
{{
    "functional_strategies": {{
        "sales": {{
            "current_state": {{
                "model": "...",
                "maturity": "nascent|developing|maturing|mature",
                "key_challenges": ["...", "..."]
            }},
            "strategic_objectives": ["...", "..."],
            "key_initiatives": [
                {{
                    "initiative": "...",
                    "description": "...",
                    "priority": "p0|p1|p2",
                    "timeline": "...",
                    "investment": "..."
                }}
            ],
            "success_metrics": [
                {{
                    "metric": "...",
                    "target": "...",
                    "current": "..."
                }}
            ],
            "quick_wins": ["...", "..."],
            "risks": ["...", "..."]
        }},
        "marketing": {{...}},
        "product_engineering": {{...}},
        "operations": {{...}},
        "finance": {{...}},
        "human_resources": {{...}},
        "it_technology": {{...}}
    }},
    "cross_functional_alignment": {{
        "critical_dependencies": [
            {{
                "functions": ["sales", "marketing"],
                "dependency": "...",
                "alignment_level": "strong|moderate|weak"
            }}
        ],
        "shared_objectives": ["...", "..."],
        "collaboration_needs": ["...", "..."]
    }},
    "investment_priorities": [
        {{
            "function": "...",
            "initiative": "...",
            "investment": "...",
            "expected_roi": "...",
            "priority": 1
        }}
    ],
    "executive_summary": {{
        "overall_functional_maturity": "nascent|developing|maturing|mature",
        "strongest_functions": ["...", "..."],
        "weakest_functions": ["...", "..."],
        "top_investment_priorities": ["...", "..."],
        "total_investment_required": "...",
        "expected_outcomes": "..."
    }}
}}"""

    try:
        client = Anthropic(api_key=config.get("llm", {}).get("api_key"))
        response = client.messages.create(
            model=config.get("llm", {}).get("model", "claude-3-5-sonnet-20241022"),
            max_tokens=16000,
            temperature=0.7,
            messages=[{"role": "user", "content": analysis_prompt}]
        )

        response_text = response.content[0].text

        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()

        return json.loads(response_text)

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {str(e)}")
        return {"error": "Failed to parse analysis", "raw_response": response_text[:500]}
    except Exception as e:
        logger.error(f"Error calling Claude API: {str(e)}")
        raise


def _prepare_context_summary(
    value_chain: Dict[str, Any],
    org_structure: Dict[str, Any],
    swot: Dict[str, Any]
) -> str:
    """Prepare context summary."""
    summary_parts = []

    if value_chain:
        summary_parts.append("VALUE CHAIN: See previous analysis")

    if org_structure:
        summary_parts.append("ORG STRUCTURE: See previous analysis")

    if swot:
        summary_parts.append("SWOT: See previous analysis")

    return "\n".join(summary_parts) if summary_parts else "Limited context."
