# Implementation Plan

Derived from the grilling session on 2026-06-25. Each item references decisions recorded in `CONTEXT.md` and `docs/adr/`.

---

## Phase 1 — Domain Model Redesign ✅ DONE

> Foundational change. Must be done before anything that touches the schedule.

### 1.1 Remove `Course`, add `Instrument` M2M to `ClassSession` ✅

**Why:** A teacher's time slot covers multiple instruments simultaneously. The `Course` abstraction forced one session per instrument per teacher, which required disabling the overlap validation. See `docs/adr/0001-classsession-instruments-m2m.md`.

**Steps:**
- Remove `Course` model from `schedules/models.py`
- Add `instruments = ManyToManyField('teachers.Instrument')` to `ClassSession`
- Re-enable the teacher overlap validation in `ClassSession.clean()`
- Write and run the migration
- Update `ScheduleView` to group rows by Teacher (not Course)
- Update the schedule template accordingly
- Update `seed_sample_data` command to reflect the new model
- Delete all `Course`-related admin registrations

---

## Phase 2 — High Priority (Conversion) ✅ DONE

### 2.1 Contact form email notification ✅

**Why:** New inquiries arrive silently — the admin must log in to notice them. A missed inquiry is a missed enrollment.

**Steps:**
- Configure `EMAIL_BACKEND` and SMTP settings in `settings.py`
- In `contact/views.py`, send an email to `SITE_EMAIL` after a valid form submission
- Email should include: sender name, email, phone, subject, and message body

### 2.2 ✅ Home page — teacher preview section

**Why:** Parents trust faces. The home page currently has no dynamic content beyond the hero text.

**Steps:**
- In `HomeView.get_context_data`, query 3 active teachers ordered by `display_order`
- Add a "اساتید ما" section to `templates/pages/home.html` with teacher cards (photo, name, instruments)
- Each card links to the teacher's detail page
- Add a "مشاهده همه اساتید" link to `teachers:teacher_list`

### 2.3 ✅ Home page — gallery preview section

**Why:** Real photos of the academy build trust faster than text.

**Steps:**
- Query the 6 most recent active `GalleryImage` objects for the home page
- Add a gallery preview section to `templates/pages/home.html`
- Link to the main gallery page

### 2.4 ✅ Home page — testimonials section

**Why:** Parent social proof tips undecided visitors toward making contact.

**Steps:**
- Create `Testimonial` model in a new `testimonials` app (fields: `author_name`, `quote`, `is_active`, `display_order`)
- Register in admin
- Add to `HomeView` context
- Add testimonials section to `templates/pages/home.html` between the teacher preview and the contact CTA

### 2.5 ✅ Admin-editable hero image

**Why:** Changing the home page hero image currently requires a code deployment.

**Steps:**
- Add `hero_image = ImageField(blank=True)` to `SitePageContent`
- Apply `process_image` on save (consistent with other image fields)
- Write and run the migration
- Update `templates/pages/home.html` to use `page_hero_image` when available, falling back to the static file

### 2.6 ✅ SEO — meta descriptions and Open Graph tags

**Why:** The site has no `<meta name="description">` or Open Graph tags. SEO is a primary goal.

**Steps:**
- Add `meta_description = TextField(blank=True)` to `SitePageContent`
- Write and run the migration
- Add `{% block meta_description %}` and `{% block og_tags %}` to `base.html`
- In `PageContentMixin`, pass `meta_description` to context
- For teacher detail pages: auto-generate from the first 160 characters of `biography`
- For gallery pages: use `GalleryPage.description`
- For the contact page: add a static meta description block in the template
- Add Open Graph `og:title`, `og:description`, `og:image`, `og:url` to `base.html`

### 2.7 ✅ Sitemap

**Why:** Google needs a sitemap to discover and index all pages (teachers, gallery pages).

**Steps:**
- Add `django.contrib.sitemaps` to `INSTALLED_APPS`
- Create `sitemap.py` with sitemaps for: home, about, schedule, contact, teacher list, each teacher detail, each gallery page
- Wire to `sitemap.xml` URL in `config/urls.py`

---

## Phase 3 — Content & Trust ✅ DONE

### 3.1 ✅ About page — physical space photos

**Why:** Parents care about the environment their child will learn in.

**Steps:**
- Create a dedicated `GalleryPage` (e.g. "فضای آموزشگاه") for space photos
- In `AboutView`, query images from that page by a fixed slug (e.g. `academy-space`)
- Add a photo grid section to `templates/pages/about.html`

### 3.2 ✅ Teacher detail page — show schedule

**Why:** A visitor reading a teacher's bio naturally asks "when does this teacher teach?"

**Steps:**
- In `TeacherDetailView`, query the teacher's active `ClassSession` objects with their instruments
- Add a schedule section to `templates/teachers/teacher_detail.html`
- Display: instruments, weekday, start–end time for each session

