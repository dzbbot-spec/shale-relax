import { useState, useEffect } from 'react'

const CLOUD = import.meta.env.VITE_CLOUDINARY_CLOUD || 'dfbhw1rfx'

const HERO_PHOTOS = [
  'shale-relax/20250712_201908',
  'shale-relax/20250712_201919',
  'shale-relax/20250712_201931',
  'shale-relax/20250712_201943',
  'shale-relax/20250101_182454',
  'shale-relax/20250101_182514',
]

function cloudUrl(publicId: string, w = 800) {
  return `https://res.cloudinary.com/${CLOUD}/image/upload/w_${w},c_fill,q_auto,f_auto/${publicId}.jpg`
}

interface Props {
  autoPlay?: boolean
  interval?: number
}

export default function PhotoSlider({ autoPlay = true, interval = 4000 }: Props) {
  const [current, setCurrent] = useState(0)
  const [loaded, setLoaded] = useState<boolean[]>(new Array(HERO_PHOTOS.length).fill(false))

  useEffect(() => {
    if (!autoPlay) return
    const timer = setInterval(() => {
      setCurrent(c => (c + 1) % HERO_PHOTOS.length)
    }, interval)
    return () => clearInterval(timer)
  }, [autoPlay, interval])

  const markLoaded = (i: number) => {
    setLoaded(prev => {
      const next = [...prev]
      next[i] = true
      return next
    })
  }

  return (
    <div className="relative w-full h-full overflow-hidden">
      {HERO_PHOTOS.map((photo, i) => (
        <div
          key={photo}
          className="absolute inset-0 transition-opacity duration-1000"
          style={{ opacity: i === current ? 1 : 0 }}
        >
          <img
            src={cloudUrl(photo)}
            alt=""
            className="w-full h-full object-cover"
            loading={i === 0 ? 'eager' : 'lazy'}
            onLoad={() => markLoaded(i)}
            style={{ opacity: loaded[i] ? 1 : 0, transition: 'opacity 0.3s' }}
          />
        </div>
      ))}

      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-10">
        {HERO_PHOTOS.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className="w-2 h-2 rounded-full transition-all"
            style={{
              backgroundColor: i === current ? 'white' : 'rgba(255,255,255,0.4)',
              transform: i === current ? 'scale(1.3)' : 'scale(1)',
            }}
          />
        ))}
      </div>
    </div>
  )
}
