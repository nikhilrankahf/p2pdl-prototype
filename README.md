# P2PDL (Print 2 PDL) - Riptide v2 Prototype

## Overview
Interactive prototype demonstrating P2PDL functionality for Riptide v2 AZ Go-Live.

**P2PDL** allows planners to selectively start assembly for specific lanes from PDL before ODL drops, enabling them to pull ahead volume and derisk CPT misses.

## Features Implemented

### FR1: Lane Selection Interface
- Filter lanes by Ship Day, Brand, Selection Status
- Sortable table with Lane, Brand, Ship Day, CPT, Box Volume
- Selection tracking with unique lane identifiers

### FR2: Simulation and Validation
- Run simulation to assess P2PDL impact
- View metrics: ODL/PDL Volume, Allocated/Total, Unallocated, Completed
- Volume Metrics section with RoW Volume, Grocery Complexity, and P2PDL Volume by Shift
- Drill-down to see which lanes contribute to each shift's P2PDL volume

### FR3: Plan Promotion
- Promote validated simulation to Production mode
- Configuration persists across modes
- View and manage active P2PDL lanes in Production

## Running Locally

```bash
pip install -r requirements.txt
streamlit run p2pdl_prototype_v3.py
```

## User Flow

### Simulation Mode
1. Click hamburger menu (☰) → Configuration
2. Scroll to P2PDL section
3. Filter and select lanes for P2PDL
4. Click "Save Configuration"
5. Return to Dashboard → Click "Simulate Plan Gen"
6. Review metrics and P2PDL volume breakdown
7. Click "Promote to Production Plan"

### Production Mode
1. View active P2PDL configuration in Key Metrics
2. Click hamburger menu (☰) → Configuration to view/edit selected lanes
3. Can add or deselect lanes as needed

## Technical Notes

- **Lane Selection**: Uses unique Lane_ID (lane name + ship day + index) to prevent duplicate selections
- **P2PDL Scheduling**: Lanes are scheduled 1 day before ship day (e.g., Tuesday ship day → Monday P2PDL shift)
- **Shift Assignment**: CPT time determines AM (day) or PM (night) shift
- **Sample Data**: 50 lanes with randomized attributes (brands: HF/EP, ship days: Mon-Sun)

## Feedback

For questions or feedback, contact Nikhil Ranka or open an issue in this repo.

---

*Built with Streamlit • Prototype for Requirements Gathering*
