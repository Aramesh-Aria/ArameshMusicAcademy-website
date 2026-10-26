# Step 19: `/break-ui` with the worst cases

Run on 2026-10-27. The worst case enters where the demo data does, through the database:
`apps/core/management/commands/seed_worst_case.py` loads the real seed, then pushes it to the limits the models allow.
It refuses to run with `DEBUG` off or against `database/db.sqlite3`. To flip between the two:

```bash
DATABASE_PATH=database/worst.sqlite3 DEBUG=True python manage.py migrate
DATABASE_PATH=database/worst.sqlite3 DEBUG=True python manage.py seed_worst_case
DATABASE_PATH=database/worst.sqlite3 DEBUG=True python manage.py runserver 8002   # worst case; :8000 is the demo
```

What the worst case holds, field by field (limits from the models):

| Field | Worst-case value | Limit |
| --- | --- | --- |
| Teacher's Instruments | Ali Shams with six (piano, accordion, harmonica, electric guitar, pop guitar, flute), a «.» biography, no portrait, teaching six days a week at the same hours | M2M, unbounded |
| Teacher name | «سیدمحمدحسین میرهاشمی طباطبایی‌نژاد» | 100 + 100 |
| Lineage | a 100-character line of teachers and a degree | 120 |
| Instrument name | «سازهای کوبه‌ای آفریقایی و آمریکای لاتین», no photo | 100 |
| Programme name, age label | «آموزش موسیقی کودک به روش ارف، ویژهٔ پیش‌دبستانی», «از ۴ تا ۶ سال، همراه با یکی از والدین» | 100, 40 |
| Gallery | three empty top-level albums (real), plus an empty sub-page with a 66-character concert title | 150 |
| Testimonials | exactly one, with a 52-character relation line | 120 |
| FAQ | one, with a two-line question, linked to the children's Programme | 200 |

Checked at 1440, 768, 390 and 320 on 12 pages, then with the root text at 150% and 200%. No page scrolls sideways at
any width. Screenshots: `screenshots/step19-break/`.

## What broke

| # | Severity | Field | Worst-case value | What happens | Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | Ugly | testimonials | one quote | The marquee repeats it: at 1440 the same quote sits twice side by side over an empty half, sliding. | Fewer than four quotes stand still and are listed once (`marquee--still`, `templates/pages/home.html`). **Fixed**, with a test. |
| 2 | Ugly | offerings | «…گیتار پاپ · تئوری و سلفژ» | Sahel draws the middle dot like a Persian zero, so the line reads «پاپ ۰ تئوری». | A Persian semicolon: «…گیتار پاپ؛ تئوری و سلفژ» (`Offerings.__str__`, `apps/schedules/models.py`). **Fixed**; tests updated. |
| 3 | Ugly | Instrument name | the 40-character name, at 320 | In a two-column tile it breaks word by word over five lines, «و» alone on one. | One tile a row below 22.5em (360px) (`.tile-grid`, `site.css`). **Fixed.** |
| 4 | Fragile | navbar | root text at 200% on a wide screen | The call button is pushed 79px off the left edge and the page scrolls sideways. A browser's own zoom or default font size also moves the em breakpoints, so this needs text-only zoom to happen. | The links wrap onto a second row (`.navbar__links`, `site.css`). **Fixed.** |

## Decisions for the owner

- **Identical sessions on consecutive days.** Ali Shams's six tiles all read «۸ تا ۹:۳۰» with the same Instruments
  (and today, Masoud Aramesh's four on the santur page). Merging them into «شنبه تا پنجشنبه، ۸ تا ۹:۳۰» changes the
  schedule's display rule; recommended, but it's the owner's call how the week should read.
- **A teacher card with six Instruments** (`teacher-card-390-six-instruments.png`) wraps to four lines and may break
  inside a name («گیتار / پاپ»). Keeping each name whole risks overflow with a long Instrument name; recommended to
  leave it wrapping.
- **A 40-character age label** wraps to two lines on the card's chip. Readable; the admin help text could ask for about
  20 characters.

## What held up

- Ali Shams and Mohsen Homayouni: the «.» biography is never shown (`public_biography`); with no portrait the card and
  page show their initials in Amiri.
- Six Instruments on the teacher page wrap cleanly in the definition list; six session tiles fill their grid.
- The long teacher name wraps to three lines in the page head and stays whole on the card; the lineage line wraps.
- The long Programme name and age label wrap inside the card; the card with no photo keeps its text at the foot.
- Empty albums and the empty sub-page say so and offer ways on (back to the parent, all albums, the schedule).
- No testimonials and no FAQ: both sections are absent, not empty. One FAQ opens and closes on the Programme page.
- No horizontal scroll at 320–1440 on any page with the worst case.
