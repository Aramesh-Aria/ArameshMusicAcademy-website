# Gate 1: proposed models, migrations and Persian copy

**Status:** approved at Gate 1 (2026-10-26), with the owner's answers below. Nothing here is built yet. It implements section 1 of [02-redesign-brief.md](02-redesign-brief.md) and ADR-0002. Everything that goes **beyond** the brief's list is marked **[beyond brief]** and needs a yes or no.

---

## Part 1: Models

### 1.1 New app `apps.programmes`: `Programme`

A separate app, because `Teacher` and `ClassSession` both point at it and it points at nothing, so there is no import cycle.

| Field | Type | Notes |
|---|---|---|
| `name` | Char(100), unique | «کلاس خصوصی» |
| `slug` | Slug, unique | Latin, for the URL `/programmes/<slug>/`: `private`, `ensemble`, `children`, `theory` |
| `kind` | choice: `with_teacher` / `fixed_time` | from ADR-0002 |
| `short_description` | Text | for the card, about 25 words |
| `long_description` | Text | for its page; blank lines make paragraphs |
| `age_label` | Char(40), blank | chip text, e.g. «از ۷ سال»; the chip hides when blank |
| `photo_1`, `photo_2`, `photo_3` | Image, blank | up to 3 photos that crossfade in the card. Processed on save like the other images, to 900×600 (3:2), using the same `save()` pattern as `GalleryPage` |
| `instruments_shown` **[beyond brief]** | choice: `all` / `children_only` / `none` | Which Instruments the Programme page lists: the full grid for کلاس خصوصی, the children-only ones for موسیقی کودک, none for the other two. Without it the views would need hardcoded slugs. |
| `display_order` | PositiveInt | |
| `is_active` | Bool | |

Three separate photo fields rather than an inline table: the brief caps them at 3, and three file inputs are simpler for staff than an inline with a max of 3.

**How کلاس خصوصی stays untagged:** the Teacher → Programme field only offers Programmes whose `instruments_shown` is not `all` and whose `kind` is `with_teacher`. So staff can tag تئوری و سلفژ and موسیقی کودک, and can never tag کلاس خصوصی or گروه نوازی on a teacher.

### 1.2 `teachers.Instrument`: new fields

| Field | Type | Notes |
|---|---|---|
| `slug` | Slug, unique | Latin, for `/instruments/<slug>/`. Filled by the data migration from a fixed list (below); prepopulated from the name in the admin for new rows. |
| `overview` | Text, blank | The short overview on its page and tile. The owner writes these later; the page works without one. |
| `photo` | Image, blank | Processed to 1200×800 (3:2). No photo → the designed typographic tile. |
| `display_order` | PositiveInt | Ordering becomes `display_order, name`. |
| `children_only` | Bool | بلز and فلوت. Kept out of the main grid; shown only on the موسیقی کودک page and the teacher's profile. |

Slugs for today's Instruments: سنتور `santur` · تار `tar` · سه تار `setar` · پیانو `piano` · ویولن `violin` · آواز ایرانی `persian-voice` · تنبک `tombak` · دف `daf` · داربوکا `darbuka` · هنگدرام `handpan` · کاخن `cajon` · آکوردئون `accordion` · هارمونیکا `harmonica` · گیتار الکتریک `electric-guitar` · گیتار پاپ `pop-guitar` · بلز `glockenspiel` · فلوت `flute`.

### 1.3 `teachers.Teacher`: one new field

- `programmes`: M2M to `Programme`, blank, limited as in 1.1. Help text: «دوره‌هایی که این استاد در همان روزهای حضورش درس می‌دهد (مثل تئوری و سلفژ). کلاس خصوصی را انتخاب نکنید؛ همهٔ کلاس‌ها خصوصی است.»

### 1.4 `schedules.ClassSession`

- `programme`: FK to `Programme`, nullable, `PROTECT`, limited to `kind = fixed_time`. Help text: «فقط برای جلسه‌ای که برای یک دورهٔ زمان‌دار (مثل گروه نوازی) رزرو شده است. در این جلسه چیز دیگری تدریس نمی‌شود.»
- `instruments` becomes `blank=True`, because a reserved session has none.
- Validation, in the admin form (model `clean()` cannot see M2M values): a session needs either Instruments or a Programme, never both.

**Schedule display rule** (one function, tested in step 7): a reserved session shows only its Programme. Any other session shows its Instruments (children-only ones excluded), then a dot, then the teacher's `with_teacher` Programmes. Example: Ali Shams, Wednesday → «پیانو، گیتار الکتریک، گیتار پاپ · تئوری و سلفژ».

