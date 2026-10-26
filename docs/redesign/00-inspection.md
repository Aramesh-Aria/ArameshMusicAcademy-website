# Phase 0: Inspection

Read-only inspection of the backend, templates, static files and the running site on `re-design-ui` (2026-10-26). The domain vocabulary follows `CONTEXT.md`.

"Before" screenshots of every page at 1440, 768 and 390 px are in `screenshots/before/`. `home-scrolled-*.png` shows the home page after scrolling, because AOS keeps every section below the fold invisible until it's scrolled into view, so plain full-page captures show blank areas.

---

## 1. Backend: what the frontend can show

### 1.1 URLs and views

| URL | Name | View | Template |
|---|---|---|---|
| `/` | `pages:home` | `HomeView` | `pages/home.html` |
| `/about/` | `pages:about` | `AboutView` | `pages/about.html` |
| `/teachers/` | `teachers:teacher_list` | `TeacherListView` | `teachers/teacher_list.html` |
| `/teachers/<pk>/` | `teachers:teacher_detail` | `TeacherDetailView` | `teachers/teacher_detail.html` |
| `/schedule/` | `schedules:schedule` | `ScheduleView` | `schedules/schedule.html` |
| `/gallery/` | `gallery:gallery_root` | `GalleryRootView` | `gallery/gallery_page.html` |
| `/gallery/<path:slug_path>/` | `gallery:gallery_detail` | `GalleryPageView` | `gallery/gallery_page.html` |
| `/contact/` | `contact:contact` | `ContactView` (FormView) | `contact/contact.html` |
| `/contact/success/` | `contact:contact_success` | `ContactSuccessView` | `contact/contact_success.html` |
| `/captcha/…` | django-simple-captcha | image and refresh endpoints | none |
| `/sitemap.xml` | sitemap | static views, active teachers, active gallery pages | none |
| `/favicon.ico` | redirect | to `static/assets/img/favicon.ico` | none |

There is **no `404.html` or `500.html`**. With `DEBUG=False`, Django's bare default pages render.

### 1.2 Global context (every template)

From `core.context_processors.site_info`:

| Key | Source | Current value / notes |
|---|---|---|
| `site_email` | `settings.SITE_EMAIL` | `aramesh.music.acad@gmail.com` |
| `site_phones` | `settings.SITE_PHONES` (list) | 4 numbers in `+98 21 4445 7748` form, Latin digits, spaces |
| `site_phone_primary` | `site_phones[0]` or `''` | used for `tel:` with `\|cut:' '` |
| `site_address` | `settings.SITE_ADDRESS` | long Persian string (about 80 chars) with a trailing space |
| `site_hours` | `settings.SITE_HOURS` (list) | 2 lines; can be `[]` |
| `site_instagram`, `site_telegram` | env, with defaults | can be `''` |
| `site_instruments` | `Instrument.objects.all()` | a query on every request |
| `google_analytics_id` | env | the GA snippet renders only when set |
| `current_year` | `datetime.now().year` | Gregorian (2026); the site otherwise speaks Persian |

From `gallery.context_processors.gallery_nav_tree`: `gallery_nav_tree` is a list of `{page, children:[…]}` nodes built recursively from **all active** `GalleryPage`s. Each `page` carries only `id, title, slug, parent_id`. Calling `get_absolute_url` walks `parent`, which costs **extra queries per node** (deferred fields). That is cheap at the current size, but worth knowing.

### 1.3 Per-view context

**`PageContentMixin`** (home, about, schedule) provides `page_content` (or None), `page_title`, `page_body`, `meta_description` and `page_hero_image` (an ImageFieldFile or None). It reads `SitePageContent` where `page_key=…` and `is_active=True`.

| View | Extra context |
|---|---|
| Home | `featured_teachers`: the first 3 active teachers, with instruments prefetched. `gallery_preview_images`: up to 6 active images from the gallery page whose slug is `ABOUT_GALLERY_SLUG` (default `academy-space`). `testimonials`: all active, unbounded. |
| About | `space_images`: **all** active images from the `ABOUT_GALLERY_SLUG` page, unbounded. |
| Schedule | `weekdays` (the `WEEKDAY_ORDER` enum list, Sat→Fri). `schedule_rows`: a list of `{teacher, instruments (sorted, union over the teacher's sessions), color_index (0–5), cells: [{weekday, label, sessions:[ClassSession]}] ×7}` |
| Teacher list | `teachers` (all active, no pagination) |
| Teacher detail | `teacher`, `meta_description` (from the bio, or a generated line), `teacher_sessions` (active, ordered by day and start) |
| Gallery root | `current_page=None`, `breadcrumbs=[]`, `child_pages` (active top-level), `images=[]`. **No `videos` key.** |
| Gallery page | `current_page`, `breadcrumbs` (root→current), `child_pages`, `images`, `videos` (active), `meta_description` |
| Contact | `form` (ContactForm) |

