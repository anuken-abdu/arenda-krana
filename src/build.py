# -*- coding: utf-8 -*-
"""Генератор сайта аренды автокранов: python3 src/build.py → dist/"""
import html, json, re, shutil, sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from data import *

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
VER = "0311261800"
TODAY = date.today().isoformat()
E = lambda s: html.escape(str(s), quote=True)
PAGES = []

# ---------------------------------------------------------------- мелочи
def wa(text): return f"https://wa.me/{WA_NUMBER}?text=" + re.sub(r"\s", "%20", html.escape(text))
def wa_attr(text): return f'href="{wa(text)}" target="_blank" rel="noopener" data-wa="{E(text)}"'
def city_url(slug): return f"/goroda/{slug}/"
def fleet_url(f): return f"/avtokrany/{f['slug']}/"

ICON = {
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "wa": '<path d="M3.5 20.5l1.2-4.3A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 8.5c0 3 2.5 6.3 6 6.8l1.3-1.6-2-1-1 .9c-1-.5-2-1.5-2.4-2.5l.9-1-1-2z"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
 "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "close": '<path d="M6 6l12 12M18 6L6 18"/>',
 "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "hook": '<path d="M12 2v7"/><path d="M8.5 9h7v3h-7z"/><path d="M12 12v3a3.5 3.5 0 1 1-3.5 3.5"/>',
 "chev": '<path d="M6 9l6 6 6-6"/>',
 "send": '<path d="M4 12l16-8-6 16-2.5-6.5z"/>',
}
ICON.update({
 "ibeam": '<path d="M5 3.5h14v3.5h-5v10h5v3.5H5V17h5V7H5z"/>',
 "slab": '<path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M2.5 9.5v4L12 18l9.5-4.5v-4"/><path d="M7 12v2.5M12 14v2.5M17 12v2.5"/>',
 "load": '<path d="M12 2.5v6M9 5.5l3-3 3 3"/><rect x="5" y="11" width="14" height="7" rx="1"/><path d="M3 21h18M9 11v7M15 11v7"/>',
 "machine": '<rect x="3" y="9" width="12" height="10" rx="1.5"/><path d="M15 12h3.5l2.5 3v4h-6"/><circle cx="9" cy="14" r="2.6"/><path d="M6 9V6h6v3"/>',
 "tcrane": '<path d="M6 21V4M6 4h15M3 4h3M6 4l4 3.5M10 4v3M18 4v6"/><path d="M16.5 10h3v2.5h-3z"/><path d="M3 21h7M6 9h3M6 14h3"/>',
 "wind": '<path d="M12 11v10.5M9.5 21.5h5"/><circle cx="12" cy="9" r="1.6"/><path d="M12 7.4V2M13.4 9.9l4.8 2.8M10.6 9.9l-4.8 2.8"/>',
 "demol": '<path d="M3 21h18M5 21v-9h6v9M14 21v-5h5v5"/><path d="M14 3l6 6M20 3l-6 6"/>',
 "height": '<path d="M3 21V10l5-4 5 4v11M3 21h10"/><path d="M18 21V4M15 7l3-3 3 3"/><path d="M7 14h2M7 17h2"/>',
 "hangar": '<path d="M3 20.5V11a9 7 0 0 1 18 0v9.5"/><path d="M2 20.5h20M8 20.5V14h8v6.5M12 14v6.5"/>',
 "modules": '<rect x="2.5" y="12" width="9.5" height="7.5" rx=".8"/><rect x="12" y="12" width="9.5" height="7.5" rx=".8"/><rect x="7" y="4.5" width="10" height="7.5" rx=".8"/><path d="M5.5 15h3M15 15h3M10.5 7.5h3"/>',
 "tank": '<ellipse cx="12" cy="5.5" rx="7" ry="2.5"/><path d="M5 5.5v13c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-13M5 12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5"/>',
 "transf": '<rect x="5" y="9" width="14" height="11" rx="1.2"/><path d="M8.5 9V5.5M12 9V4M15.5 9V5.5M7 4.5h3M10.5 3h3M14 4.5h3M8.5 12.5v4.5M12 12.5v4.5M15.5 12.5v4.5"/>',
 "pylon": '<path d="M8.5 22L12 2l3.5 20"/><path d="M4 7h16M6 11.5h12M4 7v2.5M20 7v2.5M6 11.5V14M18 11.5V14M9.6 16h4.8M9 19.5l6-3.5M15 19.5l-6-3.5"/>',
 "bridge": '<path d="M2 15h20M4 15v5M20 15v5"/><path d="M2 9.5c3 0 5.5 5.5 10 5.5s7-5.5 10-5.5"/><path d="M7 12.6V15M12 15v0M17 12.6V15"/>',
 "hvac": '<rect x="2.5" y="6" width="19" height="13" rx="1.5"/><circle cx="9" cy="12.5" r="3.6"/><path d="M9 8.9v7.2M5.4 12.5h7.2M15.5 9.5h3M15.5 12.5h3M15.5 15.5h3"/>',
 "board": '<rect x="3" y="3.5" width="18" height="10" rx="1"/><path d="M8 13.5v8M16 13.5v8M5 21.5h14M7 7.5h10M7 10h6"/>',
 "mast": '<path d="M12 9v12.5M8.5 21.5L12 9l3.5 12.5M9.7 17h4.6"/><circle cx="12" cy="6.3" r="1.6"/><path d="M8.3 2.8a5.2 5.2 0 0 0 0 7M15.7 2.8a5.2 5.2 0 0 1 0 7"/>',
 "trailer": '<path d="M2 15.5h13.5l2-3h3.5l1 3v2H2z"/><rect x="4" y="9.5" width="9" height="6"/><circle cx="5.5" cy="18.5" r="1.6"/><circle cx="9.5" cy="18.5" r="1.6"/><circle cx="19" cy="18.5" r="1.6"/>',
 "container": '<rect x="2" y="6.5" width="20" height="12" rx="1"/><path d="M6 6.5v12M10 6.5v12M14 6.5v12M18 6.5v12"/>',
 "hookbox": '<path d="M12 2v4.5"/><path d="M10 6.5h4v2.2h-4z"/><path d="M12 8.7v1.8a2 2 0 1 1-2 2"/><rect x="5" y="15" width="14" height="6.5" rx="1"/><path d="M9 15l3-2.5 3 2.5"/>',
 "weight": '<path d="M5.5 10h13l3 11.5h-19z"/><path d="M9 10a3 3 0 1 1 6 0"/><path d="M10 14.5v4M10 16.5h2.5l1.5-2M12.5 16.5l1.5 2"/>',
 "derrick": '<path d="M8 21.5L12 2.5l4 19M9.6 14h4.8M10.6 9h2.8M4 21.5h16"/><path d="M9 18.5l5-4.5M15 18.5l-5-4.5"/>',
 "plant": '<path d="M3.5 21.5c1-4 1-8 0-12h6c-1 4-1 8 0 12M13.5 21.5c1-4 1-8 0-12h6c-1 4-1 8 0 12M2 21.5h20"/><path d="M6 6.5c0-1.5 1.5-1.5 1.5-3M16 6.5c0-1.5 1.5-1.5 1.5-3"/>',
 "factory": '<path d="M2 21V11l6 4V11l6 4V7l8 4v10z"/><path d="M6 21v-3M11 21v-3M16 21v-3"/>',
 "road": '<path d="M8.5 3L4 21M15.5 3L20 21M12 4.5v3M12 10.5v3M12 16.5v3"/>',
 "silo": '<path d="M3.5 21V8a3 3 0 0 1 6 0v13M9.5 21V8a3 3 0 0 1 6 0v13M15.5 21v-9h5v9M2 21h20"/>',
 "legal": '<path d="M3 21h18M5 21V9h14v12M9 21v-4h6v4M8 12h2M14 12h2M12 3l9 6H3z"/>',
 "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.5 4.2-6.5 8-6.5s7 2 8 6.5"/>',
 "cash": '<rect x="2.5" y="6" width="19" height="12" rx="1.5"/><circle cx="12" cy="12" r="3"/><path d="M6 9.5v5M18 9.5v5"/>',
 "card": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M2.5 9.5h19M6 15h4"/>',
 "spark": '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M18.5 15l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
})
def ui(n, cls="ui"): return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[n]}</g></svg>'

