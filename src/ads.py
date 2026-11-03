# -*- coding: utf-8 -*-
"""Google Ads: поисковая кампания на каждый город, группы — общая аренда, каждый тоннаж, монтаж/погрузка.
Файлы для веб-интерфейса: Инструменты → Массовые действия → Загрузки. Все лимиты проверяются при сборке."""
import collections, re, sys
from pathlib import Path
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font
sys.path.insert(0, str(Path(__file__).parent))
from data import CITIES, FLEET, BRAND, SITE_URL, units

OUT = Path(__file__).resolve().parent.parent / "google-ads"
NEG_LIST = f"{BRAND} минус-слова"
def camp(nom): return f"{BRAND} {nom} Поиск"

# Названия местоположений — в том виде, в каком их принял Google при загрузке кампаний DezClub
GEO = {"almaty": "Almaty, Kazakhstan", "astana": "Astana, Kazakhstan", "shymkent": "Shymkent, Kazakhstan",
       "karaganda": "Karaganda,Karaganda Region,Kazakhstan", "aktobe": "Aktobe,Aktobe Region,Kazakhstan",
       "taraz": "Taraz,Zhambyl District,Jambyl Region,Kazakhstan", "pavlodar": "Pavlodar Region,Kazakhstan",
       "ust-kamenogorsk": "Oskemen,East Kazakhstan Region,Kazakhstan", "semey": "Semey, Kazakhstan", "atyrau": "Atyrau,Atyrau Region,Kazakhstan",
       "kostanay": "Kostanay Region,Kazakhstan", "kyzylorda": "Kyzylorda Region,Kazakhstan", "uralsk": "Uralsk,West Kazakhstan Region,Kazakhstan",
       "petropavlovsk": "Petropavl,North Kazakhstan Region,Kazakhstan", "aktau": "Aktau,Mangystau Region,Kazakhstan", "taldykorgan": "Taldykorgan, Kazakhstan",
       "turkestan": "Turkistan Region,Kazakhstan", "kokshetau": "Kokshetau,Akmola Region,Kazakhstan", "ekibastuz": "Ekibastuz,Pavlodar Region,Kazakhstan",
       "temirtau": "Temirtau,Karaganda Region,Kazakhstan", "zhezkazgan": "Zhezqazghan,Kazakhstan", "konaev": "Konaev,Almaty Region,Kazakhstan",
       "kaskelen": "Kaskelen,Almaty Region,Kazakhstan", "talgar": "Talgar,Almaty Region,Kazakhstan", "esik": "Esik,Almaty Region,Kazakhstan",
       "balkhash": "Balkhash,Karaganda Region,Kazakhstan", "zhanaozen": "Zhanaozen,Mangystau Region,Kazakhstan", "rudny": "Rudny,Kostanay Region,Kazakhstan",
       "satpaev": "Satpayev, Kazakhstan", "ridder": "Ridder,East Kazakhstan Region,Kazakhstan", "stepnogorsk": "Stepnogorsk,Akmola Region,Kazakhstan"}
# Промышленные города, где тяжёлые краны востребованы, получают бюджет выше
BUDGET = {"almaty": 5, "astana": 5, "shymkent": 3, "atyrau": 3, "aktau": 3, "karaganda": 3, "aktobe": 3, "pavlodar": 3, "ust-kamenogorsk": 2,
          "uralsk": 2, "kostanay": 2, "kyzylorda": 2, "taraz": 2, "semey": 2, "petropavlovsk": 2, "taldykorgan": 2, "turkestan": 2, "kokshetau": 2,
          "ekibastuz": 2, "temirtau": 2, "zhanaozen": 2}
ALT = {"ust-kamenogorsk": ["оскемен"], "semey": ["семипалатинск"], "konaev": ["капчагай"], "uralsk": ["орал"], "almaty": ["алма-ата"]}
PATH2 = {"ust-kamenogorsk": "оскемен"}

