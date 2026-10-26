# Handoff: Aramesh Music Academy redesign, Phase 2 (build)

Repo: `/Users/aria/Documents/ArameshMusicAcademy-website`, branch `re-design-ui`. Never touch `main`, never push.

## Hard rules from the user (override everything)
- **Do not commit anything.** No `git commit`, no `git add`/`git mv` staging either.
- **Move phase by phase, and stop after each phase (and each Phase 2 page/step if in doubt) for the user's approval.** Show screenshots, then wait.
- **Ask questions when something is unclear** rather than guessing.
- No emoji anywhere in templates.

## Start here
1. Run the `implement` skill on `docs/REDESIGN_PROMPT.md` (the full spec: phases, ground rules, skills list, authority order). Phase 0 and Phase 1 are **done**; begin at Phase 2.
2. Read, in this order:
   - `docs/redesign/01-direction.md`: the chosen direction, the page and section inventory mapped to context keys, proposals P1–P4, the vendor stay/go table, the CSS/JS architecture (§4), the Phase 2 order (§5), the skill conflicts (§6), and **"Decisions so far"** at the end.
   - `docs/redesign/00-inspection.md`: backend URLs, views, context keys, models, edge cases, real live content (§6), decisions (§7).
   - `PRODUCT.md` (impeccable product context) and `CLAUDE.md` (the static workflow, commands).
3. The visual source of truth is `docs/redesign/mockups/full-A.html` (`?page=home` / `?page=schedule`), with screenshots in `docs/redesign/mockups/screenshots/full/A-*.png`. `full-B.html` was rejected and serves as reference only.

## State at handoff
- Phase 1 is closed. The **user chose Direction A, "The programme"**, with one change: the home «اساتید آموزشگاه» section shows **three portraits** (one large with bio, two smaller beside it; rows with thumbnails on phone), taken from B. This is already in `full-A.html`. The director (first featured teacher) stays as the hero plate, so the section shows featured teachers 2–4. In production that means `featured_teachers` needs 4 items, `[1:4]` for the section, or `[:3]` when `page_hero_image` replaces the director plate.
- The impeccable direction choice was already recorded (`concept-seed --kind assigned`); don't resend it.
- A Phase 2 attempt was started and then **fully reverted at the user's request**. The working tree matches the session start: modified `.gitignore`, `CLAUDE.md`, `seed_sample_data.py`, `config/settings.py`; untracked `.taste-skill/`, `PRODUCT.md`, `docs/redesign/`. All of these are intentional Phase 0/1 work, so don't revert them. Templates and `static_dev/` are original.
- Tests: 34 passing at the end of Phase 0 (`python manage.py test`).

## Decisions the user made (don't re-ask)
- **Numbers:** Latin digits on the site. `SITE_HOURS` has already been changed to Latin. **`SITE_ADDRESS` keeps its Persian digits «۱۴۲»**; leave it.
- **Placeholder text** in the view fallbacks stays as it is.
- **Map:** keep the Google Maps embed and add a Neshan backup link (`https://neshan.org/maps/@35.745776,51.331922,17z`).
- **Gallery:** design for exactly two levels. The seed is fixed. No backend thumbnail generation.
- **P1 approved:** add a `week_schedule` context key to `HomeView`, with a test. **P2 approved:** prefetch sessions in `TeacherListView`, with a test. P3 is done. P4 is not pursued.
- **Logo:** the official logo is the teal Nastaliq wordmark plus the icons in `public/static/assets/img`. A transparent cutout made for the mockups is in `docs/redesign/mockups/img/logo-{paper,ink,jade}.png`. The user may be able to supply a proper transparent/vector version; ask if needed.
- The live site https://aramesh-academy.ir/ may be used for real content and screenshots. The local DB only has seed data.

## Notes from the reverted attempt (to save time)
- **Fonts:** Markazi Text variable woff2 (arabic + latin subsets) from `https://cdn.jsdelivr.net/fontsource/fonts/markazi-text:vf@latest/{arabic,latin}-wght-normal.woff2` downloaded fine. Self-host them under `static_dev/assets/fonts/`.
- **Tests assert on rendered text:** `apps/pages`, `teachers`, `schedules` ('شنبه', 'Guitar', not '11:00'), `gallery` (page and image titles), `contact` (admin count). Keep that content in the markup.
- **`aspect-ratio` gotcha:** an `<img>` with `width`/`height` attributes needs `height: auto`, or the attribute height wins.
- **Lazy images:** set them to eager before full-page Playwright screenshots, or they render blank.
- **Broken portraits:** two live teachers (علی شمس, محسن همایونی) point to missing media files. They need an initials fallback; catch the image `error` event early, from an inline head script.
- **Context available:**
  - `site_info` provides `site_phones`, `site_phone_primary`, `site_address`, `site_hours`, `site_email`, `site_instagram`, `site_telegram`, `current_year`, `site_instruments`.
  - `gallery_nav_tree` provides a list of `{page, children}`.
  - `Weekday` values are `sat…fri`, and `WEEKDAY_ORDER` is in `apps/schedules/models.py`.
  - The contact form widgets carry the class `form-input`, and there is a captcha refresh endpoint under `/captcha/`.
- **No `404.html` exists yet**, and `config/urls.py` has no handler.
- **Static workflow:** edit `static_dev/` (gitignored), run `collectstatic`, and the result lands in `public/static/`. Normally that gets committed, but **not now**.
- **Dev server:** `DEBUG=True python manage.py runserver`. A sandboxed curl to localhost timed out before, but Playwright reached it fine.

## Suggested skills
- `implement`: drives the phases from `docs/REDESIGN_PROMPT.md` (the user asked for it explicitly).
- `impeccable`: run `impeccable context` once, and read `reference/craft-floor.md` before UI edits. Use `document` at the end for DESIGN.md.
- `design-taste-frontend`: house rules and `inspect.mjs` checks. The directions in `.taste-skill/` are already drawn.
- `emil-design-eng`, `apple-design`: polish and interaction details.
- `find-animation-opportunities`, `animate`, `review-animations`, `animation-performance`: for the motion pass.
- `mobile-native`: the phone call bar, tap highlight, input zoom, safe areas.
- `break-ui`: worst-case data (long names, 6 instruments, empty bios, missing portraits, empty Friday, zero testimonials).
- `simplify`, `code-review`: for cleanup at the end of Phase 2.
