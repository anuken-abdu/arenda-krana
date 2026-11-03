(function () {
  "use strict";
  var KB = /*__KB__*/{};
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
  // встроенный автоответчик: работает без ИИ-ключа и при сбое сети
  var INTENTS = [
    [/цен|стоим|сколько стоит|прайс|почем|по чем|тариф|сколько будет/, "Стоимость зависит от класса крана, времени работы, массы груза, вылета и высоты, удалённости объекта и условий площадки. Напишите задачу и город — менеджер назовёт точную цену."],
    [/налич|безнал|оплат|перевод|счет|счёт|kaspi|каспи/, "Оплата наличными или безналичным расчётом. Порядок оплаты уточнит менеджер при заявке."],
    [/юр\.|юрлиц|юридич|компан|тоо|(^|\s)ип(\s|$)|организац|физлиц|физическ|частн|для себя/, "Работаем и с юридическими, и с физическими лицами — от разовой разгрузки у частного дома до работ на промышленных объектах."],
    [/договор|документ|акт|ндс|счет-фактур|эсф/, "По документам и закрывающим бумагам подскажет менеджер при заявке — напишите, что нужно вашей бухгалтерии."],
    [/выбр|какой кран|подобр|грузовысот|вылет|хватит|потянет|поднимет/, "Кран выбирают по грузовысотной таблице, а не по цифре в названии. Нужны: масса груза со стропами, расстояние от стоянки крана до точки установки и высота подъёма. Напишите эти данные — подберём класс с запасом."],
    [/площадк|грунт|выносн|подъезд|стоянк|подготов/, "Нужны ровная площадка под кран и выносные опоры, плотный грунт без свежей засыпки, свободный подъезд, без колодцев и траншей под опорами. Если рядом ЛЭП — сообщите заранее.", "/stati/podgotovka-ploshchadki/"],
    [/ппр|проект производств|наряд|допуск/, "Для сложных подъёмов, работ рядом с ЛЭП и на действующих предприятиях обычно нужен ППР. Подскажем, требуется ли он для вашей задачи."],
    [/лэп|провод|электролин/, "Работа вблизи ЛЭП выполняется только с соблюдением охранной зоны и по наряду-допуску. Сообщите о линии заранее — учтём при подборе стоянки крана."],
    [/город|регион|выезд|казахстан|межгород|другой город|перебаз|доставк/, "Работаем по всему Казахстану. Выезд в другой город включает перебазировку крана — сроки и стоимость называем при заявке."],
    [/sany|xcmg|zoomlion|сани|зумлион|марк|бренд|производ|модел/, "В парке техника SANY, XCMG и Zoomlion. Конкретную модель, длину стрелы и грузовысотную таблицу уточнит менеджер под вашу задачу."],
    [/стрел|высот|метр/, "Длину стрелы и высоту подъёма конкретного крана уточнит менеджер. Напишите, на какую высоту и на каком расстоянии от крана нужно поднять груз."],
    [/смен|(^|\s)(час|часа|часов)(\s|$)|почасов|сутк|долгосроч|недел|месяц|время работ|минимал/, "Время работы согласуем под задачу: разовый подъём, смена или весь этап работ. Минимальное время и порядок оплаты уточнит менеджер."],
    [/срочн|сегодня|завтра|когда приед|как быстро|выходн|ночь|ночью/, "Сроки подачи крана зависят от его занятости и удалённости объекта. Напишите дату, адрес и задачу — менеджер скажет, когда кран сможет приехать."],
    [/оператор|машинист|крановщик|стропал/, "По составу экипажа и стропальщикам подскажет менеджер при заявке."],
    [/металлоконстр|ферм|колонн|каркас|балк/, "Монтаж металлоконструкций — краны 50–100 тонн в зависимости от массы элементов и вылета.", "/uslugi/montazh-metallokonstrukciy/"],
    [/жби|плит|блок|фбс|ригел/, "Монтаж ЖБИ — обычно краны 50–80 тонн. Сообщите массу самой тяжёлой плиты и вылет.", "/uslugi/montazh-zhbi/"],
    [/разгруз|погруз|трал|длинномер|фур/, "Погрузка и разгрузка тяжёлых грузов, тралов и длинномеров — краны 50–100 тонн.", "/uslugi/razgruzka-tralov-i-dlinnomerov/"],
    [/контейнер/, "Погрузка и установка контейнеров 20 и 40 футов — краны 50 и 70 тонн.", "/uslugi/pogruzka-konteynerov/"],
    [/модул|бытовк|вагон/, "Разгрузка и установка блок-модулей и бытовок, в том числе в несколько ярусов.", "/uslugi/montazh-modulnyh-zdaniy/"],
    [/резервуар|емкост|ёмкост|цистерн|(^|\s)бак/, "Монтаж резервуаров и ёмкостей — краны 70–400 тонн, длинные ёмкости можно поднимать двумя кранами.", "/uslugi/montazh-rezervuarov/"],
    [/трансформатор|подстанц|ктп/, "Монтаж трансформаторов и энергооборудования — краны 50–100 тонн.", "/uslugi/montazh-transformatorov/"],
    [/кондиционер|чиллер|вентиляц|крыш|кровл/, "Подъём оборудования на крышу — рассчитаем вылет до точки установки.", "/uslugi/montazh-ventilyacii-i-kondicionerov/"],
    [/ветр|вэу|ветряк/, "Для подъёмов при монтаже ВЭУ есть кран 400 тонн, возможность конкретного подъёма проверяем по массе и высоте.", "/uslugi/vetroenergetika/"],
    [/(^|\s)мост|путепровод|эстакад/, "Мостовые конструкции — краны 80, 100 и 400 тонн.", "/uslugi/montazh-mostovyh-konstrukciy/"],
    [/нефт|газов|газопр|нпз|месторожд/, "Работаем на нефтегазовых объектах — краны 70–400 тонн.", "/uslugi/neftegazovye-obekty/"],
    [/ангар|склад/, "Монтаж ангаров и складов — краны 50–80 тонн.", "/uslugi/montazh-angarov-i-skladov/"],
    [/демонтаж|разобрать|снять/, "Демонтаж металлоконструкций, ЖБИ и оборудования с погрузкой на транспорт.", "/uslugi/demontazh/"],
    [/опор|столб|мачт|башн/, "Установка опор, мачт и башен — краны 50–100 тонн.", "/uslugi/montazh-opor-lep/"],
    [/(^|\s)бот|робот|ты кто|живой|человек/, "Я онлайн-консультант сайта. Живой менеджер ответит по телефону или в WhatsApp — кнопка ниже."],
    [/спасиб|рахмет|благодар/, "Пожалуйста! Если удобно, оставьте номер или напишите в WhatsApp — менеджер свяжется."],
    [/привет|здравств|салем|сәлем|добрый|ассалам/, "Здравствуйте! Подскажу по автокранам 50–400 тонн. Что нужно поднять и в каком городе?"]
  ];
  function local(q) {
    var s = low(q);
    if (s.replace(/\D/g, "").length >= 10) return { t: "Спасибо! Чтобы заявка точно дошла, отправьте номер менеджеру в WhatsApp кнопкой ниже." };
    var fl = KB.fleet || [];
    for (var i = 0; i < fl.length; i++) {
      if (new RegExp("(^|\\D)" + fl[i][0] + "(\\s*т|\\s*тонн|\\D|$)").test(s)) return { t: "Автокран " + fl[i][0] + " тонн есть в парке (" + fl[i][1] + "). Напишите массу груза, высоту и адрес — проверим, подходит ли этот класс, и назовём стоимость.", u: fl[i][2] };
    }
    var cs = KB.cities || [];
    for (var j = 0; j < cs.length; j++) {
      var n = low(cs[j][1]).slice(0, Math.max(4, cs[j][1].length - 2));
      if (s.indexOf(n) > -1) return { t: "Да, работаем " + cs[j][2] + ". Сроки подачи крана согласуем при заявке. Что нужно поднять?", u: cs[j][3] };
    }
    for (var k = 0; k < INTENTS.length; k++) if (INTENTS[k][0].test(s)) return { t: INTENTS[k][1], u: INTENTS[k][2] };
    var m = s.match(/(\d+[.,]?\d*)\s*(т|тонн)/);
    if (m) { var w = parseFloat(m[1].replace(",", ".")); var c = fl.filter(function (f) { return f[0] >= w * 2; })[0] || fl[fl.length - 1];
      return { t: "Для груза около " + w + " т кран подбирают с запасом по вылету — ориентир от " + c[0] + " тонн, точно скажет менеджер по грузовысотной таблице. Напишите вылет и высоту.", u: c[2] }; }
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
      .catch(function () { busy = false; wait.remove(); var r = local(q); hist.push({ role: "assistant", content: r.t }); reply(r); if (qbox) qbox.innerHTML = ""; });
  }
  function openChat() {
    chat.hidden = false; if (opener) opener.hidden = true;
    if (!started) { started = true; add("Здравствуйте! Я ИИ-консультант. Помогу подобрать автокран 50–400 тонн, подскажу по оплате, площадке и документам. Что нужно поднять и в каком городе?", "b"); quick(["Сколько стоит?", "Какой кран выбрать?", "Оплата и юрлица", "Работаете в моём городе?", "Подготовка площадки", "Кран 400 тонн"]); }
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
