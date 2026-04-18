import { useState, useEffect } from 'react'
import type { Page } from '../App'
import { HERO_PHOTOS } from '../config/photos'

interface Props {
  navigate: (p: Page) => void
}

export default function Home({ navigate }: Props) {
  const [current, setCurrent] = useState(0)

  useEffect(() => {
    const t = setInterval(() => setCurrent(c => (c + 1) % HERO_PHOTOS.length), 4500)
    return () => clearInterval(t)
  }, [])

  return (
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff' }}>
      {/* Шапка */}
      <div style={{ padding: '20px 24px 12px' }}>
        <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 2, color: '#999999', textTransform: 'uppercase', marginBottom: 12 }}>
          Приэльбрусье · КБР
        </div>
        <h1 style={{ margin: 0, fontSize: 32, fontWeight: 300, lineHeight: 1.15, color: '#111111', letterSpacing: '-0.5px' }}>
          Шале Релакс
        </h1>
        <p style={{ margin: '4px 0 0', fontSize: 16, fontWeight: 300, color: '#666666' }}>
          у подножия Эльбруса
        </p>
      </div>

      {/* Карточка с фото */}
      <div style={{ padding: '0 16px', marginTop: 8 }}>
        <div
          style={{
            borderRadius: 20,
            overflow: 'hidden',
            position: 'relative',
            height: 420,
            backgroundColor: '#f0f0f0',
            boxShadow: '0 2px 20px rgba(0,0,0,0.1)',
          }}
        >
          {HERO_PHOTOS.map((src, i) => (
            <img
              key={src}
              src={src}
              alt=""
              style={{
                position: 'absolute',
                inset: 0,
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                opacity: i === current ? 1 : 0,
                transition: 'opacity 0.8s ease',
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
              padding: '32px 20px 20px',
              background: 'linear-gradient(to top, rgba(0,0,0,0.65) 0%, transparent 100%)',
              display: 'flex',
              alignItems: 'flex-end',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ color: 'rgba(255,255,255,0.75)', fontSize: 12, fontWeight: 400, marginBottom: 2 }}>
                от
              </div>
              <div style={{ color: '#ffffff', fontSize: 26, fontWeight: 500, letterSpacing: '-0.5px' }}>
                15 000 ₽
              </div>
              <div style={{ color: 'rgba(255,255,255,0.75)', fontSize: 12 }}>
                за сутки
              </div>
            </div>
            <div style={{ display: 'flex', gap: 6 }}>
              {HERO_PHOTOS.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setCurrent(i)}
                  style={{
                    width: i === current ? 20 : 6,
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
      <div style={{ padding: '16px 16px 8px', display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        {['1800 м н.у.м.', '2 домика', '5 мин до подъёмника', '2 спальни'].map(tag => (
          <span
            key={tag}
            style={{
              padding: '6px 14px',
              borderRadius: 50,
              border: '1px solid #e0e0e0',
              fontSize: 12,
              color: '#444444',
              fontWeight: 400,
            }}
          >
            {tag}
          </span>
        ))}
      </div>

      {/* Кнопки */}
      <div style={{ padding: '12px 16px 24px', display: 'flex', gap: 10 }}>
        <button
          onClick={() => navigate('chalet')}
          style={{
            flex: 1,
            padding: '14px 0',
            borderRadius: 50,
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
            padding: '14px 0',
            borderRadius: 50,
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

      {/* Блок описания */}
      <div style={{ margin: '0 16px 24px', padding: '20px', borderRadius: 16, backgroundColor: '#f5f5f5' }}>
        <p style={{ margin: 0, fontSize: 14, fontWeight: 300, color: '#444444', lineHeight: 1.7 }}>
          Два уютных шале у подножия Эльбруса. 5 минут пешком до подъёмников.
          Тишина, горный воздух и вид на двуглавую вершину прямо из окна.
        </p>
      </div>
    </div>
  )
}
