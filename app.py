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
import re

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.orchestrator import BusinessContextOrchestrator
from utils.session_manager import SessionManager, slugify
from utils.logger import setup_logger
from reports.markdown_report import generate_markdown_report, generate_business_overview_report
from utils.progress_tracker import ProgressTracker, ProgressStatus, ProgressLevel
from components.visualizations import (
    create_business_model_canvas,
    create_value_chain_diagram,
    export_to_image
)
from components.data_transformers import (
    transform_bmc_for_visualization,
    transform_value_chain_for_visualization
)
from components.interactive_editor import (
    init_edit_session_state,
    get_bmc_section_options,
    get_value_chain_section_options,
    render_edit_panel,
    save_edited_data_to_file
)

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


def create_progress_display():
    """
    Create comprehensive progress display UI elements.

    Returns:
        Dictionary of UI elements for real-time updates
    """
    # Header with phase info
    header = st.empty()

    # Task checklist container
    task_list = st.empty()

    # Current action with animation
    current_action = st.empty()

    # Progress bar
    progress_bar = st.progress(0)

    # Time estimates
    time_info = st.empty()

    return {
        'header': header,
        'task_list': task_list,
        'action': current_action,
        'bar': progress_bar,
        'time': time_info
    }


def update_progress_ui(status: dict, ui_elements: dict):
    """
    Update all progress UI elements with current status.

    Args:
        status: Current progress status from ProgressTracker
        ui_elements: Dictionary of Streamlit UI elements
    """
    # Update header
    phase = status.get('phase', 'Analysis')
    completed = status.get('completed', 0)
    total = status.get('total_tasks', 0)
    failed = status.get('failed', 0)

    header_text = f"**{phase}** - {completed}/{total} tasks completed"
    if failed > 0:
        header_text += f" ({failed} failed)"
    ui_elements['header'].markdown(header_text)

    # Build task checklist with detailed actions
    tasks = status.get('tasks', [])
    if tasks:
        checklist_html = '<div style="font-family: monospace; font-size: 14px; line-height: 1.6;">'

        for task in tasks:
            task_status = task.get('status', 'pending')
            task_name = task.get('name', 'Unknown task')

            # Choose icon and color based on status
            if task_status == 'completed':
                icon = "✓"
                color = "#28a745"  # Green
                opacity = "0.7"
            elif task_status == 'in_progress':
                icon = "⏳"
                color = "#007bff"  # Blue
                opacity = "1.0"
            elif task_status == 'failed':
                icon = "✗"
                color = "#dc3545"  # Red
                opacity = "1.0"
            else:
                icon = "⏸"
                color = "#6c757d"  # Gray
                opacity = "0.5"

            # Add task line
            checklist_html += f'<div style="color: {color}; opacity: {opacity}; margin-bottom: 2px;">'
            checklist_html += f'{icon} <strong>{task_name}</strong>'
            checklist_html += '</div>'

            # Add recent actions for in-progress or just-completed tasks
            if task_status in ['in_progress', 'completed']:
                actions = task.get('actions', [])
                recent_actions = actions[-3:]  # Last 3 actions

                for action_info in recent_actions:
                    action_text = action_info.get('action', '')
                    action_level = action_info.get('level', 'task')

                    # Different indentation and style based on level
                    if action_level == 'skill':
                        indent = "  └─ "
                        action_color = "#17a2b8"  # Teal
                    elif action_level == 'api':
                        indent = "    └─ "
                        action_color = "#6610f2"  # Purple
                    elif action_level == 'llm':
                        indent = "    └─ "
                        action_color = "#fd7e14"  # Orange
                    else:
                        indent = "  · "
                        action_color = "#6c757d"  # Gray

                    checklist_html += f'<div style="color: {action_color}; opacity: 0.8; font-size: 12px; margin-left: 20px;">'
                    checklist_html += f'{indent}{action_text}'
                    checklist_html += '</div>'

        checklist_html += '</div>'
        ui_elements['task_list'].markdown(checklist_html, unsafe_allow_html=True)

    # Update current action
    current = status.get('current_action')
    if current:
        action_text = current.get('action', '')
        level = current.get('level', 'task')

        # Choose emoji based on level
        if level == 'skill':
            emoji = "🔧"
        elif level == 'api':
            emoji = "🌐"
        elif level == 'llm':
            emoji = "🤖"
        else:
            emoji = "⚙️"

        ui_elements['action'].info(f"{emoji} {action_text}")

    # Update progress bar
    progress_percent = status.get('progress_percent', 0)
    ui_elements['bar'].progress(int(progress_percent) / 100)

    # Update time info
    elapsed = status.get('elapsed', 'Calculating...')
    eta = status.get('eta', 'Calculating...')

    time_text = f"⏱️ **Elapsed:** {elapsed}"
    if status.get('in_progress', True):
        time_text += f" | **ETA:** {eta}"

    ui_elements['time'].caption(time_text)


