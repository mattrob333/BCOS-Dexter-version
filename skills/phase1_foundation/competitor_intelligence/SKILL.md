# Competitor Intelligence Skill

## Purpose

Build comprehensive intelligence on key competitors including their strategies, strengths, weaknesses, positioning, and competitive threats. Essential for understanding the competitive landscape.

## What This Skill Analyzes

### For Each Competitor

1. **Company Profile**
   - Size, scale, ownership
   - Geographic footprint
   - Market presence

2. **Products & Services**
   - Product portfolio
   - Pricing strategy
   - Differentiation

3. **Market Positioning**
   - Target segments
   - Value proposition
   - Market share

4. **Strengths & Weaknesses**
   - Competitive advantages
   - Vulnerabilities to exploit

5. **Strategy & Moves**
   - Current strategic focus
   - Recent actions (M&A, launches, partnerships)
   - Future direction

6. **Threat Assessment**
   - Threat level to our company
   - Areas of overlap
   - Where they win vs. where we win

### Competitive Landscape Analysis

7. **Market Structure**
   - Leaders, challengers, followers, niche players
   - Our position in the landscape

8. **Positioning Map**
   - Visual mapping of competitive positions
   - Key differentiating dimensions

9. **Feature Comparison**
   - Head-to-head capability comparison
   - Gap analysis

10. **Strategic Groups**
    - Clusters of competitors with similar strategies
    - Group characteristics

## Dependencies

**Requires**:
- Company Intelligence (Phase 1)
- Market Intelligence (Phase 1)
- Competitor list from config.yaml

## Configuration

In `config.yaml`:

```yaml
competitors:
  - "Square"
  - "Adyen"
  - "PayPal"
  - "Braintree"
```

## Outputs

```json
{
  "competitor_profiles": [
    {
      "name": "Square",
      "profile": {
        "revenue": "$17B",
        "employees": "8,000+",
        "headquarters": "San Francisco, CA",
        "ownership": "public (NYSE: SQ)"
      },
      "products_services": {
        "core_products": ["Point of Sale", "Cash App", "Square Banking"],
        "differentiation": "Integrated commerce ecosystem for SMBs",
        "pricing_strategy": "value"
      },
      "market_positioning": {
        "target_segments": ["Small businesses", "Individual sellers"],
        "value_proposition": "All-in-one commerce platform",
        "market_share": "~15%"
      },
      "strengths": [
        {
          "strength": "Cash App consumer network",
          "impact": "high",
          "description": "40M+ monthly active users"
        }
      ],
      "weaknesses": [
        {
          "weakness": "Limited enterprise capabilities",
          "exploitability": "high",
          "description": "Focused on SMB, less competitive upmarket"
        }
      ],
      "threat_assessment": {
        "threat_level": "high",
        "overlapping_segments": ["SMB payments"],
        "areas_where_they_win": ["Retail POS", "Small merchants"],
        "areas_where_we_win": ["Online platforms", "Enterprise", "Global"]
      }
    }
  ],
  "competitive_landscape": {
    "market_leaders": ["Stripe", "PayPal", "Adyen"],
    "our_position": "leader"
  },
  "competitive_positioning_map": {
    "axis_1": "price",
    "axis_2": "feature breadth",
    "positions": [
      {"company": "Our Company", "x": 7, "y": 8},
      {"company": "Square", "x": 4, "y": 5}
    ]
  },
  "competitive_insights": [
    "Market is segmenting into SMB-focused (Square) vs enterprise-focused (Stripe, Adyen)",
    "Winner-take-most dynamics in platform/ecosystem plays",
    "Geographic expansion is key competitive battleground"
  ]
}
```

## Analysis Frameworks Used

### Competitive Profile Matrix
Compares competitors across key success factors

### Positioning Map
2D visualization of competitive positions

### Strategic Group Analysis
Identifies clusters of competitors with similar strategies

### VRIO Analysis (per competitor)
- **V**aluable - Do they have valuable resources?
- **R**are - Are these resources rare?
- **I**nimitable - Hard to copy?
- **O**rganized - Can they exploit them?

## Usage in BCOS Workflow

**Position**: Phase 1 - Foundation Building
**Sequence**: After company intelligence and market intelligence
**Feeds Into**:
- Phase 2 SWOT (threats, competitive position)
- Phase 2 Porter's Five Forces (rivalry analysis)
- Competitive strategy recommendations
- Sales intelligence (competitor battlecards)

## Key Features

- **Multi-Competitor Analysis**: Profiles all key competitors
- **Threat Assessment**: Prioritizes competitive threats
- **Actionable Intelligence**: Identifies where to compete and how to win
- **Visual Mapping**: Positioning maps and comparisons
- **Strategic Insights**: Strategic group and landscape analysis

## Success Criteria

Competitor intelligence is complete when:
- All listed competitors are profiled
- Strengths and weaknesses identified for each
- Threat levels assessed
- Competitive positioning mapped
- Strategic insights generated
- Recommendations provided

## Future Enhancements

- Real-time competitor monitoring (news, launches)
- Website/product scraping for feature comparison
- Competitive pricing analysis
- Win/loss analysis integration
- Automated competitive battlecards
- Competitor social media analysis
- Patent and technology analysis
- Hiring trends analysis (job postings)

## Tips for Better Analysis

1. **Be Specific**: Don't just say "good product" - explain what makes it good
2. **Quantify**: Use numbers where possible (market share, pricing, scale)
3. **Current**: Focus on current state and recent moves
4. **Balanced**: Include both strengths and weaknesses
5. **Actionable**: Frame insights as competitive opportunities
