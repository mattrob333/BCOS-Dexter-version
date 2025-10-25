"""
McKinsey 7S Framework Skill

Analyzes organizational effectiveness using the McKinsey 7S model:
Strategy, Structure, Systems, Shared Values, Style, Staff, Skills.
"""

import json
import logging
from typing import Any, Dict
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SKILL_METADATA = {
    "name": "mckinsey_7s",
    "description": "Organizational effectiveness using McKinsey 7S Framework",
    "phase": "phase2",
    "dependencies": ["org_structure_analysis", "company_intelligence"],
    "outputs": ["mckinsey_7s_analysis"]
}


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute McKinsey 7S Framework analysis."""
    logger.info(f"Executing McKinsey 7S Analysis: {task.description if hasattr(task, 'description') else '7S Analysis'}")

    try:
        company_name = config.get("company", {}).get("name", "Unknown Company")

        org_structure = context.get("org_structure_analysis", {})
        company_intel = context.get("company_intelligence", {})
        value_chain = context.get("value_chain_analysis", {})

        analysis = _analyze_7s_framework(
            company_name=company_name,
            org_structure=org_structure,
            company_intel=company_intel,
            value_chain=value_chain,
            config=config
        )

        logger.info("McKinsey 7S analysis completed")
        return {
            "status": "success",
            "data": analysis,
            "metadata": {
                "company": company_name,
                "framework": "McKinsey 7S",
                "skill": "mckinsey_7s"
            }
        }

    except Exception as e:
        logger.error(f"Error in 7S analysis: {str(e)}")
        return {"status": "error", "error": str(e), "data": {}}


def _analyze_7s_framework(
    company_name: str,
    org_structure: Dict[str, Any],
    company_intel: Dict[str, Any],
    value_chain: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Analyze organization using McKinsey 7S with Claude."""

    context_summary = _prepare_context_summary(org_structure, company_intel, value_chain)

    analysis_prompt = f"""You are a McKinsey organizational consultant performing a 7S Framework analysis.

Company: {company_name}

CONTEXT:
{context_summary}

## MCKINSEY 7S FRAMEWORK

The 7S model analyzes organizational effectiveness through seven interconnected elements:

**HARD ELEMENTS** (easier to define and change):
1. Strategy
2. Structure
3. Systems

**SOFT ELEMENTS** (harder to define, culturally rooted):
4. Shared Values (culture)
5. Style (leadership approach)
6. Staff (people)
7. Skills (capabilities)

All seven elements must be aligned for organizational effectiveness.

## YOUR ANALYSIS TASK

Analyze {company_name} across all 7 elements and their alignment:

### 1. STRATEGY

**Current Strategy:**
- Strategic direction and priorities
- Competitive positioning
- Value creation model
- Strategic goals
- Resource allocation priorities

**Strategy Assessment:**
- Clarity and coherence
- Differentiation strength
- Execution feasibility
- Stakeholder buy-in
- Rating: excellent|good|adequate|needs_work|unclear

**Strategic Gaps:**
- Unaddressed opportunities
- Competitive vulnerabilities
- Strategic inconsistencies

### 2. STRUCTURE

**Organizational Structure:**
- Structure type (functional, divisional, matrix, etc.)
- Reporting relationships
- Decision-making authority
- Spans of control
- Geographic/functional organization

**Structure Assessment:**
- Fit with strategy
- Efficiency and agility
- Clarity of roles and responsibilities
- Scalability
- Rating: excellent|good|adequate|needs_work|problematic

**Structural Issues:**
- Bottlenecks
- Silos and coordination problems
- Unclear accountabilities

### 3. SYSTEMS

**Key Systems:**
- Planning and budgeting
- Performance management
- Information systems
- Communication systems
- HR systems (recruiting, development, compensation)
- Customer relationship systems
- Quality/compliance systems

**Systems Assessment:**
- Effectiveness and efficiency
- Integration across systems
- Technology enablement
- Process maturity
- Rating: excellent|good|adequate|needs_work|inadequate

**System Gaps:**
- Missing critical systems
- Outdated or ineffective systems
- Integration issues

### 4. SHARED VALUES (Culture)

**Core Values:**
- Stated mission, vision, values
- Actual cultural norms and behaviors
- What's truly valued and rewarded

**Cultural Characteristics:**
- Innovation vs risk aversion
- Collaboration vs competition
- Customer vs internal focus
- Results vs process orientation
- Transparency vs hierarchy

**Culture Assessment:**
- Values clarity and communication
- Walk the talk (stated vs lived values)
- Cultural strengths
- Cultural weaknesses
- Rating: strong|moderate|weak|misaligned

**Cultural Issues:**
- Values conflicts
- Subculture fragmentation
- Culture-strategy misalignment

### 5. STYLE (Leadership)

**Leadership Style:**
- Management approach (directive, participative, coaching)
- Decision-making style
- Communication patterns
- Conflict resolution approach
- Change management approach

**Leadership Behaviors:**
- How leaders spend time
- What gets attention and recognition
- Symbolic actions
- Crisis response

**Style Assessment:**
- Fit with strategy and culture
- Consistency across leadership team
- Effectiveness
- Rating: excellent|good|adequate|needs_work|problematic

**Style Issues:**
- Inconsistent leadership
- Style-strategy misfit
- Leadership gaps

### 6. STAFF

**People Profile:**
- Headcount and growth
- Demographics and diversity
- Talent quality and depth
- Key roles and people
- Recruitment and retention

**People Capabilities:**
- Skill levels
- Experience and expertise
- Bench strength
- High-potential talent

**Staff Assessment:**
- Right people in right roles
- Talent gaps
- Retention of key people
- Development opportunities
- Rating: excellent|good|adequate|needs_work|critical

**Staffing Issues:**
- Key talent gaps
- Retention challenges
- Capability shortfalls

### 7. SKILLS (Organizational Capabilities)

**Core Capabilities:**
- Technical skills
- Functional expertise
- Cross-functional capabilities
- Innovation capability
- Execution excellence

**Distinctive Competencies:**
- What does the org do world-class
- Capabilities that create competitive advantage
- Capabilities that are hard to replicate

**Skills Assessment:**
- Alignment with strategy
- Capability maturity
- Gaps vs competitors
- Development investments
- Rating: excellent|good|adequate|needs_work|inadequate

**Skills Gaps:**
- Critical missing capabilities
- Underdeveloped skills
- Capability development needs

### 8. ALIGNMENT ANALYSIS

**Cross-Element Alignment:**

Analyze alignment between each pair of elements:
- Strategy ↔ Structure
- Strategy ↔ Systems
- Strategy ↔ Shared Values
- Structure ↔ Systems
- Style ↔ Shared Values
- Staff ↔ Skills
- All elements ↔ Shared Values (center)

For each relationship:
- Alignment level: strong|moderate|weak|misaligned
- Key synergies or conflicts
- Impact on effectiveness

**Overall Alignment:**
- Overall alignment score (0-10)
- Most aligned elements
- Most misaligned elements
- Organizational effectiveness impact

### 9. RECOMMENDATIONS

**Quick Wins (0-6 months):**
- Specific improvements to each S
- Alignment improvements
- Priority order

**Medium-term (6-18 months):**
- Strategic initiatives
- Organizational changes
- Capability building

**Long-term (18+ months):**
- Transformational changes
- Major realignments
- Strategic shifts

Provide analysis in valid JSON:
{{
    "seven_s_analysis": {{
        "strategy": {{
            "current_strategy": "...",
            "key_priorities": ["...", "..."],
            "assessment": {{
                "rating": "excellent|good|adequate|needs_work|unclear",
                "strengths": ["...", "..."],
                "gaps": ["...", "..."]
            }}
        }},
        "structure": {{
            "structure_type": "...",
            "key_characteristics": ["...", "..."],
            "assessment": {{
                "rating": "excellent|good|adequate|needs_work|problematic",
                "strengths": ["...", "..."],
                "issues": ["...", "..."]
            }}
        }},
        "systems": {{
            "key_systems": [
                {{
                    "system": "...",
                    "effectiveness": "high|medium|low",
                    "description": "..."
                }}
            ],
            "assessment": {{
                "rating": "excellent|good|adequate|needs_work|inadequate",
                "strengths": ["...", "..."],
                "gaps": ["...", "..."]
            }}
        }},
        "shared_values": {{
            "stated_values": ["...", "..."],
            "lived_values": ["...", "..."],
            "cultural_characteristics": {{
                "innovation_orientation": "high|medium|low",
                "collaboration": "high|medium|low",
                "customer_focus": "high|medium|low"
            }},
            "assessment": {{
                "rating": "strong|moderate|weak|misaligned",
                "strengths": ["...", "..."],
                "issues": ["...", "..."]
            }}
        }},
        "style": {{
            "leadership_style": "...",
            "key_behaviors": ["...", "..."],
            "assessment": {{
                "rating": "excellent|good|adequate|needs_work|problematic",
                "strengths": ["...", "..."],
                "issues": ["...", "..."]
            }}
        }},
        "staff": {{
            "headcount": "...",
            "talent_quality": "excellent|good|adequate|needs_work|critical",
            "key_capabilities": ["...", "..."],
            "assessment": {{
                "rating": "excellent|good|adequate|needs_work|critical",
                "strengths": ["...", "..."],
                "gaps": ["...", "..."]
            }}
        }},
        "skills": {{
            "core_capabilities": ["...", "..."],
            "distinctive_competencies": ["...", "..."],
            "assessment": {{
                "rating": "excellent|good|adequate|needs_work|inadequate",
                "strengths": ["...", "..."],
                "gaps": ["...", "..."]
            }}
        }}
    }},
    "alignment_analysis": {{
        "pairwise_alignment": [
            {{
                "elements": ["strategy", "structure"],
                "alignment": "strong|moderate|weak|misaligned",
                "analysis": "...",
                "impact": "high|medium|low"
            }}
        ],
        "overall_alignment_score": 7.5,
        "most_aligned": ["...", "..."],
        "most_misaligned": ["...", "..."],
        "effectiveness_impact": "..."
    }},
    "strategic_recommendations": {{
        "quick_wins": [
            {{
                "element": "...",
                "action": "...",
                "impact": "...",
                "difficulty": "low|medium|high"
            }}
        ],
        "medium_term": [...],
        "long_term": [...]
    }},
    "executive_summary": {{
        "organizational_effectiveness": "high|medium|low",
        "overall_alignment": "strong|moderate|weak",
        "key_strengths": ["...", "..."],
        "critical_gaps": ["...", "..."],
        "top_priorities": ["...", "..."]
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
    org_structure: Dict[str, Any],
    company_intel: Dict[str, Any],
    value_chain: Dict[str, Any]
) -> str:
    """Prepare context summary."""
    summary_parts = []

    if org_structure:
        if "organizational_structure" in org_structure:
            summary_parts.append(f"Structure: {org_structure['organizational_structure']}")

    if company_intel:
        if "business_overview" in company_intel:
            summary_parts.append(f"Overview: {company_intel['business_overview'][:200]}...")

    return "\n".join(summary_parts) if summary_parts else "Limited context."
