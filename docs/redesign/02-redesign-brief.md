# Redesign brief, pass 2: Aramesh Music Academy

**Status:** agreed with the owner through a grill-with-docs interview (2026-10-26). Nothing here is built yet.

**What this replaces:** the "printed programme" direction in [01-direction.md](01-direction.md), and the design system in `DESIGN.md` that came from it. Both stay as history. The first pass was built from them, and the owner judged the result not premium enough.

**How to use this file:** open a new Claude Code session in this project and say:

> Read `docs/redesign/02-redesign-brief.md` and carry it out, phase by phase. Stop at every **owner gate**.

The work spans several chats. **Keep the progress log below up to date:** after every numbered step, tick it, note the commit, and record anything the next chat must know. A new chat starts from the first unticked step.

## Progress log

| Step | Status | Commit | Notes for the next chat |
|---|---|---|---|
| Prep: real seed data, saffron logo and icons, references, ADR-0002, this brief | done | `6ffe226`, `89f8e18` | |
| 1. `/impeccable init` | done | `4ab8eb2` | PRODUCT.md refreshed from this brief (Programmes, every lesson private, Persian digits, absent content, saffron assets). DESIGN.md is left for step 3, where shape/new-work replaces the world. No image generation here, so the build path is code-first (not stored). Flag for Gate 1: `SITE_HOURS` says Thursday 10–14, but Masoud Aramesh's Thursday ensemble session is 10–19. |
| 2. `/design-taste-frontend` bar | done | `4ab8eb2` | Read `tells.md` and `critique.md`. The bar, and where the owner-pinned Ethos devices knowingly override the skill's house rules (eyebrows, floating pill nav, large-radius panels, age chips, marquee), is recorded in `03-direction.md` § Anti-slop bar. Use its critique format (§4) and caps in every later look round. |
| 3. `/impeccable shape` → `03-direction.md` | done (awaiting Gate 1) | `4ab8eb2` | Direction pinned by this brief (Ethos-led); concept-seed `seed:53b75618a6a3d972` assigned grounded candidate 5 (the radif's teacher-to-student path), which became the idea «سینه به سینه». All six challengers declined, each lending one named discipline (§7). Live thing: «امروز در آموزشگاه» from real ClassSessions in Tehran time. Direction contract is drafted in §8; write it to the surface brief (`impeccable surface-brief write`) only after Gate 1. Telemetry ping not sent yet (send `--kind assigned` after approval). |
| 4. `/impeccable critique` baseline | done | `4ab8eb2` | Dual-agent run. 19/36 (heuristic 7 n/a), 1 P0, 3 P1. Report: `critique-baseline-pass1.md`; screenshots: `screenshots/pass1-baseline/`; snapshot in `.impeccable/critique/`. In-browser detector clean; the 21 CLI findings are false positives (`{% static %}` unresolved). The P0 (four phone numbers, phone optional on the form) is added to the Gate 1 questions. |
| **Gate 1** | approved 2026-10-26 | `4ab8eb2` | Owner said yes to all four [beyond brief] items. Answers are recorded in `gate-1-models-and-copy.md` Part 4: don't touch Thursday `SITE_HOURS`; `021 4445 7748` and the mobile `+98 990 233 8431` are both primary (the landline on the navbar pill); age chips and FAQ are left blank for the owner to fill in the admin; internal student concerts and call-backs are confirmed. Questions for the Academy: `academy-questions-fa.md` (none blocks the build). Next: step 5. |
| **Phase A** (steps 1–4 and Gate 1) | **complete** | `4ab8eb2` | Everything for Phase A is in `PRODUCT.md`, `03-direction.md`, `gate-1-models-and-copy.md`, `critique-baseline-pass1.md`, `academy-questions-fa.md` and `screenshots/pass1-baseline/`. Committed. The next chat starts at Phase B, step 5. |
| 5. `/emil-prototype` buttons | done | `1c151e3` | Picker: `mockups/prototype-buttons.html` (serve the repo root, e.g. `python3 -m http.server 8766 --directory .`, then open `/docs/redesign/mockups/prototype-buttons.html`; keys 1–4, ← →). Four variants: **Plain** (flat fills, colour carries state), **Disc** (Ethos icon-in-a-disc that travels on hover), **Strike** (key on a solid ledge that sinks on press, santur-hammer feel; bends the no-shadow rule), **Fact** (the button carries its fact: the phone number, «۴ دوره»). Each shows primary/secondary/quiet on ground and stone, a state strip (rest, hover, press, focus, disabled) and a live submit (sending → sent). Focus ring is saffron on ground and ink on stone (saffron on stone fails 3:1). Verified with Playwright (scripted, headless Chrome; the Playwright MCP browser was locked by another instance) at 1440/768/390: no console errors or 404s, no horizontal overflow, keyboard reaches the hero call first, reduced motion zeroes transitions. Screenshots: `screenshots/step5-buttons/`. The age chip was left out (owner leaves ages blank). |
| 6. `/emil-prototype` hero | done | `9d525b9` | Picker: `mockups/prototype-hero.html` (same server). The four seed `home-hero` photos are copied to `mockups/img/hero-1…4.jpg` with their titles. Four variants: **Frame** (03-direction §4 as written: copy on the photo at the start, today strip and bars in the far corner, plain 1.2s crossfade), **Split** (copy on the ground, photo in its own frame with a slow scale settle while shown; no text over the dim photos), **Index** (the four photo titles are a visible, clickable index with a saffron progress line), **Curtain** (one caption row, pills at the far end, slides drawn across right-to-left with clip-path). All: slide clock is the progress bar's CSS animation, so hover, focus, off-screen (IntersectionObserver) and hidden tab pause it; reduced motion shows the first photo still with no bars; «امروز در آموزشگاه» is computed live from the real sessions in Tehran time (after hours it reads «کلاس‌های امروز تمام شده. فردا از ساعت ۱۲.»). Verified with scripted Playwright at 1440/768/390: no console errors or 404s, no overflow, auto-advance after one slide, hover and focus pause, reduced motion holds slide 1. Screenshots: `screenshots/step6-hero/` (including `-mid` mid-transition frames). Known: `hero-1.jpg` is 1111px wide, so the full-width variants upscale it at 1440 (Split does not); Split's pills fall just below the fold at 390×844. |
| **Gate 2** | approved 2026-10-26 | | Owner picked **Disc** for buttons and **Frame** for the hero. Disc: label first, the icon in a 40px disc at the end (36px at the small size); primary = saffron pill with a ground disc and saffron icon; secondary = stone pill (on ground) or ink-tint pill (on stone) with a dark disc; on hover the arrow slides out leftwards and its twin slides in (260ms, strong ease-out), the phone icon tilts −14°; press scales to 0.97; quiet = text with a 2px saffron underline (`#9a6c12` on stone) and a bare arrow that nudges 4px; a button with no icon (the phone «منو») gets no disc. Frame: as 03-direction §4: full-height framed photo, copy at the start over a side + bottom scrim, slide title above the h1, progress bars and the today strip in the far bottom corner (top corner on phones, and the strip moves under the hero), plain 1.2s crossfade every 6.5s, the bar's CSS animation is the clock. The neutral stand-in buttons in `prototype-hero.html` are Plain; build the hero with Disc. **Keep both prototype files and `mockups/img/hero-*.jpg` as the reference** until steps 9 (buttons) and 11 (home hero) have built them; delete them at step 14. |
| **Phase B** (steps 5–6 and Gate 2) | **complete** | | The next chat starts at Phase C, step 7. |
| 7. Models, migrations, admin, seed, tests | done | `61d2198` | As `gate-1-models-and-copy.md` Parts 1–2, plus: new app `apps.programmes`; `Teacher.lineage`; contact phone required, email optional (`contact/0004`); `HERO_GALLERY_SLUG` with `GalleryPage.objects.listed()` hiding `home-hero` from menu, index and sitemap. The display rule is `ClassSession.offerings()` (an `Offerings` with `instruments`, `programmes`, and a `__str__` like «پیانو، گیتار پاپ · تئوری و سلفژ»); the schedule, week partial and teacher page already use it. **Deviation:** Nasim Haghi's Saturday session gets بلز and فلوت as its Instruments (children-only, so the schedule still reads «موسیقی کودک»), because the admin form needs Instruments or a reserved Programme. The data migration does nothing on an empty database. `Instrument.save()` fills a missing slug (name, or `instrument-<pk>` for Persian) for code paths; the admin still asks for one. Seed: `academy.json` gains `instruments`, `programmes`, per-teacher `programmes`/`lineage`, session `programme`, and `sections` (the approved «شیوهٔ آموزش» and «سه قدم» copy, also seeded as `SitePageContent`). **Production:** after deploy, `migrate` moves the data; the `teaching` and `first_lesson` rows and FAQ entries must be added in the admin (report item). No age labels or FAQ seeded (Gate 1). Tests: 92 pass, including the data migration forwards and back on seed-shaped data. Dev DB migrated and reseeded; a copy from before is not kept in the repo. |
| 8. Tokens and base (`/impeccable typeset`, `/impeccable colorize`, `apple-design`) | done | see `git log` («step 8») | **Fonts:** Sahel v3.4.0 downloaded with the owner's yes (2026-10-26), the **Farsi-Digits** build, subset with fontTools to `static_dev/assets/fonts/sahel-fd-{400,700}.woff2` (~24 KB each) plus `Sahel-OFL.txt`. FD means every number in Sahel shows Persian digits while the HTML keeps ASCII (tel: links work). Amiri is now 700 only (display); its 400 files are deleted. Amiri draws Latin digits, so numbers in display type use the new `fa_digits` filter (`site_tags`). `base.html` preloads Sahel 400 + Amiri fa 700. **Tokens** (`site.css` `tokens` layer, rewritten): `--ground #17130f`, `--ground-2 #24201b`, `--stone #ebe5dc`, `--stone-soft #aba69e` (7.6:1 on ground), `--ink-soft #57524d` (6.2:1 on stone), `--field #f7f4ef`, `--field-line #8c8780` (3.3:1), `--saffron #e2a72e` (ink on it 8.6:1), `--saffron-deep #9a6c12` (marks on stone, 3.7:1; saffron itself is 1.7:1 on stone, never text there), `--error #a8321f` (5.3:1). Surface roles `--surface/--text/--text-soft/--mark/--focus`; `.on-stone` (and legacy `.sheet`) flips them, with an **ink** focus ring on stone. Type: Sahel `--text-xs/s/m/l` (14/16/18–20/20–24), Amiri `--display-s/m/l` (26–36/32–52/44–76); leading 1.25 display, 1.4 UI, 1.85 body on ground, 1.8 on stone; tracking 0 everywhere (it breaks Persian joins; `apple-design` §15's negative display tracking is knowingly not applied). Two radii: `--radius-panel` 20→28px, `--radius-pill`. `--frame` (12–24px ground around panels), `--panel-pad`, `--dur-fade` 1.2s. **Legacy bridge:** a marked block maps pass-1 names (`--paper`, `--accent`, `--font`, `--text-xl`…) to the new tokens so the old component/page CSS still renders; steps 9–11 replace those rules and **step 14 deletes the bridge**. Verified with the Playwright MCP at 1440/768/390 on 10 pages: Sahel and Amiri load, body computes to Sahel 20px/37px at 1440, no overflow, no asset 404s, no console errors (the DEBUG 404 page aside). Screenshots: `screenshots/step8-tokens/`. Detector (`--scope type`): only `design-system-font(-size)` against the pass-1 DESIGN.md, expected until step 22 rewrites it. |