def logo(dark=False):
    src = "/assets/art/logo-crane-w.svg" if dark else "/assets/art/logo-crane.svg"
    return (f'<a class="logo" href="/" aria-label="{BRAND} — на главную"><span class="logo-m"><img src="{src}" alt="" width="54" height="38"></span>'
            f'<span class="logo-t">АРЕНДА<b>КРАНА</b><small>.kz · автокраны 50–400 т</small></span></a>')

def photo(src, alt, label, cls="ph"):
    """Слот под фото: если файла нет — аккуратная заглушка с подписью, без поломанной картинки."""
    return (f'<div class="{cls}"><span class="ph-l">{label}</span>'
            f'<img src="{src}?v={VER}" alt="{E(alt)}" loading="lazy" onerror="this.remove()"></div>')

def clients_html():
    return '<div class="cli">' + "".join(f'<div><span class="cli-i">{ui(i)}</span><b>{E(t)}</b><p>{E(d)}</p></div>' for i, t, d in CLIENTS) + "</div>"

def btns(msg, light=False):
    return (f'<div class="btns"><a class="btn btn-y" href="tel:{PHONE_TEL}" data-call>{ui("phone")}Позвонить</a>'
            f'<a class="btn {"btn-l" if light else "btn-o"}" {wa_attr(msg)}>{ui("wa")}WhatsApp</a></div>')

def sec(title, inner, sub="", alt=False, sid="", link=None):
    lk = f'<a class="lnk" href="{link[1]}">{link[0]} {ui("arrow")}</a>' if link else ""
    return (f'<section class="sec{" sec-alt" if alt else ""}"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}><div class="wrap">'
            f'<div class="sec-h"><div><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>{lk}</div>{inner}</div></section>')

# ---------------------------------------------------------------- блоки
def fleet_cards(cin=""):
    out = []
    for f in FLEET:
        tasks = "".join(f"<li>{ui('check')}{E(t)}</li>" for t in f["tasks"][:3])
        out.append(f'''<article class="fc">{photo(f"/images/tehnika/{f['slug']}.jpg", f"Автокран {f['t']} тонн", f"{f['t']} т")}
<div class="fc-b"><div class="fc-t"><b>{f['t']}<span>тонн</span></b><em>в парке: {units(f['n'])}</em></div>
<h3><a href="{fleet_url(f)}">Автокран {f['t']} тонн{(' ' + cin) if cin else ''}</a></h3><ul class="ticks">{tasks}</ul>
<a class="lnk" href="{fleet_url(f)}">Подробнее {ui("arrow")}</a></div></article>''')
    return '<div class="fleet">' + "".join(out) + "</div>"

