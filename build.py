#!/usr/bin/env python3
"""Сборка статических страниц GIGANT Agro из partials/ и pages/."""
import os, re, sys

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

def build_page(slug, body_file, title, desc, ogimage):
    body = read(os.path.join('pages', body_file))
    head = (HEAD.replace('{{TITLE}}', title)
                .replace('{{DESC}}', desc)
                .replace('{{OGTITLE}}', OGTITLES.get(slug, title))
                .replace('{{OGIMAGE}}', ogimage))
    header, footer = HEADER, FOOTER
    if slug != 'index':
        header = header.replace('<body class="', '<body class="page-inner ', 1)
        # якоря главной работают с любой страницы
        header = re.sub(r'href="#(top|catalog|podbor|komplekty|flagmany|zhivotnye|kak-rabotaet|avtonomno|dostavka|faq|konsultaciya)"',
                        r'href="index.html#\1"', header)
        footer = re.sub(r'href="#(top|catalog|podbor|komplekty|flagmany|zhivotnye|kak-rabotaet|avtonomno|dostavka|faq|konsultaciya)"',
                        r'href="index.html#\1"', footer)
    out = head + '\n' + header + '\n' + body + '\n' + footer
    open(os.path.join(ROOT, slug + '.html'), 'w', encoding='utf-8').write(out)
    return slug + '.html', len(out)

if __name__ == '__main__':
    only = sys.argv[1:] or None
    for slug, body_file, title, desc, og in PAGES:
        if only and slug not in only: continue
        if not os.path.exists(os.path.join(ROOT, 'pages', body_file)):
            print(f'  пропуск: pages/{body_file} нет'); continue
        name, size = build_page(slug, body_file, title, desc, og)
        print(f'  {name:32} {size//1024} KB')
