# Redesign report: Aramesh Music Academy

The public site was rebuilt from scratch on the `re-design-ui` branch, following `docs/REDESIGN_PROMPT.md`. The chosen direction is **A, "The programme"** (`01-direction.md`): the site reads as the Academy's printed programme, with cool paper sheets on a green-black ground, one jade action and one Naskh family, and every photo printed in monochrome. The system is documented in [`DESIGN.md`](../../DESIGN.md).

This report takes the eight items of the $10K checklist one at a time, each with evidence and before/after screenshots at 1440, 768 and 390 pixels. It ends with performance numbers, the code review, known gaps, and what to do in the admin.

**About the screenshots**
- **Before** (`screenshots/before/`) is the old CoreBiz/Bootstrap theme on the local seed database.
- **Live** (`screenshots/live/`) is the production site's real content on 2026-10-26, for comparison.
- **After** (`screenshots/after/`) is the new design on a copy of that real content, served with `DEBUG=False`. The albums in the gallery screenshots come from a stress-test database, because the real site has no videos yet.

All screenshots are full-page. The Google map is grey in them because the iframe is cross-origin and lazy-loaded; it renders in a real browser.

---

## 1. Point of view, not a template

**Verdict: met.**

- **One direction, carried everywhere.** Every page is set as a programme: a sheet with a torn foot, columns of time, performer and instrument, and colour that changes only by whole chapters. The references are *Golha* radio listings and 1960s–70s Tehran concert programmes (see `01-direction.md`).
- **The home hero answers a parent's real question.** «امروز در آموزشگاه» (today at the academy) shows who teaches today and when, built from real ClassSession data. All seven days sit in a row, today is struck forward in ink, and Friday stays visible, marked تعطیل (closed).
- **Tied to this academy.** The director's black-and-white portrait at the santur sits on the far side as a tipped-in plate with a short introduction. The jade comes from the Academy's own Nastaliq wordmark.
- **Inspector.** taste-skill's inspector found no template tells on any of the 11 pages: no gradients, eyebrow labels or card grids. What it did flag is listed under [Known gaps](#known-gaps).

| Width | Before | After |
|---|---|---|
| 1440 | ![](screenshots/before/home-1440.png) | ![](screenshots/after/home-1440.png) |
| 768 | ![](screenshots/before/home-768.png) | ![](screenshots/after/home-768.png) |
| 390 | ![](screenshots/before/home-390.png) | ![](screenshots/after/home-390.png) |

## 2. Typography that does work

**Verdict: met, with one approved deviation.**

- **One family.** The checklist asks for "a paired display face and body face". At Phase 2, step 1, you replaced Markazi Text with **Amiri** (Khaled Hosny, OFL) as a single family for display and text, as a programme would be set. Neither Inter nor Roboto is used.
- **Self-hosted fonts.** The woff2 files are subset into a Persian file and a Latin file per weight:
  - Persian: 43 KB per weight;
  - Latin: 20 KB per weight.

  They load with `font-display: swap`, and the two Persian weights are preloaded. No font comes from a CDN, which matters during Iran's internet cuts.
- **Hierarchy from scale and weight.** There are five sizes (18, 21, 22–27, 34–48 and 44–80px) and two weights (400 and 700), because Amiri ships no 600. Body text is 21px at 1.6 leading on a 34em measure, and headings keep 1.2 leading for Amiri's tall letters.
- **Numbers.** Phones and times use Latin digits, tabular and lining, kept left-to-right inside RTL text. The street address keeps its Persian digits, by your decision.

| Width | Before | After |
|---|---|---|
| 1440 | ![](screenshots/before/teacher-1440.png) | ![](screenshots/after/teacher-1440.png) |
| 768 | ![](screenshots/before/teacher-768.png) | ![](screenshots/after/teacher-768.png) |
| 390 | ![](screenshots/before/teacher-390.png) | ![](screenshots/after/teacher-390.png) |

## 3. A restrained colour system

**Verdict: met.**

- **Five colours, all tokens.** The palette is green-black, cool paper, jade, white and an error red, each with only the steps it needs for contrast. They are defined in the tokens layer of `site.css` and listed in the `DESIGN.md` frontmatter.
- **Jade marks two things only:** the call action and focus rings.
- **Whole chapters.** A `.sheet` flips the surface, text and focus roles together, so no component hard-codes a colour for where it sits.
- **Contrast measured.**
  - Ink on paper: 14.1:1.
  - Soft ink on paper: 6.9:1.
  - Text on the ground: 13.5:1.
  - White on jade: 5.3:1.
  - Error red on paper: 6.3:1.

  The lowest contrast measured on a rendered page is 5.27:1.