def svc_cards(items=None):
    items = items or SERVICES
    return '<div class="svc">' + "".join(
        f'<a class="sv" href="/uslugi/{s["slug"]}/"><span class="sv-i">{ui(s["ic"])}</span><b>{E(s["name"])}</b><span>{E(s["short"])}</span>'
        f'<small>{" · ".join(f"{t} т" for t in s["fit"])}</small>{ui("arrow", "ui sv-a")}</a>' for s in items) + "</div>"

def cat_blocks():
    """Три направления услуг со ссылками на все страницы — для главной и городов."""
    out = []
    for key, name, desc in SERVICE_CATS:
        items = [s for s in SERVICES if s["cat"] == key]
        li = "".join(f'<li><a href="/uslugi/{s["slug"]}/">{ui(s["ic"])}{E(s["name"])}</a></li>' for s in items)
        out.append(f'<div class="cat"><div class="cat-h"><b>{name}</b><span>{desc}</span></div><ul>{li}</ul></div>')
    return '<div class="cats">' + "".join(out) + "</div>"

def brands_strip():
    return '<ul class="brands">' + "".join(f"<li>{b}</li>" for b in BRANDS) + "</ul>"

def steps_html():
    return '<ol class="steps">' + "".join(f'<li><span>{i}</span><b>{E(t)}</b><p>{E(d)}</p></li>' for i, (t, d) in enumerate(STEPS, 1)) + "</ol>"

def factors_html():
    return '<div class="fac">' + "".join(f'<div><b>{E(t)}</b><p>{E(d)}</p></div>' for t, d in PRICE_FACTORS) + "</div>"

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)}{ui("chev")}</summary><p>{E(a)}</p></details>' for q, a in faq) + "</div>"

def cities_html(cur=""):
    return '<ul class="chips">' + "".join(f'<li><a href="{city_url(c[0])}"{" class=cur" if c[0] == cur else ""}>{c[1]}</a></li>' for c in CITIES) + "</ul>"

def lead_form(title="Подберём автокран под вашу задачу", city=""):
    tons = "".join(f'<option>{f["t"]} тонн</option>' for f in FLEET)
    copts = "".join(f'<option{" selected" if c[0] == city else ""}>{c[1]}</option>' for c in CITIES)
    return f'''<section class="sec sec-dark" id="zayavka"><div class="wrap lead">
<div><h2>{title}</h2><p>Напишите массу груза, высоту и адрес объекта — подберём кран нужного класса и назовём стоимость. Заявка откроется в WhatsApp с заполненными данными.</p>
<div class="lead-c"><a href="tel:{PHONE_TEL}" data-call>{ui("phone")}{PHONE_DISPLAY}</a></div></div>
<form class="form" data-lead novalidate>
<div class="fld"><label for="fN">Имя</label><input id="fN" name="name" autocomplete="name"></div>
<div class="fld"><label for="fP">Телефон</label><input id="fP" name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="+7"></div>
<div class="fld"><label for="fC">Город</label><select id="fC" name="city">{copts}</select></div>
<div class="fld"><label for="fT">Грузоподъёмность</label><select id="fT" name="ton"><option>Нужна консультация</option>{tons}</select></div>
<div class="fld fld-w"><label for="fM">Задача</label><textarea id="fM" name="msg" rows="3" placeholder="Что поднимаем, масса, высота, сроки"></textarea></div>
<p class="f-err" hidden>Укажите телефон, чтобы мы могли связаться.</p>
<button class="btn btn-y fld-w" type="submit">{ui("wa")}Отправить в WhatsApp</button>
<p class="f-note fld-w">Нажимая кнопку, вы соглашаетесь с <a href="/privacy-policy/">политикой конфиденциальности</a>.</p></form></div></section>'''

def geo_sec(slug=None):
    if slug:
        c = next(x for x in CITIES if x[0] == slug)
        title, areas, note = CITY_AREAS.get(slug, (f"{c[1]}: где работаем", GEN_ALL, f"Выезжаем по всему городу и по региону: {c[3]}."))
        chips = '<ul class="chips chips-s">' + "".join(f"<li>{E(a)}</li>" for a in areas) + "</ul>"
        left = f'<div><h3>{E(title)}</h3><p>{E(note)} Подачу крана на объект согласуем при заявке.</p>{chips}</div>'
    else:
        left = '<div><h3>По всему Казахстану</h3><p>Работаем в городах и регионах республики. Выезд в другой город включает перебазировку крана — сроки и стоимость называем при заявке.</p></div>'
    return sec("География работы", f'<div class="geo">{left}<div><h3>Города</h3>{cities_html(slug or "")}</div></div>', alt=True, sid="goroda")

def article_cards():
    return '<div class="arts">' + "".join(f'<a class="art" href="/stati/{a["slug"]}/"><b>{E(a["title"])}</b><span>{E(a["desc"])}</span>{ui("arrow")}</a>' for a in ARTICLES) + "</div>"

def crumbs_html(cr):
    items = [("Главная", "/")] + cr
    li = "".join(f'<li><a href="{u}">{E(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{E(n)}</li>' for i, (n, u) in enumerate(items))
    return f'<nav class="crumbs" aria-label="Навигация"><ol>{li}</ol></nav>'

def ph_hero(h1, lead, crumbs, msg, extra=""):
    return f'''<section class="phd"><div class="wrap">{crumbs_html(crumbs)}<div class="phd-in"><div><h1>{h1}</h1><p class="lead-t">{lead}</p>{btns(msg, light=True)}</div>{extra}</div></div></section>'''

