# CleanQ: Laundry Order Queue and Pickup Tracker

**Course:** CCC181 · Week 1 Proposal
**Author:** Kate Mikaela R. Dagohoy

---

## 1. Problem Statement

Neighborhood laundry shops in the Philippines usually track orders with a notebook. This causes recurring problems:

- Customers repeatedly ask if their laundry is ready by text, call, or in person.
- Orders can get mixed up or claimed by the wrong person.
- There are no promised pickup times.

**CleanQ** is a web app where staff log each laundry order, move it through its stages, and let customers check their order's status and estimated pickup time without contacting the shop.

## 2. Setting

A small, owner-operated laundry shop (a few staff, mostly walk-in customers, payment in cash or GCash). Orders are charged per kilo, with some items (comforters, bulky items) priced differently. Shops run mostly on a mobile phone or pen and paper to jot down orders.

## 3. Stakeholders and User Profiles

### Shop Staff / Owner / Manager (primary user)
- **Who:** The person running the counter: a laundry worker, attendant, or the owner or manager. In small shops these are usually the same person, who both handles orders and runs the business. Comfortable with a phone but not with complex software.
- **Goals:** Log an order in seconds, know what to wash next, show customers when their orders are ready quickly, collect every payment, avoid disputes, and understand daily volume and income.
- **Pain points:** Busy hands, constant interruptions, handwriting errors, lost stubs, unpaid balances, unclaimed laundry piling up, no record of daily kilos or revenue.
- **Needs:** Few taps, large buttons, minimal typing, payment status per order, a list of pending and unclaimed orders, and a daily summary.

### Customer
- **Who:** Student, dorm resident, or working adult who drops off laundry and returns later.
- **Goals:** Know when to pick up, avoid wasted trips, be sure the right items come back.
- **Pain points:** Uncertain ready time, having to message the shop repeatedly.
- **Needs:** An order number and a page showing current status and estimated pickup time.

## 4. Research

### 4.1 Existing practice through observation
- Paper notebook logs and numbered claim stubs.
- Customer often just go back to the shops in-person to check if their laundry iss ready or end up staying in the shop the whole time.

## 5. Functional Requirements

Priority: **Must** = needed for the Week 2 prototype, **Should** = planned for later weeks, **Could** = if time allows.

| ID | Requirement | Priority | Profile | Acceptance criteria |
|----|-------------|----------|---------|---------------------|
| FR-01 | The staff dashboard shall list all current orders by ticket number only. | Must | Staff | Dashboard shows one clickable ticket number for every order that is not yet claimed, with no other order details. |
| FR-02 | Clicking a ticket number shall open a detail page with the full order information. | Must | Staff | Opening `/queue/<number>` shows customer name, mobile number, service, kilos, notes, payment status, current stage, total, and estimated pickup time; an unknown number returns a 404 page. |
| FR-03 | Each order shall record customer name, mobile number, service type, kilos, notes, and payment status. | Must | Staff | Every order in the data has all of these fields. |
| FR-04 | The system shall offer a defined list of services, each with a price per kilo and a normal turnaround time. | Must | Staff | Services include wash-dry-fold, wash only, dry only, and comforter/bulky. |
| FR-05 | The system shall compute the order total from kilos and service price. | Must | Staff | Total shown on the detail page matches kilos × price per kilo. |
| FR-06 | The system shall estimate a ready time for each order based on its service's turnaround time. | Must | Staff, Customer | Detail page shows the estimated hours until pickup. |
| FR-07 | Each order shall be linked to the customer's mobile number, and customers shall be able to enter their mobile number to see their ticket number(s). | Must | Customer | Entering a registered mobile number lists the ticket number(s) tied to it; an unregistered number shows a "no orders found" message. |
| FR-08 | Customers shall be able to click their ticket number to see their order's status and estimated pickup time. | Must | Customer | The customer page shows the ticket number, service, current stage, and estimated pickup time, without showing the mobile number or other customers' tickets. |
| FR-09 | Staff shall be able to create a new order through a form. | Should | Staff | Submitting the form adds an order with the next ticket number. |
| FR-10 | Staff shall be able to advance an order to its next stage with one action. | Should | Staff | One click moves the status forward and the change appears on the detail page. |
| FR-11 | Staff shall be able to mark an order as paid. | Should | Staff | Payment status updates on the detail page. |
| FR-12 | The system shall flag orders that are ready but unclaimed after a set number of days. | Could | Staff | Orders past the limit appear in a separate "unclaimed" list. |
| FR-13 | The system shall show a daily summary of orders received, kilos processed, and revenue. | Could | Staff | Summary page totals match the order records for the day. |

## 6. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-01 | **Usability:** Staff can log an order in under 30 seconds on a phone screen. |
| NFR-02 | **Readability:** Large buttons and plain Filipino/English labels (Taglish) suited to non-technical staff. |
| NFR-03 | **Performance:** Pages load in under 2 seconds on a typical mobile connection. |
| NFR-04 | **Privacy:** Customers can only see tickets linked to the mobile number they enter, and mobile numbers are never displayed on customer pages. |
| NFR-05 | **Portability:** Runs on any modern browser with no installation. |

## 7. Scope

**In scope (course project):**
- Flask web app with Jinja2 templates
- In-memory data first, with a possible later move to a database
- Order list, order detail, order creation, status updates

**Out of scope (future work):**
- Real SMS or Messenger notifications
- Online payment processing
- Delivery and rider management
- Offline sync and multi-branch support

## 8. Data Model (initial)

**Service:** `id`, `name`, `price_per_kilo`, `hours`

**Ticket (order):** `number`, `name`, `phone`, `service_id`, `kilos`, `notes`, `paid`, `status`

**Status values:** `received`, `washing`, `drying`, `folding`, `ready`, `claimed`

## 9. Success Measures

- A staff member can create and advance an order without help.
- A customer can see their order's status and estimated pickup time using their mobile number alone.
- The owner can see which orders are unpaid or unclaimed at a glance.

## 10. Risks

| Risk | Mitigation |
|------|------------|
| Staff find the app slower than the notebook and go back to paper | Keep order entry to a few fields and test with a real user |
| Unreliable shop internet | Keep the app lightweight; list offline support as future work |
| Estimated ready times are inaccurate | Start with fixed turnaround per service; refine using real data later |
| Customer data privacy | Hide phone numbers from public pages (NFR-04) |

## 11. Work Plan

| Week | Deliverable |
|------|-------------|
| 1 | Proposal, profiles, research, requirements (this document) |
| 2 | Flask starter app with sample laundry data, ticket dashboard, order detail page, and customer lookup (FR-01 to FR-09) |
| 3+ | Order form, status updates, payment tracking (FR-10 to FR-12), then extras |