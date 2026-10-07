# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH
from app.db.models import Booking, Slot


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


def test_TC_BKG_01_1_booking_success(client, db, make_slot):
    # Given ผู้รับบริการยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When ผู้รับบริการกดยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then บันทึกการจองสำเร็จ
    assert res.status_code == 201
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 1
    # Then แสดงหมายเลขคิว (รอ Q-02): ยังไม่ตรวจการแสดงหมายเลขคิว
    # Then ที่นั่งว่างของช่วงนั้นลดลงเป็น 0
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_2_full_slot_conflict(client, make_slot):
    # Given ผู้รับบริการยืนยันตัวตนแล้ว และช่วง 09.00 น. ไม่มีที่นั่งว่าง (เหลือ 0 ที่)
    slot = make_slot(start="09:00", remaining=0)

    # When ผู้รับบริการพยายามยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then ปฏิเสธการจองด้วย HTTP 409
    assert res.status_code == 409


def test_TC_BKG_01_3_unverified_user_blocked(client, db, make_slot):
    # Given ผู้รับบริการยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When ผู้รับบริการกดยืนยันการจองช่วง 09.00 น.
    res = client.post("/bookings", json={"slot_id": slot.id})

    # Then ปฏิเสธคำขอด้วย HTTP 401
    assert res.status_code == 401
    # Then ไม่บันทึกการจอง
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 0
    # Then ไม่แสดงหมายเลขคิว
    assert "queue_no" not in res.json()
    # Then ไม่ลดจำนวนที่นั่งของช่วงนั้น
    assert db.get(Slot, slot.id).remaining == 1