# ---------------------------------------------------------------- schema
ORG = {"@type": "Organization", "@id": SITE_URL + "/#org", "name": BRAND, "url": SITE_URL + "/", "telephone": PHONE_TEL,
       "logo": SITE_URL + "/assets/icon-512.png", "areaServed": {"@type": "Country", "name": "Казахстан"},
       "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_TEL, "contactType": "customer service", "availableLanguage": ["ru", "kk"]}}
def service_schema(name, url, desc, city=None):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": "Аренда автокрана", "url": SITE_URL + url,
            "description": desc, "provider": {"@id": SITE_URL + "/#org"},
            "areaServed": {"@type": "City", "name": city} if city else {"@type": "Country", "name": "Казахстан"}, "brand": [{"@type": "Brand", "name": b} for b in BRANDS]}
def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

# ---------------------------------------------------------------- страница
def nav_html():
    fl = "".join(f'<li><a href="{fleet_url(f)}">Автокран {f["t"]} тонн</a></li>' for f in FLEET)
    sv = "".join(f'<li><a href="/uslugi/#{k}">{n}</a></li>' for k, n, _ in SERVICE_CATS)
    return f'''<nav class="nav" id="nav" aria-label="Меню"><ul>
<li class="has"><a href="/avtokrany/">Автокраны</a><ul class="sub">{fl}</ul></li>
<li class="has"><a href="/uslugi/">Услуги</a><ul class="sub">{sv}</ul></li><li><a href="/goroda/">Города</a></li><li><a href="/stati/">Статьи</a></li>
<li><a href="/o-kompanii/">О компании</a></li><li><a href="/kontakty/">Контакты</a></li></ul>
<div class="nav-m">{btns("Здравствуйте! Нужен автокран.")}</div></nav>'''

def gtag():
    ids = [x for x in (GA_ID, GADS_ID) if x]
    if not ids: return ""
    cfg = "".join(f"gtag('config','{x}');" for x in ids)
    return f'<script async src="https://www.googletagmanager.com/gtag/js?id={ids[0]}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());{cfg}</script>'

def page(path, title, desc, body, schemas=(), crumbs=None, prio="0.7", kw=""):
    PAGES.append((path, prio, title, kw))
    bc = []
    if crumbs:
        items = [("Главная", "/")] + crumbs
        bc = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(items)]}]
    org = {"@context": "https://schema.org", **ORG}
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in [org, *schemas, *bc])
    cfg = json.dumps({"ga": GA_ID, "ads": GADS_ID, "call": GADS_CALL_LABEL, "wa": GADS_WA_LABEL, "wan": WA_NUMBER}, ensure_ascii=False)
    doc = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_KZ"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:image" content="{SITE_URL}/assets/og.png"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0d0c">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.png" type="image/png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/onest-cyrillic-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/unbounded-cyrillic-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/styles.css?v={VER}">
{ld}{gtag()}
</head>
<body>
<a class="skip" href="#main">К содержимому</a>
<header class="hdr"><div class="wrap hdr-in">{logo()}{nav_html()}
<div class="hdr-c"><a class="hdr-ph" href="tel:{PHONE_TEL}" data-call>{PHONE_DISPLAY}<small>по всему Казахстану</small></a>
<a class="hdr-call" href="tel:{PHONE_TEL}" data-call aria-label="Позвонить {PHONE_DISPLAY}">{ui("phone")}</a>
<a class="btn btn-y btn-s hdr-wa" {wa_attr("Здравствуйте! Нужен автокран.")}>{ui("wa")}WhatsApp</a>
<button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="nav">{ui("menu")}{ui("close", "ui ui-x")}</button></div></div></header>
<main id="main">
{body}
</main>
<footer class="ftr"><div class="wrap ftr-g">
<div>{logo(True)}<p>Аренда автокранов 50, 70, 80, 100 и 400 тонн по всему Казахстану. Работаем с юридическими и физическими лицами, наличный и безналичный расчёт. Техника {", ".join(BRANDS)}.</p>
<a class="ftr-ph" href="tel:{PHONE_TEL}" data-call>{PHONE_DISPLAY}</a></div>
<div><h4>Автокраны</h4><ul>{"".join(f'<li><a href="{fleet_url(f)}">{f["t"]} тонн</a></li>' for f in FLEET)}</ul></div>
<div><h4>Услуги</h4><ul>{"".join(f'<li><a href="/uslugi/{s["slug"]}/">{E(s["name"])}</a></li>' for s in SERVICES[:6])}</ul></div>
<div><h4>Компания</h4><ul><li><a href="/o-kompanii/">О компании</a></li><li><a href="/goroda/">Города</a></li><li><a href="/stati/">Статьи</a></li><li><a href="/kontakty/">Контакты</a></li><li><a href="/privacy-policy/">Политика конфиденциальности</a></li></ul></div>
</div><div class="wrap ftr-b"><span>© {date.today().year} {BRAND}. Информация на сайте не является публичной офертой.</span>
<a href="{DEV[1]}" target="_blank" rel="noopener">Разработка сайта — {DEV[0]}</a></div></footer>
<div class="fab"><button class="fab-b" type="button" data-back aria-label="Назад" title="Назад">{ui("back")}</button><button class="fab-b" type="button" data-top aria-label="Наверх" title="Наверх">{ui("up")}</button></div>
<button class="chat-o" type="button" data-chat aria-label="ИИ-консультант"><span class="chat-o-i">{ui("spark")}</span><span class="chat-o-t">ИИ-консультант<small>ответит за минуту</small></span></button>
<div class="chat" id="chat" hidden role="dialog" aria-label="Онлайн-консультант"><div class="chat-h"><b>{BRAND}<small>онлайн-консультант</small></b><button type="button" data-chat-x aria-label="Закрыть чат">{ui("close")}</button></div>
<div class="chat-l" aria-live="polite"></div><div class="chat-q"></div>
<form class="chat-f"><input name="q" autocomplete="off" placeholder="Напишите вопрос" aria-label="Ваш вопрос"><button type="submit" aria-label="Отправить">{ui("send")}</button></form>
<a class="chat-wa" {wa_attr("Здравствуйте! Пишу с сайта, нужен автокран.")}>{ui("wa")}Продолжить в WhatsApp</a></div>
<script>window.CFG={cfg};</script>
<script src="/assets/app.js?v={VER}" defer></script>
</body></html>'''
    out = DIST / path.strip("/") / "index.html" if path != "/404" else DIST / "404.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")

# ---------------------------------------------------------------- страницы
def build_home():
    tons = "".join(f'<li><a href="{fleet_url(f)}"><b>{f["t"]}</b><span>тонн</span></a></li>' for f in FLEET)
    body = f'''<section class="hero"><div class="wrap hero-in"><div class="hero-t">
