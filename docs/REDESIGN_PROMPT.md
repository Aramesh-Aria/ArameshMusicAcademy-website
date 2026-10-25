# Prompt: Aramesh Music Academy — frontend redesign from scratch

Copy everything below the line into a new Claude Code session opened in this project.

---

You are redesigning the public frontend of **Aramesh Music Academy** (آکادمی موسیقی آرامش), a Persian-language music school site built with Django 5.2 server-rendered templates. Design it **from scratch**. Don't restyle the current CoreBiz/Bootstrap theme. The goal is a site that feels like a $10K commission, not a $200 template.

## What the site is for

Read `CLAUDE.md`, `CONTEXT.md` and `docs/adr/` first. They are current. Use the domain vocabulary from `CONTEXT.md` in your documents, and avoid the terms it lists as ones to avoid.

- **Purpose:** an informational site. The single goal of a visit is **Conversion**: the Visitor contacts the Academy by form, phone or an in-person visit. Every page should move the Visitor toward that, with a clear, never pushy path to contact (form, tap-to-call phone, address, hours).
- **Audience:** mainly parents researching lessons for their children; adult learners second. Design for trust, warmth and credibility, not only for spectacle.
- **Out of scope by design:** online enrollment, payment, student accounts and portals. Don't design or propose them.

## Ground rules

- Work only on the `re-design-ui` branch. Check with `git branch --show-current` before every commit. Never touch `main`, and don't push.
- Do not build anything until Phase 1 is approved by me. Phases 0–1 are read-only plus writing documents.
- The backend is the source of truth. Don't change models, migrations, URL names, view context keys or form fields unless you propose the change in Phase 1 and I approve it. Templates must keep working with the real context the views provide.
- Leave the Django admin (Jazzmin) alone.
- Language and direction: the site stays `lang="fa" dir="rtl"`. Every layout decision, icon direction, animation direction and number format must be right for RTL Persian.
- No frontend build pipeline unless I approve one in Phase 1. Plain CSS (custom properties, `@layer`, modern features) and small vanilla JS are preferred. You may drop Bootstrap, AOS, Swiper, Isotope, GLightbox, PureCounter, Waypoints, etc. if the new design doesn't need them. Remove whatever you don't use.
- Static files workflow: edit sources in `static_dev/` (gitignored, dev only). Then run `python manage.py collectstatic --noinput` so `public/static/` is updated, and commit `public/static/`. Production serves `public/static/` via WhiteNoise. Static URL is `/public/static/`, media is `/public/media/`.
- Run locally with `source .venv/bin/activate && DEBUG=True python manage.py runserver`. Use `python manage.py seed_sample_data` if the DB is empty.

## Skills to use

These are installed in `.claude/skills/`. Invoke them with the Skill tool and actually follow them, don't just name them.

1. **`impeccable`**: the backbone of the process.
   - Start with `/impeccable init` to capture product and design context.
   - Use `shape` to form the direction and `craft` / `layout` / `typeset` / `colorize` while building.
   - Use `critique` and `audit` to review, `harden` for edge cases and `polish` to finish.
   - Let it produce `DESIGN.md` documenting the final system.
2. **`design-taste-frontend`** (taste-skill): the art direction.
   - Use its direction library to propose distinct directions grounded in real reference sites.
   - Follow its anti-slop rules (`references/tells.md`).
   - Use its browser inspector and screenshot look-and-fix loop on every page.
3. **`apple-design`** (Emil Kowalski): the motion and interaction standard.
   - Physical, interruptible motion and springs where they fit, used with restraint.
   - Correct typography details (tracking, leading, optical sizes).
   - `prefers-reduced-motion` support, and feedback on every interaction.
4. Supporting skills, each tied to a phase:

   | Skill | Phase | Use it for |
   |---|---|---|
   | `prototype` | 1 | Throwaway hero mockups for each direction, so I can compare them before choosing. |
   | `emil-design-eng` | 2 | Component polish and the small details that make UI feel right. |
   | `find-animation-opportunities` | 2, once a page's layout is done | Decide where motion helps and where it doesn't, with exact values. It's read-only, so act on what it finds with `animate`. |
   | `animate` | 2 | Build each chosen animation: purpose, property, curve, duration, interruption, exit. |
   | `mobile-native` | 2 and 3 | The phone pass: tap highlights, `100vh`, input zoom, safe areas, sticky hover. |
   | `review-animations` | 3 | A strict review of all motion. It only runs when called by name, so call it explicitly. |
   | `animation-performance` | 3 | Keep motion on composite-only properties and inside the frame budget. |
   | `break-ui` | 3 | Push the worst-case content from Phase 0 through each page. |
   | `simplify` | End of Phase 2 | Clean up the new templates, CSS and JS. |
   | `code-review` | Before the final report | Review the branch against `main` for standards and spec. |

   Most of Emil Kowalski's skills assume React and Framer Motion. Translate their advice into plain CSS (transitions, `@keyframes`, `linear()` easing for springs) and vanilla JS (WAAPI). Don't add a framework to follow them.

   Between Phase 1 and Phase 2, I may run `grilling` myself to stress-test the chosen direction. Wait for the outcome before building.

