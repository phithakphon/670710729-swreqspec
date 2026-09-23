from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Time, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Slot(Base):
    """รองรับ CON-TECH-01, FR-BKG-01, FR-BKG-06"""

    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    package_code = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    remaining = Column(Integer, nullable=False)


class Booking(Base):
    """รองรับ FR-BKG-02, FR-BKG-04, IF-HIS-01"""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    hn = Column(String(20), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    booking_date = Column(Date, nullable=False)
    queue_no = Column(String(20), nullable=True)
    status = Column(String(20), nullable=False, default="booked")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class AuditLog(Base):
    """รองรับ DOM-PDPA-01"""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    hn = Column(String(20), nullable=False, index=True)
    accessed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
