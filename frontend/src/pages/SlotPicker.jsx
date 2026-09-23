import { useEffect, useMemo, useState } from 'react'

import { api } from '../api/client.js'

// รองรับ FR-BKG-01, FR-BKG-06
export default function SlotPicker() {
  const today = useMemo(() => new Date().toISOString().slice(0, 10), [])
  const [packageCode, setPackageCode] = useState('STD')
  const [dateFrom, setDateFrom] = useState(today)
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let ignore = false

    async function loadSlots() {
      setLoading(true)
      setError('')

      try {
        const response = await api.getSlots({ dateFrom, packageCode })
        const nextSlots = Array.isArray(response?.slots) ? response.slots : []

        if (!ignore) {
          setSlots(nextSlots)
        }
      } catch (err) {
        if (!ignore) {
          setError('ไม่สามารถโหลดช่วงเวลาว่างได้ในขณะนี้')
          setSlots([])
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadSlots()

    return () => {
      ignore = true
    }
  }, [dateFrom, packageCode])

  return (
    <section className="space-y-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div>
        <p className="text-sm font-medium uppercase tracking-wide text-teal-700">เลือกแพ็กเกจ</p>
        <div className="mt-3 flex gap-3">
          {['STD', 'PLUS', 'VIP'].map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => setPackageCode(item)}
              className={[
                'rounded-full border px-4 py-2 text-sm font-semibold transition',
                item === packageCode
                  ? 'border-teal-600 bg-teal-600 text-white'
                  : 'border-slate-300 bg-white text-slate-700 hover:border-teal-400',
              ].join(' ')}
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label htmlFor="slot-date" className="block text-sm font-medium text-slate-700">
          เลือกวันที่
        </label>
        <input
          id="slot-date"
          type="date"
          value={dateFrom}
          onChange={(event) => setDateFrom(event.target.value)}
          className="mt-2 w-full rounded-xl border border-slate-300 px-3 py-2 text-slate-800 focus:border-teal-500 focus:outline-none"
        />
      </div>

      <div>
        <h2 className="text-lg font-bold text-slate-800">ช่วงเวลาว่าง</h2>

        {loading && <p className="mt-3 text-sm text-slate-500">กำลังโหลดช่วงเวลาว่าง...</p>}
        {error && <p className="mt-3 text-sm text-red-600">{error}</p>}

        {!loading && !error && slots.length === 0 && (
          <p className="mt-3 text-sm text-slate-500">ไม่มีช่วงเวลาว่างสำหรับแพ็กเกจนี้ในวันที่เลือก</p>
        )}

        {!loading && !error && slots.length > 0 && (
          <ul className="mt-4 space-y-3">
            {slots.map((slot) => (
              <li
                key={`${slot.slot_date}-${slot.start_time}-${slot.package_code}`}
                className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 p-3"
              >
                <div>
                  <p className="font-semibold text-slate-800">{slot.slot_date}</p>
                  <p className="text-sm text-slate-600">{slot.start_time}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-slate-500">ที่นั่งคงเหลือ</p>
                  <p className="text-xl font-bold text-teal-700">{slot.remaining}</p>
                </div>
                <button
                  type="button"
                  className="rounded-lg bg-teal-600 px-3 py-2 text-sm font-semibold text-white hover:bg-teal-700"
                >
                  เลือก
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  )
}
