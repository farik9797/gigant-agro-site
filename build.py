#!/usr/bin/env python3
"""Сборка статических страниц GIGANT Agro из partials/ и pages/."""
import os, re, sys, json, hashlib, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
def read(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()

HEAD   = read('partials/head.html')
HEADER = read('partials/header.html')
FOOTER = read('partials/footer.html')

# slug, файл тела, title, description, og-картинка
OGTITLES = {
 'index': 'Электроизгородь, которая держит стадо — GIGANT Agro',
}

PAGES = [
 ('index',                 'index.html',
  'Электропастухи GIGANT и Bekci в Алматы — GIGANT Agro',
  'Электропастухи GIGANT и Bekci от 6,9 до 25&nbsp;Дж, готовые комплекты для овец, лошадей и КРС. Склад в Алматы, доставка по Казахстану, подбор за минуту.',
  'assets/img/hero-gigant-1920.jpg'),
 ('catalog',               'catalog.html',
  'Каталог электропастухов и комплектующих — GIGANT Agro',
  'Электропастухи, готовые комплекты, сетки и шнуры, изоляторы, кабели, солнечное питание и оборудование для стрижки овец. Склад в Алматы, доставка по Казахстану.',
  'assets/img/kit-sheep-poultry.jpg'),
 ('catalog-elektropastuhi','catalog-elektropastuhi.html',
  'Электропастухи GIGANT и Bekci — купить в Алматы',
  'Электропастухи от 6,9 до 25&nbsp;Дж: GIGANT 15, Bekci 6.9, Bekci 14.5, Bekci 25. Цены, характеристики, помощь в подборе под животных и площадь.',
  'assets/img/product-gigant15.jpg'),
 ('catalog-komplekty',     'catalog-komplekty.html',
  'Готовые комплекты электроизгороди — GIGANT Agro',
  'Готовые комплекты для овец, КРС и лошадей от 125 000 ₸. Аккумулятор в подарок. Всё нужное в одной коробке, доставка по Казахстану.',
  'assets/img/kit-sheep-poultry.jpg'),
 ('catalog-setki',         'catalog-setki.html',
  'Сетки и шнуры для электроизгороди — GIGANT Agro',
  'Шнур многожильный 6 жил, проволока оцинкованная 1,6 мм, электросетки. Проводники для электроизгороди со склада в Алматы.',
  'assets/img/cat-nets.jpg'),
 ('catalog-izolyatory',    'catalog-izolyatory.html',
  'Изоляторы и колышки для электроизгороди — GIGANT Agro',
  'Изоляторы под проволоку, шнур и ленту, колышки и стойки для электроизгороди. Комплектующие со склада в Алматы.',
  'assets/img/cat-insulators.jpg'),
 ('catalog-kabeli',        'catalog-kabeli.html',
  'Кабели, клеммы и аксессуары для электропастуха — GIGANT Agro',
  'Кабели подключения, клеммы, зажимы, заземление и ворота для электроизгороди. Комплектующие со склада в Алматы.',
  'assets/img/cat-cables.jpg'),
 ('catalog-solnce',        'catalog-solnce.html',
  'Солнечные панели, контроллеры и аккумуляторы — GIGANT Agro',
  'Солнечные панели, MPPT-контроллеры и аккумуляторы 12 В для автономной работы электропастуха на дальних пастбищах.',
  'assets/img/solar-line.jpg'),
 ('catalog-strizhka',      'catalog-strizhka.html',
  'Оборудование для стрижки овец — GIGANT Agro',
  'Машинки для стрижки овец, ножи и запчасти. Оборудование для животноводства со склада в Алматы.',
  'assets/img/cat-shearing.jpg'),
 ('catalog-pogonyala',     'catalog-pogonyala.html',
  'Электропогонялa для скота — GIGANT Agro',
  'Электропогонялa GIGANT для управления движением КРС, свиней и мелкого рогатого скота. 44 500 ₸, склад в Алматы.',
  'assets/img/product-gigant15.jpg'),
 ('product-gigant-15',     'product-gigant-15.html',
  'Электропастух GIGANT 15 Дж — 105 000 ₸, Алматы',
  'Электропастух GIGANT 15 Дж: импульс 15 Дж, напряжение 12 000 В, питание 220 В и 12 В, пульт ДУ, гарантия 1 год. Доставка по Казахстану.',
  'assets/img/product-gigant15.jpg'),
 ('podbor',                'podbor.html',
  'Подбор комплекта электроизгороди за минуту — GIGANT Agro',
  'Ответьте на три вопроса: животные, площадь и питание. Покажем модель электропастуха, состав комплекта и ориентировочную цену.',
  'assets/img/hero-gigant-1920.jpg'),
 ('kak-vybrat',            'kak-vybrat.html',
  'Как выбрать электропастух — гид GIGANT Agro',
  'Гид по выбору электропастуха: как считать мощность в джоулях и периметр, сколько линий нужно каждому животному, как сделать заземление и выбрать питание.',
  'assets/img/why-cow-fence.jpg'),
 ('instrukcii',            'instrukcii.html',
  'Инструкции и схемы подключения электроизгороди — GIGANT Agro',
  'Схемы подключения электропастуха, заземления и солнечной панели. Порядок установки электроизгороди шаг за шагом.',
  'assets/img/insulator.jpg'),
 ('dostavka',              'dostavka.html',
  'Доставка и оплата — GIGANT Agro',
  'Самовывоз со склада в Алматы, доставка транспортными компаниями по Казахстану, России и СНГ. Оплата наличными и безналичным переводом.',
  'assets/img/hero-gigant-1920.jpg'),
 ('garantiya',             'garantiya.html',
  'Гарантия, возврат и обмен — GIGANT Agro',
  'Гарантия на электропастухи GIGANT 1 год, Bekci 2 года. Возврат и обмен в течение 14 дней по закону РК «О защите прав потребителей».',
  'assets/img/product-bekci25.jpg'),
 ('o-kompanii',            'o-kompanii.html',
  'О компании GIGANT Agro — электропастухи в Алматы',
  'GIGANT Agro продаёт электропастухи, электроизгороди и комплектующие фермерам Казахстана. Склад в Алматы, опт и розница, доставка по регионам.',
  'assets/img/why-cow-fence.jpg'),
 ('kontakty',              'kontakty.html',
  'Контакты — GIGANT Agro, Алматы',
  'Алматы, мкр. Атырау, 159/8, склад № 1. Телефоны +7 705 428-57-07 и +7 775 771-60-24, WhatsApp. Пн–Пт 10:00–18:00, Сб 10:00–16:00.',
  'assets/img/hero-gigant-1920.jpg'),
 ('faq',                   'faq.html',
  'Вопросы и ответы об электропастухах — GIGANT Agro',
  'Какую мощность выбрать, как рассчитать периметр, сколько линий нужно, как сделать заземление, чем отличается питание 12 В, 220 В и солнечная панель.',
  'assets/img/cow-tape.jpg'),
 ('spasibo',               'spasibo.html',
  'Заявка отправлена — GIGANT Agro',
  'Спасибо за заявку. Менеджер GIGANT Agro свяжется с вами в рабочее время.',
  'assets/img/hero-gigant-1920.jpg'),
 ('policy',                'policy.html',
  'Политика конфиденциальности — GIGANT Agro',
  'Как GIGANT Agro обрабатывает и защищает персональные данные, оставленные через формы на сайте.',
  'assets/img/hero-gigant-1920.jpg'),
 ('404',                   '404.html',
  'Страница не найдена — GIGANT Agro',
  'Такой страницы нет. Вернитесь в каталог электропастухов или подберите комплект за минуту.',
  'assets/img/hero-gigant-1920.jpg'),
]

BASE = 'https://farik9797.github.io/gigant-agro-site/'
MANIFEST = json.load(open(os.path.join(ROOT, 'assets/img/opt/manifest.json'))) if os.path.exists(os.path.join(ROOT, 'assets/img/opt/manifest.json')) else {}
HERO_IMAGES = {'hero-gigant-1920.jpg', 'steppe-horses-1920.jpg', 'why-cow-fence.jpg', 'solar-line.jpg'}
ICON_DIR = os.path.join(ROOT, 'node_modules/lucide-static/icons')
_icon_cache = {}

def file_hash(path):
    return hashlib.md5(open(os.path.join(ROOT, path), 'rb').read()).hexdigest()[:8]

def build_css():
    """Статический CSS: свои шрифты + стили сайта → Tailwind CLI → assets/css/site.css"""
    bundle = os.path.join(ROOT, 'src/_bundle.css')
    open(bundle, 'w', encoding='utf-8').write(read('src/fonts.css') + '\n' + read('src/site.css'))
    subprocess.run([os.path.join(ROOT, 'node_modules/.bin/tailwindcss'), '-c', 'tailwind.config.js',
                    '-i', 'src/_bundle.css', '-o', 'assets/css/site.css', '--minify'],
                   cwd=ROOT, check=True, capture_output=True)
    os.remove(bundle)

def inline_icons(html):
    """<i data-lucide="x" class="…"> → встроенный SVG из lucide-static (без рантайма и CDN)."""
    def rep(m):
        name, cls = m.group(1), m.group(2)
        if name not in _icon_cache:
            svg = open(os.path.join(ICON_DIR, name + '.svg'), encoding='utf-8').read()
            inner = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1)
            _icon_cache[name] = re.sub(r'\s+', ' ', inner).replace('> <', '><').strip()
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
                f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                f'class="lucide {cls}" aria-hidden="true" focusable="false">{_icon_cache[name]}</svg>')
    return re.sub(r'<i data-lucide="([\w-]+)" class="([^"]*)"(?: aria-hidden="true")?></i>', rep, html)

