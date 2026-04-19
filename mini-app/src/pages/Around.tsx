import type { Page } from '../App'

interface Props {
  navigate: (p: Page) => void
}

interface Place {
  name: string
  detail?: string
}

interface Section {
  title: string
  places: Place[]
}

const SECTIONS: Section[] = [
  {
    title: 'Горнолыжные курорты',
    places: [
      { name: 'Эльбрус (Поляна Азау)', detail: '5 мин езды' },
      { name: 'Чегет', detail: '10 мин езды' },
    ],
  },
  {
    title: 'Природа',
    places: [
      { name: 'Водопад Девичьи Косы', detail: '20 мин пешком' },
      { name: 'Джилы-Су', detail: 'нарзанные источники' },
      { name: 'Озеро Донгуз-Орун', detail: 'пешеходный маршрут' },
      { name: 'Баксанское ущелье', detail: 'вдоль реки Баксан' },
    ],
  },
  {
    title: 'Активности',
    places: [
      { name: 'Эндуро-маршруты', detail: 'горные тропы Приэльбрусья' },
      { name: 'Конные прогулки', detail: 'по ущельям' },
      { name: 'Параплан', detail: 'с горных склонов' },
      { name: 'Термальные источники', detail: 'в ущелье' },
    ],
  },
  {
    title: 'Инфраструктура',
    places: [
      { name: 'Кафе и рестораны', detail: 'в посёлке Эльбрус' },
      { name: 'Прокат снаряжения', detail: 'лыжи, сноуборд, мотоциклы' },
      { name: 'Аптека и магазины', detail: 'в посёлке' },
    ],
  },
]

export default function Around({ navigate: _navigate }: Props) {
  return (
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff', paddingBottom: 'calc(env(safe-area-inset-bottom, 16px) + 70px)' }}>

      <div style={{ padding: '16px 16px 8px' }}>
        <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 2, color: '#999999', textTransform: 'uppercase', marginBottom: 8 }}>
          Приэльбрусье
        </div>
        <h1 style={{ margin: 0, fontSize: 22, fontWeight: 300, color: '#111111' }}>
          Вокруг нас
        </h1>
      </div>

      <div style={{ padding: '8px 16px 0' }}>
        {SECTIONS.map((section) => (
          <div key={section.title} style={{ marginBottom: 20 }}>
            <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 1.5, color: '#999999', textTransform: 'uppercase', marginBottom: 10 }}>
              {section.title}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {section.places.map((place) => (
                <div
                  key={place.name}
                  style={{
                    padding: '12px 14px',
                    borderRadius: 10,
                    backgroundColor: '#f5f5f5',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: 12,
                  }}
                >
                  <div style={{ fontSize: 13, fontWeight: 400, color: '#111111' }}>
                    {place.name}
                  </div>
                  {place.detail && (
                    <div style={{ fontSize: 11, fontWeight: 300, color: '#999999', flexShrink: 0, textAlign: 'right' }}>
                      {place.detail}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
