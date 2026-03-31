from fpdf import FPDF
from fpdf.enums import RenderStyle

FONT_PATH    = '/System/Library/Fonts/Supplemental/'
FONT_REGULAR = FONT_PATH + 'Arial Unicode.ttf'
FONT_BOLD    = FONT_PATH + 'Arial Bold.ttf'

YEL  = (255, 210, 0)    # HATOR yellow
BG   = (10, 10, 10)     # near-black
CARD = (22, 22, 22)     # card bg
C2   = (32, 32, 32)     # lighter card
TEXT = (245, 245, 245)
MUTE = (145, 145, 145)
DIM  = (60, 60, 60)
BLK  = (0, 0, 0)
RED  = (170, 40, 40)


class PDF(FPDF):
    # ── shared helpers ──────────────────────────────────────
    def bg(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, 210, 297, 'F')

    def ybar(self, y, h=2):
        self.set_fill_color(*YEL)
        self.rect(0, y, 210, h, 'F')

    def rr(self, x, y, w, h, fill=None, stroke=False, r=3):
        mode = RenderStyle.DF if stroke else RenderStyle.F
        self.set_line_width(0.4)
        self._draw_rounded_rect(x, y, w, h, mode, True, r)
        self.set_line_width(0.2)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*BG)
        self.rect(0, 0, 210, 11, 'F')
        self.ybar(0, 1.5)
        self.set_font('bold', size=6)
        self.set_text_color(*DIM)
        self.set_y(4)
        self.cell(0, 4, 'HATOR SOFTWARE  ·  UI REDESIGN CONCEPT  ·  2025', align='C')

    def footer(self):
        self.set_y(-10)
        self.set_fill_color(*BG)
        self.rect(0, 287, 210, 10, 'F')
        self.ybar(295.5, 1.5)
        self.set_font('regular', size=6.5)
        self.set_text_color(*DIM)
        self.cell(0, 5, f'{self.page_no()}', align='C')

    # ── components ──────────────────────────────────────────
    def tag(self, text, x=20, y=None):
        if y is None:
            y = self.get_y()
        self.set_font('bold', size=7)
        tw = self.get_string_width(text) + 14
        self.set_fill_color(*YEL)
        self.rr(x, y, tw, 7.5)
        self.set_text_color(*BLK)
        self.set_xy(x, y)
        self.cell(tw, 7.5, text, align='C')
        self.set_xy(x, y + 7.5)
        self.ln(2)

    def h1(self, text, x=20, y=None, size=26, w=165):
        if y is None:
            y = self.get_y() + 2
        self.set_font('bold', size=size)
        self.set_text_color(*TEXT)
        self.set_xy(x, y)
        self.multi_cell(w, size * 0.50, text)
        self.ln(2)

    def body(self, text, x=20, y=None, w=170, size=9.5, color=None):
        if y is None:
            y = self.get_y()
        self.set_font('regular', size=size)
        self.set_text_color(*(color or MUTE))
        self.set_xy(x, y)
        self.multi_cell(w, 5.6, text)
        self.ln(1)

    def bullet(self, text):
        self.set_x(20)
        y = self.get_y()
        self.set_fill_color(*YEL)
        self.rect(20, y + 2.5, 2.5, 2.5, 'F')
        self.set_x(27)
        self.set_font('regular', size=8.5)
        self.set_text_color(*MUTE)
        self.multi_cell(0, 5, text)
        self.ln(0.5)

    def stat(self, number, label, x, y, w=40):
        self.set_font('bold', size=21)
        self.set_text_color(*YEL)
        self.set_xy(x, y)
        self.cell(w, 13, number, align='C')
        self.set_font('regular', size=7.5)
        self.set_text_color(*MUTE)
        self.set_xy(x, y + 13)
        self.cell(w, 5, label, align='C')

    def fcard(self, num, title, desc, x, y, w=84, h=33):
        self.set_fill_color(*CARD)
        self.rr(x, y, w, h)
        self.set_fill_color(*YEL)
        self.rect(x, y + 5, 2.5, h - 10, 'F')
        self.set_font('bold', size=7)
        self.set_text_color(*YEL)
        self.set_xy(x + 7, y + 4)
        self.cell(14, 5, f'{num:02d}')
        self.set_font('bold', size=9.5)
        self.set_text_color(*TEXT)
        self.set_xy(x + 7, y + 10)
        self.cell(w - 14, 6, title)
        self.set_font('regular', size=7.5)
        self.set_text_color(*MUTE)
        self.set_xy(x + 7, y + 17.5)
        self.multi_cell(w - 12, 4.5, desc)

    def sec(self, text):
        self.ln(3)
        self.set_font('bold', size=10.5)
        self.set_text_color(*YEL)
        self.set_x(20)
        self.cell(0, 6, text)
        self.ln(1)
        y = self.get_y()
        self.set_draw_color(*YEL)
        self.set_line_width(0.7)
        self.line(20, y, 78, y)
        self.set_line_width(0.2)
        self.set_draw_color(*DIM)
        self.ln(5)