<p class="eyebrow">{" · ".join(BRANDS)}</p>
<h1>Аренда автокранов <em>50–400 тонн</em> по всему Казахстану</h1>
<p class="lead-t">Монтаж металлоконструкций и ЖБИ, погрузка и разгрузка, установка промышленного оборудования и сверхтяжёлые подъёмы. Подбираем кран по массе груза, вылету и высоте — с запасом по грузовысотной таблице.</p>
{btns("Здравствуйте! Нужен автокран.", light=True)}</div>
<div class="hero-v"><div class="hero-art"><img src="/assets/art/crane-lines.webp?v={VER}" alt="" width="1600" height="892" fetchpriority="high"><img class="hero-ph" src="/images/hero.jpg?v={VER}" alt="Автокран на объекте" onerror="this.remove()"></div><ul class="tons">{tons}</ul></div></div>
<div class="wrap">{brands_strip()}</div></section>
{sec("Автокраны в парке", fleet_cards(), "Пять классов грузоподъёмности — от монтажа на стройке до сверхтяжёлых промышленных подъёмов.", sid="park", link=("Все автокраны", "/avtokrany/"))}
{sec("Услуги автокрана", cat_blocks(), "Под каждую задачу — подходящий класс крана. Выберите работу, чтобы узнать подробности.", alt=True, link=("Все услуги", "/uslugi/"))}
{sec("Как мы работаем", steps_html())}
{sec("Работаем с компаниями и частными клиентами", clients_html(), "Юридические и физические лица, оплата наличными или безналичным расчётом.", alt=True)}
{sec("От чего зависит стоимость", factors_html(), "Цену называем после уточнения задачи — так вы платите за подходящий кран, а не за лишний тоннаж.")}
{geo_sec()}
{sec("Полезно знать", article_cards(), link=("Все статьи", "/stati/"))}
{sec("Частые вопросы", faq_html(FAQ), alt=True)}
{lead_form()}'''
    page("/", f"Аренда автокрана 50–400 тонн по всему Казахстану — {BRAND}",
         "Аренда автокранов SANY, XCMG, Zoomlion грузоподъёмностью 50, 70, 80, 100 и 400 тонн по всему Казахстану: монтаж, погрузка, промышленные подъёмы.",
         body, [service_schema("Аренда автокранов 50–400 тонн", "/", "Аренда автокранов грузоподъёмностью 50, 70, 80, 100 и 400 тонн по всему Казахстану."), faq_schema(FAQ)],
         prio="1.0", kw="главная аренда автокрана")

def build_fleet():
    body = f'''{ph_hero("Автокраны 50, 70, 80, 100 и 400 тонн", f"Техника {', '.join(BRANDS)}. Подберём класс по массе груза, вылету и высоте подъёма.", [("Автокраны", "/avtokrany/")], "Здравствуйте! Нужен автокран, помогите подобрать.")}
{sec("Парк техники", fleet_cards())}{sec("Как выбрать грузоподъёмность", f'<div class="prose"><p>{E(FAQ[3][1])}</p></div>', alt=True)}{lead_form()}'''
    page("/avtokrany/", f"Автокраны 50–400 тонн в аренду — парк техники {BRAND}", f"Парк автокранов {', '.join(BRANDS)}: 50, 70, 80, 100 и 400 тонн. Аренда по всему Казахстану.",
         body, crumbs=[("Автокраны", "/avtokrany/")], prio="0.9", kw="автокраны парк техники")
    for f in FLEET:
        url = fleet_url(f); t = f["t"]
        fit = [s for s in SERVICES if t in s["fit"]]
        others = [x for x in FLEET if x is not f]
        tasks = "".join(f"<li>{ui('check')}{E(x)}</li>" for x in f["tasks"])
        faq = [(f"Сколько автокранов {t} тонн в парке?", f"В парке {units(f['n'])} грузоподъёмностью {t} тонн. Технику подбираем под дату и объект."),
               (f"Сколько стоит аренда автокрана {t} тонн?", "Стоимость зависит от времени работы, массы груза, вылета и высоты, удалённости объекта и условий площадки. Назовём цену после уточнения задачи."),
               (f"Поднимет ли кран {t} тонн груз массой {t} тонн?", f"Только на минимальном вылете стрелы. С ростом вылета и высоты допустимая масса снижается по грузовысотной таблице. Сообщите массу, расстояние до точки установки и высоту — проверим, подходит ли {t}-тонный кран или нужен класс выше."),
               ("Работаете в других городах?", "Да, по всему Казахстану. Выезд в другой город включает перебазировку крана — сроки и стоимость называем при заявке.")]
        sib = "".join(f'<li><a href="{fleet_url(x)}">Автокран {x["t"]} тонн</a></li>' for x in others)
        body = f'''{ph_hero(f"Аренда автокрана {t} тонн", E(f["text"]), [("Автокраны", "/avtokrany/"), (f"{t} тонн", url)], f"Здравствуйте! Нужен автокран {t} тонн.",
               photo(f"/images/tehnika/{f['slug']}.jpg", f"Автокран {t} тонн", f"{t} т", "ph ph-side"))}
