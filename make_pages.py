#!/usr/bin/env python3
"""Генерация тел страниц в pages/ из общих блоков и данных проекта."""
import os
ROOT=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(ROOT,'pages')
os.makedirs(OUT,exist_ok=True)
def w(name, html): open(os.path.join(OUT,name),'w',encoding='utf-8').write(html.strip()+'\n'); print('  pages/'+name)

WA='https://wa.me/77054285707'
def order(name):
    import urllib.parse, html as _h
    return 'kontakty.html?tovar='+urllib.parse.quote(_h.unescape(name).replace('\xa0',' '))+'#leadForm'

def wa(text): 
    import urllib.parse; return WA+'?text='+urllib.parse.quote(text)

# ---------- общие блоки ----------
def crumbs(items):
    """items: [(title, href|None), ...] последний — текущая страница"""
    li=[]; ld=[]
    for i,(t,h) in enumerate(items,1):
        if h: li.append(f'<li><a href="{h}" class="hover:text-ink">{t}</a></li>')
        else: li.append(f'<li aria-current="page" class="text-ink font-medium">{t}</li>')
        ld.append('{"@type":"ListItem","position":%d,"name":"%s"%s}'%(i,t.replace('&nbsp;',' '),
                  ',"item":"%s"'%h if h else ''))
    return f'''<nav aria-label="Хлебные крошки" class="container-site pt-28 md:pt-32">
  <ol class="no-scrollbar flex items-center gap-x-2 gap-y-1 text-[14px] text-muted whitespace-nowrap overflow-x-auto -mx-5 px-5 sm:mx-0 sm:px-0 sm:flex-wrap sm:whitespace-normal sm:overflow-visible">
    {'<li aria-hidden="true">/</li>'.join(li)}
  </ol>
</nav>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{','.join(ld)}]}}</script>'''

def page_head(h1, lead, aside=''):
    return f'''<header class="container-site pt-6 md:pt-8">
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 lg:gap-10 items-end">
    <div class="lg:col-span-7"><h1 class="h2">{h1}</h1>{f'<p class="lead mt-4">{lead}</p>' if lead else ''}</div>
    {f'<div class="lg:col-span-5 lg:text-right">{aside}</div>' if aside else ''}
  </div>
</header>'''

def cta_band(title='Не уверены, что выбрать?', text='Опишите хозяйство — подберём модель, число линий и питание за один разговор.'):
    return f'''<section class="bg-deep text-cream mt-16 md:mt-24">
  <div class="container-site py-12 md:py-16 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
    <div class="lg:col-span-7">
      <h2 class="h2">{title}</h2>
      <p class="mt-4 text-cream/80 text-[17px] leading-[1.6] max-w-[52ch]">{text}</p>
    </div>
    <div class="lg:col-span-5 flex flex-col sm:flex-row lg:justify-end gap-3">
      <a href="podbor.html" class="btn-primary btn-lg">Подобрать комплект<i data-lucide="arrow-right" class="w-5 h-5" aria-hidden="true"></i></a>
      <a href="{wa('Здравствуйте! Нужна консультация по электропастуху.')}" target="_blank" rel="noopener" class="btn-glass btn-lg"><img src="assets/icons/whatsapp-FFFFFF.svg" alt="" class="w-5 h-5" width="20" height="20">WhatsApp</a>
    </div>
  </div>
</section>'''

def helper_card():
    return f'''<article class="rounded-2xl bg-deep text-cream p-5 flex flex-col justify-between gap-4 min-h-[220px]">
  <div><p class="font-extrabold text-[18px] leading-tight">Не нашли нужное?</p><p class="text-cream/75 text-[14px] mt-2">Напишите, что за животные и сколько гектаров — подберём комплект и посчитаем количество.</p></div>
  <a href="{wa('Здравствуйте! Помогите подобрать комплектующие.')}" target="_blank" rel="noopener" class="btn-primary h-11 px-4 self-start text-[15px]"><img src="assets/icons/whatsapp-16191C.svg" alt="" class="w-5 h-5" width="20" height="20">Спросить в WhatsApp</a>
</article>'''

def product_card(img, alt, name, sub, price, specs, href=None, badge=None, badge_style='bg-cream text-brand-dark'):
    specs=[(k,'уточняйте' if k=='Наличие' and '[уточнить' in v else v) for k,v in specs]
    specs=[(k,v) for k,v in specs if '[уточнить' not in v]   # пометки для заказчика на сайт не выводим
    spec_html=''.join(f'<div class="border-t border-line pt-2"><dt class="text-[12px] text-muted">{k}</dt><dd class="font-bold text-[14px]">{v}</dd></div>' for k,v in specs)
    title=f'<a href="{href}" class="hover:underline underline-offset-4">{name}</a>' if href else name
    return f'''<article class="card lift overflow-hidden flex flex-col">
  <div class="relative bg-white aspect-[16/10] sm:aspect-[4/3] border-b border-line">
    <img src="{img}" alt="{alt}" class="absolute inset-0 w-full h-full object-contain p-4" loading="lazy" width="800" height="600">
    {f'<span class="absolute left-3 top-3 rounded-full {badge_style} text-[13px] font-bold px-2.5 py-1">{badge}</span>' if badge else ''}
  </div>
  <div class="p-5 flex flex-col flex-1">
    <div class="flex items-baseline justify-between gap-3">
      <h2 class="font-extrabold text-[19px] leading-tight">{title}</h2>
      <p class="font-black text-[19px] leading-none tabular-nums whitespace-nowrap">{price}</p>
    </div>
    <p class="text-muted text-[14px] mt-2">{sub}</p>
    <dl class="mt-4 grid grid-cols-2 gap-x-4 gap-y-2">{spec_html}</dl>
    <div class="mt-auto pt-5 flex flex-wrap gap-2">
      <a href="{order(name)}" class="btn-primary h-11 sm:h-10 px-4 text-[15px] flex-1 sm:flex-none">Заказать</a>
      <a href="{wa('Здравствуйте! Интересует '+name.replace('&nbsp;',' '))}" target="_blank" rel="noopener" class="btn-outline h-11 sm:h-10 px-3.5 sm:px-3 text-[15px] shrink-0"><img src="assets/icons/whatsapp-16191C.svg" alt="" class="w-5 h-5" width="20" height="20">WhatsApp</a>
    </div>
  </div>
</article>'''

def prose(html):
    return f'<div class="prose-block max-w-[70ch] text-[17px] leading-[1.65] text-ink">{html}</div>'


# ---------- данные ----------
CATS=[
 ('catalog-elektropastuhi.html','Электропастухи','GIGANT 15&nbsp;Дж и Bekci от 6,9 до 25&nbsp;Дж','assets/img/product-gigant15.jpg','Электропастух GIGANT 15 Дж','4 модели'),
 ('catalog-komplekty.html','Готовые комплекты','Для овец, КРС и лошадей, аккумулятор в подарок','assets/img/kit-sheep-poultry.jpg','Готовый комплект для овец с электросеткой','от 125 000 ₸'),
 ('catalog-setki.html','Сетки и шнуры','Шнур 6 жил, проволока 1,6 мм, электросетки','assets/img/cat-nets.jpg','Рулоны электросетки','от 21 900 ₸'),
 ('catalog-izolyatory.html','Изоляторы и колышки','Под проволоку, шнур и ленту','assets/img/cat-insulators.jpg','Изолятор на столбе','цена по запросу'),
 ('catalog-kabeli.html','Кабели и аксессуары','Подключение, клеммы, заземление, ворота','assets/img/cat-cables.jpg','Кабели подключения с клеммами','цена по запросу'),
 ('catalog-solnce.html','Солнечные системы','Панели, MPPT-контроллеры, аккумуляторы','assets/img/solar-line.jpg','Солнечная панель на линии электроизгороди','цена по запросу'),
 ('catalog-strizhka.html','Стрижка овец','Машинки, ножи и запчасти','assets/img/cat-shearing.jpg','Машинка для стрижки овец','цена по запросу'),
 ('catalog-pogonyala.html','Электропогонялa','Для перемещения скота','assets/img/product-gigant15.jpg','Электропогоняло GIGANT','44 500 ₸'),
]

PRIBORY=[
 dict(img='assets/img/product-gigant15.jpg',alt='Электропастух GIGANT 15 Дж с адаптером, пультом и клеммами',
      name='GIGANT 15&nbsp;Дж',sub='Стандартные хозяйства и средние периметры',price='105 000 ₸',
      href='product-gigant-15.html',badge='Собственная марка',
      specs=[('Импульс','15 Дж'),('Напряжение','12 000 В'),('Питание','220 В / 12 В'),('Гарантия','1 год')]),
 dict(img='assets/img/product-bekci25.jpg',alt='Электропастух Bekci 25 Дж',
      name='Bekci 25&nbsp;Дж',sub='Большие периметры, густая трава, крупные и дикие животные',price='145 000 ₸',
      badge='Максимальная мощность',badge_style='bg-pulse text-ink',
      specs=[('Импульс','25 Дж'),('Производство','Турция'),('Питание','220 В / 12 В'),('Гарантия','2 года')]),
 dict(img='assets/img/product-bekci25.jpg',alt='Электропастух Bekci 14.5 Дж',
      name='Bekci 14,5&nbsp;Дж',sub='Хозяйства среднего размера, КРС и овцы',price='105 000 ₸',
      specs=[('Импульс','14,5 Дж'),('Производство','Турция'),('Питание','220 В / 12 В'),('Гарантия','2 года')]),
 dict(img='assets/img/product-bekci25.jpg',alt='Электропастух Bekci 6.9 Дж',
      name='Bekci 6,9&nbsp;Дж',sub='Небольшие загоны и спокойные животные',price='69 000 ₸',
      specs=[('Импульс','6,9 Дж'),('Производство','Турция'),('Питание','[уточнить]'),('Гарантия','2 года')]),
]

