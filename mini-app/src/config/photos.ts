export const CLOUD = import.meta.env.VITE_CLOUDINARY_CLOUD || 'dfbhw1rfx'

export function cloudUrl(publicId: string, w = 800) {
  return `https://res.cloudinary.com/${CLOUD}/image/upload/w_${w},c_fill,q_auto,f_auto/${publicId}.jpg`
}

// Uploaded to Cloudinary: shale-relax/
export const HERO_PHOTOS = [
  'shale-relax/20250712_201908',
  'shale-relax/20250712_201919',
  'shale-relax/20250712_201931',
  'shale-relax/20250712_201943',
  'shale-relax/20250101_182454',
  'shale-relax/20250101_182514',
]

export const GALLERY_PHOTOS = [
  'shale-relax/20250712_201908',
  'shale-relax/20250712_201919',
  'shale-relax/20250712_201931',
  'shale-relax/20250712_201943',
  'shale-relax/20250101_182454',
  'shale-relax/20250101_182514',
  'shale-relax/20250101_182622',
  'shale-relax/20250101_182641',
  'shale-relax/20241230_182844',
  'shale-relax/20241230_182922',
]
