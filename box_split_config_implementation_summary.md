# Box Split Configuration Implementation Summary

## Overview
Added a new **Configuration** tab to the Riptide v2 Streamlit app with a "Process Path Box Splits" feature that allows planners to configure target box-type split percentages by process path.

## What Changed

### 1. New Files Created
- **`p2pdl_prototype_v4_config.py`** - Updated version with Configuration tab

### 2. Key Features Added

#### Configuration Tab
- New top-level tab "⚙️ Configuration" alongside Planning and Kitting tabs
- Uses accordion/collapsible sections (st.expander) for different configuration types
- Currently implements "Process Path Box Splits" section (can expand with more config types later)

#### Process Path Box Splits Feature

**Navigation:**
- Configuration tab → "🔲 Process Path Box Splits" expander (expanded by default)
- Tabs for each process path: Auto, LDL, Manual Lines

**Table Structure (per process path):**
- **Rows:** 16 shifts
  - Wednesday 1 Day/Night
  - Thursday Day/Night
  - Friday Day/Night
  - Saturday Day/Night
  - Sunday Day/Night
  - Monday Day/Night
  - Tuesday Day/Night
  - Wednesday 2 Day/Night

- **Columns:** 
  - Shift (non-editable)
  - M-2P % (editable, 0-100)
  - M-4P % (editable, 0-100)
  - G-2P % (editable, 0-100)
  - G-4P % (editable, 0-100)
  - T-2P % (editable, 0-100)
  - T-4P % (editable, 0-100)

**Validation:**
- For each row, validates that:
  - M-2P% + M-4P% = 100%
  - G-2P% + G-4P% = 100%
  - T-2P% + T-4P% = 100%
- Shows inline error messages if validation fails
- "Save Configuration" button disabled until all validations pass

**Bulk Actions (per process path):**
1. **"📋 Apply First Row to All Shifts"** - Copies first row values to all other rows
2. **"🔄 Reset to Defaults (75/25)"** - Sets all values to 75% 2P, 25% 4P
3. **"📥 Copy from Previous Week"** - Placeholder (disabled for now)

**Save/Cancel:**
- **"💾 Save Configuration"** (green button) - Saves config to session state
  - Disabled if validation fails
  - Shows success message when saved
- **"Cancel"** (grey button) - Reverts to last saved state
- **Warning banner** - Shows when there are unsaved changes

**Data Structure:**
```python
box_split_config = {
    "Auto": {
        "Wednesday 1 Day": {
            "M": {"2P": 75, "4P": 25},
            "G": {"2P": 75, "4P": 25},
            "T": {"2P": 75, "4P": 25}
        },
        "Wednesday 1 Night": {...},
        ...
    },
    "LDL": {...},
    "Manual Lines": {...}
}
```

### 3. Session State Variables Added
- `current_tab` - Tracks active tab (Planning, Kitting, Configuration)
- `box_split_config` - Current working configuration
- `box_split_saved` - Last saved configuration (for cancel functionality)
- `box_split_modified` - Flag indicating unsaved changes

### 4. UI/UX Improvements
- Consistent styling with existing app (green accent for primary actions)
- Error boxes in red for validation failures
- Warning boxes in yellow for unsaved changes
- Success messages on save
- Responsive table height (600px for comfortable viewing of all 16 shifts)
- Disabled state for Save button when validation fails

## Testing Guide

### 1. Start the App
```bash
cd /Users/nikhil.ranka/pm-os
streamlit run p2pdl_prototype_v4_config.py
```

### 2. Navigate to Configuration Tab
- Click "⚙️ Configuration" button in the top navigation
- Should see "Process Path Box Splits" expander (expanded by default)

### 3. Test Box Split Configuration

#### Test Case 1: View Default Configuration
- Click on "Auto" tab
- Verify all rows show 75% 2P, 25% 4P for all box types (M, G, T)
- Repeat for "LDL" and "Manual Lines" tabs

#### Test Case 2: Edit Values
- Change "Wednesday 1 Day" → M-2P% to 80
- Change "Wednesday 1 Day" → M-4P% to 20
- Verify no validation error (80 + 20 = 100)
- Verify "unsaved changes" warning appears at bottom
- Verify "Save Configuration" button is enabled

#### Test Case 3: Validation Errors
- Change "Thursday Day" → G-2P% to 60
- Change "Thursday Day" → G-4P% to 50
- Should see red error box: "Thursday Day - G: 60% + 50% ≠ 100%"
- Verify "Save Configuration" button is disabled