### 3.3 ✅ Video embeds in gallery

**Why:** Concert videos and student performances are planned content.

**Steps:**
- Add `Video` model to `gallery` app (fields: `gallery_page FK`, `title`, `embed_url`, `platform` choices: YouTube/Aparat, `caption`, `is_active`, `display_order`)
- Register in admin
- Update the gallery detail template to render embedded videos alongside photos
- Validate that `embed_url` is a legitimate YouTube or Aparat URL

### 3.4 ✅ Analytics

**Why:** Knowing which pages convert and where visitors drop off is essential for improving the site.

**Steps:**
- Choose a provider (Google Analytics 4 or Plausible)
- Add tracking snippet to `base.html` inside a `{% block analytics %}` block
- Store the tracking ID in `settings.py`

---

## Phase 4 — Configuration & Admin UX ✅ DONE

### 4.1 ✅ Social links in `settings.py`

**Why:** Instagram and Telegram URLs are hardcoded in the footer template.

**Steps:**
- Add `SITE_INSTAGRAM` and `SITE_TELEGRAM` to `settings.py`
- Inject via `core/context_processors.py` (`site_info`)
- Update `templates/partials/footer.html` to use `{{ site_instagram }}` and `{{ site_telegram }}`
- Conditionally render each link (skip if empty)

### 4.2 ✅ Working hours in `settings.py`

**Why:** Office hours are hardcoded in the contact page template.

**Steps:**
- Add `SITE_HOURS` (list of strings) to `settings.py`
- Inject via `core/context_processors.py`
- Update `templates/contact/contact.html` to render `{{ site_hours }}`

### 4.3 ✅ Footer instrument list — dynamic from DB

**Why:** The footer hardcodes four instruments (پیانو، گیتار، ویولن، آواز). New instruments added to the schedule won't appear automatically.

**Steps:**
- In `core/context_processors.py`, query all `Instrument` objects and inject as `site_instruments`
- Update `templates/partials/footer.html` to loop over `site_instruments`
- Each instrument links to `schedules:schedule`

### 4.4 ✅ Cap gallery nesting to 2 levels in admin

**Why:** The `GalleryPage` model allows unlimited nesting but only 2 levels are used. Deep nesting would break the navbar dropdown.

**Steps:**
- In `gallery/admin.py`, override `get_form` or `formfield_for_foreignkey` to only show top-level pages as valid parent choices (i.e. exclude pages that already have a parent)

---

## Already Done

- ✅ Google Maps embed re-enabled on contact page
- ✅ "Get in Touch" translated to "با ما در ارتباط باشید"
- ✅ `CONTEXT.md` written
- ✅ `docs/adr/0001-classsession-instruments-m2m.md` written
- ✅ **Phase 1** — `Course` removed; `ClassSession.instruments` M2M added; overlap validation re-enabled; schedule view/template group by teacher; admin, seed data, and tests updated; migration `0006` applied
- ✅ Bug fix: `process_image` now no-ops gracefully when the file is missing on disk (unblocked the test suite)
- ✅ **Phase 2** — contact email notifications; home page teacher/testimonial/gallery preview + contact CTA; admin-editable hero image; SEO meta + Open Graph tags; `sitemap.xml`; new `testimonials` app; `SitePageContent.hero_image` + `meta_description`; migrations `pages/0004`, `testimonials/0001` applied
- ✅ Bug fix: `contact` captcha test now generates a real captcha (was a pre-existing failure) — full suite green (26 tests)
- ✅ Wired `python-dotenv` so a gitignored `.env` is loaded locally (real env vars still win on Runflare); added `.env.example`
- ✅ **Phase 3** — About page space-photo grid; teacher schedule on detail page; `gallery.Video` model (YouTube/Aparat embeds) + admin/inline + template; GA4 analytics gated on `GOOGLE_ANALYTICS_ID`; seed data + tests updated; migration `gallery/0004` applied. Full suite green (31 tests)
- ✅ **Phase 4** — social links (`SITE_INSTAGRAM`/`SITE_TELEGRAM`) and working hours (`SITE_HOURS`) moved to settings + context processor; footer instrument list now pulled from the `Instrument` model; footer social links conditional; gallery admin caps nesting at 2 levels (parent dropdown shows only top-level pages). Full suite green (32 tests)

## Deployment notes

- **Email (Phase 2):** production must set `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` plus `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` (and optionally `CONTACT_NOTIFICATION_EMAIL`) as env vars on Runflare. Without them, the console backend is used and notifications are only printed to logs.
- **Analytics (Phase 3):** set `GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX` (env var / `.env`) to activate Google Analytics. Empty = no tracking script rendered.
- **About page (Phase 3):** create a gallery page with slug `academy-space` (or set `ABOUT_GALLERY_SLUG`) and add images to populate the "فضای آموزشگاه" section. The seed data creates this page locally.
