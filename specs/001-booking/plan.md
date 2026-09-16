# แผนทางเทคนิค: จองคิวตรวจสุขภาพ (Booking)

## 1. สรุปแนวทาง
- ฟีเจอร์นี้จะให้ผู้รับบริการที่ยืนยันตัวตนแล้วเลือกแพ็กเกจ วัน และช่วงเวลาตรวจสุขภาพ แล้วได้รับหมายเลขคิวภายในกระบวนการจองที่ชัดเจน
- ผู้ใช้หลักคือผู้รับบริการที่ผ่านการยืนยันตัวตนแล้ว และระบบจะใช้ข้อมูล HN จาก HIS เพื่อยืนยันความสัมพันธ์กับผู้รับบริการโดยไม่เก็บเลขบัตรประชาชนในตารางการจอง
- แนวทางคือสร้างกระบวนการค้นหาช่วงว่างแบบอ่าน-คำนวณ-ยืนยัน ตาม FR-BKG-01 ถึง FR-BKG-06 พร้อมบันทึก audit log และจัดการการส่งข้อความยืนยันแบบ asynchronous
- สำหรับข้อที่ยังไม่ได้ชัดเจนใน spec จะคงให้เป็น Open Questions และไม่สร้างลอจิกเพิ่มเติมจนกว่าจะได้รับคำตอบจากทีม เช่น Q-01 และ Q-02
- เนื่องจาก spec อยู่ในสถานะ Draft v1 จึงจัดทำแผนนี้ตามความต้องการที่ระบุไว้ใน spec โดยไม่เพิ่มความต้องการใหม่

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| Frontend: React + Vite | ทีมเลือกเอง ไม่ได้มาจาก spec | สร้างหน้าเลือกแพ็กเกจ วัน และช่วงเวลาก่อนยืนยันการจอง |
| Backend: Python FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | จัดการ business flow ของการจองและคิวส่งข้อความ |
| Database: MySQL | CON-TECH-01 | ใช้เก็บข้อมูลการจอง, ช่วงเวลา, audit log และคิวส่งข้อความ |
| TLS 1.2+ สำหรับรับส่งข้อมูล | NFR-SEC-01 | ใช้ในสภาพแวดล้อม deployment และการสื่อสารระหว่าง client/server |
| ระบบแจ้งเตือน SMS/LINE แบบ asynchronous | IF-NOT-01 | การส่งข้อความยืนยันต้องไม่ทำให้การจองหยุดชะงัก |
| HIS integration via HN lookup | IF-HIS-01 | ใช้ HN เป็นข้อมูลอ้างอิงภายในระบบ ไม่เก็บเลขบัตรประชาชนในตารางการจอง |
| Identity verification integration | IF-IDP-01 | ใช้ผลยืนยันตัวตนเป็น precondition ก่อนเปิดใช้งานฟีเจอร์ |

## 3. โมเดลข้อมูล

| Entity | ฟิลด์หลัก | รองรับ FR / Constraint |
|---|---|---|
| Booking | booking_id, patient_hn, package_id, visit_date, slot_id, status, queue_number, created_at, confirmed_at | รองรับ FR-BKG-02, FR-BKG-04, FR-BKG-05 และ IF-HIS-01 |
| Package | package_id, name, description, valid_from, valid_to | รองรับ FR-BKG-01, FR-BKG-06 |
| Slot | slot_id, date, time_from, time_to, quota_total, quota_remaining, package_id | รองรับ FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-06 |
| QueueNumber | queue_id, date, sequence_no, prefix, issued_at | รองรับ FR-BKG-04 และ Q-02 (ยังรอคำตอบ) |
| NotificationMessage | notification_id, booking_id, channel, payload, status, retry_count, next_retry_at, created_at | รองรับ FR-BKG-05 และ IF-NOT-01 |
| AuditLog | audit_id, accessed_by, accessed_at, patient_hn, action, resource | รองรับ DOM-PDPA-01 และ AC-BKG-06 |
| IdentityVerificationResult | verification_id, patient_hn, verified_at, status | รองรับ IF-IDP-01 |

ข้อสำคัญ: ตาราง Booking จะเก็บ HN เป็นข้อมูลอ้างอิงภายในระบบ โดยไม่เก็บเลขบัตรประชาชนตาม IF-HIS-01 และจะไม่เก็บข้อมูลบัตรประชาชนในตารางใด ๆ ที่เกี่ยวกับการจอง

## 4. API / หน้าจอ

### หน้า/ส่วนประกอบหลัก
- หน้ารายการแพ็กเกจ: แสดงแพ็กเกจที่พร้อมให้เลือก; รองรับ FR-BKG-01, FR-BKG-06
- หน้ารายการวันและช่วงเวลา: แสดงวันภายใน 30 วันข้างหน้า พร้อมจำนวนที่นั่งคงเหลือ; รองรับ FR-BKG-01
- Modal ยืนยันการจอง: แสดงสรุปข้อมูลและปุ่มยืนยัน; รองรับ FR-BKG-04
- แจ้งเตือนช่วงเวลาเต็ม: แสดงข้อความ “ช่วงเวลาเต็ม” และแสดง 3 ตัวเลือกที่ใกล้เคียง; รองรับ FR-BKG-03
- หน้าผลการจอง: แสดงหมายเลขคิวและสถานะการส่งข้อความยืนยัน; รองรับ FR-BKG-04, FR-BKG-05

### API หลัก
- GET /api/booking/slots?patient_hn=&package_id=&from_date=&to_date=  
  Output: list of date + slot + quota_remaining; รองรับ FR-BKG-01, FR-BKG-06
