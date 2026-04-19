import { useState, useEffect, useRef } from 'react'
import Home from './pages/Home'
import Chalet from './pages/Chalet'
import GalleryPage from './pages/GalleryPage'
import Booking from './pages/Booking'
import Around from './pages/Around'
import Contacts from './pages/Contacts'
import NavBar from './components/NavBar'

export type Page = 'home' | 'gallery' | 'chalet' | 'around' | 'booking' | 'contacts'

export default function App() {
  const [page, setPage] = useState<Page>('home')
  const [fadeKey, setFadeKey] = useState(0)
  const prevPage = useRef<Page>('home')

  const navigate = (p: Page) => {
    if (p === prevPage.current) return
    prevPage.current = p
    setPage(p)
    setFadeKey(k => k + 1)
    window.scrollTo(0, 0)
  }

  useEffect(() => {}, [fadeKey])

  return (
    <div style={{ backgroundColor: '#ffffff', minHeight: '100dvh', paddingBottom: 'calc(65px + env(safe-area-inset-bottom, 0px))' }}>
      <div key={fadeKey} className="page-fade">
        {page === 'home'     && <Home navigate={navigate} />}
        {page === 'gallery'  && <GalleryPage navigate={navigate} />}
        {page === 'chalet'   && <Chalet navigate={navigate} />}
        {page === 'around'   && <Around navigate={navigate} />}
        {page === 'booking'  && <Booking navigate={navigate} />}
        {page === 'contacts' && <Contacts navigate={navigate} />}
      </div>
      <NavBar current={page} navigate={navigate} />
    </div>
  )
}
