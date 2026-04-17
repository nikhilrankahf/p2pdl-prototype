# P2PDL Prototype Ready for Review - Riptide v2

Hi team,

I've built an interactive prototype for the **P2PDL (Print 2 PDL)** feature that demonstrates the end-to-end workflow planners will use in Riptide v2. This is for requirements validation and feedback gathering.

**🔗 Access the prototype:** [Your Streamlit URL here]

---

## 📌 Important Note

**This prototype focuses on workflow and functionality, not final UX.** The goal is to validate:
• The step-by-step planner workflow
• Lane selection logic and filters
• Simulation and validation flow
• How P2PDL configuration moves from Simulation to Production

The final UX in Riptide v2 will be polished and may look different. Some UI elements, layouts, and interactions should be expected to change in the production implementation.

---

## What This Prototype Demonstrates

✅ **FR1: Lane Selection Interface** - Filter, sort, and select lanes for P2PDL
✅ **FR2: Simulation & Validation** - Run simulation to assess P2PDL impact on volume metrics
✅ **FR3: Plan Promotion** - Promote validated configuration from Simulation to Production

---

## How to Use the Prototype

### **Scenario: Configure P2PDL Lanes and Validate Impact**

#### **Step 1: Switch to Simulation Mode**
• In the top header, change **Mode** dropdown from `Production` to `Simulation`
• You'll see a blue "Simulation Mode" banner

#### **Step 2: Configure P2PDL Lanes**
1. Click the **☰ hamburger menu** (in the Simulation 7 row, first column)
2. Select **"Configuration"** from the Planning Levers menu
3. A modal will open - scroll down past Live Needs, Kit Inventory, and Line Throughput
4. In the **P2PDL (Print 2 PDL)** section:
   • Use filters to narrow down lanes (Ship Day, Brand, Selection Status)
   • Click column headers to sort (CPT, Box Volume, etc.)
   • Check the boxes next to lanes you want to select for P2PDL
   • Note: "Ship Day" shows when the lane ships (from CPT). P2PDL work happens **1 day before** ship day
5. Click **"Save Configuration"** at the bottom

#### **Step 3: Run Simulation**
1. You'll return to the Dashboard - notice the info box showing your P2PDL configuration
2. Click **"▶️ Simulate Plan Gen"** (blue button)
3. The simulation will run and display:
   • **Key Metrics**: ODL/PDL Volume, Allocated/Total, Unallocated, Completed
   • **Needs Action - LATE Boxes Risk**: Expandable section showing CPT risk status
   • **Volume Metrics**: Expandable section with:
     - RoW Volume and Grocery (Complexity) tables
     - **Total P2PDL Volume by Shift**: Shows shift-level P2PDL volume
     - **Drill-down**: Select a shift from the dropdown to see which specific lanes contribute to that shift's volume

#### **Step 4: Promote to Production**
1. If the simulation looks good, click **"📋 Promote to Production Plan"** (gray button)
2. You'll see a success message: "✅ Your configuration has been saved to Production Mode"
3. Toggle **Mode** to `Production` in the header to see the promoted configuration

#### **Step 5: View Production Configuration**
1. In Production mode, you'll see:
   • Green success banner showing P2PDL is active with lane count and volume
   • Hamburger menu (☰) below "AZ 2026-W15"
2. Click **☰ → Configuration** to view/edit selected P2PDL lanes
3. In Production mode, **only selected P2PDL lanes** are shown (not all lanes)
4. You can add more lanes or deselect lanes, then "Save Configuration"

---

## Key Behaviors to Note

📌 **Lane Identification**: Each lane is uniquely identified by Lane + Ship Day (prevents duplicate selections)
📌 **P2PDL Scheduling**: Lanes are scheduled for P2PDL **1 day before ship day** (e.g., Tuesday ship → Monday P2PDL shift)
📌 **Shift Assignment**: CPT time determines AM (day) vs PM (night) shift assignment
📌 **Production Management**: In Production mode, Configuration shows only selected P2PDL lanes (FR6)

---

## What I Need from You

**Engineering:**
• Does the workflow match your technical understanding of how P2PDL should work?
• Any concerns about the lane selection logic (1 day before ship day, shift assignment based on CPT time)?
• Feedback on the Configuration modal structure (Live Needs, Kit Inventory, Line Throughput, P2PDL)

**Planners/Ops:**
• Does this workflow reflect how you'd want to configure P2PDL?
• Are the filters and drill-downs (shift → lanes) useful for your decision-making?
• What's missing or confusing?

**Focus your feedback on the workflow and functionality, not the visual design.**

**Please test the workflow and reply with feedback by [date].**

---

📧 Questions? Ping me on Slack or reply to this thread.

Thanks!
Nikhil
