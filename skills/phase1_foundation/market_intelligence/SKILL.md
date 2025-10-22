# Market Intelligence Skill

## Purpose

Gather comprehensive intelligence about the market landscape, size, growth, trends, and opportunities in the target company's industry. Provides critical context for understanding the company's operating environment.

## What This Skill Analyzes

1. **Market Size & Growth**
   - TAM, SAM, SOM estimates
   - Historical and projected growth rates
   - Geographic distribution

2. **Market Segmentation**
   - Key market segments
   - Segment characteristics and sizes
   - Growth dynamics by segment

3. **Market Trends**
   - Technology trends
   - Consumer behavior shifts
   - Business model innovations

4. **Market Drivers**
   - Growth catalysts
   - Macroeconomic factors
   - Technology and regulatory enablers

5. **Challenges & Opportunities**
   - Industry headwinds
   - Untapped opportunities
   - Expansion possibilities

6. **Competitive Dynamics**
   - Market concentration
   - Barriers to entry
   - Competitive intensity

7. **Future Outlook**
   - Market trajectory
   - Disruption risks
   - Structural changes

## Dependencies

**Requires**: Company Intelligence (Phase 1)
- Industry classification
- Business description
- Target market information

## Outputs

```json
{
  "market_size": {
    "tam": {"value": "$1.2T", "unit": "USD", "year": 2024},
    "sam": {"value": "$150B", "unit": "USD", "year": 2024},
    "som": {"value": "$15B", "unit": "USD", "year": 2024},
    "growth_rate_cagr": "12.5%",
    "projected_size_2030": "$2.1T"
  },
  "market_segments": [
    {
      "segment_name": "SMB Payment Processing",
      "size": "$45B",
      "growth_rate": "15%",
      "characteristics": ["Fast-growing", "Digital-first"],
      "company_plays_here": true
    }
  ],
  "trends": [
    {
      "trend": "Embedded finance",
      "impact": "high",
      "timeframe": "current",
      "description": "Non-financial companies offering financial services",
      "implications_for_company": "Opportunity to power embedded payments"
    }
  ],
  "opportunities": [
    {
      "opportunity": "Southeast Asia expansion",
      "type": "geography",
      "size": "$25B by 2028",
      "effort_required": "high",
      "description": "Fast-growing digital payments market",
      "rationale": "Underserved market with rapid digitalization"
    }
  ],
  "competitive_dynamics": {
    "market_concentration": "moderately-concentrated",
    "barriers_to_entry": "high",
    "key_success_factors": ["Technology", "Trust", "Compliance"],
    "switching_costs": "medium"
  },
  "future_outlook": {
    "trajectory": "rapid-growth",
    "disruption_risk": "medium",
    "key_uncertainties": ["Regulation", "Crypto adoption"],
    "potential_disruptors": ["CBDCs", "DeFi protocols"]
  }
}
```

## Key Features

- **Quantitative Analysis**: Market sizing with TAM/SAM/SOM
- **Trend Identification**: Spot emerging trends early
- **Opportunity Mapping**: Identify growth opportunities
- **Risk Assessment**: Understand market challenges
- **Forward-Looking**: Future outlook and disruption analysis

## Market Sizing Framework

**TAM (Total Addressable Market)**: Total market demand if company achieved 100% market share

**SAM (Serviceable Addressable Market)**: Portion of TAM company can realistically serve given its business model

**SOM (Serviceable Obtainable Market)**: Portion of SAM company can realistically capture in near term

## Usage in BCOS Workflow

**Position**: Phase 1 - Foundation Building
**Sequence**: After company intelligence
**Feeds Into**:
- Business Model Canvas (market context)
- Competitor Intelligence (market dynamics)
- Phase 2 SWOT (opportunities & threats)
- Phase 2 strategic frameworks

## Success Criteria

Market intelligence is complete when:
- Market size estimates provided (TAM/SAM/SOM)
- Key trends identified and assessed
- Growth drivers and challenges documented
- Opportunities mapped
- Competitive dynamics understood
- Future outlook articulated

## Data Sources

Currently uses LLM knowledge base. Future enhancements:

- Industry reports via web scraping
- Market research databases
- News APIs for trend analysis
- Financial data APIs
- Regulatory filings

## Future Enhancements

- Real-time market data integration
- Industry-specific analysis templates
- Competitor market share analysis
- Market trend tracking over time
- Interactive market maps
- Automated opportunity scoring
