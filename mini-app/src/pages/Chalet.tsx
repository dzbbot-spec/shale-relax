import Gallery from '../components/Gallery'
import NavBar from '../components/NavBar'
import type { Page } from '../App'

interface Props {
  navigate: (p: Page) => void
}

const FEATURES = [
  { icon: '🛏', text: '2 спальни' },
  { icon: '👥', text: 'до 6 гостей' },
  { icon: '🍳', text: 'Кухня с посудой' },
  { icon: '🌡', text: 'Тёплый пол' },
  { icon: '📺', text: 'Телевизор' },
  { icon: '📶', text: 'Wi-Fi' },
  { icon: '🔥', text: 'Мангал' },
  { icon: '🚗', text: 'Парковка' },
]

export default function Chalet({ navigate }: Props) {
  return (
    <div style={{ minHeight: '100dvh', backgroundColor: 'var(--color-beige)' }}>
      {/* Шапка */}
      <div className="p-5 pt-4 pb-2">
        <h1 className="font-bold" style={{ color: 'var(--color-green)', fontSize: 26 }}>
          Наши домики
        </h1>
        <p className="mt-1" style={{ color: '#555', fontSize: 14 }}>
          2 одинаковых уютных домика у Эльбруса
        </p>
      </div>

      {/* Галерея */}
      <Gallery />

      {/* Описание */}
      <div className="p-5">
        <div
          className="p-4 rounded-2xl mb-4"
          style={{ backgroundColor: 'var(--color-green)', color: 'white' }}
        >
          <div className="flex justify-between items-center">
            <div>
              <div className="text-sm opacity-70">Стоимость</div>
              <div className="font-bold" style={{ fontSize: 28 }}>
                15 000 ₽
                <span className="text-sm font-normal opacity-70 ml-1">/ сутки</span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm opacity-70">Расположение</div>
              <div className="text-sm">📍 п. Эльбрус · 1800 м</div>
            </div>
          </div>
        </div>

        {/* Удобства */}
        <h2 className="font-semibold mb-3" style={{ color: 'var(--color-green)', fontSize: 17 }}>
          Что включено
        </h2>
        <div className="grid grid-cols-2 gap-2 mb-5">
          {FEATURES.map(({ icon, text }) => (
            <div
              key={text}
              className="flex items-center gap-3 p-3 rounded-xl"
              style={{ backgroundColor: 'white' }}
            >
              <span style={{ fontSize: 20 }}>{icon}</span>
              <span style={{ fontSize: 14, color: 'var(--color-green)' }}>{text}</span>
            </div>
          ))}
        </div>

        {/* Дополнительно */}
        <div
          className="p-4 rounded-xl mb-5"
          style={{ backgroundColor: 'rgba(26,58,42,0.08)' }}
        >
          <p style={{ fontSize: 13, color: '#444', lineHeight: 1.5 }}>
            🚠 5 минут пешком до подъёмников Эльбруса и Чегета<br />
            🏔 Вид на двуглавую вершину прямо из окна<br />
            🌲 Тихий конец посёлка — тишина и горный воздух<br />
            🔑 Самозаезд, встреча по договорённости
          </p>
        </div>

        <button
          onClick={() => navigate('booking')}
          className="w-full py-4 rounded-2xl font-semibold text-white text-base transition-opacity active:opacity-80"
          style={{ backgroundColor: 'var(--color-green)' }}
        >
          Забронировать — 15 000 ₽/сутки
        </button>
      </div>

      <div style={{ height: 80 }} />
      <NavBar current="chalet" navigate={navigate} />
    </div>
  )
}
