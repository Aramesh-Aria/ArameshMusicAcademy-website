# Direction, pass 2: «سینه به سینه»

**Status:** proposed at Gate 1 (2026-10-26). Shaped with `/impeccable shape` from [02-redesign-brief.md](02-redesign-brief.md) and `references/`. Nothing is built.

The brief pins the look: **Ethos-led**, dark warm frame, light panels for reading, saffron as the one accent, Amiri + Sahel, pills, a floating rounded navbar, a rotating framed hero. This file does not reopen any of that. It decides what the brief left open: the idea that makes the Ethos shape language the Academy's own, how far each device goes, and what the first screen must do.

---

## 1. The idea

> On this site, **the way Persian music is handed down, teacher to student, gusheh by gusheh (سینه به سینه)** becomes **Ethos's sequence of framed panels**: every page is a short, ordered path from a real person to the next step, and it ends at a door the Visitor can knock on.

Why this, and not a santur motif: the santur is what every Persian music school would draw. The lineage is what only this Academy can show truthfully. The teacher bios already carry it:

- مسعود آرامش learned santur from his mother فاطمه روح‌بخش from 1365, and the radif from محمدرضا روح‌بخش and اصغر حسینی.
- سیاوش برهانی learned from his father and uncle, both students of علی‌اکبرخان شهنازی, then from هوشنگ ظریف, فرهاد فخرالدینی and حسین علیزاده.
- علیرضا مهدی‌زاده trained with محمدرضا شجریان.
- فرزاد دهپور learned violin from his father, a student of شکیبی and شاملو, then from ارسلان کامکار.

**Competitor test:** put another Tehran academy's name on it. The panels and pills survive; the lineage, the founder's Yazd story, the Thursday ensemble and these teachers do not. The idea lives in the content sequence, not in an ornament, so it holds.

**What it changes in practice (not decoration):**
1. **Every page reads as a path, not a catalogue.** Programme → Instrument → the Teacher who teaches it → when they are in → contact. Each page ends by handing the Visitor to the next step, never to a dead end.
2. **Teachers are introduced by who taught them.** On teacher cards and pages, one short line of lineage (taken from the bio, owner-approved) sits under the name. It is the strongest proof a parent can read in five seconds.
3. **Ensemble and concerts are the destination.** گروه نوازی and the concert gallery are shown as where private lessons lead (the "از کلاس تا صحنه" step), not as extra products.

## 2. The live thing: «امروز در آموزشگاه»

One thing that differs on every visit, built from real `ClassSession` data in Tehran time:

- Inside the hero, a small framed strip: today's weekday, and who is in today with what they teach, for example «امروز، شنبه — سنتور، پیانو، آواز ایرانی، موسیقی کودک · تا ساعت ۲۱».
- On Friday, or after the last session ends, it says when the Academy opens next, from the same data.
- It links to the schedule, scrolled to today. Server-rendered, so it works with no JavaScript.

It earns its place because a parent's real question is "can I call today and who would my child see?", and it answers it with facts.

## 3. Shaping the pinned world

### Colour (to be tuned in `/impeccable colorize`, step 8)

Scene: a parent on a phone in the evening, after work, in a dim Tehran flat, or an adult learner at a desk. A dark warm ground suits that light; the light panels are where reading happens.

| Token | Proposal | Role |
|---|---|---|
| `ground` | warm near-black, about `#17130f` | The frame, header, footer and photo sections. Also the **ink** on light panels (one token, two jobs). |
| `stone` | warm stone, about `#ebe5dc`, low chroma | Reading panels: about, how we teach, FAQ, contact form. Also the text colour on the ground. **Not** yellow-cream: the taste skill bans cream + warm accent as the third-wave AI look, so the stone stays greyer than the mockup's panel. |
| `saffron` | `#e2a72e`, dark text on it | The primary pill, the active nav item, focus rings, the today marker, the age chip's dot. One large field per page at most (the contact band). |
| `error` | a brick red, about `#a8321f` | Form errors only. |

Secondary text is the ink or stone at reduced opacity, not a fifth colour. Four tokens in total.

### Type

- **Amiri** 700 for display only: the hero headline, section headlines, names on teacher pages, the instrument typographic tiles. Its tall alef and deep descenders need 1.2 leading at display size.
- **Sahel** for everything else: body 18px on phones and 19–20px on desktop, nav, buttons, chips, forms. Weights 400 and 700 (Sahel ships more; we load two).
- **Persian digits everywhere**, through a template filter, never by hand.
- **Never letter-space Persian.** Tracking breaks the joins. Ethos's tracked uppercase eyebrows become short Sahel 700 labels at about 14px, no tracking, in saffron or soft ink.

### Shape