COMMON_H = ["Автокраны 50–400 тонн", "Техника SANY, XCMG, Zoomlion", "Работаем по всему Казахстану", "Подбор крана по задаче",
            "Монтаж, погрузка, подъёмы", "Краны 50, 70, 80, 100, 400 т", "Расчёт по массе и вылету", "Звоните или пишите в WhatsApp",
            "Юр. и физ. лица", "Наличный и безналичный расчёт", "Строительство и промышленность", "Перебазировка по Казахстану", "Сверхтяжёлый кран 400 тонн", "Монтаж металлоконструкций"]
COMMON_D = ["Аренда автокранов 50, 70, 80, 100 и 400 тонн SANY, XCMG, Zoomlion по всему Казахстану.",
            "Работаем с юр. и физ. лицами, наличный и безналичный расчёт. Подберём кран под задачу."]

GEN = ["аренда автокрана", "услуги автокрана", "автокран", "заказать автокран", "автокран в аренду", "аренда крана", "услуги крана", "кран в аренду", "вызвать автокран"]
def tonnage_base(t): return [f"автокран {t} тонн", f"аренда автокрана {t} тонн", f"кран {t} тонн", f"аренда крана {t} тонн", f"услуги автокрана {t} тонн", f"автокран {t}т", f"{t} тонный кран"]

def groups():
    G = [("Аренда автокрана", "CITY", GEN, ["аренда автокрана", "услуги автокрана", "заказать автокран", "автокран в аренду", "аренда крана", "вызвать автокран"],
          ["Аренда автокрана {in}", "Услуги автокрана {in}", "Автокран {in}", "Заказать автокран {in}", "Автокраны в аренду"],
          ["Аренда автокранов {in}: монтаж, погрузка и разгрузка, установка оборудования.",
           "Автокраны 50, 70, 80, 100 и 400 тонн {in}. Подберём класс под вес груза и высоту."], "аренда")]
    for f in FLEET:
        t = f["t"]
        G.append((f"Автокран {t} тонн", f"/avtokrany/{f['slug']}/", tonnage_base(t), [f"автокран {t} тонн", f"аренда автокрана {t} тонн", f"кран {t} тонн", f"аренда крана {t} тонн"],
                  [f"Автокран {t} тонн {{in}}", f"Аренда автокрана {t} тонн", f"Кран {t} тонн в аренду", f"{t} т: в парке {units(f['n'])}", f"Автокран {t} т {{in}}"],
                  [f"Автокран {t} тонн {{in}}: {f['tasks'][0][0].lower() + f['tasks'][0][1:]}.",
                   f"{f['tasks'][1]}. Проверим подъём по грузовысотной таблице."], f"{t}-тонн"))
    G.append(("Монтаж и погрузка", "/uslugi/montazh-metallokonstrukciy/",
              ["автокран для монтажа", "кран для монтажа металлоконструкций", "монтаж металлоконструкций автокраном", "погрузка автокраном", "разгрузка автокраном", "автокран для разгрузки", "монтаж жби автокраном"],
              ["автокран для монтажа", "монтаж металлоконструкций автокраном", "разгрузка автокраном"],
              ["Монтаж автокраном {in}", "Кран для монтажа {in}", "Погрузка и разгрузка краном", "Монтаж ЖБИ и металлоконструкций", "Установка оборудования"],
              ["Монтаж металлоконструкций и ЖБИ, погрузка и разгрузка автокраном {in}.",
               "Каркасы, фермы, плиты, оборудование и контейнеры. Кран подбираем по массе и вылету."], "монтаж"))
    return G

