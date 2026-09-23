import SlotPicker from './pages/SlotPicker.jsx'

// รองรับ FR-BKG-01, FR-BKG-06
export default function App() {
  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-bold text-teal-800">ระบบจองคิวตรวจสุขภาพ</h1>
      <div className="mt-6">
        <SlotPicker />
      </div>
    </main>
  )
}
