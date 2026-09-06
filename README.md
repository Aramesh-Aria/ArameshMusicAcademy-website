# Aramesh Music Academy Website

A Persian, right-to-left informational website for a Tehran music academy — it introduces the academy, its teachers, its class schedule and its concert gallery to visitors, and moves parents and adult learners toward contacting the academy. Enrollment, payment and student accounts are deliberately out of scope.

**Status:** In production &nbsp;·&nbsp;
🔗 **Live:** <https://aramesh-academy.ir> &nbsp;·&nbsp;
📦 **Releases:** no tagged releases — 54 commits on `main` &nbsp;·&nbsp;
🧪 **Tests:** Django test runner — 34 tests across the six apps (model validation, view context, gallery tree/slug logic, contact form + captcha)

---

## Screenshots

<!-- Add real captures to docs/images/ and update the paths below. -->

![Home page](docs/images/home.png)
![Admin — class schedule](docs/images/admin-schedule.png)

Until images are added, the running site is the best reference: <https://aramesh-academy.ir>.

---

## Problem

The academy had no web presence. Prospective students — mostly parents researching lessons for their children — could only learn about the teachers, the instruments taught and the weekly class times by phone or by visiting in person. There was no single place to see who teaches what, when classes run, or what past concerts looked like, and no low-friction way to send an inquiry.

## What I built

A server-rendered Django site in Persian with a Bootstrap 5 RTL layout and the Vazirmatn font. It covers a teacher directory, a rowspan-aware weekly class schedule grouped by teacher, a two-level photo gallery with embedded YouTube/Aparat concert videos, parent testimonials on the home page, CMS-editable content for the home/about/schedule pages, and a contact form (captcha-protected) that emails the academy on each submission. All content is managed from a Persian-branded Django admin (django-jazzmin) that also surfaces the unread-message count. The site is live in production on Runflare.

**My role:** Sole developer — requirements, domain modelling, architecture, implementation, tests and deployment.

---

## Architecture

| App | Responsibility |
|---|---|
| `config` | Single `settings.py` (no split settings), URL config, WSGI. `DEBUG` hardcoded `False`; contact info, social links and working hours live here. |
| `core` | No models. `context_processors.site_info` injects email/phones/address/year into every template; `sitemaps.py`; `admin_config` swaps in an admin site that shows the unread contact-message count; `seed_sample_data` management command. |
| `pages` | `SitePageContent` — CMS-style editable title/body/meta-description/hero-image for the named `home`, `about` and `schedule` pages, with hardcoded fallbacks. |
| `teachers` | `Instrument` and `Teacher` (M2M to `Instrument`, Jalali birth date, display order, active flag). List and detail views. |
| `schedules` | `ClassSession` — FK to `Teacher`, M2M to `Instrument`, weekday enum ordered Sat→Fri, start/end times with teacher-overlap validation. The view builds a rowspan grid grouped by teacher. |
| `gallery` | `GalleryPage` (self-FK tree, slug path, cover image; admin caps nesting at 2 levels), `GalleryImage`, and `Video` (YouTube/Aparat embed by URL). `context_processors.gallery_nav_tree` feeds the navbar dropdown. |
| `contact` | Captcha-protected `ContactForm`; `ContactMessage` stores submissions; a valid submission is saved and then emailed to the academy (mail failure is logged, never blocks the visitor). |
| `testimonials` | `Testimonial` — short parent quotes shown on the home page for social proof. |

When a visitor submits the contact form, `ContactView.form_valid` saves the `ContactMessage` first, then calls `send_notification`, which sends an `EmailMessage` to `CONTACT_NOTIFICATION_EMAIL` with the visitor's address as `reply_to`. The send is wrapped so any SMTP error is logged and swallowed — the submission is already persisted and the visitor still sees the success page. The email backend is chosen from env vars, so production uses Gmail SMTP while local dev and tests fall back to the console backend with no credentials.

---

## Key design decisions

| Decision | Why | Trade-off accepted |
|---|---|---|
| `ClassSession` links to instruments via M2M instead of a `Course` FK ([ADR-0001](docs/adr/0001-classsession-instruments-m2m.md)) | A teacher covers several instruments in one time slot; the old `Course`-per-instrument model forced duplicate session rows and required disabling overlap validation | One session concept that must be explained; the schedule grid needs rowspan logic to render one row per teacher slot |
| Informational site only — no enrollment, payment, login or student portal ([CONTEXT.md](CONTEXT.md)) | The goal is conversion: get the visitor to contact the academy. Everything else is scope the client does not need yet | Contact still happens off-site (phone, in person); nothing about enrolment is tracked in the system |
| Single `settings.py` with `DEBUG = False` hardcoded, config via a gitignored `.env` (`python-dotenv`) | One small single-tenant site on one PaaS; a base/dev/prod split would be ceremony with no payoff | Running locally means setting `DEBUG = True` by hand; secret key and allowed hosts sit in the committed file |
| SQLite in production, not PostgreSQL | Read-heavy brochure site with one admin editor; zero database ops, file lives on the Runflare disk | No real concurrent writes; a heavier traffic or multi-editor future would need a migration |
| Content editable through Django admin (`SitePageContent`, jazzmin theme) rather than a headless CMS or flat files | The academy staff update teachers, schedule and photos themselves without a deploy | Editors work in the Django admin UI; page structure is still fixed in templates |
| Vendored front-end assets (Bootstrap 5 RTL, AOS, GLightbox, Swiper, Isotope) committed under `static_dev/`, no build pipeline | No Node toolchain to maintain for a site whose JS needs are small and stable | Dependency updates are manual; `collectstatic` is the only asset step |
| Deployed from git on Runflare with WhiteNoise, no Docker | Iranian PaaS with the shortest path to a running site; WhiteNoise serves static files with no separate web server | Environment is defined by the platform, not the repo; less portable than a container |