### 1.4 Models: what's optional

- **`SitePageContent`**: `page_key` is one of `home|about|schedule` (unique). `title` and `body` are required. `meta_description` is optional (160 chars). `hero_image` is optional and **cropped to 1200×800**. The help text says it's used only on home today; the mixin exposes it to about and schedule too.
- **`Instrument`**: only `name` (unique).
- **`Teacher`**: `first_name` and `last_name` (100 chars each). `instruments` is an M2M (the admin requires at least one, but it can be empty at the DB level). `biography` is **required, no length limit**. `profile_image` is **required** and **cropped to 600×600**. `display_order`. There is **no Jalali birth date field**, despite what `CLAUDE.md` says (see §5).
- **`ClassSession`**: `teacher` FK (PROTECT). `instruments` M2M (one or more). `weekday` (sat…fri). `start_time` and `end_time`. `notes` is optional, **no length limit, and shown in the grid**. The teacher-overlap check is in `clean()`.
- **`GalleryPage`**: `title`, `slug` (automatic, unicode allowed), `parent` (self-FK), `description` and `intro_text` (both optional), and `cover_image`, which is optional and **cropped to 900×600**.
- **`GalleryImage`**: `title` and `caption` are optional. `image` is required and **fitted inside 1920×1920**, keeping its aspect ratio (any shape: portrait, landscape, panorama).
- **`Video`**: `title`, `platform` (`youtube|aparat`), `video_url`, optional `caption`. `embed_url` returns None for unparseable URLs, and the template skips those silently.
- **`Testimonial`**: `author_name` (120). `relation` is optional (120). `quote` is unbounded.
- **`ContactMessage`** is written by the form and never shown publicly.

### 1.5 The contact form

`ContactForm(ModelForm)` has the fields `full_name`, `email`, `phone` (optional), `subject`, `message` and `captcha` (`CaptchaField`: a text input plus a hidden key plus an `<img>`, with no refresh button rendered). All widgets get the class `form-input` (`message` also gets `message-input`). The placeholders are Persian, and the labels are not rendered anywhere except for the captcha. The error messages are Persian.

On success the view saves the message, sends email (failures are logged and swallowed) and redirects to `/contact/success/`. **States to design for:** empty, field errors (including a wrong captcha) and success. There's no SMTP-failure state.

### 1.6 Sitemaps and seed data

The sitemap covers the static pages, active teachers and active gallery pages. `seed_sample_data` creates 4 instruments, 3 teachers (solid-color 400×400 squares with tiny initials), 5 sessions, 5 gallery pages and 5 images (solid colors).

It does **not** create testimonials, videos or `SitePageContent`, even though `CLAUDE.md` says it seeds testimonials. The local DB currently has 1 testimonial and 1 video that someone added by hand, and **no `SitePageContent`**, so every page shows its fallback.

### 1.7 Image pipeline (design constraints)

| Image | Processed size | Ratio | Notes |
|---|---|---|---|
| Teacher portrait | 600×600 | 1:1 | required; may be a phone selfie or a stage shot |
| Gallery cover | 900×600 | 3:2 | optional; fallback needed |
| Page hero | 1200×800 | 3:2 | optional; **at most 1200 px wide**, so a full-bleed hero looks soft at 1440 px and up |
| Gallery image | ≤1920 on the long side | any | unknown ratio; no thumbnails are generated, so grids download full-size files |

Everything becomes JPEG quality 85. There are no responsive `srcset` variants, so a 390 px phone downloads the 1920 px original in a grid. That's a performance gap the frontend can only partly mitigate (`loading=lazy`, `sizes`, `decoding=async`); see the proposals in Phase 1.

---

## 2. Frontend today

### 2.1 Stack

- The CoreBiz BootstrapMade theme. `main.css` has **4,904 lines**, with theme tokens `--accent-color: #09947d` and the fonts Roboto, Montserrat and Open Sans (overridden by an inline `--default-font: Vazirmatn`).
- **Vendors loaded on every page:** Bootstrap 5 CSS and JS bundle, Bootstrap Icons, AOS, GLightbox, Swiper, PureCounter, imagesLoaded, Isotope, php-email-form `validate.js`. **Only AOS, GLightbox and Bootstrap's grid are actually used.** Swiper, Isotope, PureCounter, imagesLoaded, Waypoints and validate.js serve nothing.
- **Fonts** come from Google Fonts (Vazirmatn). They aren't self-hosted, and Google Fonts is unreliable from Iran.
- Inline `<style>` blocks live in `base.html` and `schedule.html` (with its own palette of six Tailwind-ish row colors).
- `public/static/` is **30 MB** (Bootstrap source maps etc. alone are 8.3 MB).

