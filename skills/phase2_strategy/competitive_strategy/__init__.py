"""
Competitive Strategy Skill

Analyzes competitive positioning, differentiation strategies, and sustainable
competitive advantages (economic moats).
"""

import json
import logging
from typing import Any, Dict
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SKILL_METADATA = {
    "name": "competitive_strategy",
    "description": "Analyze competitive positioning and sustainable advantages",
    "phase": "phase2",
    "dependencies": ["competitor_intelligence", "porters_five_forces"],
    "outputs": ["competitive_strategy_analysis"]
}


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute competitive strategy analysis."""
    logger.info(f"Executing Competitive Strategy Analysis: {task.description if hasattr(task, 'description') else 'Competitive Strategy'}")

    try:
        company_name = config.get("company", {}).get("name", "Unknown Company")
        industry = config.get("company", {}).get("industry", "")

        competitor_intel = context.get("competitor_intelligence", {})
        porters = context.get("porters_five_forces_analysis", {})
        swot = context.get("swot_analysis", {})
        value_chain = context.get("value_chain_analysis", {})

        analysis = _analyze_competitive_strategy(
            company_name=company_name,
            industry=industry,
            competitor_intel=competitor_intel,
            porters=porters,
            swot=swot,
            value_chain=value_chain,
            config=config
        )

        logger.info("Competitive strategy analysis completed")
        return {
            "status": "success",
            "data": analysis,
            "metadata": {
                "company": company_name,
                "analysis_type": "Competitive Strategy",
                "skill": "competitive_strategy"
            }
        }

    except Exception as e:
        logger.error(f"Error in competitive strategy analysis: {str(e)}")
        return {"status": "error", "error": str(e), "data": {}}


def _analyze_competitive_strategy(
    company_name: str,
    industry: str,
    competitor_intel: Dict[str, Any],
    porters: Dict[str, Any],
    swot: Dict[str, Any],
    value_chain: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Analyze competitive strategy using Claude."""

    context_summary = _prepare_context_summary(competitor_intel, porters, swot, value_chain)

    analysis_prompt = f"""You are a competitive strategy expert developing a comprehensive competitive strategy.

Company: {company_name}
Industry: {industry}

CONTEXT:
{context_summary}

## YOUR TASK

Develop a comprehensive competitive strategy covering positioning, differentiation, and sustainable competitive advantages.

### 1. COMPETITIVE POSITIONING

**Current Position:**
- Market position (leader, challenger, follower, nicher)
- Market share estimate
- Position vs key competitors
- Positioning statement

**Generic Strategy** (Porter):
- Which strategy: Cost Leadership, Differentiation, or Focus (niche)
- Evidence of strategy execution
- Consistency of strategy
- Effectiveness vs competitors

**Strategic Group Analysis:**
- Identify 3-5 strategic groups in the industry
- Positioning of company within groups
- Mobility barriers between groups
- Most attractive group

**Positioning Assessment:**
- Clarity of positioning
- Differentiation strength
- Consistency with capabilities
- Market perception

### 2. DIFFERENTIATION STRATEGY

**Sources of Differentiation:**

Analyze differentiation across all value chain activities:

**Product Differentiation:**
- Features and functionality
- Quality and reliability
- Design and aesthetics
- Customization
- Innovation

**Service Differentiation:**
- Customer service quality
- Support and training
- Responsiveness
- Expertise

**Brand Differentiation:**
- Brand strength and recognition
- Brand associations
- Brand trust and reputation
- Emotional connection

**Channel Differentiation:**
- Distribution access
- Channel relationships
- Channel service levels

**People Differentiation:**
- Employee quality and expertise
- Culture and values
- Customer relationships

**Differentiation Assessment:**
- Most powerful differentiators
- Sustainability of differentiation
- Value to customers
- Cost of differentiation
- Competitive gaps

### 3. COMPETITIVE ADVANTAGES (MOATS)

Analyze sustainable competitive advantages using moat framework:

**Network Effects:**
- Is there a network effect?
- Type (direct, indirect, platform)
- Strength and defensibility
- Growth trajectory

**Switching Costs:**
- Customer switching costs
- Types (financial, procedural, relational, risk)
- Magnitude and impact
- Lock-in mechanisms

**Cost Advantages:**
- Economies of scale
- Proprietary technology
- Preferential access to resources
- Process advantages
- Location advantages

**Intangible Assets:**
- Brand strength
- Patents and IP
- Regulatory licenses
- Data and algorithms
- Trade secrets

**Moat Assessment:**
- Overall moat width (none|narrow|medium|wide)
- Moat sustainability
- Moat expansion opportunities
- Competitive threats to moat

### 4. COMPETITIVE DYNAMICS

**Competitive Moves:**
- Recent competitive actions
- Likely competitor responses to your moves
- Emerging competitive threats
- Competitive signaling

**Competitive Scenarios:**
Create 2-3 scenarios for competitive evolution:
- Optimistic scenario
- Most likely scenario
- Challenging scenario

For each:
- Key developments
- Competitive landscape
- Strategic implications
- Recommended responses

### 5. STRATEGIC OPTIONS ANALYSIS

Evaluate strategic options:

**Option 1: Strengthen Current Position**
- Double down on existing strategy
- Deepen moats
- Extend advantages
- Pros and cons
- Resource requirements

**Option 2: Reposition**
- Change competitive positioning
- Target different segment/needs
- Shift generic strategy
- Pros and cons
- Risks and requirements

**Option 3: Disrupt**
- Change the basis of competition
- New business model
- Technology disruption
- Pros and cons
- Investment and timeline

**Option 4: Collaborate**
- Partnerships and alliances
- Ecosystem play
- Coopetition
- Pros and cons
- Partner requirements

### 6. RECOMMENDED COMPETITIVE STRATEGY

**Strategic Choice:**
- Primary strategic option
- Rationale
- Expected outcomes

**Positioning Strategy:**
- Target positioning
- Key messages
- Differentiation focus

**Competitive Moves:**
- Immediate actions (0-6 months)
- Medium-term initiatives (6-18 months)
- Long-term strategic shifts (18+ months)

**Defensive Strategies:**
- Moat strengthening
- Competitive responses
- Disruption mitigation

**Offensive Strategies:**
- Share gain tactics
- Competitive disruption
- Market expansion

**Resource Allocation:**
- Investment priorities
- Capability building
- M&A targets

Provide analysis in valid JSON:
{{
    "competitive_positioning": {{
        "current_position": "leader|strong_challenger|challenger|follower|nicher",
        "market_share_estimate": "...",
        "generic_strategy": "cost_leadership|differentiation|focus_cost|focus_differentiation",
        "strategic_group": "...",
        "positioning_strength": "strong|moderate|weak",
        "positioning_statement": "..."
    }},
    "differentiation_strategy": {{
        "primary_differentiators": [
            {{
                "differentiator": "...",
                "category": "product|service|brand|channel|people",
                "strength": "strong|moderate|weak",
                "sustainability": "high|medium|low",
                "value_to_customer": "high|medium|low"
            }}
        ],
        "differentiation_gaps": ["...", "..."],
        "differentiation_opportunities": ["...", "..."]
    }},
    "competitive_advantages": {{
        "moats": [
            {{
                "type": "network_effects|switching_costs|cost_advantages|intangible_assets",
                "description": "...",
                "strength": "strong|moderate|weak",
                "sustainability": "durable|moderate|fragile",
                "evidence": "..."
            }}
        ],
        "overall_moat_width": "none|narrow|medium|wide",
        "moat_trends": "widening|stable|narrowing",
        "threats_to_moat": ["...", "..."]
    }},
    "competitive_dynamics": {{
        "recent_competitive_moves": ["...", "..."],
        "emerging_threats": ["...", "..."],
        "scenarios": [
            {{
                "name": "optimistic|likely|challenging",
                "description": "...",
                "probability": "high|medium|low",
                "implications": ["...", "..."],
                "recommended_response": "..."
            }}
        ]
    }},
    "strategic_options": [
        {{
            "option": "strengthen|reposition|disrupt|collaborate",
            "description": "...",
            "pros": ["...", "..."],
            "cons": ["...", "..."],
            "resource_requirements": "...",
            "risk_level": "low|medium|high",
            "potential_impact": "transformational|significant|moderate|incremental"
        }}
    ],
    "recommended_strategy": {{
        "strategic_choice": "...",
        "rationale": "...",
        "target_positioning": "...",
        "key_differentiation": ["...", "..."],
        "competitive_moves": {{
            "immediate": ["...", "..."],
            "medium_term": ["...", "..."],
            "long_term": ["...", "..."]
        }},
        "defensive_priorities": ["...", "..."],
        "offensive_priorities": ["...", "..."],
        "investment_priorities": [
            {{
                "priority": "...",
                "investment": "...",
                "expected_impact": "..."
            }}
        ]
    }},
    "executive_summary": {{
        "competitive_position": "strong|moderate|weak|vulnerable",
        "moat_quality": "excellent|good|adequate|weak|none",
        "key_advantages": ["...", "..."],
        "critical_vulnerabilities": ["...", "..."],
        "strategic_imperative": "...",
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
    competitor_intel: Dict[str, Any],
    porters: Dict[str, Any],
    swot: Dict[str, Any],
    value_chain: Dict[str, Any]
) -> str:
    """Prepare context summary."""
    return "See previous analyses: Competitor Intelligence, Porter's Five Forces, SWOT, Value Chain"
