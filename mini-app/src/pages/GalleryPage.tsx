import { useState } from 'react'
import type { Page } from '../App'
import { OUTSIDE_PHOTOS, INSIDE_PHOTOS } from '../config/photos'

interface Props {
  navigate: (p: Page) => void
}

type Tab = 'outside' | 'inside'

export default function GalleryPage({ navigate: _navigate }: Props) {
  const [tab, setTab] = useState<Tab>('outside')
  const [lightbox, setLightbox] = useState<string | null>(null)

  const photos = tab === 'outside' ? OUTSIDE_PHOTOS : INSIDE_PHOTOS

  return (
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff' }}>
      {/* Шапка */}
      <div style={{ padding: '20px 24px 16px' }}>
        <h1 style={{ margin: 0, fontSize: 28, fontWeight: 300, color: '#111111', letterSpacing: '-0.5px' }}>
          Галерея
        </h1>
      </div>

      {/* Переключатель */}
      <div style={{ padding: '0 16px 16px' }}>
        <div
          style={{
            display: 'inline-flex',
            backgroundColor: '#f0f0f0',
            borderRadius: 50,
            padding: 3,
          }}
        >
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

      {/* Сетка фото */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 3,
          padding: '0 3px',
        }}
      >
        {photos.map((src, i) => (
          <button
            key={src}
            onClick={() => setLightbox(src)}
            style={{
              aspectRatio: '4/3',
              overflow: 'hidden',
              borderRadius: i === 0 ? '14px 0 0 0' : i === 1 ? '0 14px 0 0' : 0,
              backgroundColor: '#f0f0f0',
            }}
          >
            <img
              src={src}
              alt=""
              loading="lazy"
              style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
            />
          </button>
        ))}
      </div>

      {/* Лайтбокс */}
      {lightbox && (
        <div
          onClick={() => setLightbox(null)}
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 100,
            backgroundColor: 'rgba(0,0,0,0.95)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <img
            src={lightbox}
            alt=""
            style={{ maxWidth: '100%', maxHeight: '90dvh', objectFit: 'contain' }}
          />
          <button
            style={{
              position: 'absolute',
              top: 20,
              right: 20,
              width: 36,
              height: 36,
              borderRadius: 50,
              backgroundColor: 'rgba(255,255,255,0.15)',
              color: '#ffffff',
              fontSize: 20,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            ×
          </button>
        </div>
      )}
    </div>
  )
}