- POST /api/booking/validate  
  Input: patient_hn, package_id, date, slot_id; Output: ok/blocked/recommendation; รองรับ FR-BKG-02, FR-BKG-03
- POST /api/booking/create  
  Input: patient_hn, package_id, date, slot_id; Output: booking_id, queue_number, booking_status; รองรับ FR-BKG-04
- POST /api/booking/notification/retry  
  Input: notification_id; Output: retry queued; รองรับ FR-BKG-05, NFR-REL-02
- GET /api/booking/audit  
  Input: patient_hn, access_by; Output: audit records; รองรับ DOM-PDPA-01, AC-BKG-06

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| CON-TECH-01 | ใช้ MySQL เป็นฐานข้อมูลหลักในโมเดลข้อมูลและ API architecture | ใช้แล้ว |
| DOM-PDPA-01 | AuditLog entity และ API /api/booking/audit; กำหนดบันทึกผู้เข้าถึงเวลาและ HN ใน log | ใช้แล้ว |
| IF-IDP-01 | IdentityVerificationResult และ precondition ในสรุปแนวทางและหน้า/ส่วนประกอบหลัก | ใช้แล้ว |
| IF-HIS-01 | Booking entity และ API validation ใช้ HN เป็นข้อมูลอ้างอิงภายในระบบ; ระบุไม่เก็บเลขบัตรประชาชน | ใช้แล้ว |
| IF-NOT-01 | NotificationMessage entity และ API /api/booking/create + /api/booking/notification/retry; การส่งข้อความเป็น asynchronous | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-BKG-01 | test_AC_BKG_01_success_booking_reduces_quota | ทดสอบกรณีช่วง 09.00 น. มีที่นั่ง 1 ที่ เมื่อยืนยันการจองแล้ว ต้องบันทึกการจอง แสดงหมายเลขคิว และ quota_remaining = 0 |
| AC-BKG-02 | test_AC_BKG_02_reject_duplicate_active_queue_same_day | ทดสอบกรณีผู้รับบริการมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ต้องปฏิเสธการจองใหม่และแสดงหมายเลขคิวเดิม |
| AC-BKG-03 | test_AC_BKG_03_show_full_slot_and_alternatives | ทดสอบกรณีช่วงเวลาถูกคนอื่นยืนยันก่อนแล้ว ต้องแสดง “ช่วงเวลาเต็ม” และเสนอช่วงเวลาใกล้เคียง 3 ตัวเลือก โดยไม่มีการจองซ้อน |
| AC-BKG-04 | test_AC_BKG_04_notification_failure_keeps_booking | ทดสอบกรณีระบบแจ้งเตือนไม่ตอบสนอง ต้องยังบันทึกการจองและมีรายการในคิวส่งซ้ำภายใน 5 นาที |
| AC-BKG-05 | test_AC_BKG_05_slot_search_p95_under_2s | ใช้ load test 200 concurrent users เพื่อวัด p95 ของเวลา response เมื่อค้นหาช่วงว่าง |
| AC-BKG-06 | test_AC_BKG_06_audit_log_written_on_access | ทดสอบการเข้าถึงข้อมูลการจองของผู้รับบริการแล้วต้องมี audit log ที่มีผู้เข้าถึง เวลา และ HN |

## 7. ลำดับงาน

1. ตั้งค่าโครงสร้างโปรเจกต์และ database schema สำหรับ Booking, Slot, NotificationMessage, AuditLog ตาม CON-TECH-01 และ IF-HIS-01 (FR-BKG-01, FR-BKG-04, DOM-PDPA-01)
2. สร้าง API สำหรับค้นหาช่วงเวลาว่างและจำนวนที่นั่งคงเหลือ ตาม FR-BKG-01 และ NFR-PERF-01
3. สร้างฟังก์ชันตรวจสิทธิ์และตรวจคิวซ้ำตาม FR-BKG-02 เพื่อปฏิเสธการจองที่ซ้ำในวันเดียวกัน
4. สร้างลอจิกยืนยันการจองและการลด quota พร้อมการสร้าง queue number ตาม FR-BKG-04 และ AC-BKG-01
5. สร้างลอจิก fallback เมื่อช่วงเวลาลงทะเบียนเต็ม: แจ้งเตือนและเสนอ 3 ตัวเลือกใกล้เคียง ตาม FR-BKG-03 และ AC-BKG-03
6. สร้างคิวส่งข้อความยืนยันแบบ asynchronous และฟังก์ชัน retry ภายใน 5 นาที ตาม FR-BKG-05 และ NFR-REL-02
7. สร้าง audit log และการเข้าถึงข้อมูลตาม DOM-PDPA-01 และ AC-BKG-06
8. ทดสอบครบตาม AC-BKG-01 ถึง AC-BKG-06 และตรวจความสอดคล้องกับ Open Questions ที่ยังค้างอยู่

## 8. สิ่งที่ยังไม่ทำ
- Q-01 และ Q-02 ได้รับคำตอบจากทีมแล้ว จึงไม่คงสถานะ Open Question ไว้ในแผนนี้
- ข้อผิดพลาดของระบบแจ้งเตือนจะถือเป็น “ไม่สำเร็จ” แบบใดบ้างยังไม่ชัดเจน จึงยังคงให้เป็นค่าใน scope ของ retry ตาม IF-NOT-01 และ FR-BKG-05 โดยไม่เพิ่มเงื่อนไขเพิ่มเติมจนกว่าจะได้รับคำตอบ

> หมายเหตุ: แผนนี้ถูกจัดทำตาม spec.md หลังการปรับปรุงจากคำตอบของทีมและยังคงให้ความสำคัญต่อข้อที่ยังกำกวมในเรื่อง retry ของระบบแจ้งเตือน