KITS=[
 dict(img='assets/img/animal-sheep.jpg',alt='Овцы за электросеткой',name='Комплект «Для овец»',sub='Овцы и козы · до 1 га',price='125 000 ₸',
      items=['Генератор импульсов','Проводник и изоляторы','Ворота','Аккумулятор 12 В']),
 dict(img='assets/img/cattle-meadow.jpg',alt='Коровы на пастбище',name='Комплект «Для КРС»',sub='КРС · до 5 га',price='145 000 ₸',
      items=['Генератор импульсов','Аккумулятор 12 В, 7 Ач','Проводник 1000 м, изоляторы','Предупреждающие таблички']),
 dict(img='assets/img/horses-steppe-2.jpg',alt='Лошади на пастбище',name='Комплект «Для лошадей»',sub='Лошади · до 6 га',price='125 000 ₸',
      items=['Генератор импульсов','Проволока, шнур, верёвка','Ворота и изоляторы','Аккумулятор 12 В']),
 dict(img='assets/img/solar-energizer.jpg',alt='Электропастух с солнечной панелью',name='Автономный комплект',sub='Любые животные · дальние пастбища',price='Цена по запросу',
      items=['Электропастух 15 или 25 Дж','Солнечная панель','MPPT-контроллер','Аккумулятор 12 В']),
]

def kit_card(k):
    li=''.join(f'<li class="flex gap-2"><i data-lucide="check" class="w-4 h-4 text-brand-dark shrink-0 mt-1" aria-hidden="true"></i>{i}</li>' for i in k['items'])
    return f'''<article class="card lift overflow-hidden flex flex-col">
  <div class="relative aspect-[4/3] overflow-hidden"><img src="{k['img']}" alt="{k['alt']}" class="w-full h-full object-cover" loading="lazy" width="900" height="675"><span class="absolute left-3 top-3 rounded-full bg-pulse text-ink text-[13px] font-bold px-2.5 py-1">Аккумулятор в подарок</span></div>
  <div class="p-5 flex flex-col flex-1">
    <p class="text-[13px] text-muted">{k['sub']}</p>
    <h2 class="font-extrabold text-[20px] leading-tight mt-1">{k['name']}</h2>
    <ul class="mt-3 space-y-1.5 text-[14px] text-muted">{li}</ul>
    <div class="mt-auto pt-5 flex items-center justify-between gap-3">
      <p class="font-black text-[20px] leading-none tabular-nums">{k['price']}</p>
      <a href="{order(k['name'])}" class="btn-primary h-11 sm:h-10 px-5 sm:px-4 text-[15px]">Заказать</a>
    </div>
  </div>
</article>'''

# ---------- каталог (все категории) ----------
tiles=''.join(f'''      <a href="{href}" class="card lift overflow-hidden group flex flex-row sm:flex-col">
        <div class="w-[112px] shrink-0 sm:w-auto aspect-square sm:aspect-[4/3] bg-[#EEF1EA] overflow-hidden"><img src="{img}" alt="{alt}" class="w-full h-full object-cover transition-transform duration-500 ease-out group-hover:scale-[1.03]" loading="lazy" width="900" height="675"></div>
        <div class="min-w-0 flex-1 p-3.5 sm:p-4 md:p-5 flex items-center justify-between gap-2 sm:gap-3">
          <div class="min-w-0 flex-1"><h2 class="font-extrabold text-[17px] leading-tight">{name}</h2><p class="text-muted text-[14px] leading-snug mt-1">{sub}</p><p class="sm:hidden mt-1.5 text-[13px] font-bold text-brand-dark">{meta}</p></div>
          <span class="hidden sm:block text-[13px] text-muted whitespace-nowrap">{meta}</span>
          <i data-lucide="chevron-right" class="sm:hidden w-5 h-5 text-muted shrink-0" aria-hidden="true"></i>
        </div>
      </a>
''' for href,name,sub,img,alt,meta in CATS)

w('catalog.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Каталог',None)])}
{page_head('Каталог', 'Электропастухи, готовые комплекты и все комплектующие для электроизгороди. Основной ассортимент — на складе в Алматы, отгружаем в день заказа.',
  '<a href="podbor.html" class="btn-primary btn-lg">Подобрать комплект<i data-lucide="arrow-right" class="w-5 h-5" aria-hidden="true"></i></a>')}
<section class="container-site mt-10 md:mt-12">
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
{tiles}  </div>
</section>
{cta_band()}
</main>''')

# ---------- категория: электропастухи ----------
cards=''.join(product_card(p['img'],p['alt'],p['name'],p['sub'],p['price'],p['specs'],p.get('href'),p.get('badge'),p.get('badge_style','bg-cream text-brand-dark')) for p in PRIBORY)
w('catalog-elektropastuhi.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Каталог','catalog.html'),('Электропастухи',None)])}
{page_head('Электропастухи', 'Четыре модели от 6,9 до 25&nbsp;Дж. Мощность выбирают по длине линии, густоте травы и виду животных: чем длиннее периметр и плотнее растительность, тем больше джоулей нужно.')}
<section class="container-site mt-8 md:mt-10 grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
  <div class="order-last lg:order-none lg:col-span-3">
    <div class="lg:sticky lg:top-28 card p-5">
      <p class="font-extrabold text-[17px]">Подобрать по задаче</p>
      <ul class="mt-4 space-y-2.5 text-[15px]">
        <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Загон и спокойные животные — 6,9&nbsp;Дж</li>
        <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Хозяйство с КРС, лошадьми, овцами — 14,5–15&nbsp;Дж</li>
        <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Большой периметр и дикие животные — 25&nbsp;Дж</li>
      </ul>
      <a href="podbor.html" class="btn-primary w-full mt-5">Подобрать за минуту</a>
      <a href="kak-vybrat.html" class="link mt-4">Как выбрать электропастух<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a>
    </div>
  </div>
  <div class="lg:col-span-9 grid grid-cols-1 sm:grid-cols-2 gap-4 md:gap-5">
{cards}{helper_card()}
  </div>
</section>
{cta_band()}
</main>''')

# ---------- категория: комплекты ----------
w('catalog-komplekty.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Каталог','catalog.html'),('Готовые комплекты',None)])}
{page_head('Готовые комплекты', 'Всё нужное в одной коробке: прибор, проводник, изоляторы, ворота и аккумулятор. При покупке полного комплекта аккумулятор — в подарок.')}
<section class="container-site mt-8 md:mt-10">
  <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-5">
{''.join(kit_card(k) for k in KITS)}  </div>
  <p class="mt-6 text-[15px] text-muted max-w-[70ch]">Площадь в описании комплекта — ориентир для участка близкой к квадрату формы. Вытянутый участок при той же площади даёт больший периметр, поэтому проводника и изоляторов потребуется больше. Посчитаем при подборе.</p>