NEG = ["купить", "куплю", "продажа", "продам", "продается", "цена нового", "б/у", "бу", "лизинг", "запчасти", "запчасть", "ремонт", "сервис", "шины",
       "вакансия", "вакансии", "работа", "работа машинистом", "машинист", "крановщик", "зарплата", "резюме", "обучение", "курсы", "удостоверение", "экзамен",
       "игрушка", "игрушечный", "радиоуправляемый", "лего", "lego", "модель", "раскраска", "мультик", "мультфильм", "рисунок", "игра",
       "чертеж", "чертежи", "схема", "характеристики", "технические характеристики", "таблица", "гост", "инструкция", "устройство", "реферат", "фото", "видео",
       "башенный", "мостовой", "козловой", "кран балка", "кран-балка", "портальный", "тельфер", "лебедка", "манипулятор", "кму", "воровайка", "самогруз",
       "эвакуатор", "автовышка", "вышка", "ямобур", "экскаватор", "погрузчик",
       "10 тонн", "14 тонн", "16 тонн", "20 тонн", "25 тонн", "32 тонн", "35 тонн", "40 тонн",
       "ивановец", "галичанин", "клинцы", "челябинец", "углич", "камышин", "дрогобыч", "бесплатно"]

ERR = []
def chk(t, n, what):
    if len(t) > n: ERR.append(f"{what} >{n}: {t} ({len(t)})")
    return t

def headlines(hs, nom, cin):
    out = []
    for h in hs + ["Аренда автокрана {in}", "Работаем {in}", "Автокраны {in}"] + COMMON_H:
        t = h.format(**{"in": cin, "nom": nom})
        if len(t) > 30 and "{in}" in h: t = h.replace(" {in}", "")
        if len(t) <= 30 and t.lower() not in {x.lower() for x in out}: out.append(t)
        if len(out) == 15: break
    return out

def descriptions(ds, cin):
    out = []
    for d in ds:
        t = d.format(**{"in": cin})
        if len(t) > 90: t = d.replace(" {in}", "").format(**{"in": ""})
        out.append(t)
    return out + COMMON_D

def xlsx(path, cols, rows):
    wb = Workbook(); ws = wb.active; ws.title = "Upload"; ws.append(cols)
    for c in ws[1]: c.font = Font(bold=True)
    for r in rows: ws.append([r.get(c, "") for c in cols])
    for i, c in enumerate(cols, 1): ws.column_dimensions[ws.cell(1, i).column_letter].width = max(14, min(48, len(c) + 4))
    wb.save(path)

def campaigns_file(path, template):
    wb = openpyxl.load_workbook(template)
    for n in list(wb.sheetnames):
        if n.startswith("(Example)"): del wb[n]
    ws = wb[wb.sheetnames[0]]
    hdr = [c.value for c in ws[2]]
    if "EU political ads" not in hdr:
        ws.cell(1, len(hdr) + 1, "#Required: EU political ads"); ws.cell(2, len(hdr) + 1, "EU political ads"); hdr.append("EU political ads")
    for slug, nom, *_ in CITIES:
        r = {"Action": "Add", "Campaign status": "Paused", "Campaign": camp(nom), "Campaign type": "Search", "Networks": "Google search",
             "Budget": BUDGET.get(slug, 1), "Budget type": "Daily", "Bid strategy type": "Maximize clicks", "Location": GEO[slug], "EU political ads": "No"}
        ws.append([r.get(h) for h in hdr])
    wb.save(path)

