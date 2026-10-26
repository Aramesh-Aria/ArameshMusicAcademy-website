# Step 17: `/impeccable critique` against the references

Method: dual-agent (A: design review in its own Playwright tab · B: detector CLI on the live URLs and the templates),
2026-10-27, on the `DEBUG=False` server at 1440×900 and 390×844, 14 pages. The live overlay was skipped (one shared
browser, in use by A); B's URL scans are the fallback signal. Screenshots: `screenshots/step17-critique/` (`a-*` from
A, `fix-*` after the fixes below). Baseline: [critique-baseline-pass1.md](critique-baseline-pass1.md), 19/36.

## Design health score

| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of system status | 3 | The «امروز» strip read as open before the day's first class («… تا ساعت ۲۳» at 02:30). Fixed: it now says «از ساعت ۱۲ تا ۲۳» until classes start. |
| 2 | Match system / real world | 3 | Persian digits and a warm voice; the schedule writes ranges as LTR «۱۲:۰۰ – ۲۱:۰۰» where everything else says «۱۲ تا ۲۱»; the captcha is Latin letters. |
| 3 | User control and freedom | 3 | Escape everywhere, crumbs, ways on from empty pages; `/gallery/` lists empty albums before the one with photos (admin order). |
| 4 | Consistency and standards | 2 | **The published hours contradict the timetable** (owner question 1). Mixed portrait treatments (black-and-white, colour, a circle inside a square). |
| 5 | Error prevention | 3 | Phone required, email optional; but a call-back still needs a subject, a message and the captcha. |
| 6 | Recognition rather than recall | 3 | The Instrument grid and the دوره‌ها menu answer "who teaches tar?"; the phone schedule's day tabs are single letters. |
| 7 | Flexibility and efficiency | n/a | Persuade surface; the always-visible call button is the accelerator. |
| 8 | Aesthetic and minimalist design | 2 | Coherent, but the no-photo fallback repeated 19 times on home (partly fixed), and the contact band and footer repeat the same facts. |
| 9 | Error recovery | 3 | An error summary that links each field, specific messages, input kept; the captcha's message is the generic one. |
| 10 | Help and documentation | 2 | «سه قدم» and «شیوهٔ آموزش» answer "how do I start"; "from what age?" is answered nowhere while the FAQ and age labels are empty. |
| **Total** | | **24/36** | **Acceptable, close to Good** (baseline 19/36) |

## Design specificity verdict

**Assessment A:** specific in its content, borrowed in its shape. The Ethos structure is copied closely and executed with
discipline; what makes it the Academy's own is real content: the lineage line under every teacher (the «سینه به سینه»
idea, which passes the competitor test), the «امروز» strip from the real schedule, the director's own frames on hero
slide 1, the saffron calligraphic logo as the close. The weak point was the fallback: with no Programme or Instrument
photos, the santur shape had become the most repeated image on the site (19 times on home).

**Assessment B (detector):** 4 findings on the 15 live URLs at 1280 and 1 at 390, three rules. `hero-eyebrow-chip` is the
owner-pinned slide title (`03-direction.md` §6). The `low-contrast` findings on the hero (1.2–1.5:1) are false
positives: the detector reads the photo without the scrim; the measured minimum is 6.4:1 for the title and 10.9:1 for
the headline. `line-length` on the longest biography is real but minor: `--measure` is 36em, about 85 Persian
characters, and its comment said 65 (corrected). The template scan's 30 findings in live templates are artefacts
(`{% static %}` unresolved → `design-system-color` ×28; `data-src` crossfade photos → `broken-image` ×2); the 41 in
`templates/corebiz_raw/` are unused theme files.

## What's working

1. **Teachers are the proof.** Portrait, Amiri name, instruments in bold, a lineage line, the weekly days; initials in Amiri
   when there is no photo; teacher pages end with a band that names them.
2. **Contact is always within reach without being pushed.** The navbar pill, the round call button that never leaves a
   phone's screen, two labelled numbers, good form errors.
3. **A disciplined system.** Amiri over Sahel, Persian digits, saffron only for action and the one band, two radii,
   visible focus everywhere.

## Priority issues, and what this step did

- **[P1] The no-photo fallback repeated until it became the design. Partly fixed.** Programme cards, Programme page
  heads and gallery albums with no photo now drop the image slot (a card is its text, set at the foot so it lines up
  with photographed neighbours; a Programme head sets its name beside its text on wide screens). That leaves the
  santur shape where the brief and direction put it: Instrument tiles without a photo, the Instrument page's type tile,
  the about panel and the notices. The 15 identical Instrument tiles remain: owner question 2.
- **[P1] Published hours contradict the timetable. Owner question 1.** The band, footer and contact page say «شنبه تا
  چهارشنبه: ۱۰ تا ۲۱ / پنجشنبه: ۱۰ تا ۱۴»; the schedule has sessions to 23:00 on Tuesday and Wednesday and to 19:00 on
  Thursday. Gate 1 kept `SITE_HOURS` as the owner wrote it.
- **[P2] The closing chrome takes half of a short page.** On `/instruments/santur/` at 390 the band and footer are 52% of
  the page, and both list the phones, address and hours. Owner question 3.
- **[P2] Thin pages leave content at one side at 1440.** One teacher card and one session tile on
  `/programmes/children/`; four identical session tiles on `/instruments/santur/` («۱۲ تا ۲۱ مسعود آرامش» on four
  days). Merging identical days («شنبه تا سه‌شنبه، ۱۲ تا ۲۱») is a display-rule change; left for step 19 (`/break-ui`).
- **[P2] Calling and the form have friction on a phone.** Numbers sit about 1,300px below the form's start; subject and
  message are required; the captcha is Latin letters. Owner question 4 (a form change is a model/behaviour change).

## Persona red flags

- **Tehran parent on a phone at 21:30:** the hero says «تا ساعت ۲۳» while the band says «۱۰ تا ۲۱»; nothing says from what
  age; the form wants a subject, a message and Latin captcha letters. The round call button and the teacher rail with
  faces carry them.
- **Adult learner after tar or Persian voice:** the path works (دوره‌ها → همه سازها → تار → سیاوش برهانی and his lineage →
  his days), but the Instrument page has no overview of the instrument yet (owner to-do), and there is no audio or video.
- **Less digital Visitor:** the LTR time ranges in the desktop schedule, single-letter day tabs on phones, the Latin captcha.

## Minor observations (not fixed here)

Hero photos 941–1,280px wide fill a 1,392px frame at 1440 and look soft; portraits mix black-and-white and colour; on
`/instruments/` the h1 sits 12px under the navbar; «۱۱ استاد» and «همهٔ اساتید» sit far from their headings at 1440;
«گیتار الکتریک» wraps in the phone tile; the address in the «سه قدم» panel breaks at «نبش خ»; the About copy is the raw
admin text; the email placeholder falls back to a Latin face.

## Questions for the owner

1. **Hours:** should the line read as phone hours («ساعت پاسخ‌گویی تلفن»), or be worked out from the timetable as class
   hours? Today it contradicts the 23:00 sessions.
2. **Instrument tiles with no photo:** keep the santur shape on each (as the direction says), or make them text-only RAM
   tiles (name and chevron) until photos arrive?
3. **Band and footer:** keep the facts in the footer and cut the band to its headline and two buttons, or the reverse?
4. **The form:** may subject and message become optional, and the captcha use digits instead of Latin letters?