def estimate_total_tasks(config: dict) -> int:
    """
    Estimate total number of tasks based on configuration.

    Args:
        config: Analysis configuration

    Returns:
        Estimated total task count
    """
    # Base Phase 1 tasks (typically 5-7 tasks)
    phase1_tasks = 7  # Company intel, BMC, market, competitors, value chain, org, synthesis

    # Phase 2 tasks based on selected frameworks
    phase2_tasks = 0
    frameworks = config.get('scope', {}).get('phase2_frameworks', [])
    phase2_tasks = len(frameworks) * 2  # Each framework typically has 2-3 tasks

    analysis_mode = config.get('analysis_mode', 'full')

    if analysis_mode == 'business_overview':
        return phase1_tasks
    elif analysis_mode == 'frameworks':
        return phase2_tasks if phase2_tasks > 0 else 4
    else:  # full
        return phase1_tasks + phase2_tasks


def validate_and_correct_url(url: str) -> tuple[bool, str, str]:
    """
    Validate and correct URL format.

    Returns:
        (is_valid, corrected_url, error_message)
    """
    url = url.strip()

    # Check if empty
    if not url:
        return False, url, "URL cannot be empty"

    # Add https:// if no protocol specified
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"

    # Basic domain pattern validation
    # Matches: domain.com, subdomain.domain.com, domain.co.uk, etc.
    domain_pattern = r'^https?://([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/.*)?$'

    if not re.match(domain_pattern, url):
        return False, url, "Invalid URL format. Please enter a valid domain (e.g., example.com)"

    return True, url, ""


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
            placeholder="e.g., stripe.com or https://stripe.com",
            help="Enter the company's website URL (https:// will be added automatically if needed)"
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

        # Analysis type selection
        st.subheader("📊 Analysis Type")
        business_overview = st.checkbox(
            "Business Overview",
            value=True,
            help="Comprehensive foundation analysis including: Company Intelligence, Business Model Canvas, Market Analysis, Top 4 Competitors, and Value Chain"
        )

        if business_overview:
            st.info("✓ Business Overview includes: Company Intelligence • Business Model Canvas • Market Analysis • Competitor Landscape • Value Chain")

        # Framework selection
        st.subheader("📈 Strategic Frameworks (Optional)")
        st.caption("Strategic frameworks can be run on top of Business Overview")

        col1, col2 = st.columns(2)

        with col1:
            swot = st.checkbox("SWOT Analysis", value=False)
            porters = st.checkbox("Porter's Five Forces", value=False)

        with col2:
            pestel = st.checkbox("PESTEL Analysis", value=False)
            bcg = st.checkbox("BCG Matrix", value=False, disabled=True, help="Coming soon")

        submitted = st.form_submit_button("🚀 Run Analysis", type="primary")

    # Handle form submission OUTSIDE the form context
    if submitted:
        if not company_name or not company_website or not industry:
            st.error("Please fill in all required fields (Company Name, Website, Industry)")
        else:
            # Validate and correct URL format
            is_valid, corrected_url, error_msg = validate_and_correct_url(company_website)

            if not is_valid:
                st.error(f"❌ {error_msg}")
            else:
                # Show correction if URL was modified
                if corrected_url != company_website.strip():
                    st.info(f"🔗 Auto-corrected URL to: `{corrected_url}`")

                # Determine analysis mode
                frameworks_selected = swot or porters or pestel or bcg

                if not business_overview and not frameworks_selected:
                    st.error("❌ Please select at least one analysis type (Business Overview or a Strategic Framework)")
                elif not business_overview and frameworks_selected:
                    st.warning("⚠️ Strategic frameworks require Business Overview as foundation. Either:\n- Check 'Business Overview' to run both together, or\n- Run frameworks on an existing Business Overview")
                    # TODO: Allow selecting existing Business Overview session
                else:
                    # Determine mode
                    if business_overview and frameworks_selected:
                        analysis_mode = "full"  # Both phases
                        st.info("📊 Running: Business Overview + Strategic Frameworks")
                    elif business_overview and not frameworks_selected:
                        analysis_mode = "business_overview"  # Phase 1 only
                        st.info("📊 Running: Business Overview Only")
                    else:
                        analysis_mode = "frameworks"  # Phase 2 only
                        st.info("📊 Running: Strategic Frameworks Only")

                    run_analysis(
                        company_name=company_name,
                        company_website=corrected_url,
                        industry=industry,
                        user_context=user_context,
                        competitors=[c.strip() for c in competitors.split('\n') if c.strip()],
                        frameworks={
                            'swot': swot,
                            'porters': porters,
                            'pestel': pestel,
                            'bcg': bcg
                        },
                        analysis_mode=analysis_mode,
                        run_business_overview=business_overview
                    )

    # Display results if available (outside form context)
    if st.session_state.get('analysis_results'):
        display_results(
            st.session_state.analysis_results['results'],
            st.session_state.analysis_results['session'],
            Path(st.session_state.analysis_results['session_dir'])
        )