---

## 0. Ground rules

- Work only on the `re-design-ui` branch. Check with `git branch --show-current` before every commit. Never touch `main`, and don't push.
- Read first: `CLAUDE.md`, `CONTEXT.md` (the domain vocabulary; use its terms and avoid the ones it lists), `docs/adr/0001-…` and `docs/adr/0002-programme-separate-from-instrument.md`, `docs/redesign/references/README.md` and its screenshots, and this brief.
- **Purpose:** an informational site whose one goal is **Conversion**: the Visitor contacts the Academy by phone, form or visit. The audience is mainly parents, then adult learners. Enrollment, payment, accounts and prices are out of scope.
- **Every lesson at the Academy is private.** Never present "private" as an option the Visitor chooses.
- **Static workflow:** edit in `static_dev/` (gitignored, dev only), run `python manage.py collectstatic --noinput`, and commit `public/static/`.
- **Run locally:** `source .venv/bin/activate && DEBUG=True python manage.py runserver`. `python manage.py seed_sample_data` loads the real academy content from `apps/core/management/commands/seed_data/`.
- **Copy:** Claude drafts all new Persian text using only facts from the live site, the teacher bios and `seed_data/academy.json`. No invented numbers, awards or quotes. The owner approves the copy at a gate.
- **Model changes:** keep them to what this brief lists. Propose anything beyond it at a gate.

