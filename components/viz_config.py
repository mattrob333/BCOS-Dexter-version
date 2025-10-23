"""
Visualization Configuration and Styling.

Centralized configuration for Business Model Canvas and Value Chain visualizations.
"""

# Business Model Canvas Colors (Clean, readable palette)
BMC_COLORS = {
    'key_partners': '#FFFFFF',          # White
    'key_activities': '#F5F5F5',        # Off-white
    'key_resources': '#F5F5F5',         # Off-white
    'value_propositions': '#E8F4F8',    # Very light blue (central, most important)
    'customer_relationships': '#F5F5F5',# Off-white
    'channels': '#F5F5F5',              # Off-white
    'customer_segments': '#FFFFFF',     # White
    'cost_structure': '#FFF8DC',        # Light cream
    'revenue_streams': '#F0FFF0'        # Very light green
}

# Value Chain Colors (Porter's Value Chain palette)
VALUE_CHAIN_COLORS = {
    'primary': '#4A90E2',      # Blue
    'support': '#7B68EE',      # Medium slate blue
    'margin': '#50C878',       # Emerald green
    'text': '#2C3E50'          # Dark gray for text
}

# Typography
FONT_CONFIG = {
    'family': 'Arial, sans-serif',
    'title_size': 18,
    'section_title_size': 14,
    'content_size': 11,
    'small_size': 9
}

# Business Model Canvas Layout (Strategyzer proportions)
# The official BMC has specific width ratios
BMC_LAYOUT = {
    'width': 1400,
    'height': 900,
    'margin': {'l': 20, 'r': 20, 't': 60, 'b': 20},

    # Column widths (proportional)
    'col_widths': [0.22, 0.22, 0.22, 0.17, 0.17],  # 5 columns

    # Section positions (x, y, width, height) as fractions of total
    'sections': {
        'key_partners': {
            'x': 0.02, 'y': 0.15, 'width': 0.18, 'height': 0.70,
            'title': 'Key Partners'
        },
        'key_activities': {
            'x': 0.22, 'y': 0.15, 'width': 0.18, 'height': 0.35,
            'title': 'Key Activities'
        },
        'key_resources': {
            'x': 0.22, 'y': 0.52, 'width': 0.18, 'height': 0.33,
            'title': 'Key Resources'
        },
        'value_propositions': {
            'x': 0.42, 'y': 0.15, 'width': 0.18, 'height': 0.70,
            'title': 'Value Propositions'
        },
        'customer_relationships': {
            'x': 0.62, 'y': 0.15, 'width': 0.18, 'height': 0.35,
            'title': 'Customer Relationships'
        },
        'channels': {
            'x': 0.62, 'y': 0.52, 'width': 0.18, 'height': 0.33,
            'title': 'Channels'
        },
        'customer_segments': {
            'x': 0.82, 'y': 0.15, 'width': 0.16, 'height': 0.70,
            'title': 'Customer Segments'
        },
        'cost_structure': {
            'x': 0.02, 'y': 0.02, 'width': 0.48, 'height': 0.11,
            'title': 'Cost Structure'
        },
        'revenue_streams': {
            'x': 0.52, 'y': 0.02, 'width': 0.46, 'height': 0.11,
            'title': 'Revenue Streams'
        }
    }
}

# Value Chain Layout (Porter's model)
VALUE_CHAIN_LAYOUT = {
    'width': 1400,
    'height': 800,
    'margin': {'l': 40, 'r': 100, 't': 60, 'b': 40},

    # Primary activities (bottom row)
    'primary_activities': {
        'y': 0.50,
        'height': 0.35,
        'sections': [
            {'name': 'Inbound Logistics', 'x': 0.05, 'width': 0.15},
            {'name': 'Operations', 'x': 0.22, 'width': 0.15},
            {'name': 'Outbound Logistics', 'x': 0.39, 'width': 0.15},
            {'name': 'Marketing & Sales', 'x': 0.56, 'width': 0.15},
            {'name': 'Service', 'x': 0.73, 'width': 0.15}
        ]
    },

    # Support activities (top row)
    'support_activities': {
        'y': 0.15,
        'height': 0.30,
        'sections': [
            {'name': 'Firm Infrastructure', 'x': 0.05, 'width': 0.83},
            {'name': 'Human Resource Management', 'x': 0.05, 'width': 0.83},
            {'name': 'Technology Development', 'x': 0.05, 'width': 0.83},
            {'name': 'Procurement', 'x': 0.05, 'width': 0.83}
        ]
    },

    # Margin box (the visual element on the right side)
    'margin_box': {
        'x': 0.90,
        'y': 0.15,
        'width': 0.08,
        'height': 0.70
    }
}

# Export settings
EXPORT_CONFIG = {
    'formats': ['png', 'svg', 'pdf'],
    'png': {
        'width': 2000,
        'height': 1200,
        'scale': 2
    },
    'svg': {
        'width': 1400,
        'height': 900
    },
    'pdf': {
        'width': 11,  # inches
        'height': 8.5  # inches
    }
}

# Print optimization
PRINT_CONFIG = {
    'dpi': 300,
    'paper_size': 'letter',  # or 'a4'
    'orientation': 'landscape',
    'margins': {
        'top': 0.5,
        'bottom': 0.5,
        'left': 0.5,
        'right': 0.5
    }
}

# Interactive settings
INTERACTIVE_CONFIG = {
    'hover_bg_opacity': 0.3,
    'click_highlight_color': '#FFD700',  # Gold
    'edit_mode_border': '#FF6347',       # Tomato red
    'transition_duration': 200  # milliseconds
}