If two skills disagree, the order of authority is: my approved direction → the 10K checklist below → impeccable → taste-skill → apple-design. Tell me about real conflicts instead of silently picking one.

## The $10K checklist (acceptance criteria)

The finished site must pass all eight. Each one becomes a section of the final report, with evidence.

1. **Point of view, not a template.** One specific design direction, executed without flinching. It must fit a music school (craft, rehearsal, sound, Persian musical heritage, the instruments taught) and must not be generic "modern".
2. **Typography that does work.** A paired display face and body face, neither of them Inter or Roboto. Both must have excellent Persian/Arabic-script support; check how they render Persian, not just Latin. Self-host the fonts (woff2, subset, `font-display: swap`). Scale and weight carry the hierarchy, and headlines feel chosen.
3. **A restrained color system.** Three to five colors, defined as tokens and used consistently. Premium comes from restraint, not decoration.
4. **Hierarchy that breathes.** Whitespace, scale and contrast give every page a clear primary, secondary and tertiary level. No flat walls of content.
5. **Imagery with intent.** Almost all images are admin uploads of unpredictable quality.
   - On save they are processed by `core.image_utils.process_image`:
     - teacher portraits are cropped to 600×600 (1:1),
     - gallery covers to 900×600 (3:2),
     - page hero images to 1200×800 (3:2),
     - gallery images are fitted within 1920×1920 with their original aspect ratio kept.
   - Design for those real ratios and sizes. Hero images max out at 1200px wide, so a full-bleed hero needs a treatment that holds up at that resolution.
   - Make the images feel commissioned: consistent framing, unified tone, and good fallbacks for missing images. No stock-photo defaults.
6. **Motion that whispers.** Hand-crafted micro-interactions and scroll behavior, not AOS fade-up everywhere. A designer shouldn't roll their eyes at any of it.
7. **Mobile that's designed, not shrunk.** The phone layouts are their own decisions (navigation, the schedule grid, gallery browsing, the contact form), not the desktop compressed.
8. **The invisible expensive stuff.**
   - Under 2s load (LCP), WCAG AA contrast, full keyboard navigation with visible focus.
   - Semantic HTML landmarks, real meta tags (title, description, Open Graph, canonical) and a correct `lang`/`dir`.
   - Accessible forms with captcha, and no console errors.

## Phase 0: Full inspection (read-only)

Inspect everything, then write `docs/redesign/00-inspection.md`. `CLAUDE.md` is your map, but verify it against the code.