---

## Tech stack

- **Language:** Python 3.12
- **Framework:** Django 5.2
- **Database:** SQLite (local and production)
- **Front end:** server-rendered templates, Bootstrap 5 RTL, Vazirmatn font; vendored AOS / GLightbox / Swiper / Isotope — no build step
- **Serving:** WhiteNoise (compressed static files), Runflare PaaS
- **Other:** `django-jalali` (Persian calendar), `django-simple-captcha`, `django-jazzmin` (admin theme), `Pillow`, `python-dotenv`, `django.contrib.sitemaps`, optional Google Analytics 4

---

## Getting started

```bash
git clone https://github.com/Aramesh-Aria/ArameshMusicAcademy-website.git
cd ArameshMusicAcademy-website
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # optional locally — fill in only what you need

# For local development, set DEBUG = True in config/settings.py so that
# static files are served from static_dev/ and you get detailed error pages.

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_sample_data   # optional: teachers, sessions, gallery pages/images
python manage.py runserver
```

**Environment variables** (all optional — sensible defaults are used when unset)

| Variable | Purpose |
|---|---|
| `EMAIL_BACKEND` | Set to `django.core.mail.backends.smtp.EmailBackend` in production; defaults to the console backend |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP credentials for the contact-form notification email (Gmail app password) |
| `DEFAULT_FROM_EMAIL` | From address for outgoing mail — defaults to `SITE_EMAIL` |
| `CONTACT_NOTIFICATION_EMAIL` | Inbox that receives contact-form submissions — defaults to `SITE_EMAIL` |
| `ABOUT_GALLERY_SLUG` | Slug of the gallery page whose images fill the "فضای آموزشگاه" block on the About page (default `academy-space`) |
| `GOOGLE_ANALYTICS_ID` | GA4 measurement ID (`G-XXXXXXXXXX`); empty disables the tracking script |
| `SITE_INSTAGRAM`, `SITE_TELEGRAM` | Social links in the footer; empty hides the link |

---

## Deployment

Deployed to **Runflare** straight from the git repository — no Docker image.

- WhiteNoise serves compressed static files, so there is no separate web server or CDN.
- After static changes, run `python manage.py collectstatic` (output goes to `public/static/`, the `STATIC_ROOT`).
- User uploads (teacher portraits, gallery images, hero images) are written to `public/media/`.
- SQLite database lives at `database/db.sqlite3` (gitignored); apply migrations with `python manage.py migrate` on deploy.
- Set the email env vars listed above in the Runflare dashboard so contact-form notifications actually send; without them the console backend only logs them.
- `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in `settings.py` cover `aramesh-academy.ir` and `aramesh-academy.runflare.run`; `SECURE_PROXY_SSL_HEADER` is set because Runflare terminates TLS at its proxy.
- To populate the About page, create a gallery page with the slug `academy-space` and add images to it.

---

## Testing

```bash
python manage.py test
# or per app:
python manage.py test gallery
```

34 tests across the six apps. Covered: `ClassSession` teacher-overlap validation and weekday ordering, gallery tree/slug-path and nesting rules, the contact form including a real generated captcha, and view context for the teacher, schedule and page views. Not covered: template rendering, the vendored front-end JS, and the email-notification path end to end.

---

## Roadmap

- [ ] Add real screenshots to `docs/images/` and wire them into this README
- [ ] Add CI (GitHub Actions) to run the test suite on every push
- [ ] Tag releases so deploys are traceable to a version
- [ ] Broaden test coverage to template rendering and the contact-email path

---

## Documentation

- [CONTEXT.md](CONTEXT.md) — domain vocabulary and scope boundaries
- [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) — the phased build plan and what shipped in each phase
- [docs/adr/](docs/adr/) — architecture decision records
- [CLAUDE.md](CLAUDE.md) — commands and architecture notes for working in the repo

---

## License

Proprietary — all rights reserved.

## Contact

Ahmad (Aria) Aramesh Moghaddam — aramesh_aria@yahoo.com — [github.com/Aramesh-Aria](https://github.com/Aramesh-Aria)
