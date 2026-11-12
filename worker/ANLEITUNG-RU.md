# Сервер для «Оценки по видео»: настройка (≈10 минут, без программирования)

Ключ Anthropic вводите только вы сами, в Cloudflare. В код и в чат его не вставляйте.

## 1. Ключ Anthropic
1. console.anthropic.com → Settings → Billing: пополнить на 5 $ (хватит примерно на 300–500 оценок).
2. Settings → API Keys → Create Key, имя `iltan-raumscan`. Скопируйте ключ (показывается один раз).
3. Settings → Limits: поставьте месячный лимит, например 10 $, чтобы не было сюрпризов.

## 2. Worker в Cloudflare
1. dash.cloudflare.com → Workers & Pages → Create → Create Worker.
2. Имя: `iltan-raumscan` → Deploy.
3. Edit code → удалите всё → вставьте содержимое `worker.js` → Deploy.

## 3. Хранилище для лимита (KV)
1. Storage & Databases → KV → Create namespace, имя `RL`.
2. Worker `iltan-raumscan` → Settings → Bindings → Add → KV namespace: Variable name `RL`, namespace `RL` → Save.

## 4. Ключ как секрет
Worker → Settings → Variables and Secrets → Add:
- Type **Secret**, Name `ANTHROPIC_API_KEY`, Value — ваш ключ → Save (Deploy).
- (по желанию) Type Text, `DAILY_LIMIT` = `8` — сколько оценок в день с одного телефона.

## 5. Адрес
Наверху страницы worker'а будет адрес вида `https://iltan-raumscan.XXXX.workers.dev`.
Адрес: https://iltan-raumscan.katovski32.workers.dev (уже вписан в /scan/).