</section>
{cta_band()}
</main>''')

# ---------- остальные категории (общий шаблон) ----------
SIMPLE={
 'catalog-setki.html':('Сетки и шнуры','Проводник — то, что животное видит и чувствует. Для КРС и лошадей берут проволоку или шнур, для овец, коз и птицы — готовую электросетку.',
   [dict(img='assets/img/cat-nets.jpg',alt='Рулоны электросетки',name='Шнур многожильный, 6 жил',sub='Универсальный проводник для КРС, лошадей и овец',price='21 900 ₸',
         specs=[('Жил','6'),('Длина бухты','[уточнить]'),('Цвет','[уточнить]'),('Скидка','до 10 %')]),
    dict(img='assets/img/fence-tape.jpg',alt='Линии электроизгороди',name='Проволока оцинкованная 1,6 мм',sub='Бухта 1000 м, для длинных периметров и защиты от диких животных',price='22 000 ₸',
         specs=[('Диаметр','1,6 мм'),('Длина бухты','1000 м'),('Покрытие','Оцинковка'),('Скидка','до 10 %')]),
    dict(img='assets/img/cat-nets.jpg',alt='Электросетка в рулоне',name='Электросетка',sub='Для овец, коз и птицы: держит внутри и не пускает хищников снаружи',price='цена по запросу',
         specs=[('Высота','[уточнить]'),('Длина','[уточнить]'),('Цвет','[уточнить]'),('Наличие','[уточнить]')])]),
 'catalog-izolyatory.html':('Изоляторы и колышки','Изолятор не даёт импульсу уйти в столб. Это самая дешёвая часть изгороди и первая причина, по которой линия перестаёт бить.',
   [dict(img='assets/img/cat-insulators.jpg',alt='Изолятор на деревянном столбе',name='Изоляторы',sub='Под проволоку, шнур и ленту, для дерева и металла',price='цена по запросу',
         specs=[('Тип','Кольцевые, угловые'),('Крепление','Шуруп, гвоздь'),('Материал','Полимер'),('Наличие','[уточнить]')]),
    dict(img='assets/img/cat-nets.jpg',alt='Колышки и стойки',name='Колышки и стойки',sub='Переносная изгородь и деление пастбища на загоны',price='цена по запросу',
         specs=[('Высота','[уточнить]'),('Материал','[уточнить]'),('Ушек под линии','[уточнить]'),('Наличие','[уточнить]')])]),
 'catalog-kabeli.html':('Кабели и аксессуары','Всё, что соединяет прибор, линию и землю: кабель высокого напряжения, клеммы, штыри заземления и ворота для прохода техники.',
   [dict(img='assets/img/cat-cables.jpg',alt='Кабели подключения с клеммами',name='Кабель подключения и клеммы',sub='Соединение прибора с линией и заземлением',price='цена по запросу',
         specs=[('Сечение','[уточнить]'),('Длина','[уточнить]'),('Клеммы','В комплекте'),('Наличие','[уточнить]')]),
    dict(img='assets/img/cat-cables.jpg',alt='Ворота для электроизгороди',name='Ворота и ручки',sub='Проход для людей и техники без разбора линии',price='цена по запросу',
         specs=[('Тип','Пружинные'),('Длина','[уточнить]'),('Изоляция','Есть'),('Наличие','[уточнить]')]),
    dict(img='assets/img/insulator.jpg',alt='Штыри заземления',name='Заземление',sub='Штыри и провод. Без хорошего заземления изгородь не работает',price='цена по запросу',
         specs=[('Штырей','[уточнить]'),('Длина штыря','[уточнить]'),('Материал','Оцинковка'),('Наличие','[уточнить]')])]),
 'catalog-solnce.html':('Солнечные системы','Комплект для пастбища без розетки: панель заряжает аккумулятор днём, контроллер бережёт его от перезаряда и глубокого разряда.',
   [dict(img='assets/img/solar-line.jpg',alt='Солнечная панель на линии электроизгороди',name='Солнечная панель',sub='Подбирается под мощность прибора и число солнечных часов',price='цена по запросу',
         specs=[('Мощность','[уточнить]'),('Напряжение','12 В'),('Крепление','На столб'),('Наличие','[уточнить]')]),
    dict(img='assets/img/solar-energizer.jpg',alt='MPPT-контроллер',name='MPPT-контроллер',sub='Бережёт аккумулятор от перезаряда и глубокого разряда',price='цена по запросу',
         specs=[('Тип','MPPT'),('Напряжение','12 В'),('Ток','[уточнить]'),('Наличие','[уточнить]')]),
    dict(img='assets/img/solar-netting.jpg',alt='Аккумулятор 12 В',name='Аккумулятор 12 В',sub='Запас энергии на ночь и пасмурные дни',price='цена по запросу',
         specs=[('Ёмкость','7 Ач и выше'),('Напряжение','12 В'),('Тип','Свинцово-кислотный'),('Наличие','[уточнить]')])]),
 'catalog-strizhka.html':('Оборудование для стрижки овец','Машинки и расходники для сезона стрижки. Ножи затупляются быстро, поэтому запасной комплект берут сразу.',
   [dict(img='assets/img/cat-shearing.jpg',alt='Машинка для стрижки овец',name='Машинка для стрижки овец',sub='Сетевая, для отары среднего размера',price='цена по запросу',
         specs=[('Питание','220 В'),('Мощность','[уточнить]'),('Ножи','В комплекте'),('Наличие','[уточнить]')]),
    dict(img='assets/img/cat-shearing.jpg',alt='Ножи для машинки',name='Ножи и запчасти',sub='Верхний и нижний нож, гребёнки, расходники',price='цена по запросу',
         specs=[('Совместимость','[уточнить]'),('Материал','Сталь'),('В упаковке','[уточнить]'),('Наличие','[уточнить]')])]),
 'catalog-pogonyala.html':('Электропогонялa','Прибор для управления движением животных при перегоне, погрузке и ветеринарных обработках.',
   [dict(img='assets/img/product-gigant15.jpg',alt='Электропогоняло GIGANT',name='Электропогоняло GIGANT',sub='Для КРС, свиней и мелкого рогатого скота',price='44 500 ₸',
         specs=[('Питание','Аккумуляторное'),('Длина','[уточнить]'),('Для кого','КРС, свиньи, МРС'),('Наличие','В наличии')])]),
}
for fname,(title,lead,items) in SIMPLE.items():
    cards=''.join(product_card(i['img'],i['alt'],i['name'],i['sub'],i['price'],i['specs']) for i in items)
    w(fname, f'''
<main id="top">
{crumbs([('Главная','index.html'),('Каталог','catalog.html'),(title,None)])}
{page_head(title, lead)}
<section class="container-site mt-8 md:mt-10">
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
{cards}{helper_card()}
  </div>
  <p class="mt-6 text-[15px] text-muted max-w-[70ch]">Цены и наличие по части позиций уточняйте у менеджера. Напишите в WhatsApp, что нужно: посчитаем количество под ваш периметр и назовём цену.</p>
</section>
{cta_band()}
</main>''')

# ---------- карточка товара ----------
SPEC_TABLE=[('Импульс, Дж','15'),('Максимальное напряжение','12 000 В'),('Питание','Сеть 220 В или аккумулятор 12 В'),
 ('Управление','Пульт дистанционного управления'),
 ('Габариты','250 × 200 × 50 мм'),('Вес','5 кг'),('Для кого','КРС, овцы, козы'),
 ('Производство','Россия'),('Гарантия','1 год')]
spec_rows=''.join(f'<div class="flex justify-between gap-6 border-b border-line py-3"><dt class="text-muted">{k}</dt><dd class="font-bold text-right">{v}</dd></div>' for k,v in SPEC_TABLE)

w('product-gigant-15.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Каталог','catalog.html'),('Электропастухи','catalog-elektropastuhi.html'),('GIGANT 15&nbsp;Дж',None)])}
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Product","name":"Электропастух GIGANT 15 Дж","brand":{{"@type":"Brand","name":"GIGANT"}},"category":"Электропастухи","image":"https://farik9797.github.io/gigant-agro-site/assets/img/product-gigant15.jpg","description":"Генератор импульсов для электроизгороди: 15 Дж, 12 000 В, питание 220 В и 12 В, пульт ДУ, гарантия 1 год.","offers":{{"@type":"Offer","price":"105000","priceCurrency":"KZT","availability":"https://schema.org/InStock","url":"https://farik9797.github.io/gigant-agro-site/product-gigant-15.html","seller":{{"@type":"Organization","name":"GIGANT Agro"}}}}}}</script>
<section class="container-site mt-6 md:mt-8 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
  <div class="lg:col-span-7">
    <div class="card overflow-hidden">
      <div class="relative bg-white aspect-[4/3]">
        <img src="assets/img/product-gigant15.jpg" alt="Электропастух GIGANT 15 Дж с адаптером, пультом и клеммами" class="absolute inset-0 w-full h-full object-contain p-6" fetchpriority="high" width="800" height="600">
        <span class="absolute left-4 top-4 rounded-full bg-cream text-brand-dark text-[13px] font-bold px-2.5 py-1">Собственная марка</span>
      </div>
    </div>
  </div>
  <div class="lg:col-span-5">
    <h1 class="font-black text-[clamp(1.8rem,3vw,2.4rem)] leading-[1.05] tracking-[-0.02em]">Электропастух GIGANT 15&nbsp;Дж</h1>
    <p class="lead mt-3">Флагман собственной марки. Держит стандартное хозяйство с КРС, овцами и козами, работает от сети и от аккумулятора, управляется пультом.</p>
    <div class="mt-6 flex flex-wrap items-center gap-3">
      <p class="font-black text-[32px] leading-none tabular-nums">105 000 ₸</p>
      <span class="inline-flex items-center gap-1.5 rounded-full bg-cream text-brand-dark text-[14px] font-bold px-3 py-1.5"><i data-lucide="check" class="w-4 h-4" aria-hidden="true"></i>В наличии</span>
    </div>
    <div class="mt-6 grid grid-cols-3 gap-3">
      <div class="card p-3 text-center"><p class="font-black text-[20px] tabular-nums">15</p><p class="text-[12px] text-muted mt-0.5">Дж</p></div>
      <div class="card p-3 text-center"><p class="font-black text-[20px] tabular-nums">12 000</p><p class="text-[12px] text-muted mt-0.5">В</p></div>
      <div class="card p-3 text-center"><p class="font-black text-[20px]">220/12</p><p class="text-[12px] text-muted mt-0.5">В, питание</p></div>
    </div>
    <div class="mt-6 flex flex-col sm:flex-row gap-3">
      <a href="{order('Электропастух GIGANT 15 Дж')}" class="btn-primary btn-lg">Заказать</a>
      <a href="{wa('Здравствуйте! Интересует электропастух GIGANT 15 Дж за 105 000 ₸.')}" target="_blank" rel="noopener" class="btn-secondary btn-lg"><img src="assets/icons/whatsapp-FFFFFF.svg" alt="" class="w-5 h-5" width="20" height="20">Спросить в WhatsApp</a>
    </div>
    <ul class="mt-6 space-y-2 text-[15px] text-muted">
      <li class="flex gap-2.5"><i data-lucide="truck" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Самовывоз в Алматы в день заказа, доставка по Казахстану и СНГ</li>
      <li class="flex gap-2.5"><i data-lucide="shield-check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Гарантия 1 год, возврат 14 дней по закону РК</li>
      <li class="flex gap-2.5"><i data-lucide="wrench" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Поможем с монтажом и заземлением по телефону и в WhatsApp</li>
    </ul>
  </div>
</section>

<section class="container-site mt-12 md:mt-16 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
  <div class="lg:col-span-7">
    <h2 class="h3">Характеристики</h2>
    <dl class="mt-4 text-[15px]">{spec_rows}</dl>
  </div>
  <div class="lg:col-span-5">
    <h2 class="h3">Комплектация</h2>
    <ul class="mt-4 space-y-2 text-[15px]">
      <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Электропастух</li>
      <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Адаптер питания 220 В</li>
      <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Кабель с клеммами для аккумулятора</li>
      <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Пульт дистанционного управления</li>
      <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Предупреждающие таблички</li>
      <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Инструкция по эксплуатации</li>
    </ul>
    <div class="card p-5 mt-6">
      <p class="font-extrabold">Что докупить</p>
      <p class="text-muted text-[15px] mt-2">Прибор — это только источник импульса. К нему нужен проводник, изоляторы и заземление.</p>
      <div class="mt-4 flex flex-wrap gap-2">
        <a href="catalog-setki.html" class="chip h-10">Сетки и шнуры</a>
        <a href="catalog-izolyatory.html" class="chip h-10">Изоляторы</a>
        <a href="catalog-kabeli.html" class="chip h-10">Заземление</a>
        <a href="catalog-solnce.html" class="chip h-10">Солнечная панель</a>
      </div>
    </div>
  </div>
</section>

<section class="container-site mt-12 md:mt-16">
  <h2 class="h2">Похожие приборы</h2>
  <div id="relScroll" class="m-slider mt-6 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-5" role="group" aria-label="Похожие приборы, прокрутка по горизонтали">
{''.join(product_card(p['img'],p['alt'],p['name'],p['sub'],p['price'],p['specs'],p.get('href'),p.get('badge'),p.get('badge_style','bg-cream text-brand-dark')) for p in PRIBORY[1:])}  </div>
  <div class="md:hidden mt-4 h-1 rounded-full bg-line overflow-hidden" aria-hidden="true"><div id="relProgress" class="h-full rounded-full bg-brand-dark" style="width:34%"></div></div>
</section>
{cta_band('Подобрать комплект с этим прибором','Скажите вид животных и площадь — посчитаем проводник, изоляторы и заземление под ваш периметр.')}
</main>''')

