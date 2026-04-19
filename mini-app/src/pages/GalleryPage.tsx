import { useState } from 'react'
import type { Page } from '../App'
import { OUTSIDE_PHOTOS, INSIDE_PHOTOS } from '../config/photos'

interface Props {
  navigate: (p: Page) => void
}

type Tab = 'outside' | 'inside'

export default function GalleryPage({ navigate: _navigate }: Props) {
  const [tab, setTab] = useState<Tab>('outside')
  const [lightboxIndex, setLightboxIndex] = useState<number | null>(null)
  const [touchStartX, setTouchStartX] = useState<number | null>(null)

  const photos = tab === 'outside' ? OUTSIDE_PHOTOS : INSIDE_PHOTOS

  const openLightbox = (i: number) => setLightboxIndex(i)
  const closeLightbox = () => setLightboxIndex(null)

  const prev = () => setLightboxIndex(i => i !== null ? (i - 1 + photos.length) % photos.length : null)
  const next = () => setLightboxIndex(i => i !== null ? (i + 1) % photos.length : null)

  const onTouchStart = (e: React.TouchEvent) => setTouchStartX(e.touches[0].clientX)
  const onTouchEnd = (e: React.TouchEvent) => {
    if (touchStartX === null) return
    const diff = touchStartX - e.changedTouches[0].clientX
    if (Math.abs(diff) > 50) diff > 0 ? next() : prev()
    setTouchStartX(null)
  }

  return (
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff' }}>
      <div style={{ padding: '20px 24px 16px' }}>
        <h1 style={{ margin: 0, fontSize: 28, fontWeight: 300, color: '#111111', letterSpacing: '-0.5px' }}>
          Галерея
        </h1>
      </div>

      <div style={{ padding: '0 16px 16px' }}>
        <div style={{ display: 'inline-flex', backgroundColor: '#f0f0f0', borderRadius: 50, padding: 3 }}>
          {(['outside', 'inside'] as Tab[]).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                padding: '8px 24px',
                borderRadius: 50,
                fontSize: 13,
                fontWeight: 500,
                backgroundColor: tab === t ? '#111111' : 'transparent',
                color: tab === t ? '#ffffff' : '#666666',
                transition: 'all 0.2s ease',
              }}
            >
              {t === 'outside' ? 'Снаружи' : 'Внутри'}
            </button>
          ))}
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 3, padding: '0 3px' }}>
        {photos.map((src, i) => (
          <button
            key={src}
            onClick={() => openLightbox(i)}
            style={{
              aspectRatio: '4/3',
              overflow: 'hidden',
              borderRadius: i === 0 ? '14px 0 0 0' : i === 1 ? '0 14px 0 0' : 0,
              backgroundColor: '#f0f0f0',
            }}
          >
            <img src={src} alt="" loading="lazy" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} />
          </button>
        ))}
      </div>

      {lightboxIndex !== null && (
        <div
          style={{ position: 'fixed', inset: 0, zIndex: 100, backgroundColor: 'rgba(0,0,0,0.95)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          onTouchStart={onTouchStart}
          onTouchEnd={onTouchEnd}
        >
          <img
            src={photos[lightboxIndex]}
            alt=""
            style={{ maxWidth: '100%', maxHeight: '90dvh', objectFit: 'contain', userSelect: 'none' }}
          />

          {/* Закрыть */}
          <button
            onClick={closeLightbox}
            style={{ position: 'absolute', top: 20, right: 20, width: 36, height: 36, borderRadius: '50%', backgroundColor: 'rgba(255,255,255,0.15)', color: '#ffffff', fontSize: 20, display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          >×</button>

          {/* Назад */}
          <button
            onClick={(e) => { e.stopPropagation(); prev() }}
            style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', width: 40, height: 40, borderRadius: '50%', backgroundColor: 'rgba(255,255,255,0.15)', color: '#ffffff', fontSize: 22, display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          >‹</button>

          {/* Вперёд */}
          <button
            onClick={(e) => { e.stopPropagation(); next() }}
            style={{ position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)', width: 40, height: 40, borderRadius: '50%', backgroundColor: 'rgba(255,255,255,0.15)', color: '#ffffff', fontSize: 22, display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          >›</button>

          {/* Счётчик */}
          <div style={{ position: 'absolute', bottom: 24, left: '50%', transform: 'translateX(-50%)', color: 'rgba(255,255,255,0.6)', fontSize: 13 }}>
            {lightboxIndex + 1} / {photos.length}
          </div>
        </div>
      )}
    </div>
  )
}
