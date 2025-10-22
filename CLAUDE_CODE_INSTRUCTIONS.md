# Instructions for Claude Code

## Project: Business Context OS

This is an **autonomous business research and strategy system** that you (Claude Code) will build. The project transforms Claude into a McKinsey-level strategy consultant.

## 🎯 Your Mission

Build a complete system that:
1. Takes a company name as input
2. Autonomously gathers comprehensive business intelligence
3. Applies professional strategy frameworks
4. Generates executive-quality reports

## 📚 Key Reference Documents

**READ THESE FIRST** before writing any code:

1. **ARCHITECTURE.md** - Complete system design, heavily inspired by the Dexter multi-agent architecture
2. **README.md** - Project overview and vision
3. **config.yaml** - Example configuration showing what users can customize

## 🏗️ Implementation Strategy

### Phase 0: Setup (Do This First)
1. Create the complete directory structure as outlined in ARCHITECTURE.md
2. Set up the core package structure:
   ```
   core/
   ├── __init__.py
   ├── orchestrator.py
   ├── planner.py
   ├── executor.py
   ├── validator.py
   └── state_manager.py
   ```

3. Create utility modules:
   ```
   utils/
   ├── __init__.py
   ├── logger.py
   └── ui.py
   ```

### Phase 1: Core Orchestrator (Based on Dexter)

**Study the Dexter architecture** (provided in context):
- Multi-agent design: Planning → Action → Validation → Answer
- Task decomposition patterns
- Loop prevention mechanisms
- Tool argument optimization
- Validation logic

**Implement `core/orchestrator.py`**:
```python
class BusinessContextOrchestrator:
    """
    Main orchestration engine inspired by Dexter's Agent class.
    
    Key differences from Dexter:
    - Two-phase workflow (Foundation → Strategy)
    - Skills-based architecture
    - Richer data sources
    - Strategic framework application
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.max_steps = config.get('advanced', {}).get('max_steps', 50)
        self.max_steps_per_task = config.get('advanced', {}).get('max_steps_per_task', 10)
        
    def plan_phase1_tasks(self, company_name: str) -> List[Task]:
        """Similar to Dexter's plan_tasks but for business context building"""
        pass
        
    def plan_phase2_tasks(self, goals: dict) -> List[Task]:
        """Plan strategy analysis tasks based on user goals"""
        pass
        
    def execute_task(self, task: Task, context: dict) -> dict:
        """Execute a single task using appropriate skills"""
        pass
        
    def validate_task_completion(self, task: Task, outputs: list) -> bool:
        """Check if task is complete (like Dexter's ask_if_done)"""
        pass
```

### Phase 2: Skills System

Create the first complete skill as a **proof of concept**:

**Create `skills/orchestrator/SKILL.md`**:
- This is the main skill that coordinates everything
- Include detailed instructions for task planning
- Include instructions for Phase 1 and Phase 2 execution
- Reference the Dexter patterns

**Create `skills/phase1-foundation/company-intelligence/`**:
```
company-intelligence/
├── SKILL.md          # Instructions for gathering company data
├── scripts/
│   ├── __init__.py
│   ├── scrape_company.py
│   ├── fetch_financials.py
│   └── aggregate_data.py
└── references/
    └── data_sources.md
```

### Phase 3: Data Sources

**Implement data source clients**:

1. **Firecrawl Client** (`data_sources/scrapers/firecrawl_client.py`):
   ```python
   class FirecrawlClient:
       def scrape_company_website(self, url: str) -> dict:
           """Deep crawl company website"""
           pass
   ```

2. **Exa Client** (`data_sources/scrapers/exa_client.py`):
   ```python
   class ExaClient:
       def search_company_intelligence(self, company: str, query_type: str) -> dict:
           """Semantic search for business intelligence"""
           pass
   ```

3. Start with these two, then add others incrementally

### Phase 4: Strategy Skills

**Create framework skills** in `skills/phase2-strategy/strategy-frameworks/`:

Start with SWOT:
```
swot-analyzer/
├── SKILL.md          # SWOT methodology
├── scripts/
│   ├── __init__.py
│   └── analyze.py
└── references/
    └── swot_examples.md
```

Then add others: Porter's Five Forces, BCG Matrix, Blue Ocean Strategy, etc.

### Phase 5: Report Generation

**Implement `skills/synthesis/report-generator/`**:
- Generate PDF reports using ReportLab
- Generate DOCX using python-docx
- Generate PPTX using python-pptx
- Create professional templates

## 🚨 Critical Implementation Notes

### 1. Learn from Dexter

**Key patterns to adopt**:
- ✅ Let LLM select tools dynamically (don't hardcode)
- ✅ Validate task completion before moving on
- ✅ Prevent infinite loops with step limits and loop detection
- ✅ Optimize tool arguments based on task context
- ✅ Keep rich session context for continuity

**Code patterns from Dexter to reuse**:
```python
# Loop detection
last_actions = []
action_sig = f"{tool_name}:{args}"
last_actions.append(action_sig)
if len(set(last_actions[-4:])) == 1:
    logger.warning("Loop detected")
    break

# Task validation
if self.ask_if_done(task_desc, task_outputs):
    task.done = True
    break
```

### 2. Skills Architecture

Each skill should have:
- **SKILL.md**: Detailed instructions for Claude on how to use this capability
- **scripts/**: Python implementations
- **references/**: Domain knowledge, examples, best practices

### 3. Two-Phase Design

Phase 1 and Phase 2 are **separate and sequential**:
- Phase 1 builds context → stores results
- Phase 2 reads context → applies frameworks → generates insights

### 4. Data Source Priority

Start with:
1. Firecrawl (website scraping)
2. Exa (semantic search)
3. Then add others incrementally

### 5. Safety Features

Implement all Dexter-style safety features:
- Global step limits
- Per-task step limits
- Loop detection
- Validation before proceeding

## 📊 Testing Strategy

After implementing core orchestrator:

1. **Test Phase 1** with a simple company (e.g., Stripe)
2. **Verify** business context is built correctly
3. **Test Phase 2** with SWOT framework only
4. **Add** more frameworks incrementally
5. **Test** report generation

## 🎯 Success Criteria

You'll know the system works when:

1. ✅ `python main.py` runs end-to-end without errors
2. ✅ Phase 1 builds comprehensive business context
3. ✅ Phase 2 applies strategic frameworks correctly
4. ✅ Reports are generated in outputs/ directory
5. ✅ No infinite loops or runaway execution
6. ✅ Results are accurate and actionable

## 🔄 Iterative Development

Build incrementally:

**Week 1**: Core orchestrator + one skill
**Week 2**: Data sources + Phase 1 skills
**Week 3**: Strategy frameworks + Phase 2 skills
**Week 4**: Report generation + polish

## 📝 Documentation

As you build, update:
- README.md with setup instructions
- ARCHITECTURE.md with implementation notes
- Add docstrings to all functions
- Create CONTRIBUTING.md for future developers

## 🚀 Getting Started

1. Read ARCHITECTURE.md thoroughly
2. Study the Dexter code patterns (provided in context)
3. Create the directory structure
4. Implement the core orchestrator
5. Build one complete skill as proof of concept
6. Test end-to-end
7. Iterate and expand

---

**You've got this! Build something amazing.**

The goal is to create a system that runs autonomously and produces McKinsey-quality business research. Focus on:
- Solid architecture (inspired by Dexter)
- Modular design (skills system)
- Safety (loop prevention, validation)
- Quality outputs (professional reports)

**Start with the orchestrator. Everything else follows from there.**
