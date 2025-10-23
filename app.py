"""
BCOS Streamlit Web UI.

Easy-to-use interface for running business context analyses.
"""

import streamlit as st
import yaml
import json
from pathlib import Path
from datetime import datetime
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import BusinessContextOrchestrator
from utils.session_manager import SessionManager, slugify
from utils.logger import setup_logger
from reports.markdown_report import generate_markdown_report

# Page config
st.set_page_config(
    page_title="BCOS - Business Context OS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()

if 'current_session' not in st.session_state:
    st.session_state.current_session = None

if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False


def main():
    """Main Streamlit app."""
    st.title("🎯 Business Context OS")
    st.markdown("**Autonomous Business Research & Strategy Analysis**")

    # Sidebar navigation
    page = st.sidebar.radio(
        "Navigation",
        ["New Analysis", "Past Analyses", "About"]
    )

    if page == "New Analysis":
        new_analysis_page()
    elif page == "Past Analyses":
        past_analyses_page()
    else:
        about_page()


def new_analysis_page():
    """Page for creating a new analysis."""
    st.header("Start New Analysis")

    with st.form("analysis_form"):
        st.subheader("Company Information")

        company_name = st.text_input(
            "Company Name *",
            placeholder="e.g., Stripe",
            help="Enter the company name you want to analyze"
        )

        company_website = st.text_input(
            "Company Website *",
            placeholder="e.g., https://stripe.com",
            help="Enter the company's website URL"
        )

        industry = st.text_input(
            "Industry *",
            placeholder="e.g., Financial Technology",
            help="Enter the industry vertical"
        )

        st.subheader("Analysis Configuration")

        user_context = st.text_area(
            "Context / Goals (Optional)",
            placeholder="e.g., Evaluate for Series B investment, focus on enterprise segment growth opportunities",
            help="Provide additional context about what you're looking for in this analysis",
            height=100
        )

        competitors = st.text_area(
            "Competitors (Optional)",
            placeholder="Enter competitor names, one per line",
            help="List key competitors to include in the analysis",
            height=100
        )

        # Framework selection
        st.subheader("Strategy Frameworks")
        col1, col2 = st.columns(2)

        with col1:
            swot = st.checkbox("SWOT Analysis", value=True)
            porters = st.checkbox("Porter's Five Forces", value=True)

        with col2:
            pestel = st.checkbox("PESTEL Analysis", value=False)
            bcg = st.checkbox("BCG Matrix", value=False, disabled=True, help="Coming soon")

        submitted = st.form_submit_button("🚀 Run Analysis", type="primary")

        if submitted:
            if not company_name or not company_website or not industry:
                st.error("Please fill in all required fields (Company Name, Website, Industry)")
                return

            run_analysis(
                company_name=company_name,
                company_website=company_website,
                industry=industry,
                user_context=user_context,
                competitors=[c.strip() for c in competitors.split('\n') if c.strip()],
                frameworks={
                    'swot': swot,
                    'porters': porters,
                    'pestel': pestel,
                    'bcg': bcg
                }
            )


def run_analysis(
    company_name: str,
    company_website: str,
    industry: str,
    user_context: str,
    competitors: list,
    frameworks: dict
):
    """Run the analysis."""
    # Create session
    session_manager = st.session_state.session_manager
    session = session_manager.create_session(company_name, user_context)

    st.session_state.current_session = session
    company_slug = session['company_slug']
    session_id = session['session_id']

    # Build config
    config = {
        'company': {
            'name': company_name,
            'website': company_website,
            'industry': industry
        },
        'goals': {
            'primary': user_context or f"Comprehensive analysis of {company_name}",
            'secondary': []
        },
        'scope': {
            'phase1_depth': 'comprehensive',
            'phase2_frameworks': []
        },
        'competitors': competitors,
        'advanced': {
            'debug': False,
            'max_steps': 50,
            'max_steps_per_task': 10
        }
    }

    # Add selected frameworks
    if frameworks.get('swot'):
        config['scope']['phase2_frameworks'].append('SWOT Analysis')
    if frameworks.get('porters'):
        config['scope']['phase2_frameworks'].append("Porter's Five Forces")
    if frameworks.get('pestel'):
        config['scope']['phase2_frameworks'].append('PESTEL Analysis')

    # Show progress
    progress_container = st.container()

    with progress_container:
        st.info(f"🔄 Running analysis for **{company_name}**...")
        st.markdown(f"Session ID: `{session_id}`")

        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Initialize orchestrator
            status_text.text("Initializing orchestrator...")
            progress_bar.progress(10)

            orchestrator = BusinessContextOrchestrator(config)

            # Run analysis
            status_text.text("Phase 1: Building business foundation...")
            progress_bar.progress(30)

            results = orchestrator.run()

            progress_bar.progress(90)

            # Check for errors
            if 'error' in results:
                st.error(f"Analysis failed: {results['error']}")
                session_manager.update_session(session_id, company_slug, {
                    'status': 'failed',
                    'error': results['error'],
                    'completed_at': datetime.now().isoformat()
                })
                return

            # Save outputs
            status_text.text("Generating reports...")

            session_dir = session_manager.get_session_dir(session_id, company_slug)

            # Save JSON
            json_file = session_dir / "analysis.json"
            with open(json_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            session_manager.add_output_file(session_id, company_slug, 'json', str(json_file))

            # Save Markdown
            md_file = session_dir / "report.md"
            generate_markdown_report(results, str(md_file))
            session_manager.add_output_file(session_id, company_slug, 'markdown', str(md_file))

            # Save state
            state_file = session_dir / "state.json"
            orchestrator.save_state(str(state_file))
            session_manager.add_output_file(session_id, company_slug, 'state', str(state_file))

            # Update session
            session_manager.update_session(session_id, company_slug, {
                'completed_at': datetime.now().isoformat(),
                'status': 'completed',
                'summary': results.get('summary', {})
            })

            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")

            st.success(f"✅ Analysis complete for **{company_name}**!")
            st.session_state.analysis_complete = True

            # Display results
            display_results(results, session, session_dir)

        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            session_manager.update_session(session_id, company_slug, {
                'status': 'failed',
                'error': str(e),
                'completed_at': datetime.now().isoformat()
            })


def display_results(results: dict, session: dict, session_dir: Path):
    """Display analysis results."""
    st.header("📊 Analysis Results")

    # Summary metrics
    summary = results.get('summary', {})
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Company", summary.get('company', 'N/A'))
    with col2:
        st.metric("Phase", summary.get('current_phase', 'N/A'))
    with col3:
        tasks = summary.get('tasks', {})
        st.metric("Tasks Completed", f"{tasks.get('completed', 0)}/{tasks.get('total', 0)}")
    with col4:
        st.metric("Status", "Complete" if tasks.get('failed', 0) == 0 else "With Warnings")

    # Download buttons
    st.subheader("📥 Download Reports")

    col1, col2, col3 = st.columns(3)

    with col1:
        json_file = session_dir / "analysis.json"
        if json_file.exists():
            with open(json_file, 'r') as f:
                st.download_button(
                    label="📄 Download JSON",
                    data=f.read(),
                    file_name=f"{session['company_slug']}_analysis.json",
                    mime="application/json"
                )

    with col2:
        md_file = session_dir / "report.md"
        if md_file.exists():
            with open(md_file, 'r') as f:
                st.download_button(
                    label="📝 Download Markdown",
                    data=f.read(),
                    file_name=f"{session['company_slug']}_report.md",
                    mime="text/markdown"
                )

    with col3:
        st.button("📊 Download PDF", disabled=True, help="PDF generation coming soon")

    # Display markdown report
    st.subheader("📄 Executive Report")

    md_file = session_dir / "report.md"
    if md_file.exists():
        with open(md_file, 'r') as f:
            report_content = f.read()
            st.markdown(report_content)


def past_analyses_page():
    """Page showing past analyses."""
    st.header("📚 Past Analyses")

    session_manager = st.session_state.session_manager
    sessions = session_manager.list_sessions()

    if not sessions:
        st.info("No past analyses found. Start a new analysis to get started!")
        return

    st.markdown(f"**Total analyses:** {len(sessions)}")

    # Group by company
    companies = {}
    for session in sessions:
        company_slug = session['company_slug']
        if company_slug not in companies:
            companies[company_slug] = []
        companies[company_slug].append(session)

    # Display grouped by company
    for company_slug, company_sessions in companies.items():
        with st.expander(f"**{company_sessions[0]['company_name']}** ({len(company_sessions)} analyses)"):
            for session in sorted(company_sessions, key=lambda x: x['created_at'], reverse=True):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

                with col1:
                    st.markdown(f"**Session:** `{session['session_id']}`")
                with col2:
                    created = datetime.fromisoformat(session['created_at'])
                    st.text(created.strftime('%Y-%m-%d %H:%M'))
                with col3:
                    status = session.get('status', 'unknown')
                    if status == 'completed':
                        st.success(status.title())
                    elif status == 'failed':
                        st.error(status.title())
                    else:
                        st.warning(status.title())
                with col4:
                    if session.get('status') == 'completed':
                        session_dir = Path(session['output_dir'])
                        md_file = session_dir / "report.md"

                        if md_file.exists():
                            if st.button("View Report", key=f"view_{session['session_id']}"):
                                st.session_state.viewing_session = session
                                with open(md_file, 'r') as f:
                                    st.markdown("---")
                                    st.markdown(f.read())


def about_page():
    """About page."""
    st.header("About BCOS")

    st.markdown("""
    ## Business Context OS

    **BCOS** is an autonomous multi-agent system for comprehensive business research and strategy analysis.

    ### What It Does

    BCOS transforms a company URL into executive-quality business intelligence through two phases:

    **Phase 1: Foundation Building**
    - 🔍 Company Intelligence - Deep website analysis and business understanding
    - 📊 Business Model Canvas - 9-block business model analysis
    - 📈 Market Intelligence - TAM/SAM/SOM sizing, trends, opportunities
    - 🎯 Competitor Intelligence - Multi-competitor profiling and positioning

    **Phase 2: Strategy Analysis**
    - 💪 SWOT Analysis - Strengths, weaknesses, opportunities, threats + TOWS matrix
    - ⚖️ Porter's Five Forces - Industry attractiveness assessment
    - 🌍 PESTEL Analysis - Macro-environmental factors
    - 📊 BCG Matrix - Portfolio analysis (coming soon)

    ### Key Features

    - ✅ **Autonomous** - Runs end-to-end with minimal input
    - ✅ **Multi-Agent** - Dexter-inspired task planning and execution
    - ✅ **Context-Aware** - Each phase builds on previous findings
    - ✅ **Professional Output** - Executive-quality reports
    - ✅ **Session-Based** - Clean isolation between analyses
    - ✅ **Reusable** - Analyze any company without conflicts

    ### Architecture

    ```
    User Input → Session Manager → Orchestrator → Multi-Agent System

    Orchestrator:
      ├─> Planner (LLM-based task decomposition)
      ├─> Executor (Dynamic skill loading)
      ├─> Validator (Task completion verification)
      └─> StateManager (Context passing between phases)

    Skills (Modular & Extensible):
      Phase 1: Company Intelligence, BMC, Market, Competitors
      Phase 2: SWOT, Porter's, PESTEL, BCG, Blue Ocean

    Outputs:
      ├─> JSON (Structured data)
      ├─> Markdown (Executive report)
      ├─> PDF (Coming soon)
      └─> PPTX (Coming soon)
    ```

    ### Technology Stack

    - **LLM**: Claude 3.5 Sonnet (Anthropic)
    - **Framework**: LangChain + custom orchestration
    - **Data Sources**: Firecrawl, Exa, Web Scraping
    - **UI**: Streamlit
    - **Reports**: Markdown, JSON, PDF, DOCX, PPTX

    ### Use Cases

    - 💰 Investment Due Diligence
    - 🎯 Competitive Intelligence
    - 📊 Market Research
    - 🚀 Strategic Planning
    - 🌍 Market Entry Assessment
    - 📈 Business Model Analysis

    ---

    **Version**: 1.0.0
    **Status**: Production Ready
    **License**: MIT
    """)


if __name__ == "__main__":
    main()
