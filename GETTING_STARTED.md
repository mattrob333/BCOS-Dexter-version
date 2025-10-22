# Getting Started with BCOS

Welcome! This guide will help you set up and run your first business analysis with BCOS.

## What's Been Implemented

✅ **Core System** (Ready to use):
- Multi-agent orchestrator with Dexter-inspired architecture
- Task planning, execution, and validation
- State management and context passing
- Loop detection and safety limits

✅ **Data Sources**:
- Firecrawl client (with fallback to requests/BeautifulSoup)

✅ **Skills**:
- Company Intelligence skill (Phase 1)
- More skills will use LLM fallback until implemented

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
    # Add more frameworks as skills are implemented
```

### 4. Run Your First Analysis

```bash
python main.py
```

## What Will Happen

When you run BCOS, it will:

1. **Initialize**: Load config, set up orchestrator
2. **Phase 1**: Plan and execute foundation-building tasks
   - Gather company intelligence (using the company-intelligence skill)
   - Other Phase 1 tasks will use LLM fallback
3. **Phase 2**: Plan and execute strategy analysis
   - All Phase 2 tasks currently use LLM fallback
4. **Save Results**: Output analysis to `outputs/[company-name]/`

## Understanding the Output

After running, you'll find:

```
outputs/
└── Stripe/
    ├── analysis_20241022_143022.json    # Full analysis results
    ├── state_20241022_143022.json       # State for recovery
    └── logs/
        └── bcos_20241022_143022.log     # Debug logs (if enabled)
```

### Analysis Results

The `analysis_*.json` file contains:

```json
{
  "company": "Stripe",
  "phase1": {
    "company_intelligence": {
      "business_description": "...",
      "products_services": [...],
      "value_proposition": "...",
      ...
    }
  },
  "phase2": {
    "swot": {...},
    ...
  },
  "summary": {
    "company": "Stripe",
    "current_phase": "phase2",
    "tasks": {
      "total": 8,
      "completed": 7,
      "failed": 1
    }
  }
}
```

## Current Capabilities

### What Works Now

- ✅ Task planning using LLM
- ✅ Task execution with loop detection
- ✅ Task validation
- ✅ Company intelligence gathering (with web scraping)
- ✅ LLM fallback for unimplemented skills
- ✅ State persistence and recovery
- ✅ JSON output

### What Uses LLM Fallback

Most skills aren't implemented yet, so the system will use the LLM's knowledge to accomplish tasks. This means:

- ✅ The system will complete the analysis
- ⚠️ Results will be based on LLM knowledge, not real-time data
- ℹ️ Results are marked with `"_fallback": true`

### Coming Soon

- 🔜 More Phase 1 skills (Business Model Canvas, Value Chain, etc.)
- 🔜 Phase 2 strategy skills (SWOT, Porter's, BCG Matrix, etc.)
- 🔜 More data sources (Exa, Crunchbase, News APIs)
- 🔜 Report generation (PDF, DOCX, PPTX)

## Testing the System

### Test 1: Basic Execution

Run with default Stripe config:

```bash
python main.py
```

Expected: System completes Phase 1 and Phase 2, saves results.

### Test 2: Your Own Company

Edit `config.yaml`:

```yaml
company:
  name: "YourCompany"
  website: "https://yourcompany.com"
  industry: "Your Industry"
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

This will create detailed logs in `outputs/logs/`.

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

Check the logs (enable debug mode) to see why validation is failing. The validator may be too strict - you can adjust validation logic in `core/validator.py`.

## Next Steps

1. **Add More Skills**: Implement additional Phase 1 and Phase 2 skills
2. **Add Data Sources**: Integrate Exa, Crunchbase, news APIs
3. **Report Generation**: Build PDF/DOCX/PPTX report generators
4. **Customize**: Adjust task planning, validation, or execution logic

## Getting Help

- **Documentation**: See ARCHITECTURE.md for system design
- **Implementation Guide**: See CLAUDE_CODE_INSTRUCTIONS.md
- **Project Context**: See CLAUDE.md

## Current Architecture

```
main.py
  └─> BusinessContextOrchestrator
       ├─> Planner (creates tasks using LLM)
       ├─> Executor (runs tasks via skills)
       ├─> Validator (checks completion)
       └─> StateManager (tracks context)

Skills are dynamically loaded from:
  skills/phase1_foundation/company_intelligence/
  skills/phase2_strategy/...
```

## What You've Accomplished

By running BCOS for the first time, you've:

1. ✅ Set up a multi-agent autonomous system
2. ✅ Executed intelligent task planning
3. ✅ Gathered real business intelligence
4. ✅ Applied strategic frameworks (via LLM)
5. ✅ Generated structured analysis output

The foundation is built - now you can expand with more skills and data sources!

---

**Happy Analyzing! 🚀**
