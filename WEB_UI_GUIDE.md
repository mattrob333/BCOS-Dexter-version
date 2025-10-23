# BCOS Web UI Guide

## Quick Start - Web Interface

The easiest way to use BCOS is through the Streamlit web interface.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file:

```bash
cp env.example .env
```

Edit `.env` and add your API key:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional (recommended)
FIRECRAWL_API_KEY=fc-your-key-here
EXA_API_KEY=your-exa-key-here
```

### 3. Launch Web UI

```bash
streamlit run app.py
```

This will open the BCOS web interface in your browser (usually http://localhost:8501).

## Using the Web UI

### New Analysis Tab

1. **Enter Company Information**:
   - Company Name (e.g., "Stripe")
   - Company Website (e.g., "https://stripe.com")
   - Industry (e.g., "Financial Technology")

2. **Optional: Add Context**:
   - Describe what you're looking for
   - Example: "Evaluate for Series B investment, focus on enterprise growth"

3. **Optional: List Competitors**:
   - One competitor per line
   - Example:
     ```
     Square
     Adyen
     PayPal
     ```

4. **Select Frameworks**:
   - ✅ SWOT Analysis (recommended)
   - ✅ Porter's Five Forces (recommended)
   - ⬜ PESTEL Analysis (optional)
   - ⬜ BCG Matrix (coming soon)

5. **Click "Run Analysis"**:
   - The system will run for 2-5 minutes
   - Progress bar shows current phase
   - Results display when complete

### Viewing Results

After analysis completes, you'll see:

1. **Summary Metrics**:
   - Company name
   - Analysis phase
   - Tasks completed
   - Status

2. **Download Options**:
   - 📄 JSON (structured data)
   - 📝 Markdown (executive report)
   - 📊 PDF (coming soon)
   - 📑 DOCX (coming soon)

3. **Inline Report**:
   - Executive summary
   - Phase 1 foundation
   - Phase 2 strategy
   - Recommendations

### Past Analyses Tab

- View all previous analyses
- Grouped by company
- Click "View Report" to see past results
- Each analysis has a unique session ID

### About Tab

- Learn about BCOS capabilities
- View architecture overview
- Understand use cases

## Output Organization

All analyses are saved to:

```
outputs/
└── {company-slug}/
    └── {session-id}/
        ├── analysis.json      # Full structured data
        ├── report.md          # Executive report
        ├── state.json         # System state
        ├── report.pdf         # PDF report (coming soon)
        └── report.docx        # Word report (coming soon)
```

### Session IDs

Each analysis gets a unique 8-character session ID (e.g., `a1b2c3d4`). This ensures:
- ✅ Multiple analyses of the same company don't conflict
- ✅ You can compare analyses over time
- ✅ Clean separation between runs

## Key Features

### Reusability

- Analyze ANY company without modifying code
- No hard-coded company names
- Each analysis is isolated
- Core system remains clean

### Session Management

- Each analysis creates a new session
- Outputs organized by company + session
- Manifest tracks all analyses
- Easy to find and compare past work

### Clean Workflow

1. **Input** → Company URL + context
2. **Process** → Autonomous multi-agent analysis
3. **Output** → Reports in multiple formats
4. **View** → Inline or download
5. **Reuse** → Run again for any company

## Tips

### For Best Results

1. **Provide Context**: The more context you provide, the better the analysis
2. **List Competitors**: Helps with competitive intelligence
3. **Select Frameworks**: Choose frameworks relevant to your goals
4. **Review Inline**: Check the markdown report before downloading

### Multiple Companies

You can analyze multiple companies:
- Each gets its own directory
- Session IDs prevent conflicts
- Compare side-by-side using Past Analyses

### Comparing Over Time

Analyze the same company multiple times to:
- Track market changes
- See strategic evolution
- Compare before/after major events

## Troubleshooting

### Web UI Won't Start

```bash
# Make sure Streamlit is installed
pip install streamlit

# Check for port conflicts
streamlit run app.py --server.port 8502
```

### Analysis Fails

- Check `.env` has `ANTHROPIC_API_KEY`
- Ensure company website is accessible
- Check logs in terminal for errors
- Try again with debug mode

### Can't Find Past Analyses

- Check `outputs/` directory exists
- Look for `outputs/manifest.json`
- Each company creates a slug (e.g., "stripe" from "Stripe")

## Command Line Alternative

You can still use the CLI if preferred:

```bash
# Edit config.yaml with company details
python main.py
```

But the web UI is recommended for:
- Easier input
- Better visualization
- Session management
- Download capabilities

## Advanced Usage

### Custom Output Directory

Edit `app.py` line 21:

```python
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager("custom/output/path")
```

### Multiple Concurrent Analyses

The web UI supports running multiple analyses:
- Open multiple browser tabs
- Each gets a unique session
- No conflicts

### API Integration

The session manager can be used programmatically:

```python
from utils.session_manager import SessionManager

sm = SessionManager()
session = sm.create_session("Stripe", "Investment analysis")
# ... run analysis ...
sm.update_session(session['session_id'], session['company_slug'], {'status': 'completed'})
```

## Next Steps

### After Your First Analysis

1. ✅ Review the markdown report
2. ✅ Download JSON for deeper inspection
3. ✅ Compare with competitors (run analyses for them too)
4. ✅ Share reports with your team

### Extend the System

- Add custom skills in `skills/`
- Integrate additional data sources
- Customize frameworks in `config.yaml`
- Build custom report formats

---

**The web UI makes BCOS accessible to anyone - no coding required!**
