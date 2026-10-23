# CleanQ Personas

## Kim Possible, the person waiting

> Wants to know when her laundry would be ready for pickup.

| | |
| --- | --- |
| **Photo or sketch** | docs/week3/screenshots/KimPossible_Persona1.png |
| **Age, role and background** | 20, 3rd-year student living in a dorm, drops off laundry before class and returns later in the day |
| **Goals** | Know when her laundry is ready so she doesn't waste a trip; be sure she gets the right bag back; see the estimated pickup time without messaging the shop |
| **Frustrations** | Customers often have to go back to the shop in person just to check if laundry is ready, or end up staying the whole time *(observation)*; the only proof of her order is a numbered claim stub that can get lost *(observation)* |
| **Devices and context** | Her own phone, between classes or in the dorm, usually with one hand free and a limited data plan |
| **Tech comfort** | High: uses messaging, social and payment apps daily, but has no patience for apps that need sign-up |
| **Accessibility needs** | One-handed use on a small screen, possibly slow mobile data, bright daylight glare, so readable text and high contrast |

### Scenario

Kim drops off 5 kilos of laundry at the shop near her dorm before her 8 AM class and gets ticket #1. At lunch she wonders if it is ready, but the shop is a 10-minute walk away. She opens CleanQ on her phone, types her mobile number, and sees ticket #1 listed. She taps it, sees that it is still in the washer with an estimated 2 hours in total, and decides to check again after her last class instead of making a wasted trip.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Look up my tickets using my mobile number | Check my laundry | FR-07 |
| See the status of my ticket | My ticket | FR-08 |
| See the estimated pickup time | My ticket | FR-06, FR-08 |
| Know which stage my laundry is in (received → ... → ready) | My ticket | FR-08 |

### What this means for my interface

1. Because Kim checks between classes with one hand free, my interface must let her find her ticket with just her mobile number and one tap, with no account or sign-up.
2. Because she may have more than one ticket, my interface must list ticket numbers first and show details only after she taps one.
3. Because she has a limited data plan and often slow connections, my interface must stay lightweight, with plain text and no large images.
4. Because her mobile number is private, my interface must never display a mobile number on customer pages, and she must only see tickets tied to the number she entered.

## Mort, the staff member

> Staff Member

| | |
| --- | --- |
| **Photo or sketch** | docs/week3/screenshots/Mort_Persona2.png |
| **Age, role and background** | 48, owner who also works the counter at a small neighborhood laundry shop with a few staff |
| **Goals** | Log each order quickly while customers wait; know what to wash next; collect every payment; stop customers from asking "ready na ba?" again and again |
| **Frustrations** | Orders are written in a paper notebook *(observation)*; customers rely on numbered claim stubs that can be lost or mixed up *(observation)*; customers keep coming back in person to ask for updates *(observation)* |
| **Devices and context** | A smartphone propped on the counter or one shared computer, used while sorting clothes, handling customers and taking payment, often with wet or busy hands |
| **Tech comfort** | Low to medium: comfortable with messaging and GCash on her phone, but not with complex software |
| **Accessibility needs** | Busy or wet hands, so large tap targets; glasses, so large readable text; a noisy, interrupted counter, so very few steps per task |

### Scenario

It is mid-afternoon and the shop is full. A customer hands Mort a bag of laundry while another asks if their clothes are ready. Mort opens CleanQ on the counter phone, sees the list of ticket numbers, and taps ticket #3 to check its details. He sees that it is marked ready and paid, tells the customer right away, and moves on. When the next bag arrives, he logs it in a few taps instead of writing in the notebook.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| See all current tickets at a glance | Dashboard | FR-01 |
| Open a ticket to see its full details | Ticket detail | FR-02 |
| Log a new order | New order | FR-09 |
| Move an order to the next stage | Ticket detail | FR-10 |
| Mark an order as paid | Ticket detail | FR-11 |

### What this means for my interface

1. Because Mort is often interrupted and has busy hands, my interface must use large buttons and as few taps as possible for every task.
2. Because he handles many orders at once, my interface must show only ticket numbers on the dashboard so the list is easy to scan, and put all other details one tap away.
3. Because he is not comfortable with complex software, my interface must use plain English labels and avoid long forms or hidden menus.
4. Because customers keep asking if their laundry is ready, my interface must show each order's current stage clearly on the ticket page so she can answer in seconds.