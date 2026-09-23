from sqlalchemy import create_engine, inspect

from app.db.models import AuditLog, Base, Booking, Slot


def test_task_T_01_schema_and_migration_contract():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)

    assert "slots" in inspector.get_table_names()
    assert "bookings" in inspector.get_table_names()
    assert "audit_logs" in inspector.get_table_names()

    bookings_columns = [col["name"] for col in inspector.get_columns("bookings")]
    assert "hn" in bookings_columns
    assert "national_id" not in bookings_columns
    assert "slot_id" in bookings_columns

    slot = Slot(slot_date="2026-09-23", start_time="09:00:00", package_code="STD", capacity=10, remaining=10)
    booking = Booking(hn="HN-1001", slot_id=1, booking_date="2026-09-23", status="booked")
    audit_log = AuditLog(actor_id="staff-01", action="VIEW_BOOKING", hn="HN-1001")

    assert slot.package_code == "STD"
    assert booking.hn == "HN-1001"
    assert audit_log.actor_id == "staff-01"
