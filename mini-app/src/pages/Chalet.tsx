import type { Page } from '../App'
import { INSIDE_PHOTOS } from '../config/photos'

interface Props {
  navigate: (p: Page) => void
}

const FEATURES = [
  '2 спальни',
  'до 6 гостей',
  'Кухня',
  'Тёплый пол',
  'Телевизор',
  'Wi-Fi',
  'Мангал',
  'Парковка',
]

export default function Chalet({ navigate }: Props) {
  return (
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff' }}>
      {/* Шапка */}
      <div style={{ padding: '20px 24px 8px' }}>
        <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 2, color: '#999999', textTransform: 'uppercase', marginBottom: 8 }}>
          пос. Эльбрус, КБР
        </div>
        <h1 style={{ margin: 0, fontSize: 28, fontWeight: 300, color: '#111111', letterSpacing: '-0.5px' }}>
          Шале Релакс
        </h1>
      </div>

      {/* Цена */}
      <div style={{ padding: '12px 24px 16px', display: 'flex', alignItems: 'baseline', gap: 6 }}>
        <span style={{ fontSize: 32, fontWeight: 500, color: '#111111', letterSpacing: '-1px' }}>
          15 000 ₽
        </span>
        <span style={{ fontSize: 14, color: '#999999', fontWeight: 300 }}>
          / сутки
        </span>
      </div>

      {/* Характеристики 2x4 */}
      <div style={{ padding: '0 16px 20px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
          {FEATURES.map(f => (
            <div
              key={f}
              style={{
                padding: '14px 16px',
                borderRadius: 12,
                backgroundColor: '#f5f5f5',
                fontSize: 13,
                fontWeight: 400,
                color: '#111111',
              }}
            >
              {f}
            </div>
          ))}
        </div>
      </div>

      {/* Галерея внутри — горизонтальный скролл */}
      <div style={{ paddingBottom: 12 }}>
        <div style={{ padding: '0 24px 12px', fontSize: 13, fontWeight: 500, color: '#999999', letterSpacing: 1, textTransform: 'uppercase' }}>
          Интерьер
        </div>
        <div
          style={{
            display: 'flex',
            gap: 10,
            overflowX: 'auto',
            padding: '0 16px',
            scrollSnapType: 'x mandatory',
            scrollbarWidth: 'none',
          }}
        >
          {INSIDE_PHOTOS.map(src => (
            <div
              key={src}
              style={{
                flex: '0 0 220px',
                height: 160,
                borderRadius: 12,
                overflow: 'hidden',
                backgroundColor: '#f0f0f0',
                scrollSnapAlign: 'start',
              }}
            >
              <img
                src={src}
                alt=""
                loading="lazy"
                style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
              />
            </div>
          ))}
          <div style={{ flex: '0 0 16px' }} />
        </div>
      </div>

      {/* Описание */}
      <div style={{ margin: '8px 16px 20px', padding: '18px 20px', borderRadius: 12, backgroundColor: '#f5f5f5' }}>
        <p style={{ margin: 0, fontSize: 13, fontWeight: 300, color: '#444444', lineHeight: 1.7 }}>
          5 минут пешком до подъёмников Эльбруса и Чегета.
          Вид на двуглавую вершину из окна. Тихий конец посёлка.
          Самозаезд, встреча по договорённости.
        </p>
      </div>

      {/* Кнопка */}
      <div style={{ padding: '0 16px 24px' }}>
        <button
          onClick={() => navigate('booking')}
          style={{
            width: '100%',
            padding: '16px 0',
            borderRadius: 12,
            backgroundColor: '#111111',
            color: '#ffffff',
            fontSize: 15,
            fontWeight: 500,
            letterSpacing: 0.3,
          }}
        >
          Забронировать
        </button>
      </div>
    </div>
  )
}