<section class="sec"><div class="wrap two"><div><h2>Для каких работ</h2><ul class="ticks ticks-l">{tasks}</ul></div>
<div class="specs"><div><span>Грузоподъёмность</span><b>{t} тонн</b></div><div><span>В парке</span><b>{units(f['n'])}</b></div><div><span>Производители техники</span><b>{", ".join(BRANDS)}</b></div><div><span>География</span><b>Вся Республика Казахстан</b></div>
<p class="specs-n">Длину стрелы, вылет и грузовысотную таблицу конкретного крана уточняйте у менеджера под вашу задачу.</p></div></div></section>
{sec("Услуги с этим краном", svc_cards(fit), alt=True) if fit else ""}
{sec("Другие классы", f'<ul class="chips">{sib}</ul>')}
{geo_sec()}
{sec("Вопросы", faq_html(faq), alt=True)}
{lead_form(f"Заказать автокран {t} тонн")}'''
        page(url, f"Аренда автокрана {t} тонн по всему Казахстану — {BRAND}",
             f"Автокран {t} тонн в аренду: {f['tasks'][0].lower()}, {f['tasks'][1].lower()}. В парке {units(f['n'])}, техника {', '.join(BRANDS)}. Работаем по всему Казахстану.",
             body, [service_schema(f"Аренда автокрана {t} тонн", url, f["text"]), faq_schema(faq)], crumbs=[("Автокраны", "/avtokrany/"), (f"{t} тонн", url)], prio="0.9", kw=f"автокран {t} тонн")

def build_services():
    body = f'''{ph_hero("Услуги автокрана", "Монтаж, погрузка, подъём на высоту и сверхтяжёлые подъёмы — подбираем класс крана под задачу.", [("Услуги", "/uslugi/")], "Здравствуйте! Нужны услуги автокрана.")}
{"".join(sec(n, svc_cards([x for x in SERVICES if x["cat"] == k]), d, alt=i % 2 == 1, sid=k) for i, (k, n, d) in enumerate(SERVICE_CATS))}{lead_form()}'''
    page("/uslugi/", f"Услуги автокрана по всему Казахстану — {BRAND}", "Монтаж металлоконструкций и ЖБИ, погрузка и разгрузка, монтаж оборудования, демонтаж и подъём грузов на высоту автокранами 50–400 тонн.",
         body, crumbs=[("Услуги", "/uslugi/")], prio="0.8", kw="услуги")
    for s in SERVICES:
        url = f"/uslugi/{s['slug']}/"
        fl = [f for f in FLEET if f["t"] in s["fit"]]
        pts = "".join(f"<li>{ui('check')}{E(p)}</li>" for p in s["points"])
        tons = "".join(f'<li><a href="{fleet_url(f)}"><b>{f["t"]} т</b><span>{units(f["n"])}</span></a></li>' for f in fl)
        body = f'''{ph_hero(E(s["name"]) + " автокраном", E(s["text"]), [("Услуги", "/uslugi/"), (s["name"], url)], f"Здравствуйте! Нужен автокран: {s['name'].lower()}.")}
