# CleanQ requirements

**Setting:** Small neighborhood laundry shop in the Philippines. Mostly walk-in customers who drop off a bag and come back later. Payment in cash or GCash. Orders are charged per kilo.
**People who wait:** Customers who drop off laundry, such as students and dorm residents. See Kim Possible in [docs/week3/personas.md](week3/personas.md).
**People who serve:** The shop owner or attendant at the counter, often with busy hands. See Mort in [docs/week3/personas.md](week3/personas.md).

**Problem statement:** A student who drops off laundry needs a way to know when it will be ready without walking back to the shop, because the paper claim stub says nothing about progress and she has to ask in person or stay and wait.

Status values: *Built (Week 3)*, *This week*, *Later*, *Dropped*. IDs are never reused or renumbered. These IDs replace the draft numbering in the Week 1 proposal.

## Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
|----|-------------|----------|--------------|--------|
| FR-01 | A staff member can create an order by entering the customer's name, mobile number, service, kilos, paid or unpaid, and notes, and get the next ticket number. | Must | Yes | Built (Week 3) |
| FR-02 | A staff member can see all active tickets in ticket order and filter them by service. | Must | Yes | Built (Week 3) |
| FR-03 | A staff member can open a ticket to see its full details: name, mobile number, service, kilos, notes, total price, payment status, stage and estimated pickup. | Must | Yes | Built (Week 3) |
| FR-04 | A staff member can move a ticket to its next stage with one tap (received, washing, drying, folding, ready, claimed). | Must | Yes | Built (Week 3) |
| FR-05 | A staff member can mark a ticket as paid. | Must | Yes | Built (Week 3) |
| FR-06 ★ | A staff member is warned when a ticket is claimed while still unpaid. | Must | Yes | Built (Week 3) |
| FR-07 | A customer can enter only their mobile number to see their own tickets. | Must | Yes | Built (Week 3) |
| FR-08 | A customer can see their ticket number, service, current stage in words, estimated pickup time and how many tickets are ahead of them. | Must | Yes | Built (Week 3) |
| FR-09 | A customer can leave the queue before their laundry is finished. | Must | Yes | Built (Week 3) |
| FR-10 | A staff member can start the next waiting load with one tap, optionally for one service. | Should | Yes | Built (Week 3) |
| FR-11 ★ | A staff member can see today's claimed orders with kilos, sales collected and unpaid totals. | Should | Yes | Built (Week 3) |
| FR-12 ★ | A staff member can add, rename, change the price or turnaround of, and switch off a service. | Must | Yes | This week |
| FR-13 | A staff member can cancel a ticket. | Should | Yes | Built (Week 3) |
| FR-14 | A customer's ticket page updates its status every 10 seconds without a reload. | Should | No | Built (Week 3) |
| FR-15 ★ | A staff member can see a list of orders that are ready but unclaimed for more than a set number of days. | Should | Yes | Later |
| FR-16 ★ | A staff member can see a list of all unpaid orders, including claimed ones. | Should | Yes | Later |
| FR-17 | A staff member must log in before using any staff page. | Should | Yes | Later |
| FR-18 | A staff member can correct the kilos or notes of an order after it is created. | Could | Yes | Later |

## Non-functional requirements

| ID | Requirement | Category | Priority |
|----|-------------|----------|----------|
| NFR-01 | No ticket is lost when the server or the database restarts. | Reliability | Must |
| NFR-02 | Two customers can never get the same ticket number, even if two orders are created at the same moment. | Data integrity | Must |
| NFR-03 | The customer ticket page loads in under 2 seconds on mobile data. | Performance | Should |
| NFR-04 | Every screen scores 90 or higher in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-05 | No password or secret key is stored in the repository. | Security | Must |
| NFR-06 | Customer pages never show a mobile number, a name, a price or another customer's ticket. | Privacy | Must |
| NFR-07 | A staff member can create an order in under 30 seconds on a phone. | Usability | Should |

## MVP

**MVP:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08, FR-09, FR-12, and NFR-01, NFR-02, NFR-04, NFR-05, NFR-06. These cover the full loop: staff log and advance orders, customers check their own ticket, and everything survives a restart. Anything less leaves customers asking "ready na ba?" again.

**Out of scope:**
- Real SMS or Messenger notifications: they need a paid provider and approval, and the ticket page already answers the same question.
- Online payment processing (GCash integration): it needs a merchant account and raises security risks; staff just mark orders paid.
- Delivery and rider management: the shop is walk-in only, and this is a separate product.
- Multi-branch support: the persona is a single owner-run shop.

## Check with a real person

I showed this list to one person from the setting for about 10 minutes. I asked what was missing, what was wrong or unimportant, and which three requirements mattered most.

| Who (role only, no full name) | What they said | What I changed |
|-------------------------------|----------------|----------------|
| Laundry customer | "I can't think of anything missing. It already covers the basics, and adding more would just make it complicated." Most important to them: FR-01, FR-03 and FR-08. | Nothing. I kept the list as it is. Their answer supports keeping the MVP small and leaving SMS, online payment and delivery out of scope. |

**Why I kept the list as it is:** The person found that the requirements already cover the basic needs, and said more features would only make the app complicated. That matches the few-tap, plain design in my personas. Their top three (FR-01, FR-03, FR-08) are all Must and already Built (Week 3), and all three are in the MVP, so no priority needed to change. Their answer also supports keeping SMS, online payment and delivery out of scope. I will keep the Should, Could and Later items out of the MVP unless a later test shows a real need.