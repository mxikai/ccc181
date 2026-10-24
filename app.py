"""CleanQ: a laundry order queue built with Flask.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import re

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
# Needed so Flask can remember which mobile number a customer looked up.
app.secret_key = "change-this-before-sharing"

# Services the shop offers. Price is per kilo; hours is the normal turnaround.
SERVICES = [
    {"id": 1, "name": "Wash, dry & fold", "price_per_kilo": 65, "hours": 3},
    {"id": 2, "name": "Wash only", "price_per_kilo": 35, "hours": 2},
    {"id": 3, "name": "Dry only", "price_per_kilo": 30, "hours": 1},
    {"id": 4, "name": "Comforter / bulky", "price_per_kilo": 100, "hours": 6},
]

# The order moves through these statuses, one tap at a time.
STATUSES = ["received", "washing", "drying", "folding", "ready", "claimed"]

# Each ticket: number, name, phone, service_id, kilos, notes, paid, status
TICKETS = [
    {"number": 1, "name": "Ana Reyes", "phone": "09171234567", "service_id": 1,
     "kilos": 5.0, "notes": "No fabcon", "paid": False, "status": "washing"},
    {"number": 2, "name": "Ben Santos", "phone": "09287654321", "service_id": 4,
     "kilos": 3.5, "notes": "Separate whites", "paid": True, "status": "received"},
    {"number": 3, "name": "Ana Reyes", "phone": "09171234567", "service_id": 2,
     "kilos": 2.0, "notes": "", "paid": True, "status": "ready"},
    {"number": 4, "name": "Carla Cruz", "phone": "09451112222", "service_id": 3,
     "kilos": 4.0, "notes": "", "paid": False, "status": "claimed"},
]


def get_service(service_id):
    return next((s for s in SERVICES if s["id"] == service_id), None)


def normalize_phone(raw):
    """Turn '+63 917 123 4567' or '0917-123-4567' into '09171234567'.

    Returns None if it doesn't look like a Philippine mobile number.
    """
    digits = re.sub(r"\D", "", raw or "")
    if digits.startswith("63") and len(digits) == 12:
        digits = "0" + digits[2:]
    elif len(digits) == 10 and digits.startswith("9"):
        digits = "0" + digits
    if len(digits) == 11 and digits.startswith("09"):
        return digits
    return None


def describe(ticket):
    """Return a copy of the ticket with the service name, total price and ETA filled in."""
    service = get_service(ticket["service_id"])
    return {
        **ticket,
        "service_name": service["name"],
        "price_per_kilo": service["price_per_kilo"],
        "total": round(ticket["kilos"] * service["price_per_kilo"], 2),
        "eta_hours": service["hours"],
    }


# Statuses where the laundry is still being processed (the customer is "waiting").
IN_PROGRESS = ("received", "washing", "drying", "folding")


def tickets_ahead(ticket):
    """Earlier tickets for the same service that are still being processed."""
    return sum(
        1 for t in TICKETS
        if t["service_id"] == ticket["service_id"]
        and t["number"] < ticket["number"]
        and t["status"] in IN_PROGRESS
    )


def public_view(ticket):
    """What a customer may see: no name, no mobile number, no price."""
    full = describe(ticket)
    return {
        "number": full["number"],
        "service_name": full["service_name"],
        "status": full["status"],
        "eta_hours": full["eta_hours"],
        "ahead": tickets_ahead(ticket),
    }

# ---------- Staff side ----------

@app.route("/")
def index():
    # Short welcome page for the person waiting.
    return render_template("index.html")


@app.get("/join")
def join_form():
    # Show an empty order form.
    return render_template("join.html", services=SERVICES, form={}, errors={})


@app.post("/join")
def join():
    # Handle the submitted form. Never trust the input: check every field here,
    # even though the browser may have checked it already.
    form = request.form
    name = " ".join(form.get("name", "").split())
    phone = normalize_phone(form.get("phone", ""))
    service_id = form.get("service_id", type=int)
    paid = form.get("paid", "unpaid")
    notes = form.get("notes", "").strip()

    try:
        kilos = round(float(form.get("kilos", "")), 2)
    except ValueError:
        kilos = None

    errors = {}
    if not name:
        errors["name"] = "Enter the customer's name."
    elif len(name) > 60:
        errors["name"] = "Keep the name to 60 characters or fewer."
    if phone is None:
        errors["phone"] = "Enter a valid mobile number, like 0917 123 4567."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."
    if kilos is None or not (0.1 <= kilos <= 50):
        errors["kilos"] = "Enter the weight in kilos, between 0.1 and 50."
    if paid not in ("paid", "unpaid"):
        errors["paid"] = "Choose paid or unpaid."
    if len(notes) > 200:
        errors["notes"] = "Keep the notes to 200 characters or fewer."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template(
            "join.html", services=SERVICES, form=form, errors=errors
        ), 400

    number = max((t["number"] for t in TICKETS), default=0) + 1
    TICKETS.append({
        "number": number, "name": name, "phone": phone,
        "service_id": service_id, "kilos": kilos, "notes": notes,
        "paid": paid == "paid", "status": "received",
    })
    flash(f"Ticket #{number} created for {name}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.route("/staff")
def staff_dashboard():
    # FR-01: ticket numbers only, and only orders not yet claimed.
    # Placeholder page until the full dashboard is built (Part 7).
    active = [t for t in TICKETS if t["status"] not in ("claimed", "left")]
    return render_template("staff_dashboard.html", tickets=active)

@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # FR-02: all the details live here.
    ticket_data = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if not ticket_data:
        abort(404)
    return render_template(
        "ticket.html", ticket=describe(ticket_data), statuses=STATUSES
    )
    
# ---------- Customer side ----------

@app.route("/track")
def track():
    # Customer enters a mobile number and sees the tickets linked to it.
    raw = request.args.get("phone", "").strip()
    if not raw:
        return render_template("track.html", searched=False, error=None, tickets=[])

    phone = normalize_phone(raw)
    if phone is None:
        return render_template(
            "track.html", searched=False, tickets=[],
            error="Please enter a valid mobile number, like 0917 123 4567.",
        )

    session["phone"] = phone  # remembered so the ticket page can check it
    mine = [t for t in TICKETS if t["phone"] == phone]
    return render_template("track.html", searched=True, error=None, tickets=mine)


@app.route("/track/<int:ticket_id>")
def track_ticket(ticket_id):
    # A customer can only open tickets tied to the number they entered.
    phone = session.get("phone")
    if not phone:
        return redirect(url_for("track"))
    ticket_data = next(
        (t for t in TICKETS if t["number"] == ticket_id and t["phone"] == phone), None
    )
    if not ticket_data:
        abort(404)
    return render_template(
        "track_ticket.html", ticket=public_view(ticket_data), statuses=STATUSES
    )

@app.post("/track/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    # Customer cancels their own ticket. Only works for a number they looked up.
    phone = session.get("phone")
    if not phone:
        return redirect(url_for("track"))
    ticket_data = next(
        (t for t in TICKETS if t["number"] == ticket_id and t["phone"] == phone), None
    )
    if not ticket_data:
        abort(404)
    if ticket_data["status"] in IN_PROGRESS:
        ticket_data["status"] = "left"
        flash(f"You left the queue. Ticket #{ticket_id} was cancelled.", "success")
    else:
        flash("This ticket can no longer be cancelled.", "warning")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)