- **Panels:** one large radius, about 28px desktop / 20px phone, inset 12–24px from the viewport edge on the dark ground.
- **Images inside panels:** inner radius = outer radius minus the inset, so corners nest.
- **Pills:** full radius for buttons, chips and the floating navbar. Nothing in between (no 8–16px "soft" radius anywhere).
- **The one shape:** the brief asks for "a subtle saffron shape" on typographic tiles, and Ethos uses blobs behind its about panel. Proposal: replace the blobs with **one shape from the subject, the santur's trapezoid body**, cropped large off one corner at low contrast (saffron at about 18% on stone). It appears in two places only: the about panel and the instrument tiles that have no photo. Never as a pattern, never on the dark ground.

### Imagery

All photos are the Academy's own phone shots of its rooms: dim, warm, mixed white balance, mostly portrait. One treatment unifies them:
- a light warm grade (a slight multiply of the ground colour, never a filter that changes faces),
- a bottom scrim only where text sits on the photo,
- large-radius frames, and the real pipeline ratios (portraits 1:1, covers 3:2, hero 3:2 at 1200px max, gallery at their own ratio).
- The 1200px hero is framed inside the page margins, never stretched past it, so it stays sharp at 1440.
- Missing pictures: teachers get their initials in Amiri on a stone plate; instruments get the typographic tile; empty gallery pages show their description and a quiet "photos coming" state, not a grey box.

### Motion grammar (built in step 12)

Slow and continuous where it carries content, quick where it answers a hand.
- **Hero and Programme cards:** crossfade of about 1.2s every 6–7s; paused on hover, focus and when off-screen; a still image for reduced motion.
- **Pages:** cross-document View Transitions. The clicked card's photo becomes the next page's framed image.
- **Testimonials:** a slow marquee (when real quotes exist), paused on hover and focus, static for reduced motion.
- **Press:** pills scale to 0.97 on press; hover only on devices that hover.
- Content is **visible on first paint**. No section waits for an observer to show itself.

## 4. First viewport

**Desktop (1440×900):** the floating navbar sits 16px from the top: the saffron logo at the start (right), the five links, the saffron pill «تماس ۰۲۱ ۴۴۴۵ ۷۷۴۸» at the end (left). Under it, the hero panel fills the rest of the screen inside 24px margins. On the photo, along the right: the slide's title as a small Sahel label (for example «کلاس سنتور»), the Amiri headline at about 5vw over two lines at most, one supporting sentence, and the two pills (primary saffron «تماس با آموزشگاه», secondary stone «دوره‌ها»). The «امروز در آموزشگاه» strip sits at the hero's bottom-left corner as a small dark frame. Slide progress shows as four short bars by the strip.

**Phone (390×844):** the navbar keeps the logo, a «منو» button and a round saffron call button that never leaves the screen. The hero is a portrait crop (the gallery photos are mostly portrait, which suits it). The headline, sentence and two full-width pills stack at the bottom over the scrim; the «امروز» strip moves under the hero as its own small panel.

## 5. The home page as an argument

| # | Section (brief order) | Claim | Proof on the page |
|---|---|---|---|
| 1 | Hero | This is a real music academy in Tehran, and you can call it now. | Its own rooms; today's teachers; the phone. |
| 2 | About panel + photo | It is led by a working musician. | Masoud Aramesh's facts: santur player and composer, 40+ years, founded 1395. |
| 3 | Programmes | There is a way in for your child or for you. | Four cards with real photos, age chips, short facts. |
| 4 | Instrument grid | They teach the instrument you want. | Every real Instrument as a RAM-style tile. |
| 5 | Director and teachers | Your child would learn from these people. | Portraits, instruments, one lineage line each. |
| 6 | How we teach + three steps | It is personal, and starting is easy. | Private lessons, teachers who perform, ensemble and concerts; call → choose → come in. |
| 7 | Testimonials | Other parents trust it. | Real quotes only; **hidden today**. |
| 8 | Gallery preview | It is a lively place. | The academy-space photos; concerts when uploaded. |
| 9 | FAQ | Your doubts have answers. | Owner-approved answers only. |
| 10 | Contact band | Here is how to reach us. | Phone, address, hours, map link, the form. |

Neighbouring sections never share a layout: full-bleed frame → split panel → card row → tile grid → portrait row → stone reading panel → marquee → mosaic → accordion → saffron field.

## 6. The anti-slop bar (Phase A step 2)

From `/design-taste-frontend` (`references/tells.md`, `critique.md`). Every look round in Phases C and D uses its critique format (§4) and its caps.

