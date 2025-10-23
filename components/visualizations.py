"""
Interactive Plotly Visualizations for BCOS.

Creates professional, interactive Business Model Canvas and Value Chain diagrams
using Plotly with Strategyzer-style layouts.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Optional
import os

from .viz_config import (
    BMC_COLORS, BMC_LAYOUT, VALUE_CHAIN_COLORS, VALUE_CHAIN_LAYOUT,
    FONT_CONFIG, EXPORT_CONFIG
)
from .data_transformers import get_hover_text, format_text_for_display


def create_business_model_canvas(bmc_data: Dict[str, Any], title: str = "Business Model Canvas") -> go.Figure:
    """
    Create interactive Business Model Canvas visualization with Strategyzer-style layout.

    Args:
        bmc_data: Structured BMC data with 9 sections
        title: Title for the canvas

    Returns:
        Plotly Figure object
    """
    # Create figure
    fig = go.Figure()

    # Canvas dimensions
    width = BMC_LAYOUT['width']
    height = BMC_LAYOUT['height']

    # Add each BMC section as a shape + annotation
    sections = BMC_LAYOUT['sections']

    for section_key, section_config in sections.items():
        # Get section data
        section_items = bmc_data.get(section_key, [])
        if not isinstance(section_items, list):
            section_items = [str(section_items)]

        # Calculate absolute positions
        x0 = section_config['x'] * width
        y0 = section_config['y'] * height
        x1 = (section_config['x'] + section_config['width']) * width
        y1 = (section_config['y'] + section_config['height']) * height

        # Section color
        color = BMC_COLORS.get(section_key, '#EFEFEF')

        # Add rectangle shape
        fig.add_shape(
            type="rect",
            x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color="#333333", width=2),
            fillcolor=color,
            opacity=0.7,
            layer='below'
        )

        # Add section title
        title_y = y1 - 30  # Near top of section
        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=title_y,
            text=f"<b>{section_config['title']}</b>",
            showarrow=False,
            font=dict(size=FONT_CONFIG['section_title_size'], family=FONT_CONFIG['family']),
            xanchor='center',
            yanchor='top'
        )

        # Add section content
        content_y = title_y - 35  # Below title
        content_text = _format_section_content(section_items, max_items=5)

        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=content_y,
            text=content_text,
            showarrow=False,
            font=dict(size=FONT_CONFIG['content_size'], family=FONT_CONFIG['family']),
            xanchor='center',
            yanchor='top',
            align='left'
        )

        # Add invisible scatter point for hover interactivity
        hover_text = get_hover_text(section_config['title'], section_items)
        fig.add_trace(go.Scatter(
            x=[(x0 + x1) / 2],
            y=[(y0 + y1) / 2],
            mode='markers',
            marker=dict(size=0.1, opacity=0),
            hovertext=hover_text,
            hoverinfo='text',
            name=section_config['title'],
            showlegend=False
        ))

    # Update layout
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=FONT_CONFIG['title_size'], family=FONT_CONFIG['family']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            range=[0, width],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[0, height],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        width=width,
        height=height,
        margin=BMC_LAYOUT['margin'],
        plot_bgcolor='white',
        hovermode='closest',
        dragmode='pan'
    )

    return fig


def create_value_chain_diagram(vc_data: Dict[str, Any], title: str = "Value Chain Analysis") -> go.Figure:
    """
    Create interactive Value Chain visualization (Porter's model).

    Args:
        vc_data: Structured value chain data with primary and support activities
        title: Title for the diagram

    Returns:
        Plotly Figure object
    """
    # Create figure
    fig = go.Figure()

    # Canvas dimensions
    width = VALUE_CHAIN_LAYOUT['width']
    height = VALUE_CHAIN_LAYOUT['height']

    # Get activities data
    primary = vc_data.get('primary_activities', {})
    support = vc_data.get('support_activities', {})

    # Add primary activities (bottom row)
    primary_config = VALUE_CHAIN_LAYOUT['primary_activities']
    primary_sections = primary_config['sections']

    for section in primary_sections:
        section_name_key = section['name'].lower().replace(' ', '_').replace('&', 'and')
        activity_data = primary.get(section_name_key, {})

        # Calculate positions
        x0 = section['x'] * width
        y0 = primary_config['y'] * height
        x1 = (section['x'] + section['width']) * width
        y1 = (primary_config['y'] + primary_config['height']) * height

        # Add rectangle
        fig.add_shape(
            type="rect",
            x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color="#2C3E50", width=2),
            fillcolor=VALUE_CHAIN_COLORS['primary'],
            opacity=0.6,
            layer='below'
        )

        # Add title
        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=y1 - 25,
            text=f"<b>{section['name']}</b>",
            showarrow=False,
            font=dict(size=FONT_CONFIG['section_title_size'], family=FONT_CONFIG['family'], color='white'),
            xanchor='center',
            yanchor='top'
        )

        # Add hover point
        description = activity_data.get('description', '')
        key_elements = activity_data.get('key_elements', [])
        comp_adv = activity_data.get('competitive_advantage', '')

        hover_text = f"<b>{section['name']}</b><br><br>"
        if description:
            hover_text += f"{format_text_for_display(description, 100)}<br><br>"
        if key_elements:
            hover_text += "<b>Key Elements:</b><br>"
            for elem in key_elements[:3]:
                hover_text += f"• {elem}<br>"
        if comp_adv:
            hover_text += f"<br><b>Competitive Advantage:</b><br>{format_text_for_display(comp_adv, 100)}"

        fig.add_trace(go.Scatter(
            x=[(x0 + x1) / 2],
            y=[(y0 + y1) / 2],
            mode='markers',
            marker=dict(size=0.1, opacity=0),
            hovertext=hover_text,
            hoverinfo='text',
            name=section['name'],
            showlegend=False
        ))

    # Add support activities (top section, stacked)
    support_config = VALUE_CHAIN_LAYOUT['support_activities']
    support_sections = support_config['sections']
    support_names = ['Firm Infrastructure', 'Human Resource Management', 'Technology Development', 'Procurement']
    support_keys = ['firm_infrastructure', 'hrm', 'technology_development', 'procurement']

    # Each support activity gets 1/4 of the height
    support_height_each = support_config['height'] / 4

    for i, (name, key) in enumerate(zip(support_names, support_keys)):
        activity_data = support.get(key, {})

        # Calculate positions
        x0 = 0.05 * width
        y0 = (support_config['y'] + (i * support_height_each / support_config['height']) * support_config['height']) * height
        x1 = 0.88 * width
        y1 = (support_config['y'] + ((i + 1) * support_height_each / support_config['height']) * support_config['height']) * height

        # Add rectangle
        fig.add_shape(
            type="rect",
            x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color="#2C3E50", width=2),
            fillcolor=VALUE_CHAIN_COLORS['support'],
            opacity=0.5,
            layer='below'
        )

        # Add title
        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=(y0 + y1) / 2,
            text=f"<b>{name}</b>",
            showarrow=False,
            font=dict(size=FONT_CONFIG['content_size'], family=FONT_CONFIG['family'], color='white'),
            xanchor='center',
            yanchor='middle'
        )

        # Add hover point
        description = activity_data.get('description', '')
        key_elements = activity_data.get('key_elements', [])
        comp_adv = activity_data.get('competitive_advantage', '')

        hover_text = f"<b>{name}</b><br><br>"
        if description:
            hover_text += f"{format_text_for_display(description, 100)}<br><br>"
        if key_elements:
            hover_text += "<b>Key Elements:</b><br>"
            for elem in key_elements[:3]:
                hover_text += f"• {elem}<br>"
        if comp_adv:
            hover_text += f"<br><b>Competitive Advantage:</b><br>{format_text_for_display(comp_adv, 100)}"

        fig.add_trace(go.Scatter(
            x=[(x0 + x1) / 2],
            y=[(y0 + y1) / 2],
            mode='markers',
            marker=dict(size=0.1, opacity=0),
            hovertext=hover_text,
            hoverinfo='text',
            name=name,
            showlegend=False
        ))

    # Add margin arrow on the right
    margin_config = VALUE_CHAIN_LAYOUT['margin_box']
    margin_x0 = margin_config['x'] * width
    margin_y0 = margin_config['y'] * height
    margin_x1 = (margin_config['x'] + margin_config['width']) * width
    margin_y1 = (margin_config['y'] + margin_config['height']) * height

    # Margin rectangle
    fig.add_shape(
        type="rect",
        x0=margin_x0, y0=margin_y0, x1=margin_x1, y1=margin_y1,
        line=dict(color="#2C3E50", width=2),
        fillcolor=VALUE_CHAIN_COLORS['margin'],
        opacity=0.7,
        layer='below'
    )

    # Margin text (vertical)
    fig.add_annotation(
        x=(margin_x0 + margin_x1) / 2,
        y=(margin_y0 + margin_y1) / 2,
        text="<b>M<br>A<br>R<br>G<br>I<br>N</b>",
        showarrow=False,
        font=dict(size=FONT_CONFIG['section_title_size'], family=FONT_CONFIG['family'], color='white'),
        xanchor='center',
        yanchor='middle'
    )

    # Update layout
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=FONT_CONFIG['title_size'], family=FONT_CONFIG['family']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            range=[0, width],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[0, height],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        width=width,
        height=height,
        margin=dict(l=40, r=100, t=60, b=40),
        plot_bgcolor='white',
        hovermode='closest',
        dragmode='pan'
    )

    return fig


def export_to_image(fig: go.Figure, filename: str, format: str = 'png', output_dir: Optional[str] = None) -> str:
    """
    Export Plotly figure to image file.

    Args:
        fig: Plotly figure to export
        filename: Output filename (without extension)
        format: Export format ('png', 'svg', 'pdf')
        output_dir: Output directory (defaults to current directory)

    Returns:
        Path to exported file
    """
    if output_dir is None:
        output_dir = os.getcwd()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Build full path
    full_path = os.path.join(output_dir, f"{filename}.{format}")

    # Export based on format
    if format == 'png':
        config = EXPORT_CONFIG['png']
        fig.write_image(
            full_path,
            format='png',
            width=config['width'],
            height=config['height'],
            scale=config['scale']
        )
    elif format == 'svg':
        config = EXPORT_CONFIG['svg']
        fig.write_image(
            full_path,
            format='svg',
            width=config['width'],
            height=config['height']
        )
    elif format == 'pdf':
        fig.write_image(full_path, format='pdf')
    else:
        raise ValueError(f"Unsupported format: {format}")

    return full_path


def _format_section_content(items: List[str], max_items: int = 5) -> str:
    """
    Format section content for display in BMC.

    Args:
        items: List of items to display
        max_items: Maximum number of items to show

    Returns:
        Formatted HTML string
    """
    if not items:
        return "<i>No data</i>"

    # Take top N items
    display_items = items[:max_items]

    # Format as bullet list
    formatted_lines = []
    for item in display_items:
        # Truncate long items
        clean_item = format_text_for_display(item, 80)
        formatted_lines.append(f"• {clean_item}")

    # Add "and more" if truncated
    if len(items) > max_items:
        formatted_lines.append(f"<i>... +{len(items) - max_items} more</i>")

    return "<br>".join(formatted_lines)
