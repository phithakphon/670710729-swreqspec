import { render, screen, waitFor } from '@testing-library/react'
import SlotPicker from '../pages/SlotPicker.jsx'

const mockGetSlots = vi.fn()

vi.mock('../api/client.js', () => ({
  api: { getSlots: (...args) => mockGetSlots(...args) },
}))

describe('T-09 SlotPicker', () => {
  beforeEach(() => {
    mockGetSlots.mockResolvedValue({
      slots: [
        { slot_date: '2026-09-23', start_time: '09:00:00', package_code: 'STD', remaining: 4 },
        { slot_date: '2026-09-23', start_time: '10:00:00', package_code: 'STD', remaining: 2 },
      ],
    })
  })

  test('แสดงแพ็กเกจและช่วงเวลาว่างพร้อมจำนวนที่นั่งคงเหลือ', async () => {
    render(<SlotPicker />)

    await waitFor(() => {
      expect(screen.getByText('ช่วงเวลาว่าง')).toBeTruthy()
      expect(screen.getAllByText('ที่นั่งคงเหลือ').length).toBeGreaterThan(0)
      expect(screen.getByText('4')).toBeTruthy()
      expect(screen.getByText('2')).toBeTruthy()
    })

    expect(mockGetSlots).toHaveBeenCalled()
  })
})
