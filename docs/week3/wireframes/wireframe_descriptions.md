# CleanQ Wireframe Descriptions

---

### Frame 1: Join Queue — Mobile
- **Persona:** Mort (Staff Member) / Kim Possible (Customer)
- **Device:** Mobile / Phone Width
- **Requirement IDs:** FR-03, FR-04, FR-07, FR-09
- **Main Flow**: Open site -> Fill customer name & mobile -> Select service & weight -> Tap "Create ticket"  
- **Key Features:**
  - Form fields (Name, Mobile, Service, Weight) are stacked in a single vertical column with large touch targets for easy one-handed typing on a phone.
  - Displays live ticket preview card near the bottom so Mort can double-check order totals and pickup times before submitting.
  - Includes an "Already in the queue?" search box at the bottom allowing Kim to quickly look up her ticket using her mobile number.

---

### Frame 2: Join Queue — Desktop
- **Persona:** Mort (Staff Member) / Kim Possible (Customer)
- **Device:** Desktop / Laptop Width
- **Requirement IDs:** FR-03, FR-04, FR-07, FR-09
- **Main Flow**: Open site -> Input order details -> Review sticky preview -> Click "Create ticket #1053"
- **Key Features:**
  - Uses a 2-column layout with order entry inputs on the left side and a sticky Ticket Preview card on the right.
  - Shows service choices as full-width cards detailing price per kilo and turnaround time for fast counter selection.
  - Prominently features the primary action button ("Create ticket #1053") inside the right panel for immediate visibility on wide screens.

---

### Frame 3: Customer Dashboard — Mobile
- **Persona:** Kim Possible (Customer)
- **Device:** Mobile / Phone Width
- **Requirement IDs:** FR-01, FR-07, FR-08
- **Main Flow**: Open site -> Enter mobile number -> Tap "Find my tickets" -> See ticket status & pickup time
- **Key Features:**
  - Shows Kim's active ticket number (`#1053`) in extra-large text right at the top so she sees her status instantly.
  - Summarizes service type, current processing stage, and estimated pickup time into high-contrast stacked cards.
  - Displays full shop queue grid with ticket numbers only, visually highlighting Kim's active ticket in blue.

---

### Frame 4: Customer Dashboard — Desktop
- **Persona:** Kim Possible (Customer)
- **Device:** Desktop / Laptop Width
- **Requirement IDs:** FR-01, FR-07, FR-08
- **Main Flow**: Open site -> View horizontal status overview -> Locate highlighted ticket in queue grid
- **Key Features:**
  - Spreads status cards (Service, Current Stage, Estimated Pickup) horizontally across top banner for desktop viewing.
  - Displays a multi-column grid of all active shop tickets, hiding personal names/numbers to protect privacy.
  - Places a wide lookup input card at the bottom allowing returning customers to retrieve their ticket by phone number.

---

### Frame 5: Manage Queue (Ticket Detail) — Mobile
- **Persona:** Mort (Staff Member)
- **Device:** Mobile / Phone Width
- **Requirement IDs:** FR-02, FR-05, FR-06, FR-10, FR-11
- **Main Flow**: Staff opens dashboard -> Selects ticket #1048 -> Taps "Advance to Drying" -> Taps "Mark as paid" 
- **Key Features:**
  - Displays full customer details (Name, Phone, Weight, Special Notes) in a clear vertical list for counter reference.
  - Features a prominent blue primary button ("Advance to Drying") below stage timeline for quick one-tap status updates.
  - Includes payment calculation breakdown and a dedicated "Mark as paid" action button at bottom.

---

### Frame 6: Manage Queue (Ticket Detail) — Desktop
- **Persona:** Mort (Staff Member)
- **Device:** Desktop / Laptop Width
- **Requirement IDs:** FR-02, FR-05, FR-06, FR-10, FR-11
- **Main Flow**: Staff opens dashboard -> Clicks ticket #1048 -> Reviews left-side order details -> Clicks right-side stage & payment actions
- **Key Features:**
  - Employs side-by-side layout: left column contains customer order details; right column holds stage progress and payment actions.
  - Stage tracking timeline clearly marks completed steps with checkmarks and highlights current active stage.
  - Keeps operational control buttons permanently visible on right sidebar without needing to scroll.