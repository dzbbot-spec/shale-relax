import { useState } from 'react'
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

const labelStyle: React.CSSProperties = {
  display: 'block',
  fontSize: 11,
  fontWeight: 500,
  letterSpacing: 1.5,
  textTransform: 'uppercase' as const,
  color: '#999999',
  marginBottom: 8,
}

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

  const set = (key: keyof FormData) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => setForm(f => ({ ...f, [key]: e.target.value }))

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
      if (!res.ok) throw new Error()
      setStatus('success')
    } catch {
      setStatus('error')
    }
  }

  const nights = (() => {
    if (!form.check_in || !form.check_out) return 0
    return Math.max(0, Math.round(
      (new Date(form.check_out).getTime() - new Date(form.check_in).getTime()) / 86400000
    ))
  })()

  if (status === 'success') {
    return (
      <div style={{
        minHeight: '100dvh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '40px 24px',
        textAlign: 'center',
        backgroundColor: '#ffffff',
      }}>
        <div style={{
          width: 64,
          height: 64,
          borderRadius: 50,
          backgroundColor: '#111111',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: 24,
        }}>
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
        <h2 style={{ margin: '0 0 12px', fontSize: 24, fontWeight: 300, color: '#111111' }}>
          Заявка отправлена
        </h2>
        <p style={{ margin: '0 0 32px', fontSize: 14, fontWeight: 300, color: '#666666', lineHeight: 1.6 }}>
          Свяжемся с вами в ближайшее время
          для подтверждения бронирования.
        </p>
        <button
          onClick={() => navigate('home')}
          style={{
            padding: '14px 40px',
            borderRadius: 50,
            backgroundColor: '#111111',
            color: '#ffffff',
            fontSize: 14,
            fontWeight: 500,
          }}
        >
          На главную
        </button>
      </div>
    )
  }

  const today = new Date().toISOString().split('T')[0]

  return (
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff' }}>
      <div style={{ padding: '20px 24px 8px' }}>
        <h1 style={{ margin: 0, fontSize: 28, fontWeight: 300, color: '#111111', letterSpacing: '-0.5px' }}>
          Заявка
        </h1>
        <p style={{ margin: '4px 0 0', fontSize: 13, fontWeight: 300, color: '#999999' }}>
          Ответим в течение часа
        </p>
      </div>

      <form onSubmit={handleSubmit} style={{ padding: '20px 16px 32px' }}>
        {/* Имя */}
        <div style={{ marginBottom: 20 }}>
          <label style={labelStyle}>Имя</label>
          <input
            type="text"
            placeholder="Как вас зовут"
            value={form.name}
            onChange={set('name')}
            required
            className="booking-input"
          />
        </div>

        {/* Даты */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 20 }}>
          <div>
            <label style={labelStyle}>Заезд</label>
            <input
              type="date"
              value={form.check_in}
              min={today}
              onChange={set('check_in')}
              required
              className="booking-input"
            />
          </div>
          <div>
            <label style={labelStyle}>Выезд</label>
            <input
              type="date"
              value={form.check_out}
              min={form.check_in || today}
              onChange={set('check_out')}
              required
              className="booking-input"
            />
          </div>
        </div>

        {/* Гости — счётчик */}
        <div style={{ marginBottom: 20 }}>
          <label style={labelStyle}>Гостей</label>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <button
              type="button"
              onClick={() => setForm(f => ({ ...f, guests: Math.max(1, f.guests - 1) }))}
              style={{
                width: 44,
                height: 44,
                borderRadius: 50,
                border: '1.5px solid #e8e8e8',
                fontSize: 20,
                color: '#111111',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              −
            </button>
            <span style={{ fontSize: 20, fontWeight: 400, minWidth: 24, textAlign: 'center', color: '#111111' }}>
              {form.guests}
            </span>
            <button
              type="button"
              onClick={() => setForm(f => ({ ...f, guests: Math.min(6, f.guests + 1) }))}
              style={{
                width: 44,
                height: 44,
                borderRadius: 50,
                border: '1.5px solid #e8e8e8',
                fontSize: 20,
                color: '#111111',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              +
            </button>
            <span style={{ fontSize: 13, color: '#999999', fontWeight: 300 }}>
              из 6 максимум
            </span>
          </div>
        </div>

        {/* Контакт */}
        <div style={{ marginBottom: 20 }}>
          <label style={labelStyle}>Контакт</label>
          <input
            type="text"
            placeholder="+7 900 000-00-00 или @username"
            value={form.contact}
            onChange={set('contact')}
            required
            className="booking-input"
          />
        </div>

        {/* Комментарий */}
        <div style={{ marginBottom: 24 }}>
          <label style={labelStyle}>Комментарий</label>
          <textarea
            placeholder="Пожелания или вопросы"
            value={form.comment}
            onChange={set('comment')}
            rows={3}
            className="booking-input"
            style={{ resize: 'none' }}
          />
        </div>

        {/* Итог */}
        {nights > 0 && (
          <div style={{
            padding: '16px 20px',
            borderRadius: 16,
            backgroundColor: '#f5f5f5',
            marginBottom: 20,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
            <span style={{ fontSize: 13, color: '#666666', fontWeight: 300 }}>
              {nights} {nights === 1 ? 'ночь' : nights < 5 ? 'ночи' : 'ночей'} × 15 000 ₽
            </span>
            <span style={{ fontSize: 18, fontWeight: 500, color: '#111111' }}>
              {(nights * 15000).toLocaleString('ru')} ₽
            </span>
          </div>
        )}

        {status === 'error' && (
          <div style={{
            padding: '12px 16px',
            borderRadius: 12,
            backgroundColor: '#fff0f0',
            color: '#cc0000',
            fontSize: 13,
            marginBottom: 16,
          }}>
            Не удалось отправить. Напишите напрямую в @shalerelax
          </div>
        )}

        <button
          type="submit"
          disabled={status === 'sending'}
          style={{
            width: '100%',
            padding: '16px 0',
            borderRadius: 50,
            backgroundColor: status === 'sending' ? '#888888' : '#111111',
            color: '#ffffff',
            fontSize: 15,
            fontWeight: 500,
            letterSpacing: 0.3,
          }}
        >
          {status === 'sending' ? 'Отправляем...' : 'Отправить заявку'}
        </button>
      </form>
    </div>
  )
}
