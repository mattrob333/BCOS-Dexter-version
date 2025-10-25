# Getting Started with BCOS

Welcome! This guide will help you set up and run your first business analysis with BCOS.

## What's Been Implemented

✅ **Core System** (Production Ready):
- Multi-agent orchestrator with Dexter-inspired architecture
- Task planning, execution, and validation
- State management and context passing
- Loop detection and safety limits

✅ **Data Sources**:
- Firecrawl client (with fallback to requests/BeautifulSoup)

✅ **Phase 1 Skills** (Foundation Building - 6 Skills):
- **Company Intelligence** - Scrapes website, extracts business info
- **Business Model Canvas** - Analyzes business model across 9 building blocks
- **Market Intelligence** - TAM/SAM/SOM, trends, opportunities, competitive dynamics
- **Competitor Intelligence** - Profiles competitors, positioning, threat assessment
- **Value Chain Mapper** - Porter's Value Chain analysis (primary & support activities)
- **Org Structure Analyzer** - Leadership, structure, decision-making, organizational health

✅ **Phase 2 Skills** (Strategy Analysis - 10 Skills):
- **SWOT Analysis** - Strengths, weaknesses, opportunities, threats + TOWS matrix + prioritization
- **Porter's Five Forces** - Industry attractiveness across all 5 competitive forces
- **PESTEL Analysis** - Macro-environmental analysis (Political, Economic, Social, Tech, Environmental, Legal)
- **BCG Matrix** - Portfolio analysis (Stars, Cash Cows, Question Marks, Dogs)
- **Ansoff Matrix** - Growth strategies (Market Penetration, Development, Product Dev, Diversification)
- **Value Proposition Canvas** - Product-market fit analysis (Customer jobs, pains, gains)
- **McKinsey 7S Framework** - Organizational effectiveness (Strategy, Structure, Systems, Values, Style, Staff, Skills)
- **Functional Strategy** - Department-level strategies (Sales, Marketing, Product, Ops, Finance, HR, IT)
- **Competitive Strategy** - Positioning, differentiation, competitive advantages (moats)
- **Sales Intelligence** - ICP, account targeting, sales playbooks, battlecards, messaging

✅ **Report Generation**:
- Professional markdown reports with executive summary
- JSON output for programmatic access
- State persistence for recovery

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file with your API keys:

```bash
cp env.example .env
```

Then edit `.env` and add your keys:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional (recommended for better website scraping)
FIRECRAWL_API_KEY=fc-...
```

**Minimum requirement**: You only need `ANTHROPIC_API_KEY` to get started. The system will work without Firecrawl (using fallback scraping).

### 3. Configure Your Analysis

The `config.yaml` file comes pre-configured with Stripe as an example. You can use it as-is or modify it:

```yaml
company:
  name: "Stripe"
  website: "https://stripe.com"
  industry: "Financial Technology"

goals:
  primary: "Identify growth opportunities in enterprise segment"

scope:
  phase1_depth: "comprehensive"
  phase2_frameworks:
    - "SWOT Analysis"
    - "Porter's Five Forces"

competitors:
  - "Square"
  - "Adyen"
  - "PayPal"
  - "Braintree"
```

### 4. Run Your First Analysis

```bash
python main.py
```

## What Will Happen

When you run BCOS, it will:

1. **Initialize**: Load config, set up orchestrator
2. **Phase 1 - Foundation Building** (6 skills):
   - Gather company intelligence (scrape website, analyze business)
   - Build Business Model Canvas (9 building blocks)
   - Research market landscape (size, growth, trends, opportunities)
   - Profile competitors (positioning, strengths, weaknesses, threats)
   - Map value chain (primary & support activities)
   - Analyze organizational structure (leadership, decision-making, culture)
3. **Phase 2 - Strategy Analysis** (10 frameworks):
   - SWOT Analysis (+ TOWS matrix and strategic implications)
   - Porter's Five Forces (industry attractiveness assessment)
   - PESTEL Analysis (macro-environmental factors)
   - BCG Matrix (portfolio analysis)
   - Ansoff Matrix (growth strategies)
   - Value Proposition Canvas (product-market fit)
   - McKinsey 7S (organizational effectiveness)
   - Functional Strategy (department-level strategies)
   - Competitive Strategy (positioning & moats)
   - Sales Intelligence (playbooks & battlecards)
4. **Generate Reports**: Create markdown report and save JSON data
5. **Save State**: Persist state for potential recovery

## Understanding the Output

After running, you'll find:

```
outputs/
└── Stripe/
    ├── analysis_20241022_143022.json    # Full analysis results (JSON)
    ├── report_20241022_143022.md        # Executive report (Markdown)
    ├── state_20241022_143022.json       # State for recovery
    └── logs/
        └── bcos_20241022_143022.log     # Debug logs (if enabled)