### 2.2 Measured (home, Playwright, local dev server)

- 28 requests: **8 stylesheets and 9 scripts**, about **2.1 MB decoded**.
- LCP is the `<h1>` text at about 50–80 ms locally. That's unrealistic for production, where the render-blocking CSS, the Google Fonts round trip and 9 scripts dominate.
- Console errors: home requests `assets/img/bg/abstract-bg-1.webp` (referenced in `main.css:1079`), which **404s**. No other JS errors were seen.
- The fallback images referenced in templates, `assets/img/person/person-m-2.webp` and `assets/img/portfolio/portfolio-5.webp`, **don't exist**. They would 404 whenever a teacher or cover image is missing.

### 2.3 Page by page

| Page | What it does | Problems |
|---|---|---|
| **Shared header** | A green topbar (email and phone, `dir=ltr`), then the logo and nav. Gallery dropdown via a recursive partial. | The logo is an `<h1>` on every page, so there are **two `h1`s per page**. The mobile toggle is an `<i>` element: **not a button and not keyboard-reachable**. No skip link. No `aria-expanded`. The dropdown chevron toggles only by mouse. The topbar duplicates the footer. |
| **Footer** | Address, the first 2 phones, email, quick links, an "دوره‌ها" list (4 instruments all linking to the schedule), Telegram and Instagram icons. | "دوره‌ها" (courses) contradicts ADR-0001 (there are no courses). The social icons have no accessible names. No hours. Phones aren't `tel:` links. Gregorian year. |
| **Home** | A hero (title + body + 2 CTAs + an image), 3 teacher cards, testimonials, a 6-image space preview, a contact CTA. | The fallback body is a **developer placeholder** ("این صفحه فعلا به عنوان نقطه شروع بک‌اند و معماری Django…"), so it's live copy until the admin fills `SitePageContent`. The hero image is a static calligraphy logo, not a photo. A single testimonial sits alone in a 3-column grid. The gallery preview images aren't clickable into the lightbox (they link to the album). The CTA uses an email icon; no phone. Everything sits behind AOS fade-up. |
| **About** | Title + `page_body\|linebreaks` + a 3-column space gallery with GLightbox. | `<p class="lead">{{ page_body\|linebreaks }}</p>` nests `<p>` inside `<p>` (invalid HTML). The fallback body is again a placeholder ("محتوای این صفحه بعدا…"). No teachers, no CTA, so it's a dead end. |
| **Teacher list** | A 4-column card grid. | The bio is truncated at 120 chars. There's an empty state, but no CTA. Card names are `h4` under an `h2`, with no `h3`. |
| **Teacher detail** | Portrait, name, instruments, bio, a session list. | Duplicate name (`h1` in the page title, and an `h2`). No contact CTA, so a parent who decides here has nowhere to go. Times show as Latin digits `09:00 – 10:00` with `dir=ltr`. |
| **Schedule** | A table: teacher \| instruments \| 7 day columns, with the teacher column sticky, per-row tint bands and time chips. | **On a 390 px phone only Saturday is visible**, and the other six days need a horizontal scroll with no affordance. The heading "زمان‌بندی کلاس‌های تخصصی" is hardcoded. `page_body\|safe\|linebreaks` renders CMS HTML unescaped (a trusted admin, but notable). Notes render inside the chips with no length limit. Empty days show "—". Friday is always shown even when empty. Latin-digit times. |
| **Gallery root / page** | One template: optional intro, child-page cards (cover + overlay zoom + arrow), an image grid with GLightbox, video iframes. | A hardcoded "گالری / مرور تصاویر و رویدادها" title repeats on every gallery page, under the real `h1`. Breadcrumbs show "گالری" **and** the seed root "گالری تصاویر". **YouTube/Aparat iframes load eagerly** (heavy, and YouTube is filtered in Iran, so it shows as a blank box: confirmed in `gallery-videos-1440.png`). The overlay controls are hover-only. Images are forced to 3:2 with `object-fit:cover`, which crops portraits badly. The `<title>` doubles up as "گالری تصاویر \| گالری تصاویر" on a category named "گالری تصاویر". |
| **Contact** | Form (7 cols) + sidebar (5 cols): address, email, 4 phones, hours, Google Maps iframe, map link. | **On mobile the sidebar comes first** and the form starts far below the fold. **The inputs have no visible `<label>`s**, only placeholders (an a11y failure). The captcha has no refresh link. The Google Maps iframe is blank here (it's filtered/slow in Iran too), and the "open in map" link uses the button class. Phones aren't `tel:` links. Errors are plain text and not tied to inputs (`aria-describedby`, `aria-invalid`). |
| **Contact success** | A centered heading, a line and a home button. | Bootstrap `btn btn-primary` styling that differs from the rest. No next steps (call us, see the schedule). |
| **404** | None (Django's default). | Needs designing. |

### 2.4 Meta and SEO

`<title>`, a description, Open Graph and Twitter tags exist in `base.html`, with block overrides. Missing: **`<link rel="canonical">`**, page-specific `og:image` (teacher portraits and gallery covers would make better previews) and `theme-color` tied to the new palette. The OG image is a static `og-image.jpg`.

### 2.5 Accessibility baseline (home)

Landmarks: `header`, `nav`, `main` and `footer` all exist. **Two `h1`s.** The heading order skips (`h2`→`h4`). No skip link. The mobile toggle isn't a button. Social links have no names. Form inputs have no labels. Every image does have `alt`.

### 2.6 Housekeeping

The Playwright MCP writes logs to `.playwright-mcp/` in the repo root, and **that folder isn't gitignored**. It should be ignored before any commit.

---

## 3. Persian and RTL notes for the redesign

- **Digits (decided):** keep Latin digits for phones, times and numbers. No digit-conversion filter. The chosen fonts must render Latin digits well alongside Persian text, with tabular figures for times.
- **Times:** keep `09:00 – 10:00`, isolated with `dir=ltr` or `<bdi>` so the range doesn't flip.
- **Direction-sensitive pieces:** arrows ("←" means *forward* in RTL), chevrons, the sticky schedule column (right), slide-in directions, and the breadcrumb separators.
- **Year:** `current_year` is Gregorian. The Jalali year is available through `django_jalali`/`jdatetime` (already installed).

---

## 4. Edge cases the design must survive

| Case | Where it bites today | What the design must do |
|---|---|---|
| Long Persian names (for example «سیدمحمدحسین میرعمادی‌نژاد خراسانی») | card titles, the sticky schedule column (`white-space:nowrap`, `min-width:120px`) | wrap gracefully; no nowrap on names |
| A very long biography | the list truncates at 120 chars (fine). The detail page has one unbroken block. | readable measure (about 65ch), paragraph rhythm, maybe a pull-quote |
| A teacher with many instruments (6+) | comma lists overflow card subtitles | chips that wrap, or "+N" |
| A teacher with many sessions / one day with 3+ sessions | the chips stack in a cell; row height explodes | compact stacking; the mobile view lists them |
| A day with no sessions, or a whole week column empty (Friday) | "—" in every cell | dim or collapse empty days; consider hiding all-empty columns |
| A session covering many instruments | per-teacher instruments are unioned, so it's invisible per session | show per-session instruments where useful |
| Long session `notes` | rendered inside the time chip | clamp, or move to a tooltip/disclosure |
| An empty gallery category, or one with only children | only children: fine. Empty: one line. | a designed empty state |
| A gallery page with only videos | iframes load eagerly | a click-to-load facade |
| An unparseable video URL | skipped silently | fine (an admin-side issue) |
| Gallery images in any ratio | forced to 3:2 crop | a justified/masonry layout that respects ratio, or `object-position` |
| No testimonials / one / many | one sits alone in a 3-column grid; many are unbounded | a single featured quote layout; cap or scroll for many |
| `SitePageContent` missing | **the placeholder text shows publicly** | better fallback copy in the views (a view change, proposed in Phase 1) |
| No hero image | the static calligraphy logo shows | a designed typographic or illustrative hero that doesn't need a photo |
| Empty `site_hours` / social links / phones | hours: an empty labeled block; social: hidden; phones: an empty topbar link | hide each block when empty |
| Missing teacher portrait or gallery cover | the fallback files don't exist (404) | a CSS/SVG monogram or pattern fallback; no stock photos |
| No teachers / no sessions | simple text | a designed empty state with a contact CTA |
| A 3-level gallery (the seed creates `gallery-root/academy-concerts/concert-1404`) | renders fine, but the nav dropdown nests 3 deep | design for 2 levels; tolerate a 3rd |

---

## 5. Where CLAUDE.md doesn't match the code

1. **"Teacher (M2M to Instrument, Jalali birth date)"**: there's no birth date field on `Teacher`.
2. **"Nesting is capped at 2 levels in `clean()`"**: `GalleryPage.clean()` has no depth check. The cap is only enforced in `GalleryPageAdmin.formfield_for_foreignkey`, which offers only top-level parents. `seed_sample_data` creates a **3-level** tree, bypassing it.
3. **"seed_sample_data … teachers, sessions, gallery, testimonials…"**: it doesn't create testimonials, videos or page content.
4. The home view takes `gallery_preview_images` from the `ABOUT_GALLERY_SLUG` page (not across all galleries), so "about gallery" also feeds home.

None of these block the redesign. I'm noting them so the docs can be corrected later, outside this branch's scope unless you want it.

---

## 6. Real content on the live site (aramesh-academy.ir)

The local DB has only seed data, so I read the live site's real content (read-only) on 2026-10-26. The screenshots are in `screenshots/live/`. **Design against this data, not the seed.**

- **Teachers: 11.** Their instruments lean heavily on **Persian classical** (سنتور, تار, سه‌تار, تنبک, دف, آواز ایرانی) alongside piano, violin, pop guitar, accordion, hang drum, cajón and children's music. The director, مسعود آرامش, is a santur player and composer with 40+ years of activity.
  - **Instrument lists go up to 6** (علی شمس: آکوردئون، تئوری و سلفژ، هارمونیکا، پیانو، گیتار الکتریک، گیتار پاپ).
  - **Bios are 350–860 chars** for most, but **two teachers have an empty bio** (a single space or character), so the "required" field is effectively blank.
  - **Two teachers have broken portraits** (علی شمس, محسن همایونی). Their DB rows point at media files that no longer exist on the server (`teachers/teacher-1_*.jpg` returns 404). The template's `{% if teacher.profile_image %}` check passes, so no fallback shows, just a broken image. The design needs a **client-side fallback for images that fail to load** (for example an `onerror` swap to a monogram), not only a template-level one. The admin fix is re-uploading those two portraits.
  - Two portraits predate image processing and are **3408×3408 and 1254×1254**, much heavier than 600×600.
- **Schedule: 11 teacher rows, at most 1 session per cell, up to 5 instruments per row. Friday is empty for everyone.** Sunday and Thursday have one session each, and Saturday, Monday and Tuesday have four. No session notes are used. The schedule `SitePageContent` body is just the line "زمان‌بندی کلاس‌های تخصصی".
- **Home content exists live.** The hero body is "✨ موسیقی را بیاموز، آرامش را احساس کن 🎵 🎹", which contains emoji, so the hero typography must tolerate emoji. No hero image is uploaded (the static calligraphy image shows). **Zero testimonials**, so the "no testimonials" state is today's reality.
- **About content exists**: about 450 chars of real text with a list written as plain lines ("عمده فعالیت های آموزشگاه: …") and a Latin "40". `linebreaks` output must read well as a short list.
- **Gallery: one top-level page, `academy-space`, whose title is the slug itself ("academy-space")**, with 13 images and no children and no videos. **Most photos are portrait 960×1280 (3:4)**, with some 4:3 and square ones. The current forced 3:2 crop cuts the portrait photos badly, so the gallery layout must respect each photo's own ratio.

Edge cases from §4 that are **confirmed in production**: many instruments, an empty bio, a missing portrait, an empty weekday column, no testimonials, portrait-ratio gallery images, and a gallery title that is a Latin slug.

---

## 7. Decisions from review (2026-10-26)

1. **Fallback/placeholder text:** leave the view fallbacks as they are. Production has real `SitePageContent`.
2. **Map:** keep the Google Maps embed, and add a **Neshan** link as a backup for when Google Maps doesn't load.
3. **Digits:** keep Latin digits (see §3).
4. **Gallery depth:** design for exactly two levels (category → album). `seed_sample_data` now creates two levels only (`academy-concerts/concert-1404`, `academy-misc`, `academy-space`). In the local DB the old `gallery-root` is deactivated and its children moved to the top level.
5. **Image thumbnails:** no backend thumbnail generation.
6. **CLAUDE.md:** corrected for the mismatches in §5 (birth date, where the gallery cap is enforced, what the seed creates, and the shared `ABOUT_GALLERY_SLUG` photos).

---

## 8. Tests

`python manage.py test` runs 34 tests, all passing. The tests cover views and context (pages, teachers, schedule, gallery, contact), so template changes that keep the context keys and URL names won't break them. Some tests assert on rendered strings, which I'll check as templates change.
