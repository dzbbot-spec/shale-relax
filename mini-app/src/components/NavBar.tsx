import React from 'react'
import type { Page } from '../App'

interface Props {
  current: Page
  navigate: (p: Page) => void
}

const HomeIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
    <polyline points="9 22 9 12 15 12 15 22"/>
  </svg>
)

const GalleryIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2"/>
    <circle cx="8.5" cy="8.5" r="1.5"/>
    <polyline points="21 15 16 10 5 21"/>
  </svg>
)

const InfoIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <line x1="12" y1="8" x2="12" y2="12"/>
    <line x1="12" y1="16" x2="12.01" y2="16"/>
  </svg>
)

const BookIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="4" width="18" height="18" rx="2"/>
    <line x1="16" y1="2" x2="16" y2="6"/>
    <line x1="8" y1="2" x2="8" y2="6"/>
    <line x1="3" y1="10" x2="21" y2="10"/>
  </svg>
)

const ITEMS: { page: Page; Icon: () => React.ReactElement }[] = [
  { page: 'home', Icon: HomeIcon },
  { page: 'gallery', Icon: GalleryIcon },
  { page: 'chalet', Icon: InfoIcon },
  { page: 'booking', Icon: BookIcon },
]

export default function NavBar({ current, navigate }: Props) {
  return (
    <div
      style={{
        position: 'fixed',
        bottom: 16,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 50,
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 4,
          backgroundColor: '#111111',
          borderRadius: 50,
          padding: '6px 6px',
          boxShadow: '0 4px 24px rgba(0,0,0,0.25)',
        }}
      >
        {ITEMS.map(({ page, Icon }) => {
          const active = current === page
          return (
            <button
              key={page}
              onClick={() => navigate(page)}
              style={{
                width: 52,
                height: 44,
                borderRadius: 50,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: active ? '#ffffff' : 'transparent',
                color: active ? '#111111' : 'rgba(255,255,255,0.6)',
                transition: 'all 0.2s ease',
              }}
            >
              <Icon />
            </button>
          )
        })}
      </div>
    </div>
  )
}
