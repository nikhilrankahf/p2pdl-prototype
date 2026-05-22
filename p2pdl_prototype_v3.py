import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Riptide v2 - P2PDL Prototype", layout="wide")

# Custom CSS with modal styling
st.markdown("""
<style>
    .block-container {
        padding-top: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Push main content below Streamlit header */
    .main > div {
        padding-top: 1rem;
    }

    /* Simulation banner */
    .simulation-banner {
        background-color: #4169E1;
        color: white;
        padding: 0.75rem;
        text-align: center;
        font-weight: 600;
        margin: 0 -2rem 1.5rem -2rem;
    }

    /* Buttons */
    .stButton > button[kind="primary"] {
        background-color: #22c55e !important;
        color: white !important;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: none;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #16a34a !important;
    }

    button[key="hamburger"] {
        background-color: #374151 !important;
        color: white !important;
        border-radius: 6px;
        padding: 0.4rem 0.8rem !important;
        font-size: 1.2rem;
        border: none;
    }

    /* Modal overlay */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 999;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }

    .modal-content {
        background: white;
        border-radius: 12px;
        width: 90%;
        max-width: 1200px;
        max-height: 85vh;
        overflow-y: auto;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        padding: 2rem;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
    }

    .section-divider {
        border-top: 1px solid #e5e7eb;
        margin: 2rem 0;
    }

    /* Info boxes */
    .info-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }

    .success-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }

    .warning-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }

    .error-box {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }

    /* Metrics */
    .metric-container {
        background-color: #f9fafb;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }

    .config-section {
        background-color: #f9fafb;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
    }

    h1 { color: #111827; font-weight: 700; }
    h2 { color: #374151; font-weight: 600; font-size: 1.5rem; }
    h3 { color: #374151; font-weight: 600; }

    /* Ensure modal backdrop covers popover */
    [data-testid="stDialog"] {
        z-index: 9999 !important;
    }

    [data-testid="stDialog"]::backdrop {
        z-index: 9998 !important;
        background-color: rgba(0, 0, 0, 0.5) !important;
    }

    /* Hide popover when modal is open */
    [data-testid="stPopover"] {
        z-index: 1 !important;
    }

    /* Tab button styling */
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #f3f4f6 !important;
        color: #374151 !important;
    }

    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #e5e7eb !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = 'Production'
if 'show_config_modal' not in st.session_state:
    st.session_state.show_config_modal = False
if 'selected_lanes' not in st.session_state:
    st.session_state.selected_lanes = []
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
if 'promoted' not in st.session_state:
    st.session_state.promoted = False
if 'show_promotion_message' not in st.session_state:
    st.session_state.show_promotion_message = False
if 'popover_open' not in st.session_state:
    st.session_state.popover_open = False
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 'Planning'
if 'box_split_config' not in st.session_state:
    # Initialize default configuration: 75% 2P, 25% 4P for all box types
    st.session_state.box_split_config = {}
if 'box_split_saved' not in st.session_state:
    st.session_state.box_split_saved = {}
if 'box_split_modified' not in st.session_state:
    st.session_state.box_split_modified = False

# Default shifts
SHIFTS = [
    'Wednesday 1 Day', 'Wednesday 1 Night',
    'Thursday Day', 'Thursday Night',
    'Friday Day', 'Friday Night',
    'Saturday Day', 'Saturday Night',
    'Sunday Day', 'Sunday Night',
    'Monday Day', 'Monday Night',
    'Tuesday Day', 'Tuesday Night',
    'Wednesday 2 Day', 'Wednesday 2 Night'
]

PROCESS_PATHS = ['Auto', 'LDL', 'Manual Line', 'Grocery Line']
BOX_TYPES = ['M', 'G', 'T']

def initialize_box_split_config():
    """Initialize box split config with default 75/25 split"""
    config = {}
    for path in PROCESS_PATHS:
        config[path] = {}
        for shift in SHIFTS:
            config[path][shift] = {}
            for box_type in BOX_TYPES:
                config[path][shift][box_type] = {'2P': 75, '4P': 25}
    return config

# Initialize if empty
if not st.session_state.box_split_config:
    st.session_state.box_split_config = initialize_box_split_config()
    st.session_state.box_split_saved = initialize_box_split_config()

# Generate sample lane data
@st.cache_data
def generate_lane_data():
    np.random.seed(42)
    lanes = []
    brands = ['HF', 'EP']
    ship_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ship_day_full = {'Mon': 'MONDAY', 'Tue': 'TUESDAY', 'Wed': 'WEDNESDAY',
                     'Thu': 'THURSDAY', 'Fri': 'FRIDAY', 'Sat': 'SATURDAY', 'Sun': 'SUNDAY'}

    for i in range(50):
        lane_num = np.random.choice(['AIR-1', 'AIR-2', 'G-1', 'G-2', 'POROR', 'PORTO', 'LAXCA', 'SDGCA'])
        brand = np.random.choice(brands)
        ship_day_abbr = np.random.choice(ship_days)
        ship_day_name = ship_day_full[ship_day_abbr]

        # Create unique lane identifier
        lane_name = f'AZ_FEDEX-{lane_num}' + (f'_{brand}' if brand == 'EP' else '')
        lane_id = f'{lane_name}_{ship_day_name}_{i}'  # Unique identifier

        # CPT shows the ship day
        cpt_time = f"{np.random.randint(8,18):02d}:00"
        cpt = f"04-{np.random.randint(7,12):02d} ({ship_day_abbr}) {cpt_time}"

        lanes.append({
            'Lane_ID': lane_id,  # Unique identifier
            'Lane': lane_name,
            'Brand': brand,
            'Ship Day': ship_day_name,  # Full day name from CPT
            'CPT': cpt,
            'Box Volume': np.random.randint(50, 5000)
        })

    return pd.DataFrame(lanes)

df_lanes = generate_lane_data()

# Header - add spacing to avoid Streamlit header overlap
st.markdown('<div style="height: 2.5rem;"></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.5, 1.3, 1.3, 1.5, 2.9, 1, 1.5, 1.5])

with col1:
    st.markdown('<p style="font-size: 1.2rem; font-weight: 700; color: #111827; margin: 0.5rem 0;">⚡ Riptide</p>', unsafe_allow_html=True)

with col2:
    if st.button("📦 Planning", disabled=(st.session_state.current_tab == 'Planning'), use_container_width=True, key="planning_tab"):
        st.session_state.current_tab = 'Planning'
        st.rerun()

with col3:
    if st.button("🏭 Kitting", disabled=True, use_container_width=True, type="secondary", key="kitting_tab"):
        st.session_state.current_tab = 'Kitting'
        st.rerun()

with col4:
    if st.button("⚙️ Configuration", disabled=(st.session_state.current_tab == 'Configuration'), use_container_width=True, key="config_tab"):
        st.session_state.current_tab = 'Configuration'
        st.rerun()

with col6:
    st.selectbox("DC", options=['AZ'], index=0, key='dc_selector', label_visibility='visible', disabled=True)

with col7:
    st.selectbox("Week", options=['2026-W22'], index=0, key='week_selector', label_visibility='visible', disabled=True)

with col8:
    mode_selection = st.selectbox(
        "Mode",
        options=['Production', 'Simulation'],
        index=0 if st.session_state.mode == 'Production' else 1,
        key='mode_selector',
        label_visibility='visible'
    )
    if mode_selection != st.session_state.mode:
        st.session_state.mode = mode_selection
        st.rerun()

st.markdown('<hr style="margin: 1rem -2rem; border: none; border-top: 1px solid #e5e7eb;">', unsafe_allow_html=True)

# Simulation mode banner
if st.session_state.mode == 'Simulation':
    st.markdown('<div class="simulation-banner">Simulation Mode</div>', unsafe_allow_html=True)


# Configuration Modal Function
@st.dialog("Simulation: Configuration", width="large")
def show_configuration():
    st.caption("DC: AZ - Week: 2026-W22")
    st.markdown("---")

    # Mode-specific messaging
    if st.session_state.mode == 'Production':
        if st.session_state.promoted and len(st.session_state.selected_lanes) > 0:
            st.markdown('<div class="success-box">✅ <strong>Production Mode:</strong> P2PDL configuration is active. You can view, add, or deselect lanes below.</div>', unsafe_allow_html=True)

    # Live Needs % by Shift
    st.markdown("### Live Needs % by Shift")
    st.caption("Live needs cannot be set below 3% to ensure the plan can be generated successfully.")

    # Create the live needs table
    live_needs_data = {
        'Weekday': ['Wednesday 1', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday 2'],
        'AM - Live Needs %': [3, 3, 3, 3, 3, 3, 3, 3],
        'PM - Live Needs %': [3, 3, 3, 3, 3, 3, 3, 3]
    }
    live_needs_df = pd.DataFrame(live_needs_data)

    # Style the dataframe with green header
    st.markdown("""
    <style>
    div[data-testid="stDataFrame"] thead tr th {
        background-color: #d1fae5 !important;
        color: #065f46 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.dataframe(
        live_needs_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Weekday": st.column_config.TextColumn("Weekday", width="medium"),
            "AM - Live Needs %": st.column_config.NumberColumn("AM - Live Needs %", width="medium"),
            "PM - Live Needs %": st.column_config.NumberColumn("PM - Live Needs %", width="medium"),
        }
    )

    st.markdown("---")

    # Kit Inventory Constraints
    st.markdown("### Kit Inventory Constraints")
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.markdown("**Max Kit Inventory**")
    with col2:
        st.text_input("Max Kit Inventory", value="50000", label_visibility="collapsed", disabled=True, key="max_kit_inv")
    with col3:
        st.caption("Maximum total kit inventory allowed at any point")

    st.markdown("---")

    # Line Throughput
    st.markdown("### Line Throughput")

    # First row: AUTO, CORE, GL
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])
    with col1:
        st.markdown("**AUTO**")
    with col2:
        st.text_input("AUTO throughput", value="138", label_visibility="collapsed", disabled=True, key="auto_throughput")
    with col3:
        st.caption("units/hr")
    with col4:
        st.markdown("**CORE**")
    with col5:
        st.text_input("CORE throughput", value="80", label_visibility="collapsed", disabled=True, key="core_throughput")
    with col6:
        st.caption("units/hr")
    with col7:
        st.markdown("**GL**")
    with col8:
        st.text_input("GL throughput", value="80", label_visibility="collapsed", disabled=True, key="gl_throughput")
    with col9:
        st.caption("units/hr")

    st.markdown("<br>", unsafe_allow_html=True)

    # Second row: EP, LDL, KT
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])
    with col1:
        st.markdown("**EP**")
    with col2:
        st.text_input("EP throughput", value="130", label_visibility="collapsed", disabled=True, key="ep_throughput")
    with col3:
        st.caption("units/hr")
    with col4:
        st.markdown("**LDL**")
    with col5:
        st.text_input("LDL throughput", value="105", label_visibility="collapsed", disabled=True, key="ldl_throughput")
    with col6:
        st.caption("units/hr")
    with col7:
        st.markdown("**KT**")
    with col8:
        st.text_input("KT throughput", value="330", label_visibility="collapsed", disabled=True, key="kt_throughput")
    with col9:
        st.caption("units/hr")

    st.markdown("<br>", unsafe_allow_html=True)

    # Third row: Flexi, HP
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 4])
    with col1:
        st.markdown("**Flexi**")
    with col2:
        st.text_input("Flexi throughput", value="370", label_visibility="collapsed", disabled=True, key="flexi_throughput")
    with col3:
        st.caption("units/hr")
    with col4:
        st.markdown("**HP**")
    with col5:
        st.text_input("HP throughput", value="30", label_visibility="collapsed", disabled=True, key="hp_throughput")
    with col6:
        st.caption("units/hr")

    st.markdown("---")

    # P2PDL Section
    st.markdown("### P2PDL (Print 2 PDL)")

    st.markdown("**Filters**")
    col1, col2, col3 = st.columns(3)
    with col1:
        ship_day_filter = st.multiselect("Ship Day", options=sorted(df_lanes['Ship Day'].unique()), default=[], key="modal_ship_filter")
    with col2:
        brand_filter = st.multiselect("Brand", options=sorted(df_lanes['Brand'].unique()), default=[], key="modal_brand_filter")
    with col3:
        selection_filter = st.selectbox("Selection Status", options=['All', 'Selected Only', 'Unselected Only'], index=0, key="modal_selection_filter")

    # Apply filters
    filtered_df = df_lanes.copy()

    # In Production mode, show only selected lanes (or empty if none selected)
    if st.session_state.mode == 'Production':
        if len(st.session_state.selected_lanes) > 0:
            filtered_df = filtered_df[filtered_df['Lane_ID'].isin(st.session_state.selected_lanes)]
        else:
            # Show empty dataframe with same columns
            filtered_df = pd.DataFrame(columns=filtered_df.columns)

    # Add Selected column based on saved state
    filtered_df['Selected'] = filtered_df['Lane_ID'].isin(st.session_state.selected_lanes)

    if ship_day_filter:
        filtered_df = filtered_df[filtered_df['Ship Day'].isin(ship_day_filter)]
    if brand_filter:
        filtered_df = filtered_df[filtered_df['Brand'].isin(brand_filter)]

    if selection_filter == 'Selected Only':
        filtered_df = filtered_df[filtered_df['Selected']]
    elif selection_filter == 'Unselected Only':
        filtered_df = filtered_df[~filtered_df['Selected']]

    # Keep Lane_ID for tracking but don't display it
    display_df = filtered_df[['Lane_ID', 'Selected', 'Lane', 'Brand', 'Ship Day', 'CPT', 'Box Volume']].copy()

    # Show current selection count
    current_selected = len(st.session_state.selected_lanes)
    if st.session_state.mode == 'Production':
        if current_selected > 0:
            st.markdown(f"**Selected P2PDL Lanes** (*{len(display_df)} lanes configured*)")
        else:
            st.markdown("**Selected P2PDL Lanes**")
    else:
        # Simulation mode
        if current_selected > 0:
            st.markdown(f"**Lane Selection** (*{current_selected} selected*)")
        else:
            st.markdown("**Lane Selection**")

    # Calculate dynamic height based on number of rows
    # Each row is ~35px, add header (~35px), min 150px, max 600px
    row_height = 35
    header_height = 35
    num_rows = len(display_df)
    dynamic_height = min(max(num_rows * row_height + header_height, 150), 600)

    edited_df = st.data_editor(
        display_df,
        column_config={
            "Lane_ID": None,  # Hide Lane_ID column
            "Selected": st.column_config.CheckboxColumn(
                "Select for P2PDL",
                help="Select lanes to include in P2PDL",
                default=False,
                width="small"
            ),
            "Lane": st.column_config.TextColumn("Lane"),
            "Brand": st.column_config.TextColumn("Brand", width="small"),
            "Ship Day": st.column_config.TextColumn("Ship Day"),
            "CPT": st.column_config.TextColumn("CPT"),
            "Box Volume": st.column_config.NumberColumn("Box Volume", format="%d"),
        },
        disabled=["Lane", "Brand", "Ship Day", "CPT", "Box Volume"],
        hide_index=True,
        use_container_width=True,
        height=dynamic_height,
        key=f"modal_lane_editor_{st.session_state.mode}"  # Unique key per mode to ensure proper state
    )

    newly_selected = edited_df[edited_df['Selected']]['Lane_ID'].tolist()

    st.markdown("<br>", unsafe_allow_html=True)

    # Save button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Configuration", use_container_width=True, type="primary", key="save_config"):
            st.session_state.selected_lanes = newly_selected.copy()  # Make a copy to ensure it's saved
            # Show success and close modal
            st.toast(f"✅ Configuration saved! {len(newly_selected)} lanes selected for P2PDL.", icon="✅")
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True, key="cancel_config"):
            st.rerun()