- **Backend:** every app under `apps/`. Cover:
  - models and their fields (what's optional or blank),
  - views and the exact context each passes, URL names,
  - forms (including django-simple-captcha),
  - context processors: `site_info` (email, phones, address, hours, Instagram/Telegram, instruments, GA ID) and `gallery_nav_tree`,
  - sitemaps and `seed_sample_data`.

  Write down every piece of content the frontend can show and where it comes from. Specifics to capture:
  - `SitePageContent` (`home`, `about`, `schedule`) is CMS-editable, with hardcoded fallbacks in the views. Design for both the edited and the fallback content.
  - `ClassSession` is grouped **by Teacher**, and each session lists **several Instruments** (M2M, no Course model; see ADR-0001). The schedule view builds a rowspan grid grouped by teacher.
  - `GalleryPage` is a tree **capped at 2 levels**: top-level categories, then events/albums. `Video` is a YouTube/Aparat embed built from a URL and lives under its own top-level gallery category.
  - The About page can pull a gallery via `ABOUT_GALLERY_SLUG`.
  - `Testimonial` quotes from parents sit on the home page between the teacher preview and the contact call to action, as social proof.
  - The contact view saves `ContactMessage`, then emails. SMTP errors never block the Visitor, so design only for success and validation-error states.
  - Google Analytics is included when `GOOGLE_ANALYTICS_ID` is set.
- **Frontend:** every template in `templates/` (ignore `corebiz_raw/`), `static_dev/assets/css/main.css`, `static_dev/assets/js/main.js` and the vendor libraries in use. Note what each page does today and what's broken, generic or missing.
- **Live site:** run the dev server and use the **Playwright MCP tools** (`mcp__playwright__*`). Screenshot every page at 1440px, 768px and 390px widths, and record console errors and the current problems.
- **Edge cases:** the content extremes the design must survive:
  - long Persian names,
  - a teacher with a very long bio or many instruments,
  - a teacher with many sessions, or a weekday with no sessions,
  - a session covering many instruments,
  - an empty gallery category, or a category with only child pages,
  - a gallery page with only videos,
  - no testimonials, or a single one,
  - `SitePageContent` missing, so the fallbacks show,
  - empty `site_hours` or social links.

## Phase 1: Direction (then stop and wait for me)

Write `docs/redesign/01-direction.md` containing:

- 2–3 **genuinely different** directions from `design-taste-frontend` and `impeccable shape`. For each one: the concept in one line, references, type pairing (with a Persian sample), the palette, the imagery treatment, the motion character and a sketch of the home page structure.
- Your recommendation and why it fits this academy.
- The page and section inventory for the new site, mapped to the real backend data from Phase 0. Make sure every model has a place to appear. List anything the backend doesn't provide that you'd want, as optional proposals, and don't build them.
- Which vendor libraries stay or go, and the CSS/JS architecture.

Use `prototype` to build one static HTML mockup of the home page hero per direction in `docs/redesign/mockups/`, then screenshot them with Playwright.

**Stop here.** Don't write production templates until I choose a direction.

## Phase 2: Build

Build in this order, and commit after each step with a conventional commit message:

1. Design tokens and base: fonts, color, type scale, spacing, radii, motion tokens, plus reset and layout primitives in a fresh stylesheet.
2. `base.html` and the shared parts:
   - header and navigation, including the 2-level gallery menu from `gallery_nav_tree`, designed for both desktop and mobile,
   - an always-reachable contact path (on mobile, consider tap-to-call),
   - the footer, using the `site_info` values: phones, address, hours, social links.
3. Pages, one at a time:
   - home
   - about
   - teacher list and teacher detail
   - schedule: grouped by teacher with each session's instruments listed, as a rowspan grid on desktop and a purpose-built mobile view (for example, by teacher or by day)
   - gallery root and gallery pages, including images, a lightbox, and video embeds using a lightweight click-to-load facade (don't load YouTube/Aparat iframes on page load)
   - contact and contact success, including captcha and form error states
   - a 404 page
4. Motion pass: run `find-animation-opportunities` on the finished pages, build what it approves with `animate` (held to the `apple-design` standard), then apply `emil-design-eng` and `mobile-native` across the site.
5. Remove unused vendor files, old CSS/JS and dead template partials, then run `simplify` on the new code.

After each page, run the Phase 3 loop on that page before moving to the next one.

## Phase 3: Verify with Playwright (on every page, every time)

Use the Playwright MCP tools against the running dev server:

- Screenshot at **1440×900, 768×1024 and 390×844**, then look at the screenshots critically and fix what's off. Repeat until it's right. Also use taste-skill's inspector.
- Check `browser_console_messages` for zero errors and `browser_network_requests` for no 404s, using sensible asset sizes.
- Keyboard: Tab through the whole page and confirm the focus order makes sense in RTL, focus is always visible, menus open and close with the keyboard, and Escape closes overlays.
- Check `prefers-reduced-motion` with `browser_emulate_media`, and check that nothing animates in a way that blocks content.
- Check contrast against WCAG AA, check that a heading hierarchy and landmarks exist, and check that images have alt text.
- Test the worst-case content from Phase 0 with `break-ui`.
- After the motion pass, run `review-animations` and `animation-performance`, and fix what they flag.
- Run `python manage.py test` and keep it passing.
- Before writing the final report, run `code-review` on the branch and fix what it finds.

## Final deliverables

- The redesigned templates and static files, with `public/static/` regenerated, committed on `re-design-ui`.
- `DESIGN.md`, written with `impeccable document`.
- `docs/redesign/report.md`:
  - each checklist item with before/after screenshots at all three widths,
  - Lighthouse-style numbers (or Playwright-measured LCP and transfer size),
  - the known gaps,
  - anything I need to do in the admin, such as uploading better hero images.
