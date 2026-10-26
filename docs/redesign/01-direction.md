# Phase 1: Direction

**Status: waiting for your choice.** No production templates have been written.

Inputs: [00-inspection.md](00-inspection.md), [`PRODUCT.md`](../../PRODUCT.md) and the live site's real content.

**Mockup:** [`mockups/prototype-home-hero.html`](mockups/prototype-home-hero.html). Open it in a browser and switch with `?variant=A|B|C`, the pink bar, or the ← → keys. It's a throwaway prototype: real live content and the academy's own photos (downloaded to `mockups/img/`), with fonts from a CDN for the prototype only.

**Screenshots:** `mockups/screenshots/{A,B,C}-{1440,768,390}.png`, plus `B-1440-instrument.png`, which shows variant B's instrument picker in use.

---

## How the directions were found

1. **Inventory.** The things that belong to this Academy and no competitor:
   - آرامش means *calm*, and it's also the director's family name.
   - مسعود آرامش is a santur player and composer with 40+ years in music.
   - The santur itself: a trapezoid body, rows of string bridges, and the photo of a dozen santurs lined up against the wall.
   - The termeh cloth under the teaching santur (photo s2).
   - The tar and setar on the chairs.
   - The week: open Saturday to Thursday, Friday closed, and on Monday four teachers are in.
   - The address: No. 142, second floor, Ashrafi Esfahani.
   - Student concerts.
   - The academy's teal Nastaliq wordmark.
2. **The rut to avoid.** Music-school sites ship a stock photo of a child at a piano, cream and serif, and a clip-art note. Persian-heritage sites ship turquoise girih tiles, an Isfahan dome blue and a calligraphy hero. Both are excluded.
3. **Seven candidates from the Visitor's own world,** ordered by resonance:
   1. a 1970s Iranian modernist concert poster (the Momayez and Shiva lineage)
   2. the santur's field of bridges
   3. the Golha radio programme sheet
   4. printed radif notation
   5. a Tehran courtyard at dusk
   6. the front-desk timetable
   7. Persian miniature painting
4. **Two engines, one hand.**
   - impeccable's `concept-seed` (seed reference `seed:63420297e6d395aa`) **assigned candidate 3**, the programme sheet, and dealt six catalog challengers.
   - taste-skill's `draw` (sector *education*, tone *warm*) dealt two compositions that match: **page-is-the-object** (seed 1825784119) for the programme, and **one-motif** (seed 1641450272) for the poster.
   - I swapped the sheets' Latin faces (Bricolage Grotesque, Hanken Grotesk) for Persian faces, and their dealt colors for colors taken from the subject. Both are recorded below.

The skills' rules disagree in a few places, which are listed in §6.

---

## Direction A: The programme (برنامه) · *assigned by the roll; recommended*

**Concept:** the site is the Academy's printed programme. It's a sheet that lists who is playing this week, and when.

**References:**
- *Golha* (گلها) radio programme listings and 1960s–70s Tehran concert programmes, set as plain columns of time, performer and instrument.
- weeksync.app and sarahandmatt.wedding, from taste-skill's studied sites: pages built as one printed object.
- impeccable's QUALITY BAR boards for the world it was raised by (see the declined challengers).

**First viewport** (`A-1440.png`):
- A deep green-black ground.
- A tall cool-paper sheet on the start (right) side, running off the bottom with a punched tear-off edge.
- On the sheet: the `h1`, the one-sentence promise, and **«امروز در آموزشگاه»**, which is today's real programme. All seven days sit in a row, today is struck forward, and Friday stays visible, marked تعطیل.
- The call button, as a real `tel:` link, sits at the foot of the sheet.
- On the far side, the black-and-white portrait of مسعود آرامش at the santur, as a tipped-in plate with a caption.

**The live thing:** tap any day to see which teachers are in, with times and instruments. That answers a parent's real question, "when can I bring my child, and who's there?", and it's built only from real ClassSession data.

**Type:** **Markazi Text** (Borna Izadpanah, OFL), a Persian Naskh with real stroke contrast, used for both display (700) and text (400/600). One family, as a programme would be set. Latin digits come from its own Latin, set tabular in the schedule.
> «موسیقی را بیاموز، آرامش را احساس کن. سنتور، تار، سه‌تار، تنبک، دف و آواز ایرانی.» — 12:00 – 21:00

**Palette** (four colors; contrast measured):

| Role | Color | Notes |
|---|---|---|
| Ground | `#12201b` green-black | |
| Paper | `#e9ece5` cool paper, not cream | ink on paper 14.1:1 |
| Ink | `#12201b` | secondary ink `#45524c` is 6.9:1 |
| Accent | `#0e7a64` jade | taken from the Academy's own teal wordmark; white on jade is 5.3:1; used for the call action and focus rings only |

