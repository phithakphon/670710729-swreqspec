# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:31 | test: 8 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 (ตรวจเฉพาะเวลา ไม่ตรวจรายการช่วงว่าง/30 วัน/จำนวนที่นั่ง) | T-02 เสร็จ; T-10 พร้อมทำ | `backend/app/slots/router.py:get_slots`; `backend/app/slots/service.py:list_available_slots` (`DAYS_AHEAD=14`) | `test_AC_BKG_05` ผ่าน แต่เรียกตามลำดับ ไม่จำลองผู้ใช้พร้อมกัน และไม่ assert ผลรายการช่วงเวลา | ช่องโหว่ (F-05, F-07) |
| FR-BKG-02 | AC-BKG-02 | T-04 พร้อมทำ | ยังไม่มีการตรวจคิวซ้ำใน `backend/app/booking/service.py:create_booking` | ไม่มี | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 พร้อมทำ | `backend/app/booking/router.py:create_booking` คืน 409 เมื่อเต็ม แต่ไม่มีช่วงเวลาแนะนำหรือหน้าจอแสดงตัวเลือก | ไม่มี | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01; AC-BKG-04 | T-03 เสร็จ; T-06 รอ Q-02; T-07 พร้อมทำ | `backend/app/booking/service.py:create_booking`, `next_queue_no`; `backend/app/booking/router.py:create_booking` | `test_AC_BKG_01` ผ่านแต่ตรวจเพียง 201; `test_TC_BKG_01_1_booking_success` ผ่าน (ตรวจการบันทึกและ remaining); `test_TC_BKG_01_2_full_slot_conflict` ผ่าน; `test_TC_BKG_01_3_unverified_user_blocked` ผ่าน; ไม่มี test หน้าจอแสดงคิว | ช่องโหว่ (F-04) |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ; T-06 รอ Q-02 | ไม่พบคิวส่งข้อความหรือหน้าจอผลการจอง | ไม่มี | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC ที่ตรวจการเปลี่ยนแพ็กเกจ | T-02 เสร็จ; T-10 พร้อมทำ | `backend/app/slots/service.py:list_available_slots` กรองด้วย `package_code`; ไม่มีหน้าจอเปลี่ยนแพ็กเกจ | ไม่มี test สำหรับ FR-BKG-06 | ช่องโหว่ (F-08) |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | `backend/app/slots/router.py:get_slots` | `test_AC_BKG_05` ผ่าน; วัด p95 จาก 200 คำขอเรียงลำดับ ไม่ได้ทดสอบผู้ใช้พร้อมกัน 200 คน | ช่องโหว่ (F-06) |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task ที่ระบุ TLS | ไม่พบการตั้งค่า TLS ใน `backend/app/` หรือ `frontend/src/` | ไม่มี | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | ไม่พบกลไกส่งซ้ำ | ไม่มี | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task ทดสอบผู้ใช้ใหม่ | ไม่พบการทดสอบกับผู้ใช้ 10 คน/เกณฑ์ 8 ใน 10 คน | ไม่มี | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 เสร็จ | `backend/app/config.py:DATABASE_URL`; `backend/app/db/session.py:engine`; `backend/app/db/models.py` | `test_T01_tables_created`, `test_T01_no_national_id` ผ่านบน SQLite; ไม่มี test ยืนยัน PostgreSQL | ช่องโหว่ (F-09) |
| DOM-PDPA-01 | AC-BKG-06 | T-01 เสร็จ (มีตาราง); T-08 พร้อมทำ | `backend/app/db/models.py:AuditLog`; ไม่พบ middleware/การเขียน audit log | ไม่มี `test_AC_BKG_06`; test T-01 ตรวจเพียงการสร้างตาราง | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC เฉพาะ (ตรวจร่วมกับ AC-BKG-01) | T-03 เสร็จ | `backend/app/auth/idp.py:get_verified_hn` | `test_TC_BKG_01_3_unverified_user_blocked` ผ่านเมื่อไม่มี header; ไม่ทดสอบการตรวจ token กับ IdP จริง | ช่องโหว่ (F-02) |
| IF-HIS-01 | ไม่มี AC เฉพาะ | T-01 เสร็จ; T-09 พร้อมทำ | `backend/app/db/models.py:Booking` ไม่มีคอลัมน์ national_id; แต่ `backend/app/booking/router.py:BookingRequest` รับ national_id และ `create_booking` เขียนลง log; ไม่พบ HIS client/lookup endpoint | `test_T01_no_national_id` ผ่านเฉพาะการตรวจ schema | ช่องโหว่ (F-01) |
| IF-NOT-01 | AC-BKG-04 | T-07 พร้อมทำ | ไม่พบการส่งคำขอแจ้งเตือนแบบ asynchronous | ไม่มี | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/main.py:lifespan`, `include_router` | T-01, T-02, T-03; CON-TECH-01 | บางส่วน | สร้างตารางและรวม router; ไม่มี audit middleware, HIS หรือ notification components ตามงานที่ยังไม่ทำ |
| `backend/app/config.py:DATABASE_URL`, `backend/app/db/session.py:engine`, `get_db` | CON-TECH-01 | ยังยืนยันไม่ได้ | ใช้ `DATABASE_URL` ได้ แต่ค่าเริ่มต้นเป็น SQLite และ test ทั้งหมดใช้ SQLite; ไม่มีการยืนยันการเชื่อม PostgreSQL |
| `backend/app/db/models.py:Slot`, `Booking`, `AuditLog`; `backend/app/db/migrations/001_init.py:upgrade` | FR-BKG-01, FR-BKG-02, FR-BKG-04, FR-BKG-06, CON-TECH-01, DOM-PDPA-01, IF-HIS-01 | บางส่วน | ตารางรองรับการจองและ audit log; ไม่มี national_id column; schema ยังไม่ได้บังคับ PostgreSQL และ AuditLog ยังไม่มีการบันทึกผ่าน middleware |
| `backend/app/slots/router.py:GET /slots` | FR-BKG-01, FR-BKG-06 | ไม่ครบ | ส่งรายการที่นั่งคงเหลือและรับ package_code; ช่วงวันที่จริงจำกัด 14 วัน |
| `backend/app/slots/service.py:list_available_slots` | FR-BKG-01, FR-BKG-06 | ไม่ตรงทั้งหมด | กรองแพ็กเกจ/ช่วงที่ยังว่างถูกต้อง แต่ `DAYS_AHEAD=14` ไม่ใช่ 30 วัน |
| `backend/app/booking/router.py:POST /bookings` | FR-BKG-02, FR-BKG-03, FR-BKG-04, IF-IDP-01, IF-HIS-01 | ไม่ครบ | สร้าง booking และแปลงช่วงเต็มเป็น 409; ยังไม่มีตรวจจองซ้ำ/ช่วงแนะนำ/การแจ้งเตือน; รับ national_id ที่ไม่จำเป็นและ log ค่านั้น |
| `backend/app/booking/service.py:create_booking` | FR-BKG-04 | บางส่วน | ตรวจที่นั่งว่าง ตัดที่นั่ง และบันทึก booking; การส่งแจ้งเตือนยังไม่มี |
| `backend/app/booking/service.py:next_queue_no` | FR-BKG-04 | ไม่ตรง/ยังรอคำตอบ | กำหนดรูปแบบ A001 และรีเซ็ตรายวัน ทั้งที่ยังรอ Q-02 |
| `backend/app/auth/idp.py:get_verified_hn` | IF-IDP-01 | ไม่ครบ | ตรวจเพียง prefix ของ Authorization แล้วใช้ส่วนที่เหลือเป็น HN; ไม่มีการยืนยันผลกับระบบ IdP |
| `frontend/src/api/client.js:api.getSlots`, `api.createBooking` | FR-BKG-01, FR-BKG-03, FR-BKG-04 | บางส่วน | มี client เรียก API; ไม่มีหน้า/การแสดงข้อมูลจองจริงใน `App.jsx` |
| `frontend/src/App.jsx:App` | ไม่มี AC โดยตรง | โครงเริ่มต้นเท่านั้น | แสดงข้อความ placeholder; ยังไม่มี SlotPicker, ConfirmBooking หรือ BookingResult |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง  
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ละเมิด Constraint | `backend/app/booking/router.py:BookingRequest`, `create_booking` | IF-HIS-01 | `POST /bookings` รับ national_id และเขียนค่าลง application log ทั้งที่ไม่ใช้; ยังไม่มี HIS lookup ที่ส่งเลขบัตรไปค้น HN ตาม interface ที่กำหนด | |
| F-02 | ละเมิด Constraint | `backend/app/auth/idp.py:get_verified_hn` | IF-IDP-01 | ยอมรับ Authorization จากการตรวจ prefix แล้วตีความ suffix เป็น HN โดยไม่ตรวจผลยืนยันตัวตนจากระบบ IdP; test ปัจจุบันตรวจเพียงกรณีไม่มี header | |
| F-04 | เดา Q-02 | `backend/app/booking/service.py:next_queue_no` | Q-02 | กำหนดเลขคิวเป็น A001 และเริ่มนับใหม่ทุกวัน โดยนำตัวอย่างในวงเล็บของ Q-02 มาใช้ก่อนทีมตอบ | |
| F-05 | ตัวเลขไม่ตรง spec | `backend/app/slots/service.py:DAYS_AHEAD` | FR-BKG-01 | จำกัดช่วงค้นหา 14 วัน ขณะที่ spec กำหนดให้แสดงภายใน 30 วันข้างหน้า | |
| F-06 | test อ่อน | `backend/tests/test_AC_BKG_05.py:test_AC_BKG_05` | NFR-PERF-01, AC-BKG-05 | วัด 200 requests แบบเรียงลำดับ ไม่ได้สร้างผู้ใช้พร้อมกัน 200 คนตาม Given จึงไม่ตรวจ p95 ภายใต้ concurrency ที่กำหนด | |
| F-07 | FR ไม่มี AC | `spec.md:FR-BKG-01`, AC-BKG-05 | FR-BKG-01 | AC-BKG-05 ตรวจเพียงเวลาตอบสนอง; ไม่มี AC ตรวจว่ารายการช่วงว่าง/จำนวนที่นั่งและขอบเขต 30 วันถูกแสดงถูกต้อง | |
| F-08 | FR ไม่มี AC | `spec.md:FR-BKG-06` | FR-BKG-06 | ไม่มี AC สำหรับการเปลี่ยนแพ็กเกจและคำนวณช่วงเวลาว่างใหม่; ระบุไว้ใน tasks.md ว่ายังไม่มี AC | |
| F-09 | test อ่อน | `backend/app/config.py:DATABASE_URL`, `backend/tests/test_T01_schema.py` | CON-TECH-01 | การทดสอบ schema ใช้ SQLite เท่านั้น และค่าเริ่มต้นแอปก็เป็น SQLite; ยังไม่มีหลักฐานทดสอบการทำงานกับ PostgreSQL หรือการกำหนดค่า PostgreSQL สำหรับระบบจริง | |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| F-03 | ตามคำตัดสินของทีม ลบ `DELETE /bookings/{booking_id}` และ `cancel_booking` ออกจากโค้ด เพราะการยกเลิกคิวอยู่ใน Out of scope (UC-02) | ตรวจ `backend/app/booking/router.py` และ `backend/app/booking/service.py` แล้วไม่พบ endpoint หรือฟังก์ชันดังกล่าว |
