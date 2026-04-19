import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { Page } from '../App'

interface Props {
  navigate: (p: Page) => void
}

const LAT = 43.251272
const LNG = 42.636834

function MapWidget() {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<L.Map | null>(null)

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return

    const map = L.map(containerRef.current, {
      center: [LAT, LNG],
      zoom: 15,
      zoomControl: false,
      scrollWheelZoom: false,
      dragging: false,
      attributionControl: false,
    })

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://carto.com/">CartoDB</a>',
      subdomains: 'abcd',
      maxZoom: 19,
    }).addTo(map)

    const icon = L.divIcon({
      className: '',
      html: '<div style="width:14px;height:14px;background:#111111;border-radius:50%;border:2px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3)"></div>',
      iconSize: [14, 14],
      iconAnchor: [7, 7],
    })

    L.marker([LAT, LNG], { icon })
      .addTo(map)
      .bindPopup('Шале Релакс')

    mapRef.current = map

    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [])

  return (
    <div style={{ borderRadius: 12, overflow: 'hidden', boxShadow: '0 2px 12px rgba(0,0,0,0.08)' }}>
      <div ref={containerRef} style={{ height: 220, width: '100%' }} />
    </div>
  )
}

const PhoneIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.62 1.27h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.91a16 16 0 0 0 6.09 6.09l1.21-1.21a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7a2 2 0 0 1 1.72 2z"/>
  </svg>
)

const TgIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13"/>
    <polygon points="22 2 15 22 11 13 2 9 22 2"/>
  </svg>
)

const InstIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="2" width="20" height="20" rx="5"/>
    <circle cx="12" cy="12" r="4"/>
    <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor"/>
  </svg>
)

const PinIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
    <circle cx="12" cy="10" r="3"/>
  </svg>
)

const CONTACTS = [
  {
    Icon: PhoneIcon,
    label: 'Телефон',
    value: '+7 928 910-76-01',
    href: 'tel:+79289107601',
    btnText: 'Позвонить',
  },
  {
    Icon: TgIcon,
    label: 'Telegram',
    value: '@shale_relax_elbrus',
    href: 'https://t.me/shale_relax_elbrus',
    btnText: 'Написать',
  },
  {
    Icon: InstIcon,
    label: 'Instagram',
    value: '@shale_relax_elbrus',
    href: 'https://instagram.com/shale_relax_elbrus',
    btnText: 'Перейти',
  },
]

export default function Contacts({ navigate: _navigate }: Props) {
  return (
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff', paddingBottom: 'calc(env(safe-area-inset-bottom, 16px) + 70px)' }}>

      <div style={{ padding: '16px 16px 8px' }}>
        <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 2, color: '#999999', textTransform: 'uppercase', marginBottom: 8 }}>
          Шале Релакс
        </div>
        <h1 style={{ margin: 0, fontSize: 22, fontWeight: 300, color: '#111111' }}>
          Контакты
        </h1>
      </div>

      <div style={{ padding: '12px 16px 0' }}>
        {CONTACTS.map(({ Icon, label, value, href, btnText }) => (
          <div
            key={label}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              padding: '14px 16px',
              borderRadius: 12,
              backgroundColor: '#f5f5f5',
              marginBottom: 10,
            }}
          >
            <div style={{ color: '#555555', flexShrink: 0 }}>
              <Icon />
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 11, fontWeight: 500, color: '#999999', marginBottom: 2 }}>{label}</div>
              <div style={{ fontSize: 13, fontWeight: 400, color: '#111111', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{value}</div>
            </div>
            <a
              href={href}
              target={href.startsWith('tel:') ? undefined : '_blank'}
              rel="noopener noreferrer"
              style={{
                flexShrink: 0,
                padding: '8px 14px',
                borderRadius: 8,
                backgroundColor: '#111111',
                color: '#ffffff',
                fontSize: 12,
                fontWeight: 500,
                textDecoration: 'none',
              }}
            >
              {btnText}
            </a>
          </div>
        ))}
      </div>

      <div style={{ padding: '16px 16px 0' }}>
        <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 2, color: '#999999', textTransform: 'uppercase', marginBottom: 10 }}>
          Адрес
        </div>
        <div style={{ display: 'flex', gap: 12, padding: '14px 16px', borderRadius: 12, backgroundColor: '#f5f5f5', marginBottom: 12 }}>
          <div style={{ color: '#555555', flexShrink: 0, marginTop: 2 }}>
            <PinIcon />
          </div>
          <div>
            <div style={{ fontSize: 13, fontWeight: 400, color: '#111111', lineHeight: 1.6 }}>
              пос. Эльбрус, Кабардино-Балкария
            </div>
            <div style={{ fontSize: 12, fontWeight: 300, color: '#999999', marginTop: 2 }}>
              1800 м н.у.м. — 5 минут до подъёмников
            </div>
          </div>
        </div>

        <MapWidget />

        <a
          href={`https://maps.google.com/?q=${LAT},${LNG}`}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: 'block',
            marginTop: 10,
            padding: '12px 0',
            borderRadius: 12,
            border: '1.5px solid #111111',
            backgroundColor: 'transparent',
            color: '#111111',
            fontSize: 14,
            fontWeight: 500,
            textAlign: 'center',
            textDecoration: 'none',
            letterSpacing: 0.3,
          }}
        >
          Открыть в картах
        </a>
      </div>
    </div>
  )
}