```

### Markdown Report

The `report_*.md` file contains a professionally formatted executive report with:

- **Executive Summary**: Company overview and key findings
- **Phase 1 Foundation**:
  - Company Intelligence
  - Business Model Canvas
  - Market Intelligence
  - Competitor Intelligence
- **Phase 2 Strategy**:
  - SWOT Analysis
  - Porter's Five Forces
- **Strategic Recommendations**
- **Appendix**: Methodology and metadata

Open it in any markdown viewer or text editor.

### JSON Analysis Data

The `analysis_*.json` file contains complete structured data:

```json
{
  "company": "Stripe",
  "phase1": {
    "company_intelligence": {
      "business_description": "Payment infrastructure for the internet...",
      "products_services": ["Payment processing", "Stripe Terminal", ...],
      "value_proposition": "Developer-friendly APIs...",
      "key_facts": {...}
    },
    "business_model_canvas": {
      "customer_segments": [...],
      "value_propositions": [...],
      "revenue_streams": [...],
      "key_resources": {...},
      "key_partnerships": [...]
    },
    "market_intelligence": {
      "market_size": {"tam": {...}, "growth_rate_cagr": "12%"},
      "trends": [...],
      "opportunities": [...],
      "competitive_dynamics": {...}
    },
    "competitor_intelligence": {
      "competitor_profiles": [...],
      "competitive_landscape": {...},
      "competitive_positioning_map": {...}
    }
  },
  "phase2": {
    "swot": {
      "strengths": [...],
      "weaknesses": [...],
      "opportunities": [...],
      "threats": [...],
      "tows_matrix": {...},
      "prioritization": {...},
      "strategic_implications": [...]
    },
    "porters_five_forces": {
      "threat_of_new_entrants": {...},
      "supplier_power": {...},
      "buyer_power": {...},
      "threat_of_substitutes": {...},
      "competitive_rivalry": {...},
      "overall_assessment": {
        "industry_attractiveness": "moderately-attractive",
        "attractiveness_score": 7
      }
    }
  },
  "summary": {
    "company": "Stripe",
    "current_phase": "complete",
    "tasks": {"total": 6, "completed": 6, "failed": 0}
  }
}
```

## Current Capabilities - What Actually Works

### Fully Implemented ✅

1. **Company Intelligence**
   - Real website scraping with Firecrawl
   - Fallback to BeautifulSoup if needed
   - LLM analysis of website content
   - Business description, products, value proposition extraction

2. **Business Model Canvas**
   - All 9 building blocks analyzed
   - Customer segments identified
   - Value propositions mapped
   - Revenue streams and cost structure
   - BMC archetype classification

3. **Market Intelligence**
   - TAM/SAM/SOM market sizing
   - Market trends identification
   - Opportunity mapping
   - Competitive dynamics assessment
   - Growth projections

4. **Competitor Intelligence**
   - Multi-competitor profiling
   - Strengths and weaknesses analysis
   - Market positioning
   - Threat assessment
   - Competitive positioning maps

5. **SWOT Analysis**
   - Comprehensive SWOT across all dimensions
   - TOWS matrix (strategic initiatives)
   - Prioritization of items
   - Strategic implications
   - Recommended focus areas

6. **Porter's Five Forces**
   - All 5 forces analyzed in depth
   - Barriers to entry assessment
   - Industry attractiveness rating
   - Strategic recommendations per force

7. **Professional Reports**
   - Executive-quality markdown reports
   - Structured JSON output
   - State persistence

### Coming Soon 🔜

- Additional data sources (Exa for semantic search, Crunchbase, News APIs)
- PDF/DOCX/PPTX report generation
- Additional strategy frameworks (Blue Ocean Strategy, Scenario Planning)
- Automated OKR/KPI recommendations
- Web UI for interactive analysis
- V2: AI Opportunity Assessment (12-agent system for identifying AI automation opportunities)

## Testing the System

### Test 1: Basic Execution

Run with default Stripe config:

```bash
python main.py
```

**Expected**:
- System completes Phase 1 (4 tasks) and Phase 2 (2 tasks)
- Generates JSON analysis and markdown report
- Takes 2-5 minutes depending on API speed

### Test 2: Your Own Company

Edit `config.yaml`:

```yaml
company:
  name: "YourCompany"
  website: "https://yourcompany.com"
  industry: "Your Industry"

