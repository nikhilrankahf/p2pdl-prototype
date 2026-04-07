import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Riptide v2 - P2PDL Prototype", layout="wide")

# Custom CSS with modal styling
st.markdown("""
<style>
    .block-container {
        padding-top: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
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

        # TNT (Time in Transit) - typically 1-5 days depending on lane type
        tnt = np.random.choice([1, 2, 3, 4, 5])

        lanes.append({
            'Lane_ID': lane_id,  # Unique identifier
            'Lane': lane_name,
            'Brand': brand,
            'Ship Day': ship_day_name,  # Full day name from CPT
            'TNT': tnt,
            'CPT': cpt,
            'Box Volume': np.random.randint(50, 5000)
        })

    return pd.DataFrame(lanes)

df_lanes = generate_lane_data()

# Header
st.markdown('<div style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding: 0.75rem 2rem; margin: 0 -2rem 0 -2rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);"></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1.5, 1.5, 3.5, 1, 1.5, 1.5])

with col1:
    st.markdown('<p style="font-size: 1.2rem; font-weight: 700; color: #111827; margin: 0.5rem 0;">⚡ Riptide</p>', unsafe_allow_html=True)

with col2:
    st.button("📦 Planning", disabled=True, use_container_width=True, key="planning_tab")

with col3:
    st.button("🏭 Kitting", disabled=True, use_container_width=True, type="secondary", key="kitting_tab")

with col5:
    st.selectbox("DC", options=['AZ'], index=0, key='dc_selector', label_visibility='visible', disabled=True)

with col6:
    st.selectbox("Week", options=['2026-W15'], index=0, key='week_selector', label_visibility='visible', disabled=True)

with col7:
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
    st.caption("DC: AZ - Week: 2026-W15")
    st.markdown("---")

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
    display_df = filtered_df[['Lane_ID', 'Selected', 'Lane', 'Brand', 'TNT', 'Ship Day', 'CPT', 'Box Volume']].copy()

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
            "TNT": st.column_config.NumberColumn("TNT (days)", width="small", format="%d"),
            "Ship Day": st.column_config.TextColumn("Ship Day"),
            "CPT": st.column_config.TextColumn("CPT"),
            "Box Volume": st.column_config.NumberColumn("Box Volume", format="%d"),
        },
        disabled=["Lane", "Brand", "TNT", "Ship Day", "CPT", "Box Volume"],
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
            st.session_state.show_config_modal = False  # Close modal
            # Show success and close modal
            st.toast(f"✅ Configuration saved! {len(newly_selected)} lanes selected for P2PDL.", icon="✅")
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True, key="cancel_config"):
            st.session_state.show_config_modal = False  # Close modal
            st.rerun()

# Call modal if triggered
if st.session_state.show_config_modal:
    show_configuration()
    st.session_state.show_config_modal = False

# Main Dashboard
st.markdown("# Planning Dashboard")

# Success banner for plan generation (Production mode only)
if st.session_state.mode == 'Production':
    st.markdown('<div class="success-box">✅ <strong>Plan generation completed</strong> at 4/7/2026, 6:20:30 AM MST for AZ 2026-W15</div>', unsafe_allow_html=True)

# DC/Week header (only show in Production mode, Simulation mode has its own layout)
if st.session_state.mode == 'Production':
    st.markdown('<div style="color: #22c55e; font-size: 1.1rem; font-weight: 600; margin: 1rem 0 0.5rem 0;">AZ 2026-W15</div>', unsafe_allow_html=True)

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
                            ['Lane', 'Brand', 'TNT', 'Ship Day', 'CPT', 'Box Volume']
                        ].copy()
                        shift_lanes = shift_lanes.rename(columns={'Ship Day': 'Original Ship Day'})

                        st.dataframe(
                            shift_lanes,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Lane": st.column_config.TextColumn("Lane", width="large"),
                                "Brand": st.column_config.TextColumn("Brand", width="small"),
                                "TNT": st.column_config.NumberColumn("TNT (days)", width="small", format="%d"),
                                "Original Ship Day": st.column_config.TextColumn("Original Ship Day", width="medium"),
                                "CPT": st.column_config.TextColumn("CPT", width="medium"),
                                "Box Volume": st.column_config.NumberColumn("Box Volume", width="medium", format="%d"),
                            }
                        )

    else:
        # Before simulation runs - no info box needed
        pass

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #6b7280; font-size: 0.875rem; padding: 2rem 0 1rem 0;"><strong>P2PDL Feature Prototype</strong> • Riptide v2 • Built with Streamlit</div>', unsafe_allow_html=True)
