import type { Page } from '../App'

interface Props {
  navigate: (p: Page) => void
}

const FEATURES = [
  { label: '2 спальни', desc: 'Двуспальные кровати' },
  { label: 'до 6 гостей', desc: 'Вместимость' },
  { label: 'Кухня', desc: 'Посуда и техника' },
  { label: 'Тёплый пол', desc: 'Во всём домике' },
  { label: 'Телевизор', desc: 'Smart TV' },
  { label: 'Wi-Fi', desc: 'Высокоскоростной' },
  { label: 'Мангал', desc: 'Костровая зона' },
  { label: 'Парковка', desc: 'Бесплатно' },
]

const FAQ_ITEMS = [
  { q: 'Есть ли залог?', a: 'Да, залог при заселении. Возвращается после выезда.' },
  { q: 'Можно с животными?', a: 'Да, по согласованию с владельцем.' },
  { q: 'Ранний заезд / поздний выезд?', a: 'Возможен при наличии свободных дат, обсуждается индивидуально.' },
  { q: 'Можно курить?', a: 'Некурящий объект. Курение только на улице.' },
  { q: 'Есть ли парковка?', a: 'Да, бесплатная парковка на территории.' },
]

const INFO_BLOCKS = [
  {
    title: 'Расположение',
    text: 'Тихий конец посёлка Эльбрус, Кабардино-Балкария. Высота 1800 м над уровнем моря. До подъёмников Эльбруса и Чегета — 5 минут пешком.',
  },
  {
    title: 'Вид',
    text: 'Из окон открывается вид на двуглавую вершину Эльбруса. Утром — рассветы над горным хребтом, вечером — закаты над ущельем.',
  },
  {
    title: 'Заселение',
    text: 'Самозаезд по коду, встреча по договорённости. Заезд с 14:00, выезд до 12:00. Возможен ранний заезд или поздний выезд при наличии свободных дат.',
  },
  {
    title: 'Правила',
    text: 'Некурящий объект. Разрешено с животными по согласованию. Тихий час с 23:00. Залог при заселении.',
  },
]

export default function Chalet({ navigate }: Props) {
  return (
    <div style={{ minHeight: '100dvh', backgroundColor: '#ffffff', paddingBottom: 'calc(env(safe-area-inset-bottom, 16px) + 70px)' }}>

      <div style={{ padding: '16px 16px 8px' }}>
        <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 2, color: '#999999', textTransform: 'uppercase', marginBottom: 8 }}>
          пос. Эльбрус · КБР · 1800 м
        </div>
        <h1 style={{ margin: 0, fontSize: 22, fontWeight: 300, color: '#111111' }}>
          Шале Релакс
        </h1>
        <div style={{ marginTop: 8, display: 'flex', alignItems: 'baseline', gap: 6 }}>
          <span style={{ fontSize: 26, fontWeight: 500, color: '#111111' }}>15 000 ₽</span>
          <span style={{ fontSize: 13, color: '#999999', fontWeight: 300 }}>/ сутки</span>
        </div>
      </div>

      <div style={{ padding: '16px 16px 0' }}>
        <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 1.5, color: '#999999', textTransform: 'uppercase', marginBottom: 10 }}>
          Удобства
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
          {FEATURES.map(f => (
            <div key={f.label} style={{ padding: '12px 14px', borderRadius: 10, backgroundColor: '#f5f5f5' }}>
              <div style={{ fontSize: 13, fontWeight: 500, color: '#111111', marginBottom: 2 }}>{f.label}</div>
              <div style={{ fontSize: 11, fontWeight: 300, color: '#999999' }}>{f.desc}</div>
            </div>
          ))}
        </div>
      </div>

      <div style={{ padding: '20px 16px 0' }}>
        {INFO_BLOCKS.map((block, i) => (
          <div key={i} style={{ marginBottom: 12, padding: '14px 16px', borderRadius: 10, border: '1px solid #f0f0f0' }}>
            <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 1.5, color: '#999999', textTransform: 'uppercase', marginBottom: 6 }}>
              {block.title}
            </div>
            <p style={{ margin: 0, fontSize: 13, fontWeight: 300, color: '#444444', lineHeight: 1.7 }}>
              {block.text}
            </p>
          </div>
        ))}
      </div>

      <div style={{ padding: '20px 16px 0' }}>
        <div style={{ fontSize: 11, fontWeight: 500, letterSpacing: 1.5, color: '#999999', textTransform: 'uppercase', marginBottom: 10 }}>
          Вопросы и ответы
        </div>
        {FAQ_ITEMS.map((item, i) => (
          <div key={i} style={{ marginBottom: 8, padding: '14px 16px', borderRadius: 10, backgroundColor: '#f5f5f5' }}>
            <div style={{ fontSize: 13, fontWeight: 500, color: '#111111', marginBottom: 4 }}>{item.q}</div>
            <div style={{ fontSize: 13, fontWeight: 300, color: '#555555', lineHeight: 1.6 }}>{item.a}</div>
          </div>
        ))}
      </div>

      <div style={{ padding: '16px 16px 0' }}>
        <button
          onClick={() => navigate('booking')}
          style={{ width: '100%', padding: '14px 0', borderRadius: 12, backgroundColor: '#111111', color: '#ffffff', fontSize: 15, fontWeight: 500, border: 'none', cursor: 'pointer' }}
        >
          Забронировать
        </button>
      </div>
    </div>
  )
}