# ---------- подбор комплекта (страница-конфигуратор) ----------
w('podbor.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Подбор комплекта',None)])}
{page_head('Подбор комплекта за минуту', 'Три вопроса — и мы покажем модель электропастуха, состав комплекта и ориентировочную цену. Точный состав и итог подтвердит менеджер.')}
<section class="container-site mt-8 md:mt-10">
  <div class="rounded-2xl bg-cream border border-brand/25 p-5 md:p-8 lg:p-10">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-7 md:gap-8 lg:gap-0">
      <div class="lg:col-span-7 lg:pr-10">
        <fieldset class="pb-6">
          <legend class="flex items-center gap-3 font-extrabold text-[17px]"><span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-white md:bg-cream border border-line md:border-0 text-brand-dark text-[14px] font-black tabular-nums" aria-hidden="true">1</span>Кого держите</legend>
          <div id="pickAnimal" class="mt-4 flex flex-wrap gap-2" role="group" aria-label="Вид животных">
            <button class="chip" data-v="krs" aria-pressed="true">КРС</button>
            <button class="chip" data-v="horse" aria-pressed="false">Лошади</button>
            <button class="chip" data-v="sheep" aria-pressed="false">Овцы и козы</button>
            <button class="chip" data-v="pig" aria-pressed="false">Свиньи</button>
            <button class="chip" data-v="bird" aria-pressed="false">Птица</button>
            <button class="chip" data-v="wild" aria-pressed="false">Дикие животные</button>
          </div>
        </fieldset>
        <fieldset class="mt-2 pb-6">
          <legend class="flex items-center gap-3 font-extrabold text-[17px]"><span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-white md:bg-cream border border-line md:border-0 text-brand-dark text-[14px] font-black tabular-nums" aria-hidden="true">2</span>Сколько земли</legend>
          <div class="mt-4 flex flex-col sm:flex-row sm:items-center gap-3">
            <label class="relative w-full sm:w-36"><span class="sr-only">Площадь или периметр</span><input id="pickArea" type="number" min="0.1" step="0.1" value="5" class="input" inputmode="decimal" aria-describedby="pickAreaHint" autocomplete="off"></label>
            <div id="pickUnit" class="grid grid-cols-2 w-full sm:inline-flex sm:w-auto self-start rounded-xl border border-line bg-white p-1" role="group" aria-label="Единицы">
              <button class="h-10 px-3 sm:px-4 rounded-lg text-[14px] sm:text-[15px] font-medium bg-ink text-white" data-v="ha" aria-pressed="true">гектаров</button>
              <button class="h-10 px-3 sm:px-4 rounded-lg text-[14px] sm:text-[15px] font-medium whitespace-nowrap" data-v="m" aria-pressed="false">метров периметра</button>
            </div>
          </div>
          <p id="pickAreaHint" class="mt-3 text-[14px] text-muted">Не знаете периметр — укажите площадь, мы посчитаем.</p>
        </fieldset>
        <fieldset class="mt-2">
          <legend class="flex items-center gap-3 font-extrabold text-[17px]"><span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-white md:bg-cream border border-line md:border-0 text-brand-dark text-[14px] font-black tabular-nums" aria-hidden="true">3</span>Откуда питание</legend>
          <div id="pickPower" class="mt-4 flex flex-wrap gap-2" role="group" aria-label="Источник питания">
            <button class="chip" data-v="220" aria-pressed="true">Розетка 220&nbsp;В</button>
            <button class="chip" data-v="12" aria-pressed="false">Аккумулятор 12&nbsp;В</button>
            <button class="chip" data-v="sun" aria-pressed="false">Солнечная панель</button>
          </div>
        </fieldset>
      </div>
      <div class="lg:col-span-5 lg:pl-10 lg:border-l lg:border-brand/25 flex flex-col gap-5">
        <div>
          <button id="pickGo" class="btn-primary btn-lg w-full">Показать решение<i data-lucide="arrow-right" class="w-5 h-5" aria-hidden="true"></i></button>
          <p class="mt-3 text-[14px] text-muted">Результат ориентировочный, точный состав подтвердит менеджер.</p>
        </div>
        <div id="pickResult" aria-live="polite" tabindex="-1" class="flex-1 rounded-2xl bg-white border border-line p-5 md:p-6 outline-none">
          <div id="resEmpty" class="h-full min-h-[200px] hidden md:flex flex-col items-center justify-center text-center gap-3 text-muted">
            <i data-lucide="sliders-horizontal" class="w-8 h-8 text-brand-dark" aria-hidden="true"></i>
            <p class="text-[15px] max-w-[26ch]">Выберите животных, площадь и питание — здесь появится модель, комплект и цена.</p>
          </div>
          <div id="resBody" hidden>
            <div class="flex flex-wrap items-start justify-between gap-x-6 gap-y-2">
              <div class="min-w-0"><p class="text-[13px] font-semibold text-brand-dark">Рекомендуем</p><p id="resModel" class="h3 mt-1"></p></div>
              <p id="resPrice" class="font-black text-[28px] leading-none tabular-nums whitespace-nowrap"></p>
            </div>
            <p id="resKit" class="mt-3 text-muted"></p>
            <p id="resPower" class="mt-1 text-muted"></p>
            <p id="resWhy" class="mt-2 text-[14px] text-muted"></p>
            <div class="mt-5 flex flex-col gap-2">
              <a id="resOrder" href="kontakty.html#leadForm" class="btn-primary">Заказать</a>
              <a id="resWa" href="#" target="_blank" rel="noopener" class="btn-secondary"><img src="assets/icons/whatsapp-FFFFFF.svg" alt="" class="w-5 h-5" width="20" height="20">Обсудить в WhatsApp</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="container-site mt-12 md:mt-16">
  <h2 class="h2">Как мы считаем</h2>
  <div class="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-5">
    <div class="card p-5"><p class="font-extrabold">Периметр из площади</p><p class="text-muted text-[15px] mt-2">Для участка, близкого к квадрату: 1 га — около 400 м, 5 га — около 900 м, 6 га — около 980 м. Вытянутый участок при той же площади даёт больший периметр.</p></div>
    <div class="card p-5"><p class="font-extrabold">Длина проводника</p><p class="text-muted text-[15px] mt-2">Периметр умножаем на число линий. Крупным спокойным животным хватает одной-двух, овцам и козам нужно четыре-пять или готовая сетка.</p></div>
    <div class="card p-5"><p class="font-extrabold">Запас мощности</p><p class="text-muted text-[15px] mt-2">Густая трава и длинная линия съедают импульс. Поэтому для больших периметров и защиты от диких животных берут 25&nbsp;Дж, а не 15.</p></div>
  </div>
