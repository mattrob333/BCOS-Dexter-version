# Porter's Five Forces Analyzer Skill

## Purpose

Analyze industry structure and competitive dynamics using Michael Porter's Five Forces framework. Assesses industry attractiveness and helps identify strategic positioning opportunities.

## Framework Overview

Porter's Five Forces examines five competitive forces that shape industry competition:

### The Five Forces

1. **Threat of New Entrants**
   - How easy is it for new competitors to enter?
   - What barriers protect incumbents?

2. **Bargaining Power of Suppliers**
   - How much leverage do suppliers have?
   - Can they raise prices or reduce quality?

3. **Bargaining Power of Buyers**
   - How much leverage do customers have?
   - Can they demand lower prices or better terms?

4. **Threat of Substitute Products/Services**
   - What alternatives exist?
   - How easily can customers switch?

5. **Rivalry Among Existing Competitors**
   - How intense is competitive competition?
   - What's the basis of competition?

### Industry Attractiveness

The interaction of these five forces determines:
- **Profitability potential** of the industry
- **Strategic positioning opportunities**
- **Competitive advantages** to pursue

**High Force Intensity** → **Lower Industry Attractiveness** → **Lower Profit Potential**

## Dependencies

**Requires** (Phase 1 outputs):
- Company Intelligence
- Business Model Canvas
- Market Intelligence
- Competitor Intelligence

## Outputs

```json
{
  "threat_of_new_entrants": {
    "intensity": "low",
    "trend": "stable",
    "barriers_to_entry": {
      "capital_requirements": {"level": "high", "description": "$100M+ to build global payment infrastructure"},
      "regulatory_requirements": {"level": "high", "description": "Money transmitter licenses in 50+ jurisdictions"},
      "network_effects": {"level": "high", "description": "Two-sided marketplace benefits from scale"},
      "brand_loyalty": {"level": "medium", "description": "Switching costs moderate for established merchants"}
    },
    "strategic_implications": "Maintain barriers through continued investment in infrastructure and compliance"
  },
  "supplier_power": {
    "intensity": "medium",
    "key_suppliers": ["Card networks (Visa, Mastercard)", "Banks", "Cloud providers"],
    "supplier_concentration": "concentrated",
    "forward_integration_threat": "low",
    "strategic_implications": "Diversify payment rails, build direct bank relationships"
  },
  "buyer_power": {
    "intensity": "medium",
    "customer_concentration": "fragmented",
    "price_sensitivity": "high",
    "switching_costs": "medium",
    "strategic_implications": "Differentiate through superior product, increase switching costs via platform"
  },
  "threat_of_substitutes": {
    "intensity": "medium",
    "substitutes": [
      {
        "substitute": "Direct bank integrations",
        "price_performance": "inferior",
        "switching_cost": "high",
        "description": "Cheaper but far more complex to build"
      },
      {
        "substitute": "Cryptocurrency payments",
        "price_performance": "similar",
        "adoption_rate": "low",
        "description": "Emerging but limited merchant/consumer adoption"
      }
    ],
    "emerging_substitutes": ["CBDCs", "Account-to-account payments"],
    "strategic_implications": "Monitor crypto evolution, potentially integrate as additional rail"
  },
  "competitive_rivalry": {
    "intensity": "high",
    "number_of_competitors": "10+ major players",
    "market_growth_rate": "15% CAGR",
    "product_differentiation": "medium",
    "competitive_tactics": ["Price competition", "Geographic expansion", "Feature innovation"],
    "strategic_implications": "Compete on innovation and developer experience rather than price"
  },
  "overall_assessment": {
    "industry_attractiveness": "moderately-attractive",
    "attractiveness_score": 7,
    "strongest_force": "competitive_rivalry",
    "weakest_force": "threat_of_new_entrants",
    "profit_potential": "medium",
    "key_dynamics": [
      "High growth mitigates intense rivalry",
      "Strong barriers protect from new entrants",
      "Platform effects favor scaled players"
    ]
  },
  "strategic_recommendations": [
    {
      "recommendation": "Strengthen network effects through platform expansion",
      "force_addressed": "threat_of_new_entrants",
      "rationale": "Make it harder for new entrants by deepening platform value",
      "priority": "high"
    }
  ]
}
```

## Analysis Methodology

### For Each Force

1. **Identify Key Factors**: What drives this force?
2. **Assess Intensity**: Low/Medium/High
3. **Determine Trend**: Increasing/Stable/Decreasing
4. **Quantify Impact**: How does it affect profitability?
5. **Derive Implications**: What should company do?

### Barrier Analysis

For **Threat of New Entrants**, analyzes seven key barriers:
- Capital requirements
- Economies of scale
- Technology complexity
- Regulatory requirements
- Brand loyalty
- Network effects
- Access to distribution

### Overall Assessment

Synthesizes all five forces into:
- Industry attractiveness rating
- Profitability potential
- Strongest vs weakest forces
- Key strategic opportunities

## Usage in BCOS Workflow

**Position**: Phase 2 - Strategy Analysis
**Sequence**: After SWOT, complements competitive analysis
**Feeds Into**:
- Competitive strategy formulation
- Market entry/expansion decisions
- M&A target identification
- Pricing strategy
- Partnership strategy

## Key Insights Provided

1. **Industry Structure**: Is this an attractive industry to compete in?
2. **Profit Drivers**: What determines profitability in this industry?
3. **Competitive Dynamics**: How do companies compete?
4. **Strategic Opportunities**: Where can we build competitive advantage?
5. **Risk Factors**: What forces threaten profitability?

## Relationship to Other Frameworks

**Complements SWOT**:
- SWOT threats often map to Five Forces
- SWOT opportunities may come from weak forces
- Porter's provides industry-level view, SWOT is company-specific

**Informs Blue Ocean Strategy**:
- High-intensity forces → seek blue ocean alternatives
- Identify which forces to alter or eliminate

**Links to Business Model Canvas**:
- Supplier power → Key Partnerships analysis
- Buyer power → Customer Relationships strategy
- Rivalry → Value Proposition differentiation

## Success Criteria

Five Forces analysis is complete when:
- All five forces analyzed comprehensively
- Intensity and trend assessed for each
- Key factors identified and explained
- Strategic implications articulated
- Overall industry attractiveness determined
- Recommendations provided

## Strategic Applications

### Competitive Strategy
- Where to compete (attractive segments)
- How to compete (bases of differentiation)
- When to compete (timing of entry/expansion)

### Risk Management
- Identify threats to profitability
- Develop contingency plans
- Monitor force intensity changes

### Investment Decisions
- M&A target evaluation
- Market entry decisions
- Resource allocation

## Future Enhancements

- Time-series analysis (force evolution)
- Industry comparison (benchmarking)
- Scenario analysis (how forces might change)
- Sub-segment analysis (forces vary by segment)
- Visual force diagrams
- Integration with financial modeling
- Automated force monitoring (news, competitive moves)

## Common Pitfalls (Avoided)

❌ **Static Analysis**: Forces change over time → ✅ Trend analysis included

❌ **Industry Too Broad**: "Technology" is not an industry → ✅ Specific to relevant industry

❌ **Ignoring Complements**: Some models add "6th force" → ✅ Covered in supplier analysis

❌ **No Strategic Link**: Just description → ✅ Strategic implications for each force

❌ **Copying Generic Analysis**: Same for all companies → ✅ Company-specific context
