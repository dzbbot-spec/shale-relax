import NavBar from '../components/NavBar'
import type { Page } from '../App'

interface Props {
  navigate: (p: Page) => void
}

const ACTIVITIES = [
  { icon: '🏔', title: 'Эльбрус', desc: 'Канатная дорога, горнолыжные трассы, подъём на 3500+ м' },
  { icon: '⛷', title: 'Чегет', desc: 'Горнолыжный курорт с трассами разной сложности' },
  { icon: '💧', title: 'Водопады', desc: 'Чегемские, Гедмишх — живописные маршруты' },
  { icon: '🏞', title: 'Озёра', desc: 'Голубые озёра, Донгузорун — горные жемчужины' },
  { icon: '🏍', title: 'Эндуро', desc: 'Маршруты по горным тропам для мотоциклистов' },
  { icon: '🥾', title: 'Пешие маршруты', desc: 'Трекинг к леднику Большой Азау и Поляна Нарзанов' },
]

const HOW_TO_GET = [
  { icon: '✈️', title: 'Самолётом', desc: 'Аэропорт Минеральные Воды (2.5 ч) или Нальчик (1 ч)' },
  { icon: '🚗', title: 'На автомобиле', desc: 'Трасса А-158 через Нальчик → п. Эльбрус' },
  { icon: '🚌', title: 'На автобусе', desc: 'Из Нальчика маршрутки до п. Эльбрус (~1.5 ч)' },
]

export default function Location({ navigate }: Props) {
  return (
    <div style={{ minHeight: '100dvh', backgroundColor: 'var(--color-beige)' }}>
      {/* Шапка */}
      <div className="p-5 pt-4 pb-2">
        <h1 className="font-bold" style={{ color: 'var(--color-green)', fontSize: 26 }}>
          Локация
        </h1>
        <p className="mt-1" style={{ color: '#555', fontSize: 14 }}>
          Посёлок Эльбрус, КБР · Высота 1800 м н.у.м.
        </p>
      </div>

      {/* Карта-плейсхолдер */}
      <div
        className="mx-5 mb-4 rounded-2xl overflow-hidden flex items-center justify-center"
        style={{ height: 160, backgroundColor: '#d4e8db', position: 'relative' }}
      >
        <div className="text-center">
          <div style={{ fontSize: 40 }}>📍</div>
          <div style={{ color: 'var(--color-green)', fontWeight: 600, fontSize: 15 }}>
            п. Эльбрус, ул. Лесная 1
          </div>
          <div style={{ color: '#555', fontSize: 12, marginTop: 2 }}>
            43.3897° N, 42.5083° E
          </div>
        </div>
      </div>

      {/* Расстояния */}
      <div className="px-5 mb-4">
        <div
          className="p-4 rounded-2xl grid grid-cols-3 gap-3 text-center"
          style={{ backgroundColor: 'var(--color-green)', color: 'white' }}
        >
          {[
            { val: '5 мин', label: 'до подъёмника' },
            { val: '1800 м', label: 'высота' },
            { val: '2 км', label: 'до центра' },
          ].map(({ val, label }) => (
            <div key={label}>
              <div className="font-bold" style={{ fontSize: 18 }}>{val}</div>
              <div style={{ fontSize: 11, opacity: 0.7 }}>{label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Активности */}
      <div className="px-5 mb-4">
        <h2 className="font-semibold mb-3" style={{ color: 'var(--color-green)', fontSize: 17 }}>
          Что рядом
        </h2>
        <div className="flex flex-col gap-2">
          {ACTIVITIES.map(({ icon, title, desc }) => (
            <div
              key={title}
              className="flex items-start gap-3 p-3 rounded-xl"
              style={{ backgroundColor: 'white' }}
            >
              <span style={{ fontSize: 22, lineHeight: 1 }}>{icon}</span>
              <div>
                <div className="font-semibold" style={{ color: 'var(--color-green)', fontSize: 14 }}>
                  {title}
                </div>
                <div style={{ color: '#666', fontSize: 12, marginTop: 2 }}>{desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Как добраться */}
      <div className="px-5 mb-4">
        <h2 className="font-semibold mb-3" style={{ color: 'var(--color-green)', fontSize: 17 }}>
          Как добраться
        </h2>
        <div className="flex flex-col gap-2">
          {HOW_TO_GET.map(({ icon, title, desc }) => (
            <div
              key={title}
              className="flex items-start gap-3 p-3 rounded-xl"
              style={{ backgroundColor: 'white' }}
            >
              <span style={{ fontSize: 22, lineHeight: 1 }}>{icon}</span>
              <div>
                <div className="font-semibold" style={{ color: 'var(--color-green)', fontSize: 14 }}>
                  {title}
                </div>
                <div style={{ color: '#666', fontSize: 12, marginTop: 2 }}>{desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div
        className="mx-5 mb-5 p-4 rounded-xl"
        style={{ backgroundColor: 'rgba(26,58,42,0.08)' }}
      >
        <p style={{ fontSize: 13, color: '#444', lineHeight: 1.6 }}>
          🌤 Лучшее время: июль–август (лето) и январь–март (зима)<br />
          ❄️ Горнолыжный сезон: ноябрь–апрель<br />
          🌿 Пешие маршруты: май–октябрь
        </p>
      </div>

      <button
        onClick={() => navigate('booking')}
        className="mx-5 w-[calc(100%-40px)] py-4 rounded-2xl font-semibold text-white text-base transition-opacity active:opacity-80 mb-5"
        style={{ backgroundColor: 'var(--color-green)' }}
      >
        Забронировать
      </button>

      <div style={{ height: 80 }} />
      <NavBar current="location" navigate={navigate} />
    </div>
  )
}
