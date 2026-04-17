import streamlit as st
import pandas as pd
import numpy as np
import math

# Page config
st.set_page_config(page_title="Line Allocation Prototypes", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select View", ["Streamlit Version", "HTML Prototype"])

# Custom CSS to match the mockup
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Clean table styling */
    div[data-testid="stDataFrame"] {
        font-size: 0.95rem;
    }

    div[data-testid="stDataFrame"] table {
        border-collapse: collapse;
    }

    /* Header styling */
    div[data-testid="stDataFrame"] thead tr th {
        background-color: #f3f4f6 !important;
        color: #374151 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #e5e7eb !important;
        padding: 12px 8px !important;
    }

    /* Row styling */
    div[data-testid="stDataFrame"] tbody tr td {
        padding: 10px 8px !important;
        border-bottom: 1px solid #e5e7eb !important;
    }

    /* Shift total rows */
    .shift-total-row {
        background-color: #f9fafb !important;
        font-weight: 600 !important;
    }

    h1 {
        color: #111827;
        font-weight: 700;
        font-size: 1.75rem;
        margin-bottom: 0.25rem;
    }

    .subtitle {
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Filter section */
    .stSelectbox label {
        font-weight: 500;
        color: #374151;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        background-color: white;
        color: #374151;
        font-weight: 500;
        padding: 0.5rem 1rem;
    }

    .stButton > button:hover {
        border-color: #9ca3af;
        background-color: #f9fafb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'expanded_rows' not in st.session_state:
    st.session_state.expanded_rows = set()

# Generate sample line allocation data
@st.cache_data
def generate_line_allocation_data():
    """Generate realistic line allocation data"""
    np.random.seed(42)

    shifts = [
        'thursday_night', 'friday_day', 'friday_night',
        'saturday_day', 'saturday_night', 'sunday_day',
        'sunday_night', 'monday_day'
    ]

    line_types = ['AUTO', '3Bay', 'LDL', 'EP', 'KT_Flexi', 'KT_HP', 'Flexi']

    line_configs = {
        'AUTO': {'max_lines': 4, 'hc_per_line': 10.33, 'runtime': 4.49, 'bph': 206},
        '3Bay': {'max_lines': 1, 'hc_per_line': 36, 'runtime': 8.98, 'bph': 159},
        'LDL': {'max_lines': 1, 'hc_per_line': 51.8, 'runtime': 8.49, 'bph': 131},
        'EP': {'max_lines': 1, 'hc_per_line': 17, 'runtime': 5.50, 'bph': 156},
        'KT_Flexi': {'max_lines': 1, 'hc_per_line': 20.67, 'runtime': 8.98, 'bph': 105},
        'KT_HP': {'max_lines': 1, 'hc_per_line': 15.25, 'runtime': 7.50, 'bph': 95},
        'Flexi': {'max_lines': 1, 'hc_per_line': 10, 'runtime': 8.59, 'bph': 110}
    }

    parent_rows = []
    child_rows = []

    for shift in shifts:
        active_line_types = np.random.choice(line_types, size=np.random.randint(3, 6), replace=False)

        for line_type in active_line_types:
            config = line_configs[line_type]

            if line_type == 'AUTO':
                num_lines = np.random.randint(2, config['max_lines'] + 1)
            else:
                num_lines = 1

            hc_per_line = config['hc_per_line']
            total_hc_calculated = hc_per_line * num_lines
            hc_allocated = math.ceil(total_hc_calculated)

            runtime_per_line = config['runtime']
            total_runtime = round(runtime_per_line * num_lines, 2)

            boxes_per_line = int(runtime_per_line * config['bph'])
            total_boxes = boxes_per_line * num_lines

            parent_rows.append({
                'row_id': f"{shift}_{line_type}",
                'shift': shift,
                'line_type': line_type,
                'total_lines': num_lines,
                'hc_allocated': hc_allocated,
                'total_line_runtime': total_runtime,
                'total_boxes': total_boxes
            })

            # Child rows
            for line_num in range(1, num_lines + 1):
                if line_type in ['KT_Flexi', 'KT_HP']:
                    total_hc = hc_per_line
                    bay1 = round(total_hc * 0.15, 2)
                    bay2 = round(total_hc * 0.35, 2)
                    bay3 = round(total_hc - bay1 - bay2, 2)
                    hc_breakdown = f"1Bay: {bay1}, 2Bay: {bay2}, 3Bay: {bay3}"
                else:
                    hc_breakdown = None

                child_rows.append({
                    'parent_id': f"{shift}_{line_type}",
                    'shift': shift,
                    'line_type': line_type,
                    'line_id': f"{line_type} Line {line_num}",
                    'hc': hc_per_line,
                    'hc_breakdown': hc_breakdown,
                    'runtime': runtime_per_line,
                    'boxes': boxes_per_line,
                    'bph': config['bph']
                })

    return pd.DataFrame(parent_rows), pd.DataFrame(child_rows)

df_parent, df_child = generate_line_allocation_data()

if page == "HTML Prototype":
    # HTML Prototype Page
    st.markdown("# 📊 Line Allocation Table - HTML Prototype")
    st.markdown('<p class="subtitle">Interactive table with sorting, filtering, and expandable rows</p>', unsafe_allow_html=True)

    import streamlit.components.v1 as components

    # Read the HTML file
    with open('line_allocation_table_prototype_fixed.html', 'r') as f:
        html_content = f.read()

    # Display the HTML
    components.html(html_content, height=900, scrolling=True)

    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #9ca3af; font-size: 0.875rem;">HTML Prototype • Ready for user testing</div>', unsafe_allow_html=True)

else:
    # Streamlit Version Page
    # Header
    st.markdown("# 📊 Line Allocation Table")
st.markdown('<p class="subtitle">View and drill down into line allocations by shift and line type</p>', unsafe_allow_html=True)

# Filters
col1, col2, col3, col4 = st.columns([1.5, 1.5, 1, 1])

    with col1:
        shift_options = ['All Shifts'] + sorted(df_parent['shift'].unique().tolist())
        selected_shift = st.selectbox("Shift", options=shift_options, index=0)

    with col2:
        line_type_options = ['All Lines'] + sorted(df_parent['line_type'].unique().tolist())
        selected_line_type = st.selectbox("Line Type", options=line_type_options, index=0)

    with col3:
        if st.button("⊞ Expand All"):
            st.session_state.expanded_rows = set(df_parent['row_id'].tolist())
            st.rerun()

    with col4:
        if st.button("⊟ Collapse All"):
            st.session_state.expanded_rows = set()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter data
    filtered_parent = df_parent.copy()

    if selected_shift != 'All Shifts':
        filtered_parent = filtered_parent[filtered_parent['shift'] == selected_shift]

    if selected_line_type != 'All Lines':
        filtered_parent = filtered_parent[filtered_parent['line_type'] == selected_line_type]

    # Build display dataframe
    display_data = []

    shifts_in_view = filtered_parent['shift'].unique()

    for shift in sorted(shifts_in_view):
        shift_data = filtered_parent[filtered_parent['shift'] == shift]

        for _, row in shift_data.iterrows():
            row_id = row['row_id']
            is_expanded = row_id in st.session_state.expanded_rows

            # Parent row
            display_data.append({
                '': '▼' if is_expanded else '▶',
                'Shift': shift,
                'Line Type': row['line_type'],
                'Total Lines': row['total_lines'],
                'HC Allocated': row['hc_allocated'],
                'Total Line Runtime (hrs)': f"{row['total_line_runtime']:.2f}",
                'Total Boxes': f"{row['total_boxes']:,}",
                '_row_id': row_id,
                '_row_type': 'parent'
            })

            # Child rows if expanded
            if is_expanded:
                child_data = df_child[df_child['parent_id'] == row_id]

                for _, child in child_data.iterrows():
                    if child['hc_breakdown']:
                        # Kitting line
                        display_data.append({
                            '': '  ',
                            'Shift': f"    {child['line_id']}",
                            'Line Type': f"HC: {child['hc']:.2f}",
                            'Total Lines': child['hc_breakdown'],
                            'HC Allocated': '',
                            'Total Line Runtime (hrs)': f"{child['runtime']:.2f}",
                            'Total Boxes': f"{child['boxes']:,}",
                            '_row_id': f"{row_id}_child",
                            '_row_type': 'child'
                        })
                    else:
                        # Regular line
                        display_data.append({
                            '': '  ',
                            'Shift': f"    {child['line_id']}",
                            'Line Type': f"HC: {child['hc']:.2f}",
                            'Total Lines': f"Runtime: {child['runtime']:.2f}h",
                            'HC Allocated': f"BPH: {child['bph']}",
                            'Total Line Runtime (hrs)': f"Boxes: {child['boxes']:,}",
                            'Total Boxes': '',
                            '_row_id': f"{row_id}_child",
                            '_row_type': 'child'
                        })

        # Shift total
        shift_total_lines = shift_data['total_lines'].sum()
        shift_total_hc = shift_data['hc_allocated'].sum()
        shift_total_runtime = shift_data['total_line_runtime'].sum()
        shift_total_boxes = shift_data['total_boxes'].sum()

        display_data.append({
            '': '',
            'Shift': 'SHIFT TOTAL',
            'Line Type': '',
            'Total Lines': int(shift_total_lines),
            'HC Allocated': int(shift_total_hc),
            'Total Line Runtime (hrs)': f"{shift_total_runtime:.2f}",
            'Total Boxes': f"{int(shift_total_boxes):,}",
            '_row_id': f"total_{shift}",
            '_row_type': 'total'
        })

    display_df = pd.DataFrame(display_data)

    # Display table with click handling
    st.markdown("### Line Allocations")

    selection = st.dataframe(
        display_df[['', 'Shift', 'Line Type', 'Total Lines', 'HC Allocated', 'Total Line Runtime (hrs)', 'Total Boxes']],
        use_container_width=True,
        hide_index=True,
        height=600,
        on_select="rerun",
        selection_mode="single-row"
    )

    # Handle row clicks
    if selection.selection.rows:
        clicked_idx = selection.selection.rows[0]
        clicked_row = display_df.iloc[clicked_idx]

        if clicked_row['_row_type'] == 'parent':
            row_id = clicked_row['_row_id']
            if row_id in st.session_state.expanded_rows:
                st.session_state.expanded_rows.remove(row_id)
            else:
                st.session_state.expanded_rows.add(row_id)
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #9ca3af; font-size: 0.875rem;">Line Allocation Table • Riptide v2</div>', unsafe_allow_html=True)