| Width | Before | After |
|---|---|---|
| 1440 | ![](screenshots/before/schedule-1440.png) | ![](screenshots/after/schedule-1440.png) |
| 768 | ![](screenshots/before/schedule-768.png) | ![](screenshots/after/schedule-768.png) |
| 390 | ![](screenshots/before/schedule-390.png) | ![](screenshots/after/schedule-390.png) |

## 4. Hierarchy that breathes

**Verdict: met.**

- **One h1 per page, and no skipped heading levels.** Checked on all 11 pages at 1440 and 390.
- **Rhythm.** Chapters sit 96–160px apart on one 12-column grid. Inside a sheet there are clear primary (h1 or name), secondary (lead and instruments) and tertiary (meta, times and days) levels.
- **The teachers page** is a programme index rather than a card grid. Each entry has a name, instruments and days, and the portrait appears on hover or focus at desktop width. Thumbnails stay visible on the phone.
- **Long content.** Long notes and titles are clamped:
  - schedule notes to 2 lines, with the full text in a tooltip;
  - gallery titles to 3 lines.

  Testimonials are capped at 3, so worst-case content can't flatten the page (break-ui, Phase 3).

| Width | Before | After |
|---|---|---|
| 1440 | ![](screenshots/before/teachers-1440.png) | ![](screenshots/after/teachers-1440.png) |
| 768 | ![](screenshots/before/teachers-768.png) | ![](screenshots/after/teachers-768.png) |
| 390 | ![](screenshots/before/teachers-390.png) | ![](screenshots/after/teachers-390.png) |

## 5. Imagery with intent

**Verdict: met for treatment; the files themselves are a known gap.**

- **One darkroom process.** Every upload is shown in monochrome (grayscale with contrast 1.06) on a paper plate, so mixed phone snapshots read as one set.
- **Real ratios.** Plates use the ratio the pipeline produces:
  - portraits: 1:1;
  - covers: 3:2;
  - page heroes: 3:2;
  - gallery photos: their own ratio, in balanced columns.

  Nothing is force-cropped, which fixes the old 3:2 crop that cut portrait photos badly.
- **Fallbacks.**
  - A missing or broken portrait shows the teacher's initials on a paper plate.
  - A gallery page with no cover now uses its first active photo (`GalleryPage.display_cover`). With no photos at all, it shows a paper plate set with the title.
- **Loading.** Photos that are still loading develop out of the paper tone once; images already cached show at once.
- **Lightbox.** Built in-house to replace GLightbox. It has keyboard support, swipe with a spring-back, and returns focus to the photo when it closes.

| Width | Before | After |
|---|---|---|
| 1440 | ![](screenshots/before/gallery-space-1440.png) | ![](screenshots/after/gallery-space-1440.png) |
| 768 | ![](screenshots/before/gallery-space-768.png) | ![](screenshots/after/gallery-space-768.png) |
| 390 | ![](screenshots/before/gallery-space-390.png) | ![](screenshots/after/gallery-space-390.png) |

## 6. Motion that whispers

**Verdict: met.**

- **No AOS fade-up anywhere.** AOS, Swiper, Isotope, GLightbox, PureCounter and Waypoints were all removed. Motion is "printed paper, handled":
  - **Struck day:** an ink block slides between day tabs (220ms, ease-in-out, interruptible). It is a clipped ink copy of the tab row, so the colour change is exact.
  - **Programme rows:** they fade over 140ms when the day changes.
  - **Develop:** photos still loading come up out of the paper tone (600ms, once).
  - **Entrance:** the opening section is set down on load, its parts 60ms apart (480ms, opacity plus a 0.75rem rise, CSS only). Later sections rise about 2rem into place as they scroll in. This uses a CSS scroll timeline and moves them only, so a page captured without scrolling never shows them missing.
  - **Lightbox swipe:** the photo follows the finger and springs back (a 560ms damped spring with 1.5% overshoot).
  - **Press feedback:** pressable controls scale to 0.97 over 120ms. Hover effects run only on devices that can hover.
- **Video facade.** Videos no longer load YouTube or Aparat iframes on page load. A paper poster is replaced by the iframe on click, and the iframe fades in when it has loaded.
- **Reviews.** `review-animations` and `animation-performance` ran in Phase 3, and their findings were fixed. Everything animates transform, opacity or clip-path only.
- **Reduced motion.** Nothing travels. State changes are instant, fades keep an 80–160ms beat, and the scroll settle is off.