**Imagery treatment:** every upload goes through one darkroom process. Portraits and space photos are shown in monochrome on paper, so phone snapshots with mixed white balance look like one commissioned set. Ratios follow the pipeline: portraits 1:1, covers 3:2, gallery photos at their own ratio. A missing or broken image falls back to a paper plate with the person's initials in Markazi.

**Motion character:** printed paper, handled.
- The struck-day block slides between days, transform only, about 220ms ease-out, interruptible.
- Programme rows swap with a 140ms fade.
- Teacher names use *index with preview*: hovering or focusing a name shows the portrait.
- Photos "develop" once as they enter, with opacity from the paper tone.
- No AOS-style fade-up anywhere, and nothing stays hidden without JavaScript.

**Home page structure:**
1. **Programme sheet:** hero, today, the call action.
2. **The performers:** `featured_teachers` as programme entries (name, instruments, link), with portrait preview.
3. **The rooms:** `gallery_preview_images` as tipped-in plates at their own ratios.
4. **Letters from parents:** `testimonials`. Hidden when there are none (today's reality), one long letter for a single quote, a run of letters for several.
5. **The back of the programme:** address, every phone as `tel:`, hours, the Google map with a Neshan link, Instagram and Telegram.

**Raises,** each named for the declined challenger it came from (impeccable's rule):
- **From the cathode numeral stack:** all seven days are always present, the chosen one struck forward, and Friday stays readable as "closed" instead of being hidden.
- **From the transit diagram:** the schedule page is a disciplined diagram, one line per teacher with days as stations. On a phone it focuses one day or one teacher, and never shrinks the whole week into a miniature.
- **From the Crouwel grid specimen:** one measured column grid (time, name, instruments) that every section obeys.
- **From the darkroom safelight bay:** one controlled process for every image (the monochrome treatment above).
- **From the cyclorama:** colors change by whole chapters. Paper sheets on the dark ground, never accents scattered on a neutral page.
- **From the curved-crease shell:** no added support. Nothing is boxed or outlined; structure comes from the grid and the paper's edge alone.

**Honest risk:**
- Dark pages read as *evening*, and some parents expect a bright, cheerful school site.
- Markazi's text sizes have to run larger (20px body) to match a sans's apparent size.
- The "today" block needs one small, additive context key on the home view (proposal P1). Without it, the hero falls back to the opening hours and a link to the schedule.

---

## Direction B: Santur poster (سنتور) · *impeccable's pick*

**Concept:** an Iranian modernist concert poster, where the santur's trapezoid is the one shape the whole site is built from.

**References:**
- Morteza Momayez's and Ghobad Shiva's concert and festival posters: flat color fields, monumental Persian lettering.
- **Lalezar**, the typeface itself, named after Tehran's historic theatre and cinema street, Lalezar Street, and drawn from its painted poster lettering.
- askmidnight.com and superlocaldesign.com, from taste-skill's studied sites: one motif running the whole system.

**First viewport** (`B-1440.png`):
- A cool off-white ground.
- A giant saffron trapezoid cropped by the left edge of the viewport, with the photo of a dozen santurs lined up against the wall printed into it as a saffron-and-black duotone.
- The `h1` in Lalezar on two lines.
- The call button cut to the trapezoid's slant.
- Below, a black band with every instrument the Academy teaches set large: «چه سازی؟». Pick one and see who teaches it, and on which days.

**Type:** **Lalezar** for display (one weight, poster-loud), with **Estedad** (Amin Abedi, OFL, variable 100–900) for text. Both are Persian-first.
> «آموزشگاه موسیقی آرامش» in Lalezar, over «موسیقی را بیاموز، آرامش را احساس کن.» in Estedad.

**Palette:**

| Role | Color | Notes |
|---|---|---|
| Ground | `#f3f4f1` | |
| Ink | `#161616` | 16.4:1 |
| Saffron | `#f2b705` | ink on saffron 9.9:1 |
| Soft ink | `#3d3d3a` | |

**Imagery treatment:** photos sit inside the trapezoid as duotones (grayscale, multiplied on saffron). The shape is also the mask for portraits, the button and the list marks.

**Motion character:** a shutter. The trapezoid wipes open over a photo with a `clip-path` transition, and words light up in saffron on hover or press.

**Home page structure:**
1. The poster hero.
2. «چه سازی؟», the instrument wall (the live thing).
3. Teachers in trapezoid masks.
4. The rooms as a strip of duotone shapes.
5. Testimonials as one large quote.
6. The footer as the wordmark built large on saffron.

**Honest risk:**
- It's the loudest option. Saffron and black poster energy argues with «آرامش» (calm) and with the warm-and-respectful voice.
- One motif repeated on every page can tip into gimmick.
- It's the direction most often reached for when "Persian heritage" is the brief.

---

## Direction C: The category standard · *the standing exit, played straight*

A conventional, well-made music-school site:
- Split hero, with the text on the right and a large rounded photo of a classroom on the left.
- Vazirmatn throughout, the incumbent teal for actions, pill buttons.
- A light wash band of facts: 11 teachers, the days, the address.
- Then teacher cards, testimonials and a contact band.

It's familiar, safe and quick to build. I don't recommend it, because it's the page every academy in Tehran could have, and the 10K checklist's first item ("point of view, not a template") rules it out. It's here so the familiar path stays a real choice.

---

## Challengers the roll dealt, and their verdicts

Each challenger was judged against A on two axes: whether a Tehrani parent recognises themselves in it, and how clearly it presents the Academy. None beat A, so all six are demoted. Each still lent A one discipline (the raises above).

| Challenger | Verdict | What A kept from it |
|---|---|---|
| Curved-crease paper shell | declined | no added support or boxes |
| Theatre cyclorama, dusk to day | declined | whole-chapter color fields |
| Crouwel gridded type specimen | declined | one measured column grid |
| Midnight transit diagram | declined (the closest; clear for the schedule, foreign for the rest) | the schedule as a disciplined diagram |
| Darkroom safelight bay | declined | one controlled image process |
| Cathode numeral stack | declined | every option present, the chosen one struck forward |

---

## 1. Recommendation: A, the programme

- **It's built from something only this Academy has: its actual week.** The first thing a parent sees is a real, useful answer: who is teaching today, when, and on what instrument, with the call button right under it. It passes the competitor test: another academy's programme would carry other teachers and other days.
- **It fits the name and the voice.** Paper, one Naskh face, one jade action. Calm, personal and warm, never shouting.
- **Heritage is lived in, not decorated** (PRODUCT.md principle 3). The santur appears because مسعود آرامش plays it in the portrait, and the instruments appear in every programme line. There are no ornamental tiles anywhere.
- **It carries the real content well**, including the bad cases: empty bios, broken portraits (paper initials plate), no testimonials (the section disappears cleanly), mixed-quality photos (one darkroom treatment), the empty Friday (shown as closed).
- **It travels to every page:**
  - The schedule is the programme in full.
  - Teacher pages are performer entries.
  - The gallery is the album of plates.
  - The contact form is the tear-off stub.
  - The footer is the back of the programme.

B is the stronger poster but the weaker Academy: it sells *Persian music*, while A sells *this place and these teachers*.

---

## 2. Page and section inventory (for Direction A), mapped to the real data

| Page | Sections | Backend data |
|---|---|---|
| **Every page** | Header: wordmark, 5 links, the 2-level gallery menu (desktop: a disclosure panel; phone: a full-screen menu with nested lists). A phone-only bottom bar with **تماس** (`tel:`) and **مسیر** (directions). The footer as the back of the programme. | `gallery_nav_tree`, `site_phones`, `site_phone_primary`, `site_address`, `site_hours`, `site_email`, `site_instagram`, `site_telegram`, `current_year`, `google_analytics_id` |
| **Home** | The programme sheet (h1, promise, today, call) · director plate · performers · rooms · letters · back of the programme | `page_title`, `page_body`, `page_hero_image` (if uploaded, it replaces the director plate), `featured_teachers`, `gallery_preview_images`, `testimonials`, plus `week_schedule` (proposal P1) |
| **About** | The letter: `page_body` on a paper sheet, signed «آموزشگاه موسیقی آرامش» (no invented first-person text) · the rooms as plates with the lightbox · a call close | `page_title`, `page_body`, `meta_description`, `space_images`, `page_hero_image` |
| **Teacher list** | The performers: one row per teacher with a 1:1 portrait plate, name, instruments, and the days they teach (proposal P2; without it, just the link) · a call close | `teachers` (+ `instruments`) |
| **Teacher detail** | Performer page: portrait plate, h1 name, instruments, biography (empty bio: the page leads with instruments and the week instead), their weekly programme, «برای هماهنگی کلاس با … تماس بگیرید» | `teacher`, `teacher_sessions`, `meta_description` |
| **Schedule** | Desktop: the week diagram, one row per teacher (the rowspan grid the view already builds), instruments listed per teacher, today's column struck, Friday shown closed. Phone: by day (today first, swipe or tap the day row), each teacher with time and instruments. `page_body` below. | `schedule_rows`, `weekdays`, `page_title`, `page_body` (the by-day view is built in the template from `schedule_rows`, with no backend change) |
| **Gallery root** | The album index: top-level categories as programme entries with 3:2 covers (no cover: a paper plate with the title) | `child_pages`, `breadcrumbs` |
| **Gallery page** | Title and `intro_text` · child albums · photos at their own ratios in balanced columns · a native `<dialog>` lightbox with captions, keyboard and swipe · videos as a click-to-load facade (a paper poster with the title and a play control; the YouTube or Aparat iframe is created only on click) · designed empty state | `current_page`, `breadcrumbs`, `child_pages`, `images`, `videos` (`embed_url`, `title`, `caption`, `platform`) |
| **Contact** | Form first on phones · visible labels · errors tied to fields (`aria-describedby`, `aria-invalid`) · the captcha with a "new image" refresh · then phones (`tel:`), address, hours, the Google map (lazy) **plus a Neshan link as backup** | `form` (`full_name`, `email`, `phone`, `subject`, `message`, `captcha`), `site_*` |
| **Contact success** | The tear-off stub: «پیام شما رسید», what happens next, the phone, links back to the schedule and the teachers | none |
| **404** | A programme with a missing page: a short apology, links to home, the schedule and contact. New `templates/404.html` (Django picks it up when `DEBUG=False`; no view change) | none |

**Meta (template-only):**
- `<link rel="canonical">` on every page.
- A page-specific `og:image`: the teacher portrait, the gallery cover, or the page hero.
- A `theme-color` matching the ground.
- One `h1` per page. The logo becomes a link, not an `h1`.

Every model has a place to appear:

| Model | Where it appears |
|---|---|
| `SitePageContent` | home, about, schedule |
| `Teacher` and `Instrument` | home, teachers, schedule, footer |
| `ClassSession` | home (P1), teacher detail, schedule |
| `GalleryPage` | menu, gallery, home and about via `ABOUT_GALLERY_SLUG` |
| `GalleryImage` | gallery, home, about |
| `Video` | gallery |
| `Testimonial` | home |
| `ContactMessage` | contact form |

### Optional backend proposals (not built unless you approve)

| # | Proposal | Why | Size |
|---|---|---|---|
| **P1** | Add a `week_schedule` context key to `HomeView`: active sessions grouped by weekday, each with teacher and instruments. | Powers «امروز در آموزشگاه», the hero's live thing. Without it the hero shows the hours and a schedule link. | Additive context key, about 15 lines, plus a test. No model or URL change. |
| **P2** | Prefetch `class_sessions` in `TeacherListView`. | Lets each teacher row show the days they teach without N+1 queries. | One queryset line, plus a test. |
| **P3** | Change `SITE_HOURS` in `settings.py` to Latin digits («شنبه تا چهارشنبه: 10 تا 21 …»). | Matches the digits decision; today these strings use Persian digits. | Content edit. |
| P4 | *(Nice to have, not needed)* An optional short "role" field on `Teacher` (for example «مدیر آموزشگاه»). | The director plate's caption could say it; until then it shows name and instruments only. | Model field plus a migration. |

**Admin to-dos** (yours, no code):
- Re-upload the two missing portraits (علی شمس, محسن همایونی).
- Re-save the two oversize portraits so they're processed to 600×600.
- Rename the gallery page titled `academy-space` to a Persian title.
- Consider removing the emoji from the home `SitePageContent` body (see §6).
- Upload concert photos and real parent quotes when you have them.

---

## 3. Vendor libraries: stay or go

| Library | Verdict | Replaced by |
|---|---|---|
| Bootstrap 5 CSS and JS (8.3 MB in `vendor/`) | **remove** | own grid and layout primitives |
| Bootstrap Icons | **remove** | about 8 inline SVG icons in one stroke weight (phone, map pin, clock, Instagram, Telegram, play, close, arrow) |
| AOS | **remove** | a small IntersectionObserver entrance, with content visible by default |
| GLightbox | **remove** | a native `<dialog>` lightbox (vanilla, about 2 KB) |
| Swiper, Isotope, imagesLoaded, PureCounter, Waypoints, php-email-form `validate.js` | **remove** (unused today) | none |
| Google Fonts (Vazirmatn) | **remove** | self-hosted woff2, Arabic plus Latin subsets, `font-display: swap`, the display weight preloaded |
| django-simple-captcha | **keep** (backend) | restyled, plus a refresh link |

The CoreBiz `main.css` (4,904 lines) and `main.js` are retired. `templates/corebiz_raw/` stays untouched unless you want it deleted.

## 4. CSS and JS architecture (no build step)

- **`static_dev/assets/css/site.css`:** one file in cascade layers, `@layer reset, tokens, base, layout, components, pages, utilities;`
  - **tokens:** color roles, the type scale (five steps), the space scale, one radius (0: square corners), and motion tokens (durations plus `linear()` spring easings).
  - **layout:** the 12-column grid, outer margins and section rhythm.
  - **components:** sheet, plate, programme list, day switcher, button, form field, menu, dialog, video facade.
  - **pages:** small per-page rules.
  - Logical properties throughout (`inset-inline`, `margin-inline-start`), so RTL is native, not patched. `prefers-reduced-motion` is handled at the token level.
- **`static_dev/assets/js/site.js`:** small vanilla modules, `defer`red, each a no-op when its markup is absent:
  - the menu (disclosure, Escape, focus return)
  - the day switcher
  - the lightbox
  - the video facade
  - the image-error fallback
  - the captcha refresh
- **Fonts:** in `static_dev/assets/fonts/`. **Templates:** a fresh `base.html` plus partials (`header`, `menu`, `footer`, `contact-bar`, `plate`, `programme-row`), with the old partials removed.
- Then `collectstatic` refreshes `public/static/`, with the unused vendor folders gone from both trees.

## 5. Phase 2 plan once you choose

This follows the spec's order: tokens and base → `base.html` and shared parts → home → about → teachers → schedule → gallery → contact and success → 404 → motion pass → cleanup and `simplify`. The Phase 3 Playwright loop runs after each page. **No commits**, as you asked; I'll pause after each phase.

## 6. Where the skills disagree (flagged rather than silently resolved)

1. **Emoji in your CMS text.** taste-skill bans emoji, but the live home body is «✨ موسیقی را بیاموز، آرامش را احساس کن 🎵 🎹». It's your content, so templates will render whatever the admin holds. The mockups drop the emoji, and I recommend removing them in the admin. Your call.
2. **Two typefaces versus one.** The spec asks for a "paired display face and body face". taste-skill prefers one family, and A uses one: Markazi Text for both jobs. If the pair must be two families, A's fallback pairing is Markazi Text for display with Estedad for long body text. B already pairs Lalezar with Estedad.
3. **The tear-off edge.** taste-skill bans thin rules and dotted borders as decoration but allows real paper edges (perforation) on a page built as an object. A uses it once, on the sheet's foot.
4. **Mode rules versus the spec on the primary action.** impeccable wants the working action in the first viewport, and the spec says "never pushy". A puts one call button at the foot of the sheet, below the useful content, not above it.
5. **The decision page.** impeccable normally collects this choice on its own decision page. Because you asked to approve each phase yourself, the choice is presented here and in the question box instead.

---

## Decisions so far (2026-10-26)

- **P1** approved (add `week_schedule` to `HomeView`, with a test). **P2** approved (prefetch sessions in `TeacherListView`, with a test). **P3** done: `SITE_HOURS` now uses Latin digits. **P4** not pursued.
- **Logo:** the teal Nastaliq wordmark and the icons in `public/static/assets/img` are the official logo; other colour versions exist. For the mockups, a transparent cutout was extracted from `home_pic.webp` (`mockups/img/logo-{paper,ink,jade}.png`). For production, a vector or transparent original is preferred; the user may be able to get one.
- **No emoji** anywhere in templates. The live home body text in the admin still contains emoji; removing them there is recommended.
- `SITE_ADDRESS` keeps its Persian digits («۱۴۲»), by the user's decision. Only the hours use Latin digits.
- Full-page mockups of A and B (home and schedule, desktop and phone) are in `mockups/full-A.html` and `mockups/full-B.html`, with screenshots in `mockups/screenshots/full/`. **Chosen: Direction A, the programme**, with one change from B: the home teachers section («اساتید آموزشگاه») shows three portraits, one large with its biography and two smaller beside it (rows with thumbnails on the phone), in place of the list with a single preview. The director stays in the hero plate, so the section shows the next three featured teachers. `mockups/full-A.html` is updated to match.
- **Typeface (Phase 2, step 1):** the user replaced Markazi Text with **Amiri** (Khaled Hosny, OFL), still one family for display and text. Amiri ships only 400 and 700, so hierarchy uses those two weights (no 600). Its smaller x-height means body text runs at 21px and headings at 1.2 leading. The self-hosted Persian files are subset to the Persian alphabet and punctuation (43 KB each).
