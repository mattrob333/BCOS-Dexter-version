"""
Organizational Structure Analyzer Skill

Analyzes company organizational structure, leadership, reporting relationships,
and organizational effectiveness.
"""

import json
import logging
from typing import Any, Dict
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SKILL_METADATA = {
    "name": "org_structure_analyzer",
    "description": "Analyzes organizational structure, leadership, and effectiveness",
    "phase": "phase1",
    "dependencies": ["company_intelligence"],
    "outputs": ["org_structure_analysis"]
}


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute organizational structure analysis.

    Analyzes leadership, org structure, decision-making, and organizational health.

    Args:
        task: Task object with description and requirements
        context: Execution context with company intelligence and other phase 1 data
        config: Configuration including company details and API keys

    Returns:
        Dict containing comprehensive organizational analysis
    """
    logger.info(f"Executing Org Structure Analyzer: {task.description if hasattr(task, 'description') else 'Org Structure Analysis'}")

    try:
        company_name = config.get("company", {}).get("name", "Unknown Company")
        company_website = config.get("company", {}).get("website", "")
        industry = config.get("company", {}).get("industry", "")

        # Get context from previous analyses
        company_intel = context.get("company_intelligence", {})
        business_model = context.get("business_model_canvas", {})
        value_chain = context.get("value_chain_analysis", {})

        # Perform organizational structure analysis
        analysis = _analyze_org_structure(
            company_name=company_name,
            industry=industry,
            company_intel=company_intel,
            business_model=business_model,
            value_chain=value_chain,
            config=config
        )

        logger.info("Organizational structure analysis completed successfully")
        return {
            "status": "success",
            "data": analysis,
            "metadata": {
                "company": company_name,
                "analysis_type": "Organizational Structure",
                "skill": "org_structure_analyzer"
            }
        }

    except Exception as e:
        logger.error(f"Error in org structure analysis: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "data": {}
        }


def _analyze_org_structure(
    company_name: str,
    industry: str,
    company_intel: Dict[str, Any],
    business_model: Dict[str, Any],
    value_chain: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze organizational structure using Claude.

    Args:
        company_name: Company name
        industry: Industry sector
        company_intel: Company intelligence data
        business_model: Business model canvas data
        value_chain: Value chain analysis data
        config: Configuration with API keys

    Returns:
        Comprehensive organizational structure analysis
    """

    # Prepare context from previous analyses
    context_summary = _prepare_context_summary(company_intel, business_model, value_chain)

    analysis_prompt = f"""You are a McKinsey-level organizational consultant performing an Organizational Structure Analysis.

Company: {company_name}
Industry: {industry}

CONTEXT FROM PREVIOUS ANALYSES:
{context_summary}

Analyze this company's organizational structure, leadership, and organizational effectiveness. Provide a comprehensive analysis covering:

## LEADERSHIP TEAM

### Executive Leadership
- CEO and C-Suite composition
- Leadership backgrounds and experience
- Tenure and stability
- Diversity of leadership team
- Leadership style and culture
- Succession planning indicators

### Board of Directors
- Board composition and expertise
- Independent vs insider directors
- Key committees (audit, compensation, etc.)
- Governance quality

### Key Strengths and Concerns
- Leadership team strengths
- Potential gaps or risks
- Cultural indicators

## ORGANIZATIONAL STRUCTURE

### Structure Type
Identify the primary organizational structure:
- Functional (organized by business function)
- Divisional (organized by product/geography)
- Matrix (hybrid functional-divisional)
- Flat/Networked
- Other

### Organizational Chart Analysis
- Number of organizational layers
- Span of control (average reports per manager)
- Reporting relationships
- Centralization vs decentralization
- Geographic distribution

### Departmental Structure
Analyze key departments:
- Sales & Marketing structure
- Product/Engineering structure
- Operations structure
- Finance & Administration
- HR and People Operations
- IT and Technology
- Customer Success/Support

### Strengths and Weaknesses
- What works well in current structure
- Structural inefficiencies or bottlenecks
- Alignment with strategy
- Scalability assessment

## DECISION-MAKING & GOVERNANCE

### Decision-Making Processes
- How are strategic decisions made?
- Delegation of authority
- Speed of decision-making
- Consensus vs command-and-control
- Use of data in decisions

### Communication Patterns
- Top-down vs bottom-up communication
- Cross-functional collaboration
- Information flow effectiveness
- Meeting culture

### Autonomy & Empowerment
- Employee empowerment level
- Innovation encouragement
- Risk tolerance
- Experimentation culture

## ORGANIZATIONAL HEALTH

### Culture & Values
- Stated values and mission
- Cultural strengths
- Cultural challenges
- Values alignment across org

### Employee Experience
- Employee satisfaction indicators
- Retention and turnover
- Career development opportunities
- Work-life balance
- Compensation philosophy

### Talent Management
- Recruitment and hiring approach
- Onboarding processes
- Performance management
- Learning and development
- High-potential talent programs

### Organizational Capabilities
- Core competencies
- Capability gaps
- Knowledge management
- Change readiness

## ORGANIZATIONAL EFFECTIVENESS

### Efficiency Metrics
- Organizational complexity (unnecessary layers)
- Decision velocity
- Bureaucracy level
- Resource allocation efficiency

### Alignment Assessment
- Strategy-structure alignment
- Org structure vs value chain fit
- Cross-functional coordination
- Goal alignment across levels

### Agility & Adaptability
- Response to market changes
- Innovation capability
- Digital maturity
- Change management effectiveness

## GROWTH & SCALING READINESS

### Scalability Analysis
- Can current structure support 2x growth?
- Bottlenecks to scaling
- Infrastructure readiness
- Process maturity

### Future State Recommendations
- Optimal structure for next growth phase
- Key hires needed
- Process improvements required
- Technology enablement needs

## STRATEGIC RECOMMENDATIONS

### Immediate Actions (0-6 months)
List 3-5 quick wins with:
- Specific organizational issue to address
- Recommended action
- Expected impact
- Implementation difficulty

### Medium-term Initiatives (6-18 months)
List 3-5 structural improvements with:
- Area to transform
- Recommended changes
- Benefits
- Change management requirements

### Long-term Transformation (18+ months)
List 2-3 major organizational transformations with:
- Vision for future structure
- Strategic rationale
- Implementation roadmap
- Success metrics

Provide your analysis in valid JSON format with this exact structure:
{{
    "leadership_team": {{
        "executive_leadership": {{
            "ceo": {{"name": "...", "background": "...", "tenure": "..."}},
            "c_suite": [
                {{"title": "...", "name": "...", "background": "...", "tenure": "..."}}
            ],
            "leadership_style": "...",
            "strengths": ["...", "..."],
            "concerns": ["...", "..."]
        }},
        "board_of_directors": {{
            "size": 0,
            "independence": "...",
            "key_expertise": ["...", "..."],
            "governance_quality": "excellent|good|adequate|needs_improvement"
        }}
    }},
    "organizational_structure": {{
        "structure_type": "functional|divisional|matrix|flat|hybrid",
        "structure_description": "...",
        "layers": 0,
        "span_of_control": 0,
        "centralization": "highly_centralized|centralized|balanced|decentralized|highly_decentralized",
        "departments": [
            {{
                "name": "...",
                "size_estimate": "...",
                "structure": "...",
                "key_roles": ["...", "..."]
            }}
        ],
        "strengths": ["...", "..."],
        "weaknesses": ["...", "..."],
        "scalability": "high|medium|low"
    }},
    "decision_making_governance": {{
        "decision_style": "...",
        "decision_speed": "fast|moderate|slow",
        "data_driven": "highly|moderately|minimally",
        "communication_effectiveness": "excellent|good|adequate|poor",
        "collaboration_quality": "excellent|good|adequate|poor",
        "autonomy_level": "high|medium|low"
    }},
    "organizational_health": {{
        "culture": {{
            "stated_values": ["...", "..."],
            "cultural_strengths": ["...", "..."],
            "cultural_challenges": ["...", "..."],
            "culture_rating": "strong|moderate|weak"
        }},
        "employee_experience": {{
            "satisfaction_level": "high|medium|low",
            "retention": "excellent|good|adequate|poor",
            "development_opportunities": "extensive|moderate|limited",
            "work_life_balance": "excellent|good|adequate|poor"
        }},
        "talent_management": {{
            "recruitment_quality": "excellent|good|adequate|poor",
            "development_programs": ["...", "..."],
            "succession_planning": "robust|adequate|weak"
        }},
        "core_capabilities": ["...", "..."],
        "capability_gaps": ["...", "..."]
    }},
    "organizational_effectiveness": {{
        "efficiency": {{
            "complexity_level": "low|medium|high",
            "decision_velocity": "fast|moderate|slow",
            "bureaucracy": "minimal|moderate|excessive"
        }},
        "alignment": {{
            "strategy_structure_fit": "excellent|good|adequate|poor",
            "cross_functional_coordination": "excellent|good|adequate|poor",
            "goal_alignment": "excellent|good|adequate|poor"
        }},
        "agility": {{
            "market_responsiveness": "high|medium|low",
            "innovation_capability": "high|medium|low",
            "digital_maturity": "advanced|developing|nascent",
            "change_readiness": "high|medium|low"
        }}
    }},
    "growth_scaling_readiness": {{
        "current_headcount_estimate": "...",
        "can_support_2x_growth": true,
        "scaling_bottlenecks": ["...", "..."],
        "infrastructure_readiness": "ready|needs_investment|not_ready",
        "key_hires_needed": ["...", "..."]
    }},
    "strategic_recommendations": {{
        "immediate_actions": [
            {{
                "issue": "...",
                "recommendation": "...",
                "expected_impact": "...",
                "difficulty": "low|medium|high"
            }}
        ],
        "medium_term": [...],
        "long_term": [...]
    }},
    "executive_summary": {{
        "overall_assessment": "...",
        "organizational_maturity": "nascent|developing|maturing|mature|optimized",
        "key_strengths": ["...", "..."],
        "critical_issues": ["...", "..."],
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
        return {
            "error": "Failed to parse analysis",
            "raw_response": response_text[:500]
        }
    except Exception as e:
        logger.error(f"Error calling Claude API: {str(e)}")
        raise


def _prepare_context_summary(
    company_intel: Dict[str, Any],
    business_model: Dict[str, Any],
    value_chain: Dict[str, Any]
) -> str:
    """Prepare a concise summary of context from previous analyses."""

    summary_parts = []

    # Company intelligence summary
    if company_intel:
        summary_parts.append("COMPANY INTELLIGENCE:")
        if "business_overview" in company_intel:
            summary_parts.append(f"- Overview: {company_intel['business_overview'][:300]}...")
        if "company_size" in company_intel:
            summary_parts.append(f"- Size: {company_intel['company_size']}")
        if "founding_year" in company_intel:
            summary_parts.append(f"- Founded: {company_intel['founding_year']}")

    # Business model summary
    if business_model:
        summary_parts.append("\nBUSINESS MODEL:")
        if "key_activities" in business_model:
            ka = business_model["key_activities"]
            if isinstance(ka, dict) and "activities" in ka:
                summary_parts.append(f"- Key Activities: {', '.join(ka['activities'][:3])}")

    # Value chain summary
    if value_chain and "executive_summary" in value_chain:
        summary_parts.append("\nVALUE CHAIN INSIGHTS:")
        es = value_chain["executive_summary"]
        if "key_strengths" in es:
            summary_parts.append(f"- Strengths: {', '.join(es['key_strengths'][:3])}")

    return "\n".join(summary_parts) if summary_parts else "Limited context available - performing analysis based on publicly available information."