Entrance filmstrips, 0–700ms:

| Home 1440 | Home 390 | About 1440 |
|---|---|---|
| ![](screenshots/motion/entrance-home-1440.png) | ![](screenshots/motion/entrance-home-390.png) | ![](screenshots/motion/entrance-about-1440.png) |

Video facade (stress-test data):

| Width | Before | After |
|---|---|---|
| 1440 | ![](screenshots/before/gallery-videos-1440.png) | ![](screenshots/after/gallery-videos-1440.png) |
| 768 | ![](screenshots/before/gallery-videos-768.png) | ![](screenshots/after/gallery-videos-768.png) |
| 390 | ![](screenshots/before/gallery-videos-390.png) | ![](screenshots/after/gallery-videos-390.png) |

## 7. Mobile that's designed, not shrunk

**Verdict: met.**

- **Navigation.** A full-screen menu on the ground opens from «منو». It closes with Escape, a link, or rotating the phone into the desktop layout, and focus returns to the toggle.
- **Always-reachable contact.** A fixed bottom bar carries «تماس» (a `tel:` link) and «مسیر» (directions), and respects safe areas.
- **Schedule.** The desktop week grid becomes a day view on the phone. Day tabs shorten to their first letter, and each day lists time, teacher and instruments. The whole week is never shrunk into a miniature.
- **Gallery.** Photos sit in two balanced columns, and the lightbox supports swipe.
- **Contact form.**
  - Fields are 48px tall and their text is at least 16px, so the page never zooms on focus.
  - The captcha refresh is an icon button of at least 44px.
  - Error states show a summary that takes focus.
- **mobile-native pass.** No tap-highlight flash, no sticky hover, `dvh` instead of `100vh`, and safe-area padding.

| Width | Before | After |
|---|---|---|
| 1440 | ![](screenshots/before/contact-1440.png) | ![](screenshots/after/contact-1440.png) |
| 768 | ![](screenshots/before/contact-768.png) | ![](screenshots/after/contact-768.png) |
| 390 | ![](screenshots/before/contact-390.png) | ![](screenshots/after/contact-390.png) |

## 8. The invisible expensive stuff

