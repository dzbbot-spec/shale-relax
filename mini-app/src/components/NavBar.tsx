import type { Page } from '../App'

interface Props {
  current: Page
  navigate: (p: Page) => void
}

const ITEMS: { page: Page; label: string; icon: string }[] = [
  { page: 'home', label: 'Главная', icon: '🏠' },
  { page: 'chalet', label: 'Домики', icon: '🛏' },
  { page: 'location', label: 'Локация', icon: '🏔' },
  { page: 'booking', label: 'Забронировать', icon: '📅' },
]

export default function NavBar({ current, navigate }: Props) {
  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-40 flex"
      style={{
        backgroundColor: 'var(--color-green)',
        paddingBottom: 'env(safe-area-inset-bottom)',
      }}
    >
      {ITEMS.map(({ page, label, icon }) => (
        <button
          key={page}
          onClick={() => navigate(page)}
          className="flex-1 flex flex-col items-center py-2 gap-0.5 transition-opacity"
          style={{
            color: current === page ? 'var(--color-gold)' : 'rgba(255,255,255,0.6)',
            fontSize: 10,
          }}
        >
          <span style={{ fontSize: 20 }}>{icon}</span>
          <span>{label}</span>
        </button>
      ))}
    </nav>
  )
}
