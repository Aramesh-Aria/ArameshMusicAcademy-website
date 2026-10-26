# Step 17: `/impeccable audit`

Run on 2026-10-27 on the seeded site, against both the `DEBUG=False` server (hashed static, WhiteNoise) and the
`DEBUG=True` one. Evidence: `impeccable detect` on six pages at 1280 and 390; axe-core 4.10 (WCAG 2.0–2.2 A/AA and
best practice) on 15 pages at 1440 and 390; pixel contrast of the hero text measured with the text hidden, on every
slide at 1440, 1280, 1024, 844×390, 768 and 390; LCP, CLS and transfer size under Chrome's network throttling
(fast 4G: 9 Mb/s, 60 ms; slow 4G: 1.6 Mb/s, 150 ms) with the cache off. Screenshots: `screenshots/step17-audit/`.

## Audit health score

| # | Dimension | Before | After | Key finding |
|---|---|---|---|---|
| 1 | Accessibility | 2 | 4 | The hero's saffron slide title fell to 1.4:1 over the white wall at 1280 (fixed); axe now finds nothing on 15 pages. |
| 2 | Performance | 2 | 3 | The schedule's day tabs collapsed after first paint on phones (CLS 0.33, fixed); the home hero fetched all four slides at once (fixed). Slow-4G LCP on home is still 3.0s. |
| 3 | Theming | 3 | 3 | Tokens throughout; the hero scrims spell the ground as `rgb(23 19 15 / a)` because a token can't take an alpha there without `color-mix`. One theme by design (dark ground, stone panels). |
| 4 | Responsive design | 3 | 4 | Landscape phone: the scrim faded out under the copy and the slide bars covered the slide title (both fixed). No overflow at any width; targets ≥ 40px (step 13). |
| 5 | Implementation integrity | 3 | 4 | Coherent system; the detector's remaining findings are false positives or the owner-pinned eyebrow. |
| **Total** | | **13/20** | **18/20** | **Excellent (minor polish)** |

## Implementation integrity verdict

Pass. One token set, one button system, one frame, used on every page; the detector finds no slop patterns beyond
the hero eyebrow, which the owner pinned (`03-direction.md` §6). Detector findings, verified:

| Finding | Where | Verdict |
|---|---|---|
| `hero-eyebrow-chip` | home | Owner-pinned (the slide's photo title). |
| `low-contrast` (1.1–1.5:1 "via canvas-img-underlay") | home hero h1, lede, slide title | Real for the slide title on desktop before the fix (1.4–2.3:1 measured), partly real for the h1 (2.3:1). The detector reads the photo without the scrim, so its numbers are lower than the truth; after the fix the measured minimum is 6.4:1 (title) and 10.9:1 (h1). |
| `line-length` (~88 chars) | a teacher's biography | The measure is set; Persian words are short, so a line of ~88 characters is about 15 words. Left as is. |

## Findings by severity

- **[P1] Hero text over the bright window (fixed).** `.hero__frame::before`, `static_dev/assets/css/site.css`. The side
  scrim faded from 0.55 at 38% to nothing at 68%, but the copy reaches 47.5rem, about 62% of the frame at 1280. WCAG
  1.4.3. Now dark (0.86) as far as the copy reaches and fading over the next 18rem; on phones dark for at least 30rem
  above the foot.
- **[P1] Schedule layout shift on phones (fixed).** `templates/partials/week.html`, `site.js`. The page painted all
  seven days, then the deferred script hid six (CLS 0.33 at 390, 0.36 on slow 4G). A `js` class set in the head lets
  the CSS open today's tab before first paint; `onerror` on site.js removes it, so a failed script still shows the
  whole week. CLS now 0.01.
- **[P2] Hero photos all fetched at once (fixed).** The three hidden slides were `loading="lazy"` but stacked in view,
  so they loaded with the first (436 KB). They now wait in `data-src`; the script fetches each a turn ahead, after
  `load`. The same holds for Programme card stacks, whose extra photos only ever show under a mouse.
- **[P2] Album photos without a size (fixed).** `partials/plates.html`. The contact band below jumped as photos
  arrived (CLS 0.1–0.27). A new `image_size` tag writes `width`/`height`, and is empty if the file can't be read.
- **[P2] Heading order on the teachers list (fixed).** Card names were `h3` straight under the `h1`.
- **[P2] Home LCP on slow 4G is 3.0s (open).** The LCP photo is the 1111×1280 JPEG (204 KB) shown at 366px wide on a
  phone. Responsive sizes (`srcset`) need smaller copies made on upload, which is an image-pipeline change outside the
  brief. Fast 4G: 0.6s.
- **[P3] Hero scrim colour as a literal (open).** `rgb(23 19 15 / a)` repeats `--ground`. Could be
  `color-mix(in oklab, var(--ground) 86%, transparent)`; left, since it is one place and reads clearly.

## Measurements after the fixes

| Page | Fast 4G LCP | Slow 4G LCP | CLS | Transfer |
|---|---|---|---|---|
| Home (390) | 0.6s | 3.0s | < 0.01 | 673 KB by load + 2s (was 911 KB) |
| Teachers | 0.5s | 2.2–2.4s | < 0.01 | 666 KB |
| Schedule (390) | 0.3s | 0.9s | 0.01 (was 0.33) | 225 KB |
| Contact | 0.3s | 0.8s | < 0.04 | 208–242 KB |
| Rooms album | 1.2s | 6.4–7.5s | ~0.01 | 2.3 MB (13 photos at up to 1920px; lazy below the fold) |

The album's slow-4G figure is the cost of full-size gallery photos; the same `srcset` work would fix it.

## Positive findings

- Persian digits from the font (Sahel FD) with ASCII `tel:` links: correct numbers for the reader and the dialler.
- Every overlay closes on Escape and returns focus; every focus ring now measures at least 3:1 against what is behind it.
- Content is visible with no script at all; motion only ever enhances.

## Recommended actions

1. **[P2] `/impeccable optimize`**: responsive image sizes made on upload (`srcset`/`sizes`) for the hero, teacher
   portraits and gallery photos; the largest remaining LCP and transfer cost.
2. **[P3] `/impeccable polish`**: the scrim literal, at step 22.
