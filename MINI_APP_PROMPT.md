Прочитай файлы TZ_v2.2.md и MINI_APP_TZ.md — это полное ТЗ проекта Шале Релакс включая новый раздел про Mini App.

Твоя задача: создать Telegram Mini App для Шале Релакс.

## Стек
- React + Vite + TypeScript + Tailwind CSS
- Папка: /Users/annakucenko/shale-relax/mini-app/
- Хостинг: Vercel (деплой через GitHub)
- Фото: Cloudinary (cloud name: dfbhw1rfx)

## Что создать

### 1. Инициализировать проект
```bash
cd /Users/annakucenko/shale-relax
npm create vite@latest mini-app -- --template react-ts
cd mini-app && npm install
npm install -D tailwindcss postcss autoprefixer
npm install @twa-dev/sdk
npx tailwindcss init -p
```

### 2. Структура папок
```
mini-app/
├── src/
│   ├── pages/
│   │   ├── Home.tsx        — главный экран со слайдшоу
│   │   ├── Chalet.tsx      — о домиках с галереей
│   │   ├── Location.tsx    — локация и активности
│   │   └── Booking.tsx     — форма бронирования
│   ├── components/
│   │   ├── PhotoSlider.tsx — слайдер фото
│   │   ├── Gallery.tsx     — галерея фото
│   │   └── BookingForm.tsx — форма с date picker
│   ├── App.tsx             — роутинг между экранами
│   └── main.tsx
├── public/
├── .env.local
├── vercel.json
└── package.json
```

### 3. Экраны (подробно)

**Home.tsx:**
- Полноэкранное слайдшоу фото с Cloudinary
- Поверх фото: название "Шале Релакс", подзаголовок "Домики у подножия Эльбруса"
- Бейджи: "1800 м" "5 мин до подъёмников" "2 домика"
- Две кнопки: "Подробнее" и "Забронировать"
- Цвета: тёмно-зелёный (#1a3a2a) + бежевый (#f5f0e8) + белый

**Chalet.tsx:**
- Галерея фото домиков
- Карточки с иконками: 🛏 2 спальни, 👥 до 6 гостей, 🍳 Кухня, 🌡 Тёплый пол, 📺 ТВ, 📶 Wi-Fi, 🔥 Мангал, 🚗 Парковка
- Цена: 15 000 ₽/сутки
- Кнопка "Забронировать"

**Location.tsx:**
- Что рядом: Эльбрус, Чегет, озёра, водопады, эндуро-маршруты
- Как добраться: аэропорт МВ или Нальчик, трасса А-158

**Booking.tsx:**
- Поля: Имя, Дата заезда, Дата выезда, Кол-во гостей (1-6), Контакт, Комментарий
- При отправке: POST /api/booking на Railway
- После успеха: экран подтверждения "Заявка принята!"

### 4. Фото в Cloudinary
Загрузи лучшие фото из /Users/annakucenko/shale-relax/Фото/ в Cloudinary:
- cloud name: dfbhw1rfx
- Используй Cloudinary CLI или Python скрипт для массовой загрузки
- Папка в Cloudinary: shale-relax/

Для загрузки через Python:
```python
import cloudinary
import cloudinary.uploader
cloudinary.config(cloud_name="dfbhw1rfx", api_key="957944298884622", api_secret="I76HdRg6HqW9GfCoHXEZMOTOods")
```

### 5. Backend endpoint в Railway
Добавь в проект файл api/booking_webhook.py или добавь endpoint в main.py:
- POST /api/booking
- Принимает JSON: {name, check_in, check_out, guests, contact, comment}
- Форматирует и отправляет владельцу через бота (OWNER_CHAT_ID=1914219730)
- Возвращает {"status": "ok"}

### 6. Кнопка в боте
В bot/keyboard.py добавь кнопку "🌐 Витрина" которая открывает Mini App через WebApp.
В bot/handlers.py добавь обработчик.

### 7. .env.local для mini-app
```
VITE_CLOUDINARY_CLOUD=dfbhw1rfx
VITE_API_URL=https://твой-railway-url.railway.app
```

### 8. vercel.json
```json
{
  "rewrites": [{"source": "/(.*)", "destination": "/"}]
}
```

### 9. Деплой
После создания:
1. cd mini-app && npm run build — проверить что собирается
2. git add -A && git commit -m "feat: telegram mini app" && git push
3. Подключить репо к Vercel (vercel.com → New Project → dzbbot-spec/shale-relax → Root Directory: mini-app)
4. Получить Vercel URL и добавить в BotFather как Mini App URL

## Стиль
- Тёмно-зелёный: #1a3a2a
- Бежевый: #f5f0e8  
- Акцент: #8B6914 (золотистый)
- Шрифт: системный sans-serif
- Без резких переходов — плавные анимации
- Мобильный дизайн (Telegram Mini App всегда мобильный)

## После создания
Покажи итоговую структуру и URL для деплоя на Vercel.

Начинай. Работай последовательно, не останавливайся без причины.