**Verdict: met, except the LCP target on two gallery pages on a slow phone connection** (see [Performance](#performance)).

- **LCP under 2s.**
  - All 11 pages meet it on desktop.
  - On a throttled phone (slow 4G), 9 of 11 meet it.
  - The gallery root (2.08s) and the photo-heavy album (7.3s) miss it because they serve full-size uploads.
- **WCAG AA contrast.** Measured on every page; there are no failures, and the minimum is 5.27:1.
- **Keyboard.** Checked with Playwright on 1440 and 390:
  - The first Tab reaches a skip link, and Enter on it jumps to the main content.
  - All 30 tab stops on the home page show a visible focus ring, and none of them is off screen.
  - The gallery menu opens with Enter, and Escape closes it and returns focus to its button.
  - The phone menu opens with Enter and moves focus inside; Escape closes it and returns focus to the toggle.
  - The day tabs follow RTL arrow keys (← is the next day), and Home and End work.
  - The lightbox opens with Enter, the arrow keys move between photos, and Escape closes it and returns focus to the photo.
  - The map iframe shows a focus ring while it holds focus.
- **Landmarks and meta.**
  - Every page has a header, nav, main and footer, `lang="fa" dir="rtl"`, a unique `<title>` and a meta description.
  - Each page has a canonical link and Open Graph and Twitter cards, all naming `https://aramesh-academy.ir`. Teacher, gallery and hero pages use their own photo as `og:image`.
- **Forms.** Every field has a label, errors are tied to their fields, and the error summary takes focus. The captcha has an accessible refresh button.
- **Console.** There are no errors or 404s on real data. The only console errors in testing came from portraits deliberately missing in the stress-test data, which show the initials fallback.
- **Tests.** `python manage.py test`: 65 tests, all passing.

| Width | Before | After |
|---|---|---|
| 1440 | ![](screenshots/before/404-1440.png) | ![](screenshots/after/404-1440.png) |
| 768 | ![](screenshots/before/404-768.png) | ![](screenshots/after/404-768.png) |
| 390 | ![](screenshots/before/404-390.png) | ![](screenshots/after/404-390.png) |

---

## Remaining before/after pages

| Page | 1440 | 768 | 390 |
|---|---|---|---|
| About, before | ![](screenshots/before/about-1440.png) | ![](screenshots/before/about-768.png) | ![](screenshots/before/about-390.png) |
| About, after | ![](screenshots/after/about-1440.png) | ![](screenshots/after/about-768.png) | ![](screenshots/after/about-390.png) |
| Gallery root, before | ![](screenshots/before/gallery-root-1440.png) | ![](screenshots/before/gallery-root-768.png) | ![](screenshots/before/gallery-root-390.png) |
| Gallery root, after | ![](screenshots/after/gallery-root-1440.png) | ![](screenshots/after/gallery-root-768.png) | ![](screenshots/after/gallery-root-390.png) |
| Gallery category, before | ![](screenshots/before/gallery-cat-1440.png) | ![](screenshots/before/gallery-cat-768.png) | ![](screenshots/before/gallery-cat-390.png) |
| Gallery category, after | ![](screenshots/after/gallery-cat-1440.png) | ![](screenshots/after/gallery-cat-768.png) | ![](screenshots/after/gallery-cat-390.png) |
| Gallery album, before | ![](screenshots/before/gallery-album-1440.png) | ![](screenshots/before/gallery-album-768.png) | ![](screenshots/before/gallery-album-390.png) |
| Gallery album, after | ![](screenshots/after/gallery-album-1440.png) | ![](screenshots/after/gallery-album-768.png) | ![](screenshots/after/gallery-album-390.png) |
| Contact success, before | ![](screenshots/before/contact-success-1440.png) | ![](screenshots/before/contact-success-768.png) | ![](screenshots/before/contact-success-390.png) |
| Contact success, after | ![](screenshots/after/contact-success-1440.png) | ![](screenshots/after/contact-success-768.png) | ![](screenshots/after/contact-success-390.png) |

---

## Performance

**How it was measured**
- Playwright on Chromium against the real-content copy, served with `DEBUG=False` through WhiteNoise, with a cold cache on every run.
- **Desktop:** 1440×900 on an unthrottled connection.
- **Phone:** 390×844, throttled to slow 4G (1.6 Mbps down, 150ms latency).
- **Transfer:** bytes over the wire, compressed, for everything loaded by the end of the run (lazy images included once they load).
- These are single runs on localhost, so they leave out real server and CDN distance. Treat them as relative, not absolute.

| Page | Desktop FCP | Desktop LCP | Desktop transfer | Phone FCP | Phone LCP | Phone transfer |
|---|---|---|---|---|---|---|
| Home | 92 ms | 640 ms (portrait) | 1,280 KB / 19 req | 688 ms | 1,088 ms (lead) | 287 KB / 11 req |
| About | 72 ms | 556 ms | 2,253 KB / 22 req | 688 ms | 1,036 ms | 2,253 KB / 22 req |
| Teachers | 108 ms | 560 ms | 644 KB / 20 req | 672 ms | 1,104 ms | 616 KB / 20 req |
| Teacher | 76 ms | 608 ms (portrait) | 244 KB / 10 req | 688 ms | 1,124 ms | 244 KB / 10 req |
| Schedule | 88 ms | 556 ms | 213 KB / 9 req | 708 ms | 1,092 ms | 213 KB / 9 req |
| Gallery root | 92 ms | 608 ms (cover) | 347 KB / 10 req | 660 ms | **2,076 ms** (cover) | 347 KB / 10 req |
| Gallery: space | 76 ms | 708 ms (photo) | 2,253 KB / 22 req | 676 ms | **7,260 ms** (photo) | 2,253 KB / 22 req |
| Gallery: concerts | 76 ms | 540 ms | 190 KB / 9 req | 672 ms | 672 ms | 190 KB / 9 req |
| Contact | 72 ms | 540 ms | 198 KB / 10 req | 756 ms | 1,220 ms | 198 KB / 10 req |
| Contact success | 96 ms | 560 ms | 190 KB / 9 req | 740 ms | 1,208 ms | 190 KB / 9 req |
| 404 | 76 ms | 560 ms | 190 KB / 9 req | 688 ms | 1,040 ms | 190 KB / 9 req |

**Before**
- The old home page made 28 requests: 8 stylesheets and 9 scripts, about 2.1 MB decoded.
- It also requested a missing background image (404) and loaded fonts from Google.
- `public/static/` held 29.8 MB in git.

**After**
- **Shell.** One stylesheet (56 KB, 12 KB compressed) and one deferred script (17 KB, 5.5 KB compressed). The text-only pages weigh about 190–245 KB in total, most of it the four font files.
- **`public/static/`.** Down to 16.9 MB in git. Most of what's left is the Django admin and the theme files Jazzmin collects.
- **The entrance animation.** It moves LCP back by about 480ms on desktop: text paints at about 80ms, but Chrome counts LCP when the fade finishes. Every page still finishes well under 2s.
- **The two misses** are both caused by image files rather than the page:
  - The space album and About load up to 13 full-size uploads (up to 1920px each, 2.2 MB in total). The backend makes no thumbnails, which was decided in Phase 0.
  - The gallery root's cover for «فضای آموزشگاه» is a full-size photo, because no 900×600 cover has been uploaded. The new fallback uses the first photo.
  - In this pass, the first row of gallery covers was changed from lazy to eager loading, so the largest one starts loading at once.

---

## Code review

`code-review` ran against `main`, on two axes in parallel: Standards (`CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, the ADR and `DESIGN.md`) and Spec (`REDESIGN_PROMPT.md` and `01-direction.md`).

**Standards: 3 hard findings and 9 judgement calls. Worst: `DESIGN.md` rules stricter than the shipped code.**

| Finding | Outcome |
|---|---|
| Six fluid font sizes outside the five type steps (initials, the week title, the teacher plate names, the single letter, the 404 numeral) | **Fixed in `DESIGN.md`.** These are deliberate display sizes, so the rule now names them as exceptions. |
| Transitions on `background-color`, `filter` and `clip-path`, while `DESIGN.md` said "transform and opacity only" | **Fixed in `DESIGN.md`.** Anything that travels uses transform or opacity. State fades may use colour or filter, and the struck day uses clip-path, as the motion review approved. |
| `CLAUDE.md` and `AGENTS.md` don't list `SITE_MAP_NESHAN` or `SITE_MAP_EMBED`, and still describe the schedule as a "rowspan grid" | **Not changed.** These are your agent-guidance files; the edits are proposed below. |
| The Google Maps iframe loads from google.com | **Kept, by your decision.** The Neshan link is the offline-safe backup. |
| `display_cover` runs one query per child page without a cover | **Kept.** An index has only a few child pages. Prefetching every photo row to save those queries would cost more. |
| The gallery `og:image` repeated the cover fallback | **Fixed.** It now uses `display_cover`. |
| "Director" isn't in `CONTEXT.md` | **Proposed below.** |
| `week.active_sessions()` shares its name with Teacher's prefetched `active_sessions` and is a thin wrapper | **Kept.** Minor, and both read clearly where they're used. |
| `.order_by('weekday_order', 'start_time')` repeats the model's `Meta.ordering` | **Kept.** It differs on purpose. `Meta.ordering` adds `teacher__last_name`, which joins the teacher table, and both teacher views fetch only one teacher's sessions, where that join is wasted. |
| Schedule rows are dicts beside typed `Day` cells | **Kept.** This is a judgement call. |
| A commented-out `SITE_MAP_GOOGLE` while `site_map_google` is still added to the template context | **Kept.** You switched the Google route link off; the footer shows it again when the setting is set. |
| Director and testimonial tests sit inside the week-schedule test class | **Kept.** Minor. |
| `_subpage.html` loads the first three covers eagerly, which assumes a three-column first row | **Kept.** It is documented in the template comment; on the phone this means at most two extra covers. |

**Spec: 7 findings. Worst: the canonical URL takes its host from the request.**

| Finding | Outcome |
|---|---|
| Instruments are no longer listed in the footer | **Kept.** The approved "every page" inventory in `01-direction.md` doesn't include instruments in the footer. Instruments appear on the home page, the teachers pages and the schedule. |
| The schedule isn't a rowspan grid | **Deliberate.** Direction A's "transit diagram" raise has one row per teacher with days as columns, and each cell stacks that day's sessions. It is still grouped by teacher, with each session's instruments. |
| Context keys changed (`weekdays` and `color_index` removed, `week_schedule` added to the schedule view, `featured_teachers` split into `director` and `home_teachers`) | **Recorded here.** P1 and the three-portrait decision cover the home view. The schedule-view change came with the day view and was not proposed separately. |
| A new `ClassSessionQuerySet`, and the seed's "gallery-root" page dropped | **Recorded here.** Both are internal and covered by tests. |
| An HTML comment shipped a dead email block in the contact page source | **Fixed.** It is now a `{% comment %}` block, so nothing renders. |
| The canonical, og:url and og:image host come from the request, so pages served on `aramesh-academy.runflare.run` call themselves canonical | **Fixed.** A new `SITE_DOMAIN = 'aramesh-academy.ir'` setting (exposed as `site_url`) now builds all three, whichever host served the page. `sitemap.xml` uses the same domain over https, through a shared `PublicSitemap` base. Tests cover both. |
| Gallery photos have no `width` or `height`, so the page can shift as they load | **Open.** Photos keep their own ratio and the model doesn't store dimensions. The fix needs width and height fields (a migration). |

---

## Known gaps

1. **Full-size gallery images.** Albums and About serve original uploads (up to 1920px), with no thumbnails. On a slow phone connection, the 13-photo album needs about 7s to its largest paint. The fix is a backend thumbnail step, for example a 900px-wide copy made on save. It was ruled out in Phase 0, so it's listed here as a proposal and not built.
2. **Entrance motion and LCP.** Chrome counts the opening section's LCP when its 480ms fade ends. Starting the fade from a barely visible opacity instead of 0 would make LCP match first paint. Left as is, since every page stays under 2s on desktop.
3. **One typeface.** Amiri is used for both display and text, by your decision. This departs from the checklist's "paired display and body face".
4. **Home photo preview.** The masonry columns end unevenly, because photos keep their natural ratios (approved earlier). It's a judgement call, not a bug.
5. **Teacher page at 768px.** The portrait stands alone above the sheet. This is minor.
6. **Inspector findings left on purpose.**
   - **"Still page" on short pages:** the motion is kept restrained by design.
   - **One shadow:** on the gallery dropdown, which really floats.
   - **Hairline rules:** they are part of the programme style.
   - **Too few pictures:** on the teachers, schedule and contact pages, by design.
   - **No video:** there is no footage yet.
   - **False alarms:** "off-centre" on the schedule (the table doesn't fill its sheet) and "covered text" (the sticky header passes over text while scrolling).
7. **The map** is Google Maps, which may not load during internet cuts. The Neshan link is the backup.
8. **Gallery photo dimensions.** Album and About photos have no `width` or `height`, so the columns can shift as photos load. The proposed fix is `width_field` and `height_field` on `GalleryImage` (a migration), written into the `<img>` tags.
9. **Docs to update.** In `CLAUDE.md` and `AGENTS.md`:
    - add `SITE_MAP_NESHAN` and `SITE_MAP_EMBED` to the list of hardcoded settings;
    - describe the schedule as "one row per teacher, a cell per day" instead of "a rowspan grid".

    In `CONTEXT.md`, define the **Director** (the Teacher shown in the home hero plate).
10. **Admin theme files.** About 9.5 MB of Jazzmin/Bootswatch theme CSS is still collected into `public/static/`. Only the admin uses it, and Visitors never download it.

## Admin to-dos

1. **Run the migrations on Runflare:** `python manage.py migrate`. The branch adds three:
   - `pages` 0005: help text on titles;
   - `gallery` 0005: help text on titles;
   - `teachers` 0006: `Teacher.home_intro`.
2. **Write the director's home introduction.** In the admin go to Teachers, then مسعود آرامش, then «معرفی در صفحه اصلی». Two or three sentences for parents, separate from the biography.
3. **Upload a cover for every gallery page,** especially «کنسرت سال ۱۴۰۴», which has no photos yet and shows an empty paper plate. Covers are cropped to 900×600, so use a landscape photo.
4. **Add descriptions** to «گالری» and «فضای آموزشگاه», so the first screen says what the visitor is looking at.
5. **Upload a page hero for About,** a 3:2 landscape photo at 1200px or more. It turns the About sheet into a sheet plus a plate. Without one, the sheet shows the fallback text alone.
6. **Write the home and About page text** in Page content (SitePageContent). The new fallback copy is real copy, but the Academy's own words are better.
7. **Remove the emoji** from the live home text («✨», «🎵», «🎹»). The design sets text in Amiri, and emoji break the programme look.
8. **Keep titles short.** Gallery titles are clamped at 3 lines and schedule notes at 2, with help text in the admin saying so.
9. **Add testimonials** from parents. The home page shows up to 3 and hides the section when there are none.
10. **Optional:** get a vector or transparent original of the wordmark, so the logo files can be replaced with a crisper version.
