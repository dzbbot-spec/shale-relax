import { useState } from 'react'
import NavBar from '../components/NavBar'
import type { Page } from '../App'

interface Props {
  navigate: (p: Page) => void
}

interface FormData {
  name: string
  check_in: string
  check_out: string
  guests: number
  contact: string
  comment: string
}

const API_URL = import.meta.env.VITE_API_URL || 'https://shale-relax-production.up.railway.app'

export default function Booking({ navigate }: Props) {
  const [form, setForm] = useState<FormData>({
    name: '',
    check_in: '',
    check_out: '',
    guests: 2,
    contact: '',
    comment: '',
  })
  const [status, setStatus] = useState<'idle' | 'sending' | 'success' | 'error'>('idle')
  const [errorMsg, setErrorMsg] = useState('')

  const set = (key: keyof FormData) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => setForm(f => ({ ...f, [key]: key === 'guests' ? Number(e.target.value) : e.target.value }))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.name || !form.check_in || !form.check_out || !form.contact) return
    setStatus('sending')
    try {
      const res = await fetch(`${API_URL}/api/booking`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      setStatus('success')
    } catch (err) {
      setErrorMsg('Не удалось отправить. Свяжитесь с нами напрямую.')
      setStatus('error')
    }
  }

  if (status === 'success') {
    return (
      <div
        style={{ minHeight: '100dvh', backgroundColor: 'var(--color-beige)' }}
        className="flex flex-col items-center justify-center p-8 text-center"
      >
        <div style={{ fontSize: 64 }}>✅</div>
        <h1 className="font-bold mt-4 mb-2" style={{ color: 'var(--color-green)', fontSize: 24 }}>
          Заявка принята!
        </h1>
        <p style={{ color: '#555', fontSize: 15, lineHeight: 1.6, marginBottom: 8 }}>
          Свяжемся с вами в ближайшее время для подтверждения бронирования.
        </p>
        <p style={{ color: '#777', fontSize: 13 }}>
          Вопросы: <strong>@shalerelax</strong>
        </p>
        <button
          onClick={() => navigate('home')}
          className="mt-8 px-8 py-3 rounded-2xl font-semibold text-white transition-opacity active:opacity-80"
          style={{ backgroundColor: 'var(--color-green)' }}
        >
          На главную
        </button>
      </div>
    )
  }

  const inputStyle: React.CSSProperties = {
    width: '100%',
    padding: '12px 14px',
    borderRadius: 12,
    border: '1.5px solid #e0dbd0',
    backgroundColor: 'white',
    fontSize: 15,
    color: 'var(--color-green)',
    outline: 'none',
  }

  const labelStyle: React.CSSProperties = {
    display: 'block',
    marginBottom: 6,
    fontSize: 13,
    fontWeight: 600,
    color: 'var(--color-green)',
  }

  const today = new Date().toISOString().split('T')[0]

  return (
    <div style={{ minHeight: '100dvh', backgroundColor: 'var(--color-beige)' }}>
      <div className="p-5 pt-4 pb-2">
        <h1 className="font-bold" style={{ color: 'var(--color-green)', fontSize: 26 }}>
          Бронирование
        </h1>
        <p className="mt-1" style={{ color: '#555', fontSize: 14 }}>
          Заполните форму — свяжемся в течение часа
        </p>
      </div>

      <form onSubmit={handleSubmit} className="px-5 pb-8">
        {/* Имя */}
        <div className="mb-4">
          <label style={labelStyle}>Ваше имя *</label>
          <input
            type="text"
            placeholder="Как вас зовут?"
            value={form.name}
            onChange={set('name')}
            required
            style={inputStyle}
          />
        </div>

        {/* Даты */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div>
            <label style={labelStyle}>Дата заезда *</label>
            <input
              type="date"
              value={form.check_in}
              min={today}
              onChange={set('check_in')}
              required
              style={inputStyle}
            />
          </div>
          <div>
            <label style={labelStyle}>Дата выезда *</label>
            <input
              type="date"
              value={form.check_out}
              min={form.check_in || today}
              onChange={set('check_out')}
              required
              style={inputStyle}
            />
          </div>
        </div>

        {/* Гости */}
        <div className="mb-4">
          <label style={labelStyle}>Количество гостей *</label>
          <select
            value={form.guests}
            onChange={set('guests')}
            style={inputStyle}
          >
            {[1, 2, 3, 4, 5, 6].map(n => (
              <option key={n} value={n}>
                {n} {n === 1 ? 'гость' : n < 5 ? 'гостя' : 'гостей'}
              </option>
            ))}
          </select>
        </div>

        {/* Контакт */}
        <div className="mb-4">
          <label style={labelStyle}>Телефон или @username *</label>
          <input
            type="text"
            placeholder="+7 900 000-00-00 или @username"
            value={form.contact}
            onChange={set('contact')}
            required
            style={inputStyle}
          />
        </div>

        {/* Комментарий */}
        <div className="mb-5">
          <label style={labelStyle}>Комментарий</label>
          <textarea
            placeholder="Пожелания, вопросы..."
            value={form.comment}
            onChange={set('comment')}
            rows={3}
            style={{ ...inputStyle, resize: 'none' }}
          />
        </div>

        {/* Расчёт стоимости */}
        {(() => {
          if (!form.check_in || !form.check_out) return null
          const nights = Math.max(0, Math.round(
            (new Date(form.check_out).getTime() - new Date(form.check_in).getTime()) / 86400000
          ))
          if (nights <= 0) return null
          return (
            <div
              className="p-4 rounded-xl mb-4"
              style={{ backgroundColor: 'rgba(26,58,42,0.08)' }}
            >
              <div className="flex justify-between" style={{ fontSize: 14, color: '#555' }}>
                <span>{nights} {nights === 1 ? 'ночь' : nights < 5 ? 'ночи' : 'ночей'} × 15 000 ₽</span>
                <span className="font-bold" style={{ color: 'var(--color-green)' }}>
                  {(nights * 15000).toLocaleString('ru')} ₽
                </span>
              </div>
            </div>
          )
        })()}

        {status === 'error' && (
          <div
            className="p-3 rounded-xl mb-4 text-center"
            style={{ backgroundColor: '#fde8e8', color: '#c0392b', fontSize: 13 }}
          >
            {errorMsg}
          </div>
        )}

        <button
          type="submit"
          disabled={status === 'sending'}
          className="w-full py-4 rounded-2xl font-semibold text-white text-base transition-opacity active:opacity-80"
          style={{
            backgroundColor: status === 'sending' ? '#888' : 'var(--color-green)',
            cursor: status === 'sending' ? 'not-allowed' : 'pointer',
          }}
        >
          {status === 'sending' ? 'Отправляем...' : 'Отправить заявку'}
        </button>
      </form>

      <div style={{ height: 80 }} />
      <NavBar current="booking" navigate={navigate} />
    </div>
  )
}