def main(template):
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*"): f.unlink()
    H = [f"Headline {i}" for i in range(1, 16)]; D = [f"Description {i}" for i in range(1, 5)]
    G = groups(); grp, kws, ads, assoc, txt, stats = [], [], [], [], [], []
    for slug, nom, cin, region in CITIES:
        C = camp(nom); kw = nom.lower().replace("-", " ") if slug == "ust-kamenogorsk" else nom.lower()
        assoc.append({"Action": "Add", "Negative keyword": NEG_LIST, "Keyword or list": "List", "Campaign": C})
        seen = collections.Counter(); n = 0
        txt += ["=" * 70, f"КАМПАНИЯ: {C}", f"Местоположение: {GEO[slug]}", "=" * 70, ""]
        for name, path, base, exact, hs, ds, p1 in G:
            grp.append({"Action": "Add", "Campaign": C, "Ad group": name, "Ad group state": "Enabled"})
            words = []
            for b in base:
                for form in [f"{b} {kw}"] + [f"{b} {a}" for a in ALT.get(slug, [])]:
                    words += [f'"{form}"', f"[{form}]"]
            words += [f"[{e}]" for e in exact]
            words = list(dict.fromkeys(words))
            for w in words:
                seen[w] += 1; plain = w.strip('"[]')
                kws.append({"Action": "Add", "Campaign": C, "Ad group": name, "Keyword": w})
                if len(plain) > 80 or len(plain.split()) > 10: ERR.append("длинный ключ " + plain)
                for ng in NEG:
                    if f" {ng} " in f" {plain} ": ERR.append(f"минус «{ng}» режет «{plain}»")
            n += len(words)
            heads = headlines(hs, nom, cin); descs = descriptions(ds, cin)
            if len(heads) != 15: ERR.append(f"{C}/{name}: заголовков {len(heads)}")
            url = SITE_URL + (f"/goroda/{slug}/" if path == "CITY" else path)
            r = {"Action": "Add", "Campaign": C, "Ad group": name, "Ad type": "Responsive search ad", "Final URL": url,
                 "Path 1": chk(p1, 15, "path1"), "Path 2": chk(PATH2.get(slug, kw), 15, "path2")}
            for i, h in enumerate(heads): r[H[i]] = chk(h, 30, "headline")
            for i, d in enumerate(descs): r[D[i]] = chk(d, 90, "description")
            ads.append(r)
            txt += [f"Группа: {name}", f"URL: {url}", "Заголовки: " + " | ".join(heads), "Описания: " + " | ".join(descs), ""]
        dup = [k for k, v in seen.items() if v > 1]
        if dup: ERR.append(f"{C}: дубли {dup[:4]}")
        stats.append((C, GEO[slug], BUDGET.get(slug, 1), n))
    if ERR: print("\n".join(ERR[:40])); raise SystemExit(1)
    campaigns_file(OUT / "0-sozdat-kampanii.xlsx", template)
    xlsx(OUT / "1-gruppy.xlsx", ["Action", "Campaign", "Ad group", "Ad group state"], grp)
    xlsx(OUT / "2-klyuchevye-slova.xlsx", ["Action", "Campaign", "Ad group", "Keyword"], kws)
    xlsx(OUT / "3-obyavleniya.xlsx", ["Action", "Campaign", "Ad group", "Ad type"] + H + D + ["Path 1", "Path 2", "Final URL"], ads)
    xlsx(OUT / "4-minus-slova-v-spisok.xlsx", ["Action", "Negative keyword list name", "Negative keyword", "Keyword or list", "Match type"],
         [{"Action": "Add", "Negative keyword list name": NEG_LIST, "Negative keyword": x, "Keyword or list": "Keyword", "Match type": "Phrase Match"} for x in NEG])
    xlsx(OUT / "5-privyazat-spisok-k-kampaniyam.xlsx", ["Action", "Negative keyword", "Keyword or list", "Campaign"], assoc)
    head = ["КАМПАНИИ (создаются файлом 0, на паузе) | местоположение | бюджет $/день | ключей", ""] + [f"{c} | {g} | {b} | {k}" for c, g, b, k in stats]
    (OUT / "6-spisok-kampaniy-i-teksty.txt").write_text("\n".join(head + ["", "ТЕКСТЫ ОБЪЯВЛЕНИЙ (уже в файле 3, для проверки)", ""] + txt) + "\n", encoding="utf-8")
    print("кампаний", len(stats), "групп", len(grp), "ключей", len(kws), "объявлений", len(ads), "минус", len(NEG), "бюджет/день", sum(s[2] for s in stats))

if __name__ == "__main__":
    main(sys.argv[1])
