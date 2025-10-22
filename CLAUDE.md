# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Business Context OS (BCOS) is an autonomous multi-agent business research and strategy system that transforms Claude into a McKinsey-level strategy consultant. The system:

1. **Phase 1 - Foundation**: Builds comprehensive business context from a company name
2. **Phase 2 - Strategy**: Applies professional strategy frameworks and generates intelligence
3. **Report Generation**: Creates executive-quality outputs in multiple formats

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Then edit .env with your API keys

# Run the system
python main.py
```

### Testing
```bash
# Run tests (when test suite is implemented)
pytest

# Run tests with coverage
pytest --cov=core --cov=skills --cov=data_sources
```

### Configuration
Edit `config.yaml` to:
- Set target company name and website
- Define research goals
- Select strategic frameworks to apply
- Configure data sources and output preferences

## System Architecture

### Dexter-Inspired Multi-Agent Design

The core architecture is heavily inspired by [Dexter](https://github.com/virattt/dexter), implementing a multi-agent pattern:

```
Planning Agent → Action Agent → Validation Agent → Answer Agent
```

**Key architectural patterns adopted from Dexter:**
- Task decomposition: Break complex queries into discrete, executable tasks
- Dynamic tool selection: Let LLM choose appropriate tools, don't hardcode
- Validation loops: Verify task completion before proceeding
- Loop prevention: Detect and break infinite loops with step limits
- Session context: Maintain rich context across task execution

### Two-Phase Workflow

**Phase 1 - Foundation Building** (main.py:123-142):
1. Gather company intelligence (website scraping, APIs)
2. Build Business Model Canvas
3. Map value chain
4. Analyze organizational structure
5. Research market landscape
6. Profile competitors

**Phase 2 - Strategy Application** (main.py:143-163):
1. Apply strategic frameworks (SWOT, Porter's Five Forces, BCG Matrix, etc.)
2. Generate competitive intelligence
3. Create sales playbooks for target prospects
4. Develop KPI/OKR recommendations

### Skills-Based Modularity

Each capability is a self-contained "skill" with:
- `SKILL.md`: Instructions for Claude on methodology
- `scripts/`: Python implementation code
- `references/`: Domain knowledge and examples

**Target Structure:**
```
skills/
├── orchestrator/              # Main orchestration logic
├── phase1-foundation/         # Business context building
│   ├── company-intelligence/
│   ├── business-model-canvas/
│   ├── value-chain-mapper/
│   ├── org-structure-analyzer/
│   ├── market-intelligence/
│   └── competitor-intelligence/
└── phase2-strategy/           # Strategy frameworks
    ├── strategy-frameworks/   # SWOT, Porter's, BCG, etc.
    ├── functional-strategy/
    ├── competitive-strategy/
    └── sales-intelligence/
```

## Core Components

### Orchestrator (`core/orchestrator.py` - TO BE IMPLEMENTED)

Main agent that coordinates the entire system:
- `plan_phase1_tasks()`: Decompose foundation-building into tasks
- `plan_phase2_tasks()`: Decompose strategy analysis into tasks
- `execute_task()`: Execute individual tasks using appropriate skills
- `validate_task_completion()`: Verify task completion before proceeding
- `generate_reports()`: Synthesize findings into professional outputs

### Data Sources Layer (`data_sources/`)

Unified interface for business intelligence gathering:
- **Firecrawl**: Deep website crawling and scraping
- **Exa**: Semantic search for company intelligence
- **Crunchbase**: Company data and financials
- **Twitter/X**: Real-time market signals
- **SEC Filings**: Public company data
- **News APIs**: Recent developments and press

### State Management

The system maintains context between phases:
- Phase 1 outputs → stored context dictionary
- Phase 2 reads context → applies frameworks → generates insights
- All results stored for report generation

## Safety Features

### Loop Prevention (from Dexter)
```python
# Track recent actions to detect repetition
last_actions = []
action_sig = f"{tool_name}:{args}"
last_actions.append(action_sig)

# If repeating same action, abort
if len(last_actions) > 4 and len(set(last_actions[-4:])) == 1:
    logger.warning("Loop detected - aborting task")
    break
```

### Step Limits (config.yaml:104-108)
- `max_steps: 50`: Global safety limit
- `max_steps_per_task: 10`: Per-task limit
- Prevents runaway execution

### Task Validation
After executing tools, validate completion:
```python
if self.validate_task_completion(task, outputs):
    task.done = True
    break
```

## Implementation Priority

When building this system:

1. **Start with core orchestrator** - Get the Dexter-style multi-agent loop working
2. **Build one complete skill** - Prove the skills pattern works end-to-end
3. **Add data sources incrementally** - Start with Firecrawl + Exa
4. **Test Phase 1 → Phase 2 flow** - Ensure context passing works
5. **Add frameworks gradually** - Begin with SWOT, then expand
6. **Reports come last** - Get analysis working before formatting

## Current Status

**Stage**: Initial setup - Repository structure and core files in place

**Implemented:**
- Configuration schema (config.yaml)
- Entry point skeleton (main.py)
- Documentation (README, ARCHITECTURE, this file)
- Dependency specifications (requirements.txt)

**To Be Implemented:**
- Core orchestrator and multi-agent system
- Skills framework and individual skills
- Data source integrations
- Report generation system
- Testing suite

## Key Design Decisions

1. **Skills vs Hard-coded**: Use skills for flexibility and extensibility
2. **LLM Selects Tools**: Don't hardcode tool selection (Dexter pattern)
3. **Two-Phase Architecture**: Separate data gathering from analysis
4. **Validation at Each Step**: Prevent incomplete work from propagating
5. **Rich Context Passing**: Each phase gets full context from previous phase

## Configuration Schema

The `config.yaml` file drives the entire system:

- **company**: Target company name, website, industry
- **goals**: Primary and secondary research objectives
- **scope**: Analysis depth and frameworks to apply
- **competitors**: List of competitors for competitive analysis
- **target_prospects**: Companies for sales intelligence
- **data_sources**: Which APIs/scrapers to enable
- **output**: Report formats, detail level, visualization preferences
- **advanced**: Safety limits, debugging, caching

## References

- **ARCHITECTURE.md**: Complete system design and patterns
- **CLAUDE_CODE_INSTRUCTIONS.md**: Detailed implementation guidance
- **README (3).md**: Project vision and use cases
- **Dexter**: https://github.com/virattt/dexter - Inspiration for multi-agent design
