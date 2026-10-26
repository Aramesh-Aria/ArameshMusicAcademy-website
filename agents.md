# agents.md

This file provides guidance to Opencode when working with code in this repository.


## Commands

```bash
source .venv/bin/activate                    # Python 3.12

DEBUG=True python manage.py runserver        # DEBUG defaults to False; True is needed for static serving + error pages
python manage.py makemigrations && python manage.py migrate
python manage.py seed_sample_data            # populate an empty DB (teachers, sessions, gallery, testimonials…)
python manage.py collectstatic --noinput     # required after any static change (see Static files)

python manage.py test                                         # all tests
python manage.py test apps.schedules                          # one app
python manage.py test apps.gallery.tests.SomeTestCase.test_x  # one test
```

There is no linter or frontend build step configured.

## Architecture

**Django 5.2, server-rendered, Persian RTL** (`lang="fa" dir="rtl"`, Amiri, no CSS framework). Informational site only: the goal is getting visitors to contact the academy. Enrollment, payment and student accounts are out of scope by design. `CONTEXT.md` defines the domain vocabulary (Visitor, ClassSession, GalleryPage, Testimonial, Conversion…) and the terms to avoid. ADRs live in `docs/adr/`.

**Apps** live under `apps/` and are installed as `apps.<name>`. App labels are the bare names, so migrations and table names don't include the `apps.` prefix.
- `core`: no models. `context_processors.site_info` injects site contact info, social links, hours and year into every template. `admin_config.ArameshAdminConfig` replaces `django.contrib.admin` in `INSTALLED_APPS` so the admin sidebar can show the unread contact-message count. Also holds `sitemaps.py`, `image_utils.process_image` and the `seed_sample_data` command.
- `pages`: `SitePageContent`, CMS-editable content for the named pages `home`, `about` and `schedule`, with hardcoded fallbacks in the views.
- `teachers`: `Instrument`, plus `Teacher` (M2M to Instrument, Jalali birth date).
- `schedules`: `ClassSession` has an FK to `Teacher`, an **M2M to `Instrument`** (no Course model, see ADR-0001), a Sat→Fri weekday enum, and start/end times with teacher-overlap validation in `clean()`. The view builds a rowspan grid grouped by teacher.
- `gallery`: `GalleryPage` is a self-FK tree routed by slug path (`gallery/<path:slug_path>/`). Nesting is capped at 2 levels in `clean()`. It also has `GalleryImage` and `Video` (a YouTube/Aparat embed built from a URL; videos are never uploaded). `context_processors.gallery_nav_tree` feeds the navbar dropdown on every page.
- `contact`: a form protected by django-simple-captcha. The view saves `ContactMessage` first, then emails `CONTACT_NOTIFICATION_EMAIL`. SMTP errors are logged and swallowed, so they never block the visitor.
- `testimonials`: `Testimonial`, parent quotes shown on the home page.

**Image processing on save:** `Teacher`, `GalleryPage` and `GalleryImage` override `save()` to resize/crop new uploads to JPEG via `core.image_utils.process_image`. This can change the stored filename, which is then written back with a queryset `.update()`.

**Templates** are project-level under `templates/` (not per-app), with `base.html` as the root layout. `templates/corebiz_raw/` holds raw reference files from the purchased CoreBiz theme. Nothing routes to them.

**Admin** uses the django-jazzmin theme. Staff manage all content through it.

## Configuration

- `config/settings.py` is the only settings file. It loads a gitignored `.env` via python-dotenv. On Runflare, real environment variables are used instead. See `.env.example` for the keys: `SECRET_KEY`, `DEBUG`, email/SMTP settings, `CONTACT_NOTIFICATION_EMAIL`, `ABOUT_GALLERY_SLUG`, `SITE_INSTAGRAM`/`SITE_TELEGRAM`, `GOOGLE_ANALYTICS_ID`.
- When no email env vars are set, the console email backend is used, so local dev and tests need no credentials.
- `ALLOWED_HOSTS`, `SITE_EMAIL`, `SITE_PHONES`, `SITE_ADDRESS` and `SITE_HOURS` are hardcoded in `settings.py`.
- Locale: `LANGUAGE_CODE = 'fa-ir'`, `TIME_ZONE = 'Asia/Tehran'`, and `django_jalali` for Persian dates.
- The database is SQLite at `database/db.sqlite3` (gitignored), in production too.

## Static and media files

- Edit sources in `static_dev/`. It is **gitignored and dev-only** (`STATICFILES_DIRS`). All styling is in `static_dev/assets/css/site.css` (plain CSS in cascade layers) and all behaviour in `static_dev/assets/js/site.js` (small vanilla modules, loaded with defer). There are no vendor libraries.
- After editing, run `collectstatic` and **commit `public/static/`** (`STATIC_ROOT`). Production serves that directory through WhiteNoise.
- Static URL is `/public/static/` and media URL is `/public/media/` (not the Django defaults). Uploads go to `public/media/`, which `config/urls.py` serves explicitly.

## Deployment

The site deploys from git to Runflare PaaS (`aramesh-academy.runflare.run`), with no Docker. The production domain is `aramesh-academy.ir`.
