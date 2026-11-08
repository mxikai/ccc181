from datetime import datetime
from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean, CheckConstraint, DateTime, ForeignKey, Numeric, String, func, text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Customer(db.Model):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    phone: Mapped[str] = mapped_column(String(11), unique=True)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="customer")

    __table_args__ = (
        CheckConstraint("phone ~ '^09[0-9]{9}$'", name="ck_customers_phone"),
    )


class Staff(db.Model):
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="creator")


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True)
    price_per_kilo: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    hours: Mapped[int]
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true")
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")

    __table_args__ = (
        CheckConstraint("price_per_kilo > 0", name="ck_services_price"),
        CheckConstraint("hours > 0", name="ck_services_hours"),
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="RESTRICT")
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT")
    )
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("staff.id", ondelete="SET NULL")
    )
    kilos: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    price_per_kilo: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    notes: Mapped[str] = mapped_column(String(200), default="", server_default="")
    paid: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )
    status: Mapped[str] = mapped_column(
        String(20), default="received", server_default="received"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    customer: Mapped["Customer"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")
    creator: Mapped["Staff | None"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('received', 'washing', 'drying', 'folding', "
            "'ready', 'claimed', 'left')",
            name="ck_tickets_status",
        ),
        CheckConstraint("kilos >= 0.1 AND kilos <= 50", name="ck_tickets_kilos"),
        CheckConstraint("price_per_kilo > 0", name="ck_tickets_price"),
        CheckConstraint(
            "status <> 'claimed' OR claimed_at IS NOT NULL",
            name="ck_tickets_claimed_has_time",
        ),
        CheckConstraint(
            "status NOT IN ('ready', 'claimed') OR ready_at IS NOT NULL",
            name="ck_tickets_ready_has_time",
        ),
        CheckConstraint(
            "claimed_at IS NULL OR claimed_at >= created_at",
            name="ck_tickets_claimed_after_created",
        ),
    )