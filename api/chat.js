// Vercel Serverless Function: ИИ-консультант KRANPARK.
// Нужна переменная окружения ANTHROPIC_API_KEY (Vercel → Settings → Environment Variables).
// Без ключа функция отвечает 503, и сайт сам переключается на встроенный автоответчик.

const MODEL = process.env.ANTHROPIC_MODEL || "claude-haiku-5-5";
const PHONE = "+7 701 070 37 34";

const SYSTEM = `Ты — онлайн-консультант компании KRANPARK в чате на сайте. Компания сдаёт в аренду автокраны по всему Казахстану.
Парк: 50 тонн — 4 единицы; 70 тонн — 2 единицы; 80 тонн — 2 единицы; 100 тонн — 3 единицы; 400 тонн — 1 единица. Производители техники: SANY, XCMG, Zoomlion.
Услуги: Монтаж металлоконструкций (50, 70, 80, 100 т); Монтаж ЖБИ (50, 70, 80 т); Погрузка и разгрузка (50, 70, 80, 100 т); Монтаж оборудования (50, 70, 80, 100, 400 т); Краны для строительства (50, 70, 80, 100 т); Монтаж ветрогенераторов (100, 400 т); Демонтаж конструкций (50, 70, 80, 100 т); Подъём грузов на высоту (50, 70, 80, 100 т).
Города: Алматы, Астана, Шымкент, Караганда, Актобе, Тараз, Павлодар, Усть-Каменогорск, Семей, Атырау, Костанай, Кызылорда, Уральск, Петропавловск, Актау, Талдыкорган, Туркестан, Кокшетау, Экибастуз, Темиртау, Жезказган, Конаев, Каскелен, Талгар, Есик, Балхаш, Жанаозен, Рудный, Сатпаев, Риддер, Степногорск и другие населённые пункты Казахстана. Выезд в другой город включает перебазировку крана — сроки и стоимость называет менеджер.
Подбор крана: грузоподъёмность в названии — максимальная, на минимальном вылете. Реальную допустимую массу определяет грузовысотная таблица по вылету и высоте. Для подбора нужны: масса груза со стропами, расстояние от стоянки крана до точки установки, высота подъёма, условия площадки (подъезд, грунт, ЛЭП).
Телефон и WhatsApp: ${PHONE}.

Правила:
- Отвечай на языке клиента (русский или казахский), коротко: 1–4 предложения, без markdown, списков и эмодзи.
- Не называй цены, сроки подачи, минимальное время аренды, модели кранов, длину стрелы и любые характеристики, которых нет в этом описании. Про стоимость говори, от чего она зависит, и предлагай уточнить у менеджера.
- Не давай гарантий и не обещай, что кран точно поднимет груз — возможность подъёма проверяет менеджер по грузовысотной таблице.
- Если спрашивают, бот ли ты, честно скажи, что ты онлайн-консультант, а менеджер ответит по телефону или в WhatsApp.
- Цель — помочь и получить заявку: уточни груз, массу, высоту, город и сроки, попроси номер или предложи кнопку WhatsApp под чатом.`;

const hits = new Map();
function limited(ip) {
  const now = Date.now(), win = 10 * 60 * 1000, max = 25;
  const arr = (hits.get(ip) || []).filter((t) => now - t < win);
  arr.push(now); hits.set(ip, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length > max;
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "method" }); return; }
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { res.status(503).json({ error: "not_configured" }); return; }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) { res.status(429).json({ error: "rate" }); return; }
  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const msgs = Array.isArray(body && body.messages) ? body.messages.slice(-12) : [];
  const clean = msgs.filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .map((m) => ({ role: m.role, content: m.content.slice(0, 1500) }));
  while (clean.length && clean[0].role !== "user") clean.shift();
  if (!clean.length) { res.status(400).json({ error: "empty" }); return; }
  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({ model: MODEL, max_tokens: 400, system: SYSTEM + "\nСтраница: " + String((body && body.page) || "/").slice(0, 120), messages: clean }),
    });
    if (!r.ok) { res.status(502).json({ error: "upstream" }); return; }
    const d = await r.json();
    const text = (d.content || []).filter((c) => c.type === "text").map((c) => c.text).join("").trim();
    res.status(200).json({ text: text || "Уточню у менеджера. Позвоните " + PHONE + " или напишите в WhatsApp." });
  } catch (e) { res.status(502).json({ error: "fail" }); }
};