# ════════════════════════════════════════════════════════
pdf = PDF()
pdf.set_margins(20, 20, 20)
pdf.add_font('regular', fname=FONT_REGULAR)
pdf.add_font('bold',    fname=FONT_BOLD)


# ════════════════════════════════════════════════════════
# PAGE 1  COVER
# ════════════════════════════════════════════════════════
pdf.add_page()
pdf.bg()

# top yellow bar
pdf.ybar(0, 3)

# TOP-RIGHT yellow corner block
pdf.set_fill_color(*YEL)
pdf.rect(160, 0, 50, 52, 'F')

# "H" monogram on yellow block
pdf.set_font('bold', size=52)
pdf.set_text_color(*BLK)
pdf.set_xy(160, 4)
pdf.cell(50, 30, 'H', align='C')

# Sub-label on yellow block
pdf.set_font('bold', size=6.5)
pdf.set_text_color(*BLK)
pdf.set_xy(160, 35)
pdf.cell(50, 5, 'SOFTWARE', align='C')
pdf.set_xy(160, 41)
pdf.cell(50, 5, 'REDESIGN', align='C')

# HATOR wordmark
pdf.set_font('bold', size=60)
pdf.set_text_color(*YEL)
pdf.set_xy(16, 38)
pdf.cell(0, 26, 'HATOR')

# tagline under wordmark
pdf.set_font('regular', size=10.5)
pdf.set_text_color(*MUTE)
pdf.set_xy(20, 68)
pdf.cell(0, 6, 'S  O  F  T  W  A  R  E')

# yellow + dim divider
pdf.set_fill_color(*YEL)
pdf.rect(20, 79, 48, 2, 'F')
pdf.set_fill_color(*DIM)
pdf.rect(70, 79.7, 90, 0.6, 'F')

# main headline
pdf.set_font('bold', size=27)
pdf.set_text_color(*TEXT)
pdf.set_xy(20, 87)
pdf.multi_cell(155, 13.5, 'Ваш софт може виглядати\nяк у Razer і Logitech.')

# body
pdf.set_font('regular', size=10.5)
pdf.set_text_color(*MUTE)
pdf.set_xy(20, 124)
pdf.multi_cell(148, 6.2,
    'Я зробив повний редизайн вашого Electron-додатку. '
    'Всі 8 розділів, новий UI/UX, живі RGB-ефекти, '
    'реальні фото пристроїв, анімації. '
    'Готовий прототип — передаю безкоштовно.')

# ── STATS BOX ──────────────────────────────────────
pdf.set_fill_color(*CARD)
pdf.rr(20, 162, 170, 40, r=4)
pdf.set_fill_color(*YEL)
pdf.rect(20, 162, 3, 40, 'F')

stats = [('8', 'Розділів'), ('5', 'Тем'), ('2', 'Мови'), ('0', 'Залежностей')]
for i, (n, l) in enumerate(stats):
    pdf.stat(n, l, 26 + i * 41, 168)

# vertical separators
for i in range(1, 4):
    pdf.set_fill_color(*DIM)
    pdf.rect(26 + i * 41 - 3, 170, 0.5, 26, 'F')

# ── YELLOW BANNER STRIP ────────────────────────────
pdf.set_fill_color(*YEL)
pdf.rect(0, 220, 210, 20, 'F')
pdf.set_font('bold', size=10)
pdf.set_text_color(*BLK)
pdf.set_xy(20, 226)
pdf.cell(170, 8,
    'Готовий прототип  ·  Electron + Vanilla JS  ·  UA / EN  ·  2025',
    align='C')

# author
pdf.set_font('regular', size=8.5)
pdf.set_text_color(*DIM)
pdf.set_xy(20, 272)
pdf.cell(0, 6, 'Студент 1-го курсу  ·  НаУКМА  ·  Ініціатива для HATOR Ukraine')

pdf.ybar(294, 3)


# ════════════════════════════════════════════════════════
# PAGE 2  PROBLEM → SOLUTION + UX HIGHLIGHTS
# ════════════════════════════════════════════════════════
pdf.add_page()
pdf.bg()

