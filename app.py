"""CleanQ: a laundry order queue built with Flask.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import os
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Customer, Service, Staff, Ticket, db

load_dotenv()

app = Flask(__name__)
# Needed so Flask can remember which mobile number a customer looked up.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving

@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 26, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""

@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [
        ("Wash, dry & fold", 65, 3),
        ("Wash only", 35, 2),
        ("Dry only", 30, 1),
        ("Comforter / bulky", 100, 6),
    ]
    for name, price, hours in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, price_per_kilo=price, hours=hours))
    db.session.commit()
    print("Services are ready.")

# The order moves through these statuses, one tap at a time.
STATUSES = ["received", "washing", "drying", "folding", "ready", "claimed"]

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


def describe(t):
    """Return a dict with the ticket's customer, service, total price and ETA filled in."""
    return {
        "id": t.id,
        "number": t.id,
        "name": t.customer.name,
        "phone": t.customer.phone,
        "service_id": t.service_id,
        "service_name": t.service.name,
        "kilos": float(t.kilos),
        "notes": t.notes,
        "paid": t.paid,
        "status": t.status,
        "price_per_kilo": float(t.price_per_kilo),
        "total": round(float(t.kilos * t.price_per_kilo), 2),
        "eta_hours": t.service.hours,
        "claimed_at": t.claimed_at,
        "created_at": t.created_at,
    }

# Statuses where the laundry is still being processed (the customer is "waiting").
IN_PROGRESS = ("received", "washing", "drying", "folding")


