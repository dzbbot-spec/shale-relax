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

const API_URL = import.meta.env.VITE_API_URL || 'https://worker-production-8fd9.up.railway.app'

const labelStyle: React.CSSProperties = {
  display: 'block',
  fontSize: 11,
  fontWeight: 500,
  letterSpacing: 1.5,
  textTransform: 'uppercase' as const,
  color: '#999999',
  marginBottom: 6,
}

const onFocusScroll = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement>) => {
  setTimeout(() => e.target.scrollIntoView({ behavior: 'smooth', block: 'center' }), 300)
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
  const [pressed, setPressed] = useState<'minus' | 'plus' | null>(null)

  const pressBtn = (btn: 'minus' | 'plus') => {
    setPressed(btn)
    setTimeout(() => setPressed(null), 150)
  }

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
        padding: '40px 16px',
        textAlign: 'center',
        backgroundColor: '#ffffff',
      }}>
        <div style={{
          width: 56,
          height: 56,
          borderRadius: 12,
          backgroundColor: '#111111',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: 20,
        }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
        <h2 style={{ margin: '0 0 10px', fontSize: 20, fontWeight: 300, color: '#111111' }}>
          Заявка отправлена
        </h2>
        <p style={{ margin: '0 0 28px', fontSize: 13, fontWeight: 300, color: '#666666', lineHeight: 1.6 }}>
          Свяжемся с вами в ближайшее время для подтверждения бронирования.
        </p>
        <button
          onClick={() => navigate('home')}
          style={{
            padding: '12px 36px',
            borderRadius: 12,
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
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff', paddingBottom: 'env(safe-area-inset-bottom, 16px)' }}>
      <div style={{ padding: '16px 16px 8px' }}>
        <h1 style={{ margin: 0, fontSize: 20, fontWeight: 300, color: '#111111', letterSpacing: '-0.3px' }}>
          Заявка
        </h1>
        <p style={{ margin: '2px 0 0', fontSize: 12, fontWeight: 300, color: '#999999' }}>
          Ответим в течение часа
        </p>
      </div>

      <form onSubmit={handleSubmit} style={{ padding: '12px 16px 32px' }}>
        {/* Имя */}
        <div style={{ marginBottom: 14 }}>
          <label style={labelStyle}>Имя</label>
          <input
            type="text"
            placeholder="Как вас зовут"
            value={form.name}
            onChange={set('name')}
            onFocus={onFocusScroll}
            required
            className="booking-input"
          />
        </div>

        {/* Даты — стопкой */}
        <div style={{ marginBottom: 14 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            <div style={{ minWidth: 0 }}>
              <label style={labelStyle}>Заезд</label>
              <input
                type="date"
                value={form.check_in}
                min={today}
                onChange={set('check_in')}
                onFocus={onFocusScroll}
                required
                className="booking-input"
              />
            </div>
            <div style={{ minWidth: 0 }}>
              <label style={labelStyle}>Выезд</label>
              <input
                type="date"
                value={form.check_out}
                min={form.check_in || today}
                onChange={set('check_out')}
                onFocus={onFocusScroll}
                required
                className="booking-input"
              />
            </div>
          </div>
        </div>

        {/* Гости */}
        <div style={{ marginBottom: 14 }}>
          <label style={labelStyle}>Гостей</label>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <button
              type="button"
              onPointerDown={() => pressBtn('minus')}
              onClick={() => setForm(f => ({ ...f, guests: Math.max(1, f.guests - 1) }))}
              style={{
                width: 36,
                height: 36,
                borderRadius: 10,
                border: '1.5px solid #e0e0e0',
                fontSize: 18,
                color: pressed === 'minus' ? '#ffffff' : '#111111',
                backgroundColor: pressed === 'minus' ? '#111111' : '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'background-color 0.1s, color 0.1s',
                flexShrink: 0,
              }}
            >−</button>
            <span style={{ fontSize: 18, fontWeight: 400, minWidth: 20, textAlign: 'center', color: '#111111' }}>
              {form.guests}
            </span>
            <button
              type="button"
              onPointerDown={() => pressBtn('plus')}
              onClick={() => setForm(f => ({ ...f, guests: Math.min(6, f.guests + 1) }))}
              style={{
                width: 36,
                height: 36,
                borderRadius: 10,
                border: '1.5px solid #e0e0e0',
                fontSize: 18,
                color: pressed === 'plus' ? '#ffffff' : '#111111',
                backgroundColor: pressed === 'plus' ? '#111111' : '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'background-color 0.1s, color 0.1s',
                flexShrink: 0,
              }}
            >+</button>
            <span style={{ fontSize: 12, color: '#999999', fontWeight: 300 }}>из 6 макс.</span>
          </div>
        </div>

        {/* Контакт */}
        <div style={{ marginBottom: 14 }}>
          <label style={labelStyle}>Контакт</label>
          <input
            type="text"
            placeholder="+7 900 000-00-00 или @username"
            value={form.contact}
            onChange={set('contact')}
            onFocus={onFocusScroll}
            required
            className="booking-input"
          />
        </div>

        {/* Комментарий */}
        <div style={{ marginBottom: 20 }}>
          <label style={labelStyle}>Комментарий</label>
          <textarea
            placeholder="Пожелания или вопросы"
            value={form.comment}
            onChange={set('comment')}
            onFocus={onFocusScroll}
            rows={3}
            className="booking-input"
            style={{ resize: 'none', height: 'auto' }}
          />
        </div>

        {/* Итог */}
        {nights > 0 && (
          <div style={{
            padding: '12px 16px',
            borderRadius: 12,
            backgroundColor: '#f5f5f5',
            marginBottom: 16,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
            <span style={{ fontSize: 13, color: '#666666', fontWeight: 300 }}>
              {nights} {nights === 1 ? 'ночь' : nights < 5 ? 'ночи' : 'ночей'} × 15 000 ₽
            </span>
            <span style={{ fontSize: 16, fontWeight: 500, color: '#111111' }}>
              {(nights * 15000).toLocaleString('ru')} ₽
            </span>
          </div>
        )}

        {status === 'error' && (
          <div style={{
            padding: '10px 14px',
            borderRadius: 10,
            backgroundColor: '#fff0f0',
            color: '#cc0000',
            fontSize: 12,
            marginBottom: 14,
          }}>
            Не удалось отправить. Напишите напрямую в @shalerelax
          </div>
        )}

        <button
          type="submit"
          disabled={status === 'sending'}
          style={{
            width: '100%',
            padding: '14px 0',
            borderRadius: 12,
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
