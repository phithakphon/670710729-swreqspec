# Tasks: จองคิวตรวจสุขภาพ (Booking)
Feature: จองคิวตรวจสุขภาพ (Booking)
Spec ID: SPEC-BKG-001
อ้างอิง plan.md: specs/001-booking/plan.md
วันที่: 2569-09-23

สรุป:
- มี 12 task ที่ต้องทำเพื่อให้ฟีเจอร์นี้เสร็จตาม spec และ plan
- มี 2 task ที่ต้องรอ Open Question Q-02 (รูปแบบและวิธีออกหมายเลขคิว)

### T-01 สร้าง schema และ migration ฐานข้อมูล
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง slots, bookings และ audit_logs ได้ตามสเปก และ bookings ไม่มีคอลัมน์ national_id
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้าง API ค้นช่วงเวลาว่างและคำนวณที่นั่งคงเหลือ
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/config.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: GET /slots คืนรายการช่วงเวลา 30 วันข้างหน้า พร้อมที่นั่งคงเหลือ และ test_AC_BKG_05 ผ่านตามเกณฑ์ p95
- สถานะ: พร้อมทำ

### T-03 สร้าง API จองคิวพื้นฐานและเก็บคิวชั่วคราว
- รองรับ: FR-BKG-04, IF-HIS-01, IF-IDP-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: POST /bookings บันทึกการจองได้และคืน queue_no placeholder พร้อมข้อมูล booking ที่จำเป็นตามสเปก
- สถานะ: รอ Q-02

### T-04 ป้องกันจองซ้ำวันเดียวกัน
- รองรับ: FR-BKG-02, ASM-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/app/booking/service.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: test_AC_BKG_02 ผ่าน และระบบปฏิเสธการจองใหม่ในวันเดียวกัน พร้อมแสดงหมายเลขคิวเดิม
- สถานะ: พร้อมทำ

### T-05 จัดการช่วงเวลาที่เต็มและข้อเสนอ 3 ตัวเลือก
- รองรับ: FR-BKG-03, ASM-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/booking/service.py
- ต้องทำหลัง: T-02, T-04
- เสร็จเมื่อ: POST /bookings เมื่อช่วงเวลาเต็มคืน 409 พร้อม 3 ช่วงที่ใกล้ที่สุดในวันเดียวกันและวันถัดไป และไม่มีการจองซ้อน
- สถานะ: พร้อมทำ

### T-06 จัดการคิวส่งข้อความซ้ำและบันทึกการจองแม้ส่งไม่สำเร็จ
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ระบบคงบันทึกการจอง แม้ notify ล้ม และมีงานคิวส่งซ้ำที่กำหนดส่งภายใน 5 นาที
- สถานะ: พร้อมทำ

### T-07 เพิ่ม audit log middleware และตรวจสอบการเข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01, FR-BKG-04
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/audit/middleware.py, backend/app/main.py
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: ทุก request ที่เข้าถึงข้อมูลการจองสร้าง audit log พร้อม actor_id, accessed_at และ hn
- สถานะ: พร้อมทำ

### T-08 สร้าง lookup HIS และจัดการข้อมูลผู้รับบริการ
- รองรับ: IF-HIS-01, IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03
- ไฟล์ที่แตะ: backend/app/his/client.py, backend/app/booking/router.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: API lookup ใช้เลขบัตรเพียงส่งต่อ HIS แล้วเก็บเฉพาะ HN ในตาราง bookings
- สถานะ: พร้อมทำ

### T-09 สร้างหน้าเลือกแพ็กเกจและช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-12
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/App.jsx, frontend/src/api/client.js
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: ผู้ใช้เลือกแพ็กเกจและดูวันที่/ช่วงเวลาที่ว่าง พร้อมจำนวนที่นั่งคงเหลือได้อย่างถูกต้อง
- สถานะ: พร้อมทำ

### T-10 สร้างหน้้ายืนยันและแสดงข้อเสนอช่วงเต็ม
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-05, T-09
- เสร็จเมื่อ: UI รับ 409 จาก API แล้วแสดงข้อความ “ช่วงเวลาเต็ม” พร้อม 3 ตัวเลือกที่ใกล้ที่สุด
- สถานะ: พร้อมทำ

### T-11 สร้างหน้าแสดงผลการจองและหมายเลขคิว
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01, AC-BKG-04
- ไฟล์ที่แตะ: frontend/src/pages/BookingResult.jsx
- ต้องทำหลัง: T-03, T-06, T-09
- เสร็จเมื่อ: หน้าแสดงหมายเลขคิวและยังแสดงผลได้แม้ส่งข้อความไม่สำเร็จ
- สถานะ: รอ Q-02

### T-12 ต่อหน้าจอกับ API จริงและตรวจความสมบูรณ์
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-01, AC-BKG-03, AC-BKG-05
- ไฟล์ที่แตะ: frontend/src/api/client.js, frontend/src/App.jsx, frontend/src/pages/*
- ต้องทำหลัง: T-02, T-05, T-09, T-10, T-11
- เสร็จเมื่อ: UI เรียก API จริงครบ และตรวจสอบความถูกต้องของการทำงานของหน้าจอตาม AC ที่เกี่ยวข้อง
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ AC
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-03, T-11 |
| AC-BKG-02 | T-04 |
| AC-BKG-03 | T-05, T-10 |
| AC-BKG-04 | T-06, T-11 |
| AC-BKG-05 | T-02, T-12 |
| AC-BKG-06 | T-07 |

## ตารางตรวจความครบ Constraint
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01 |
| DOM-PDPA-01 | T-01, T-07 |
| IF-IDP-01 | T-03, T-08 |
| IF-HIS-01 | T-01, T-08 |
| IF-NOT-01 | T-06 |

## สิ่งที่ยังไม่ทำ
- Q-02: หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001)?
  -> ถามเจ้าหน้าที่เวชระเบียน (ยังไม่ได้คำตอบ)
  -> task ที่รออยู่: T-03, T-11