</section>
{cta_band('Хотите обсудить голосом?','Позвоните или напишите в WhatsApp: уточним вид животных, форму участка и подберём комплект без формы.')}
</main>''')

# ---------- как выбрать (гид) ----------
TOC=[('power','Мощность в джоулях'),('perimeter','Периметр и площадь'),('lines','Сколько линий'),
     ('conductor','Проводник'),('ground','Заземление'),('supply','Питание'),('table','Таблица по животным')]
toc_html=''.join(f'<li><a href="#{i}" class="hover:text-ink">{t}</a></li>' for i,t in TOC)
ANIMAL_TABLE=[('КРС','1–2','Проволока 1,6 мм или шнур 6 жил','GIGANT 15 · Bekci 25','«Для КРС», 5 га'),
 ('Лошади','2–3','Лента или шнур 6 жил','GIGANT 15 · Bekci 25','«Для лошадей», 6 га'),
 ('Овцы и козы','4–5 или сетка','Электросетка или шнур 6 жил','Bekci 14,5 · GIGANT 15','«Для овец», 1 га'),
 ('Свиньи','2–3, низко','Проволока или шнур','GIGANT 15','Под периметр'),
 ('Птица','Сетка','Электросетка','Bekci 6,9 · GIGANT 15','Под периметр'),
 ('Дикие животные','3–4, от земли','Проволока 1,6 мм','Bekci 25','Под периметр')]
animal_cards=''.join(f'''<div class="card p-4"><h3 class="font-extrabold text-[17px]">{a}</h3><dl class="mt-3 grid grid-cols-[auto,1fr] gap-x-4 gap-y-1.5 text-[15px]"><dt class="text-muted">Линий</dt><dd class="font-semibold tabular-nums">{l}</dd><dt class="text-muted">Проводник</dt><dd class="font-semibold">{c}</dd><dt class="text-muted">Прибор</dt><dd class="font-semibold">{d}</dd><dt class="text-muted">Комплект</dt><dd class="font-semibold">{k}</dd></dl></div>''' for a,l,c,d,k in ANIMAL_TABLE)
rows=''.join(f'<tr class="border-b border-line"><th scope="row" class="text-left font-bold py-3 pr-4">{a}</th><td class="py-3 pr-4 tabular-nums">{l}</td><td class="py-3 pr-4">{c}</td><td class="py-3 pr-4">{d}</td><td class="py-3">{k}</td></tr>' for a,l,c,d,k in ANIMAL_TABLE)

w('kak-vybrat.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Как выбрать электропастух',None)])}
{page_head('Как выбрать электропастух', 'Шесть параметров решают всё: мощность, периметр, число линий, проводник, заземление и питание. Ниже — как их определить для своего хозяйства.')}
<section class="container-site mt-8 md:mt-10 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
  <div class="lg:col-span-3">
    <nav aria-label="Содержание" class="lg:sticky lg:top-28 card p-5">
      <p class="font-extrabold text-[15px]">Содержание</p>
      <ol class="mt-3 space-y-2 text-[15px] text-muted list-decimal list-inside">{toc_html}</ol>
      <a href="podbor.html" class="btn-primary w-full mt-5">Подобрать за минуту</a>
    </nav>
  </div>
  <div class="lg:col-span-9 space-y-10">
    <article id="power" class="scroll-mt-28"><h2 class="h3">Мощность в джоулях</h2>
      {prose('<p class="mt-3">Джоуль — это энергия одного импульса. Чем длиннее линия и гуще трава, которая касается проводника, тем больше энергии теряется по дороге и тем мощнее нужен прибор.</p><p class="mt-3">Ориентир: небольшой загон со спокойными животными — 6,9&nbsp;Дж; стандартное хозяйство с КРС, лошадьми или овцами — 14,5–15&nbsp;Дж; большой периметр, густая растительность и защита от диких животных — 25&nbsp;Дж. Запас мощности лишним не бывает, недостаток — бывает.</p>')}
    </article>
    <article id="perimeter" class="scroll-mt-28"><h2 class="h3">Периметр и площадь</h2>
      {prose('<p class="mt-3">Прибор работает с длиной линии, а не с площадью. Для участка, близкого к квадрату, 1 га — это около 400 м периметра, 5 га — около 900 м, 6 га — около 980 м.</p><p class="mt-3">Вытянутый участок при той же площади даёт периметр заметно больше. Поэтому при подборе мы спрашиваем и площадь, и форму участка.</p>')}
    </article>
    <article id="lines" class="scroll-mt-28"><h2 class="h3">Сколько линий</h2>
      {prose('<p class="mt-3">Число линий зависит от роста и характера животного. Крупным и спокойным хватает одной-двух на уровне груди. Мелким и активным — овцам, козам, свиньям — нужно больше линий и ниже к земле, либо готовая электросетка.</p><p class="mt-3">Длина проводника считается просто: периметр умножить на число линий. Для 5 га в две линии это около 1800 м.</p>')}
    </article>
    <article id="conductor" class="scroll-mt-28"><h2 class="h3">Проводник</h2>
      {prose('<p class="mt-3">Проволока 1,6 мм дешевле и лучше проводит ток на длинных периметрах, но хуже заметна. Шнур из шести жил и лента животное видит издалека, поэтому их берут для лошадей и для новых загонов.</p><p class="mt-3">Для овец, коз и птицы проще поставить готовую электросетку: она держит животных внутри и не пускает лис и собак снаружи.</p>')}
      <p class="mt-4"><a href="catalog-setki.html" class="link">Сетки и шнуры в каталоге<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a></p>
    </article>
    <article id="ground" class="scroll-mt-28"><h2 class="h3">Заземление</h2>
      {prose('<p class="mt-3">Импульс возвращается в прибор через землю. Без хорошего заземления животное почти ничего не чувствует, даже если прибор исправен. Это самая частая причина жалоб «изгородь не бьёт».</p><p class="mt-3">Металлические штыри вбивают во влажный грунт и соединяют с клеммой заземления. В сухом или каменистом грунте штырей нужно больше, и ставят их дальше друг от друга.</p>')}
      <p class="mt-4"><a href="instrukcii.html" class="link">Схемы подключения и заземления<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a></p>
    </article>
    <article id="supply" class="scroll-mt-28"><h2 class="h3">Питание</h2>
      {prose('<p class="mt-3">Есть розетка рядом — берите питание 220 В, это самый простой вариант. Нет розетки — аккумулятор 12 В. Пастбище далеко и надолго — аккумулятор плюс солнечная панель с MPPT-контроллером, чтобы не возить батарею на зарядку.</p><p class="mt-3">Приборы от 14,5 до 25&nbsp;Дж работают от обоих источников, переключение — на корпусе.</p>')}
      <p class="mt-4"><a href="catalog-solnce.html" class="link">Солнечные системы<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a></p>
    </article>
    <article id="table" class="scroll-mt-28"><h2 class="h3">Таблица по животным</h2>
      <div class="mt-4 space-y-3 md:hidden">{animal_cards}</div>
      <div class="mt-4 overflow-x-auto hidden md:block"><table class="w-full min-w-[640px] text-[15px]">
        <thead><tr class="border-b-2 border-ink"><th scope="col" class="text-left font-extrabold py-3 pr-4">Животные</th><th scope="col" class="text-left font-extrabold py-3 pr-4">Линий</th><th scope="col" class="text-left font-extrabold py-3 pr-4">Проводник</th><th scope="col" class="text-left font-extrabold py-3 pr-4">Прибор</th><th scope="col" class="text-left font-extrabold py-3">Комплект</th></tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
      <p class="mt-4 text-[14px] text-muted max-w-[70ch]">Таблица — обычная практика для ориентира. Высоты линий и точные количества подтверждаем при подборе.</p>
    </article>
  </div>
</section>
{cta_band()}
</main>''')

# ---------- инструкции и схемы ----------
STEPS=[('Разметьте периметр','Обойдите участок и отметьте углы. Столбы ставят чаще там, где линия поворачивает: на углах натяжение выше.'),
 ('Поставьте столбы и изоляторы','Изолятор крепят так, чтобы проводник не касался дерева или металла. На углах ставят угловые изоляторы.'),
 ('Натяните проводник','Линию натягивают без провисания, но и без перетяга: на жаре материал расширяется. Между секциями оставляют соединители.'),
 ('Сделайте заземление','Штыри вбивают во влажный грунт на расстоянии друг от друга и соединяют проводом с клеммой заземления прибора.'),
 ('Подключите прибор','Один выход — на линию, второй — на заземление. Питание подключают последним: от сети 220 В, аккумулятора или солнечной панели.'),
 ('Проверьте напряжение','Тестером на дальней точке линии. Если напряжение просело — ищите касание травы, плохой изолятор или слабое заземление.')]
steps_html=''.join(f'''<li class="relative md:pl-20 py-6 border-b border-line last:border-0">
  <span class="hidden md:flex absolute left-0 top-6 w-12 h-12 rounded-full bg-cream border-2 border-brand items-center justify-center font-black text-brand-dark tabular-nums" aria-hidden="true">{i}</span>
  <h3 class="h3 flex items-center gap-3"><span class="md:hidden inline-flex shrink-0 w-9 h-9 rounded-full bg-cream border-2 border-brand items-center justify-center font-black text-brand-dark text-[15px] tabular-nums" aria-hidden="true">{i}</span>{t}</h3>
  <p class="mt-2 pl-12 md:pl-0 text-muted max-w-[62ch]">{d}</p>
</li>''' for i,(t,d) in enumerate(STEPS,1))

w('instrukcii.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Инструкции и схемы',None)])}
{page_head('Инструкции и схемы подключения', 'Порядок установки электроизгороди от разметки до проверки напряжения. К каждому прибору идёт своя инструкция, здесь — общая последовательность.')}
<section class="container-site mt-8 md:mt-10 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
  <div class="lg:col-span-5">
    <div class="md:grid md:grid-cols-2 md:gap-5 md:items-center lg:block lg:sticky lg:top-28">
      <div class="rounded-2xl overflow-hidden aspect-[4/3]"><img src="assets/img/insulator.jpg" alt="Изолятор на столбе держит проволоку электроизгороди" class="w-full h-full object-cover" loading="lazy" width="900" height="900"></div>
      <div class="card p-5 mt-5 md:mt-0 lg:mt-5">
        <p class="font-extrabold">Нужна инструкция к прибору?</p>
        <p class="text-muted text-[15px] mt-2">Напишите модель прибора — пришлём инструкцию и схему подключения в WhatsApp.</p>
        <a href="{wa('Здравствуйте! Нужна инструкция по подключению электропастуха.')}" target="_blank" rel="noopener" class="btn-secondary w-full mt-4"><img src="assets/icons/whatsapp-FFFFFF.svg" alt="" class="w-5 h-5" width="20" height="20">Спросить в WhatsApp</a>
      </div>
    </div>
  </div>
  <div class="lg:col-span-7"><h2 class="h3">Порядок установки</h2>
  <ol class="mt-2">{steps_html}</ol></div>
</section>

<section class="container-site mt-12 md:mt-16">
  <h2 class="h2">Частые ошибки</h2>
  <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-5">
    <div class="card p-5"><p class="font-extrabold">Экономия на заземлении</p><p class="text-muted text-[15px] mt-2">Один короткий штырь в сухом грунте — и линия почти не бьёт. Это половина всех обращений.</p></div>
    <div class="card p-5"><p class="font-extrabold">Трава на линии</p><p class="text-muted text-[15px] mt-2">Заросшая нижняя линия сажает импульс. Подкос под изгородью решает проблему лучше, чем более мощный прибор.</p></div>
    <div class="card p-5"><p class="font-extrabold">Дешёвые изоляторы</p><p class="text-muted text-[15px] mt-2">Треснувший изолятор уводит ток в столб. Замена стоит копейки, поиск неисправности — полдня.</p></div>
  </div>