### 1.5 FAQ (in `apps.pages`)

`FAQ`: `question` (Char 200), `answer` (Text), `display_order`, `is_active`, as in the brief. Plus **[beyond brief]**:
- `show_on_home` (Bool, default on), and
- `programmes` (M2M to `Programme`, blank).

The brief says FAQ appears on the home page **and** on Programme pages ("relevant FAQ"). Without a link, every Programme page would show the same list. With it: home shows the entries ticked for home; a Programme page shows the entries linked to it. Each section hides when empty.

### 1.6 "How we teach" and "Three steps": the smallest change

**Proposal: two new `SitePageContent` keys, no new fields.**
- `teaching` («شیوهٔ آموزش») and `first_lesson` («سه قدم تا اولین جلسه»).
- `title` is the section heading. `body` holds the points: each point is a line for its title, the next line(s) for its text, and a blank line between points. The view splits it; the help text explains the format.
- Migration: only the `page_key` choices change.
- If either row is missing or inactive, the section hides.

Rejected: a new "points" model with an inline (cleaner data, but a new model for six short paragraphs).

### 1.7 Hero and gallery settings

- New setting `HERO_GALLERY_SLUG` (default `home-hero`), next to `ABOUT_GALLERY_SLUG`, overridable by env.
- The gallery page with that slug is excluded from `gallery_nav_tree`, the gallery index and the sitemap, by slug. No new field.

### 1.8 Not changed

`GalleryImage`, `Video`, `Testimonial`, `ContactMessage`, the contact form and captcha.

---

## Part 2: Migrations, in order

1. `programmes/0001_initial`: `Programme`.
2. `teachers/0007`: the Instrument fields (`slug` added nullable first), `Teacher.programmes`.
3. `schedules/0007`: `ClassSession.programme`; `instruments` becomes blank.
4. `pages/0006`: the new `page_key` choices; `FAQ`.
5. `programmes/0002_move_subjects_out_of_instrument` (**data**, depends on 2–4):
   1. Create the four Programmes with the copy in Part 3 (age labels left blank unless the owner gives them).
   2. Fill every Instrument's slug from the list in 1.2; any unknown name gets a slug from its pk (`instrument-<pk>`), so the migration never fails on production data.
   3. Tag Teachers: anyone who had «تئوری و سلفژ» gets تئوری و سلفژ (Masoud Aramesh, Ali Shams); anyone who had «موسیقی کودک» gets موسیقی کودک (Nasim Haghi).
   4. Every session whose only Instrument was «گروه نوازی» (Masoud Aramesh, Thursday 10–19) gets `programme = ensemble`, and its Instruments are cleared.
   5. Remove the three fake Instruments from every other session.
   6. Create بلز and فلوت with `children_only = True`, and add them to Nasim Haghi.
   7. Delete the three Instrument rows «تئوری و سلفژ», «گروه نوازی», «موسیقی کودک».
   8. A reverse function that recreates the three rows and their links, so the migration can be undone.
   Every lookup is by name and skips quietly if the row is not there, because production data may differ from the seed.
6. Seed: `seed_data/academy.json` gains a `programmes` list and per-teacher `programmes`; sessions use `programme` instead of the fake instruments; بلز and فلوت are added; the three fake names are removed. `seed_sample_data` creates Programmes before Teachers and sets `HERO_GALLERY_SLUG`'s page as it does today.
7. Tests: the schedule display rule (reserved session, a teacher with a "with the teacher" Programme, children-only Instruments hidden from the schedule and the main grid), and the data migration on a copy of the seed data.

**Nasim Haghi's Saturday session:** after the migration it has no regular Instruments, so the schedule reads «موسیقی کودک». Option: also list «بلز، فلوت» there. The brief says children-only Instruments appear only on the موسیقی کودک page and her profile, so the proposal is **not** to.

---

## Part 3: Persian copy (drafts for approval)

Every sentence uses only facts from the live site, the teacher bios and `seed_data/academy.json`. Where a fact is missing, the slot says **[owner]** and nothing is invented. Digits are shown in Persian, as they will render.

### Facts this copy relies on
- Founded in 1395 in Tehran by مسعود آرامش, a santur player and composer with more than 40 years in music (About text and his bio).
- The Academy teaches children, teens and adults; Persian classical music, world and pop music, children's music; Persian, classical and pop voice; theory and solfège; ensemble classes for children, teens and adults; master classes and professional courses (About text).
- The teachers' training and performing histories are in their bios.

### 3.1 Hero

