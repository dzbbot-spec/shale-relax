import { useState } from 'react'

const CLOUD = import.meta.env.VITE_CLOUDINARY_CLOUD || 'dfbhw1rfx'

export const GALLERY_PHOTOS = [
  'shale-relax/20250101_182454',
  'shale-relax/20250101_182514',
  'shale-relax/20250101_182622',
  'shale-relax/20250101_182641',
  'shale-relax/20250101_182706',
  'shale-relax/20250101_183012',
  'shale-relax/20250101_183133',
  'shale-relax/20250121_142412',
  'shale-relax/20250121_142438',
  'shale-relax/20250121_142453',
  'shale-relax/20250121_142615',
  'shale-relax/20250121_142755',
  'shale-relax/20250712_201908',
  'shale-relax/20250712_201919',
  'shale-relax/20250712_201931',
  'shale-relax/20250712_201943',
]

function cloudUrl(publicId: string, w = 400) {
  return `https://res.cloudinary.com/${CLOUD}/image/upload/w_${w},c_fill,q_auto,f_auto/${publicId}.jpg`
}

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