</section>
{cta_band('Не получается запустить линию?','Опишите, что происходит: не бьёт совсем, бьёт слабо или только на части периметра. Подскажем, что проверить.')}
</main>''')

# ---------- доставка и оплата ----------
w('dostavka.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Доставка и оплата',None)])}
{page_head('Доставка и оплата', 'Основной ассортимент — на складе в Алматы. Забирайте сами в день заказа или отправим транспортной компанией в любой регион.')}
<section class="container-site mt-8 md:mt-10 grid grid-cols-1 md:grid-cols-2 gap-5">
  <div class="card p-6"><i data-lucide="map-pin" class="w-7 h-7 text-brand-dark" aria-hidden="true"></i>
    <h2 class="h3 mt-4">Самовывоз в Алматы</h2>
    <p class="text-muted mt-2">Мкр. Атырау, 159/8, склад №&nbsp;1. Пн–Пт 10:00–18:00, Сб 10:00–16:00, воскресенье выходной. Наличие лучше уточнить заранее в WhatsApp — отложим товар.</p>
    <a href="kontakty.html" class="link mt-4">Как проехать<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a>
  </div>
  <div class="card p-6"><i data-lucide="truck" class="w-7 h-7 text-brand-dark" aria-hidden="true"></i>
    <h2 class="h3 mt-4">Доставка по Казахстану и СНГ</h2>
    <p class="text-muted mt-2">Отправляем транспортными компаниями во все регионы Казахстана, а также в Россию и страны СНГ. Стоимость и срок считаем индивидуально по весу, габаритам и городу.</p>
    <p class="text-muted mt-2">Отгрузка после полной оплаты. Номер накладной присылаем в WhatsApp.</p>
  </div>
  <div class="card p-6"><i data-lucide="credit-card" class="w-7 h-7 text-brand-dark" aria-hidden="true"></i>
    <h2 class="h3 mt-4">Оплата</h2>
    <p class="text-muted mt-2">Наличными на складе или безналичным переводом по реквизитам — для ИП и юридических лиц выставляем счёт.</p>
  </div>
  <div class="card p-6"><i data-lucide="store" class="w-7 h-7 text-brand-dark" aria-hidden="true"></i>
    <h2 class="h3 mt-4">Покупка на маркетплейсах</h2>
    <p class="text-muted mt-2">Привычнее покупать на площадке — мы там есть. Условия доставки и оплаты в этом случае определяет маркетплейс.</p>
    <div class="mt-4 flex flex-wrap gap-2">
      <a href="https://elektropastuh.satu.kz/" target="_blank" rel="noopener" class="chip h-10">Satu.kz</a>
      <a href="https://www.ozon.ru/product/elektropastuh-gigant-15-dzh-dlya-korov-ovets-loshadey-kabanov-1632680883/" target="_blank" rel="noopener" class="chip h-10">Ozon</a>
      <a href="https://www.wildberries.ru/catalog/694923616/detail.aspx" target="_blank" rel="noopener" class="chip h-10">Wildberries</a>
    </div>
  </div>
</section>
<section class="container-site mt-10">
  <div class="rounded-2xl bg-cream border border-brand/25 p-6 md:p-8">
    <h2 class="h3">Как проходит заказ</h2>
    <ol class="mt-5 grid grid-cols-1 md:grid-cols-4 gap-5 text-[15px]">
      <li><p class="font-extrabold text-brand-dark">01</p><p class="font-bold mt-1">Заявка</p><p class="text-muted mt-1">Через форму, WhatsApp или по телефону.</p></li>
      <li><p class="font-extrabold text-brand-dark">02</p><p class="font-bold mt-1">Подбор</p><p class="text-muted mt-1">Уточняем животных, площадь, линии и питание.</p></li>
      <li><p class="font-extrabold text-brand-dark">03</p><p class="font-bold mt-1">Оплата</p><p class="text-muted mt-1">Наличными на складе или переводом по счёту.</p></li>
      <li><p class="font-extrabold text-brand-dark">04</p><p class="font-bold mt-1">Отгрузка</p><p class="text-muted mt-1">Самовывоз или транспортная компания.</p></li>
    </ol>
  </div>
</section>
{cta_band('Посчитать доставку','Напишите город и что заказываете — узнаем стоимость у транспортной компании и вернёмся с цифрой.')}
</main>''')

# ---------- гарантия и возврат ----------
w('garantiya.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Гарантия и возврат',None)])}
{page_head('Гарантия, возврат и обмен', 'Гарантийный срок зависит от марки прибора. Возврат и обмен — в рамках закона Республики Казахстан «О защите прав потребителей».')}
<section class="container-site mt-8 md:mt-10 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
  <div class="lg:col-span-7 space-y-8">
    <article><h2 class="h3">Сроки гарантии</h2>
      <dl class="mt-4 text-[15px]">
        <div class="flex justify-between gap-6 border-b border-line py-3"><dt class="text-muted">Электропастухи GIGANT</dt><dd class="font-bold">1 год</dd></div>
        <div class="flex justify-between gap-6 border-b border-line py-3"><dt class="text-muted">Электропастухи Bekci</dt><dd class="font-bold">2 года</dd></div>
      </dl>
    </article>
    <article><h2 class="h3">Что покрывает гарантия</h2>
      {prose('<p class="mt-3">Производственный брак и отказ электроники при нормальной эксплуатации. Для гарантийного случая прибор проверяют: смотрят следы вскрытия, подключения не по инструкции, попадания воды и удара молнии.</p><p class="mt-3">Не считаются гарантийными: механические повреждения корпуса, выход из строя из-за неправильного подключения питания, работа без заземления и повреждения от грозы. Расходники — проводник, изоляторы, аккумулятор — изнашиваются и под гарантию не попадают.</p>')}
    </article>
    <article><h2 class="h3">Возврат и обмен</h2>
      {prose('<p class="mt-3">Товар надлежащего качества можно вернуть или обменять в течение 14 дней, если он не был в употреблении, сохранены товарный вид, упаковка, пломбы и есть документ о покупке.</p><p class="mt-3">Товар с недостатком принимаем на проверку. Срок проверки и порядок возврата денег — по закону РК «О защите прав потребителей».</p>')}
    </article>
    <article><h2 class="h3">Как обратиться</h2>
      {prose('<p class="mt-3">Напишите в WhatsApp или позвоните: опишите, что произошло, и приложите фото прибора и места подключения. Часто проблема решается по переписке — чаще всего дело в заземлении или в касании травы.</p>')}
      <div class="mt-5 flex flex-col sm:flex-row gap-3">
        <a href="{wa('Здравствуйте! Вопрос по гарантии на электропастух.')}" target="_blank" rel="noopener" class="btn-secondary"><img src="assets/icons/whatsapp-FFFFFF.svg" alt="" class="w-5 h-5" width="20" height="20">Написать в WhatsApp</a>
        <a href="tel:+77054285707" class="btn-outline"><i data-lucide="phone" class="w-5 h-5" aria-hidden="true"></i>+7 (705) 428-57-07</a>
      </div>
    </article>
  </div>
  <div class="lg:col-span-5">
    <div class="lg:sticky lg:top-28 card p-6">
      <p class="font-extrabold text-[17px]">Что подготовить</p>
      <ul class="mt-4 space-y-2.5 text-[15px] text-muted">
        <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Чек или номер заказа</li>
        <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Фото прибора и подключения</li>
        <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Описание: не бьёт совсем, слабо или на части линии</li>
        <li class="flex gap-2.5"><i data-lucide="check" class="w-5 h-5 text-brand-dark shrink-0" aria-hidden="true"></i>Сколько штырей заземления и какой грунт</li>
      </ul>
    </div>
  </div>
