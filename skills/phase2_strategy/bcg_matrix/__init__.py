"""
BCG Matrix (Growth-Share Matrix) Skill

Analyzes company's product/business portfolio using Boston Consulting Group's
Growth-Share Matrix framework (Stars, Cash Cows, Question Marks, Dogs).
"""

import json
import logging
from typing import Any, Dict
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SKILL_METADATA = {
    "name": "bcg_matrix",
    "description": "Portfolio analysis using BCG Growth-Share Matrix",
    "phase": "phase2",
    "dependencies": ["company_intelligence", "business_model_canvas", "market_intelligence"],
    "outputs": ["bcg_matrix_analysis"]
}


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute BCG Matrix portfolio analysis.

    Analyzes product/business unit portfolio using the BCG Growth-Share Matrix.

    Args:
        task: Task object with description and requirements
        context: Execution context with Phase 1 and Phase 2 data
        config: Configuration including company details and API keys

    Returns:
        Dict containing BCG Matrix analysis and strategic recommendations
    """
    logger.info(f"Executing BCG Matrix Analysis: {task.description if hasattr(task, 'description') else 'BCG Matrix'}")

    try:
        company_name = config.get("company", {}).get("name", "Unknown Company")
        industry = config.get("company", {}).get("industry", "")

        # Get context from Phase 1
        company_intel = context.get("company_intelligence", {})
        business_model = context.get("business_model_canvas", {})
        market_intel = context.get("market_intelligence", {})

        # Perform BCG Matrix analysis
        analysis = _analyze_bcg_matrix(
            company_name=company_name,
            industry=industry,
            company_intel=company_intel,
            business_model=business_model,
            market_intel=market_intel,
            config=config
        )

        logger.info("BCG Matrix analysis completed successfully")
        return {
            "status": "success",
            "data": analysis,
            "metadata": {
                "company": company_name,
                "framework": "BCG Growth-Share Matrix",
                "skill": "bcg_matrix"
            }
        }

    except Exception as e:
        logger.error(f"Error in BCG Matrix analysis: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "data": {}
        }


def _analyze_bcg_matrix(
    company_name: str,
    industry: str,
    company_intel: Dict[str, Any],
    business_model: Dict[str, Any],
    market_intel: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze portfolio using BCG Matrix with Claude.

    Args:
        company_name: Company name
        industry: Industry sector
        company_intel: Company intelligence from Phase 1
        business_model: Business model canvas from Phase 1
        market_intel: Market intelligence from Phase 1
        config: Configuration with API keys

    Returns:
        BCG Matrix analysis with portfolio recommendations
    """

    # Prepare context
    context_summary = _prepare_context_summary(company_intel, business_model, market_intel)

    analysis_prompt = f"""You are a McKinsey-level strategy consultant performing a BCG Growth-Share Matrix analysis.

Company: {company_name}
Industry: {industry}

CONTEXT FROM PREVIOUS ANALYSES:
{context_summary}

## BCG MATRIX FRAMEWORK

The BCG Matrix categorizes products/business units into four quadrants based on:
- **X-axis**: Relative Market Share (compared to largest competitor)
- **Y-axis**: Market Growth Rate

### Four Quadrants:

1. **STARS** (High Growth, High Market Share)
   - Market leaders in fast-growing markets
   - Require investment to maintain position
   - Future cash cows
   - Strategic priority: Invest & grow

2. **CASH COWS** (Low Growth, High Market Share)
   - Market leaders in mature markets
   - Generate strong cash flow
   - Require minimal investment
   - Strategic priority: Harvest & maintain

3. **QUESTION MARKS** (High Growth, Low Market Share)
   - Small players in fast-growing markets
   - Consume cash, uncertain future
   - Require analysis: invest or divest
   - Strategic priority: Selective investment

4. **DOGS** (Low Growth, Low Market Share)
   - Weak position in mature markets
   - Generate little value
   - Drain resources
   - Strategic priority: Divest or niche

## YOUR ANALYSIS TASK

Perform a comprehensive BCG Matrix analysis for {company_name}:

### 1. PORTFOLIO IDENTIFICATION

Identify and categorize all major products, services, or business units:
- Product/service lines
- Geographic markets (if applicable)
- Customer segments (if distinct enough to be separate units)
- Business divisions

For each unit, estimate:
- Market growth rate (industry growth %)
- Relative market share (vs #1 competitor)
- Revenue contribution
- Profit margin
- Cash flow characteristics

### 2. BCG MATRIX CLASSIFICATION

Classify each portfolio item into the appropriate quadrant:

**STARS:**
- List each product/unit
- Market position and share
- Growth rate
- Investment requirements
- Strategic importance
- Competitive threats
- Path to becoming cash cow

**CASH COWS:**
- List each product/unit
- Market dominance indicators
- Cash generation capacity
- Maturity stage
- Defensive strategies needed
- Milking opportunities
- Risk of disruption

**QUESTION MARKS:**
- List each product/unit
- Growth potential
- Market share gap vs leader
- Investment required to become star
- Probability of success
- Recommendation: invest, hold, or divest
- Risk factors

**DOGS:**
- List each product/unit
- Why underperforming
- Cash drain analysis
- Turnaround potential (if any)
- Divestiture timeline
- Exit barriers

### 3. PORTFOLIO BALANCE ASSESSMENT

Analyze the overall portfolio balance:
- Current distribution across quadrants
- Cash flow balance (cows funding stars/question marks)
- Portfolio risk level
- Future cash flow concerns
- Diversification quality
- Strategic gaps

### 4. RESOURCE ALLOCATION STRATEGY

Recommend resource allocation:
- Which stars to prioritize
- Which cash cows to maximize
- Which question marks to invest in vs divest
- Which dogs to exit
- Investment priorities
- Divestiture candidates
- Acquisition targets to fill gaps

### 5. PORTFOLIO EVOLUTION STRATEGY

Map the strategic evolution:
- How to move question marks to stars
- How to transition stars to cash cows
- How to extend cash cow lifecycle
- New opportunities to develop
- Portfolio transformation timeline (3-5 years)

### 6. COMPETITIVE PORTFOLIO COMPARISON

If possible, compare to key competitors:
- How does their portfolio balance compare?
- What strategic advantages/disadvantages?
- Competitive portfolio moves to watch

### 7. STRATEGIC RECOMMENDATIONS

Provide clear, actionable recommendations:

**Immediate Actions (0-6 months):**
- Specific portfolio decisions
- Resource reallocations
- Quick wins

**Medium-term Strategy (6-18 months):**
- Major investment decisions
- Divestiture plans
- New product development

**Long-term Portfolio Vision (18+ months):**
- Target portfolio composition
- M&A strategy
- Market positioning goals

Provide your analysis in valid JSON format with this exact structure:
{{
    "portfolio_items": [
        {{
            "name": "Product/Service/Unit Name",
            "description": "...",
            "quadrant": "star|cash_cow|question_mark|dog",
            "market_growth_rate": 15,
            "relative_market_share": 1.5,
            "revenue_contribution_pct": 25,
            "profit_margin": "high|medium|low",
            "cash_flow": "strong_positive|positive|neutral|negative|strong_negative",
            "strategic_importance": "critical|high|medium|low",
            "analysis": "..."
        }}
    ],
    "quadrant_summaries": {{
        "stars": {{
            "count": 0,
            "total_revenue_pct": 0,
            "investment_required": "...",
            "strategic_priority": "...",
            "key_items": ["...", "..."]
        }},
        "cash_cows": {{...}},
        "question_marks": {{...}},
        "dogs": {{...}}
    }},
    "portfolio_balance": {{
        "overall_assessment": "balanced|star_heavy|cow_dependent|question_mark_heavy|dog_burdened",
        "cash_flow_health": "strong|adequate|concerning|critical",
        "future_outlook": "...",
        "key_risks": ["...", "..."],
        "strategic_gaps": ["...", "..."]
    }},
    "resource_allocation_strategy": {{
        "stars_to_prioritize": [
            {{
                "item": "...",
                "investment_amount": "...",
                "expected_outcome": "..."
            }}
        ],
        "cash_cows_to_maximize": [...],
        "question_marks_to_invest": [...],
        "question_marks_to_divest": [...],
        "dogs_to_exit": [
            {{
                "item": "...",
                "exit_strategy": "...",
                "timeline": "..."
            }}
        ],
        "acquisition_targets": ["...", "..."]
    }},
    "portfolio_evolution": {{
        "year_1": {{
            "target_distribution": {{"stars": 0, "cash_cows": 0, "question_marks": 0, "dogs": 0}},
            "key_transitions": ["...", "..."]
        }},
        "year_3": {{...}},
        "year_5": {{...}}
    }},
    "competitive_comparison": {{
        "competitor_portfolios": [
            {{
                "competitor": "...",
                "portfolio_balance": "...",
                "strategic_advantage": "..."
            }}
        ],
        "relative_position": "stronger|comparable|weaker"
    }},
    "strategic_recommendations": {{
        "immediate_actions": [
            {{
                "action": "...",
                "rationale": "...",
                "impact": "...",
                "difficulty": "low|medium|high"
            }}
        ],
        "medium_term": [...],
        "long_term": [...]
    }},
    "executive_summary": {{
        "portfolio_health": "excellent|good|adequate|poor|critical",
        "top_strengths": ["...", "..."],
        "critical_issues": ["...", "..."],
        "strategic_imperative": "...",
        "key_metrics": {{
            "star_revenue_pct": 0,
            "cash_cow_revenue_pct": 0,
            "question_mark_revenue_pct": 0,
            "dog_revenue_pct": 0
        }}
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

        # Try to extract JSON from markdown code blocks
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
    market_intel: Dict[str, Any]
) -> str:
    """Prepare context summary from previous analyses."""

    summary_parts = []

    if company_intel:
        summary_parts.append("COMPANY INTELLIGENCE:")
        if "products_services" in company_intel:
            summary_parts.append(f"- Products/Services: {', '.join(company_intel['products_services'][:5])}")
        if "business_overview" in company_intel:
            summary_parts.append(f"- Overview: {company_intel['business_overview'][:250]}...")

    if business_model:
        summary_parts.append("\nBUSINESS MODEL:")
        if "revenue_streams" in business_model:
            rs = business_model["revenue_streams"]
            if isinstance(rs, dict) and "streams" in rs:
                streams = [s.get("type", "") for s in rs["streams"][:3]]
                summary_parts.append(f"- Revenue Streams: {', '.join(streams)}")

    if market_intel:
        summary_parts.append("\nMARKET INTELLIGENCE:")
        if "market_size" in market_intel:
            ms = market_intel["market_size"]
            if isinstance(ms, dict):
                if "tam" in ms:
                    summary_parts.append(f"- TAM: {ms['tam']}")
                if "growth_rate" in ms:
                    summary_parts.append(f"- Market Growth: {ms['growth_rate']}")

    return "\n".join(summary_parts) if summary_parts else "Limited context - performing analysis based on industry knowledge."
