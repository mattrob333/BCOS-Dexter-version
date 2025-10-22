"""
Markdown Report Generator.

Transforms BCOS analysis results into professional markdown reports.
"""

from typing import Dict, Any
from datetime import datetime
from pathlib import Path


def generate_markdown_report(
    results: Dict[str, Any],
    output_path: str = None
) -> str:
    """
    Generate a comprehensive markdown report from BCOS analysis results.

    Args:
        results: Complete BCOS analysis results (Phase 1 + Phase 2)
        output_path: Optional path to save report file

    Returns:
        Markdown report as string
    """
    company_name = results.get('company', 'Unknown Company')
    summary = results.get('summary', {})
    phase1 = results.get('phase1', {})
    phase2 = results.get('phase2', {})

    # Build report sections
    sections = []

    # Title and header
    sections.append(_generate_header(company_name, summary))

    # Executive Summary
    sections.append(_generate_executive_summary(company_name, phase1, phase2))

    # Phase 1: Foundation
    sections.append(_generate_phase1_section(phase1))

    # Phase 2: Strategy
    sections.append(_generate_phase2_section(phase2))

    # Appendix
    sections.append(_generate_appendix(summary))

    # Combine all sections
    report = '\n\n'.join(sections)

    # Save if output path provided
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(report)

    return report


def _generate_header(company_name: str, summary: Dict[str, Any]) -> str:
    """Generate report header."""
    timestamp = datetime.now().strftime('%B %d, %Y')

    return f"""# Business Context Analysis
## {company_name}

**Generated**: {timestamp}
**System**: Business Context OS (BCOS)
**Status**: {summary.get('current_phase', 'Complete')}

---
"""


def _generate_executive_summary(
    company_name: str,
    phase1: Dict[str, Any],
    phase2: Dict[str, Any]
) -> str:
    """Generate executive summary."""
    company_intel = phase1.get('company_intelligence', {})
    swot = phase2.get('swot', {})
    five_forces = phase2.get('porters_five_forces', {})

    business_desc = company_intel.get('business_description', 'No description available.')
    value_prop = company_intel.get('value_proposition', 'No value proposition available.')

    # Extract key insights
    top_strengths = swot.get('prioritization', {}).get('top_strengths', [])[:3]
    best_opportunities = swot.get('prioritization', {}).get('best_opportunities', [])[:3]

    industry_attractiveness = five_forces.get('overall_assessment', {}).get('industry_attractiveness', 'Unknown')

    summary = f"""## Executive Summary

### Company Overview
{business_desc}

**Value Proposition**: {value_prop}

### Key Findings

"""

    if top_strengths:
        summary += "**Top Strengths:**\n"
        for i, strength in enumerate(top_strengths, 1):
            summary += f"{i}. {strength}\n"
        summary += "\n"

    if best_opportunities:
        summary += "**Best Opportunities:**\n"
        for i, opp in enumerate(best_opportunities, 1):
            summary += f"{i}. {opp}\n"
        summary += "\n"

    if industry_attractiveness != 'Unknown':
        summary += f"**Industry Attractiveness**: {industry_attractiveness.replace('-', ' ').title()}\n"

    return summary


def _generate_phase1_section(phase1: Dict[str, Any]) -> str:
    """Generate Phase 1 foundation section."""
    sections = ["## Phase 1: Business Foundation\n"]

    # Company Intelligence
    if 'company_intelligence' in phase1:
        sections.append(_format_company_intelligence(phase1['company_intelligence']))

    # Business Model Canvas
    if 'business_model_canvas' in phase1:
        sections.append(_format_business_model_canvas(phase1['business_model_canvas']))

    # Market Intelligence
    if 'market_intelligence' in phase1:
        sections.append(_format_market_intelligence(phase1['market_intelligence']))

    # Competitor Intelligence
    if 'competitor_intelligence' in phase1:
        sections.append(_format_competitor_intelligence(phase1['competitor_intelligence']))

    return '\n\n'.join(sections)