<section class="sec"><div class="wrap two"><div><h2>Как работаем</h2><ul class="ticks ticks-l">{pts}</ul></div><div><h2>Подходящие краны</h2><ul class="tons tons-l">{tons}</ul></div></div></section>
{sec("Похожие услуги", svc_cards(([x for x in SERVICES if x["cat"] == s["cat"] and x is not s] + [x for x in SERVICES if x["cat"] != s["cat"]])[:4]), alt=True, link=("Все услуги", "/uslugi/"))}
{sec("Частые вопросы", faq_html(FAQ[2:6]))}
{lead_form()}'''
        page(url, f"{s['name']} автокраном по всему Казахстану — {BRAND}", f"{s['text'][:150].rstrip(',. ')}. Автокраны {', '.join(str(f['t']) for f in fl)} тонн.",
             body, [service_schema(s["name"], url, s["text"])], crumbs=[("Услуги", "/uslugi/"), (s["name"], url)], prio="0.7", kw=s["name"].lower())

def build_cities():
    for slug, name, cin, region in CITIES:
        url = city_url(slug)
        note = CITY_NOTE.get(slug)
        intro = (f"{name} — {note}. " if note else "") + f"Автокраны 50, 70, 80, 100 и 400 тонн {cin} и по региону ({region}): монтаж, погрузка, промышленные подъёмы."
        faq = [(f"Работаете ли вы {cin}?", f"Да. Подаём автокраны {cin} и по региону: {region}. Сроки подачи и перебазировки называем при заявке."),
               (f"Сколько стоит аренда автокрана {cin}?", "Стоимость зависит от грузоподъёмности, времени работы, массы груза, вылета и высоты, а также от того, нужна ли перебазировка крана. Назовём цену после уточнения задачи."),
               (f"Какой автокран заказать {cin}?", "Сообщите массу груза, расстояние от стоянки крана до точки установки и высоту — подберём класс из парка 50, 70, 80, 100 и 400 тонн.")]
        cfaq = faq + [x for x in FAQ if x[0] not in {q for q, _ in faq} and "по всему Казахстану" not in x[0]]
        body = f'''{ph_hero(f"Аренда автокрана {cin}", E(intro), [("Города", "/goroda/"), (name, url)], f"Здравствуйте! Нужен автокран, город {name}.")}
{sec(f"Автокраны {cin}", fleet_cards(cin), "Выберите класс по массе груза и высоте подъёма.")}
{sec("Услуги", cat_blocks(), alt=True)}
{sec("Как мы работаем", steps_html())}
{sec("Юр. и физ. лица, нал и безнал", clients_html(), alt=True)}
{geo_sec(slug)}
{sec("Частые вопросы", faq_html(cfaq))}
{lead_form(f"Заказать автокран {cin}", slug)}'''
        page(url, f"Аренда автокрана {cin} — 50, 70, 80, 100, 400 тонн | {BRAND}",
             f"Аренда автокранов {cin}: 50, 70, 80, 100 и 400 тонн, техника {', '.join(BRANDS)}. Монтаж, погрузка, промышленные подъёмы. {region}.",
             body, [service_schema(f"Аренда автокрана {cin}", url, intro, city=name), faq_schema(cfaq)], crumbs=[("Города", "/goroda/"), (name, url)], prio="0.8", kw=f"{name} {cin}")
    body = f'''{ph_hero("Работаем по всему Казахстану", "Выберите город — на странице условия работы, классы кранов и районы выезда.", [("Города", "/goroda/")], "Здравствуйте! Нужен автокран в мой город.")}
{sec("Города", cities_html())}{lead_form()}'''
    page("/goroda/", f"Аренда автокранов по городам Казахстана — {BRAND}", "Аренда автокранов 50–400 тонн в Алматы, Астане, Шымкенте, Караганде, Актобе, Атырау и других городах Казахстана.",
         body, crumbs=[("Города", "/goroda/")], prio="0.8", kw="города")

def build_articles():
    for a in ARTICLES:
        url = f"/stati/{a['slug']}/"
        parts = []
        for t, x in a["body"]:
            parts.append("<ul>" + "".join(f"<li>{E(i)}</li>" for i in x) + "</ul>" if t == "ul" else f"<{t}>{E(x)}</{t}>")
        body = f'''<section class="phd phd-s"><div class="wrap">{crumbs_html([("Статьи", "/stati/"), (a["title"], url)])}<h1>{E(a["title"])}</h1><p class="lead-t">{E(a["desc"])}</p></div></section>
<section class="sec"><div class="wrap"><article class="prose">{"".join(parts)}{btns("Здравствуйте! Прочитал статью на сайте, нужен автокран.")}</article></div></section>
{sec("Другие статьи", article_cards(), alt=True)}{lead_form()}'''
        sch = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": TODAY, "dateModified": TODAY,
               "author": {"@id": SITE_URL + "/#org"}, "publisher": {"@id": SITE_URL + "/#org"}, "mainEntityOfPage": SITE_URL + url, "inLanguage": "ru"}
        page(url, f"{a['title']} — {BRAND}", a["desc"], body, [sch], crumbs=[("Статьи", "/stati/"), (a["title"], url)], prio="0.6", kw="статья")
    body = f'''{ph_hero("Статьи", "Как выбрать автокран, подготовить площадку и спланировать сверхтяжёлый подъём.", [("Статьи", "/stati/")], "Здравствуйте! Есть вопрос по автокрану.")}
{sec("Все статьи", article_cards())}'''
    page("/stati/", f"Статьи об аренде автокранов — {BRAND}", "Как выбрать автокран по грузоподъёмности, подготовить площадку и заказать кран 400 тонн.", body, crumbs=[("Статьи", "/stati/")], prio="0.6", kw="статьи")

def build_misc():
    park = "".join(f'<li><a href="{fleet_url(f)}"><b>{f["t"]} т</b><span>{units(f["n"])}</span></a></li>' for f in FLEET)
    body = f'''{ph_hero(f"О компании {BRAND}", f"Аренда автокранов 50–400 тонн по всему Казахстану. Техника {', '.join(BRANDS)}.", [("О компании", "/o-kompanii/")], "Здравствуйте! Нужен автокран.")}
<section class="sec"><div class="wrap two"><div class="prose"><h2>Чем занимаемся</h2><p>Сдаём в аренду автокраны пяти классов грузоподъёмности — 50, 70, 80, 100 и 400 тонн — для строительства, промышленного монтажа, погрузки и сверхтяжёлых подъёмов.</p><p>Работаем по всему Казахстану: от городских строек до промышленных и энергетических объектов в регионах. Кран подбираем под задачу — по массе груза, вылету и высоте подъёма.</p></div>
<div><h2>Парк техники</h2><ul class="tons tons-l">{park}</ul></div></div></section>
{sec("Как мы работаем", steps_html(), alt=True)}{sec("Клиенты и оплата", clients_html())}{lead_form()}'''
    page("/o-kompanii/", f"О компании {BRAND} — аренда автокранов", f"{BRAND}: аренда автокранов 50, 70, 80, 100 и 400 тонн, техника {', '.join(BRANDS)}, работа по всему Казахстану.", body, crumbs=[("О компании", "/o-kompanii/")], prio="0.5", kw="о компании")
    body = f'''{ph_hero("Контакты", "Позвоните или напишите в WhatsApp — подберём кран и назовём стоимость.", [("Контакты", "/kontakty/")], "Здравствуйте! Нужен автокран.")}