</section>
{cta_band('Прибор не бьёт?','Перед возвратом проверим вместе заземление, изоляторы и траву на линии. Чаще всего проблема решается за один разговор.')}
</main>''')

# ---------- о компании ----------
w('o-kompanii.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('О компании',None)])}
{page_head('О компании', 'GIGANT Agro продаёт электропастухи, электроизгороди и комплектующие фермерам Казахстана. Склад в Алматы, работаем в розницу и оптом.')}
<section class="container-site mt-8 md:mt-10 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
  <div class="lg:col-span-7 space-y-8">
    <article>{prose('<p>Мы продаём не отдельный прибор, а рабочее решение. Клиент звонит с задачей: двадцать коров на пяти гектарах, розетки рядом нет. Наша работа — перевести это в конкретный список: какой электропастух, сколько метров проводника, сколько изоляторов, какое заземление и чем всё это питать.</p><p class="mt-4">Поэтому подбор комплекта у нас стоит на первом месте, а не каталог с сорока фильтрами. После покупки сопровождаем монтаж: по телефону и в WhatsApp разбираем схему подключения и помогаем найти причину, если линия бьёт слабо.</p>')}</article>
    <article><h2 class="h3">Чем торгуем</h2>
      {prose('<p class="mt-3">Собственная марка GIGANT — электропастухи производства России, флагман на 15&nbsp;Дж. Турецкая марка Bekci закрывает линейку от 6,9 до 25&nbsp;Дж. Плюс всё, без чего изгородь не работает: проводники, изоляторы, колышки, кабели, заземление, аккумуляторы и солнечные панели. Отдельно — оборудование для стрижки овец и электропогонялa.</p>')}
      <a href="catalog.html" class="link mt-4">Смотреть каталог<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a>
    </article>
    <article><h2 class="h3">Как работаем</h2>
      <ol class="mt-4 space-y-3 text-[15px]">
        <li class="flex gap-3"><span class="font-black text-brand-dark tabular-nums shrink-0">01</span><span>Вы оставляете заявку или пишете в WhatsApp.</span></li>
        <li class="flex gap-3"><span class="font-black text-brand-dark tabular-nums shrink-0">02</span><span>Менеджер уточняет вид животных, площадь и периметр, число линий и источник питания.</span></li>
        <li class="flex gap-3"><span class="font-black text-brand-dark tabular-nums shrink-0">03</span><span>Подбираем комплект и согласуем цену, оплату и доставку.</span></li>
        <li class="flex gap-3"><span class="font-black text-brand-dark tabular-nums shrink-0">04</span><span>Отгружаем со склада и помогаем с установкой.</span></li>
      </ol>
    </article>
  </div>
  <div class="lg:col-span-5 space-y-5">
    <div class="rounded-2xl overflow-hidden aspect-[4/3]"><img src="assets/img/why-cow-fence.jpg" alt="Коровы на пастбище за линиями электроизгороди" class="w-full h-full object-cover" loading="lazy" width="1920" height="1115"></div>
    <div class="card p-6">
      <p class="font-extrabold text-[17px]">Коротко</p>
      <dl class="mt-4 text-[15px]">
        <div class="flex justify-between gap-6 border-b border-line py-2.5"><dt class="text-muted">Город</dt><dd class="font-bold">Алматы</dd></div>
        <div class="flex justify-between gap-6 border-b border-line py-2.5"><dt class="text-muted">Склад</dt><dd class="font-bold text-right">Мкр. Атырау, 159/8</dd></div>
        <div class="flex justify-between gap-6 border-b border-line py-2.5"><dt class="text-muted">Отгрузка</dt><dd class="font-bold">В день заказа</dd></div>
        <div class="flex justify-between gap-6 border-b border-line py-2.5"><dt class="text-muted">Продажи</dt><dd class="font-bold">Опт и розница</dd></div>
        <div class="flex justify-between gap-6 border-b border-line py-2.5"><dt class="text-muted">География</dt><dd class="font-bold text-right">Казахстан, РФ и СНГ</dd></div>
      </dl>
    </div>
    <div class="card p-6">
      <p class="font-extrabold text-[17px]">Мы на площадках</p>
      <div class="mt-3 flex flex-wrap gap-2">
        <a href="https://elektropastuh.satu.kz/" target="_blank" rel="noopener" class="chip h-10">Satu.kz</a>
        <a href="https://www.ozon.ru/product/elektropastuh-gigant-15-dzh-dlya-korov-ovets-loshadey-kabanov-1632680883/" target="_blank" rel="noopener" class="chip h-10">Ozon</a>
        <a href="https://www.wildberries.ru/catalog/694923616/detail.aspx" target="_blank" rel="noopener" class="chip h-10">Wildberries</a>
      </div>
    </div>
  </div>
</section>
{cta_band('Оптовым покупателям','Работаем с хозяйствами и перепродажей. Напишите объём и позиции — пришлём условия.')}
</main>''')

# ---------- контакты ----------
w('kontakty.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Контакты',None)])}
{page_head('Контакты', 'Склад и выдача заказов в Алматы. Звоните или пишите в WhatsApp — отвечаем в рабочее время в течение часа.')}
<section class="container-site mt-8 md:mt-10 pb-14 md:pb-24 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12">
  <div class="lg:col-span-5 space-y-5">
    <div class="card p-6">
      <h2 class="h3">GIGANT Agro</h2>
      <dl class="mt-4 space-y-4 text-[16px]">
        <div><dt class="text-[13px] text-muted">Телефоны</dt>
          <dd class="mt-1 flex flex-col gap-1"><a href="tel:+77054285707" class="font-bold hover:underline">+7 (705) 428-57-07</a><a href="tel:+77757716024" class="font-bold hover:underline">+7 (775) 771-60-24</a></dd></div>
        <div><dt class="text-[13px] text-muted">WhatsApp</dt>
          <dd class="mt-1"><a href="{wa('Здравствуйте!')}" target="_blank" rel="noopener" class="link">Написать в WhatsApp<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a></dd></div>
        <div><dt class="text-[13px] text-muted">Адрес склада</dt>
          <dd class="mt-1 font-bold">Алматы, мкр. Атырау, 159/8,<br>склад №&nbsp;1</dd></div>
        <div><dt class="text-[13px] text-muted">Часы работы</dt>
          <dd class="mt-1">Пн–Пт 10:00–18:00<br>Сб 10:00–16:00<br>Вс — выходной</dd></div>
      </dl>
    </div>
    <div class="card p-6">
      <p class="font-extrabold">Как добраться</p>
      <p class="text-muted text-[15px] mt-2">Микрорайон Атырау, дом 159/8, склад №&nbsp;1. Перед выездом напишите в WhatsApp — подскажем ориентиры и проверим наличие.</p>
      <a href="https://2gis.kz/almaty/search/%D0%BC%D0%B8%D0%BA%D1%80%D0%BE%D1%80%D0%B0%D0%B9%D0%BE%D0%BD%20%D0%90%D1%82%D1%8B%D1%80%D0%B0%D1%83%20159%2F8" target="_blank" rel="noopener" class="btn-outline w-full mt-4"><i data-lucide="map-pin" class="w-5 h-5 text-brand-dark" aria-hidden="true"></i>Открыть адрес в 2ГИС</a>
    </div>
  </div>
  <div class="lg:col-span-7">
    <form id="leadForm" class="card p-6 md:p-8 grid grid-cols-1 sm:grid-cols-2 gap-4" novalidate>
      <h2 class="sm:col-span-2 h3">Оставить заявку</h2>
      <p class="sm:col-span-2 text-muted text-[15px] -mt-2">Опишите хозяйство — подберём модель, число линий и питание. Перезвоним в рабочее время.</p>
      <div id="formTovar" hidden class="sm:col-span-2 flex items-center justify-between gap-3 rounded-xl bg-cream border border-brand/30 px-4 py-3 text-[15px]"><span>Товар: <strong data-tovar-name></strong></span><button type="button" id="formTovarClear" class="text-[14px] font-semibold text-brand-dark hover:underline">Убрать</button><input type="hidden" name="tovar" id="formTovarValue" value=""></div>
      <div><label for="fName" class="block text-[14px] font-semibold">Имя</label><input id="fName" type="text" name="name" class="input mt-1.5" placeholder="Как к вам обращаться…" required autocomplete="name" aria-describedby="nameErr"><p id="nameErr" class="mt-1.5 text-[14px] text-danger" hidden></p></div>
      <div><label for="fPhone" class="block text-[14px] font-semibold">Телефон</label><input id="fPhone" type="tel" name="phone" class="input mt-1.5" placeholder="+7 (705) 000-00-00" required inputmode="tel" autocomplete="tel" aria-describedby="phoneErr"><p id="phoneErr" class="mt-1.5 text-[14px] text-danger" hidden></p></div>
      <div class="sm:col-span-2">
        <span id="formAnimalsLabel" class="text-[14px] font-semibold">Животные</span>
        <input type="hidden" name="animals" id="formAnimalsValue" value="">
        <div class="mt-1.5 flex flex-wrap gap-2" id="formAnimals" role="group" aria-labelledby="formAnimalsLabel">
          <button type="button" class="chip h-10" data-v="КРС" aria-pressed="false">КРС</button>
          <button type="button" class="chip h-10" data-v="Лошади" aria-pressed="false">Лошади</button>
          <button type="button" class="chip h-10" data-v="Овцы и козы" aria-pressed="false">Овцы и козы</button>
          <button type="button" class="chip h-10" data-v="Свиньи" aria-pressed="false">Свиньи</button>
          <button type="button" class="chip h-10" data-v="Птица" aria-pressed="false">Птица</button>
          <button type="button" class="chip h-10" data-v="Дикие" aria-pressed="false">От диких животных</button>
        </div>
      </div>
      <div><label for="fArea" class="block text-[14px] font-semibold">Площадь, га</label><input id="fArea" type="number" name="area" class="input mt-1.5" placeholder="Например, 5…" min="0" step="0.1" inputmode="decimal" autocomplete="off"></div>
      <div><label for="fPower" class="block text-[14px] font-semibold">Питание</label><select id="fPower" name="power" class="input mt-1.5" autocomplete="off"><option>220 В</option><option>12 В аккумулятор</option><option>Солнечная панель</option><option>Не знаю</option></select></div>
      <div class="sm:col-span-2"><label class="flex items-start gap-3 text-[14px] text-muted cursor-pointer"><input type="checkbox" name="consent" class="mt-1 w-4 h-4 accent-[#3E7A34] shrink-0" required aria-describedby="consentErr"><span>Согласен на обработку персональных данных. <a href="policy.html" class="underline hover:text-ink">Политика конфиденциальности</a></span></label><p id="consentErr" class="mt-1.5 text-[14px] text-danger" hidden></p></div>
      <div class="sm:col-span-2 flex flex-col sm:flex-row sm:items-center gap-3">
        <button type="submit" class="btn-primary btn-lg"><img src="assets/icons/whatsapp-16191C.svg" alt="" class="w-5 h-5" width="20" height="20">Отправить в WhatsApp</button>
        <span class="text-[14px] text-muted">Заявка придёт менеджеру в WhatsApp, ответим в рабочее время</span>
      </div>
      <p id="formOk" hidden aria-live="polite" tabindex="-1" class="sm:col-span-2 rounded-xl bg-cream border border-brand/40 p-4 text-[15px]"><strong>Открываем WhatsApp.</strong> Сообщение с вашими данными уже набрано — нажмите «Отправить». Если WhatsApp не открылся, позвоните: <a href="tel:+77054285707" class="font-semibold underline">+7 (705) 428-57-07</a>.</p>
    </form>
  </div>