def tickets_ahead(t):
    """Count tickets still being processed for the same service that joined before t."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status.in_(IN_PROGRESS),
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)


def public_view(t):
    """What a customer may see: no name, no mobile number, no price."""
    return {
        "id": t.id,
        "number": t.id,
        "service_id": t.service_id,
        "service_name": t.service.name,
        "status": t.status,
        "eta_hours": t.service.hours,
        "created_at": t.created_at,
        "ahead": tickets_ahead(t),
    }

# ---------- Staff side ----------

@app.route("/")
def index():
    # Short welcome page for the person waiting.
    return render_template("index.html")


def all_services():
    """Every service, switched on or off. Used by staff pages."""
    return db.session.scalars(
        db.select(Service).order_by(Service.sort_order, Service.id)
    ).all()


def active_services():
    """Only switched-on services. Used by the New Order form."""
    return db.session.scalars(
        db.select(Service).where(Service.is_active)
        .order_by(Service.sort_order, Service.id)
    ).all()


@app.get("/join")
def join_form():
    # Show an empty order form.
    return render_template("join.html", services=active_services(), form={}, errors={})


@app.post("/join")
def join():
    # Never trust the input: check every field here, even though the browser may have too.
    form = request.form
    name = " ".join(form.get("name", "").split())
    phone = normalize_phone(form.get("phone", ""))
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None
    paid = form.get("paid", "unpaid")
    notes = form.get("notes", "").strip()

    try:
        kilos = Decimal(form.get("kilos", "")).quantize(Decimal("0.01"))
    except InvalidOperation:
        kilos = None

    if kilos is not None and not kilos.is_finite():
        kilos = None
        
    errors = {}
    if not name:
        errors["name"] = "Enter the customer's name."
    elif len(name) > 60:
        errors["name"] = "Keep the name to 60 characters or fewer."
    if phone is None:
        errors["phone"] = "Enter a valid mobile number, like 0917 123 4567."
    if service is None or not service.is_active:
        errors["service_id"] = "Choose a service."
    if kilos is None or not (Decimal("0.1") <= kilos <= Decimal("50")):
        errors["kilos"] = "Enter the weight in kilos, between 0.1 and 50."
    if paid not in ("paid", "unpaid"):
        errors["paid"] = "Choose paid or unpaid."
    if len(notes) > 200:
        errors["notes"] = "Keep the notes to 200 characters or fewer."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template(
            "join.html", services=active_services(), form=form, errors=errors
        ), 400

    # Reuse the customer if this mobile number is already in the database.
    customer = db.session.scalar(db.select(Customer).filter_by(phone=phone))
    if customer is None:
        customer = Customer(name=name, phone=phone)

    ticket_row = Ticket(
        customer=customer,
        service=service,
        kilos=kilos,
        price_per_kilo=service.price_per_kilo,  # price at the time of the order
        notes=notes,
        paid=(paid == "paid"),
    )
    db.session.add(ticket_row)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving the ticket. Please try again.", "danger")
        return render_template(
            "join.html", services=active_services(), form=form, errors={}
        ), 409

    flash(f"Ticket #{ticket_row.id} created for {customer.name}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket_row.id))

@app.get("/staff")
def staff_dashboard():
    # FR-01. Open to everyone for now (no login until a later week).
    service_id = request.args.get("service_id", type=int)

    stmt = (db.select(Ticket)
            .where(Ticket.status.not_in(("claimed", "left")))
            .order_by(Ticket.created_at))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = [describe(t) for t in db.session.scalars(stmt).all()]

    services = all_services()

    # How many tickets are waiting (still being processed) per service.
    rows = db.session.execute(
        db.select(Ticket.service_id, func.count())
        .where(Ticket.status.in_(IN_PROGRESS))
        .group_by(Ticket.service_id)
    ).all()
    by_service = {sid: n for sid, n in rows}
    counts = {s.id: by_service.get(s.id, 0) for s in services}

    # Claim log: everything picked up today (Philippine time), newest first.
    start_of_day = datetime.now(PH_TIME).replace(hour=0, minute=0, second=0, microsecond=0)
    claimed_rows = db.session.scalars(
        db.select(Ticket)
        .where(Ticket.status == "claimed", Ticket.claimed_at >= start_of_day)
        .order_by(Ticket.claimed_at.desc())
    ).all()
    claimed_today = [describe(t) for t in claimed_rows]

    summary = {
        "orders": len(claimed_today),
        "kilos": round(sum(t["kilos"] for t in claimed_today), 1),
        "revenue": sum(t["total"] for t in claimed_today if t["paid"]),
        "unpaid": sum(t["total"] for t in claimed_today if not t["paid"]),
    }
    return render_template(
        "staff_dashboard.html", queue=queue, services=services, counts=counts,
        total_waiting=sum(counts.values()), selected=service_id, statuses=STATUSES,
        claimed_today=claimed_today, summary=summary,
    )

def back_to_staff(ticket_id=None):
    """After an action, return to the page the staff member came from."""
    if ticket_id and request.form.get("from") == "ticket":
        return redirect(url_for("ticket", ticket_id=ticket_id))
    return redirect(url_for("staff_dashboard",
                            service_id=request.form.get("service_id", type=int)))


@app.post("/staff/call-next")
def call_next():
    # Start the oldest ticket that is still only "received" (optionally for one service).
    service_id = request.form.get("service_id", type=int)
    stmt = (db.select(Ticket).where(Ticket.status == "received")
            .order_by(Ticket.created_at).limit(1))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    first = db.session.scalar(stmt)

    if first is None:
        flash("No one is waiting to be started.", "info")
    else:
        first.status = "washing"
        db.session.commit()
        flash(f"Ticket #{first.id} moved to washing.", "info")
    return back_to_staff()


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    if action not in ("advance", "cancel", "pay"):
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)

    if action == "pay":
        t.paid = True
        db.session.commit()
        flash(f"Ticket #{ticket_id} marked as paid.", "success")
    elif t.status in ("claimed", "left"):
        flash(f"Ticket #{ticket_id} is already closed.", "warning")
    elif action == "advance":
        t.status = STATUSES[STATUSES.index(t.status) + 1]
        if t.status == "ready":
            t.ready_at = func.now()      # the database fills in the time
        elif t.status == "claimed":
            t.claimed_at = func.now()
        db.session.commit()
        if t.status == "claimed":
            flash(f"Ticket #{ticket_id} claimed.", "success")
            if not t.paid:
                flash(f"Ticket #{ticket_id} was claimed but is still unpaid.", "warning")
        else:
            flash(f"Ticket #{ticket_id} moved to {t.status}.", "info")
    else:  # cancel: a soft delete, the row stays for reports
        t.status = "left"
        db.session.commit()
        flash(f"Ticket #{ticket_id} cancelled.", "info")
    return back_to_staff(ticket_id)


@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    # Hard delete: for a test ticket or one made by mistake. The row is gone for good.
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard"))

def parse_service_form(form):
    """Check the service fields. Returns (values, error message)."""
    name = " ".join(form.get("name", "").split())
    hours = form.get("hours", type=int)
    sort_order = form.get("sort_order", default=0, type=int)
    try:
        price = Decimal(form.get("price_per_kilo", "")).quantize(Decimal("0.01"))
    except InvalidOperation:
        price = None

    if not name or len(name) > 40:
        return None, "Enter a name of up to 40 characters."
    if price is None or not (Decimal("0") < price <= Decimal("9999")):
        return None, "Enter a price per kilo between 0.01 and 9999."
    if hours is None or not (1 <= hours <= 168):
        return None, "Enter a turnaround of 1 to 168 hours."
    if not (0 <= sort_order <= 999):
        return None, "Enter a position between 0 and 999."
    return {"name": name, "price_per_kilo": price,
            "hours": hours, "sort_order": sort_order}, None


@app.get("/staff/services")
def services_list():
    return render_template("services.html", services=all_services())


@app.post("/staff/services")
def service_create():
    values, error = parse_service_form(request.form)
    if error:
        flash(error, "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(**values))
    try:
        db.session.commit()
        flash(f"Service “{values['name']}” added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{values['name']}” already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/edit")
def service_edit(service_id):
    s = db.get_or_404(Service, service_id)
    values, error = parse_service_form(request.form)
    if error:
        flash(error, "danger")
        return redirect(url_for("services_list"))
    s.name = values["name"]
    s.price_per_kilo = values["price_per_kilo"]
    s.hours = values["hours"]
    s.sort_order = values["sort_order"]
    # An unticked checkbox is not sent at all.
    s.is_active = request.form.get("is_active") == "on"
    try:
        db.session.commit()
        flash(f"Service “{values['name']}” saved.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{values['name']}” already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.get_or_404(Service, service_id)
    if s.tickets:
        flash(f"“{s.name}” has tickets, so it cannot be deleted. Turn it off instead.", "danger")
        return redirect(url_for("services_list"))
    db.session.delete(s)
    db.session.commit()
    flash(f"Service “{s.name}” deleted.", "warning")
    return redirect(url_for("services_list"))

@app.get("/queue")
def queue_home():
    # The "Manage Queue" tab: open the oldest active ticket.
    first = db.session.scalar(
        db.select(Ticket)
        .where(Ticket.status.not_in(("claimed", "left")))
        .order_by(Ticket.created_at)
        .limit(1)
    )
    if first is None:
        flash("No active tickets to manage right now.", "info")
        return redirect(url_for("staff_dashboard"))
    return redirect(url_for("ticket", ticket_id=first.id))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # FR-02: all the details live here. An unknown number gives a 404 page.
    t = db.get_or_404(Ticket, ticket_id)
    return render_template("ticket.html", ticket=describe(t), statuses=STATUSES)
    
# ---------- Customer side ----------

def tickets_for_phone(phone):
    """All of one customer's tickets, newest first."""
    return db.session.scalars(
        db.select(Ticket).join(Customer)
        .where(Customer.phone == phone)
        .order_by(Ticket.created_at.desc())
    ).all()


