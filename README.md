# Business Context OS

> Autonomous McKinsey-level business research and strategy system powered by Claude AI

## 🎯 Vision

Business Context OS transforms Claude Code into an autonomous strategy consultant that:

1. **Builds complete business context** ("all the chess pieces")
   - Business Model Canvas
   - Value Chain Map
   - Org Structure & Capabilities
   - Market Position & Competitive Landscape

2. **Applies expert strategy frameworks**
   - SWOT, Porter's Five Forces, BCG Matrix, Blue Ocean Strategy
   - Functional strategies (Marketing, Sales, Product, Operations)

3. **Generates actionable intelligence**
   - Competitive analysis to outcompete rivals
   - Sales playbooks for target prospects
   - KPI/OKR recommendations

## 🏗️ System Architecture

```
User Input (config.yaml)
    ↓
Phase 1: Build Business Context (Foundation)
    → Company Intelligence
    → Business Model Canvas
    → Value Chain Mapping
    → Org Structure Analysis
    → Market & Competitive Intelligence
    ↓
Phase 2: Apply Strategy Frameworks (Analysis)
    → Strategic Frameworks (SWOT, Porter's, etc.)
    → Functional Strategies (Marketing, Sales, Product)
    → Competitive Intelligence
    → Sales Intelligence
    ↓
Output: Comprehensive Reports + Actionable Recommendations
```

## 📁 Target Repository Structure

```
business-context-os/
├── README.md                          # This file
├── ARCHITECTURE.md                    # Detailed system design
├── config.yaml                        # User configuration
├── main.py                            # Entry point
├── requirements.txt                   # Dependencies
│
├── skills/                            # Modular skill system
│   ├── orchestrator/                  # Main orchestration
│   ├── phase1-foundation/             # Business context building
│   │   ├── business-model-canvas/
│   │   ├── value-chain-mapper/
│   │   ├── org-structure-analyzer/
│   │   ├── company-intelligence/
│   │   ├── market-intelligence/
│   │   └── competitor-intelligence/
│   │
│   ├── phase2-strategy/               # Strategy frameworks
│   │   ├── strategy-frameworks/
│   │   │   ├── swot-analyzer/
│   │   │   ├── porters-five-forces/
│   │   │   ├── bcg-matrix/
│   │   │   └── ... (8+ frameworks)
│   │   ├── functional-strategy/
│   │   ├── competitive-strategy/
│   │   └── sales-intelligence/
│   │
│   └── synthesis/                     # Report generation
│       ├── report-generator/
│       └── insight-synthesizer/
│
├── data_sources/                      # Data gathering
│   ├── scrapers/
│   │   ├── firecrawl_client.py
│   │   ├── exa_client.py
│   │   └── ... (other scrapers)
│   └── apis/
│       └── ... (API integrations)
│
├── core/                              # Core system logic
│   ├── orchestrator.py
│   ├── planner.py
│   ├── executor.py
│   └── state_manager.py
│
├── outputs/                           # Generated reports (gitignored)
└── tests/                             # Test suite
```

## 🚀 Quick Start (Once Built)

### Prerequisites
- Python 3.10+
- Claude Code or Claude API access
- API keys for data sources (optional but recommended)

### Installation
```bash
git clone https://github.com/yourusername/business-context-os.git
cd business-context-os
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
```

### Configuration
Edit `config.yaml`:
```yaml
company:
  name: "Stripe"
  website: "https://stripe.com"
  
goals:
  primary: "Identify growth opportunities in enterprise segment"
```

### Run
```bash
# With Claude Code (auto-detects and runs)
claude-code

# Or manually
python main.py
```

## 🎨 Inspired By

This project draws architectural inspiration from:
- **[Dexter](https://github.com/virattt/dexter)**: Multi-agent task planning and autonomous execution
- **Anthropic Skills Framework**: Modular, reusable capability system
- **McKinsey & BCG Frameworks**: Professional strategy methodologies

## 📚 Key Design Patterns

### Multi-Agent Architecture (from Dexter)
- **Planning Agent**: Breaks queries into structured tasks
- **Action Agent**: Selects and executes appropriate tools
- **Validation Agent**: Verifies task completion
- **Answer Agent**: Synthesizes findings

### Skills-Based Modularity
- Each capability is a self-contained skill with:
  - `SKILL.md`: Instructions and methodology
  - `scripts/`: Implementation code
  - `references/`: Domain knowledge and examples

### Two-Phase Design
1. **Phase 1 - Foundation**: Build complete business understanding
2. **Phase 2 - Application**: Apply frameworks and generate intelligence

## 🛠️ Development Status

**Current Stage**: Initial setup - repository structure and core files needed

**Next Steps for Claude Code**:
1. Create complete directory structure
2. Implement core orchestrator
3. Build Phase 1 foundation skills
4. Build Phase 2 strategy skills
5. Integrate data sources (Firecrawl, Exa, etc.)
6. Create report generation system

## 📝 Use Cases

### Internal Strategy
```yaml
goals:
  primary: "Develop 3-year growth strategy"
```

### Competitive Intelligence
```yaml
competitors: ["Square", "Adyen", "PayPal"]
goals:
  primary: "Analyze positioning and identify weaknesses"
```

### Sales Intelligence
```yaml
target_prospects:
  - company: "Walmart"
    goal: "Craft value proposition for payment infrastructure"
```

## 🤝 Contributing

This is an autonomous agent system designed to be extended with new:
- Strategic frameworks
- Data sources
- Analysis capabilities
- Report formats

See `CONTRIBUTING.md` (to be created)

## 📄 License

MIT License - See `LICENSE` file

---

**Built for CEOs, Board Members, Strategy Consultants, and Sales Teams**

*Autonomous. Intelligent. Action-Oriented.*
