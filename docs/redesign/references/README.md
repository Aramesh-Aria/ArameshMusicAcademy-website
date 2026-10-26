# Design references

These are the reference sites chosen by the owner for the second redesign pass. They were captured on 2026-10-26 with the Playwright MCP.

Each folder holds:
- `desktop-hero.jpg` (1440×900, the first screen),
- `desktop-full.jpg` (the whole page),
- `mobile-hero.jpg` / `mobile-full.jpg` (390×844),
- `detail-*.jpg` close-ups of the parts the owner pointed at.

Cookie banners were declined, not accepted.

Stills can't show motion. For anything listed under **Motion**, visit the live site.

The owner's own words are quoted in each section. The other notes are observations from the screenshots.

## Design references (look and feel)

### 1. Ethos Music Academy (`ethos/`)
https://ethosmusicacademy.it/ is **the main visual reference.**

> I like how the buttons and items are shaped, for example the "chi siamo" line with the photo next to it.
> I like the course sections and how they move to new course items after some time.
> The hero that keeps changing is nice, and so is the small text inside it.

- **Shape language:** pill buttons. The secondary button is solid white, the primary a strong accent fill (yellow), with no outlines. Large-radius cards (about 24–32px) are inset from the page edge on a near-black ground, so every section reads as a framed panel. The navbar is a floating rounded bar with the call button as a pill on the end.
- **Hero** (`detail-hero-slide-1..3`): a full-bleed photo inside a rounded frame, crossfading every few seconds (drums, cello, violin). On top: a small uppercase tracked eyebrow ("ETHOS MUSIC ACADEMY"), a large light-weight headline, then a short paragraph and two pills placed bottom-opposite. The photos are dark and warm, so white text sits on them easily.
- **"Chi siamo"** (`detail-chi-siamo`): a split panel. On one side, a white rounded card with organic accent-colour blob shapes behind an eyebrow, a big headline and a short paragraph. On the other, a full-height photo card. Both sit together inside one rounded frame.
- **Courses** (`detail-courses-1..3`): three cards. Each has a rounded photo with an age chip ("+6 anni", "3–13 anni"), a title, one or two lines of description and a full-width pill button. **The photo inside each card crossfades to a new photo every few seconds.** The section background is a soft blurred accent glow.
- **Also captured:** the masterclass band (`detail-masterclass`) and events (`detail-events`).

### 2. Royal Academy of Music (`ram/`)
https://www.ram.ac.uk/

> I like how it describes everything that is taught on the main page; the navbar looks good too.

- **Departments grid** (`detail-departments`): a 4-column grid of compact tiles. Each tile has a label and a chevron on a muted fill, plus a small black-and-white photo flush to one edge. It covers every subject taught on one screen without feeling heavy. **This maps directly to our Instruments.**
- **"Find your course"** (`detail-find-your-course`) and the navbar plus hero (`detail-navbar-hero`): a thin uppercase display type, monochrome photography and a calm, institutional tone.

### 3. Aspire Music (`aspire/`)
https://www.aspiremusic.com.hk/

> I like the animated navigation through the website.

- **Motion:** watch it live. The stills only show the bold pill buttons (filled and outlined) and the large rounded type.

### 4. Bettr Academy (`bettr/`)
https://bettr.academy/ is a coffee school, used here for its motion and testimonials only.

> Love the animations here too; the testimonials look good.

- **Testimonials** (`detail-testimonials`): a row of tall cards (star rating, quote, avatar, name, role) that scrolls sideways as a marquee. The heading is a heavy condensed display face. **This maps to our `Testimonial` quotes from parents.**
- **Motion:** watch it live.

### 5. Treehouse Music Studios (`treehouse/`)
https://www.treehousemusicstudios.org/

> I like how they introduce what they teach: the photos for instruments and the overview about them.

- **What we teach** (`detail-instruments`, `detail-instrument-cards`): one column per instrument family. Each has an illustration, a title, a "Book a consultation" bar, an **Overview** paragraph, and a **Deep dive** accordion with more detail. **This maps to an instrument overview, with a call to action per instrument.**

## Content references (what to say, so pages don't feel empty)

> These are just good music academy websites to reference. The items in them, and the things they say (how they teach, descriptions of private lessons), are nice to have on our site so it doesn't feel empty.
> Some show students playing together or solo, in academy concerts or گروه نوازی (ensemble playing). We have photos like these; the owner will choose which ones to upload.

| Site | Folder | Content patterns worth adapting |
|---|---|---|
| https://lewiscentermusicacademy.com/ | `lewis-center/` | A lesson page per instrument; "Why choose us" points (qualified faculty, flexible scheduling, make-up lessons, recitals and performance opportunities, an achievement programme); parent testimonials; a repeated call-to-call band. |
| https://opus1musicstudio.com/ | `opus1/` | "A program for every stage of life" (young children → first recitals → exam prep → lifelong learners); private lessons by instrument, age and goal; recitals as goals; trust points (trained faculty, a teacher matched to your child, a path to mastery); **a parent FAQ** (best age to start, private vs group, do I need an instrument at home). |
| https://www.thrivemusicschool.com/ | `thrive/` | "Three steps to your first lesson"; real students, real growth; lesson-length options; FAQ. |
| https://www.notesnbeats.com/ | `notesnbeats/` | A page per instrument, band and ensembles, past events by year, which fits concerts and گروه نوازی. |

**Excluded on purpose:** prices, online booking, logins and "first lesson free" checkout flows. Online enrollment and payment are out of scope (see `CONTEXT.md`). Contact is the conversion.