#### Test Case 4: Bulk Actions - Apply to All Shifts
- Set "Wednesday 1 Day" values to: M(80/20), G(70/30), T(85/15)
- Click "📋 Apply First Row to All Shifts"
- Verify all 16 rows now have the same values
- Verify "unsaved changes" warning appears

#### Test Case 5: Bulk Actions - Reset to Defaults
- After making changes, click "🔄 Reset to Defaults (75/25)"
- Verify all values reset to 75/25
- Verify "unsaved changes" warning appears

#### Test Case 6: Save Configuration
- Make valid changes (e.g., change a few rows)
- Click "💾 Save Configuration"
- Should see success message: "✅ Box split configuration saved successfully!"
- Verify warning message disappears

#### Test Case 7: Cancel Changes
- Make some changes (don't save)
- Click "Cancel"
- Verify changes are reverted to last saved state
- Verify warning message disappears

#### Test Case 8: Multiple Process Paths
- Configure different values for Auto, LDL, and Manual Lines
- Verify each process path maintains its own configuration
- Save and verify all are persisted

### 4. Integration Testing

#### Test Case 9: Tab Navigation
- Switch between Planning → Configuration → Planning
- Verify Configuration state persists
- Verify Planning tab still works as expected

#### Test Case 10: Mode Switching
- Make changes in Configuration tab
- Switch between Production and Simulation modes
- Verify configuration persists across mode switches

## Dependencies

No new dependencies required! The implementation uses only existing Streamlit features:
- `streamlit` (already installed)
- `pandas` (already installed)
- `numpy` (already installed)

## File Locations

- **Main app file:** `/Users/nikhil.ranka/pm-os/p2pdl_prototype_v4_config.py`
- **Previous version:** `/Users/nikhil.ranka/pm-os/p2pdl_prototype_v3.py`
- **Implementation summary:** `/Users/nikhil.ranka/pm-os/box_split_config_implementation_summary.md`

## What to Deploy

If you want to update your Streamlit app (https://p2pdl-prototype-riptidev2.streamlit.app/):
1. Replace the current app file with `p2pdl_prototype_v4_config.py`
2. Or rename it to match your current deployment file name
3. Commit and push to trigger Streamlit Cloud redeployment

## Next Steps / Future Enhancements

Based on the Jira ticket requirements, potential future additions:
1. **Copy from Previous Week** - Implement actual functionality (currently placeholder)
2. **Deviation Tracking** - After plan generation, show actual vs target splits
3. **Reason Display** - Explain why solver deviated from target splits
4. **Historical Data** - Load previous week's configuration
5. **Export/Import** - Save/load configurations as JSON/CSV
6. **DC-specific Defaults** - Different default values per DC
7. **Validation Warnings** - Warn if splits differ significantly from historical norms
8. **Process Path Capacity Check** - Validate splits don't exceed capacity limits

## Architecture Notes

### State Management
- Configuration is stored in `st.session_state.box_split_config`
- Saved state is tracked separately in `st.session_state.box_split_saved`
- This enables "Cancel" functionality by reverting to saved state
- State persists across reruns but not across sessions (browser refresh clears it)

### Data Flow
1. User edits table → `st.data_editor` captures changes
2. Changes update `box_split_config` in session state
3. `box_split_modified` flag set to True
4. Validation runs on current config
5. User clicks Save → `box_split_saved` updated, flag cleared
6. User clicks Cancel → `box_split_config` reverted to `box_split_saved`

### Future Integration with Solver
To integrate with the actual solver:
```python
# In plan generation code:
box_split_config = st.session_state.box_split_saved  # Use saved config
solver_params = {
    'process_path_splits': box_split_config,
    # ... other params
}
result = run_solver(solver_params)
```

## Known Limitations

1. **Session State Only** - Configuration doesn't persist across browser sessions (would need database/file storage)
2. **No Historical Data** - "Copy from Previous Week" is placeholder
3. **No Backend Integration** - Currently UI-only, not connected to actual solver
4. **No User Roles** - No permissions/access control for who can modify configuration
5. **Single DC** - Currently hardcoded to AZ, would need multi-DC support

## Questions to Resolve

1. **Default Values:** Should different process paths have different defaults? (Currently all 75/25)
2. **Persistence:** Where should configuration be stored long-term? (Database, file, etc.)
3. **Solver Integration:** How should the config be passed to the solver? (API, file, direct call?)
4. **Deviation Threshold:** What % deviation should trigger a warning after plan generation?
5. **User Training:** What documentation/tooltips needed for planners to use this effectively?

## Contact

For questions or issues with this implementation:
- Implementation created: 2026-05-20
- Based on: `riptide_v2_box_split_config_jira_ticket.md`
- Related tickets: USFPT-3813 (Box routing to LDL/Manual)