## 1. Decisions (from the interview)

### Look

| # | Decision |
|---|---|
| Direction | **Ethos-led** (see `references/ethos/`). Large-radius framed panels inset on a dark ground; **pill buttons**; a floating rounded navbar with a pill call button at its end; full-bleed photography inside rounded frames; small uppercase-style eyebrows above big headlines. Use `/impeccable shape` to make it the Academy's own (Persian musical heritage, سنتور, warmth), not a copy. |
| Ground | A **dark frame** (warm near-black), alternating with **warm light panels** for reading-heavy sections: about, teaching approach, FAQ, contact form. |
| Accent | **Saffron gold**, the only accent: main call buttons, active states, highlights, focus. The colour sample is `#e2a72e` with dark text on it; tune it in `/impeccable colorize` but keep it saffron. |
| Logo and icons | Already recoloured to saffron, in `static_dev/assets/img/` and `public/static/assets/img/`: `logo-saffron.png` (938px), `logo-saffron.webp` (400px), `icon-notes-saffron.png`, plus the favicons, touch and Android icons, `og-image.jpg` and the manifest. Use them; retire `logo-paper` and `logo-ink`, or regenerate them from the saffron master if a mono version is needed. |
| Type | **Amiri** for display headlines only; **Sahel** (SIL OFL, `rastikerdar/sahel-font` v3.4.0) for everything else: body, nav, buttons, labels, forms. Self-host both as subset woff2 with `font-display: swap`. **Persian digits everywhere**, including phone numbers and times. |
| Colours | Three to five tokens in total: ground, light panel, ink, saffron, plus an error red. |

