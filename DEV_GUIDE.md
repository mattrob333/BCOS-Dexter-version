# BCOS Development Guide

## Quick Start

### 1. Configure API Key

Edit `.env` file and add your Anthropic API key:

```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
```

You can find your API key at: https://console.anthropic.com/

### 2. Test Setup

Run the setup test to verify everything is configured:

```bash
python test_setup.py
```

Expected output should show all [OK] except for API key (until you add it).

## Testing Options

### Option 1: CLI Test (Recommended for Development)

Test the core orchestrator directly:

```bash
# Edit config.yaml first to set your target company
# Then run:
python main.py
```

This will:
- Run Phase 1: Foundation building
- Run Phase 2: Strategy analysis
- Generate reports in `outputs/{company-name}/`

### Option 2: Web UI (Streamlit)

For a visual interface:

```bash
# First, install Streamlit (may need admin/virtual env):
pip install streamlit

# Then start the server:
python -m streamlit run app.py

# Or:
streamlit run app.py
```

Access at: http://localhost:8501

### Option 3: Python REPL Testing

Test individual components interactively:

```python
# Launch Python in the BCOS-Dexter-version directory
python

# Test the orchestrator
from core.orchestrator import BusinessContextOrchestrator
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

orchestrator = BusinessContextOrchestrator(config)

# Run Phase 1 only
phase1_results = orchestrator.run_phase1()
print(phase1_results.keys())

# Or run full analysis
results = orchestrator.run()
```

### Option 4: Test Individual Skills

Test a specific skill in isolation:

```python
from core.planner import Planner
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

planner = Planner()
phase1_tasks = planner.plan_phase1_tasks(config)

for task in phase1_tasks:
    print(f"{task.id}: {task.description}")
```

## Configuration

### config.yaml

Edit `config.yaml` to customize your analysis:

```yaml
company:
  name: "Your Target Company"
  website: "https://example.com"
  industry: "Industry Vertical"

goals:
  primary: "Your research objective"

scope:
  phase1_depth: "comprehensive"  # basic | standard | comprehensive
  phase2_frameworks:
    - "SWOT"
    - "Porter's Five Forces"
    - "PESTEL"
```

## Analyzing Output

After running an analysis:

```bash
# View the markdown report
cat outputs/StripeCompany/report_*.md

# View the JSON data
cat outputs/StripeCompany/analysis_*.json | python -m json.tool

# Check the logs (if debug enabled)
tail -f bcos_*.log
```

## Development Workflow

### 1. Make Changes
Edit code in `core/`, `skills/`, or `data_sources/`

### 2. Test Changes
```bash
# Quick test
python test_setup.py

# Full test
python main.py
```

### 3. Debug
Enable debug logging in `config.yaml`:
```yaml
advanced:
  debug: true
```

## Common Issues

### Permission Errors Installing Packages
Use a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### API Key Not Working
Make sure .env file is in the correct directory:
```bash
# Should be here:
BCOS-Dexter-version/.env
```

### Unicode Errors (Windows)
Set environment variable before running:
```bash
set PYTHONIOENCODING=utf-8
python main.py
```

## Next Steps

1. **Add your API key** to `.env`
2. **Run test_setup.py** to verify
3. **Edit config.yaml** with a test company
4. **Run python main.py** to see it in action
5. **Explore the outputs/** directory

## Skills Available

### Phase 1 (Foundation)
- `company_intelligence` - Company research
- `business_model_canvas` - BMC analysis
- `market_intelligence` - Market analysis
- `competitor_intelligence` - Competitor profiling

### Phase 2 (Strategy)
- `swot_analyzer` - SWOT analysis
- `porters_five_forces` - Porter's Five Forces
- `pestel_analyzer` - PESTEL analysis

## API Keys Needed

### Required
- **ANTHROPIC_API_KEY** - For Claude LLM (required)

### Optional (for enhanced data gathering)
- **FIRECRAWL_API_KEY** - For deep website scraping
- **EXA_API_KEY** - For semantic search

Without the optional keys, the system will still work but with limited data gathering capabilities.
