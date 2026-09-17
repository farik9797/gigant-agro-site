# GIGANT Agro — Design System (v2, premium)

## Visual theme
Полевой инструмент в премиальном исполнении: полноэкранное фото пастбища в hero, плавающая стеклянная навигация, крупный чёрный гротеск с одним курсивным серифным словом, тёмно-зелёные «заливные» секции для ритма, реальные фото и техпаспортные цифры.

## Color
| Token | Hex | Role |
|---|---|---|
| bg | #F4F6F1 | фон страницы, off-white с оттенком бренда |
| surface | #FFFFFF | карточки, формы |
| ink | #16191C | заголовки, текст |
| muted | #4F5A52 | вторичный текст (контраст 6:1 на bg) |
| brand | #5A984B | зелёный логотипа: иконки, крупные акценты, рамки active |
| brand-dark | #3E7A34 | ссылки, вторичные кнопки с белым текстом |
| deep | #17261B | тёмные секции, подвал, оверлеи фото |
| cream | #F3F8D6 | кремовый логотипа: панель подбора, подложки |
| pulse | #FFC400 | единственный цвет действия: главные CTA, импульс, курсивное слово в hero |
| line | #D6DCD2 | рамки 1 px |

Стратегия: committed — зелёный несёт бренд и ритм, жёлтый — только действие. Один жёлтый CTA на экран.

## Typography
- Golos Text (Google Fonts, кириллица): 400/500 текст, 600 подписи, 800–900 заголовки. Display: clamp(2.5rem, 6vw, 5.5rem), letter-spacing −0.03em, `text-wrap: balance`.
- Vollkorn Italic 700: одно акцентное слово в hero, во флагманах и в финальном CTA. Не чаще.
- Текст 17/27 на desktop, 16/26 mobile; ничего мельче 14 px.

## Layout
Контейнер 1200–1280 px, отступы секций clamp(4rem, 8vw, 7rem). Полноэкранный hero (88svh) с текстом слева-снизу. Радиусы: карточки 16 px, поля 12 px, кнопки и навигация pill. Рамки 1 px вместо теней; тень только у плавающей навигации.

## Motion
- Hero: стаггер появления 700–900 мс, cubic-bezier(0.22, 1, 0.36, 1); при прокрутке контент hero уходит вверх и гаснет.
- Секции: reveal opacity + 24 px по IntersectionObserver, видимы по умолчанию без JS.
- Бегущий импульс по линии ограждения (hero-divider, «как это работает»).
- Логотипный marquee 32 s linear.
- Кнопки: `:active` scale(0.97), 160 мс. Hover карточек: 2 px lift, 250 мс.
- `prefers-reduced-motion`: без трансформаций, только прозрачность.

## Components
Nav pill (glass), proof pill, spec strip «техпаспорт», chips выбора, product card, kit card, category tile, step list with vertical pulse line, accordion (`<details>`), lead form, mobile action bar, floating WhatsApp.
