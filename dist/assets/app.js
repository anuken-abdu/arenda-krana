(function () {
  "use strict";
  var KB = {"phone": "+7 701 070 37 34", "fleet": [[50, "4 единицы", "/avtokrany/avtokran-50-tonn/"], [70, "2 единицы", "/avtokrany/avtokran-70-tonn/"], [80, "2 единицы", "/avtokrany/avtokran-80-tonn/"], [100, "3 единицы", "/avtokrany/avtokran-100-tonn/"], [400, "1 единица", "/avtokrany/avtokran-400-tonn/"]], "brands": ["SANY", "XCMG", "Zoomlion"], "cities": [["almaty", "Алматы", "в Алматы", "/goroda/almaty/"], ["astana", "Астана", "в Астане", "/goroda/astana/"], ["shymkent", "Шымкент", "в Шымкенте", "/goroda/shymkent/"], ["karaganda", "Караганда", "в Караганде", "/goroda/karaganda/"], ["aktobe", "Актобе", "в Актобе", "/goroda/aktobe/"], ["taraz", "Тараз", "в Таразе", "/goroda/taraz/"], ["pavlodar", "Павлодар", "в Павлодаре", "/goroda/pavlodar/"], ["ust-kamenogorsk", "Усть-Каменогорск", "в Усть-Каменогорске", "/goroda/ust-kamenogorsk/"], ["semey", "Семей", "в Семее", "/goroda/semey/"], ["atyrau", "Атырау", "в Атырау", "/goroda/atyrau/"], ["kostanay", "Костанай", "в Костанае", "/goroda/kostanay/"], ["kyzylorda", "Кызылорда", "в Кызылорде", "/goroda/kyzylorda/"], ["uralsk", "Уральск", "в Уральске", "/goroda/uralsk/"], ["petropavlovsk", "Петропавловск", "в Петропавловске", "/goroda/petropavlovsk/"], ["aktau", "Актау", "в Актау", "/goroda/aktau/"], ["taldykorgan", "Талдыкорган", "в Талдыкоргане", "/goroda/taldykorgan/"], ["turkestan", "Туркестан", "в Туркестане", "/goroda/turkestan/"], ["kokshetau", "Кокшетау", "в Кокшетау", "/goroda/kokshetau/"], ["ekibastuz", "Экибастуз", "в Экибастузе", "/goroda/ekibastuz/"], ["temirtau", "Темиртау", "в Темиртау", "/goroda/temirtau/"], ["zhezkazgan", "Жезказган", "в Жезказгане", "/goroda/zhezkazgan/"], ["konaev", "Конаев", "в Конаеве", "/goroda/konaev/"], ["kaskelen", "Каскелен", "в Каскелене", "/goroda/kaskelen/"], ["talgar", "Талгар", "в Талгаре", "/goroda/talgar/"], ["esik", "Есик", "в Есике", "/goroda/esik/"], ["balkhash", "Балхаш", "в Балхаше", "/goroda/balkhash/"], ["zhanaozen", "Жанаозен", "в Жанаозене", "/goroda/zhanaozen/"], ["rudny", "Рудный", "в Рудном", "/goroda/rudny/"], ["satpaev", "Сатпаев", "в Сатпаеве", "/goroda/satpaev/"], ["ridder", "Риддер", "в Риддере", "/goroda/ridder/"], ["stepnogorsk", "Степногорск", "в Степногорске", "/goroda/stepnogorsk/"]], "faq": [["Какие автокраны есть в парке?", "В парке 12 автокранов грузоподъёмностью 50, 70, 80, 100 и 400 тонн — техника SANY, XCMG и Zoomlion: 50 тонн — 4 единицы, 70 тонн — 2, 80 тонн — 2, 100 тонн — 3, 400 тонн — 1."], ["Вы работаете по всему Казахстану?", "Да. Работаем в Алматы, Астане, Шымкенте и других городах и регионах Казахстана. Выезд в другой город включает перебазировку крана — сроки и стоимость называем при заявке."], ["Сколько стоит аренда автокрана?", "Стоимость зависит от грузоподъёмности крана, массы груза, вылета и высоты подъёма, времени работы и удалённости объекта. Позвоните или напишите в WhatsApp — назовём цену под вашу задачу."], ["Как выбрать кран нужной грузоподъёмности?", "Грузоподъёмность в названии крана — максимальная, на минимальном вылете. Реальная допустимая масса зависит от вылета стрелы и высоты по грузовысотной таблице. Сообщите массу груза, расстояние от места стоянки крана до точки установки и высоту — подберём кран с запасом."], ["На какое время можно заказать кран?", "Время работы согласуем под задачу: разовый подъём, смена или весь этап работ. Минимальное время и порядок оплаты уточняйте при заявке."], ["Нужен ли проект производства работ (ППР)?", "Для сложных и ответственных подъёмов, работ вблизи ЛЭП и на действующих предприятиях обычно требуется ППР. Подскажем, нужен ли он для вашей задачи."], ["Что подготовить на площадке?", "Ровную площадку для стоянки и выносных опор, свободный подъезд, сведения о подземных коммуникациях и ЛЭП рядом. Груз должен быть готов к строповке."], ["Кран 400 тонн можно заказать в другой город?", "Да, но перебазировка крана 400 тонн требует отдельной логистики противовеса и согласования маршрута, поэтому такие работы планируют заранее."]], "services": [["Монтаж металлоконструкций", "/uslugi/montazh-metallokonstrukciy/", [50, 70, 80, 100]], ["Монтаж ЖБИ", "/uslugi/montazh-zhbi/", [50, 70, 80]], ["Погрузка и разгрузка", "/uslugi/pogruzka-razgruzka/", [50, 70, 80, 100]], ["Монтаж оборудования", "/uslugi/montazh-oborudovaniya/", [50, 70, 80, 100, 400]], ["Краны для строительства", "/uslugi/stroitelstvo/", [50, 70, 80, 100]], ["Монтаж ветрогенераторов", "/uslugi/vetroenergetika/", [100, 400]], ["Демонтаж конструкций", "/uslugi/demontazh/", [50, 70, 80, 100]], ["Подъём грузов на высоту", "/uslugi/podem-na-vysotu/", [50, 70, 80, 100]], ["Монтаж ангаров и складов", "/uslugi/montazh-angarov-i-skladov/", [50, 70, 80]], ["Монтаж модульных зданий", "/uslugi/montazh-modulnyh-zdaniy/", [50, 70]], ["Монтаж резервуаров и ёмкостей", "/uslugi/montazh-rezervuarov/", [70, 80, 100, 400]], ["Монтаж трансформаторов", "/uslugi/montazh-transformatorov/", [50, 70, 80, 100]], ["Монтаж опор ЛЭП и освещения", "/uslugi/montazh-opor-lep/", [50, 70, 80]], ["Монтаж мостовых конструкций", "/uslugi/montazh-mostovyh-konstrukciy/", [80, 100, 400]], ["Подъём вентиляции и кондиционеров", "/uslugi/montazh-ventilyacii-i-kondicionerov/", [50, 70]], ["Монтаж рекламных конструкций", "/uslugi/montazh-reklamnyh-konstrukciy/", [50]], ["Монтаж башен и мачт связи", "/uslugi/montazh-bashen-svyazi/", [50, 70, 80, 100]], ["Разгрузка тралов и длинномеров", "/uslugi/razgruzka-tralov-i-dlinnomerov/", [50, 70, 80, 100]], ["Погрузка контейнеров", "/uslugi/pogruzka-konteynerov/", [50, 70]], ["Перестановка оборудования", "/uslugi/peremeshchenie-oborudovaniya/", [50, 70, 80, 100]], ["Подъём негабаритных грузов", "/uslugi/negabaritnye-gruzy/", [80, 100, 400]], ["Нефтегазовые объекты", "/uslugi/neftegazovye-obekty/", [70, 80, 100, 400]], ["Энергетика", "/uslugi/energetika/", [50, 70, 80, 100, 400]], ["Промышленные предприятия", "/uslugi/promyshlennye-predpriyatiya/", [50, 70, 80, 100, 400]], ["Дороги и инфраструктура", "/uslugi/infrastruktura/", [50, 70, 80, 100, 400]], ["Элеваторы и агрообъекты", "/uslugi/selskoe-hozyaystvo/", [50, 70, 80, 100]]]};
  var CFG = window.CFG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function waUrl(t) { return "https://wa.me/" + CFG.wan + "?text=" + encodeURIComponent(t); }

  /* ---------- конверсии Google Ads / GA4 ---------- */
  function conv(kind) {
    if (typeof window.gtag !== "function") return;
    var label = kind === "call" ? CFG.call : CFG.wa;
    if (CFG.ads && label) window.gtag("event", "conversion", { send_to: CFG.ads + "/" + label, value: 1.0, currency: "USD", transport_type: "beacon" });
    if (CFG.ga) window.gtag("event", kind === "call" ? "phone_click" : "whatsapp_click", { page_path: location.pathname, transport_type: "beacon" });
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    var h = a.getAttribute("href") || "";
    if (h.indexOf("tel:") === 0) conv("call");
    else if (h.indexOf("wa.me") > -1) conv("wa");
  });

  /* ---------- меню ---------- */
  var burger = $(".burger"), nav = $("#nav");
  function setNav(o) {
    if (!burger || !nav) return;
    nav.classList.toggle("open", o); burger.setAttribute("aria-expanded", o ? "true" : "false");
    burger.setAttribute("aria-label", o ? "Закрыть меню" : "Открыть меню"); document.body.classList.toggle("lock", o);
  }
  if (burger) burger.addEventListener("click", function () { setNav(!nav.classList.contains("open")); });
  if (nav) nav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
  window.addEventListener("resize", function () { if (window.innerWidth > 1023) setNav(false); });

  /* ---------- назад / наверх ---------- */
  var fab = $(".fab");
  var ftr = $(".ftr");
  function onScroll() {
    if (fab) fab.classList.toggle("on", window.pageYOffset > 500);
    // у самого низа страницы плавающие кнопки становятся полупрозрачными, чтобы не закрывать подвал
    var end = ftr ? ftr.getBoundingClientRect().top < window.innerHeight - 40 : false;
    document.body.classList.toggle("at-end", end);
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  $$("[data-top]").forEach(function (b) { b.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); }); });
  $$("[data-back]").forEach(function (b) {
    b.addEventListener("click", function () {
      var ref = document.referrer, same = ref && ref.indexOf(location.host) > -1;
      if (same && history.length > 1) history.back(); else location.href = "/";
    });
  });

  /* ---------- заявка → WhatsApp ---------- */
  $$("form[data-lead]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var ph = (f.elements.phone.value || "").replace(/[^\d+]/g, ""), err = $(".f-err", f);
      if (ph.replace(/\D/g, "").length < 10) { err.hidden = false; f.elements.phone.focus(); return; }
      err.hidden = true;
      var t = "Здравствуйте! Заявка с сайта.\nГород: " + f.elements.city.value + "\nКран: " + f.elements.ton.value +
        (f.elements.msg.value.trim() ? "\nЗадача: " + f.elements.msg.value.trim() : "") +
        (f.elements.name.value.trim() ? "\nИмя: " + f.elements.name.value.trim() : "") + "\nТелефон: " + ph;
      conv("wa");
      window.open(waUrl(t), "_blank", "noopener");
    });
  });

  /* ---------- чат: ИИ через /api/chat, без ключа — встроенный автоответчик ---------- */
  var chat = $("#chat"), list = chat && $(".chat-l", chat), qbox = chat && $(".chat-q", chat), opener = $(".chat-o");
  var hist = [], started = false, busy = false;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function add(text, who, html) {
    var d = document.createElement("div"); d.className = "msg " + (who === "u" ? "msg-u" : "msg-b");
    if (html) d.innerHTML = html; else d.textContent = text;
    list.appendChild(d); list.scrollTop = list.scrollHeight; return d;
  }
  function quick(items) {
    qbox.innerHTML = "";
    items.forEach(function (q) { var b = document.createElement("button"); b.type = "button"; b.textContent = q; b.addEventListener("click", function () { ask(q); }); qbox.appendChild(b); });
  }
  function low(s) { return s.toLowerCase().replace(/ё/g, "е"); }
  function local(q) {
    var s = low(q), m;
    var fl = KB.fleet || [];
    for (var i = 0; i < fl.length; i++) {
      if (new RegExp("(^|\\D)" + fl[i][0] + "(\\D|$)").test(s)) return { t: "Автокран " + fl[i][0] + " тонн есть в парке (" + fl[i][1] + "). Напишите массу груза, высоту и адрес объекта — проверим, подходит ли этот класс, и назовём стоимость.", u: fl[i][2] };
    }
    var cs = KB.cities || [];
    for (var j = 0; j < cs.length; j++) {
      var n = low(cs[j][1]).slice(0, Math.max(4, cs[j][1].length - 2));
      if (s.indexOf(n) > -1) return { t: "Да, работаем " + cs[j][2] + ". Сроки подачи крана и перебазировку согласуем при заявке. Какой груз нужно поднять?", u: cs[j][3] };
    }
    if (/цен|стоим|сколько|прайс|почем/.test(s)) return { t: "Стоимость зависит от класса крана, времени работы, массы груза, вылета и высоты, удалённости объекта. Напишите задачу и город — назовём цену." };
    if (/sany|xcmg|zoomlion|сани|марк|бренд|производ/.test(s)) return { t: "В парке техника " + (KB.brands || []).join(", ") + ". Подберём кран под вашу задачу." };
    if (/выбр|какой кран|подобр|грузовысот|вылет/.test(s)) return { t: "Кран выбирают по грузовысотной таблице: масса груза, расстояние от стоянки до точки установки и высота. Напишите эти данные — подберём класс с запасом." };
    if (/город|регион|выезд|казахстан|межгород/.test(s)) return { t: "Работаем по всему Казахстану. Выезд в другой город включает перебазировку крана — сроки и стоимость называем при заявке." };
    if (/ппр|проект/.test(s)) return { t: "Для сложных подъёмов, работ возле ЛЭП и на действующих предприятиях обычно нужен ППР. Подскажем, требуется ли он для вашей задачи." };
    if (/привет|здравств|салем|добрый/.test(s)) return { t: "Здравствуйте! Подскажу по автокранам 50–400 тонн. Что нужно поднять и в каком городе?" };
    if (s.replace(/\D/g, "").length >= 10) return { t: "Спасибо! Передайте номер менеджеру через WhatsApp кнопкой ниже — так заявка дойдёт быстрее." };
    return { t: "Уточню у менеджера. Напишите, что нужно поднять, массу и город — или позвоните " + KB.phone + "." };
  }
  function reply(r) {
    var h = esc(r.t) + (r.u ? '<br><a href="' + r.u + '">Открыть страницу</a>' : "");
    add("", "b", h);
  }
  function ask(q) {
    q = String(q || "").trim(); if (!q || busy) return;
    add(q, "u"); hist.push({ role: "user", content: q });
    busy = true; var wait = add("…", "b");
    var done = function (txt) { busy = false; wait.remove(); hist.push({ role: "assistant", content: txt }); add(txt, "b"); };
    var ctrl = window.AbortController ? new AbortController() : null; var to = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
    fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: hist.slice(-12), page: location.pathname }), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { clearTimeout(to); if (!r.ok) throw 0; return r.json(); })
      .then(function (d) { if (!d || !d.text) throw 0; done(d.text); })
      .catch(function () { busy = false; wait.remove(); var r = local(q); hist.push({ role: "assistant", content: r.t }); reply(r); });
  }
  function openChat() {
    chat.hidden = false; if (opener) opener.hidden = true;
    if (!started) { started = true; add("Здравствуйте! Помогу подобрать автокран 50–400 тонн. Что нужно поднять и в каком городе?", "b"); quick(["Сколько стоит?", "Какой кран выбрать?", "Работаете в моём городе?", "Кран 400 тонн"]); }
    setTimeout(function () { var i = $("input", chat); if (i && window.innerWidth > 767) i.focus(); }, 50);
  }
  if (chat) {
    $$("[data-chat]").forEach(function (b) { b.addEventListener("click", openChat); });
    $("[data-chat-x]", chat).addEventListener("click", function () { chat.hidden = true; if (opener) opener.hidden = false; });
    $(".chat-f", chat).addEventListener("submit", function (e) { e.preventDefault(); var i = this.elements.q; ask(i.value); i.value = ""; });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (chat && !chat.hidden) { chat.hidden = true; if (opener) opener.hidden = false; }
    setNav(false);
  });
})();
