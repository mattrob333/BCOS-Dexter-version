"""
Data Transformation Utilities.

Transforms analysis results into visualization-ready format.
Handles missing data gracefully and provides fallbacks.
"""

from typing import Dict, Any, List


def transform_bmc_for_visualization(phase1_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform Phase 1 results into Business Model Canvas visualization format.

    Args:
        phase1_results: Phase 1 analysis results containing BMC data

    Returns:
        Dictionary with structured BMC data for visualization
    """
    # Extract BMC data
    bmc_raw = phase1_results.get('business_model_canvas', {})
    company_intel = phase1_results.get('company_intelligence', {})

    # Initialize structured BMC
    bmc_viz = {
        'key_partners': _extract_list_items(bmc_raw.get('key_partnerships', [])),
        'key_activities': _extract_list_items(bmc_raw.get('key_activities', [])),
        'key_resources': _extract_list_items(bmc_raw.get('key_resources', [])),
        'value_propositions': _extract_value_propositions(bmc_raw.get('value_propositions', [])),
        'customer_relationships': _extract_list_items(bmc_raw.get('customer_relationships', [])),
        'channels': _extract_list_items(bmc_raw.get('channels', [])),
        'customer_segments': _extract_customer_segments(bmc_raw.get('customer_segments', [])),
        'cost_structure': _extract_list_items(bmc_raw.get('cost_structure', [])),
        'revenue_streams': _extract_list_items(bmc_raw.get('revenue_streams', []))
    }

    # Fallback to company intelligence if BMC sections are empty
    if not any(bmc_viz.values()):
        bmc_viz = _generate_fallback_bmc(company_intel)

    return bmc_viz


def transform_value_chain_for_visualization(phase1_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform Phase 1 results into Value Chain visualization format.

    Args:
        phase1_results: Phase 1 analysis results containing value chain data

    Returns:
        Dictionary with structured value chain data for visualization
    """
    vc_raw = phase1_results.get('value_chain', {})
    findings = vc_raw.get('findings', {})

    # Primary activities
    primary_raw = findings.get('primary_activities', {})
    primary_activities = {
        'inbound_logistics': _extract_activity(primary_raw.get('inbound_logistics', {})),
        'operations': _extract_activity(primary_raw.get('operations', {})),
        'outbound_logistics': _extract_activity(primary_raw.get('outbound_logistics', {})),
        'marketing_sales': _extract_activity(primary_raw.get('marketing_sales', {}) or primary_raw.get('marketing_and_sales', {})),
        'service': _extract_activity(primary_raw.get('service', {}))
    }

    # Support activities
    support_raw = findings.get('support_activities', {})
    support_activities = {
        'firm_infrastructure': _extract_activity(support_raw.get('firm_infrastructure', {})),
        'hrm': _extract_activity(support_raw.get('human_resource_management', {}) or support_raw.get('hrm', {})),
        'technology_development': _extract_activity(support_raw.get('technology_development', {})),
        'procurement': _extract_activity(support_raw.get('procurement', {}))
    }

    # Overall summary
    summary = vc_raw.get('summary', 'Value chain analysis for strategic positioning')

    return {
        'primary_activities': primary_activities,
        'support_activities': support_activities,
        'summary': summary
    }


def _extract_list_items(items: Any, max_items: int = 5) -> List[str]:
    """Extract text items from list of dictionaries or strings."""
    if not items:
        return []

    # DEFENSIVE: Handle dict vs list
    if isinstance(items, dict):
        # Convert dict values to list
        items = list(items.values())
    elif not isinstance(items, list):
        # Not a list or dict - return empty
        return []

    result = []
    for item in items[:max_items]:
        if isinstance(item, dict):
            # Try common keys
            text = (item.get('description') or
                   item.get('activity') or
                   item.get('resource_type') or
                   item.get('stream_type') or
                   item.get('cost_category') or
                   item.get('partner_type') or
                   item.get('channel_type') or
                   item.get('relationship_type') or
                   str(item))
            result.append(str(text))
        else:
            result.append(str(item))

    return result


def _extract_value_propositions(vps: List[Any]) -> List[str]:
    """Extract value propositions in readable format."""
    if not vps:
        return []

    result = []
    for vp in vps[:3]:  # Top 3
        if isinstance(vp, dict):
            segment = vp.get('for_segment', 'Customers')
            value = vp.get('core_value', vp.get('description', ''))
            if value:
                result.append(f"{segment}: {value}")
        else:
            result.append(str(vp))

    return result


def _extract_customer_segments(segments: List[Any]) -> List[str]:
    """Extract customer segments in readable format."""
    if not segments:
        return []

    result = []
    for seg in segments[:4]:  # Top 4
        if isinstance(seg, dict):
            name = seg.get('segment_name', '')
            desc = seg.get('description', '')
            if name:
                result.append(f"{name}: {desc}" if desc else name)
        else:
            result.append(str(seg))

    return result


def _extract_activity(activity: Dict[str, Any]) -> Dict[str, Any]:
    """Extract activity data for value chain."""
    if not activity:
        return {
            'description': '',
            'key_elements': [],
            'competitive_advantage': ''
        }

    return {
        'description': activity.get('description', ''),
        'key_elements': activity.get('key_elements', [])[:3],  # Top 3 elements
        'competitive_advantage': activity.get('competitive_advantage', '')
    }


def _generate_fallback_bmc(company_intel: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate fallback BMC from company intelligence if BMC data is missing.

    Args:
        company_intel: Company intelligence data

    Returns:
        Basic BMC structure
    """
    overview = company_intel.get('overview', {})
    products = company_intel.get('products', [])

    return {
        'key_partners': ['Strategic technology partners', 'Distribution partners'],
        'key_activities': ['Product development', 'Customer acquisition', 'Service delivery'],
        'key_resources': ['Technology platform', 'Brand', 'Customer data'],
        'value_propositions': [f"Product/Service: {overview.get('description', 'Value delivery')}"],
        'customer_relationships': ['Automated service', 'Personal assistance'],
        'channels': ['Website', 'Direct sales', 'Digital platforms'],
        'customer_segments': ['Enterprise customers', 'SMB customers'],
        'cost_structure': ['Technology development', 'Sales & marketing', 'Operations'],
        'revenue_streams': ['Subscription revenue', 'Transaction fees', 'Professional services']
    }


def format_text_for_display(text: str, max_length: int = 150) -> str:
    """
    Format text for display in visualization.

    Args:
        text: Input text
        max_length: Maximum length before truncation

    Returns:
        Formatted text
    """
    if not text:
        return ""

    # Truncate if too long
    if len(text) > max_length:
        return text[:max_length - 3] + "..."

    return text


def get_hover_text(section_name: str, items: List[str]) -> str:
    """
    Generate hover text for BMC sections.

    Args:
        section_name: Name of the BMC section
        items: List of items in the section

    Returns:
        Formatted hover text
    """
    if not items:
        return f"{section_name}<br><i>No data available</i>"

    # Build hover text
    hover_lines = [f"<b>{section_name}</b>", ""]

    for i, item in enumerate(items[:5], 1):  # Max 5 items in hover
        # Clean up text
        clean_item = format_text_for_display(item, 100)
        hover_lines.append(f"{i}. {clean_item}")

    if len(items) > 5:
        hover_lines.append(f"<br><i>... and {len(items) - 5} more</i>")

    return "<br>".join(hover_lines)