pdf.set_xy(20, 16)
pdf.tag('ПРОБЛЕМА ТА РІШЕННЯ')

# ── LEFT COL: Before ──
pdf.set_fill_color(*CARD)
pdf.rr(20, 32, 82, 88, r=4)
pdf.set_fill_color(140, 35, 35)
pdf.rect(20, 32, 82, 3, 'F')

pdf.set_font('bold', size=8.5)
pdf.set_text_color(220, 80, 80)
pdf.set_xy(24, 39)
pdf.cell(75, 6, 'ЗАРАЗ')

before = [
    'Застарілий мінімалістичний дизайн',
    'Немає live RGB preview',
    'Немає skeleton-loaders',
    'Немає тем та локалізації',
    'Немає статистики використання',
    'Немає ігрових профілів / макросів',
]
for item in before:
    y = pdf.get_y() + 1.5
    pdf.set_fill_color(140, 35, 35)
    pdf.rect(25, y + 2.2, 2.2, 2.2, 'F')
    pdf.set_x(32)
    pdf.set_font('regular', size=8)
    pdf.set_text_color(*MUTE)
    pdf.cell(0, 5.5, item)
    pdf.ln(0)

# ── ARROW ──
pdf.set_font('bold', size=20)
pdf.set_text_color(*YEL)
pdf.set_xy(102, 69)
pdf.cell(8, 10, '→', align='C')

# ── RIGHT COL: After ──
pdf.set_fill_color(*CARD)
pdf.rr(110, 32, 82, 88, r=4)
pdf.set_fill_color(*YEL)
pdf.rect(110, 32, 82, 3, 'F')

pdf.set_font('bold', size=8.5)
pdf.set_text_color(*YEL)
pdf.set_xy(114, 39)
pdf.cell(75, 6, 'ПІСЛЯ РЕДИЗАЙНУ')

after = [
    'Dark UI класу Razer Synapse',
    '8 RGB ефектів, Canvas live preview',
    'Skeleton → реальні фото пристроїв',
    '5 тем, UA/EN i18n в одному HTML',
    'DPI chart, activity, top processes',
    'Ігрові профілі, макроси, EQ, онбординг',
]
pdf.set_xy(114, 48)
for item in after:
    y = pdf.get_y() + 1.5
    pdf.set_fill_color(*YEL)
    pdf.rect(115, y + 2.2, 2.2, 2.2, 'F')
    pdf.set_x(122)
    pdf.set_font('regular', size=8)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 5.5, item)
    pdf.ln(0)

# ── DESCRIPTION ──────────────────────────────────────
pdf.set_font('bold', size=14)
pdf.set_text_color(*TEXT)
pdf.set_xy(20, 128)
pdf.cell(0, 9, 'Що саме зроблено')

pdf.set_font('regular', size=9)
pdf.set_text_color(*MUTE)
pdf.set_xy(20, 139)
pdf.multi_cell(170, 5.5,
    'Повний редизайн фронтенду того самого Electron-додатку який зараз '
    'доступний на hator.gg. Написаний в одному HTML-файлі, нульові зовнішні '
    'залежності. Бекенд не чіпався — новий UI просто одягається поверх '
    'існуючої IPC-архітектури.')

# ── 3 UX HIGHLIGHT CARDS ──────────────────────────────
ux3 = [
    ('Ctrl+K Search', 'Command palette для\nшвидкої навігації між\nрозділами і налаштуваннями'),
    ('Floating Save Bar', 'Як у Razer Synapse —\nповідомлення про незбережені\nзміни з анімацією пружини'),
    ('Ripple + 3D Tilt', 'Ripple на кожному кліці,\n3D perspective tilt на\nкарточках девайсів'),
]
y0 = 172
for i, (t2, d2) in enumerate(ux3):
    x = 20 + i * 62
    pdf.set_fill_color(*CARD)
    pdf.rr(x, y0, 58, 52, r=3)
    pdf.set_fill_color(*YEL)
    pdf.rect(x, y0, 58, 3, 'F')
    pdf.set_font('bold', size=8.5)
    pdf.set_text_color(*TEXT)
    pdf.set_xy(x + 5, y0 + 7)
    pdf.cell(50, 5.5, t2)
    pdf.set_font('regular', size=7.5)
    pdf.set_text_color(*MUTE)
    pdf.set_xy(x + 5, y0 + 14)
    pdf.multi_cell(50, 4.5, d2)