# Call modal if triggered
if st.session_state.show_config_modal:
    show_configuration()
    st.session_state.show_config_modal = False


# ============================================================================
# CONFIGURATION TAB
# ============================================================================
if st.session_state.current_tab == 'Configuration':
    st.markdown("# Configuration")
    st.markdown("---")

    with st.expander("🔲 Assembly Process Path Box Splits", expanded=True):
        st.markdown("Configure target box-type split percentages by process path to match operational mod configuration. The solver will use these as preferences when allocating boxes.")

        # Process path selector tabs
        path_tab1, path_tab2, path_tab3, path_tab4 = st.tabs(["Auto", "LDL", "Manual Line", "Grocery Line"])

        def validate_splits(df):
            """Validate that 2P + 4P = 100% for each box type in each row"""
            errors = []
            for idx, row in df.iterrows():
                shift = row['Shift']
                for box_type in BOX_TYPES:
                    two_p = row[f'2P-{box_type} %']
                    four_p = row[f'4P-{box_type} %']
                    if abs((two_p + four_p) - 100) > 0.01:  # Allow small floating point errors
                        errors.append(f"{shift} - {box_type}: {two_p}% + {four_p}% ≠ 100%")
            return errors

        def create_split_table(process_path):
            """Create editable table for a process path"""
            # Create dataframe from session state
            data = []
            for shift in SHIFTS:
                row = {'Shift': shift}
                for box_type in BOX_TYPES:
                    row[f'2P-{box_type} %'] = st.session_state.box_split_config[process_path][shift][box_type]['2P']
                    row[f'4P-{box_type} %'] = st.session_state.box_split_config[process_path][shift][box_type]['4P']
                data.append(row)

            return pd.DataFrame(data)

        def apply_to_all_shifts(process_path, first_row_values):
            """Copy first row values to all other shifts"""
            for shift in SHIFTS:
                for box_type in BOX_TYPES:
                    st.session_state.box_split_config[process_path][shift][box_type]['2P'] = first_row_values[f'2P-{box_type} %']
                    st.session_state.box_split_config[process_path][shift][box_type]['4P'] = first_row_values[f'4P-{box_type} %']
            st.session_state.box_split_modified = True

        def reset_to_defaults(process_path):
            """Reset all values to 75% 2P, 25% 4P"""
            for shift in SHIFTS:
                for box_type in BOX_TYPES:
                    st.session_state.box_split_config[process_path][shift][box_type]['2P'] = 75
                    st.session_state.box_split_config[process_path][shift][box_type]['4P'] = 25
            st.session_state.box_split_modified = True

        def update_config_from_df(process_path, edited_df):
            """Update session state from edited dataframe"""
            for idx, row in edited_df.iterrows():
                shift = row['Shift']
                for box_type in BOX_TYPES:
                    st.session_state.box_split_config[process_path][shift][box_type]['2P'] = row[f'2P-{box_type} %']
                    st.session_state.box_split_config[process_path][shift][box_type]['4P'] = row[f'4P-{box_type} %']
            st.session_state.box_split_modified = True

        # Auto tab
        with path_tab1:
            st.markdown("**Auto**")

            # Bulk actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Apply First Row to All Shifts", key="auto_apply_all", use_container_width=True):
                    df = create_split_table('Auto')
                    first_row = df.iloc[0].to_dict()
                    apply_to_all_shifts('Auto', first_row)
                    st.rerun()
            with col2:
                if st.button("🔄 Reset to Defaults (75/25)", key="auto_reset", use_container_width=True):
                    reset_to_defaults('Auto')
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # Create and display table
            auto_df = create_split_table('Auto')

            edited_auto_df = st.data_editor(
                auto_df,
                column_config={
                    "Shift": st.column_config.TextColumn("Shift", width="large", disabled=True),
                    "2P-M %": st.column_config.NumberColumn("2P-M %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-M %": st.column_config.NumberColumn("4P-M %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "2P-G %": st.column_config.NumberColumn("2P-G %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-G %": st.column_config.NumberColumn("4P-G %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "2P-T %": st.column_config.NumberColumn("2P-T %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-T %": st.column_config.NumberColumn("4P-T %", min_value=0, max_value=100, step=1, format="%.0f"),
                },
                hide_index=True,
                use_container_width=True,
                height=600,
                key="auto_editor"
            )

            # Update config from edited dataframe
            if not edited_auto_df.equals(auto_df):
                update_config_from_df('Auto', edited_auto_df)

            # Validate
            auto_errors = validate_splits(edited_auto_df)
            if auto_errors:
                st.markdown('<div class="error-box"><strong>⚠️ Validation Errors:</strong><br>' + '<br>'.join(auto_errors) + '</div>', unsafe_allow_html=True)

        # LDL tab
        with path_tab2:
            st.markdown("**LDL**")

            # Bulk actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Apply First Row to All Shifts", key="ldl_apply_all", use_container_width=True):
                    df = create_split_table('LDL')
                    first_row = df.iloc[0].to_dict()
                    apply_to_all_shifts('LDL', first_row)
                    st.rerun()
            with col2:
                if st.button("🔄 Reset to Defaults (75/25)", key="ldl_reset", use_container_width=True):
                    reset_to_defaults('LDL')
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # Create and display table
            ldl_df = create_split_table('LDL')

            edited_ldl_df = st.data_editor(
                ldl_df,
                column_config={
                    "Shift": st.column_config.TextColumn("Shift", width="large", disabled=True),
                    "2P-M %": st.column_config.NumberColumn("2P-M %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-M %": st.column_config.NumberColumn("4P-M %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "2P-G %": st.column_config.NumberColumn("2P-G %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-G %": st.column_config.NumberColumn("4P-G %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "2P-T %": st.column_config.NumberColumn("2P-T %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-T %": st.column_config.NumberColumn("4P-T %", min_value=0, max_value=100, step=1, format="%.0f"),
                },
                hide_index=True,
                use_container_width=True,
                height=600,
                key="ldl_editor"
            )

            # Update config from edited dataframe
            if not edited_ldl_df.equals(ldl_df):
                update_config_from_df('LDL', edited_ldl_df)

            # Validate
            ldl_errors = validate_splits(edited_ldl_df)
            if ldl_errors:
                st.markdown('<div class="error-box"><strong>⚠️ Validation Errors:</strong><br>' + '<br>'.join(ldl_errors) + '</div>', unsafe_allow_html=True)

        # Manual Line tab
        with path_tab3:
            st.markdown("**Manual Line**")

            # Bulk actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Apply First Row to All Shifts", key="manual_apply_all", use_container_width=True):
                    df = create_split_table('Manual Line')
                    first_row = df.iloc[0].to_dict()
                    apply_to_all_shifts('Manual Line', first_row)
                    st.rerun()
            with col2:
                if st.button("🔄 Reset to Defaults (75/25)", key="manual_reset", use_container_width=True):
                    reset_to_defaults('Manual Line')
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # Create and display table
            manual_df = create_split_table('Manual Line')

            edited_manual_df = st.data_editor(
                manual_df,
                column_config={
                    "Shift": st.column_config.TextColumn("Shift", width="large", disabled=True),
                    "2P-M %": st.column_config.NumberColumn("2P-M %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-M %": st.column_config.NumberColumn("4P-M %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "2P-G %": st.column_config.NumberColumn("2P-G %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-G %": st.column_config.NumberColumn("4P-G %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "2P-T %": st.column_config.NumberColumn("2P-T %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-T %": st.column_config.NumberColumn("4P-T %", min_value=0, max_value=100, step=1, format="%.0f"),
                },
                hide_index=True,
                use_container_width=True,
                height=600,
                key="manual_editor"
            )

            # Update config from edited dataframe
            if not edited_manual_df.equals(manual_df):
                update_config_from_df('Manual Line', edited_manual_df)

            # Validate
            manual_errors = validate_splits(edited_manual_df)
            if manual_errors:
                st.markdown('<div class="error-box"><strong>⚠️ Validation Errors:</strong><br>' + '<br>'.join(manual_errors) + '</div>', unsafe_allow_html=True)

        # Grocery Line tab
        with path_tab4:
            st.markdown("**Grocery Line**")

            # Bulk actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Apply First Row to All Shifts", key="grocery_apply_all", use_container_width=True):
                    df = create_split_table('Grocery Line')
                    first_row = df.iloc[0].to_dict()
                    apply_to_all_shifts('Grocery Line', first_row)
                    st.rerun()
            with col2:
                if st.button("🔄 Reset to Defaults (75/25)", key="grocery_reset", use_container_width=True):
                    reset_to_defaults('Grocery Line')
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # Create and display table
            grocery_df = create_split_table('Grocery Line')

            edited_grocery_df = st.data_editor(
                grocery_df,
                column_config={
                    "Shift": st.column_config.TextColumn("Shift", width="large", disabled=True),
                    "2P-M %": st.column_config.NumberColumn("2P-M %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-M %": st.column_config.NumberColumn("4P-M %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "2P-G %": st.column_config.NumberColumn("2P-G %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-G %": st.column_config.NumberColumn("4P-G %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "2P-T %": st.column_config.NumberColumn("2P-T %", min_value=0, max_value=100, step=1, format="%.0f"),
                    "4P-T %": st.column_config.NumberColumn("4P-T %", min_value=0, max_value=100, step=1, format="%.0f"),
                },
                hide_index=True,
                use_container_width=True,
                height=600,
                key="grocery_editor"
            )

            # Update config from edited dataframe
            if not edited_grocery_df.equals(grocery_df):
                update_config_from_df('Grocery Line', edited_grocery_df)

            # Validate
            grocery_errors = validate_splits(edited_grocery_df)
            if grocery_errors:
                st.markdown('<div class="error-box"><strong>⚠️ Validation Errors:</strong><br>' + '<br>'.join(grocery_errors) + '</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Check if all validations pass
        all_errors = []
        for path in PROCESS_PATHS:
            df = create_split_table(path)
            all_errors.extend(validate_splits(df))

        all_valid = len(all_errors) == 0

        # Save/Cancel buttons
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("💾 Save Configuration", use_container_width=True, type="primary", disabled=not all_valid, key="save_box_splits"):
                # Save current config as the "saved" version
                st.session_state.box_split_saved = {
                    path: {
                        shift: {
                            box_type: splits.copy()
                            for box_type, splits in st.session_state.box_split_config[path][shift].items()
                        }
                        for shift in SHIFTS
                    }
                    for path in PROCESS_PATHS
                }
                st.session_state.box_split_modified = False
                st.success("✅ Box split configuration saved successfully!")

        with col2:
            if st.button("Cancel", use_container_width=True, key="cancel_box_splits"):
                # Revert to saved config
                st.session_state.box_split_config = {
                    path: {
                        shift: {
                            box_type: splits.copy()
                            for box_type, splits in st.session_state.box_split_saved[path][shift].items()
                        }
                        for shift in SHIFTS
                    }
                    for path in PROCESS_PATHS
                }
                st.session_state.box_split_modified = False
                st.rerun()

        # Show warning if there are unsaved changes
        if st.session_state.box_split_modified:
            st.markdown('<div class="warning-box">⚠️ You have unsaved changes. Click "Save Configuration" to apply or "Cancel" to discard.</div>', unsafe_allow_html=True)

# ============================================================================
# PLANNING TAB (existing code)
# ============================================================================
elif st.session_state.current_tab == 'Planning':
    # Main Dashboard
    st.markdown("# Planning Dashboard")

    # Success banner for plan generation (Production mode only)
    if st.session_state.mode == 'Production':
        st.markdown('<div class="success-box">✅ <strong>Plan generation completed</strong> at 4/7/2026, 6:20:30 AM MST for AZ 2026-W22</div>', unsafe_allow_html=True)

    # DC/Week header (only show in Production mode, Simulation mode has its own layout)
    if st.session_state.mode == 'Production':
        st.markdown('<div style="color: #22c55e; font-size: 1.1rem; font-weight: 600; margin: 1rem 0 0.5rem 0;">AZ 2026-W22</div>', unsafe_allow_html=True)

        # Hamburger menu below the header (Production mode only)
        with st.popover("☰", use_container_width=False):
            st.markdown("**Planning Levers**")
            st.markdown("---")

            if st.button("Enter HC", use_container_width=True, disabled=True, key="nav_hc"):
                pass

            if st.button("Configuration", use_container_width=True, key="nav_config"):
                st.session_state.show_config_modal = True

            if st.button("EOS Kits", use_container_width=True, disabled=True, key="nav_eos"):
                pass

        st.markdown("---")

    if st.session_state.mode == 'Production':
        st.markdown("### Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-container"><div style="color: #6b7280; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">ODL/PDL Volume</div><div style="font-size: 2rem; font-weight: bold; color: #111827;">75,833</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-container"><div style="color: #6b7280; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">Allocated / Total</div><div style="font-size: 2rem; font-weight: bold; color: #111827;">75,828/75,833</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-container"><div style="color: #6b7280; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">Unallocated</div><div style="font-size: 2rem; font-weight: bold; color: #111827;">5</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-container"><div style="color: #6b7280; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">Completed</div><div style="font-size: 2rem; font-weight: bold; color: #111827;">66,592</div></div>', unsafe_allow_html=True)

        if st.session_state.promoted and len(st.session_state.selected_lanes) > 0:
            st.markdown("---")
            total_p2pdl_vol = df_lanes[df_lanes['Lane_ID'].isin(st.session_state.selected_lanes)]['Box Volume'].sum()
            st.markdown(f'<div class="success-box">✅ <strong>P2PDL Configuration Active:</strong> {len(st.session_state.selected_lanes)} lanes ({total_p2pdl_vol:,} boxes) are configured for P2PDL in the current production plan. <a href="#" style="color: #1d4ed8;">View in Configuration →</a></div>', unsafe_allow_html=True)

    else:  # Simulation mode
        # Show promotion success message if flag is set
        if st.session_state.show_promotion_message:
            st.success("✅ Your configuration has been saved to Production Mode.")
            st.session_state.show_promotion_message = False

        # Simulation header
        st.markdown('<p style="color: #4169E1; font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem;">Simulation 7 <span style="color: #9ca3af; font-size: 1rem;">✏️</span></p>', unsafe_allow_html=True)

        # Simulation selector and actions
        col1, col2, col3, col4 = st.columns([0.5, 3, 2, 2])
        with col1:
            # Hamburger menu for Simulation mode
            with st.popover("☰", use_container_width=False):
                st.markdown("**Planning Levers**")
                st.markdown("---")

                if st.button("Enter HC", use_container_width=True, disabled=True, key="nav_hc_sim"):
                    pass

                if st.button("Configuration", use_container_width=True, key="nav_config_sim"):
                    st.session_state.show_config_modal = True

                if st.button("EOS Kits", use_container_width=True, disabled=True, key="nav_eos_sim"):
                    pass
        with col2:
            sim_status = "completed" if st.session_state.simulation_run else "draft"
            st.markdown(f'<div style="padding: 0.5rem; background-color: #f3f4f6; border-radius: 6px; display: inline-block;">Simulation: <strong>Simulation 7</strong> <span style="background-color: #dbeafe; color: #1e40af; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.85rem; margin-left: 0.5rem;">{sim_status}</span></div>', unsafe_allow_html=True)
        with col3:
            if st.button("▶️ Simulate Plan Gen", use_container_width=True, type="primary", key="sim_gen"):
                st.session_state.simulation_run = True
                st.rerun()
        with col4:
            if st.session_state.simulation_run:
                if st.button("📋 Promote to Production Plan", use_container_width=True, type="primary", key="promote_btn"):
                    st.session_state.promoted = True
                    st.session_state.show_promotion_message = True
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Metrics (show after simulation runs or if P2PDL configured)
        if st.session_state.simulation_run:
            st.markdown("### Key Metrics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="metric-container"><div style="color: #6b7280; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">ODL/PDL Volume</div><div style="font-size: 2rem; font-weight: bold; color: #111827;">75,833</div></div>', unsafe_allow_html=True)
            with col2:
                # Adjusted allocated volume if P2PDL is active
                p2pdl_vol = df_lanes[df_lanes['Lane_ID'].isin(st.session_state.selected_lanes)]['Box Volume'].sum() if len(st.session_state.selected_lanes) > 0 else 0
                allocated = 75828 - p2pdl_vol + p2pdl_vol  # Showing impact
                st.markdown(f'<div class="metric-container"><div style="color: #6b7280; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">Allocated / Total Volume</div><div style="font-size: 2rem; font-weight: bold; color: #111827;">{allocated:,}/75,833</div></div>', unsafe_allow_html=True)
            with col3:
                unallocated = 75833 - allocated
                st.markdown(f'<div class="metric-container"><div style="color: #6b7280; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">Unallocated Volume</div><div style="font-size: 2rem; font-weight: bold; color: #111827;">{unallocated:,}</div></div>', unsafe_allow_html=True)
            with col4:
                st.markdown('<div class="metric-container"><div style="color: #6b7280; font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">Completed Volume</div><div style="font-size: 2rem; font-weight: bold; color: #111827;">66,592</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Needs Action section (collapsible)
            with st.expander("Needs Action - LATE Boxes Risk", expanded=True):
                st.markdown('<div style="text-align: center; padding: 2rem; color: #6b7280;">No late boxes found.</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Volume Metrics section
            with st.expander("Volume Metrics", expanded=True):
                st.markdown("### Plan KPIs")

                # RoW Volume and Grocery tables side by side
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**RoW Volume**")
                    row_volume_data = {
                        'Shift': ['wednesday_1_day', 'wednesday_1_night', 'thursday_day', 'thursday_night',
                                 'friday_day', 'friday_night', 'saturday_day', 'saturday_night',
                                 'sunday_day', 'sunday_night'],
                        'Volume': [0, 0, 0, 0, 0, 7999, 15521, 22377, 25383, 26884]
                    }
                    row_volume_df = pd.DataFrame(row_volume_data)
                    st.dataframe(
                        row_volume_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Shift": st.column_config.TextColumn("Shift", width="medium"),
                            "Volume": st.column_config.NumberColumn("Volume", width="medium", format="%d"),
                        },
                        height=400
                    )

                with col2:
                    st.markdown("**Grocery (Complexity)**")
                    grocery_data = {
                        'Shift': ['friday_night', 'saturday_day', 'saturday_night', 'sunday_day',
                                 'sunday_night', 'monday_day', 'monday_night', 'tuesday_day'],
                        '% (Grocery / Total Volume)': [43.71, 45.05, 38.75, 61.18, 14.66, 0, 0, 0],
                        '% (Grocery / Auto Volume)': [0, 0, 0, 0, 0, 0, 0, 0]
                    }
                    grocery_df = pd.DataFrame(grocery_data)
                    st.dataframe(
                        grocery_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Shift": st.column_config.TextColumn("Shift", width="medium"),
                            "% (Grocery / Total Volume)": st.column_config.NumberColumn("% (Grocery / Total Volume)", width="medium", format="%.2f"),
                            "% (Grocery / Auto Volume)": st.column_config.NumberColumn("% (Grocery / Auto Volume)", width="medium", format="%.2f"),
                        },
                        height=400
                    )

                # Show P2PDL volume table if configured
                if len(st.session_state.selected_lanes) > 0:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("**Total P2PDL Volume by Shift**")

                    # Get selected lane data
                    selected_lanes_df = df_lanes[df_lanes['Lane_ID'].isin(st.session_state.selected_lanes)].copy()

                    # Map ship days to P2PDL shifts (1 day before ship day)
                    # P2PDL work happens the day before the ship day
                    day_before_mapping = {
                        'TUESDAY': 'monday',
                        'WEDNESDAY': 'tuesday',
                        'THURSDAY': 'wednesday',
                        'FRIDAY': 'thursday',
                        'SATURDAY': 'friday',
                        'SUNDAY': 'saturday',
                        'MONDAY': 'sunday'
                    }

                    # Determine shift (day/night) based on CPT time
                    # If CPT time is before 12:00, use _day, otherwise use _night (simplified logic)
                    def get_p2pdl_shift(row):
                        ship_day = row['Ship Day']
                        cpt = row['CPT']

                        # Extract hour from CPT (format: "04-09 (Tue) 15:00")
                        time_part = cpt.split(' ')[-1]  # "15:00"
                        hour = int(time_part.split(':')[0])

                        # Get day before ship day
                        day_before = day_before_mapping.get(ship_day, 'monday')

                        # Determine AM (day) or PM (night) - simplified: < 12:00 = day, >= 12:00 = night
                        shift_time = 'day' if hour < 12 else 'night'

                        # Handle week boundaries (Wednesday appears twice)
                        if day_before == 'wednesday' and ship_day == 'THURSDAY':
                            return f'wednesday_1_{shift_time}'
                        elif day_before == 'wednesday' and ship_day != 'THURSDAY':
                            return f'wednesday_2_{shift_time}'
                        else:
                            return f'{day_before}_{shift_time}'

                    selected_lanes_df['P2PDL_Shift'] = selected_lanes_df.apply(get_p2pdl_shift, axis=1)

                    # Calculate volume by shift
                    shift_volumes = selected_lanes_df.groupby('P2PDL_Shift')['Box Volume'].sum().to_dict()

                    # All shifts in order
                    all_shifts = [
                        'wednesday_1_day', 'wednesday_1_night', 'thursday_day', 'thursday_night',
                        'friday_day', 'friday_night', 'saturday_day', 'saturday_night',
                        'sunday_day', 'sunday_night', 'monday_day', 'monday_night',
                        'tuesday_day', 'tuesday_night', 'wednesday_2_day', 'wednesday_2_night'
                    ]

                    # Create summary table
                    p2pdl_shift_data = {
                        'shift': all_shifts,
                        'Volume': [shift_volumes.get(shift, 0) for shift in all_shifts]
                    }
                    p2pdl_shift_df = pd.DataFrame(p2pdl_shift_data)

                    st.dataframe(
                        p2pdl_shift_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "shift": st.column_config.TextColumn("shift", width="medium"),
                            "Volume": st.column_config.NumberColumn("Volume", width="medium", format="%d"),
                        }
                    )

                    # Shift selector to view lane details
                    shifts_with_volume = [shift for shift in all_shifts if shift_volumes.get(shift, 0) > 0]

                    if shifts_with_volume:
                        st.markdown("<br>", unsafe_allow_html=True)
                        selected_shift = st.selectbox(
                            "Select a shift to view lane details",
                            options=shifts_with_volume,
                            format_func=lambda x: f"{x} ({shift_volumes.get(x, 0):,} boxes)",
                            key="shift_detail_selector"
                        )

                        if selected_shift:
                            st.markdown(f"**Lane Details for {selected_shift}**")
                            # Get lanes for selected shift
                            shift_lanes = selected_lanes_df[selected_lanes_df['P2PDL_Shift'] == selected_shift][
                                ['Lane', 'Brand', 'Ship Day', 'CPT', 'Box Volume']
                            ].copy()
                            shift_lanes = shift_lanes.rename(columns={'Ship Day': 'Original Ship Day'})

                            st.dataframe(
                                shift_lanes,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "Lane": st.column_config.TextColumn("Lane", width="large"),
                                    "Brand": st.column_config.TextColumn("Brand", width="small"),
                                    "Original Ship Day": st.column_config.TextColumn("Original Ship Day", width="medium"),
                                    "CPT": st.column_config.TextColumn("CPT", width="medium"),
                                    "Box Volume": st.column_config.NumberColumn("Box Volume", width="medium", format="%d"),
                                }
                            )

        else:
            # Before simulation runs
            if len(st.session_state.selected_lanes) > 0:
                total_p2pdl_vol = df_lanes[df_lanes['Lane_ID'].isin(st.session_state.selected_lanes)]['Box Volume'].sum()
                st.markdown(f'<div class="info-box">ℹ️ <strong>P2PDL Configuration Active:</strong> {len(st.session_state.selected_lanes)} lanes selected ({total_p2pdl_vol:,} boxes). Click "Simulate Plan Gen" to validate.</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #6b7280; font-size: 0.875rem; padding: 2rem 0 1rem 0;"><strong>Riptide v2 Prototype</strong> • Box Split Configuration + P2PDL • Built with Streamlit</div>', unsafe_allow_html=True)