- **Small text:** each slide's photo title (for example «کلاس سنتور»), as the brief says.
- **Headline, option A:** «موسیقی، در فضایی آرام» (21 characters). It echoes the name آرامش and the About text («در فضایی کاملا آرام»).
- **Headline, option B:** «ساز و آواز، از کودکی تا بزرگسالی» (31 characters). Plainer; says who it is for.
- **Supporting sentence:** «آموزش خصوصی سنتور، تار، پیانو، ویولن، آواز و سازهای دیگر برای کودکان، نوجوانان و بزرگسالان، با مدیریت مسعود آرامش، آهنگساز و نوازندهٔ سنتور.»
- **Buttons:** «تماس با آموزشگاه» (primary, calls the main number) · «دوره‌ها» (secondary).
- **امروز در آموزشگاه (live):** «امروز، شنبه: سنتور، پیانو، آواز ایرانی، موسیقی کودک · تا ساعت ۲۱» / on Friday: «جمعه‌ها آموزشگاه تعطیل است. شنبه از ساعت ۱۰ پاسخگوی شما هستیم.» (hours from `SITE_HOURS`).

### 3.2 About panel (home)

- **Label:** «آموزشگاه موسیقی آرامش»
- **Headline:** «با مدیریت مسعود آرامش»
- **Text:** «مسعود آرامش، آهنگساز و نوازندهٔ سنتور با بیش از چهل سال فعالیت در موسیقی، این آموزشگاه را در سال ۱۳۹۵ در تهران بنیان گذاشت. اینجا کودکان، نوجوانان و بزرگسالان در فضایی آرام، نزد استادانی ساز و آواز می‌آموزند که بیشترشان سابقهٔ اجرا در کنسرت‌ها و جشنواره‌ها دارند.»
- **Link:** «دربارهٔ آموزشگاه»

### 3.3 Programmes

- **Section heading:** «دوره‌ها»
- **Intro:** «همهٔ کلاس‌های آرامش خصوصی است: یک استاد و یک هنرجو. کنار آن، هنرجویان می‌توانند در گروه نوازی بنوازند، و کودکان و علاقه‌مندان به تئوری هم دورهٔ خودشان را دارند.»

| Programme | Age chip | Short description (card) |
|---|---|---|
| کلاس خصوصی | «کودک تا بزرگسال» | «سنتور، تار، سه‌تار، پیانو، ویولن، گیتار، آواز و سازهای کوبه‌ای؛ یک استاد و یک هنرجو، متناسب با سطح و هدف هر هنرجو.» |
| گروه نوازی | «کودک، نوجوان، بزرگسال» | «پنجشنبه‌ها هنرجویان کنار کلاس خصوصی‌شان با هم می‌نوازند، با سرپرستی مسعود آرامش.» |
| موسیقی کودک | **[owner]** e.g. «از ؟ سال» | «آشنایی کودکان با نت و ریتم و نواختن سازهای کودک مانند بلز و فلوت، نزد نسیم حقی، مدرس موسیقی کودک با دوره‌های روش ارف.» |
| تئوری و سلفژ | **[owner]** | «خواندن نت، ریتم و شنیدن موسیقی، نزد مسعود آرامش و علی شمس، در همان روزهایی که در آموزشگاه هستند.» |

**Long descriptions (Programme pages):**

- **کلاس خصوصی:** «در آموزشگاه آرامش هر کلاس خصوصی است: یک استاد و یک هنرجو، و برنامه‌ای که با سطح و هدف همان هنرجو پیش می‌رود.

می‌توانید موسیقی اصیل ایرانی بیاموزید (سنتور، تار، سه‌تار، تنبک، دف و آواز ایرانی)، یا پیانو، ویولن، گیتار، آکوردئون و سازهای کوبه‌ای دیگر. استادان آرامش بیشترشان سابقهٔ اجرا در کنسرت‌ها و جشنواره‌ها دارند و ردیف و ساز را نزد استادان شناخته‌شده آموخته‌اند.

برای انتخاب ساز و استاد، با آموزشگاه تماس بگیرید.»
- **گروه نوازی:** «گروه نوازی جایی است که هنرجویان آرامش، کنار کلاس خصوصی‌شان، با هم می‌نوازند. کلاس‌های گروه نوازی ویژهٔ کودکان، نوجوانان و بزرگسالان است و پنجشنبه‌ها با سرپرستی مسعود آرامش برگزار می‌شود؛ او پیش‌تر سرپرست ارکستر جوانان یزد و گروه نوا بوده است.

