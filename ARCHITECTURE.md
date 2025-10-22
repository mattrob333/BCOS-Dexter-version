# Business Context OS - System Architecture

## Overview

Business Context OS is an autonomous multi-agent system that conducts McKinsey-level business research and strategic analysis. It uses a two-phase approach:

1. **Phase 1 - Foundation**: Build comprehensive business context
2. **Phase 2 - Application**: Apply strategic frameworks and generate intelligence

## Design Philosophy

### Inspired by Dexter's Multi-Agent Architecture

We adopt Dexter's proven patterns:

```python
# From Dexter: Task Planning → Execution → Validation → Answer
class Agent:
    def plan_tasks(self, query: str) -> List[Task]
    def ask_for_actions(self, task_desc: str) -> AIMessage
    def ask_if_done(self, task_desc: str, results: str) -> bool
    def _generate_answer(self, query: str, outputs: list) -> str
```

**Key Learnings from Dexter**:
- ✅ Break complex queries into discrete tasks
- ✅ Let LLM select tools dynamically (don't hardcode)
- ✅ Validate task completion before moving on
- ✅ Prevent infinite loops with step limits
- ✅ Optimize tool arguments based on task context
- ✅ Keep session context for continuity

### Enhanced for Business Research

Business Context OS extends this with:
- **Two-phase workflow**: Foundation → Strategy
- **Skills system**: Modular, reusable capabilities
- **Rich data sources**: Firecrawl, Exa, Twitter, Crunchbase, etc.
- **Strategic frameworks**: SWOT, Porter's, BCG, Blue Ocean, etc.
- **Report generation**: Professional outputs (PDF, DOCX, PPTX)

## Core Components

### 1. Orchestrator (`core/orchestrator.py`)

The main agent that coordinates the entire system.

```python
class BusinessContextOrchestrator:
    """
    Main orchestration engine - similar to Dexter's Agent class
    but specialized for business research.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.max_steps = 50  # Safety limit
        self.max_steps_per_phase = 25
        
    def execute_phase1_foundation(self, company_name: str) -> dict:
        """
        Phase 1: Build business context
        Returns comprehensive context dictionary
        """
        pass
        
    def execute_phase2_strategy(self, context: dict, goals: dict) -> dict:
        """
        Phase 2: Apply frameworks and generate intelligence
        Returns strategy analysis and recommendations
        """
        pass
        
    def generate_reports(self, context: dict, strategy: dict) -> list:
        """
        Generate professional reports in requested formats
        """
        pass
```

### 2. Skills System

Each capability is a self-contained "skill":

```
skills/
├── orchestrator/
│   └── SKILL.md          # Main orchestration instructions
│
├── phase1-foundation/
│   ├── company-intelligence/
│   │   ├── SKILL.md      # How to gather company data
│   │   └── scripts/
│   │       └── scrape_company.py
│   │
│   ├── business-model-canvas/
│   │   ├── SKILL.md      # BMC methodology
│   │   ├── scripts/
│   │   │   └── build_canvas.py
│   │   └── references/
│   │       └── bmc_examples.md
│   │
│   └── ... (other Phase 1 skills)
│
└── phase2-strategy/
    ├── strategy-frameworks/
    │   ├── swot-analyzer/
    │   │   ├── SKILL.md  # SWOT methodology
    │   │   └── scripts/
    │   └── ... (other frameworks)
    │
    └── ... (other Phase 2 skills)
```

**Skill Structure**:
- `SKILL.md`: Instructions for Claude on how to use this capability
- `scripts/`: Python implementations
- `references/`: Domain knowledge, examples, best practices

### 3. Data Sources Layer

Unified interface for all data gathering:

```python
# data_sources/scrapers/firecrawl_client.py
class FirecrawlClient:
    def scrape_company_website(self, url: str) -> dict:
        """Deep crawl company website for structured data"""
        pass

# data_sources/scrapers/exa_client.py
class ExaClient:
    def search_company_intelligence(self, company: str, query_type: str) -> dict:
        """Semantic search for business intelligence"""
        pass

# data_sources/apis/crunchbase_client.py
class CrunchbaseClient:
    def get_company_data(self, company: str) -> dict:
        """Fetch company data from Crunchbase"""
        pass
```

## Execution Flow

### Phase 1: Foundation Building

```
1. User provides company name in config.yaml
2. Orchestrator creates Phase 1 task plan:
   - Task 1: Scrape company website (Firecrawl)
   - Task 2: Search for company intelligence (Exa)
   - Task 3: Fetch company data (Crunchbase)
   - Task 4: Build Business Model Canvas
   - Task 5: Map Value Chain
   - Task 6: Analyze org structure
   - Task 7: Profile competitors
   - Task 8: Analyze market

3. For each task:
   a. Load appropriate skill (read SKILL.md)
   b. Execute skill scripts with data sources
   c. Validate completeness
   d. Store results in context

4. Output: Comprehensive business context dictionary
```

### Phase 2: Strategy Application

```
1. Orchestrator reads goals from config.yaml
2. Creates Phase 2 task plan based on goals:
   - Internal Strategy: Apply frameworks (SWOT, Porter's, etc.)
   - Competitive Intelligence: Deep competitor analysis
   - Sales Intelligence: Profile prospects, craft messaging
   - KPI/OKR Framework: Set performance targets

3. For each framework/analysis:
   a. Load appropriate skill
   b. Apply to business context
   c. Generate insights
   d. Store recommendations

4. Output: Strategic analysis and recommendations
```

### Report Generation

```
1. Synthesize all findings
2. Generate reports in requested formats:
   - Executive Summary (PDF)
   - Business Model Canvas (PDF with visual)
   - Value Chain Map (PDF with visual)
   - Strategic Framework Analyses (PDF)
   - Competitive Intelligence (PDF)
   - Sales Playbooks (PDF)
   - Full Report (DOCX)
   - Presentation (PPTX)

3. Save to outputs/[company-name]/
```

## Safety Features (from Dexter)

### Loop Prevention
```python
# Track recent actions
last_actions = []
action_sig = f"{tool_name}:{args}"
last_actions.append(action_sig)

# Detect loops
if len(last_actions) > 4 and len(set(last_actions)) == 1:
    logger.warning("Loop detected - aborting")
    return
```

### Step Limits
```python
max_steps = 50              # Global limit
max_steps_per_task = 10     # Per-task limit
max_steps_per_phase = 25    # Per-phase limit
```

### Task Validation
```python
# After executing tools, validate completion
if self.ask_if_done(task_desc, task_outputs):
    task.done = True
    logger.log_task_done(task_desc)
    break
```

## Configuration Schema

### `config.yaml`

```yaml
# Target Company
company:
  name: "Stripe"
  website: "https://stripe.com"
  industry: "Financial Technology"

# Research Goals
goals:
  primary: "Identify growth opportunities in enterprise segment"
  secondary:
    - "Analyze competitive positioning"
    - "Develop sales strategy for Fortune 500"

# Analysis Scope
scope:
  phase1_depth: "comprehensive"  # basic | standard | comprehensive
  phase2_frameworks:
    - "SWOT"
    - "Porter's Five Forces"
    - "Business Model Canvas"
    - "Blue Ocean Strategy"

# Competitors (for competitive analysis)
competitors:
  - "Square"
  - "Adyen"
  - "PayPal"

# Sales Intelligence
target_prospects:
  - company: "Walmart"
    goal: "Understand payment infrastructure needs"

# Data Sources
data_sources:
  firecrawl: true
  exa: true
  twitter: true
  crunchbase: true

# Output Preferences
output:
  formats: ["pdf", "docx", "pptx"]
  detail_level: "executive"  # executive | detailed | comprehensive
```

## Tech Stack

### Core
- **Python 3.10+**: Main language
- **LangChain**: LLM orchestration
- **Pydantic**: Data validation
- **PyYAML**: Configuration

### LLM
- **Anthropic Claude Sonnet 4**: Via Claude Code or API

### Data Sources
- **Firecrawl**: Deep website scraping
- **Exa**: Semantic search
- **Twitter/X API**: Real-time signals
- **Crunchbase**: Company data
- **SEC API**: Public filings
- **News APIs**: Recent developments

### Report Generation
- **python-docx**: Word documents
- **python-pptx**: PowerPoint presentations
- **ReportLab**: PDF generation
- **Matplotlib/Plotly**: Visualizations

## Development Roadmap

### Phase 0: Setup (Current)
- [ ] Create repository structure
- [ ] Set up core files
- [ ] Configure dependencies

### Phase 1: Core System
- [ ] Implement orchestrator
- [ ] Build planner and executor
- [ ] Add state management
- [ ] Create validation logic

### Phase 2: Foundation Skills
- [ ] Company intelligence skill
- [ ] Business Model Canvas skill
- [ ] Value Chain mapper skill
- [ ] Org structure analyzer skill
- [ ] Market intelligence skill
- [ ] Competitor intelligence skill

### Phase 3: Strategy Skills
- [ ] Strategic frameworks (SWOT, Porter's, etc.)
- [ ] Functional strategies (marketing, sales, product)
- [ ] Competitive strategy skill
- [ ] Sales intelligence skill
- [ ] KPI/OKR framework skill

### Phase 4: Data Integration
- [ ] Firecrawl client
- [ ] Exa client
- [ ] Twitter client
- [ ] Crunchbase client
- [ ] SEC filings client

### Phase 5: Reports
- [ ] Report generator skill
- [ ] Insight synthesizer skill
- [ ] PDF templates
- [ ] DOCX templates
- [ ] PPTX templates

### Phase 6: Polish
- [ ] Testing suite
- [ ] Documentation
- [ ] Example configs
- [ ] Demo video

## Key Implementation Notes

### For Claude Code

When implementing this system:

1. **Read Dexter's code first** - understand the multi-agent patterns
2. **Start with orchestrator** - get the core loop working
3. **Build one complete skill** - prove the pattern works
4. **Add data sources incrementally** - start with Firecrawl + Exa
5. **Test end-to-end early** - ensure Phase 1 → Phase 2 flow works
6. **Add frameworks gradually** - start with SWOT, then expand
7. **Reports come last** - get analysis working first

### Critical Design Decisions

1. **Skills vs Hard-coded**: Use skills for flexibility and modularity
2. **LLM selects tools**: Don't hardcode tool selection (learned from Dexter)
3. **Two-phase architecture**: Separate data gathering from analysis
4. **Validation at each step**: Prevent incomplete work from propagating
5. **Rich context passing**: Each phase gets full context from previous phase

## Success Metrics

A successful implementation should:

1. ✅ Accept company name → generate full analysis autonomously
2. ✅ Build comprehensive business context (Phase 1)
3. ✅ Apply 5+ strategic frameworks (Phase 2)
4. ✅ Generate professional reports (PDF, DOCX, PPTX)
5. ✅ Complete analysis in <30 minutes
6. ✅ Prevent infinite loops and runaway execution
7. ✅ Produce actionable, McKinsey-quality insights

---

**This architecture enables autonomous, high-quality business research at scale.**