</section>
</main>''')

# ---------- FAQ ----------
FAQ=[('Какую мощность выбрать?','Для небольших загонов и спокойных животных достаточно 6,9&nbsp;Дж. Для стандартных хозяйств с КРС, лошадьми, овцами — 14,5–15&nbsp;Дж. Для больших периметров, густой травы и защиты от диких животных — 25&nbsp;Дж. Сомневаетесь — напишите нам площадь и вид животных.'),
 ('Как рассчитать периметр по площади?','Периметр зависит от формы участка. Для квадратного участка 1 га это около 400 м, 5 га — около 900 м, 6 га — около 980 м. Умножьте периметр на число линий — получите длину проводника. Вытянутый участок потребует больше.'),
 ('Сколько линий нужно?','Крупным спокойным животным обычно хватает одной-двух линий. Мелким и активным — овцам, козам, свиньям — нужно больше линий и ниже к земле, либо готовая электросетка. Точное число и высоты подскажем при подборе.'),
 ('Как сделать заземление?','Заземление — половина успеха: без него импульс слабый. Металлические штыри вбивают во влажный грунт и соединяют с клеммой заземления прибора. В сухом или каменистом грунте штырей нужно больше. Схема есть в инструкции к каждому прибору.'),
 ('12 В, 220 В или солнечная панель?','Есть розетка рядом — 220 В. Нет — аккумулятор 12 В. Пастбище далеко и надолго — аккумулятор плюс солнечная панель, чтобы не возить его на зарядку. Приборы 14,5–25&nbsp;Дж работают от обоих источников.'),
 ('Сложно ли установить самому?','Нет. Стандартный комплект ставится за несколько часов: столбики, изоляторы, проводник, заземление, прибор. Мы консультируем по телефону и в WhatsApp на каждом этапе.'),
 ('Какая гарантия и возврат?','GIGANT 15 — 1 год, Bekci — 2 года. Возврат и обмен в течение 14 дней по закону РК «О защите прав потребителей» при наличии чека и товарного вида.'),
 ('Как и сколько идёт доставка?','Самовывоз со склада в Алматы — в день заказа. По регионам Казахстана — транспортными компаниями после полной оплаты, стоимость и срок рассчитываем индивидуально. Отправляем также в Россию и страны СНГ.'),
 ('Безопасна ли изгородь для животных и людей?','Да, при правильном монтаже. Импульс короткий и повторяется примерно раз в секунду — животное успевает отойти. Стадо запоминает границу за один-два дня. По периметру ставят предупреждающие таблички.'),
 ('Работает ли изгородь зимой?','Работает, но заземление в мёрзлом грунте хуже проводит ток. Штырей ставят больше и вбивают глубже, ниже уровня промерзания. Снег на нижней линии тоже сажает импульс.'),
 ('Что делать, если линия бьёт слабо?','Проверьте по порядку: заземление, траву на нижней линии, целостность изоляторов и соединений. В девяти случаях из десяти дело в заземлении или в касании растительности. Напишите нам — разберём по фото.'),
]
faq_items=''.join(f'''<details class="py-1{' ' if i else ''}"{' open' if i==0 else ''}><summary class="flex items-center justify-between gap-4 py-4 font-extrabold text-[17px] md:text-[18px]">{q}<i data-lucide="plus" class="faq-icon w-5 h-5 shrink-0 text-brand-dark" aria-hidden="true"></i></summary><p class="pb-5 text-muted max-w-[70ch]">{a}</p></details>''' for i,(q,a) in enumerate(FAQ))
faq_ld=','.join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'%(q.replace('&nbsp;',' ').replace('"','\\"'), a.replace('&nbsp;',' ').replace('«','"').replace('»','"').replace('"','\\"')) for q,a in FAQ)

w('faq.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Вопросы и ответы',None)])}
{page_head('Вопросы и ответы', 'Что чаще всего спрашивают перед покупкой электропастуха. Не нашли свой вопрос — напишите в WhatsApp, отвечаем в рабочее время в течение часа.')}
<section class="container-site mt-8 md:mt-10 grid grid-cols-1 lg:grid-cols-12 gap-8">
  <div class="lg:col-span-4">
    <div class="lg:sticky lg:top-28 card p-6">
      <p class="font-extrabold text-[17px]">Спросить напрямую</p>
      <p class="text-muted text-[15px] mt-2">Опишите хозяйство — ответим по вашей ситуации, а не общими словами.</p>
      <a href="{wa('Здравствуйте! У меня вопрос по электропастуху.')}" target="_blank" rel="noopener" class="btn-secondary w-full mt-4"><img src="assets/icons/whatsapp-FFFFFF.svg" alt="" class="w-5 h-5" width="20" height="20">Задать вопрос</a>
      <a href="tel:+77054285707" class="btn-outline w-full mt-2"><i data-lucide="phone" class="w-5 h-5" aria-hidden="true"></i>+7 (705) 428-57-07</a>
      <a href="kak-vybrat.html" class="link mt-5">Подробный гид по выбору<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a>
    </div>
  </div>
  <div class="lg:col-span-8 divide-y divide-line border-y border-line">{faq_items}</div>
</section>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_ld}]}}</script>
{cta_band()}
</main>''')

# ---------- спасибо ----------
w('spasibo.html', f'''
<main id="top">
<section class="container-site pt-32 md:pt-40 pb-16 md:pb-24">
  <div class="max-w-[620px] mx-auto text-center">
    <span class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-cream border-2 border-brand"><i data-lucide="check" class="w-8 h-8 text-brand-dark" aria-hidden="true"></i></span>
    <h1 class="h2 mt-6">Заявка отправлена</h1>
    <p class="lead mt-4 mx-auto">Менеджер свяжется с вами в рабочее время: Пн–Пт 10:00–18:00, Сб 10:00–16:00. Уточним вид животных, площадь и питание — и подберём комплект.</p>
    <div class="mt-8 flex flex-col sm:flex-row justify-center gap-3">
      <a href="{wa('Здравствуйте! Я оставил заявку на сайте.')}" target="_blank" rel="noopener" class="btn-secondary btn-lg"><img src="assets/icons/whatsapp-FFFFFF.svg" alt="" class="w-5 h-5" width="20" height="20">Написать сейчас</a>
      <a href="catalog.html" class="btn-outline btn-lg">Смотреть каталог</a>
    </div>
    <div class="mt-10 card p-6 text-left">
      <p class="font-extrabold">Пока ждёте</p>
      <ul class="mt-3 space-y-2 text-[15px]">
        <li><a href="kak-vybrat.html" class="link">Как выбрать электропастух<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a></li>
        <li><a href="instrukcii.html" class="link">Инструкции и схемы подключения<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a></li>
        <li><a href="dostavka.html" class="link">Доставка и оплата<i data-lucide="arrow-right" class="w-4 h-4" aria-hidden="true"></i></a></li>
      </ul>
    </div>
  </div>
</section>
</main>''')

# ---------- политика ----------
w('policy.html', f'''
<main id="top">
{crumbs([('Главная','index.html'),('Политика конфиденциальности',None)])}
{page_head('Политика конфиденциальности', 'Как GIGANT Agro обрабатывает персональные данные, которые вы оставляете через формы на сайте.')}
<section class="container-site mt-8 md:mt-10 pb-14 md:pb-24">
  {prose('''<p><strong>Какие данные мы собираем.</strong> Имя и номер телефона, которые вы указываете в форме заявки, а также сведения о хозяйстве: вид животных, площадь и предпочтительный источник питания. Эти данные нужны, чтобы подобрать комплект и связаться с вами.</p>
<p class="mt-4"><strong>Зачем.</strong> Для ответа на заявку, подбора оборудования, оформления заказа и доставки. Мы не используем ваши данные для рассылок без отдельного согласия.</p>
<p class="mt-4"><strong>Кому передаём.</strong> Транспортной компании — данные, необходимые для доставки. В остальных случаях мы не передаём данные третьим лицам, кроме случаев, предусмотренных законодательством Республики Казахстан.</p>
<p class="mt-4"><strong>Сколько храним.</strong> Пока это нужно для работы с заявкой и выполнения обязательств по заказу, либо до вашего отзыва согласия.</p>
<p class="mt-4"><strong>Аналитика.</strong> Сайт использует сервисы веб-аналитики, которые собирают обезличенные данные о посещениях: страницы, источник перехода, тип устройства. Эти данные не позволяют вас идентифицировать.</p>
<p class="mt-4"><strong>Ваши права.</strong> Вы можете запросить сведения о своих данных, потребовать их исправления или удаления. Напишите нам или позвоните по номерам, указанным в контактах.</p>
<p class="mt-4"><strong>Как с нами связаться.</strong> Алматы, мкр. Атырау, 159/8, склад №&nbsp;1. Телефоны +7 (705) 428-57-07 и +7 (775) 771-60-24.</p>''')}
</section>
</main>''')

# ---------- 404 ----------
w('404.html', f'''
<main id="top">
<section class="container-site pt-32 md:pt-40 pb-16 md:pb-24">
  <div class="max-w-[620px] mx-auto text-center">
    <p class="font-black text-[clamp(4rem,12vw,7rem)] leading-none text-brand-dark tabular-nums">404</p>
    <h1 class="h2 mt-4">Такой страницы нет</h1>
    <p class="lead mt-4 mx-auto">Возможно, ссылка устарела или в адресе опечатка. Начните с каталога или подберите комплект за минуту.</p>
    <div class="mt-8 flex flex-col sm:flex-row justify-center gap-3">
      <a href="podbor.html" class="btn-primary btn-lg">Подобрать комплект<i data-lucide="arrow-right" class="w-5 h-5" aria-hidden="true"></i></a>
      <a href="catalog.html" class="btn-outline btn-lg">Смотреть каталог</a>
    </div>
    <div class="mt-10 flex flex-wrap justify-center gap-2">
      <a href="catalog-elektropastuhi.html" class="chip h-10">Электропастухи</a>
      <a href="catalog-komplekty.html" class="chip h-10">Готовые комплекты</a>
      <a href="kak-vybrat.html" class="chip h-10">Как выбрать</a>
      <a href="dostavka.html" class="chip h-10">Доставка</a>
      <a href="kontakty.html" class="chip h-10">Контакты</a>
    </div>
  </div>
</section>
</main>''')