در ساعت گروه نوازی کلاس دیگری برگزار نمی‌شود. **[owner: who can join, and is it free for enrolled students?]**»
- **موسیقی کودک:** «در کلاس موسیقی کودک، کودکان با نت‌خوانی پایه آشنا می‌شوند و سازهای کودک مانند بلز و فلوت را می‌نوازند.

مدرس این کلاس، نسیم حقی، سال‌هاست به کودکان و نوجوانان موسیقی آموزش می‌دهد، دوره‌های موسیقی کودک به روش ارف را گذرانده و کارت صلاحیت تدریس موسیقی کودک از وزارت فرهنگ و ارشاد اسلامی دارد. در کلاس‌های او آموزش اصولی موسیقی با پرورش خلاقیت کودکان همراه است.» **[owner: age range]**
- **تئوری و سلفژ:** «تئوری و سلفژ زبان مشترک همهٔ سازهاست: خواندن نت، ریتم و شنیدن دقیق. این کلاس را مسعود آرامش و علی شمس درس می‌دهند، در همان روزهایی که در آموزشگاه حضور دارند؛ برای زمانش با آموزشگاه هماهنگ کنید.»

### 3.4 Instrument grid

- **Heading:** «سازهایی که آموزش می‌دهیم»
- **Tile:** the Instrument's name and a chevron. No overview text on the home tiles.
- Instrument overviews: **left for the owner** (the brief lists them as admin work). The pages work without them, showing teachers and times.

### 3.5 Director and teachers

- **Heading:** «استادان آرامش»
- **Lineage lines under names (from the bios, for approval):**
  - مسعود آرامش: «شاگرد فاطمه روح‌بخش و محمدرضا روح‌بخش»
  - سیاوش برهانی: «آموخته نزد هوشنگ ظریف، فرهاد فخرالدینی و حسین علیزاده»
  - علیرضا مهدی‌زاده: «آموخته نزد محمدرضا شجریان، شاپور رحیمی و جعفر صادقیان»
  - فرزاد دهپور: «آموخته نزد ارسلان کامکار و فرشید فرهمند»
  - آوا آرامش: «دورهٔ پداگوژی پیانو نزد کلارا بوکوچاوا»
  - لیلی فیضی: «آموخته نزد سحاب تربتی و آذین مرزآبادی»
  - رویا خلیلی: «دارای کارت صلاحیت تدریس»
  - حمیدرضا اکبری: «کارشناسی ارشد نوازندگی ساز کلاسیک»
  - نسیم حقی: «دوره‌دیدهٔ موسیقی کودک به روش ارف»
  - علی شمس، محسن همایونی: no line (no bio yet).

  This would need one more short field on Teacher, `lineage` (Char 120, blank) **[beyond brief]**, or it can reuse the existing `home_intro` field, which today only shows for the director. Proposal: the new field.

### 3.6 How we teach (`teaching`)

- **Heading:** «شیوهٔ آموزش در آرامش»
- **یک استاد، یک هنرجو** — «همهٔ کلاس‌ها خصوصی است. استاد با سطح و هدف هر هنرجو پیش می‌رود، چه کودکی که تازه شروع می‌کند، چه بزرگسالی که سال‌ها آرزوی نواختن داشته است.»
- **استادانی که خود می‌نوازند** — «بیشتر استادان آرامش سابقهٔ اجرا در کنسرت‌ها و جشنواره‌ها دارند و ساز و ردیف را نزد استادان شناخته‌شده آموخته‌اند؛ همان راهی که موسیقی ایرانی همیشه از استاد به شاگرد رسیده است.»
- **از کلاس تا صحنه** — «هنرجویان می‌توانند پنجشنبه‌ها در گروه نوازی با هم بنوازند و در کنسرت‌های داخلی آموزشگاه، برای هنرجویان دیگر و خانواده‌هایشان اجرا کنند.» (concerts confirmed by the owner)

### 3.7 Three steps to your first lesson (`first_lesson`)

- **Heading:** «سه قدم تا اولین جلسه»
- **تماس بگیرید** — «با آموزشگاه تماس بگیرید یا فرم تماس را پر کنید.»
- **ساز و استاد را انتخاب کنید** — «با هم ساز، استاد و روز کلاس را بر اساس سن و هدف هنرجو انتخاب می‌کنیم.» **[owner: is this how it works?]**
- **به آموزشگاه بیایید** — «در روز و ساعت کلاس به آموزشگاه بیایید.» plus the address.

### 3.8 FAQ (first entries)

Questions as the brief lists them. Answers use facts where they exist; the rest are **[owner]**, because inventing a policy would be worse than an empty slot.

