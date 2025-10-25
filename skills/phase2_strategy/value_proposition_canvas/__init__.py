"""
Value Proposition Canvas Skill

Analyzes product-market fit using the Value Proposition Canvas framework.
Maps customer jobs, pains, and gains against the company's value proposition.
"""

import json
import logging
from typing import Any, Dict
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SKILL_METADATA = {
    "name": "value_proposition_canvas",
    "description": "Product-market fit analysis using Value Proposition Canvas",
    "phase": "phase2",
    "dependencies": ["business_model_canvas", "company_intelligence"],
    "outputs": ["value_proposition_analysis"]
}


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute Value Proposition Canvas analysis."""
    logger.info(f"Executing Value Proposition Canvas: {task.description if hasattr(task, 'description') else 'VPC Analysis'}")

    try:
        company_name = config.get("company", {}).get("name", "Unknown Company")

        business_model = context.get("business_model_canvas", {})
        company_intel = context.get("company_intelligence", {})
        market_intel = context.get("market_intelligence", {})

        analysis = _analyze_value_proposition(
            company_name=company_name,
            business_model=business_model,
            company_intel=company_intel,
            market_intel=market_intel,
            config=config
        )

        logger.info("Value Proposition Canvas analysis completed")
        return {
            "status": "success",
            "data": analysis,
            "metadata": {
                "company": company_name,
                "framework": "Value Proposition Canvas",
                "skill": "value_proposition_canvas"
            }
        }

    except Exception as e:
        logger.error(f"Error in VPC analysis: {str(e)}")
        return {"status": "error", "error": str(e), "data": {}}


def _analyze_value_proposition(
    company_name: str,
    business_model: Dict[str, Any],
    company_intel: Dict[str, Any],
    market_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Analyze value proposition using Claude."""

    context_summary = _prepare_context_summary(business_model, company_intel, market_intel)

    analysis_prompt = f"""You are a product strategy expert performing a Value Proposition Canvas analysis.

Company: {company_name}

CONTEXT:
{context_summary}

## VALUE PROPOSITION CANVAS FRAMEWORK

The VPC has two sides that must fit together:

### CUSTOMER PROFILE (Right side)

**Customer Jobs:**
- Functional jobs (tasks to complete)
- Social jobs (how they want to be perceived)
- Emotional jobs (how they want to feel)
- Supporting jobs (buying, maintaining, disposal)

**Pains:**
- Obstacles preventing job completion
- Risks and negative outcomes
- Problems with current solutions
- Barriers and friction points

**Gains:**
- Required outcomes for success
- Expected benefits
- Desires and aspirations
- Positive surprises

### VALUE MAP (Left side)

**Products & Services:**
- What you offer
- Features and capabilities
- Physical, digital, services

**Pain Relievers:**
- How you eliminate/reduce customer pains
- Obstacles removed
- Risks minimized
- Better than alternatives

**Gain Creators:**
- How you create customer gains
- Required benefits delivered
- Expectations exceeded
- Positive outcomes produced

## YOUR TASK

For {company_name}, analyze 2-3 key customer segments and create detailed Value Proposition Canvases:

### For Each Customer Segment:

**1. CUSTOMER PROFILE**

**Customer Jobs:**
- List 5-7 functional jobs
- List 2-3 social jobs
- List 2-3 emotional jobs
- Rank by importance

**Customer Pains:**
- List 5-7 key pains
- Categorize severity (extreme, moderate, mild)
- Rank by frequency/impact

**Customer Gains:**
- List 5-7 desired gains
- Differentiate required vs nice-to-have
- Rank by importance

**2. VALUE MAP**

**Products & Services:**
- List all relevant offerings for this segment
- Key features and capabilities

**Pain Relievers:**
- How each product addresses each pain
- Effectiveness rating (high/medium/low)
- Evidence of pain relief

**Gain Creators:**
- How each product creates each gain
- Magnitude of gain (high/medium/low)
- Evidence of gain creation

**3. FIT ANALYSIS**

**Product-Market Fit Assessment:**
- Overall fit score (0-10)
- Which pains are addressed (%)
- Which gains are delivered (%)
- Gaps and mismatches

**Competitive Comparison:**
- How competitors address same jobs/pains/gains
- Your unique advantages
- Areas where competitors are stronger

**Evidence of Fit:**
- Customer testimonials/quotes
- Usage metrics
- Retention/satisfaction data
- Win/loss patterns

**4. RECOMMENDATIONS**

**Product Improvements:**
- Pain relievers to strengthen
- Gain creators to add
- Features to prioritize

**Messaging Improvements:**
- How to better communicate value
- Pain points to emphasize
- Gains to highlight

**Segment Targeting:**
- Which segments show best fit
- Which to prioritize
- Which may not be worth pursuing

Provide analysis in valid JSON:
{{
    "customer_segments": [
        {{
            "segment_name": "...",
            "segment_description": "...",
            "segment_size": "...",
            "customer_profile": {{
                "customer_jobs": [
                    {{
                        "job": "...",
                        "type": "functional|social|emotional|supporting",
                        "importance": "critical|high|medium|low"
                    }}
                ],
                "pains": [
                    {{
                        "pain": "...",
                        "severity": "extreme|moderate|mild",
                        "frequency": "always|often|sometimes|rarely",
                        "importance": "critical|high|medium|low"
                    }}
                ],
                "gains": [
                    {{
                        "gain": "...",
                        "type": "required|expected|desired|unexpected",
                        "importance": "critical|high|medium|low"
                    }}
                ]
            }},
            "value_map": {{
                "products_services": [
                    {{
                        "name": "...",
                        "description": "...",
                        "key_features": ["...", "..."]
                    }}
                ],
                "pain_relievers": [
                    {{
                        "reliever": "...",
                        "addresses_pain": "...",
                        "effectiveness": "high|medium|low",
                        "evidence": "..."
                    }}
                ],
                "gain_creators": [
                    {{
                        "creator": "...",
                        "creates_gain": "...",
                        "magnitude": "high|medium|low",
                        "evidence": "..."
                    }}
                ]
            }},
            "fit_analysis": {{
                "overall_fit_score": 8.5,
                "pains_addressed_pct": 85,
                "gains_delivered_pct": 75,
                "fit_assessment": "excellent|strong|moderate|weak|poor",
                "gaps": ["...", "..."],
                "competitive_position": "stronger|comparable|weaker",
                "evidence": ["...", "..."]
            }},
            "recommendations": {{
                "product_improvements": ["...", "..."],
                "messaging_improvements": ["...", "..."],
                "priority": "high|medium|low"
            }}
        }}
    ],
    "cross_segment_insights": {{
        "common_jobs": ["...", "..."],
        "common_pains": ["...", "..."],
        "common_gains": ["...", "..."],
        "segment_prioritization": [
            {{
                "segment": "...",
                "fit_score": 9.0,
                "opportunity_size": "large|medium|small",
                "priority": 1
            }}
        ]
    }},
    "strategic_recommendations": {{
        "product_roadmap": [
            {{
                "initiative": "...",
                "addresses": "...",
                "priority": "p0|p1|p2",
                "impact": "high|medium|low"
            }}
        ],
        "messaging_strategy": {{
            "core_message": "...",
            "key_pain_points_to_emphasize": ["...", "..."],
            "key_gains_to_highlight": ["...", "..."]
        }},
        "segment_strategy": {{
            "primary_segment": "...",
            "secondary_segments": ["...", "..."],
            "segments_to_avoid": ["...", "..."]
        }}
    }},
    "executive_summary": {{
        "overall_value_prop_strength": "excellent|strong|moderate|weak",
        "best_fit_segment": "...",
        "key_differentiators": ["...", "..."],
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
    business_model: Dict[str, Any],
    company_intel: Dict[str, Any],
    market_intel: Dict[str, Any]
) -> str:
    """Prepare context summary."""
    summary_parts = []

    if business_model:
        if "customer_segments" in business_model:
            summary_parts.append(f"Customer Segments: {business_model['customer_segments']}")
        if "value_propositions" in business_model:
            summary_parts.append(f"Value Props: {business_model['value_propositions']}")

    if company_intel:
        if "products_services" in company_intel:
            summary_parts.append(f"Products: {', '.join(company_intel['products_services'][:5])}")

    return "\n".join(summary_parts) if summary_parts else "Limited context."