<section class="sec"><div class="wrap cont"><div><span>Телефон и WhatsApp</span><a href="tel:{PHONE_TEL}" data-call>{PHONE_DISPLAY}</a></div><div><span>Клиенты и оплата</span><b>Юр. и физ. лица, нал и безнал</b></div><div><span>Написать</span><a {wa_attr("Здравствуйте! Нужен автокран.")}>WhatsApp</a></div></div></section>
{geo_sec()}{lead_form()}'''
    page("/kontakty/", f"Контакты {BRAND} — аренда автокранов", f"Телефон и WhatsApp {PHONE_DISPLAY}. Аренда автокранов 50–400 тонн по всему Казахстану.", body, crumbs=[("Контакты", "/kontakty/")], prio="0.6", kw="контакты телефон")
    body = f'''<section class="phd phd-s"><div class="wrap">{crumbs_html([("Политика конфиденциальности", "/privacy-policy/")])}<h1>Политика конфиденциальности</h1></div></section>
<section class="sec"><div class="wrap"><div class="prose"><p>Сайт {SITE_URL.replace("https://", "")} не хранит персональные данные на своих серверах. Имя, телефон и описание задачи из формы заявки передаются в WhatsApp только после того, как вы сами нажмёте кнопку отправки.</p>
<p>Для статистики посещений могут использоваться сервисы Google Analytics и Google Ads, которые обрабатывают обезличенные данные о посещении сайта. Вопросы о данных можно задать по телефону {PHONE_DISPLAY}.</p></div></div></section>'''
    page("/privacy-policy/", f"Политика конфиденциальности — {BRAND}", "Как сайт обрабатывает данные из формы заявки и статистику посещений.", body, crumbs=[("Политика конфиденциальности", "/privacy-policy/")], prio="0.2", kw="политика конфиденциальности")
    body = f'''<section class="phd"><div class="wrap"><h1>Страница не найдена</h1><p class="lead-t">Возможно, адрес изменился. Перейдите на главную или выберите автокран.</p>
<div class="btns"><a class="btn btn-y" href="/">На главную</a><a class="btn btn-l" href="/avtokrany/">Автокраны</a></div></div></section>'''
    page("/404", f"Страница не найдена — {BRAND}", "Страница не найдена.", body, prio="0")

# ---------------------------------------------------------------- служебные файлы
def build_files():
    PAGES[:] = [p for p in PAGES if p[0] != "/404"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>" for u, p, *_ in PAGES]
    (DIST / "sitemap.xml").write_text("\n".join(sm + ["</urlset>"]), encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "YandexBot", "Bingbot"]
    (DIST / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    llms = [f"# {BRAND} — аренда автокранов по всему Казахстану", "",
            f"> Аренда автокранов грузоподъёмностью 50, 70, 80, 100 и 400 тонн. Техника {', '.join(BRANDS)}. Работа по всему Казахстану.", "",
            f"- Телефон и WhatsApp: {PHONE_DISPLAY}", f"- Сайт: {SITE_URL}/", "",
            "## Парк техники"] + [f"- Автокран {f['t']} тонн — {units(f['n'])}: {SITE_URL}{fleet_url(f)}" for f in FLEET] + [
            "", "## Услуги"] + [f"- {s['name']} ({', '.join(str(t) for t in s['fit'])} т): {SITE_URL}/uslugi/{s['slug']}/" for s in SERVICES] + [
            "", "## Стоимость", "- Цена зависит от грузоподъёмности, массы груза, вылета и высоты, времени работы, удалённости объекта и условий площадки; называется после уточнения задачи.",
            "", "## Города"] + [f"- {c[1]}: {SITE_URL}{city_url(c[0])}" for c in CITIES] + [
            "", "## Частые вопросы"] + [f"- {q} {a}" for q, a in FAQ] + ["", "## Статьи"] + [f"- {a['title']}: {SITE_URL}/stati/{a['slug']}/" for a in ARTICLES]
    (DIST / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    (DIST / "site.webmanifest").write_text(json.dumps({"name": f"{BRAND} — аренда автокранов", "short_name": BRAND, "start_url": "/", "display": "standalone",
        "background_color": "#0b0d0c", "theme_color": "#0b0d0c", "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
    # ассеты и база знаний для чата
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)
    css = (ROOT / "src" / "fonts.css").read_text(encoding="utf-8") + (ROOT / "src" / "styles.css").read_text(encoding="utf-8")
    (DIST / "assets" / "styles.css").write_text(css, encoding="utf-8")
    kb = {"phone": PHONE_DISPLAY, "fleet": [[f["t"], units(f["n"]), fleet_url(f)] for f in FLEET], "brands": BRANDS,
          "cities": [[c[0], c[1], c[2], city_url(c[0])] for c in CITIES], "faq": FAQ, "services": [[s["name"], f"/uslugi/{s['slug']}/", s["fit"]] for s in SERVICES]}
    js = (ROOT / "src" / "app.js").read_text(encoding="utf-8").replace("/*__KB__*/{}", json.dumps(kb, ensure_ascii=False))
    (DIST / "assets" / "app.js").write_text(js, encoding="utf-8")
    for f in ("favicon.png", "favicon.ico"):
        if (ROOT / "assets" / f).exists(): shutil.copy(ROOT / "assets" / f, DIST / f)

if __name__ == "__main__":
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    build_home(); build_fleet(); build_services(); build_cities(); build_articles(); build_misc(); build_files()
    print("pages:", len(PAGES))
