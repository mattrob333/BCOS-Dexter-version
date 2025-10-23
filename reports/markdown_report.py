"""
Markdown Report Generator.

Transforms BCOS analysis results into professional markdown reports.
Updated to support Multi-Source Truth Engine verified_dataset format.
"""

from typing import Dict, Any
from datetime import datetime
from pathlib import Path


def extract_from_verified_dataset(company_intel: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract data from company intelligence result.

    Handles multiple formats:
    1. New clean format: {'data': {...}} - Simple dictionary
    2. Old verified_dataset format: {'verified_dataset': {'facts': [...]}}
    3. Direct format: Company intel dictionary itself

    Args:
        company_intel: Company intelligence data

    Returns:
        Flat dictionary with extracted values
    """
    # New clean format: {'data': {...}}
    if 'data' in company_intel and isinstance(company_intel['data'], dict):
        return company_intel['data']

    # Old verified_dataset format
    if 'verified_dataset' in company_intel:
        verified_dataset = company_intel['verified_dataset']
        facts = verified_dataset.get('facts', [])

        # Convert facts array to flat dictionary
        extracted = {}
        for fact in facts:
            claim = fact.get('claim', '')
            value = fact.get('value')

            # Only include facts that have values
            if value is not None:
                extracted[claim] = value

        return extracted

    # Direct format fallback
    return company_intel


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
        with open(output_file, 'w', encoding='utf-8') as f:
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
    """Format competitor intelligence section with bulletproof error handling."""
    output = ["### Competitor Intelligence\n"]

    # Check if this is an error response
    if not isinstance(comp, dict):
        output.append("*Competitor data unavailable*\n")
        return '\n'.join(output)

    if comp.get('success') == False:
        error_msg = comp.get('error', 'Unknown error')
        output.append(f"*{error_msg}*\n")
        return '\n'.join(output)

    # Safely handle competitor_profiles
    if 'competitor_profiles' in comp:
        competitor_profiles = comp['competitor_profiles']

        # Verify it's a dict before iterating
        if isinstance(competitor_profiles, dict) and competitor_profiles:
            output.append("#### Key Competitors\n")

            try:
                for competitor_name, profile in list(competitor_profiles.items())[:5]:  # Top 5
                    if not isinstance(profile, dict):
                        continue  # Skip malformed entries

                    # Skip error entries
                    if 'error' in profile:
                        output.append(f"**{competitor_name}**: *{profile['error']}*")
                        output.append("")
                        continue

                    # Safely extract data
                    output.append(f"**{competitor_name}**")

                    positioning = profile.get('market_positioning', {})
                    if isinstance(positioning, dict):
                        value_prop = positioning.get('value_proposition', 'Unknown')
                        output.append(f"- Position: {value_prop}")

                    threat = profile.get('threat_assessment', {})
                    if isinstance(threat, dict):
                        threat_level = threat.get('threat_level', 'unknown')
                        output.append(f"- Threat Level: {threat_level}")

                    output.append("")
            except (AttributeError, TypeError) as e:
                output.append(f"*Error formatting competitor data: {str(e)}*\n")

    # Safely handle competitive_landscape
    if 'competitive_landscape' in comp:
        landscape = comp['competitive_landscape']

        if isinstance(landscape, dict):
            output.append("#### Competitive Landscape")
            our_pos = landscape.get('our_position', 'Unknown')
            output.append(f"- **Our Position**: {our_pos}")

            market_leaders = landscape.get('market_leaders', [])
            if isinstance(market_leaders, list):
                leaders_str = ', '.join(str(l) for l in market_leaders) if market_leaders else 'Unknown'
                output.append(f"- **Market Leaders**: {leaders_str}")
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


def generate_business_overview_report(
    phase1_results: Dict[str, Any],
    company_name: str,
    output_path: str = None
) -> str:
    """
    Generate a Business Overview report from Phase 1 results only.

    This report includes:
    - Company overview and products/services
    - Company fact pack
    - Complete Business Model Canvas (9 sections)
    - Market analysis
    - Top 4 competitors
    - Value chain

    Args:
        phase1_results: Phase 1 analysis results
        company_name: Name of the company
        output_path: Optional path to save report file

    Returns:
        Markdown report as string
    """
    timestamp = datetime.now().strftime('%B %d, %Y')

    sections = []

    # Header
    sections.append(f"""# Business Overview Report
## {company_name}

**Generated**: {timestamp}
**Report Type**: Business Overview (Foundation Analysis)
**System**: Business Context OS (BCOS)

---
""")

    # Executive Summary
    company_intel = phase1_results.get('company_intelligence', {})
    market_intel = phase1_results.get('market_intelligence', {})
    competitors = phase1_results.get('competitor_intelligence', {})
    bmc = phase1_results.get('business_model_canvas', {})

    sections.append(_generate_enhanced_executive_summary(
        company_name,
        company_intel,
        market_intel,
        competitors,
        bmc
    ))

    # Section 1: Products and Services
    sections.append(_generate_products_services_section(company_intel))

    # Section 2: Company Fact Pack
    sections.append(_generate_fact_pack_section(company_intel))

    # Section 3: Business Model Canvas (Complete 9 sections)
    bmc = phase1_results.get('business_model_canvas', {})
    sections.append(_generate_complete_bmc_section(bmc, company_intel))

    # Section 4: Market Analysis
    market = phase1_results.get('market_intelligence', {})
    sections.append(_generate_market_analysis_section(market))

    # Section 5: Competitive Landscape
    competitors = phase1_results.get('competitor_intelligence', {})
    sections.append(_generate_competitive_landscape_section(competitors))

    # Section 6: Value Chain
    value_chain = phase1_results.get('value_chain', {})
    sections.append(_generate_value_chain_section(value_chain))

    # Footer
    sections.append(f"""

---

## Recommended Next Steps

Based on this Business Overview of **{company_name}**, we recommend the following strategic frameworks:

### 🎯 Strategic Framework Analysis

**High Priority:**
1. **SWOT Analysis** (~5-7 min)
   - Identify key strengths to leverage
   - Uncover opportunities in the market
   - Assess competitive threats
   - Address internal weaknesses

2. **Porter's Five Forces** (~6-8 min)
   - Evaluate industry competitive dynamics
   - Assess supplier and buyer power
   - Identify barriers to entry
   - Determine industry attractiveness

**Recommended:**
3. **PESTEL Analysis** (~5-7 min)
   - Analyze macro-environmental factors
   - Identify regulatory risks and opportunities
   - Understand societal and technological trends

### 💡 How to Run Frameworks

**If viewing in Streamlit:** Use the framework selector below this report to run selected frameworks immediately.

**If viewing markdown:** Re-open this analysis in the BCOS web app and select frameworks from the results page.

### 📊 Deep Dive Options

- **Market Analysis**: Explore TAM/SAM/SOM sizing and growth projections
- **Competitive Intelligence**: Detailed competitor profiling and positioning
- **Value Chain Optimization**: Identify margin creation opportunities

---

*Report generated by Business Context OS (BCOS)*
*Business Overview - Foundation Analysis*
*Framework execution available through web interface*
""")

    # Combine all sections
    report = '\n\n'.join(sections)

    # Save if output path provided
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

    return report


def _generate_products_services_section(company_intel: Dict[str, Any]) -> str:
    """Generate detailed products and services section."""
    output = ["## 1. Products & Services\n"]

    # Extract data from verified_dataset if present
    company_data = extract_from_verified_dataset(company_intel)

    if 'products_services' in company_data:
        products = company_data['products_services']
        if isinstance(products, list) and products:
            output.append("### Product Portfolio\n")
            for product in products:
                output.append(f"- {product}")
            output.append("")

    if 'target_customers' in company_data:
        output.append(f"### Target Customers\n{company_data['target_customers']}\n")

    return '\n'.join(output)


def _generate_fact_pack_section(company_intel: Dict[str, Any]) -> str:
    """Generate company fact pack."""
    output = ["## 2. Company Fact Pack\n"]

    # Extract data from verified_dataset if present
    company_data = extract_from_verified_dataset(company_intel)

    if 'key_facts' in company_data:
        facts = company_data['key_facts']
        for key, value in facts.items():
            if value and value != "Not specified":
                label = key.replace('_', ' ').title()
                output.append(f"**{label}**: {value}  ")

    return '\n'.join(output)


def _generate_enhanced_executive_summary(
    company_name: str,
    company_intel: Dict[str, Any],
    market_intel: Dict[str, Any],
    competitors: Dict[str, Any],
    bmc: Dict[str, Any]
) -> str:
    """Generate enhanced executive summary with metrics, positioning, and insights."""
    output = ["## Executive Summary\n"]

    # Extract data from verified_dataset if present
    company_data = extract_from_verified_dataset(company_intel)

    # Company Overview
    business_desc = company_data.get('business_description', 'No description available.')
    value_prop = company_data.get('value_proposition', '')

    output.append("### Company Overview")
    output.append(f"{business_desc}\n")
    if value_prop:
        output.append(f"**Value Proposition**: {value_prop}\n")

    # Key Metrics (if available)
    key_facts = company_data.get('key_facts', {})
    if key_facts and any(key_facts.values()):
        output.append("### Key Metrics\n")
        metrics = []
        if key_facts.get('founded'):
            metrics.append(f"**Founded**: {key_facts['founded']}")
        if key_facts.get('headquarters'):
            metrics.append(f"**Headquarters**: {key_facts['headquarters']}")
        if key_facts.get('employees'):
            metrics.append(f"**Employees**: {key_facts['employees']}")
        if key_facts.get('revenue'):
            metrics.append(f"**Revenue**: {key_facts['revenue']}")
        if key_facts.get('funding'):
            metrics.append(f"**Funding**: {key_facts['funding']}")

        for metric in metrics:
            output.append(f"{metric}  ")
        output.append("")

    # Strategic Positioning
    output.append("### Strategic Positioning\n")

    # Market size insight
    market_size = market_intel.get('market_size', {})
    tam = market_size.get('tam', {}).get('value', 'Unknown')
    growth = market_size.get('growth_rate_cagr', 'Unknown')

    if tam != 'Unknown':
        output.append(f"**Market Opportunity**: Operating in a ${tam} market with {growth} CAGR growth  ")

    # Competitive position
    # Handle both old format ('competitors' list) and new format ('competitor_profiles' dict)
    competitor_profiles = competitors.get('competitor_profiles', {})
    if isinstance(competitor_profiles, dict) and competitor_profiles:
        # New format: dict keyed by competitor name
        top_competitors = list(competitor_profiles.keys())[:3]
        output.append(f"**Key Competitors**: {', '.join(top_competitors)}  ")
    else:
        # Old format: list
        comp_list = competitors.get('competitors', [])
        if comp_list and len(comp_list) > 0:
            top_competitors = [c.get('company_name', 'Unknown') for c in comp_list[:3]]
            output.append(f"**Key Competitors**: {', '.join(top_competitors)}  ")

    # Primary value proposition from BMC
    value_props = bmc.get('value_propositions', [])
    if value_props and len(value_props) > 0:
        first_vp = value_props[0]
        if isinstance(first_vp, dict):
            core_value = first_vp.get('core_value', '')
            if core_value:
                output.append(f"**Core Differentiation**: {core_value}  ")
        elif isinstance(first_vp, str):
            output.append(f"**Core Differentiation**: {first_vp}  ")

    output.append("")

    # Key Insights
    output.append("### Key Insights\n")

    insights = []

    # Market insight
    trends = market_intel.get('trends', [])
    if trends and len(trends) > 0:
        top_trend = trends[0]
        if isinstance(top_trend, dict):
            trend_name = top_trend.get('trend', '')
            if trend_name:
                insights.append(f"**Market Trend**: {trend_name}")

    # Competitive insight
    if comp_list and len(comp_list) >= 2:
        insights.append(f"**Competitive Landscape**: Competing against {len(comp_list)} identified players in the market")

    # Business model insight
    revenue_streams = bmc.get('revenue_streams', [])
    if revenue_streams and len(revenue_streams) > 0:
        insights.append(f"**Revenue Model**: {len(revenue_streams)} distinct revenue stream(s)")

    for insight in insights:
        output.append(f"{insight}  ")

    output.append("\n---\n")

    return '\n'.join(output)


def _generate_fallback_bmc(company_intel: Dict[str, Any]) -> str:
    """Generate basic BMC from company intelligence when full BMC is unavailable."""
    output = ["## 3. Business Model Canvas\n"]
    output.append("*Generated from available company intelligence*\n")

    # Extract data from verified_dataset if present
    company_data = extract_from_verified_dataset(company_intel)

    # Customer Segments
    output.append("### Customer Segments")
    target_customers = company_data.get('target_customers', 'Not specified')
    output.append(f"{target_customers}\n")

    # Value Propositions
    output.append("### Value Propositions")
    value_prop = company_data.get('value_proposition', 'Not specified')
    output.append(f"{value_prop}\n")

    # Channels
    output.append("### Channels")
    output.append("*To be determined from further analysis*\n")

    # Customer Relationships
    output.append("### Customer Relationships")
    output.append("*To be determined from further analysis*\n")

    # Revenue Streams
    output.append("### Revenue Streams")
    business_model = company_data.get('business_model', 'Not specified')
    output.append(f"{business_model}\n")

    # Key Resources
    output.append("### Key Resources")
    products = company_data.get('products_services', [])
    if products:
        output.append("**Products & Services:**")
        for product in products[:5]:  # Top 5
            output.append(f"- {product}")
        output.append("")
    else:
        output.append("*To be determined from further analysis*\n")

    # Key Activities
    output.append("### Key Activities")
    output.append("*To be determined from further analysis*\n")

    # Key Partnerships
    output.append("### Key Partnerships")
    output.append("*To be determined from further analysis*\n")

    # Cost Structure
    output.append("### Cost Structure")
    output.append("*To be determined from further analysis*\n")

    return '\n'.join(output)


def _generate_complete_bmc_section(bmc: Dict[str, Any], company_intel: Dict[str, Any] = None) -> str:
    """Generate complete Business Model Canvas with all 9 sections - BULLETPROOF."""
    output = ["## 3. Business Model Canvas\n"]

    # If BMC is empty, build fallback from company_intelligence
    if not bmc or len(bmc) == 0:
        if company_intel:
            output.append("*Note: Business Model Canvas generated from available company intelligence*\n")
            return _generate_fallback_bmc(company_intel)
        else:
            output.append("*Business Model Canvas data not available*\n")
            return '\n'.join(output)

    # Customer Segments
    if 'customer_segments' in bmc:
        output.append("### Customer Segments")
        for segment in bmc['customer_segments']:
            if isinstance(segment, dict):
                output.append(f"**{segment.get('segment_name', 'Segment')}**  ")
                output.append(f"{segment.get('description', '')}\n")
            elif isinstance(segment, str):
                output.append(f"- {segment}\n")

    # Value Propositions
    if 'value_propositions' in bmc:
        output.append("### Value Propositions")
        for vp in bmc['value_propositions']:
            if isinstance(vp, dict):
                output.append(f"**For {vp.get('for_segment', 'segment')}:**  ")
                output.append(f"{vp.get('core_value', '')}\n")
            elif isinstance(vp, str):
                output.append(f"- {vp}\n")

    # Channels
    if 'channels' in bmc:
        output.append("### Channels")
        for channel in bmc['channels']:
            if isinstance(channel, dict):
                output.append(f"- **{channel.get('channel_type', 'Channel')}**: {channel.get('description', '')}")
            elif isinstance(channel, str):
                output.append(f"- {channel}")
        output.append("")

    # Customer Relationships
    if 'customer_relationships' in bmc:
        output.append("### Customer Relationships")
        for rel in bmc['customer_relationships']:
            if isinstance(rel, dict):
                output.append(f"- **{rel.get('relationship_type', 'Type')}**: {rel.get('description', '')}")
            elif isinstance(rel, str):
                output.append(f"- {rel}")
        output.append("")

    # Revenue Streams
    if 'revenue_streams' in bmc:
        output.append("### Revenue Streams")
        for stream in bmc['revenue_streams']:
            if isinstance(stream, dict):
                output.append(f"- **{stream.get('stream_type', 'Stream')}**: {stream.get('description', '')}")
            elif isinstance(stream, str):
                output.append(f"- {stream}")
        output.append("")

    # Key Resources
    if 'key_resources' in bmc:
        output.append("### Key Resources")
        for resource in bmc['key_resources']:
            if isinstance(resource, dict):
                output.append(f"- **{resource.get('resource_type', 'Resource')}**: {resource.get('description', '')}")
            elif isinstance(resource, str):
                output.append(f"- {resource}")
        output.append("")

    # Key Activities
    if 'key_activities' in bmc:
        output.append("### Key Activities")
        for activity in bmc['key_activities']:
            if isinstance(activity, dict):
                output.append(f"- {activity.get('activity', activity.get('description', ''))}")
            elif isinstance(activity, str):
                output.append(f"- {activity}")
        output.append("")

    # Key Partnerships
    if 'key_partnerships' in bmc:
        output.append("### Key Partnerships")
        for partner in bmc['key_partnerships']:
            if isinstance(partner, dict):
                output.append(f"- **{partner.get('partner_type', 'Partner')}**: {partner.get('description', '')}")
            elif isinstance(partner, str):
                output.append(f"- {partner}")
        output.append("")

    # Cost Structure
    if 'cost_structure' in bmc:
        output.append("### Cost Structure")
        for cost in bmc['cost_structure']:
            if isinstance(cost, dict):
                output.append(f"- **{cost.get('cost_category', 'Cost')}**: {cost.get('description', '')}")
            elif isinstance(cost, str):
                output.append(f"- {cost}")
        output.append("")

    return '\n'.join(output)


def _generate_market_analysis_section(market: Dict[str, Any]) -> str:
    """Generate market analysis section."""
    output = ["## 4. Market Analysis\n"]

    # Market Size
    if 'market_size' in market:
        size = market['market_size']
        output.append("### Market Size\n")
        output.append(f"**Total Addressable Market (TAM)**: {size.get('tam', {}).get('value', 'Unknown')}  ")
        output.append(f"**Growth Rate (CAGR)**: {size.get('growth_rate_cagr', 'Unknown')}  ")
        output.append(f"**Projected 2030**: {size.get('projected_size_2030', 'Unknown')}\n")

    # Key Trends
    if 'trends' in market:
        output.append("### Key Market Trends\n")
        for trend in market['trends'][:5]:
            output.append(f"**{trend.get('trend', 'Trend')}**  ")
            output.append(f"{trend.get('description', '')}  ")
            output.append(f"*Impact: {trend.get('impact', 'unknown').title()}*\n")

    # Opportunities
    if 'opportunities' in market:
        output.append("### Market Opportunities\n")
        for opp in market['opportunities'][:3]:
            output.append(f"- {opp.get('opportunity', '')}")
        output.append("")

    return '\n'.join(output)


def _generate_competitive_landscape_section(competitors: Dict[str, Any]) -> str:
    """Generate competitive landscape with top 4 competitors."""
    output = ["## 5. Competitive Landscape\n"]

    # Handle both old format ('competitors' list) and new format ('competitor_profiles' dict)
    if 'competitor_profiles' in competitors:
        # New format: dict keyed by competitor name
        competitor_profiles = competitors['competitor_profiles']
        if isinstance(competitor_profiles, dict):
            # Convert dict to list of items and take top 4
            for i, (competitor_name, profile) in enumerate(list(competitor_profiles.items())[:4], 1):
                # Skip if this is an error entry
                if 'error' in profile:
                    output.append(f"### Competitor {i}: {competitor_name}\n")
                    output.append(f"*Data unavailable: {profile['error']}*\n")
                    continue

                output.append(f"### Competitor {i}: {competitor_name}\n")

                # Company description
                company_desc = profile.get('company_description', 'No overview available.')
                output.append(f"**Overview**: {company_desc}\n")

                # Value proposition
                value_prop = profile.get('value_proposition', '')
                if value_prop:
                    output.append(f"**Value Proposition**: {value_prop}\n")

                # Business facts
                business_facts = profile.get('business_facts', {})
                if business_facts:
                    output.append("**Key Facts:**")
                    if business_facts.get('revenue') and business_facts['revenue'] != 'Unknown':
                        output.append(f"- Revenue: {business_facts['revenue']}")
                    if business_facts.get('employees') and business_facts['employees'] != 'Unknown':
                        output.append(f"- Employees: {business_facts['employees']}")
                    output.append("")

                # Competitive strengths
                strengths = profile.get('competitive_strengths', [])
                if strengths:
                    output.append("**Competitive Strengths:**")
                    for strength in strengths[:3]:
                        output.append(f"- {strength}")
                    output.append("")

                # Recent moves
                recent_moves = profile.get('recent_moves', [])
                if recent_moves:
                    output.append("**Recent Strategic Moves:**")
                    for move in recent_moves[:2]:
                        output.append(f"- {move}")
                    output.append("")

    elif 'competitors' in competitors:
        # Old format: list of competitor objects
        comps = competitors['competitors'][:4]  # Top 4
        for i, comp in enumerate(comps, 1):
            output.append(f"### Competitor {i}: {comp.get('company_name', 'Unknown')}\n")
            output.append(f"**Overview**: {comp.get('overview', 'No overview available.')}\n")

            if 'positioning' in comp:
                output.append(f"**Positioning**: {comp['positioning']}\n")

            if 'strengths' in comp:
                output.append("**Strengths:**")
                for strength in comp['strengths'][:3]:
                    output.append(f"- {strength}")
                output.append("")

            if 'weaknesses' in comp:
                output.append("**Weaknesses:**")
                for weakness in comp['weaknesses'][:3]:
                    output.append(f"- {weakness}")
                output.append("")
    else:
        output.append("*No competitor data available*\n")

    return '\n'.join(output)


def _generate_value_chain_section(value_chain: Dict[str, Any]) -> str:
    """Generate value chain section."""
    output = ["## 6. Value Chain\n"]

    # Check if data exists
    if not value_chain or not value_chain.get('findings'):
        return '\n'.join(output)

    findings = value_chain.get('findings', {})

    # Summary
    if 'summary' in value_chain:
        output.append(f"**Overview**: {value_chain['summary']}\n")
        output.append("---\n")

    # Primary Activities
    primary = findings.get('primary_activities', {})
    if primary:
        output.append("### Primary Activities\n")
        for activity_key, activity_data in primary.items():
            # Format activity name (e.g., "inbound_logistics" -> "Inbound Logistics")
            activity_name = activity_key.replace('_', ' ').title()
            output.append(f"#### {activity_name}")
            output.append(f"{activity_data.get('description', '')}\n")

            # Key elements
            if 'key_elements' in activity_data:
                output.append("**Key Elements:**")
                for element in activity_data['key_elements']:
                    output.append(f"- {element}")
                output.append("")

            # Competitive advantage
            if 'competitive_advantage' in activity_data:
                output.append(f"*Competitive Advantage:* {activity_data['competitive_advantage']}\n")
        output.append("")

    # Support Activities
    support = findings.get('support_activities', {})
    if support:
        output.append("### Support Activities\n")
        for activity_key, activity_data in support.items():
            activity_name = activity_key.replace('_', ' ').title()
            output.append(f"#### {activity_name}")
            output.append(f"{activity_data.get('description', '')}\n")

            # Key elements
            if 'key_elements' in activity_data:
                output.append("**Key Elements:**")
                for element in activity_data['key_elements']:
                    output.append(f"- {element}")
                output.append("")

            # Competitive advantage
            if 'competitive_advantage' in activity_data:
                output.append(f"*Competitive Advantage:* {activity_data['competitive_advantage']}\n")
        output.append("")

    # Value Chain Integration
    if 'value_chain_integration' in findings:
        integration = findings['value_chain_integration']
        output.append("### Strategic Integration\n")

        if 'key_linkages' in integration:
            output.append("**Key Linkages:**")
            for linkage in integration['key_linkages']:
                output.append(f"- {linkage}")
            output.append("")

        if 'margin_creation' in integration:
            output.append("**Margin Creation:**")
            for margin in integration['margin_creation']:
                output.append(f"- {margin}")
            output.append("")

    return '\n'.join(output)