def responsive_images(html):
    """<img src="assets/img/x.jpg"> → WebP + srcset/sizes + реальные width/height."""
    def rep(m):
        tag = m.group(0)
        name = re.search(r'src="assets/img/([^"]+)"', tag).group(1)
        info = MANIFEST.get(name)
        if not info: return tag
        hero = name in HERO_IMAGES and 'absolute inset-0' in tag   # тот же файл в карточке — обычные sizes
        v = info['variants']
        default = next((x for x in v if x['w'] >= (1440 if hero else 800)), v[-1])
        tag = re.sub(r'\s(?:srcset|sizes|width|height)="[^"]*"', '', tag)
        srcset = ', '.join(f"{x['file']} {x['w']}w" for x in v)
        sizes = '100vw' if hero else '(min-width:1024px) 50vw, (min-width:640px) 60vw, 88vw'
        resp = f' srcset="{srcset}" sizes="{sizes}"' if len(v) > 1 else ''   # один размер (логотип) — без srcset
        tag = tag.replace(f'src="assets/img/{name}"',
              f'src="{default["file"]}"{resp} width="{info["width"]}" height="{info["height"]}"')
        if 'fetchpriority="high"' not in tag and 'decoding=' not in tag:
            tag = tag.replace('<img ', '<img decoding="async" ', 1)
        return tag
    return re.sub(r'<img\b[^>]*\bsrc="assets/img/[^"]+\.(?:jpe?g|png)"[^>]*>', rep, html)

