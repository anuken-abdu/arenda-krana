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