# ── BOTTOM ROW: 3 more metrics ──────────────────────────
metrics = [
    ('Sliding Nav', 'Акцентна лінія плавно\nрухається між пунктами\nменю — spring анімація'),
    ('Firmware Flow', '4-кроковий прогрес\nпрошивки з animated\nprogress bar'),
    ('Onboarding', '3-кроковий welcome\nscreen для нових\nкористувачів'),
]
y1 = 230
for i, (t2, d2) in enumerate(metrics):
    x = 20 + i * 62
    pdf.set_fill_color(*C2)
    pdf.rr(x, y1, 58, 46, r=3)
    pdf.set_fill_color(*YEL)
    pdf.rect(x, y1, 3, 46, 'F')
    pdf.set_font('bold', size=8.5)
    pdf.set_text_color(*TEXT)
    pdf.set_xy(x + 7, y1 + 6)
    pdf.cell(48, 5.5, t2)
    pdf.set_font('regular', size=7.5)
    pdf.set_text_color(*MUTE)
    pdf.set_xy(x + 7, y1 + 13)
    pdf.multi_cell(48, 4.5, d2)


# ════════════════════════════════════════════════════════
# PAGE 3  FEATURES GRID
# ════════════════════════════════════════════════════════
pdf.add_page()
pdf.bg()

pdf.set_xy(20, 16)
pdf.tag('8 ПОВНІСТЮ ПЕРЕРОБЛЕНИХ РОЗДІЛІВ')

pdf.set_font('bold', size=20)
pdf.set_text_color(*TEXT)
pdf.set_xy(20, 32)
pdf.cell(0, 11, 'Кожен екран — з нуля')

pdf.set_font('regular', size=9)
pdf.set_text_color(*MUTE)
pdf.set_xy(20, 44)
pdf.cell(0, 6,
    'Не рестайлинг — повне переписування фронтенду зі збереженням архітектури бекенду')

features = [
    ('Мої пристрої',
     'Skeleton-loaders → живі фото, hover glow,\n3D tilt, 4 demo-карти, connection bar'),
    ('Підсвічування',
     '8 ефектів з live Canvas preview:\nBreathing, Rainbow, Wave, Ripple, Reaction…'),
    ('RGB Клавіатура',
     'Full-size клавіатура з покадровою анімацією\nкожного ефекту, Ripple on click'),
    ('DPI та кнопки',
     '4 рівні DPI, polling rate, призначення кнопок,\nакселерація, DPI indicator у titlebar'),
    ('Статистика',
     'Animated counters, DPI usage chart,\ntop processes, weekly activity bars'),
    ('Ігрові профілі',
     'Автоперемикання по назві процесу гри,\nCRUD правила, inline rename'),
    ('Макроси',
     'Live-запис клавіш, chip-інтерфейс,\nзатримки між клавішами, відтворення'),
    ('Налаштування',
     'Firmware flow 4 кроки, import/export,\n5 тем, UA/EN, notification center'),
]

y0 = 56
for i, (title, desc) in enumerate(features):
    r, c = divmod(i, 2)
    pdf.fcard(i + 1, title, desc,
              20 if c == 0 else 109,
              y0 + r * 37,
              w=84, h=33)

# Bottom band
pdf.set_fill_color(*CARD)
pdf.rect(0, 208, 210, 22, 'F')
pdf.set_fill_color(*YEL)
pdf.rect(0, 208, 4, 22, 'F')

pdf.set_font('bold', size=10)
pdf.set_text_color(*TEXT)
pdf.set_xy(14, 214)
pdf.cell(100, 6, 'Повний список UX-деталей:')

ux_short = [
    'Keyboard shortcuts Ctrl+1–5, Escape',
    'Context menu, drag rename',
    'Toast notifications, badge counter',
    'Auto-update banner flow',
]
pdf.set_font('regular', size=7.5)
pdf.set_text_color(*MUTE)
pdf.set_xy(14, 221)
pdf.cell(90, 4.5, '  ·  '.join(ux_short[:2]))
pdf.set_xy(14, 226)
pdf.cell(90, 4.5, '  ·  '.join(ux_short[2:]))

# Right side of bottom band
pdf.set_font('bold', size=9)
pdf.set_text_color(*YEL)
pdf.set_xy(120, 215)
pdf.cell(70, 6, 'Один файл. Нуль залежностей.')
pdf.set_font('regular', size=7.5)
pdf.set_text_color(*MUTE)
pdf.set_xy(120, 222)
pdf.cell(70, 4.5, 'index.html · ~3000 рядків · Electron ready')


