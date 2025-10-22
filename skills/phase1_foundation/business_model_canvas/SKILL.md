# Business Model Canvas Skill

## Purpose

Analyze a company's business model using the Business Model Canvas (BMC) framework - one of the most widely used strategic analysis tools for understanding how businesses create, deliver, and capture value.

## Framework Overview

The Business Model Canvas breaks down any business model into 9 building blocks:

### Customer-Facing (Right Side)
1. **Customer Segments** - Who are we creating value for?
2. **Value Propositions** - What value do we deliver?
3. **Channels** - How do we reach customers?
4. **Customer Relationships** - How do we interact?
5. **Revenue Streams** - How do we make money?

### Infrastructure (Left Side)
6. **Key Resources** - What assets do we need?
7. **Key Activities** - What must we do?
8. **Key Partnerships** - Who helps us?

### Foundation (Bottom)
9. **Cost Structure** - What are our main costs?

## Dependencies

**Requires**: Company Intelligence (Phase 1)
- Business description
- Products/services
- Target customers
- Value proposition
- Business model overview

## Inputs

From context:
- Company name
- Industry
- Company intelligence findings
- Business description
- Products and services

## Outputs

Returns a comprehensive BMC analysis:

```json
{
  "customer_segments": [
    {
      "segment_name": "SMB SaaS Companies",
      "description": "Small to medium software companies",
      "characteristics": ["Fast growth", "Online-first", "Global"],
      "size_estimate": "10M+ businesses globally"
    }
  ],
  "value_propositions": [
    {
      "for_segment": "SMB SaaS Companies",
      "core_value": "Developer-friendly payment infrastructure",
      "problems_solved": ["Complex payment integration", "Global compliance"],
      "needs_satisfied": ["Fast setup", "Scalability", "Security"],
      "differentiation": "Superior developer experience"
    }
  ],
  "channels": {
    "awareness": ["Developer communities", "Content marketing", "Word of mouth"],
    "evaluation": ["Documentation", "Sandbox environment", "API demos"],
    "purchase": ["Self-service signup", "Online dashboard"],
    "delivery": ["API integration", "Cloud-based SaaS"],
    "after_sales": ["24/7 support", "Developer forums", "Account managers"]
  },
  "customer_relationships": [
    {
      "segment": "SMB SaaS",
      "relationship_type": "Self-service + Community",
      "description": "Developer-driven adoption with community support",
      "examples": ["Documentation", "GitHub", "Stack Overflow", "Discord"]
    }
  ],
  "revenue_streams": [
    {
      "stream_type": "Transaction fees",
      "description": "Percentage of payment volume processed",
      "pricing_mechanism": "2.9% + $0.30 per transaction",
      "contribution": "Primary revenue (90%+)"
    }
  ],
  "key_resources": {
    "physical": ["Data centers", "Global infrastructure"],
    "intellectual": ["Payment processing technology", "APIs", "Brand"],
    "human": ["Engineers", "Developer relations", "Sales"],
    "financial": ["Capital for scaling", "Regulatory licenses"]
  },
  "key_activities": [
    {
      "activity": "Payment processing",
      "category": "platform",
      "importance": "critical",
      "description": "Secure, reliable payment infrastructure"
    }
  ],
  "key_partnerships": [
    {
      "partner_type": "Financial institutions",
      "partners": ["Banks", "Card networks (Visa, Mastercard)"],
      "motivation": "Access to payment rails",
      "what_they_provide": "Payment processing capabilities"
    }
  ],
  "cost_structure": {
    "model": "value-driven",
    "major_costs": [
      {
        "cost_category": "Engineering & R&D",
        "type": "fixed",
        "description": "Product development and innovation",
        "significance": "30-40% of costs"
      }
    ],
    "economies_of_scale": "Strong - platform benefits from volume",
    "economies_of_scope": "Expanding product suite reduces CAC"
  },
  "insights": [
    "Multi-sided platform model creates network effects",
    "Developer-first approach reduces sales costs",
    "Value-driven cost structure supports premium positioning"
  ],
  "bmc_archetype": "multi-sided-platform",
  "confidence": "high"
}
```

## Key Features

1. **Comprehensive Analysis**: Covers all 9 BMC building blocks
2. **Context-Aware**: Uses company intelligence from Phase 1
3. **Strategic Insights**: Identifies business model archetype
4. **Detailed Breakdown**: Goes deep on each building block
5. **Actionable**: Provides insights for strategy work

## Business Model Archetypes

The skill identifies which archetype(s) apply:

- **Unbundled**: Separate infrastructure, product, customer relationship
- **Long Tail**: Many niche products
- **Multi-Sided Platform**: Brings together distinct groups
- **Free/Freemium**: Free offering subsidized by premium
- **Open**: Open source with services revenue

## Usage in BCOS Workflow

**Position**: Phase 1 - Foundation Building
**Sequence**: After company intelligence
**Feeds Into**:
- Phase 2 strategy frameworks (SWOT, Porter's)
- Competitive analysis
- Strategic recommendations

## Success Criteria

BMC analysis is complete when:
- All 9 building blocks are analyzed
- Customer segments are clearly defined
- Revenue and cost models are understood
- Key partnerships are identified
- Strategic insights are provided

## Future Enhancements

- Visual BMC diagram generation
- Comparison with competitor business models
- BMC evolution over time analysis
- Integration with financial data for validation
- Industry-specific BMC templates
