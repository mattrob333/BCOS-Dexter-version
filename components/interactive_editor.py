"""
Interactive Editing Functionality for Visualizations.

Provides real-time editing capabilities for BMC and Value Chain sections
with Streamlit session state management.
"""

import streamlit as st
from typing import Dict, Any, List, Optional, Tuple
import json


def init_edit_session_state():
    """Initialize session state variables for editing."""
    if 'editing_mode' not in st.session_state:
        st.session_state.editing_mode = False

    if 'edited_bmc' not in st.session_state:
        st.session_state.edited_bmc = None

    if 'edited_value_chain' not in st.session_state:
        st.session_state.edited_value_chain = None

    if 'current_edit_section' not in st.session_state:
        st.session_state.current_edit_section = None


def toggle_edit_mode():
    """Toggle editing mode on/off."""
    st.session_state.editing_mode = not st.session_state.editing_mode


def edit_bmc_section(
    section_name: str,
    section_key: str,
    current_data: List[str],
    bmc_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Provide UI for editing a BMC section.

    Args:
        section_name: Display name of the section
        section_key: Internal key for the section
        current_data: Current list of items in the section
        bmc_data: Full BMC data dictionary

    Returns:
        Updated BMC data
    """
    st.subheader(f"Edit: {section_name}")

    # Initialize edited BMC if not exists
    if st.session_state.edited_bmc is None:
        st.session_state.edited_bmc = bmc_data.copy()

    # Get current items
    current_items = st.session_state.edited_bmc.get(section_key, [])

    # Display current items with delete option
    st.write("**Current Items:**")
    items_to_keep = []

    for i, item in enumerate(current_items):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(item)
        with col2:
            if st.button("Delete", key=f"del_{section_key}_{i}"):
                continue  # Skip this item (delete it)
        items_to_keep.append(item)

    # Add new item
    st.write("**Add New Item:**")
    new_item = st.text_area(
        "Enter new item",
        key=f"new_{section_key}",
        height=100,
        placeholder=f"Add a new {section_name.lower()} item..."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Item", key=f"add_{section_key}"):
            if new_item.strip():
                items_to_keep.append(new_item.strip())
                st.success(f"Added new item to {section_name}")

    with col2:
        if st.button("Save Changes", key=f"save_{section_key}"):
            st.session_state.edited_bmc[section_key] = items_to_keep
            st.success(f"Saved changes to {section_name}")
            return st.session_state.edited_bmc

    # Update temporary state
    st.session_state.edited_bmc[section_key] = items_to_keep

    return st.session_state.edited_bmc


def edit_value_chain_activity(
    activity_name: str,
    activity_key: str,
    current_data: Dict[str, Any],
    vc_data: Dict[str, Any],
    is_primary: bool = True
) -> Dict[str, Any]:
    """
    Provide UI for editing a Value Chain activity.

    Args:
        activity_name: Display name of the activity
        activity_key: Internal key for the activity
        current_data: Current activity data
        vc_data: Full value chain data
        is_primary: Whether this is a primary activity

    Returns:
        Updated value chain data
    """
    st.subheader(f"Edit: {activity_name}")

    # Initialize edited value chain if not exists
    if st.session_state.edited_value_chain is None:
        st.session_state.edited_value_chain = vc_data.copy()

    # Get activity type
    activity_type = 'primary_activities' if is_primary else 'support_activities'

    # Get current activity data
    current_activity = st.session_state.edited_value_chain.get(activity_type, {}).get(activity_key, {})

    # Edit description
    st.write("**Description:**")
    new_description = st.text_area(
        "Description",
        value=current_activity.get('description', ''),
        key=f"desc_{activity_key}",
        height=100
    )

    # Edit key elements
    st.write("**Key Elements:**")
    current_elements = current_activity.get('key_elements', [])

    elements_to_keep = []
    for i, element in enumerate(current_elements):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(element)
        with col2:
            if st.button("Delete", key=f"del_elem_{activity_key}_{i}"):
                continue
        elements_to_keep.append(element)

    # Add new element
    new_element = st.text_input(
        "Add new key element",
        key=f"new_elem_{activity_key}",
        placeholder="Enter a key element..."
    )

    if st.button("Add Element", key=f"add_elem_{activity_key}"):
        if new_element.strip():
            elements_to_keep.append(new_element.strip())
            st.success("Added new element")

    # Edit competitive advantage
    st.write("**Competitive Advantage:**")
    new_comp_adv = st.text_area(
        "Competitive Advantage",
        value=current_activity.get('competitive_advantage', ''),
        key=f"comp_{activity_key}",
        height=100
    )

    # Save button
    if st.button("Save Changes", key=f"save_{activity_key}"):
        # Update the activity
        if activity_type not in st.session_state.edited_value_chain:
            st.session_state.edited_value_chain[activity_type] = {}

        st.session_state.edited_value_chain[activity_type][activity_key] = {
            'description': new_description,
            'key_elements': elements_to_keep,
            'competitive_advantage': new_comp_adv
        }

        st.success(f"Saved changes to {activity_name}")
        return st.session_state.edited_value_chain

    # Update temporary state
    if activity_type not in st.session_state.edited_value_chain:
        st.session_state.edited_value_chain[activity_type] = {}

    st.session_state.edited_value_chain[activity_type][activity_key] = {
        'description': new_description,
        'key_elements': elements_to_keep,
        'competitive_advantage': new_comp_adv
    }

    return st.session_state.edited_value_chain


def save_edited_data_to_file(
    edited_data: Dict[str, Any],
    output_path: str,
    data_type: str = 'bmc'
) -> bool:
    """
    Save edited data back to JSON file.

    Args:
        edited_data: Edited BMC or Value Chain data
        output_path: Path to output JSON file
        data_type: Type of data ('bmc' or 'value_chain')

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read existing file
        with open(output_path, 'r') as f:
            full_data = json.load(f)

        # Update the relevant section
        if data_type == 'bmc':
            if 'phase1' in full_data:
                full_data['phase1']['business_model_canvas'] = edited_data
            else:
                full_data['business_model_canvas'] = edited_data
        elif data_type == 'value_chain':
            if 'phase1' in full_data:
                full_data['phase1']['value_chain'] = edited_data
            else:
                full_data['value_chain'] = edited_data

        # Write back to file
        with open(output_path, 'w') as f:
            json.dump(full_data, f, indent=2)

        return True

    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False


def render_edit_panel(
    data_type: str,
    data: Dict[str, Any],
    section_options: Dict[str, str]
) -> Optional[Dict[str, Any]]:
    """
    Render a sidebar edit panel for BMC or Value Chain.

    Args:
        data_type: Type of data ('bmc' or 'value_chain')
        data: Current data dictionary
        section_options: Dictionary mapping section keys to display names

    Returns:
        Updated data if changes were made, None otherwise
    """
    st.sidebar.header(f"Edit {data_type.upper()}")

    # Section selector
    section_key = st.sidebar.selectbox(
        "Select section to edit:",
        options=list(section_options.keys()),
        format_func=lambda x: section_options[x]
    )

    if section_key:
        st.sidebar.markdown("---")

        if data_type == 'bmc':
            section_data = data.get(section_key, [])
            updated_data = edit_bmc_section(
                section_options[section_key],
                section_key,
                section_data,
                data
            )
            return updated_data

        elif data_type == 'value_chain':
            # Determine if primary or support
            is_primary = section_key in ['inbound_logistics', 'operations', 'outbound_logistics', 'marketing_sales', 'service']

            activity_type = 'primary_activities' if is_primary else 'support_activities'
            activity_data = data.get(activity_type, {}).get(section_key, {})

            updated_data = edit_value_chain_activity(
                section_options[section_key],
                section_key,
                activity_data,
                data,
                is_primary
            )
            return updated_data

    return None


def get_bmc_section_options() -> Dict[str, str]:
    """Get BMC section options for editing."""
    return {
        'key_partners': 'Key Partners',
        'key_activities': 'Key Activities',
        'key_resources': 'Key Resources',
        'value_propositions': 'Value Propositions',
        'customer_relationships': 'Customer Relationships',
        'channels': 'Channels',
        'customer_segments': 'Customer Segments',
        'cost_structure': 'Cost Structure',
        'revenue_streams': 'Revenue Streams'
    }


def get_value_chain_section_options() -> Dict[str, str]:
    """Get Value Chain section options for editing."""
    return {
        # Primary activities
        'inbound_logistics': 'Inbound Logistics',
        'operations': 'Operations',
        'outbound_logistics': 'Outbound Logistics',
        'marketing_sales': 'Marketing & Sales',
        'service': 'Service',
        # Support activities
        'firm_infrastructure': 'Firm Infrastructure',
        'hrm': 'Human Resource Management',
        'technology_development': 'Technology Development',
        'procurement': 'Procurement'
    }