def own_ticket(ticket_id, phone):
    """A ticket, only if it belongs to the mobile number this customer looked up."""
    if not phone:
        return None
    return db.session.scalar(
        db.select(Ticket).join(Customer)
        .where(Ticket.id == ticket_id, Customer.phone == phone)
    )


@app.route("/track")
def track():
    raw = request.args.get("phone", "").strip()

    if not raw:
        phone = session.get("phone")
        if request.args.get("back") and phone:
            mine = [public_view(t) for t in tickets_for_phone(phone)]
            return render_template("track.html", searched=True, error=None, tickets=mine)
        session.pop("phone", None)
        return render_template("track.html", searched=False, error=None, tickets=[])

    phone = normalize_phone(raw)
    if phone is None:
        return render_template(
            "track.html", searched=False, tickets=[],
            error="Please enter a valid mobile number, like 0917 123 4567.",
        )

    session["phone"] = phone
    mine = [public_view(t) for t in tickets_for_phone(phone)]
    return render_template("track.html", searched=True, error=None, tickets=mine)


@app.route("/track/<int:ticket_id>")
def track_ticket(ticket_id):
    # A customer can only open tickets tied to the number they entered.
    phone = session.get("phone")
    if not phone:
        return redirect(url_for("track"))
    t = own_ticket(ticket_id, phone)
    if t is None:
        abort(404)
    return render_template(
        "track_ticket.html", ticket=public_view(t), statuses=STATUSES
    )


@app.get("/track/<int:ticket_id>/status.json")
def track_ticket_status(ticket_id):
    # Same rule as the ticket page: only for a number this customer looked up.
    t = own_ticket(ticket_id, session.get("phone"))
    if t is None:
        abort(404)
    return {"status": t.status, "ahead": tickets_ahead(t)}

@app.post("/track/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    # Customer cancels their own ticket. Only works for a number they looked up.
    phone = session.get("phone")
    if not phone:
        return redirect(url_for("track"))
    t = own_ticket(ticket_id, phone)
    if t is None:
        abort(404)
    if t.status in IN_PROGRESS:
        t.status = "left"  # soft delete: the row stays for reports
        db.session.commit()
        flash(f"You left the queue. Ticket #{ticket_id} was cancelled.", "success")
    else:
        flash("This ticket can no longer be cancelled.", "warning")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)