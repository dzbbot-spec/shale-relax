import { useState } from 'react'
import Home from './pages/Home'
import Chalet from './pages/Chalet'
import GalleryPage from './pages/GalleryPage'
import Booking from './pages/Booking'
import NavBar from './components/NavBar'

export type Page = 'home' | 'gallery' | 'chalet' | 'booking'

export default function App() {
  const [page, setPage] = useState<Page>('home')

  const navigate = (p: Page) => {
    setPage(p)
    window.scrollTo(0, 0)
  }

  return (
    <div style={{ backgroundColor: '#ffffff', minHeight: '100dvh', paddingBottom: 'calc(65px + env(safe-area-inset-bottom, 0px))' }}>
      {page === 'home' && <Home navigate={navigate} />}
      {page === 'gallery' && <GalleryPage navigate={navigate} />}
      {page === 'chalet' && <Chalet navigate={navigate} />}
      {page === 'booking' && <Booking navigate={navigate} />}
      <NavBar current={page} navigate={navigate} />
    </div>
  )
}
