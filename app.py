"""CleanQ: a laundry order queue built with Flask.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import re

from flask import Flask, render_template, abort, redirect, request, session, url_for

app = Flask(__name__)
# Needed so Flask can remember which mobile number a customer looked up.
app.secret_key = "change-this-before-sharing"

# Services the shop offers. Price is per kilo; hours is the normal turnaround.
SERVICES = [
    {"id": 1, "name": "Wash, dry & fold", "price_per_kilo": 40, "hours": 24},
    {"id": 2, "name": "Wash only", "price_per_kilo": 25, "hours": 12},
    {"id": 3, "name": "Dry only", "price_per_kilo": 20, "hours": 6},
    {"id": 4, "name": "Comforter / bulky", "price_per_kilo": 60, "hours": 48},
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
        "total": round(ticket["kilos"] * service["price_per_kilo"], 2),
        "eta_hours": service["hours"],
    }


def public_view(ticket):
    """What a customer may see: no name, no mobile number, no price."""
    full = describe(ticket)
    return {
        "number": full["number"],
        "service_name": full["service_name"],
        "status": full["status"],
        "eta_hours": full["eta_hours"],
    }


# ---------- Staff side ----------

@app.route("/")
def index():
    # Ticket numbers only, and only orders that are not yet claimed.
    active = [t for t in TICKETS if t["status"] != "claimed"]
    return render_template("index.html", tickets=active)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
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


if __name__ == "__main__":
    app.run(debug=True)