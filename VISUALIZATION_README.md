# BCOS Interactive Visualizations

## Overview

This implementation adds **professional, interactive visualizations** for Business Model Canvas and Value Chain Analysis to the BCOS Streamlit web app using Plotly.

## Features Implemented

### ✅ Business Model Canvas
- **Strategyzer-style authentic layout** with properly sized sections
- **9 sections**: Key Partners, Key Activities, Key Resources, Value Propositions, Customer Relationships, Channels, Customer Segments, Cost Structure, Revenue Streams
- **Interactive hover** to see detailed content
- **Real-time editing** capability
- **Export to PNG, SVG, PDF**
- **Print-optimized** for reports

### ✅ Value Chain Analysis
- **Porter's Value Chain diagram** with two-tier layout
- **Primary Activities**: Inbound Logistics, Operations, Outbound Logistics, Marketing & Sales, Service
- **Support Activities**: Firm Infrastructure, HRM, Technology Development, Procurement
- **Margin indicator** on the right side
- **Interactive hover** with competitive advantage details
- **Real-time editing** capability
- **Export to PNG, SVG, PDF**

### ✅ Integration Features
- **Tabbed interface** in results view
- **Edit mode** with sidebar panel for section-by-section editing
- **Save edits** back to JSON files
- **Automatic data transformation** from analysis results
- **Graceful fallbacks** for missing data

## File Structure

```
BCOS-Dexter-version/
├── components/                     [NEW]
│   ├── __init__.py                # Package exports
│   ├── viz_config.py              # Styling and layout configuration
│   ├── data_transformers.py       # Transform analysis data for viz
│   ├── visualizations.py          # Core Plotly components
│   └── interactive_editor.py      # Editing functionality
├── app.py                          [MODIFIED] - Added viz tabs
├── requirements.txt                [MODIFIED] - Added kaleido
├── test_visualizations.py          [NEW] - Test script
└── VISUALIZATION_README.md         [NEW] - This file
```

## Installation

1. **Install new dependency**:
```bash
cd BCOS-Dexter-version
pip install kaleido>=0.2.1
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web App

```bash
cd BCOS-Dexter-version
streamlit run app.py
```

### Viewing Visualizations

1. **Complete an analysis** (Business Overview or Full Analysis)
2. **Navigate to results page**
3. **Click on visualization tabs**:
   - 📄 Executive Report (existing markdown)
   - 🎯 Business Model Canvas (new!)
   - ⛓️ Value Chain (new!)
   - 📈 Strategic Frameworks (if Phase 2 was run)

### Interactive Features

**Hover**: Hover over any section to see detailed content

**Edit Mode**:
1. Click "Edit Mode" checkbox
2. Select section from sidebar
3. Add, edit, or delete items
4. Click "Save to File" to persist changes

**Export**:
1. Click "Export as PNG/SVG/PDF" buttons
2. Files saved to session directory

## Testing

Run the test script to verify visualizations work:

```bash
cd BCOS-Dexter-version
python test_visualizations.py
```

This will:
- Test data transformers
- Generate sample BMC visualization
- Generate sample Value Chain visualization
- Save test HTML files for preview

## Configuration

### Customizing Colors

Edit `components/viz_config.py`:

```python
BMC_COLORS = {
    'key_partners': '#FFB6C1',
    'value_propositions': '#98FB98',
    # ... etc
}

VALUE_CHAIN_COLORS = {
    'primary': '#4A90E2',
    'support': '#7B68EE',
    'margin': '#50C878'
}
```

### Customizing Layout

Adjust section sizes in `viz_config.py`:

```python
BMC_LAYOUT = {
    'width': 1400,
    'height': 900,
    'sections': {
        'key_partners': {
            'x': 0.02, 'y': 0.15,
            'width': 0.18, 'height': 0.70
        },
        # ... etc
    }
}
```

### Export Settings

Configure export quality in `viz_config.py`:

```python
EXPORT_CONFIG = {
    'png': {
        'width': 2000,
        'height': 1200,
        'scale': 2  # Higher = better quality
    }
}
```

## Architecture

### Data Flow

```
Analysis Results (JSON)
    ↓
transform_bmc_for_visualization() / transform_value_chain_for_visualization()
    ↓
Structured Visualization Data
    ↓
create_business_model_canvas() / create_value_chain_diagram()
    ↓
Plotly Figure
    ↓
st.plotly_chart() (Display in Streamlit)
    ↓
export_to_image() (Optional export)
```

### Component Responsibilities

**viz_config.py**: All styling, colors, layouts, fonts
**data_transformers.py**: Extract and structure data from analysis results
**visualizations.py**: Create Plotly figures with interactive elements
**interactive_editor.py**: Provide editing UI and session state management
**app.py**: Integrate visualizations into Streamlit tabs

## Technical Details

### Plotly Features Used

- **Shapes**: Rectangles for BMC sections and Value Chain activities
- **Annotations**: Text labels and titles
- **Scatter traces**: Invisible points for hover interactivity
- **Custom hover text**: Rich HTML formatting
- **Static image export**: Using kaleido library

### Streamlit Integration

- **Tabs**: Separate views for different visualizations
- **Session state**: Track editing changes
- **Sidebar**: Edit panel when in edit mode
- **Plotly chart**: Native Streamlit component with full interactivity

### Data Transformation

- **Graceful degradation**: Works even with incomplete data
- **Fallback generation**: Creates basic BMC from company intelligence if needed
- **Type safety**: Handles lists, dicts, and strings flexibly
- **Text formatting**: Truncates long content, formats for display

## Troubleshooting

### "Module not found" errors

Install dependencies:
```bash
pip install plotly kaleido streamlit
```

### Visualizations not appearing

1. Check that analysis has BMC/Value Chain data in phase1 results
2. Look for errors in Streamlit console
3. Run test script to verify components work

### Export fails

1. Ensure kaleido is installed: `pip install kaleido`
2. Check write permissions for session directory
3. Try different export format (PNG vs SVG vs PDF)

### Edit mode not working

1. Check browser console for JavaScript errors
2. Refresh the page
3. Clear Streamlit cache: Settings → Clear cache

## Future Enhancements

Potential additions:
- [ ] Strategic framework visualizations (SWOT matrix, Porter's Five Forces diagram)
- [ ] Animated transitions between states
- [ ] Collaborative editing with user accounts
- [ ] Version history for edits
- [ ] Custom color themes
- [ ] Download all visualizations as PowerPoint
- [ ] AI-generated insights overlays

## Contributing

When adding new visualizations:

1. Add configuration to `viz_config.py`
2. Create visualization function in `visualizations.py`
3. Add data transformer in `data_transformers.py`
4. Integrate into `app.py` tabs
5. Add test to `test_visualizations.py`
6. Update this README

## License

Part of the BCOS project - see main project LICENSE.

## Credits

- **Business Model Canvas**: Based on Strategyzer's Business Model Canvas
- **Value Chain**: Based on Michael Porter's Value Chain Analysis
- **Plotly**: Interactive visualization library
- **Streamlit**: Web app framework

---

**Version**: 1.0.0
**Last Updated**: 2025-10-22
**Status**: Production Ready
