# Step 16: `/design-taste-frontend` inspector and look round

Run on 2026-10-27 against the production-mode server (`DEBUG=False`, `runserver --nostatic`, hashed static files),
13 pages at 1440, 768 and 390. Reports and screenshots: `.taste-skill/inspect/<page>/` (gitignored); the fixed
session tiles: `screenshots/step16-taste/`.

Allowed rules (owner-pinned in `03-direction.md` §6, or decided earlier in the brief): `eyebrow` (the hero slide
title), `still-page` (brief §3.5 and step 12 rejected section entrances), `palette-cream` (`--stone #ebe5dc` is the
approved low-chroma stone), `no-footage` (no honest clip exists; the videos page is empty).

## Round 1

```
ROUND 1
Seen in one second: a dark, warm frame around a real santur room, a two-line Amiri headline, a saffron call pill.
Idea (one sentence): the teacher-to-student lineage, told as a path of framed panels ending at contact.
Live thing: «امروز در آموزشگاه», today's teachers and closing hour from the real ClassSessions in Tehran time.
Layout words by section: hero=framed photo / about=split panel / programmes=card row / instruments=tile grid /
  teachers=portrait grid / teaching=stone reading panel / rooms=mosaic / contact=saffron field / footer=logo close.
Scores: design 7 · usability 8 · creativity 6 · content 6 → overall 6.8.
Caps applied: content capped by data the owner has still to upload (no Programme or Instrument photos, so the
  four cards and fifteen tiles all show the same santur shape; no testimonials, FAQ or concert photos).
Top three problems (most visible first), each with the screenshot it shows in and the fix:
1. Teacher, Instrument and Programme pages (teacher/desktop-page-01): the class times are hairline-ruled rows
   crammed into the right half at 1440, with 870px of nothing beside them and «برنامهٔ کامل هفته» stranded
   at the far left. Fix: one raised ground-2 tile per session across the full width, two to a row on phones.
2. Home hero (home/desktop-fold): the «امروز» strip trails off as «تنبک و …، تا ساعت ۲۳», which reads as a
   typo. Fix: «… تنبک و ۳ مورد دیگر، تا ساعت ۲۳», counted from the data.
3. Every page (home/desktop-page-02): a 1px rule over the footer's © line, the one hairline left outside the
   schedule table and form fields. Fix: delete it; the space above already separates it.
```

All three fixed. Round 2 re-ran the inspector on home, a teacher, an Instrument and a Programme: `hairline` and
`empty-middle` are gone.

## What the meter still reports, and why it stays

| Rule | Where | Verdict |
|---|---|---|
| `reduced-hidden` | every page | False positive: the ten "hidden" blocks are the closed «دوره‌ها» and «گالری» dropdown items in the navbar. Checked by hand under reduced motion: nothing in `main` is at opacity 0 or hidden. |
| `covered-text` | teachers, a teacher, a Programme | False positive: the sticky navbar passes over headings and initials while scrolling. |
| `edge-text`, `side-scroll` | home, Programme pages at 390 | The phone rails (Programmes, teachers) scroll sideways with the next card peeking in; decided at steps 11 and 13. |
| `off-centre`, `ragged-edges` | most pages | RTL artefacts: the meter measures left text edges, and right-aligned Persian lines end at different lefts. The frames measure 12/12px at 390 and 13/13px at 768. |
| `few-pictures` | schedule, contact, instruments, a teacher, Programme pages, gallery index | Owner data: Instrument and Programme photos and concert albums are owner to-dos. Pages with photos (home, about, the rooms album) pass. |
| `name-only-title` | teachers, gallery | «اساتید» and «گالری» match the navbar; the intro line under each says what the page holds. Left as is. |
| `grey-body` | gallery index | The soft ink (6.2:1) is the album cards' secondary note, not running text. |

Still falling short, for the owner rather than the code: the repeated santur fallback on cards and tiles until real
photos arrive, and the « · » between offerings, which Sahel draws small enough to read like a Persian zero (step 19).
