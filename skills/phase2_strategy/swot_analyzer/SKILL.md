# SWOT Analyzer Skill

## Purpose

Conduct comprehensive SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis - one of the most fundamental and widely-used strategic planning frameworks. Synthesizes Phase 1 findings into strategic insights.

## Framework Overview

SWOT Analysis examines four key dimensions:

### Internal Factors (Current State)
- **Strengths**: What advantages does the company have?
- **Weaknesses**: What disadvantages or gaps exist?

### External Factors (Future Potential)
- **Opportunities**: What favorable external conditions can be exploited?
- **Threats**: What external challenges or risks exist?

## Advanced Features

This skill goes beyond basic SWOT to include:

### TOWS Matrix
Strategic initiatives derived from combinations:
- **SO (Strength-Opportunity)**: Leverage strengths to capitalize on opportunities
- **WO (Weakness-Opportunity)**: Address weaknesses to pursue opportunities
- **ST (Strength-Threat)**: Use strengths to defend against threats
- **WT (Weakness-Threat)**: Minimize weaknesses to avoid threats

### Prioritization
- Ranks items by importance and impact
- Identifies "must-address" items
- Highlights best opportunities

### Strategic Implications
- Translates SWOT into strategic direction
- Recommends focus areas
- Suggests concrete actions

## Dependencies

**Requires** (Phase 1 outputs):
- Company Intelligence
- Business Model Canvas
- Market Intelligence
- Competitor Intelligence

## Outputs

```json
{
  "strengths": [
    {
      "strength": "Developer-first API platform",
      "category": "product",
      "impact": "high",
      "description": "Industry-leading developer experience drives adoption",
      "evidence": "90% of developers prefer Stripe APIs in surveys",
      "sustainability": "sustainable"
    }
  ],
  "weaknesses": [
    {
      "weakness": "Limited physical retail presence",
      "category": "product",
      "severity": "medium",
      "description": "Weaker in brick-and-mortar commerce vs Square",
      "addressability": "moderate"
    }
  ],
  "opportunities": [
    {
      "opportunity": "Embedded finance in vertical SaaS",
      "category": "market",
      "potential_impact": "high",
      "description": "Enable non-fintech companies to offer financial services",
      "timeframe": "immediate",
      "attractiveness_score": 9
    }
  ],
  "threats": [
    {
      "threat": "Big tech (Apple, Google) entering payments",
      "category": "competitive",
      "severity": "high",
      "probability": "medium",
      "timeframe": "medium-term",
      "mitigation_options": ["Differentiate on B2B", "Partner rather than compete"]
    }
  ],
  "tows_matrix": {
    "so_strategies": [
      {
        "strategy": "Use developer platform strength to capture embedded finance opportunity",
        "strength": "Developer-first platform",
        "opportunity": "Embedded finance growth",
        "description": "Build Stripe-powered banking-as-a-service for vertical SaaS",
        "priority": "high"
      }
    ]
  },
  "prioritization": {
    "top_strengths": ["Developer platform", "Global infrastructure", "Brand trust"],
    "critical_weaknesses": ["Enterprise sales motion", "Physical retail"],
    "best_opportunities": ["Embedded finance", "SE Asia expansion", "Crypto payments"],
    "biggest_threats": ["Big tech competition", "Regulatory changes", "Economic downturn"]
  },
  "strategic_implications": [
    "Double down on developer platform as core differentiator",
    "Address enterprise weakness to capture upmarket opportunity",
    "Move quickly on embedded finance before competition intensifies"
  ]
}
```

## Analysis Depth

### Strengths Analysis
- **Categorization**: Product, brand, operations, financial, team, technology
- **Impact Assessment**: High/medium/low importance
- **Sustainability**: Will this strength endure?
- **Evidence**: What supports this claim?

### Weaknesses Analysis
- **Severity**: How much does this hurt us?
- **Addressability**: How hard to fix?
- **Competitive Impact**: Do competitors exploit this?

### Opportunities Analysis
- **Attractiveness Score**: Quantified 1-10 rating
- **Timeframe**: When can we pursue this?
- **Requirements**: What's needed to capture?
- **Fit**: Alignment with capabilities

### Threats Analysis
- **Probability**: Likelihood of occurring
- **Severity**: Impact if it happens
- **Timeframe**: When might this materialize?
- **Mitigation**: How can we defend?

## Usage in BCOS Workflow

**Position**: Phase 2 - Strategy Analysis
**Sequence**: First Phase 2 framework (synthesizes all Phase 1 data)
**Feeds Into**:
- Porter's Five Forces (validates competitive threats)
- Strategic recommendations
- OKR/KPI setting
- Investment prioritization

## Key Features

1. **Context-Rich**: Uses all Phase 1 data for deep analysis
2. **TOWS Matrix**: Generates strategic initiatives, not just lists
3. **Prioritized**: Ranks items by importance
4. **Actionable**: Links to concrete strategic implications
5. **Evidence-Based**: Grounds claims in Phase 1 findings

## Success Criteria

SWOT analysis is complete when:
- All four quadrants are comprehensively analyzed
- Items are categorized and prioritized
- TOWS matrix generates strategic initiatives
- Strategic implications are articulated
- Recommended focus areas identified

## Common Pitfalls (Avoided by This Skill)

❌ **Vague Items**: "Good team" → ✅ "World-class ML engineering team with 15 PhD researchers"

❌ **Mixing Internal/External**: Opportunity listed as strength → ✅ Proper categorization

❌ **No Prioritization**: Long equal lists → ✅ Ranked by importance

❌ **No Actions**: Just lists → ✅ TOWS strategies and implications

❌ **Inconsistency**: Contradictory items → ✅ Logic-checked

## Strategic Frameworks Integration

SWOT works well with:
- **Porter's Five Forces**: Validates competitive threats
- **BCG Matrix**: Maps opportunities to resource allocation
- **Blue Ocean**: Identifies strategic moves
- **Business Model Canvas**: Links to value creation

## Future Enhancements

- Visual SWOT matrix diagram
- Quantitative scoring models
- Historical SWOT tracking (evolution over time)
- Competitor SWOT comparison
- Scenario planning based on threat/opportunity combinations
- Action plan generation from TOWS matrix
- Integration with OKR framework
