import { useState } from 'react'
import Home from './pages/Home'
import Chalet from './pages/Chalet'
import Location from './pages/Location'
import Booking from './pages/Booking'

export type Page = 'home' | 'chalet' | 'location' | 'booking'

export default function App() {
  const [page, setPage] = useState<Page>('home')

  const navigate = (p: Page) => {
    setPage(p)
    window.scrollTo(0, 0)
  }

  return (
    <div style={{ backgroundColor: 'var(--color-beige)', minHeight: '100dvh' }}>
      {page === 'home' && <Home navigate={navigate} />}
      {page === 'chalet' && <Chalet navigate={navigate} />}
      {page === 'location' && <Location navigate={navigate} />}
      {page === 'booking' && <Booking navigate={navigate} />}
    </div>
  )
}