**Held without exception:**
- Headlines two lines at most at every width. One `h1` per page; a heading on every section.
- No gradients (a neutral scrim under text on a photo is the only exception), no glows, no shadows on resting things (only the open menu and dropdown float), no glass or backdrop blur.
- No index numbering: the three steps are a real `<ol>` with words, not giant ۱ ۲ ۳ numerals.
- No hairline rules or 1px outlined boxes, except inside the real schedule table and form fields.
- No monospace, no emoji, no icon-topped feature cards, no rows of identical cards with nothing to tell them apart.
- No styled accent word in a headline.
- Running text in full ink at 16px or more; grey only for secondary notes.
- No invented proof: no testimonials, counts, awards, star rows or "1000+ students".
- Content visible by default; motion only enhances what is already there.
- At least four real pictures per page that has pictures at all; one moving picture (the hero crossfade).
- Equal outer margins, no section huddled on one side, no blank stretch over half a screen.

**Knowingly overridden, because the owner pinned them in the brief** (the critique caps that follow from these are accepted and noted, not "fixed"):

| House rule | Brief decision | How we keep it honest |
|---|---|---|
| No eyebrows | Ethos eyebrows above headlines | Only where the label carries information: the hero slide's photo title, and the Programme name above a Programme page's headline. Never a label that repeats the heading («درباره ما» above «درباره ما»). No tracking (Persian). |
| No floating pill navigation | Floating rounded navbar with a call pill | Opaque `ground` fill, no blur, no shadow at rest. |
| Square or fully round, chosen once | Large-radius panels + pill buttons | Exactly two radii: the panel radius and full round. Nothing else. |
| No pill badges | Age chips on Programme cards | They carry a fact the parent filters by (age), never hype ("New", "Popular"). |
| No meaningless infinite loops | Testimonial marquee, hero and card crossfades | Each loop carries content, pauses on hover/focus/off-screen, and has a static reduced-motion state. |
| No decorative shapes | "A subtle saffron shape" on tiles | One shape from the subject (the santur trapezoid), two places only. |

## 7. Challengers weighed (`/impeccable` concept-seed, seed:53b75618a6a3d972)

The brief pins the world, so the roll could not replace it; it could only raise it. My grounded list, by resonance: (1) the santur's body and bridges, (2) the Academy's own rooms at dusk, (3) Yazd termeh under the santur, (4) the concert hall stage, (5) **the radif, learned gusheh by gusheh, teacher to student**, (6) 1970s Shiraz Arts Festival posters, (7) the instrument maker's bench. The roll assigned **(5)**, which became the idea above. All six catalogue challengers were **declined** (none speaks to Tehran parents better than their own Academy's rooms and teachers), and each lends one discipline:

- **Cutting-bench select rail → state is a mark, not a hue.** "Today", "reserved for ensemble" and "closed" read as marks (the saffron today marker, a label), never as colour alone.
- **Risograph system → commit the accent once, fully.** Saffron is either a small action or one whole field per page (the contact band), never sprinkled across many small things.
- **Op-art textile → loops without a visible seam.** The marquee and crossfades never jump or flash at the restart.
- **Broadcast signal → a live clock drives state.** «امروز در آموزشگاه» is computed from the real schedule in Tehran time.
- **Versailles vistas → a page is a measured walk with one axis.** Each page reads top to bottom as one path that ends at contact, and View Transitions keep the axis between pages.
- **Memory quilt → every piece carries its provenance.** Every photo shows its admin title where it has one (the hero's small text, gallery captions); untitled photos stay quiet rather than getting invented captions.

## 8. Direction contract (draft; recorded in the surface brief after Gate 1)

- **THESIS:** The Academy's teacher-to-student lineage, told as Ethos's sequence of framed panels: every page is a short path from a real person to the next step, ending at contact. It refuses the category's catalogue of instruments with a "register now" button.
- **OWN-WORLD:** A warm near-black frame holding large-radius stone and photo panels; saffron only on the call pill, focus, today's marker and one field per page; Amiri display over Sahel text; pill buttons; the Academy's own dim, warm room photos in nested rounded frames.
- **STORY:** A parent sees real rooms and who is in today, reads that a working santur player leads the place, picks a Programme and an Instrument, meets the teacher through who taught them, and calls.
- **FIRST VIEWPORT:** Floating opaque navbar with the phone pill; a full-height framed hero crossfading the `home-hero` photos with each photo's title as its small text; a two-line Amiri headline and one sentence on the right; saffron «تماس با آموزشگاه» and stone «دوره‌ها» pills; the «امروز در آموزشگاه» strip in the bottom-left corner.
- **FORM:** Ethos-led (brief-pinned), raised by the assigned grounded candidate 5 of 7, the radif's teacher-to-student path. seed:53b75618a6a3d972.
- **FINISH:** unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.

## 9. Open for the owner at Gate 1

1. The idea (lineage) and the live thing («امروز در آموزشگاه»).
2. The santur trapezoid as the one shape, replacing Ethos's blobs.
3. Lineage lines under teacher names, written from the bios.
4. The four colour tokens, with the stone kept greyer than the mockup's cream.

Models, migrations and the drafted Persian copy are in [gate-1-models-and-copy.md](gate-1-models-and-copy.md).