Mockups of the agreed look, made with the real photos: `mockups/accent-compare.png` (the left variant, B, is the chosen one) and `mockups/logo-compare.png`.

### Content model (see ADR-0002)

| # | Decision |
|---|---|
| Programme (دوره) | A new admin-editable model with these fields: name, slug, **kind** (`with_teacher` or `fixed_time`), short description (for cards), long description (for its page), **age label** (chip text, e.g. «از ۷ سال»), **up to 3 photos** that crossfade in its card, display order, and is_active. |
| The Programmes | **کلاس خصوصی** (with the teacher), **گروه نوازی** (fixed time: Thursdays, an optional group activity some students join), **موسیقی کودک** (with the teacher: basic note reading, plus children's instruments such as بلز and فلوت), and **تئوری و سلفژ** (with the teacher). Master classes are added later, as a fifth, when there's a real one. |
| Teacher → Programme | An M2M field for the Programmes the Teacher offers "with the teacher" (for example, Masoud Aramesh and Ali Shams: تئوری و سلفژ; Nasim Haghi: موسیقی کودک). کلاس خصوصی is never tagged; it's implied. |
| ClassSession → Programme | A nullable reference, set only on a session **reserved** for a fixed-time Programme. Masoud Aramesh's Thursday 10–19 is reserved for گروه نوازی: nothing else is taught in that slot, and the schedule shows only گروه نوازی for it. |
| Schedule display | Each ClassSession shows its Instruments, plus the teacher's "with the teacher" Programmes. For example, Ali Shams's Wednesday reads: پیانو، گیتار … · تئوری و سلفژ. A reserved session shows only its Programme. |
| Instrument | New fields: slug, short overview, photo (optional), display order, and **children_only**. Children-only Instruments (بلز, فلوت) appear only on the موسیقی کودک page and the teacher's profile, never in the main grid. Instruments without a photo get a **designed typographic tile**: the name in large Amiri on a warm panel with a subtle saffron shape. |
| Data migration | Move تئوری و سلفژ, گروه نوازی and موسیقی کودک out of Instrument and into Programme, on Teachers and on the Thursday ClassSession. Add بلز and فلوت as children-only Instruments for Nasim Haghi. Then delete the three fake Instrument rows. Update `seed_data/academy.json` and `seed_sample_data` to match. |
| FAQ | A small new admin-editable FAQ model (question, answer, order, is_active). Shown as a short block on the home page and on Programme pages; the section hides when empty. Claude drafts the first entries for owner approval: best age to start, whether an instrument is needed at home, how a first session works, what ensemble playing is. |
| "How we teach" and "Three steps to your first lesson" | Admin-editable. Propose the smallest model change for this at Gate 1 (new `SitePageContent` keys or fields), then draft the copy. |
| Hero | Crossfades the photos of the gallery page with slug **`home-hero`** (a new setting, `HERO_GALLERY_SLUG`; it's already in the seed with 4 photos). Each slide's small text is that photo's **title**. `home-hero` must be **hidden from the gallery menu and the gallery index**. 4–6 slides, a slow crossfade, paused on hover and focus, and a still image for reduced motion. |
| Gallery | Top level: **کنسرت‌ها** (one child page per concert), **گروه نوازی**, **کلاس‌ها و فضای آموزشگاه** (`academy-space`, still `ABOUT_GALLERY_SLUG`), **ویدیوها**, plus the hidden `home-hero`. This is already in the seed. Empty pages must look intentional until the owner uploads photos of students playing solo, in ensembles and at concerts. |
| Testimonials | Show up to 8 in a slow sideways marquee (Bettr). It pauses on hover and focus, falls back to a static row for reduced motion, and the section hides when there are none. There are none today, so **never invent any**. |

### Pages and navigation

- **Navbar:** درباره ما · دوره‌ها · اساتید · برنامه کلاس‌ها · گالری, plus a saffron pill «تماس ۰۲۱ …» (the real `site_phone_primary`, in Persian digits). The **دوره‌ها** menu lists the 4 Programmes and «همه سازها». On mobile: a full-screen menu, with the call button always reachable.
- **Home, in this order** (each section hides itself when it has no content):
  1. rotating hero,
  2. an about panel with a photo beside it (Ethos "chi siamo"),
  3. Programme cards with crossfading photos and age chips (Ethos courses),
  4. the instrument grid (RAM departments tiles),
  5. the director and teachers,
  6. how we teach, plus three steps to your first lesson,
  7. testimonials marquee,
  8. gallery preview,
  9. a short FAQ,
  10. a contact band.
- **A page per Programme** (new): long description, who it's for (age), its Instruments (for کلاس خصوصی, the full grid; for موسیقی کودک, the children-only ones), teachers, class times, relevant FAQ, and a contact call to action at the end.
- **A page per Instrument** (new): overview, photo or typographic tile, who teaches it, when (the sessions), and a contact call to action.
- **Existing pages, redesigned in the new system:** about, teacher list and detail (Instruments and Programmes listed separately), schedule (the rules above; desktop grid plus a mobile view designed separately), gallery, contact and contact success, 404.

## 2. Acceptance criteria: the $10K checklist

The finished site must pass all eight. Each one becomes a section of the final report, with evidence.

1. **Point of view, not a template.** One specific design direction, executed without flinching. It must fit a music school (craft, rehearsal, sound, Persian musical heritage, the instruments taught) and must not be generic "modern".
2. **Typography that does work.** A paired display face and body face (Amiri + Sahel), neither of them Inter or Roboto. Check how they render Persian. Self-host the fonts (woff2, subset, `font-display: swap`). Scale and weight carry the hierarchy, and headlines feel chosen.
3. **A restrained colour system.** Three to five colours, defined as tokens and used consistently. Premium comes from restraint, not decoration.
4. **Hierarchy that breathes.** Whitespace, scale and contrast give every page a clear primary, secondary and tertiary level. No flat walls of content.
5. **Imagery with intent.** Almost all images are admin uploads of unpredictable quality, processed on save by `core.image_utils.process_image`:
   - teacher portraits: 600×600 (1:1),
   - gallery covers: 900×600 (3:2),
   - page hero images: 1200×800 (3:2),
   - gallery images: fitted within 1920×1920, aspect ratio kept.

   Design for those real ratios. Hero images max out at about 1200px wide, so a full-bleed hero needs a treatment that holds up (rounded frame, darkening, grain). Give images consistent framing, a unified tone and designed fallbacks. No stock-photo defaults.
6. **Motion that whispers.** Hand-crafted micro-interactions and scroll behaviour, not fade-up everywhere. A designer shouldn't roll their eyes at any of it.
7. **Mobile that's designed, not shrunk.** The phone layouts are their own decisions (navigation, schedule, gallery browsing, Programme cards, contact form).
8. **The invisible expensive stuff.**
   - Under 2s LCP, WCAG AA contrast, full keyboard navigation with visible focus.
   - Semantic landmarks, real meta tags (title, description, Open Graph, canonical) and a correct `lang`/`dir`.
   - Accessible forms with captcha, and no console errors.

## 3. Known problems the first pass had (must not come back)

1. One book face for everything: fixed by Amiri + Sahel.
2. Buttons with no design: build a real **button system**.
   - Variants: primary (saffron pill), secondary (light pill), quiet (text with an underline accent).
   - Height 48–52px, an icon slot, and hover, press, focus and disabled states.
   - Persian digits.
3. Grey placeholders: fixed, since the seed now has the real photos. Judge designs only with real data.
4. A heavy concept with no visual anchor: fixed by the Ethos direction and the rotating hero.
5. **Content hidden until an animation fires** (the teachers and schedule pages loaded empty): content must be **visible by default**. Motion may only enhance something already shown, never gate it.

## 4. Phases, skills and owner gates

Invoke each skill with the Skill tool and follow it. Several Emil Kowalski skills assume React and Framer Motion: translate their advice into plain CSS (transitions, `@keyframes`, `linear()` springs) and vanilla JS (WAAPI, View Transitions).

### Phase A: context and direction
1. `/impeccable init`: refresh the product and design context from this brief. `PRODUCT.md` and `DESIGN.md` will be rewritten.
2. `/design-taste-frontend`: read its `references/tells.md` and `critique.md`. Use them as the anti-slop bar for the whole job.
3. `/impeccable shape`, with `references/` as input: shape the Ethos-led direction into the Academy's own. Write `docs/redesign/03-direction.md`.
4. `/impeccable critique` on the current site, measured against the references, to record a baseline.

**Gate 1:** the owner approves the direction, the proposed models and migrations (section 1), and the drafted Persian copy.

### Phase B: choose by eye
5. `/emil-prototype` on the **button system**: 3–4 genuinely different variants behind the live picker.
6. `/emil-prototype` on the **hero**: 3–4 variants (crossfade style, caption treatment, pill placement).

**Gate 2:** the owner picks a button variant and a hero variant.

### Phase C: build (commit after each step)
7. Models, migrations (including the data migration), admin and seed updates; tests for the schedule display rules.
8. Tokens and base: `/impeccable typeset` (Amiri + Sahel scale, Persian digits) and `/impeccable colorize` (the saffron system). Use `apple-design` for tracking, leading and optical size.
9. Components: buttons (the chosen variant), cards, chips, tiles, navbar, menu, accordion, marquee and forms, with `/emil-design-eng` and `apple-design` for press feedback and feel.
10. `base.html`, the header and mobile menu, and the footer.
11. Pages, one at a time: home → Programme pages → Instrument pages → teachers → schedule → about → gallery → contact → 404. Use `/impeccable layout` for each page. Use `/impeccable bolder` only if a page lacks a visual anchor.
12. Motion pass:
    - `/find-animation-opportunities` across the finished pages,
    - build what it approves with `/animate`, to the `apple-design` standard: cross-document View Transitions between pages (Aspire), the hero and Programme-card crossfades (Ethos), the testimonial marquee (Bettr), and button press feedback,
    - everything respects `prefers-reduced-motion`.
13. `/mobile-native`: the phone pass (tap highlights, `100dvh`, input zoom, safe areas, sticky hover).
14. Remove the dead CSS, JS, templates and old logos; then run `/simplify`.

### Phase D: verify (after every page, and again at the end)
15. Playwright MCP at **1440×900, 768×1024 and 390×844**:
    - screenshots, looked at critically and fixed until right,
    - zero console errors, no 404s,
    - keyboard pass (RTL focus order, visible focus, Escape closes overlays),
    - reduced motion via `browser_emulate_media`,
    - nothing is invisible on first paint.
16. `/design-taste-frontend` inspector, with its look-and-fix loop.
17. `/impeccable audit` (accessibility, performance, responsive) and `/impeccable critique` against the references.
18. `/review-animations` and `/animation-performance`; fix what they flag.
19. `/break-ui` with the worst cases:
    - Ali Shams's 6 instruments,
    - a teacher with a bio of `.` and no photo (Ali Shams, Mohsen Homayouni),
    - empty gallery pages,
    - no testimonials, no FAQ,
    - very long Persian names.
20. `python manage.py test`, all passing.
21. `/code-review` on the branch.

### Phase E: finish
22. `/impeccable polish`, then `/impeccable document`, which rewrites `DESIGN.md` from the shipped site.
23. Write `docs/redesign/report.md`:
    - each checklist item with before/after screenshots at all three widths,
    - measured LCP and transfer sizes,
    - the known gaps,
    - **what the owner must do in the admin**: upload students' concert, ensemble and solo photos; choose the `home-hero` photos; add Instrument photos and overviews; collect real testimonials; and fix the two teachers with no bio or photo.

## 5. What each reference contributes

| Reference | Folder | Take |
|---|---|---|
| Ethos Music Academy | `references/ethos/` | The overall shape language, pill buttons, floating navbar, rotating framed hero with eyebrow and small text, the "chi siamo" split panel with photo, Programme cards with age chips and crossfading photos. |
| Royal Academy of Music | `references/ram/` | The instrument grid as compact tiles (label, chevron, photo flush to one edge); the calm navbar; describing everything taught on the home page. |
| Aspire Music | `references/aspire/` | Animated movement between pages: cross-document View Transitions. |
| Bettr Academy | `references/bettr/` | Motion quality; the testimonial marquee cards. |
| Treehouse Music Studios | `references/treehouse/` | Introducing each instrument: overview, a "more" accordion, and a contact action per instrument. |
| Lewis Center, Opus 1, Thrive, Notes n Beats | `references/{lewis-center,opus1,thrive,notesnbeats}/` | Content to adapt: why choose us, how we teach, three steps to your first lesson, a parent FAQ, a section per instrument, and students playing solo, in ensembles and at concerts. No prices or booking. |
