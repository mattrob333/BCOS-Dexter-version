"""
Ansoff Matrix Skill

Analyzes growth strategies using the Ansoff Matrix framework:
Market Penetration, Market Development, Product Development, and Diversification.
"""

import json
import logging
from typing import Any, Dict
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SKILL_METADATA = {
    "name": "ansoff_matrix",
    "description": "Growth strategy analysis using Ansoff Matrix",
    "phase": "phase2",
    "dependencies": ["market_intelligence", "business_model_canvas"],
    "outputs": ["ansoff_matrix_analysis"]
}


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute Ansoff Matrix growth strategy analysis.

    Args:
        task: Task object with description and requirements
        context: Execution context with Phase 1 and Phase 2 data
        config: Configuration including company details and API keys

    Returns:
        Dict containing Ansoff Matrix analysis and growth recommendations
    """
    logger.info(f"Executing Ansoff Matrix Analysis: {task.description if hasattr(task, 'description') else 'Ansoff Matrix'}")

    try:
        company_name = config.get("company", {}).get("name", "Unknown Company")
        industry = config.get("company", {}).get("industry", "")

        # Get context from Phase 1
        market_intel = context.get("market_intelligence", {})
        business_model = context.get("business_model_canvas", {})
        company_intel = context.get("company_intelligence", {})

        # Perform Ansoff Matrix analysis
        analysis = _analyze_ansoff_matrix(
            company_name=company_name,
            industry=industry,
            market_intel=market_intel,
            business_model=business_model,
            company_intel=company_intel,
            config=config
        )

        logger.info("Ansoff Matrix analysis completed successfully")
        return {
            "status": "success",
            "data": analysis,
            "metadata": {
                "company": company_name,
                "framework": "Ansoff Matrix",
                "skill": "ansoff_matrix"
            }
        }

    except Exception as e:
        logger.error(f"Error in Ansoff Matrix analysis: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "data": {}
        }


def _analyze_ansoff_matrix(
    company_name: str,
    industry: str,
    market_intel: Dict[str, Any],
    business_model: Dict[str, Any],
    company_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Analyze growth strategies using Ansoff Matrix with Claude."""

    context_summary = _prepare_context_summary(market_intel, business_model, company_intel)

    analysis_prompt = f"""You are a McKinsey-level growth strategist performing an Ansoff Matrix analysis.

Company: {company_name}
Industry: {industry}

CONTEXT FROM PREVIOUS ANALYSES:
{context_summary}

## ANSOFF MATRIX FRAMEWORK

The Ansoff Matrix identifies four growth strategies based on products and markets:

**Axis 1 - Products:** Existing vs New
**Axis 2 - Markets:** Existing vs New

### Four Growth Strategies:

1. **MARKET PENETRATION** (Existing Products, Existing Markets)
   - Increase market share in current markets
   - Lowest risk strategy
   - Tactics: pricing, promotion, distribution, product improvements
   - Goal: Take share from competitors

2. **MARKET DEVELOPMENT** (Existing Products, New Markets)
   - Take existing products to new markets
   - Medium risk strategy
   - New: geographies, segments, channels, use cases
   - Leverage existing product strengths

3. **PRODUCT DEVELOPMENT** (New Products, Existing Markets)
   - Develop new products for current customers
   - Medium risk strategy
   - Innovation, extensions, new categories
   - Leverage customer relationships

4. **DIVERSIFICATION** (New Products, New Markets)
   - Enter completely new territory
   - Highest risk strategy
   - Types: related, unrelated, horizontal, vertical
   - Requires most resources

## YOUR ANALYSIS TASK

Analyze all four growth strategies for {company_name} and provide specific, actionable recommendations:

### 1. MARKET PENETRATION STRATEGIES

Analyze opportunities to grow within existing markets:

**Current Position:**
- Current market share estimate
- Market saturation level
- Competitive intensity
- Growth headroom

**Opportunities:**
- Increase customer usage/purchase frequency
- Win customers from competitors
- Acquire dormant/lost customers
- Increase wallet share
- Optimize pricing strategy
- Enhance distribution
- Strengthen brand positioning

**Specific Tactics:**
- 5-7 concrete initiatives
- Expected impact on market share
- Investment required
- Implementation timeline
- Success metrics

**Risks and Challenges:**
- Competitive response
- Margin pressure
- Market saturation concerns

### 2. MARKET DEVELOPMENT STRATEGIES

Analyze opportunities to enter new markets with existing products:

**New Geographic Markets:**
- Which regions/countries to target
- Market attractiveness analysis
- Entry barriers and requirements
- Localization needs

**New Customer Segments:**
- Untapped segments
- Segment attractiveness
- Product-market fit
- Go-to-market approach

**New Channels:**
- Direct vs indirect
- Online vs offline
- Partnership opportunities
- Channel economics

**New Use Cases:**
- Alternative applications
- Adjacent problems to solve
- Customer jobs to be done

**Specific Tactics:**
- 5-7 concrete market development initiatives
- Market entry strategy for each
- Expected revenue potential
- Investment required
- Timeline and milestones
- Success metrics

**Risks and Challenges:**
- Market entry barriers
- Cultural/regulatory challenges
- Resource constraints

### 3. PRODUCT DEVELOPMENT STRATEGIES

Analyze opportunities to develop new products for existing customers:

**Innovation Opportunities:**
- Product line extensions
- Next-generation products
- Complementary products
- New product categories
- Platform/ecosystem expansion

**Customer Needs Analysis:**
- Unmet needs in customer base
- Pain points to address
- Jobs to be done
- Feature requests and feedback

**R&D Priorities:**
- Technology investments needed
- Build vs buy vs partner
- IP considerations
- Time to market

**Specific Tactics:**
- 5-7 product development initiatives
- Product vision for each
- Target customer segment
- Differentiation vs existing products
- Development timeline
- Launch strategy
- Revenue projections

**Risks and Challenges:**
- R&D execution risk
- Cannibalization of existing products
- Time and cost overruns
- Market acceptance

### 4. DIVERSIFICATION STRATEGIES

Analyze opportunities for entering new markets with new products:

**Related Diversification:**
- Adjacent markets/products
- Synergies with core business
- Competitive advantages that transfer
- Value chain integration opportunities

**Unrelated Diversification:**
- Completely new markets
- Portfolio diversification rationale
- Risk spreading benefits
- Strategic logic

**Specific Tactics:**
- 3-5 diversification opportunities
- Strategic rationale for each
- Synergies with core business
- Entry mode (organic, M&A, partnership)
- Investment required
- Timeline to profitability
- Success criteria

**Risks and Challenges:**
- Highest risk strategy
- Resource dilution
- Management complexity
- Market/product uncertainty

### 5. PORTFOLIO STRATEGY & PRIORITIZATION

**Recommended Growth Portfolio:**
- Allocation across four strategies (%)
- Risk-return profile
- Resource allocation
- Sequencing and dependencies

**Prioritized Growth Initiatives:**
Rank top 10 growth initiatives across all four quadrants:
- Initiative description
- Ansoff quadrant
- Expected revenue impact (3 years)
- Investment required
- Risk level
- Priority score
- Timeline

**Strategic Roadmap:**
- Year 1 focus
- Year 2-3 expansion
- 3-5 year vision

Provide your analysis in valid JSON format with this exact structure:
{{
    "market_penetration": {{
        "current_position": {{
            "market_share_estimate": "...",
            "market_saturation": "low|medium|high",
            "growth_headroom": "significant|moderate|limited"
        }},
        "opportunities": [
            {{
                "tactic": "...",
                "description": "...",
                "expected_impact": "...",
                "investment_required": "...",
                "timeline": "...",
                "difficulty": "low|medium|high"
            }}
        ],
        "risks": ["...", "..."]
    }},
    "market_development": {{
        "new_geographies": [
            {{
                "market": "...",
                "attractiveness": "high|medium|low",
                "entry_strategy": "...",
                "barriers": ["...", "..."],
                "revenue_potential": "..."
            }}
        ],
        "new_segments": [...],
        "new_channels": [...],
        "new_use_cases": [...],
        "opportunities": [...],
        "risks": ["...", "..."]
    }},
    "product_development": {{
        "innovation_opportunities": [
            {{
                "product_concept": "...",
                "description": "...",
                "target_segment": "...",
                "differentiation": "...",
                "development_timeline": "...",
                "revenue_potential": "..."
            }}
        ],
        "customer_needs": ["...", "..."],
        "rd_priorities": ["...", "..."],
        "opportunities": [...],
        "risks": ["...", "..."]
    }},
    "diversification": {{
        "related_opportunities": [
            {{
                "opportunity": "...",
                "description": "...",
                "synergies": ["...", "..."],
                "entry_mode": "organic|acquisition|partnership",
                "investment": "...",
                "timeline": "..."
            }}
        ],
        "unrelated_opportunities": [...],
        "opportunities": [...],
        "risks": ["...", "..."]
    }},
    "portfolio_strategy": {{
        "recommended_allocation": {{
            "market_penetration_pct": 40,
            "market_development_pct": 30,
            "product_development_pct": 20,
            "diversification_pct": 10
        }},
        "risk_return_profile": "conservative|balanced|aggressive",
        "resource_requirements": "..."
    }},
    "prioritized_initiatives": [
        {{
            "rank": 1,
            "initiative": "...",
            "quadrant": "market_penetration|market_development|product_development|diversification",
            "revenue_impact_3yr": "...",
            "investment_required": "...",
            "risk_level": "low|medium|high",
            "timeline": "...",
            "priority_score": 9.5
        }}
    ],
    "strategic_roadmap": {{
        "year_1": {{
            "focus": "...",
            "key_initiatives": ["...", "..."],
            "targets": "..."
        }},
        "year_2_3": {{...}},
        "year_3_5": {{...}}
    }},
    "executive_summary": {{
        "recommended_strategy": "...",
        "growth_potential": "...",
        "key_opportunities": ["...", "..."],
        "critical_risks": ["...", "..."],
        "investment_required": "...",
        "expected_outcomes": "..."
    }}
}}"""

    # Call Claude API
    try:
        client = Anthropic(api_key=config.get("llm", {}).get("api_key"))

        response = client.messages.create(
            model=config.get("llm", {}).get("model", "claude-3-5-sonnet-20241022"),
            max_tokens=16000,
            temperature=0.7,
            messages=[{"role": "user", "content": analysis_prompt}]
        )

        response_text = response.content[0].text

        # Extract JSON
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
    market_intel: Dict[str, Any],
    business_model: Dict[str, Any],
    company_intel: Dict[str, Any]
) -> str:
    """Prepare context summary."""
    summary_parts = []

    if market_intel:
        summary_parts.append("MARKET INTELLIGENCE:")
        if "market_size" in market_intel:
            summary_parts.append(f"- Market Size: {market_intel['market_size']}")
        if "growth_rate" in market_intel:
            summary_parts.append(f"- Growth Rate: {market_intel['growth_rate']}")

    if company_intel:
        if "products_services" in company_intel:
            summary_parts.append(f"\nCurrent Products: {', '.join(company_intel['products_services'][:5])}")

    return "\n".join(summary_parts) if summary_parts else "Limited context available."
