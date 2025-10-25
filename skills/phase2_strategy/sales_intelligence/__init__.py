"""
Sales Intelligence Skill

Creates sales enablement materials including account targeting strategies,
sales playbooks, competitive battlecards, and messaging frameworks.
"""

import json
import logging
from typing import Any, Dict, List
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SKILL_METADATA = {
    "name": "sales_intelligence",
    "description": "Generate sales playbooks, account targeting, and battlecards",
    "phase": "phase2",
    "dependencies": ["competitor_intelligence", "value_proposition_analysis", "competitive_strategy"],
    "outputs": ["sales_intelligence_analysis"]
}


def execute(task: Any, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute sales intelligence analysis."""
    logger.info(f"Executing Sales Intelligence Analysis: {task.description if hasattr(task, 'description') else 'Sales Intelligence'}")

    try:
        company_name = config.get("company", {}).get("name", "Unknown Company")
        industry = config.get("company", {}).get("industry", "")

        # Get target prospects from config
        target_prospects = config.get("target_prospects", [])

        # Get context
        competitor_intel = context.get("competitor_intelligence", {})
        value_prop = context.get("value_proposition_analysis", {})
        competitive_strategy = context.get("competitive_strategy_analysis", {})
        business_model = context.get("business_model_canvas", {})

        analysis = _generate_sales_intelligence(
            company_name=company_name,
            industry=industry,
            target_prospects=target_prospects,
            competitor_intel=competitor_intel,
            value_prop=value_prop,
            competitive_strategy=competitive_strategy,
            business_model=business_model,
            config=config
        )

        logger.info("Sales intelligence analysis completed")
        return {
            "status": "success",
            "data": analysis,
            "metadata": {
                "company": company_name,
                "analysis_type": "Sales Intelligence",
                "skill": "sales_intelligence"
            }
        }

    except Exception as e:
        logger.error(f"Error in sales intelligence analysis: {str(e)}")
        return {"status": "error", "error": str(e), "data": {}}


def _generate_sales_intelligence(
    company_name: str,
    industry: str,
    target_prospects: List[str],
    competitor_intel: Dict[str, Any],
    value_prop: Dict[str, Any],
    competitive_strategy: Dict[str, Any],
    business_model: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate sales intelligence using Claude."""

    context_summary = _prepare_context_summary(
        competitor_intel, value_prop, competitive_strategy, business_model
    )

    prospects_list = ", ".join(target_prospects) if target_prospects else "Enterprise B2B companies in the industry"

    analysis_prompt = f"""You are a sales enablement expert creating comprehensive sales intelligence materials.

Company: {company_name}
Industry: {industry}
Target Prospects: {prospects_list}

CONTEXT:
{context_summary}

## YOUR TASK

Create comprehensive sales intelligence covering ideal customer profiles, account targeting,
sales playbooks, competitive battlecards, and messaging frameworks.

### 1. IDEAL CUSTOMER PROFILE (ICP)

**Firmographic Criteria:**
- Industry/vertical
- Company size (employees, revenue)
- Geography
- Growth stage
- Ownership structure

**Technographic Criteria:**
- Technology stack
- Digital maturity
- Cloud adoption
- Security posture

**Behavioral Criteria:**
- Buying behavior
- Decision-making process
- Budget cycle
- Innovation adoption

**Pain Points & Triggers:**
- Common pain points for ICP
- Buying triggers and events
- Urgency drivers
- Success metrics they care about

**ICP Scoring:**
- Must-have criteria
- Nice-to-have criteria
- Disqualifying factors
- Lead scoring model

### 2. ACCOUNT TARGETING STRATEGY

For each target prospect provided (or general strategy if none specified):

**Account Intelligence:**
- Company overview
- Recent news and developments
- Strategic priorities
- Pain points and challenges
- Buying center mapping
- Budget and timing

**Personalized Value Proposition:**
- Specific value for this account
- ROI potential
- Risk mitigation
- Strategic fit

**Account Entry Strategy:**
- Best entry point (department, role)
- Key decision makers and influencers
- Champions to cultivate
- Economic buyer identification

**Engagement Approach:**
- Outreach messaging
- Conversation starters
- Content to share
- Events/touchpoints

### 3. SALES PLAYBOOK

**Discovery Questions:**

Create 20+ discovery questions across categories:

**Situational Questions:**
- Current state assessment
- Technology environment
- Team structure
- Processes

**Problem Questions:**
- Pain points and challenges
- Cost of current situation
- Failed solutions
- Workarounds

**Implication Questions:**
- Impact on business
- Downstream effects
- Opportunity cost
- Strategic implications

**Need-Payoff Questions:**
- Desired outcomes
- Value of solving problem
- Success metrics
- ROI expectations

**Sales Stages & Progression Criteria:**

For each stage, define:
- Stage definition
- Progression criteria
- Key activities
- Required evidence
- Sales materials needed
- Common obstacles

Stages:
1. Prospecting
2. Discovery
3. Solution Presentation
4. Proposal
5. Negotiation
6. Closed Won/Lost

**Objection Handling:**

For each common objection, provide:
- Objection statement
- Root cause/concern
- Response framework
- Proof points
- Follow-up questions

Common objections:
- "Too expensive"
- "We're happy with current solution"
- "Not a priority right now"
- "We'll build it ourselves"
- "Your competitor is cheaper"
- "We need more features"
- "Security concerns"
- "Implementation complexity"

### 4. COMPETITIVE BATTLECARDS

For top 3-5 competitors, create battlecards:

**Competitor Overview:**
- Company snapshot
- Market position
- Target customers
- Pricing model

**Strengths (acknowledge honestly):**
- What they do well
- When they win
- Customer types they fit

**Weaknesses (exploit):**
- Gaps and limitations
- Customer complaints
- Areas we're stronger

**Differentiation:**
- How we're different
- Why we're better
- Proof points
- Customer testimonials

**Trap-Setting Questions:**
- Questions that expose their weaknesses
- Questions that highlight our strengths
- Discovery that favors our solution

**Competitive Messaging:**
- How to position against them
- FUD to avoid
- Positive differentiation
- Win themes

**Pricing Comparison:**
- How pricing compares
- TCO comparison
- Value justification

**Win/Loss Patterns:**
- When we typically win vs them
- When we typically lose
- Deal criteria that favor us

### 5. MESSAGING FRAMEWORK

**Value Propositions by Persona:**

For each key buyer persona:
- Persona description (role, responsibilities, goals)
- Key pain points
- Tailored value proposition
- Proof points and case studies
- Success metrics they care about

Personas to cover:
- Economic Buyer (C-level, VP)
- Technical Buyer (CTO, Architect)
- End User (Manager, IC)
- Champion (Internal advocate)

**Elevator Pitches:**
- 10-second pitch
- 30-second pitch
- 2-minute pitch

For each:
- Hook/attention grabber
- Problem statement
- Solution overview
- Differentiation
- Call to action

**Messaging Pillars:**

3-5 core messages with:
- Message statement
- Supporting points
- Proof points
- Objection handling
- Use cases

**ROI & Business Case:**
- ROI calculation framework
- Cost savings categories
- Revenue impact categories
- Productivity gains
- Risk reduction
- Typical payback period
- Success metrics

### 6. SALES ENABLEMENT ASSETS

**Priority Content Needs:**
- Case studies needed
- Product demos
- ROI calculators
- Comparison guides
- White papers
- Recorded demos
- Reference customers

**Sales Tools:**
- CRM fields to capture
- Email templates
- Call scripts
- LinkedIn outreach messages
- Proposal templates
- Contract templates

Provide analysis in valid JSON:
{{
    "ideal_customer_profile": {{
        "firmographic": {{
            "industries": ["...", "..."],
            "company_size": "...",
            "revenue_range": "...",
            "geography": ["...", "..."]
        }},
        "technographic": {{
            "required_tech": ["...", "..."],
            "digital_maturity": "high|medium|low"
        }},
        "behavioral": {{
            "buying_process": "...",
            "decision_timeline": "...",
            "budget_cycle": "..."
        }},
        "pain_points": ["...", "..."],
        "buying_triggers": ["...", "..."],
        "icp_scoring": {{
            "must_have": ["...", "..."],
            "nice_to_have": ["...", "..."],
            "disqualifying": ["...", "..."]
        }}
    }},
    "target_account_strategies": [
        {{
            "account_name": "...",
            "account_intelligence": {{
                "overview": "...",
                "recent_news": ["...", "..."],
                "strategic_priorities": ["...", "..."],
                "pain_points": ["...", "..."]
            }},
            "personalized_value_prop": "...",
            "entry_strategy": {{
                "entry_point": "...",
                "key_contacts": [
                    {{
                        "name": "...",
                        "role": "...",
                        "influence_level": "decision_maker|influencer|champion|end_user"
                    }}
                ],
                "engagement_approach": "..."
            }}
        }}
    ],
    "sales_playbook": {{
        "discovery_questions": {{
            "situational": ["...", "..."],
            "problem": ["...", "..."],
            "implication": ["...", "..."],
            "need_payoff": ["...", "..."]
        }},
        "sales_stages": [
            {{
                "stage": "prospecting|discovery|solution|proposal|negotiation|closed",
                "progression_criteria": ["...", "..."],
                "key_activities": ["...", "..."],
                "required_evidence": ["...", "..."],
                "common_obstacles": ["...", "..."]
            }}
        ],
        "objection_handling": [
            {{
                "objection": "...",
                "root_cause": "...",
                "response_framework": "...",
                "proof_points": ["...", "..."],
                "follow_up_questions": ["...", "..."]
            }}
        ]
    }},
    "competitive_battlecards": [
        {{
            "competitor": "...",
            "overview": "...",
            "strengths": ["...", "..."],
            "weaknesses": ["...", "..."],
            "our_differentiation": ["...", "..."],
            "trap_questions": ["...", "..."],
            "competitive_messaging": "...",
            "pricing_comparison": "...",
            "win_loss_patterns": {{
                "we_win_when": ["...", "..."],
                "we_lose_when": ["...", "..."]
            }}
        }}
    ],
    "messaging_framework": {{
        "value_props_by_persona": [
            {{
                "persona": "...",
                "role": "...",
                "pain_points": ["...", "..."],
                "value_proposition": "...",
                "proof_points": ["...", "..."],
                "success_metrics": ["...", "..."]
            }}
        ],
        "elevator_pitches": {{
            "10_second": "...",
            "30_second": "...",
            "2_minute": "..."
        }},
        "messaging_pillars": [
            {{
                "pillar": "...",
                "supporting_points": ["...", "..."],
                "proof_points": ["...", "..."]
            }}
        ],
        "roi_framework": {{
            "cost_savings": ["...", "..."],
            "revenue_impact": ["...", "..."],
            "productivity_gains": ["...", "..."],
            "typical_payback_months": 12
        }}
    }},
    "enablement_assets": {{
        "priority_content": [
            {{
                "asset_type": "case_study|demo|calculator|guide|whitepaper",
                "topic": "...",
                "priority": "p0|p1|p2",
                "usage": "..."
            }}
        ],
        "sales_tools": [
            {{
                "tool": "...",
                "description": "...",
                "usage": "..."
            }}
        ]
    }},
    "executive_summary": {{
        "icp_clarity": "clear|moderate|needs_refinement",
        "competitive_intelligence": "strong|adequate|weak",
        "sales_readiness": "high|medium|low",
        "top_priorities": ["...", "..."],
        "quick_wins": ["...", "..."]
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
    value_prop: Dict[str, Any],
    competitive_strategy: Dict[str, Any],
    business_model: Dict[str, Any]
) -> str:
    """Prepare context summary."""
    return """Previous analyses available:
- Competitor Intelligence: Detailed competitor profiles
- Value Proposition Analysis: Customer jobs, pains, gains
- Competitive Strategy: Positioning and differentiation
- Business Model: Revenue streams and customer segments"""
