# CleanQ

A laundry order queue and pickup tracker for small neighborhood laundry shops in the Philippines, built with Flask, Jinja2 and Bootstrap 5 for **CCC181** (Git, GitHub & Flask foundations).

Staff log orders and move them through stages. Customers enter their mobile number to see their own tickets, the current stage, the estimated pickup time and how many tickets are ahead of them.

## Requirements

The full list of what CleanQ must do, with priorities, MVP and out-of-scope items, is in [docs/requirements.md](docs/requirements.md).

## Features

**Staff**
- **New Order** (`/join`): create a ticket with name, mobile number, service, weight, payment status and notes. The server checks every field.
- **Dashboard** (`/staff`): active tickets in order, a filter by service with a count of waiting tickets, a "Start next load" button, Advance and Cancel buttons on each row, and a "Claimed today" log with kilos, sales collected and unpaid totals.
- **Manage Queue** (`/queue`): one ticket's full details, a stage list, an Advance button (pinned to the bottom on phones) and a Mark as paid button.

**Customers**
- **Customer Dashboard** (`/track`): enter a mobile number to see only your own tickets.
- **Ticket page** (`/track/<id>`): large ticket number, service, current stage in words, estimated pickup and "N tickets ahead of you". The page refreshes its status every 10 seconds without a reload. Customers can leave the queue.
- Customers never see mobile numbers, names, prices or other people's tickets.

## Stages

`received → washing → drying → folding → ready → claimed`

A ticket that is cancelled by staff or by the customer gets the status `left`.

## Services

| Service | Price per kilo | Turnaround |
|---|---|---|
| Wash, dry & fold | ₱65 | 3 hours |
| Wash only | ₱35 | 2 hours |
| Dry only | ₱30 | 1 hour |
| Comforter / bulky | ₱100 | 6 hours |

## Routes

| URL | Method | What it does |
|---|---|---|
| `/` | GET | Welcome page |
| `/join` | GET, POST | New Order form and ticket creation |
| `/staff` | GET | Staff Dashboard (`?service_id=` filters by service) |
| `/staff/call-next` | POST | Start the oldest ticket that is still "received" |
| `/staff/tickets/<id>/<action>` | POST | `advance`, `cancel` or `pay` for one ticket |
| `/queue` | GET | Manage Queue tab: opens the oldest active ticket |
| `/queue/<id>` | GET | Manage Queue for one ticket (404 if unknown) |
| `/track` | GET | Customer lookup (`?phone=`); a plain visit always starts blank |
| `/track/<id>` | GET | Customer ticket page, only for the number they looked up |
| `/track/<id>/status.json` | GET | Status and "ahead" count used by the live refresh |
| `/track/<id>/leave` | POST | Customer cancels their own ticket |

Every action that changes data uses POST, never a plain link.

## Project structure

```
ccc181/
├── app.py                   # routes, sample data and helpers
├── requirements.txt
├── .gitignore               # keeps .venv and __pycache__ out of Git
├── README.md
├── templates/
│   ├── base.html            # layout, navbar, flash messages, skip link
│   ├── index.html           # welcome page
│   ├── join.html            # New Order form
│   ├── staff_dashboard.html # staff Dashboard
│   ├── ticket.html          # Manage Queue (staff)
│   ├── track.html           # customer lookup and ticket list
│   └── track_ticket.html    # customer ticket page
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js          # double-submit guard on New Order
└── docs/
    ├── requirements.md      # living requirements list
    ├── week1/
    │   └── proposal.md
    └── week3/
        ├── personas.md
        ├── feedback.md      # wireframe self-review
        ├── accessibility.md
        ├── usability-test.md
        ├── report.md
        ├── screenshots/     # before/after, persona images
        └── wireframes/      # wireframe images and descriptions
```