def _format_company_intelligence(intel: Dict[str, Any]) -> str:
    """Format company intelligence section."""
    output = ["### Company Intelligence\n"]

    if 'business_description' in intel:
        output.append(f"**Business Description**: {intel['business_description']}\n")

    if 'products_services' in intel:
        products = intel['products_services']
        if isinstance(products, list):
            output.append("**Products/Services**:")
            for product in products:
                output.append(f"- {product}")
            output.append("")

    if 'target_customers' in intel:
        output.append(f"**Target Customers**: {intel['target_customers']}\n")

    if 'key_facts' in intel:
        facts = intel['key_facts']
        output.append("**Key Facts**:")
        for key, value in facts.items():
            if value:
                output.append(f"- **{key.replace('_', ' ').title()}**: {value}")
        output.append("")

    return '\n'.join(output)


def _format_business_model_canvas(bmc: Dict[str, Any]) -> str:
    """Format Business Model Canvas section."""
    output = ["### Business Model Canvas\n"]

    if 'customer_segments' in bmc:
        output.append("#### Customer Segments")
        for segment in bmc['customer_segments'][:3]:  # Top 3
            output.append(f"**{segment.get('segment_name', 'Segment')}**")
            output.append(f"- {segment.get('description', '')}")
            output.append("")

    if 'value_propositions' in bmc:
        output.append("#### Value Propositions")
        for vp in bmc['value_propositions'][:2]:  # Top 2
            output.append(f"**For {vp.get('for_segment', 'segment')}:**")
            output.append(f"- {vp.get('core_value', '')}")
            output.append("")

    if 'revenue_streams' in bmc:
        output.append("#### Revenue Streams")
        for stream in bmc['revenue_streams'][:3]:
            output.append(f"- **{stream.get('stream_type', 'Stream')}**: {stream.get('description', '')}")
        output.append("")

    return '\n'.join(output)


def _format_market_intelligence(market: Dict[str, Any]) -> str:
    """Format market intelligence section."""
    output = ["### Market Intelligence\n"]

    if 'market_size' in market:
        size = market['market_size']
        output.append("#### Market Size")
        output.append(f"- **TAM**: {size.get('tam', {}).get('value', 'Unknown')}")
        output.append(f"- **Growth Rate (CAGR)**: {size.get('growth_rate_cagr', 'Unknown')}")
        output.append(f"- **Projected 2030**: {size.get('projected_size_2030', 'Unknown')}")
        output.append("")

    if 'trends' in market:
        output.append("#### Key Trends")
        for trend in market['trends'][:5]:  # Top 5
            impact = trend.get('impact', 'unknown')
            output.append(f"- **{trend.get('trend', 'Trend')}** ({impact} impact): {trend.get('description', '')}")
        output.append("")

    if 'opportunities' in market:
        output.append("#### Market Opportunities")
        for opp in market['opportunities'][:5]:  # Top 5
            output.append(f"- **{opp.get('opportunity', 'Opportunity')}**: {opp.get('description', '')}")
        output.append("")

    return '\n'.join(output)


def _format_competitor_intelligence(comp: Dict[str, Any]) -> str:
    """Format competitor intelligence section."""
    output = ["### Competitor Intelligence\n"]

    if 'competitor_profiles' in comp:
        output.append("#### Key Competitors\n")
        for profile in comp['competitor_profiles'][:5]:  # Top 5
            name = profile.get('name', 'Competitor')
            threat = profile.get('threat_assessment', {})

            output.append(f"**{name}**")
            positioning = profile.get('market_positioning', {})
            output.append(f"- Position: {positioning.get('value_proposition', 'Unknown')}")

            threat_level = threat.get('threat_level', 'unknown')
            output.append(f"- Threat Level: {threat_level}")
            output.append("")

    if 'competitive_landscape' in comp:
        landscape = comp['competitive_landscape']
        output.append("#### Competitive Landscape")
        output.append(f"- **Our Position**: {landscape.get('our_position', 'Unknown')}")
        output.append(f"- **Market Leaders**: {', '.join(landscape.get('market_leaders', []))}")
        output.append("")

    return '\n'.join(output)


def _generate_phase2_section(phase2: Dict[str, Any]) -> str:
    """Generate Phase 2 strategy section."""
    sections = ["## Phase 2: Strategic Analysis\n"]

    # SWOT Analysis
    if 'swot' in phase2:
        sections.append(_format_swot_analysis(phase2['swot']))

    # Porter's Five Forces
    if 'porters_five_forces' in phase2:
        sections.append(_format_five_forces(phase2['porters_five_forces']))

    return '\n\n'.join(sections)