def mark_current(html, slug):
    """aria-current для текущего пункта в шапке, мобильном меню и нижней панели."""
    exact = slug + '.html'
    section = 'catalog.html' if slug.startswith(('catalog-', 'product-')) else None
    def rep(m):
        href = m.group(1)
        if href == exact: return m.group(0).replace('<a ', '<a aria-current="page" ', 1)
        if section and href == section: return m.group(0).replace('<a ', '<a aria-current="true" ', 1)
        return m.group(0)
    return re.sub(r'<a href="([\w-]+\.html)"[^>]*>', rep, html)

def build_page(slug, body_file, title, desc, ogimage, cssv, jsv):
    body = read(os.path.join('pages', body_file))
    if slug != 'index':   # первая картинка внутренней страницы видна сразу — не откладываем её загрузку
        first = re.search(r'<img\b[^>]*>', body)
        if first and 'loading="lazy"' in first.group(0):
            body = body.replace(first.group(0), first.group(0).replace(' loading="lazy"', ' fetchpriority="high"'), 1)
    url = BASE if slug == 'index' else BASE + slug + '.html'
    head = (HEAD.replace('{{TITLE}}', title).replace('{{DESC}}', desc)
                .replace('{{OGTITLE}}', OGTITLES.get(slug, title)).replace('{{OGIMAGE}}', ogimage)
                .replace('{{URL}}', url).replace('{{BASE}}', BASE).replace('{{CSSV}}', cssv))
    header, footer = HEADER, FOOTER.replace('{{JSV}}', jsv)
    if slug != 'index':
        header = header.replace('<body class="', '<body class="page-inner ', 1)
        anchors = r'href="#(top|catalog|podbor|komplekty|flagmany|zhivotnye|kak-rabotaet|avtonomno|dostavka|faq|konsultaciya)"'
        header = re.sub(anchors, r'href="index.html#\1"', header)
        header = header.replace('<a href="index.html#podbor" class="sr-only', '<a href="#top" class="sr-only', 1).replace('>Перейти к подбору комплекта</a>', '>Перейти к содержимому</a>', 1)
        footer = footer.replace('<a href="#catalog" class="flex flex-col', '<a href="catalog.html" class="flex flex-col').replace('<a href="#podbor" class="flex flex-col', '<a href="podbor.html" class="flex flex-col')
        footer = re.sub(anchors, r'href="index.html#\1"', footer)
        header, footer = mark_current(header, slug), mark_current(footer, slug)
    if slug == 'index':
        # LCP-картинка главной: предзагрузка нужного размера
        info = MANIFEST.get('hero-gigant-1920.jpg')
        if info:
            srcset = ', '.join(f"{x['file']} {x['w']}w" for x in info['variants'])
            head = head.replace('<link rel="stylesheet"', f'<link rel="preload" as="image" imagesrcset="{srcset}" imagesizes="100vw" fetchpriority="high">\n<link rel="stylesheet"', 1)
    out = responsive_images(inline_icons(head + '\n' + header + '\n' + body + '\n' + footer))
    open(os.path.join(ROOT, slug + '.html'), 'w', encoding='utf-8').write(out)
    return slug + '.html', len(out)

if __name__ == '__main__':
    only = sys.argv[1:] or None
    build_css()
    cssv, jsv = file_hash('assets/css/site.css'), file_hash('assets/js/site.js')
    print(f'  assets/css/site.css              {os.path.getsize(os.path.join(ROOT,"assets/css/site.css"))//1024} KB')
    for slug, body_file, title, desc, og in PAGES:
        if only and slug not in only: continue
        if not os.path.exists(os.path.join(ROOT, 'pages', body_file)):
            print(f'  пропуск: pages/{body_file} нет'); continue
        name, size = build_page(slug, body_file, title, desc, og, cssv, jsv)
        print(f'  {name:32} {size//1024} KB')
