# arenda-krana.kz — сайт аренды автокранов

Сборка: `python3 src/build.py` → папка `dist/`. Деплой на Vercel: корень репозитория, настройки берутся из `vercel.json` (фото из `images/` копируются в `dist/images/` при деплое).

Перед запуском заменить в `src/data.py`:
- `SITE_URL` — уже arenda-krana.kz (с www);
- ИИ-чат: после правки данных запустить `python3 src/gen_chat.py`;
- `GA_ID`, `GADS_ID`, `GADS_CALL_LABEL`, `GADS_WA_LABEL` — теги Analytics и Google Ads.

ИИ-чат: в Vercel → Settings → Environment Variables добавить `ANTHROPIC_API_KEY`. Без ключа работает встроенный автоответчик.

Фото: список файлов — `images/README.txt`. Пока фото нет, показываются заглушки.

Google Ads: `python3 src/ads.py src/templates/Create_New_Campaigns.xlsx` → папка `google-ads/`.