def _format_swot_analysis(swot: Dict[str, Any]) -> str:
    """Format SWOT analysis section."""
    output = ["### SWOT Analysis\n"]

    # Strengths
    if 'strengths' in swot:
        output.append("#### Strengths")
        for s in swot['strengths'][:5]:  # Top 5
            output.append(f"- **{s.get('strength', 'Strength')}** ({s.get('impact', 'unknown')} impact): {s.get('description', '')}")
        output.append("")

    # Weaknesses
    if 'weaknesses' in swot:
        output.append("#### Weaknesses")
        for w in swot['weaknesses'][:5]:
            output.append(f"- **{w.get('weakness', 'Weakness')}** ({w.get('severity', 'unknown')} severity): {w.get('description', '')}")
        output.append("")

    # Opportunities
    if 'opportunities' in swot:
        output.append("#### Opportunities")
        for o in swot['opportunities'][:5]:
            output.append(f"- **{o.get('opportunity', 'Opportunity')}** ({o.get('potential_impact', 'unknown')} impact): {o.get('description', '')}")
        output.append("")

    # Threats
    if 'threats' in swot:
        output.append("#### Threats")
        for t in swot['threats'][:5]:
            output.append(f"- **{t.get('threat', 'Threat')}** ({t.get('severity', 'unknown')} severity): {t.get('description', '')}")
        output.append("")

    # Strategic Implications
    if 'strategic_implications' in swot:
        output.append("#### Strategic Implications")
        for impl in swot['strategic_implications'][:3]:
            output.append(f"- {impl}")
        output.append("")

    return '\n'.join(output)


def _format_five_forces(forces: Dict[str, Any]) -> str:
    """Format Porter's Five Forces section."""
    output = ["### Porter's Five Forces\n"]

    # Overall assessment
    if 'overall_assessment' in forces:
        assessment = forces['overall_assessment']
        output.append("#### Overall Assessment")
        output.append(f"- **Industry Attractiveness**: {assessment.get('industry_attractiveness', 'Unknown').replace('-', ' ').title()}")
        output.append(f"- **Attractiveness Score**: {assessment.get('attractiveness_score', 'N/A')}/10")
        output.append(f"- **Strongest Force**: {assessment.get('strongest_force', 'Unknown').replace('_', ' ').title()}")
        output.append(f"- **Profit Potential**: {assessment.get('profit_potential', 'Unknown')}")
        output.append("")

    # Individual forces
    force_names = {
        'threat_of_new_entrants': 'Threat of New Entrants',
        'supplier_power': 'Supplier Power',
        'buyer_power': 'Buyer Power',
        'threat_of_substitutes': 'Threat of Substitutes',
        'competitive_rivalry': 'Competitive Rivalry'
    }

    for key, name in force_names.items():
        if key in forces:
            force = forces[key]
            intensity = force.get('intensity', 'unknown')
            trend = force.get('trend', 'unknown')
            output.append(f"#### {name}")
            output.append(f"**Intensity**: {intensity.upper()} ({trend})")
            if 'impact_on_industry' in force:
                output.append(f"\n{force['impact_on_industry']}")
            output.append("")

    return '\n'.join(output)


def _generate_appendix(summary: Dict[str, Any]) -> str:
    """Generate appendix with metadata."""
    tasks = summary.get('tasks', {})

    return f"""## Appendix

### Analysis Metadata

- **Total Tasks**: {tasks.get('total', 0)}
- **Completed**: {tasks.get('completed', 0)}
- **Failed**: {tasks.get('failed', 0)}
- **Pending**: {tasks.get('pending', 0)}

### Methodology

This analysis was conducted using the Business Context OS (BCOS), an autonomous multi-agent system that:

1. **Phase 1: Foundation Building** - Gathers comprehensive business intelligence
   - Company intelligence from website and public sources
   - Business Model Canvas analysis
   - Market landscape research
   - Competitor profiling

2. **Phase 2: Strategy Analysis** - Applies strategic frameworks
   - SWOT Analysis
   - Porter's Five Forces
   - Additional strategic frameworks as configured

3. **Report Generation** - Synthesizes findings into actionable insights

---

*Report generated by Business Context OS (BCOS)*
*For questions or feedback, please review the analysis methodology and data sources.*
"""