competitors:
  - "Competitor1"
  - "Competitor2"
```

Run again:

```bash
python main.py
```

### Test 3: Enable Debug Logging

Edit `config.yaml`:

```yaml
advanced:
  debug: true
```

This creates detailed logs in `outputs/logs/` for troubleshooting.

## Troubleshooting

### "No module named 'anthropic'"

Install dependencies:

```bash
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not set"

Create `.env` file with your API key:

```bash
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env
```

### "Firecrawl not available"

This is just a warning. The system will use fallback scraping. To enable Firecrawl:

```bash
pip install firecrawl-py
# Add FIRECRAWL_API_KEY to .env
```

### Tasks are failing validation

Check the logs (enable debug mode) to see why. Validation can be adjusted in `core/validator.py` if needed.

### Analysis seems incomplete

Check `outputs/[company]/analysis_*.json` to see:
- Which tasks completed successfully
- Any error messages in task results
- Whether fallback methods were used

## Next Steps

### Extend the System

1. **Add More Skills**:
   - Create new skill modules in `skills/phase1_foundation/` or `skills/phase2_strategy/`
   - Follow the pattern from existing skills
   - Each skill needs `__init__.py` with `execute()` function and `SKILL.md` documentation

2. **Add Data Sources**:
   - Create new clients in `data_sources/scrapers/` or `data_sources/apis/`
   - Integrate Exa for semantic search
   - Add Crunchbase for financial data
   - Connect news APIs for recent developments

3. **Enhance Reports**:
   - Add PDF generation in `reports/pdf_report.py`
   - Create PowerPoint generation in `reports/pptx_report.py`
   - Build interactive dashboards

### Customize Analysis

- **Adjust task planning**: Edit prompts in `core/planner.py`
- **Modify validation**: Change criteria in `core/validator.py`
- **Add custom skills**: Create domain-specific analysis modules
- **Configure frameworks**: Update `config.yaml` to select which frameworks to apply

## Architecture Overview

```
main.py
  └─> BusinessContextOrchestrator
       ├─> Planner (creates task plan using LLM)
       │    └─> Phase 1: 4 tasks
       │    └─> Phase 2: 2+ tasks
       │
       ├─> Executor (runs tasks via skills)
       │    ├─> Company Intelligence
       │    ├─> Business Model Canvas
       │    ├─> Market Intelligence
       │    ├─> Competitor Intelligence
       │    ├─> SWOT Analyzer
       │    └─> Porter's Five Forces
       │
       ├─> Validator (checks completion)
       │    └─> Heuristic + LLM validation
       │
       └─> StateManager (tracks context)
            └─> Passes Phase 1 → Phase 2

Reports Generated:
  - JSON (analysis_*.json)
  - Markdown (report_*.md)
```

## What You'll Accomplish

By running BCOS, you'll:

1. ✅ Gather comprehensive company intelligence
2. ✅ Understand the business model in depth
3. ✅ Map the market landscape and opportunities
4. ✅ Profile key competitors
5. ✅ Analyze value chain and organizational structure
6. ✅ Apply 10 strategic frameworks (SWOT, Porter's 5 Forces, PESTEL, BCG Matrix, Ansoff, VPC, McKinsey 7S, etc.)
7. ✅ Develop functional strategies for each department
8. ✅ Create competitive positioning and moat analysis
9. ✅ Generate sales playbooks and battlecards
10. ✅ Produce executive-quality reports with actionable recommendations

All with a single command, delivering McKinsey-level analysis!

## Real-World Use Cases

- **Investment Analysis**: Evaluate potential investment targets
- **Competitive Intelligence**: Understand competitive landscape
- **Market Research**: Size markets and identify opportunities
- **Strategic Planning**: Generate strategy frameworks
- **Due Diligence**: Comprehensive company analysis
- **Market Entry**: Assess new markets before entry

## Getting Help

- **Documentation**: See ARCHITECTURE.md for system design
- **Implementation Guide**: See CLAUDE_CODE_INSTRUCTIONS.md
- **Project Context**: See CLAUDE.md
- **Skill Docs**: Check `SKILL.md` files in each skill directory

---

**Happy Analyzing! 🚀**

The system is production-ready with **16 implemented skills** covering the most important business analysis frameworks including Porter's Value Chain, BCG Matrix, Ansoff Matrix, Value Proposition Canvas, McKinsey 7S, Functional Strategy, Competitive Strategy, and Sales Intelligence. You can run comprehensive McKinsey-level analyses right now!
