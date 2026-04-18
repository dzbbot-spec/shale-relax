import { useState } from 'react'
import type { Page } from '../App'
import { HERO_PHOTOS } from '../config/photos'

interface Props {
  navigate: (p: Page) => void
}

export default function Home({ navigate }: Props) {
  const [current, setCurrent] = useState(0)
  const [touchStartX, setTouchStartX] = useState<number | null>(null)

  const prev = () => setCurrent(c => (c - 1 + HERO_PHOTOS.length) % HERO_PHOTOS.length)
  const next = () => setCurrent(c => (c + 1) % HERO_PHOTOS.length)

  const onTouchStart = (e: React.TouchEvent) => setTouchStartX(e.touches[0].clientX)
  const onTouchEnd = (e: React.TouchEvent) => {
    if (touchStartX === null) return
    const diff = touchStartX - e.changedTouches[0].clientX
    if (Math.abs(diff) > 40) diff > 0 ? next() : prev()
    setTouchStartX(null)
  }

  return (
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff' }}>
      {/* Шапка */}
      <div style={{ padding: '14px 16px 8px' }}>
        <div style={{ fontSize: 10, fontWeight: 500, letterSpacing: 2, color: '#999999', textTransform: 'uppercase', marginBottom: 8 }}>
          Приэльбрусье · КБР
        </div>
        <h1 style={{ margin: 0, fontSize: 24, fontWeight: 300, lineHeight: 1.15, color: '#111111', letterSpacing: '-0.5px' }}>
          Шале Релакс
        </h1>
        <p style={{ margin: '2px 0 0', fontSize: 14, fontWeight: 300, color: '#666666' }}>
          у подножия Эльбруса
        </p>
      </div>

      {/* Слайдер */}
      <div style={{ padding: '0 12px', marginTop: 6 }}>
        <div
          onTouchStart={onTouchStart}
          onTouchEnd={onTouchEnd}
          style={{
            borderRadius: 12,
            overflow: 'hidden',
            position: 'relative',
            height: '45dvh',
            backgroundColor: '#f0f0f0',
            boxShadow: '0 2px 16px rgba(0,0,0,0.1)',
          }}
        >
          {HERO_PHOTOS.map((src, i) => (
            <img
              key={src}
              src={src}
              alt=""
              {...(i === 0 ? { fetchPriority: 'high' } : { loading: 'lazy' })}
              style={{
                position: 'absolute',
                inset: 0,
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                opacity: i === current ? 1 : 0,
                transition: 'opacity 0.6s ease',
              }}
            />
          ))}

          {/* Плашка с ценой */}
          <div
            style={{
              position: 'absolute',
              bottom: 0,
              left: 0,
              right: 0,
              padding: '24px 16px 14px',
              background: 'linear-gradient(to top, rgba(0,0,0,0.65) 0%, transparent 100%)',
              display: 'flex',
              alignItems: 'flex-end',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ color: 'rgba(255,255,255,0.75)', fontSize: 11, fontWeight: 400, marginBottom: 2 }}>от</div>
              <div style={{ color: '#ffffff', fontSize: 22, fontWeight: 500, letterSpacing: '-0.5px' }}>15 000 ₽</div>
              <div style={{ color: 'rgba(255,255,255,0.75)', fontSize: 11 }}>за сутки</div>
            </div>
            <div style={{ display: 'flex', gap: 6 }}>
              {HERO_PHOTOS.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setCurrent(i)}
                  style={{
                    width: i === current ? 18 : 6,
                    height: 6,
                    borderRadius: 3,
                    backgroundColor: i === current ? '#ffffff' : 'rgba(255,255,255,0.4)',
                    transition: 'all 0.3s ease',
                  }}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Теги */}
      <div style={{ padding: '10px 12px 6px', display: 'flex', gap: 6, flexWrap: 'wrap' }}>
        {['1800 м н.у.м.', '2 домика', '5 мин до подъёмника', '2 спальни'].map(tag => (
          <span
            key={tag}
            style={{
              padding: '5px 10px',
              borderRadius: 8,
              border: '1px solid #e0e0e0',
              fontSize: 11,
              color: '#444444',
              fontWeight: 400,
            }}
          >
            {tag}
          </span>
        ))}
      </div>

      {/* Кнопки */}
      <div style={{ padding: '8px 12px 16px', display: 'flex', gap: 8 }}>
        <button
          onClick={() => navigate('chalet')}
          style={{
            flex: 1,
            padding: '12px 0',
            borderRadius: 12,
            border: '1.5px solid #111111',
            backgroundColor: 'transparent',
            color: '#111111',
            fontSize: 14,
            fontWeight: 500,
            letterSpacing: 0.3,
          }}
        >
          Подробнее
        </button>
        <button
          onClick={() => navigate('booking')}
          style={{
            flex: 1,
            padding: '12px 0',
            borderRadius: 12,
            backgroundColor: '#111111',
            color: '#ffffff',
            fontSize: 14,
            fontWeight: 500,
            letterSpacing: 0.3,
          }}
        >
          Забронировать
        </button>
      </div>

      {/* Описание */}
      <div style={{ margin: '0 12px 16px', padding: '14px 16px', borderRadius: 12, backgroundColor: '#f5f5f5' }}>
        <p style={{ margin: 0, fontSize: 13, fontWeight: 300, color: '#444444', lineHeight: 1.7 }}>
          Два уютных шале у подножия Эльбруса. 5 минут пешком до подъёмников.
          Тишина, горный воздух и вид на двуглавую вершину прямо из окна.
        </p>
      </div>
    </div>
  )
}
