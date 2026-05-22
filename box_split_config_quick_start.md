# Box Split Configuration - Quick Start Guide

## What's New

### New Navigation Tab
```
Before: [📦 Planning] [🏭 Kitting] [DC] [Week] [Mode]
After:  [📦 Planning] [🏭 Kitting] [⚙️ Configuration] [DC] [Week] [Mode]
```

### Configuration Tab Structure
```
Configuration
└── 🔲 Process Path Box Splits (expandable)
    ├── [Auto] [LDL] [Manual Lines] ← Process path tabs
    │
    ├── Bulk Actions Row
    │   ├── 📋 Apply First Row to All Shifts
    │   ├── 🔄 Reset to Defaults (75/25)
    │   └── 📥 Copy from Previous Week (disabled)
    │
    ├── Editable Table (16 rows × 7 columns)
    │   │ Shift              │ M-2P % │ M-4P % │ G-2P % │ G-4P % │ T-2P % │ T-4P % │
    │   │ Wednesday 1 Day    │   75   │   25   │   75   │   25   │   75   │   25   │
    │   │ Wednesday 1 Night  │   75   │   25   │   75   │   25   │   75   │   25   │
    │   │ Thursday Day       │   75   │   25   │   75   │   25   │   75   │   25   │
    │   │ ...                │  ...   │  ...   │  ...   │  ...   │  ...   │  ...   │
    │
    ├── Validation Messages
    │   └── ⚠️ Thursday Day - G: 60% + 50% ≠ 100% (if validation fails)
    │
    └── Action Buttons
        ├── [💾 Save Configuration] (green, disabled if validation fails)
        └── [Cancel] (grey)
```

## How to Use

### 1. Start the App
```bash
cd /Users/nikhil.ranka/pm-os
streamlit run p2pdl_prototype_v4_config.py
```

### 2. Navigate to Configuration
- Click **"⚙️ Configuration"** in top navigation
- Click on **"Process Path Box Splits"** expander (already expanded by default)

### 3. Configure Box Splits

#### For a Single Shift:
1. Click on the cell you want to edit (e.g., "Wednesday 1 Day" → M-2P%)
2. Type new value (e.g., 80)
3. Press Tab or click another cell
4. Edit the corresponding 4P% value (e.g., 20) to ensure sum = 100%

#### For All Shifts (Quick Method):
1. Edit the **first row** ("Wednesday 1 Day") with your desired values
2. Click **"📋 Apply First Row to All Shifts"**
3. All 16 rows will copy the first row's values

#### Reset Everything:
- Click **"🔄 Reset to Defaults (75/25)"**
- All values return to 75% 2P, 25% 4P

### 4. Validate & Save

#### Validation:
- Each row must have: M-2P% + M-4P% = 100%
- Same for G (G-2P% + G-4P% = 100%)
- Same for T (T-2P% + T-4P% = 100%)
- Red error box appears if any validation fails

#### Save:
1. Make your changes
2. Ensure no validation errors (red boxes)
3. Click **"💾 Save Configuration"**
4. Success message appears: "✅ Box split configuration saved successfully!"

#### Cancel:
- Click **"Cancel"** to discard unsaved changes
- Reverts to last saved state

## Example Workflow

### Scenario: Configure Auto lines for 80/20 split on weekday days, 70/30 on weekends

```
1. Click "Configuration" tab
2. Select "Auto" process path tab
3. Edit values:
   - Wednesday 1 Day: M(80/20), G(80/20), T(80/20)
   - Thursday Day: M(80/20), G(80/20), T(80/20)
   - Friday Day: M(80/20), G(80/20), T(80/20)
   - Saturday Day: M(70/30), G(70/30), T(70/30)
   - Sunday Day: M(70/30), G(70/30), T(70/30)
   - Monday Day: M(80/20), G(80/20), T(80/20)
   - Tuesday Day: M(80/20), G(80/20), T(80/20)
   - (Keep night shifts at default 75/25)
4. Click "Save Configuration"
5. Repeat for "LDL" and "Manual Lines" if needed
```

## Tips & Tricks

### Keyboard Shortcuts
- **Tab** - Move to next cell
- **Shift+Tab** - Move to previous cell
- **Enter** - Move to cell below
- **Arrow keys** - Navigate cells

### Quick Fill Strategy
1. Fill first row with most common values
2. Click "Apply First Row to All Shifts"
3. Edit only the exceptions (e.g., weekend shifts)
4. Save

### Validation Errors
If you see validation errors:
- Check the error message for specific shift and box type
- Ensure the two percentages sum to exactly 100
- Common mistake: 80 + 25 = 105 ≠ 100

### Warning Messages
- **Yellow warning** - "You have unsaved changes" → Click Save or Cancel
- **Red error** - Validation failure → Fix the values before saving

## What Happens After Save?

Currently:
- Configuration is saved to **session state**
- Persists while browser tab is open
- Lost on browser refresh

Future integration:
- Configuration will be passed to the solver during plan generation
- Solver will use these as target splits (soft constraint)
- Plan results will show actual vs target splits

## Troubleshooting

### "Save Configuration" button is disabled
→ You have validation errors. Look for red error boxes and fix the percentages.

### My changes disappeared
→ Did you click "Save Configuration"? Unsaved changes are lost on tab switch or refresh.

### Table is hard to read
→ Scroll horizontally if needed. Table shows all 6 columns (M-2P, M-4P, G-2P, G-4P, T-2P, T-4P).

### I want to undo
→ Click "Cancel" before saving to revert to last saved state.

## Next Steps

After configuring box splits:
1. Return to **Planning** tab
2. Run plan generation (in Simulation mode)
3. View results to see impact of configured splits
4. Adjust configuration as needed based on results

## Questions?

Refer to the full implementation summary:
- `/Users/nikhil.ranka/pm-os/box_split_config_implementation_summary.md`