# ════════════════════════════════════════════════════════
# PAGE 4  TECH STACK + CTA
# ════════════════════════════════════════════════════════
pdf.add_page()
pdf.bg()

pdf.set_xy(20, 16)
pdf.tag('ТЕХНІЧНИЙ СТЕК')

# Tech grid 2×3
tech = [
    ('Electron + Vanilla JS',
     'Один HTML-файл — нульові зовнішні залежності на фронті'),
    ('Canvas API',
     'RGB-анімація в реальному часі через requestAnimationFrame'),
    ('IPC Renderer',
     'HID-логіка підключення пристроїв готова до інтеграції'),
    ('localStorage',
     'Профілі, теми, мова, DPI — персистентне зберігання'),
    ('CSS Custom Properties',
     '5 тем кольорів через --accent, --bg без перезавантаження'),
    ('UA / EN i18n',
     'Повна система перекладу, миттєве перемикання мови'),
]

y_tech = 34
for i, (name, desc) in enumerate(tech):
    col = i % 2
    x   = 20 if col == 0 else 109
    y   = y_tech + (i // 2) * 21

    pdf.set_fill_color(*CARD)
    pdf.rr(x, y, 84, 17, r=3)
    pdf.set_fill_color(*YEL)
    pdf.rect(x, y, 2.5, 17, 'F')

    pdf.set_font('bold', size=8.5)
    pdf.set_text_color(*TEXT)
    pdf.set_xy(x + 7, y + 3)
    pdf.cell(76, 5, name)

    pdf.set_font('regular', size=7.5)
    pdf.set_text_color(*MUTE)
    pdf.set_xy(x + 7, y + 9.5)
    pdf.cell(76, 4.5, desc)

# ── What's next for backend ─────────────────────────────
pdf.sec('ЩО ПОТРІБНО ДЛЯ ПОВНОЦІННОЇ РОБОТИ')

next_steps = [
    'HID device descriptors від HATOR (Vendor ID / Product ID)',
    'Протокол команд (які байти — DPI, RGB, polling rate)',
    'node-hid підключення в main.js — фронт вже чекає через ipcRenderer',
    'IPC handlers: scan-devices, set-dpi, set-effect, set-color',
]
for step in next_steps:
    pdf.bullet(step)

# ── CTA BOX ────────────────────────────────────────────
cy = pdf.get_y() + 10

# Yellow-bordered card
pdf.set_fill_color(*CARD)
pdf.set_draw_color(*YEL)
pdf.set_line_width(1.5)
pdf._draw_rounded_rect(20, cy, 170, 50, RenderStyle.DF, True, 5)
pdf.set_line_width(0.2)
pdf.set_draw_color(*DIM)

# Yellow top accent
pdf.set_fill_color(*YEL)
pdf.rect(20, cy, 170, 3.5, 'F')

pdf.set_font('bold', size=12)
pdf.set_text_color(*TEXT)
pdf.set_xy(28, cy + 9)
pdf.cell(0, 7, 'Готовий передати весь код безкоштовно')

pdf.set_font('regular', size=9)
pdf.set_text_color(*MUTE)
pdf.set_xy(28, cy + 18)
pdf.multi_cell(155, 5.5,
    'Якщо зацікавить — готовий разом допомогти підключити HID.\n'
    'Мені важливо щоб HATOR виглядав на рівні топових брендів.')

# Contact row
pdf.set_font('bold', size=8.5)
pdf.set_text_color(*YEL)
pdf.set_xy(28, cy + 36)
pdf.cell(24, 5, 'Telegram:')
pdf.set_text_color(*TEXT)
pdf.cell(52, 5, '[ваш нік]')

pdf.set_text_color(*YEL)
pdf.cell(18, 5, 'Email:')
pdf.set_text_color(*TEXT)
pdf.cell(0, 5, '[ваш email]')

# ── FINAL YELLOW BAR ────────────────────────────────────
pdf.set_fill_color(*YEL)
pdf.rect(0, 285, 210, 12, 'F')
pdf.set_font('bold', size=7.5)
pdf.set_text_color(*BLK)
pdf.set_xy(20, 289)
pdf.cell(170, 5,
    'HATOR SOFTWARE REDESIGN CONCEPT  ·  2025  ·  НАУКМА',
    align='C')


# ════════════════════════════════════════════════════════
out = '/Users/maczone/hator-app/HATOR_Proposal.pdf'
pdf.output(out)
print(f'Done: {out}  ({pdf.page} pages)')