def run_analysis(
    company_name: str,
    company_website: str,
    industry: str,
    user_context: str,
    competitors: list,
    frameworks: dict,
    analysis_mode: str = "full",
    run_business_overview: bool = True
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
        'analysis_mode': analysis_mode,  # NEW: analysis mode
        'run_business_overview': run_business_overview,  # NEW: whether to run Phase 1
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
        # Show mode-specific message
        if analysis_mode == "business_overview":
            st.info(f"🔄 Running **Business Overview** for **{company_name}**...")
        elif analysis_mode == "frameworks":
            st.info(f"🔄 Running **Strategic Frameworks** for **{company_name}**...")
        else:
            st.info(f"🔄 Running **Full Analysis** for **{company_name}**...")

        st.markdown(f"Session ID: `{session_id}`")

        # Create comprehensive progress tracker UI
        ui_elements = create_progress_display()

        try:
            # Estimate total tasks for progress tracking
            total_tasks = estimate_total_tasks(config)

            # Create ProgressTracker instance with UI callback
            def on_progress_update(status: dict):
                update_progress_ui(status, ui_elements)

            tracker = ProgressTracker(total_tasks, callback=on_progress_update)

            # Initialize orchestrator with tracker.emit as progress callback
            orchestrator = BusinessContextOrchestrator(config, progress_callback=tracker.emit)

            # Run analysis
            results = orchestrator.run()

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
            session_dir = session_manager.get_session_dir(session_id, company_slug)

            # Save JSON
            json_file = session_dir / "analysis.json"
            with open(json_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            session_manager.add_output_file(session_id, company_slug, 'json', str(json_file))

            # Save Markdown - use appropriate report generator based on analysis type
            md_file = session_dir / "report.md"
            analysis_type = results.get('analysis_type', 'full')

            if analysis_type == "business_overview":
                # Generate Business Overview report
                generate_business_overview_report(
                    results.get('phase1', {}),
                    company_name,
                    str(md_file)
                )
            else:
                # Generate full or frameworks report
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

            st.success(f"✅ Analysis complete for **{company_name}**!")
            st.session_state.analysis_complete = True

            # Store results in session state for display outside form context
            st.session_state.analysis_results = {
                'results': results,
                'session': session,
                'session_dir': str(session_dir)
            }

        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            session_manager.update_session(session_id, company_slug, {
                'status': 'failed',
                'error': str(e),
                'completed_at': datetime.now().isoformat()
            })


def display_results(results: dict, session: dict, session_dir: Path):
    """Display analysis results with interactive visualizations."""
    # Initialize edit session state
    init_edit_session_state()

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

    col1, col2, col3, col4 = st.columns(4)

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

    # Create tabs for different views
    phase1_data = results.get('phase1', {})
    phase2_data = results.get('phase2', {})

    # Determine which tabs to show
    tab_names = ["📄 Executive Report"]

    if phase1_data.get('business_model_canvas'):
        tab_names.append("🎯 Business Model Canvas")

    if phase1_data.get('value_chain'):
        tab_names.append("⛓️ Value Chain")

    if phase2_data:
        tab_names.append("📈 Strategic Frameworks")

    # Create tabs
    tabs = st.tabs(tab_names)

    # Tab 1: Executive Report
    with tabs[0]:
        md_file = session_dir / "report.md"
        if md_file.exists():
            with open(md_file, 'r') as f:
                report_content = f.read()
                st.markdown(report_content)

    # Tab 2: Business Model Canvas (if data exists)
    tab_index = 1
    if phase1_data.get('business_model_canvas'):
        with tabs[tab_index]:
            display_bmc_visualization(phase1_data, session, session_dir)
        tab_index += 1

    # Tab 3: Value Chain (if data exists)
    if phase1_data.get('value_chain'):
        with tabs[tab_index]:
            display_value_chain_visualization(phase1_data, session, session_dir)
        tab_index += 1

    # Tab 4: Strategic Frameworks (if Phase 2 data exists)
    if phase2_data:
        with tabs[tab_index]:
            st.subheader("Strategic Analysis")
            st.info("Interactive framework visualizations coming soon!")
            st.json(phase2_data)


def display_bmc_visualization(phase1_data: dict, session: dict, session_dir: Path):
    """Display Business Model Canvas visualization tab."""
    st.subheader("🎯 Business Model Canvas")

    # Edit mode toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        edit_mode = st.checkbox("Edit Mode", key="bmc_edit_mode")

    # Transform data for visualization
    bmc_viz_data = transform_bmc_for_visualization(phase1_data)

    # Display edit panel if in edit mode
    if edit_mode:
        with st.sidebar:
            section_options = get_bmc_section_options()
            updated_bmc = render_edit_panel('bmc', bmc_viz_data, section_options)

            if updated_bmc:
                bmc_viz_data = updated_bmc

                # Save button
                if st.button("💾 Save to File", key="save_bmc_file"):
                    json_path = session_dir / "analysis.json"
                    if save_edited_data_to_file(updated_bmc, str(json_path), 'bmc'):
                        st.success("Changes saved successfully!")

    # Create and display visualization
    company_name = session.get('company_name', 'Company')
    fig = create_business_model_canvas(bmc_viz_data, title=f"{company_name} - Business Model Canvas")

    # Display with full interactivity
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

    # Export options
    st.subheader("📥 Export Visualization")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Export as PNG"):
            try:
                output_path = export_to_image(
                    fig,
                    f"{session['company_slug']}_bmc",
                    format='png',
                    output_dir=str(session_dir)
                )
                st.success(f"Exported to: {output_path}")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")

    with col2:
        if st.button("Export as SVG"):
            try:
                output_path = export_to_image(
                    fig,
                    f"{session['company_slug']}_bmc",
                    format='svg',
                    output_dir=str(session_dir)
                )
                st.success(f"Exported to: {output_path}")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")

    with col3:
        if st.button("Export as PDF"):
            try:
                output_path = export_to_image(
                    fig,
                    f"{session['company_slug']}_bmc",
                    format='pdf',
                    output_dir=str(session_dir)
                )
                st.success(f"Exported to: {output_path}")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")


def display_value_chain_visualization(phase1_data: dict, session: dict, session_dir: Path):
    """Display Value Chain visualization tab."""
    st.subheader("⛓️ Value Chain Analysis")

    # Edit mode toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        edit_mode = st.checkbox("Edit Mode", key="vc_edit_mode")

    # Transform data for visualization
    vc_viz_data = transform_value_chain_for_visualization(phase1_data)

    # Display edit panel if in edit mode
    if edit_mode:
        with st.sidebar:
            section_options = get_value_chain_section_options()
            updated_vc = render_edit_panel('value_chain', vc_viz_data, section_options)

            if updated_vc:
                vc_viz_data = updated_vc

                # Save button
                if st.button("💾 Save to File", key="save_vc_file"):
                    json_path = session_dir / "analysis.json"
                    if save_edited_data_to_file(updated_vc, str(json_path), 'value_chain'):
                        st.success("Changes saved successfully!")

    # Create and display visualization
    company_name = session.get('company_name', 'Company')
    fig = create_value_chain_diagram(vc_viz_data, title=f"{company_name} - Value Chain")

    # Display with full interactivity
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

    # Export options
    st.subheader("📥 Export Visualization")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Export as PNG", key="vc_png"):
            try:
                output_path = export_to_image(
                    fig,
                    f"{session['company_slug']}_value_chain",
                    format='png',
                    output_dir=str(session_dir)
                )
                st.success(f"Exported to: {output_path}")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")

    with col2:
        if st.button("Export as SVG", key="vc_svg"):
            try:
                output_path = export_to_image(
                    fig,
                    f"{session['company_slug']}_value_chain",
                    format='svg',
                    output_dir=str(session_dir)
                )
                st.success(f"Exported to: {output_path}")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")

    with col3:
        if st.button("Export as PDF", key="vc_pdf"):
            try:
                output_path = export_to_image(
                    fig,
                    f"{session['company_slug']}_value_chain",
                    format='pdf',
                    output_dir=str(session_dir)
                )
                st.success(f"Exported to: {output_path}")
            except Exception as e:
                st.error(f"Export failed: {str(e)}")


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