1. **«بهترین سن برای شروع موسیقی چیست؟»** — «برای کودکان خردسال، کلاس موسیقی کودک بهترین شروع است: آشنایی با نت و ریتم و سازهایی مانند بلز و فلوت. برای هر ساز، استاد همان ساز در تماس با شما دربارهٔ سن مناسب راهنمایی‌تان می‌کند.» **[owner: give the real ages]**
2. **«آیا باید از اول ساز داشته باشیم؟»** — **[owner]**
3. **«اولین جلسه چطور است؟»** — **[owner]**
4. **«گروه نوازی چیست؟»** — «گروه نوازی کلاسی است که هنرجویان، کنار کلاس خصوصی‌شان، با هم می‌نوازند. ویژهٔ کودکان، نوجوانان و بزرگسالان است و پنجشنبه‌ها با سرپرستی مسعود آرامش برگزار می‌شود.»

### 3.9 Contact band and page

- **Heading:** «برای انتخاب ساز و استاد، با ما تماس بگیرید»
- **Text:** the four phone numbers, the address, the hours from `SITE_HOURS`, and the Neshan route link.
- **Buttons:** «تماس با ۰۲۱ ۴۴۴۵ ۷۷۴۸» (primary) · «ارسال پیام» (to the form).
- **Contact success:** «پیام شما رسید. همکاران ما در ساعات کاری با شما تماس می‌گیرند.» **[owner: confirm they call back]**

### 3.10 Navigation and footer

- Navbar: «درباره ما · دوره‌ها · اساتید · برنامه کلاس‌ها · گالری», call pill «تماس ۰۲۱ ۴۴۴۵ ۷۷۴۸».
- دوره‌ها menu: the four Programmes and «همه سازها».
- Footer close: the logo at full width, the address, hours, phones, Instagram and Telegram.

---

## Part 4: Owner's answers at Gate 1 (2026-10-26)

- **All four [beyond brief] items: yes.** `Programme.instruments_shown`; FAQ `show_on_home` + `programmes`; `Teacher.lineage`; contact form with phone required and email optional.
- **Thursday hours:** do not touch `SITE_HOURS`. The owner will check with the Academy and change it in settings if needed. The schedule keeps showing the ensemble session's real time from the data.
- **Phones:** two primary numbers, the landline `021 4445 7748` and the mobile `+98 990 233 8431`. The navbar pill and the main call button use the landline, as in the brief («تماس ۰۲۱ ۴۴۴۵ ۷۷۴۸»); the mobile appears beside it, labelled «موبایل», wherever contact details are listed (hero contact line, contact band, contact page, footer). The other two numbers (`021 4445 7746`, `021 4613 3707`) are secondary and shown only on the contact page. `SITE_PHONES` is reordered so the two primaries come first (Phase C, step 7).
- **Age chips:** left blank. The owner will add them in the admin if the Academy has age limits; a blank chip hides.
- **FAQ:** no entries are seeded. The owner will add the Academy's answers in the admin; the section hides until then.
- **Concerts:** confirmed. The Academy holds internal concerts where students perform for other students and their families. Copy 3.6 updated.
- **Call-back:** confirmed. When a contact-form message arrives in the admin, the Academy calls the Visitor. Copy 3.9 stands.
- **Still open, for the Academy:** see [academy-questions-fa.md](academy-questions-fa.md). None of them blocks the build: each lands in an admin field, a setting, or copy that can be edited later.

## Part 4b: Facts that were open before Gate 1 (kept for history)


1. **Thursday hours conflict:** `SITE_HOURS` says «پنج‌شنبه: ۱۰ تا ۱۴», but Masoud Aramesh's Thursday ensemble session runs 10–19. Which is right?
2. **Age chips** for موسیقی کودک and تئوری و سلفژ (and whether «کودک تا بزرگسال» is right for کلاس خصوصی).
3. **FAQ answers** 1–3.
4. **Student concerts** (3.6) and **call-back** (3.9).
5. **Children's music:** the brief lists بلز and فلوت; Nasim Haghi's bio also mentions children's piano and voice. Should those appear on the موسیقی کودک page too?
6. **Phone numbers** (baseline critique, P0): the site shows four unlabelled numbers. Proposal: «۰۲۱ ۴۴۴۵ ۷۷۴۸» is the one number on every call button; the others appear only on the contact page, each with a label. Which number is which (landline, mobile/WhatsApp, office), and which answers in the evening?
7. **Contact form** (baseline critique, P0): today email is required and phone optional. Proposal **[beyond brief]**: phone required, email optional, since the Academy calls parents back. This changes `ContactForm` and `ContactMessage`.
