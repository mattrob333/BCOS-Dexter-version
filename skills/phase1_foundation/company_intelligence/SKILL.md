# Company Intelligence Skill

## Purpose

Gather foundational business intelligence about a target company from their website and public sources. This is typically the first skill executed in Phase 1.

## What This Skill Does

1. **Website Scraping**: Uses Firecrawl to scrape the company's website
2. **Content Analysis**: Uses LLM to analyze website content and extract structured information
3. **Fallback Knowledge**: If scraping fails, uses LLM's knowledge base

## Inputs

- **Company name**: Target company to research
- **Company website**: URL to scrape
- **Industry**: Company's industry vertical

## Outputs

Returns a dictionary with:

```json
{
  "company_name": "Stripe",
  "website": "https://stripe.com",
  "industry": "Financial Technology",
  "business_description": "Stripe builds economic infrastructure for the internet...",
  "products_services": [
    "Payment processing",
    "Stripe Terminal",
    "Stripe Atlas",
    "etc."
  ],
  "target_customers": "Online businesses, marketplaces, SaaS companies",
  "value_proposition": "Developer-friendly payment infrastructure with powerful APIs",
  "key_facts": {
    "founded": "2010",
    "headquarters": "San Francisco, CA",
    "team_size": "8000+",
    "revenue": "$14B+ ARR"
  },
  "business_model": "Transaction fees + subscription pricing",
  "confidence": "high"
}
```

## Data Sources Used

- **Firecrawl**: Primary website scraping
- **Fallback**: requests + BeautifulSoup if Firecrawl unavailable
- **LLM Knowledge**: Fallback when scraping fails

## Dependencies

- Firecrawl API key (optional but recommended)
- Anthropic API key (required)

## Configuration

No skill-specific configuration needed. Uses global config:

```yaml
company:
  name: "Stripe"
  website: "https://stripe.com"
  industry: "Financial Technology"
```

## Success Criteria

The skill successfully completes if:
1. Website content is scraped OR fallback knowledge is retrieved
2. LLM analysis produces structured output
3. Confidence level is at least "low"

## Error Handling

- If Firecrawl fails → Use requests/BeautifulSoup
- If scraping fails → Use LLM knowledge base
- If LLM fails → Return error dictionary

## Example Usage

```python
from skills.phase1_foundation.company_intelligence import execute

result = execute(
    task=task_object,
    context={'company': {...}},
    config=config_dict
)

print(result['business_description'])
print(result['products_services'])
```

## Future Enhancements

- Add Exa semantic search for richer company data
- Integrate Crunchbase for funding/financial data
- Add news API for recent developments
- Parse SEC filings for public companies
- Social media sentiment analysis
