import { useState } from 'react'
import { GALLERY_PHOTOS, cloudUrl } from '../config/photos'

export { GALLERY_PHOTOS }

interface Props {
  photos?: string[]
}

export default function Gallery({ photos = GALLERY_PHOTOS }: Props) {
  const [lightbox, setLightbox] = useState<string | null>(null)

  return (
    <>
      <div className="grid grid-cols-3 gap-1">
        {photos.map((photo) => (
          <button
            key={photo}
            onClick={() => setLightbox(cloudUrl(photo, 1200))}
            className="aspect-square overflow-hidden"
          >
            <img
              src={cloudUrl(photo)}
              alt=""
              loading="lazy"
              className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
            />
          </button>
        ))}
      </div>

      {lightbox && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center"
          style={{ backgroundColor: 'rgba(0,0,0,0.9)' }}
          onClick={() => setLightbox(null)}
        >
          <img
            src={lightbox}
            alt=""
            className="max-w-full max-h-full object-contain"
            style={{ maxHeight: '90dvh' }}
          />
          <button
            className="absolute top-4 right-4 text-white text-3xl leading-none"
            onClick={() => setLightbox(null)}
          >
            ×
          </button>
        </div>
      )}
    </>
  )
}
