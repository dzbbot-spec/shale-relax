import PhotoSlider from '../components/PhotoSlider'
import type { Page } from '../App'

interface Props {
  navigate: (p: Page) => void
}

export default function Home({ navigate }: Props) {
  return (
    <div className="flex flex-col" style={{ minHeight: '100dvh' }}>
      {/* Hero с полноэкранным слайдшоу */}
      <div className="relative flex-1" style={{ minHeight: '100dvh' }}>
        <PhotoSlider />

        {/* Тёмный оверлей снизу */}
        <div
          className="absolute inset-0"
          style={{
            background: 'linear-gradient(to bottom, rgba(0,0,0,0.1) 0%, rgba(26,58,42,0.75) 80%)',
            pointerEvents: 'none',
          }}
        />

        {/* Контент поверх фото */}
        <div className="absolute inset-0 flex flex-col justify-end p-6 pb-24">
          <div className="text-white">
            <h1
              className="font-bold mb-1"
              style={{ fontSize: 32, letterSpacing: '-0.5px', lineHeight: 1.1 }}
            >
              Шале Релакс
            </h1>
            <p className="mb-4 opacity-90" style={{ fontSize: 16 }}>
              Домики у подножия Эльбруса
            </p>

            {/* Бейджи */}
            <div className="flex flex-wrap gap-2 mb-6">
              {['⛰ 1800 м', '🚠 5 мин до подъёмников', '🏠 2 домика'].map(b => (
                <span
                  key={b}
                  className="px-3 py-1 rounded-full text-sm font-medium"
                  style={{ backgroundColor: 'rgba(255,255,255,0.2)', backdropFilter: 'blur(8px)' }}
                >
                  {b}
                </span>
              ))}
            </div>

            {/* Кнопки */}
            <div className="flex gap-3">
              <button
                onClick={() => navigate('chalet')}
                className="flex-1 py-3 rounded-xl font-semibold text-center transition-opacity active:opacity-80"
                style={{ backgroundColor: 'white', color: 'var(--color-green)', fontSize: 15 }}
              >
                Подробнее
              </button>
              <button
                onClick={() => navigate('booking')}
                className="flex-1 py-3 rounded-xl font-semibold text-center transition-opacity active:opacity-80"
                style={{ backgroundColor: 'var(--color-gold)', color: 'white', fontSize: 15 }}
              >
                Забронировать
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Нижний блок — преимущества */}
      <div className="p-5 pb-24" style={{ backgroundColor: 'var(--color-beige)' }}>
        <h2 className="font-semibold mb-4" style={{ color: 'var(--color-green)', fontSize: 18 }}>
          Почему выбирают нас
        </h2>
        <div className="grid grid-cols-2 gap-3">
          {[
            { icon: '🌄', text: 'Вид на Эльбрус из окна' },
            { icon: '🛖', text: 'Уютные тёплые домики' },
            { icon: '🎿', text: 'Рядом Эльбрус и Чегет' },
            { icon: '🤫', text: 'Тихий конец посёлка' },
          ].map(({ icon, text }) => (
            <div
              key={text}
              className="p-3 rounded-xl flex items-center gap-3"
              style={{ backgroundColor: 'white' }}
            >
              <span style={{ fontSize: 24 }}>{icon}</span>
              <span style={{ fontSize: 13, color: 'var(--color-green)' }}>{text}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
