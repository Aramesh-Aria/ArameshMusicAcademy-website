# Next round: decisions collected so far

The owner listed issues one by one; these notes were the build prompt.

**Status (2026-10-28):** sections 1, 2 and 3 are built (not committed yet; see "Built" under each). Section 4 is **on hold until the owner has photographed the instruments**: run it as its own build once the photos exist.

## 1. Display face: Amiri → IranNastaliq (decided 2026-10-28)

- **Use IranNastaliq** (https://github.com/font-store/font-IranNastaliq, `WebFonts/IranNastaliq-Web.woff2`, about 190 KB, SIL OFL 1.1, one weight). It replaces Amiri everywhere Amiri is used today: `--font-display`, so the h1, section heads, card titles and names.
- We compared it with Gulzar and Noto Nastaliq Urdu in `mockups/nastaliq-compare.html` (+ `-desktop.png`, `-mobile.png`). The owner chose IranNastaliq because it is drawn for Persian.
- **It renders about a third smaller** than Amiri at the same `font-size`, with thin strokes. Scale the `--display-*` steps up so headings keep their present visual size, and check card titles and teacher names on a 390px phone.
- **Line height:** Nastaliq needs about 1.7 (Amiri used 1.25). Recheck every heading block, the hero, cards and the navbar brand for clipping and overlap.
- **Digits** in display text stay in Sahel (wrap numbers, or keep them out of the face), as the `fa_digits` comment in `site.css` already describes for Amiri.
- **Self-host it** in `static_dev/assets/fonts/`, subset to the Persian characters the way Amiri was, with `font-display: swap` and a preload. Ship the OFL text next to it. Remove the Amiri files and update the font notes in `site.css` and `DESIGN.md`.
- **Built:** `irannastaliq-fa-400.woff2` (163 KB, cut from the 197 KB web file; Apple's `morx` table is dropped, browsers shape from GSUB) and `IranNastaliq-OFL.txt`; the face is declared for weights 400–700 so bold headings never get a synthesised bold. The display steps are Amiri's times 1.35 (measured: Nastaliq sets a word in about 0.67 of Amiri's width), leading 1.7. Digits, Latin and ASCII punctuation are left out of the file, so Sahel draws them. Also: `.label` headings (footer, contact page) are now Sahel, the schedule's teacher names and the phone teacher grid's names were scaled up, and the gallery's line-clamped album titles got room for the stroke of ک and گ, which climbs above the line and hangs past its start edge. `mockups/nastaliq-compare.html` still points at the removed Amiri file, so its Amiri column falls back to Sahel.

## 2. Hero photos cropped badly

- The four `home-hero` photos are portrait or square (1111×1280, 941×958, 1280×960, 960×1280), but the hero frame is about 16:9, and its start side (the right side in RTL) sits under the copy and a dark scrim. `object-fit: cover` cuts off the instruments (piano, santur, tar, setar).
- Fix in code: add a per-photo focal point in the admin (an `object-position` choice) as a safety net.
- Real fix: new landscape photos, see 4.
- **Built:** `GalleryImage.focal_point` («نقطهٔ مهم تصویر» in the gallery page's image rows, nine positions, default centre), written as `object-position` on the hero's slides. Off-centre positions are a quarter in from the edge (25%/75%), not the edge, so one choice suits both the desktop and phone crops. Run `migrate` after deploying.
- **Owner follow-up (2026-10-28):** photos 1, 3 and 4 still hid their instruments (the santur and half the piano sat under the copy and scrim, and the «امروز» strip covered the tar). The hero layout changed: on desktop the photo fills the far ~60% of the frame and fades into the ground under the copy, with no scrim, and the «امروز» strip moved under the buttons; on phones the photo stands above the copy at 4:3. Photo 2 (صدا سازی و آواز کلاسیک) was replaced by the children's music photo, titled «موسیقی کودک», and the tar/setar photo is set to «پایین». Both are in `seed_data`; **on the live site, make the same two changes in the admin** (home-hero gallery page).

## 3. Schedule: Masoud Aramesh's row repeats «سنتور؛ تئوری و سلفژ» on every day

- **What the owner sees:** under each of his times the grid writes «سنتور؛ تئوری و سلفژ». No other teacher's row does this. His teacher cell also lists «گروه نوازی».
- **Cause** (`apps/schedules/views.py` + `templates/schedules/schedule.html`): the teacher cell shows `Offerings.combine(row['sessions'])`, which includes his Thursday session reserved for گروه نوازی. So the row reads «سنتور؛ تئوری و سلفژ؛ گروه نوازی». A cell names its offerings only when they differ from the row's, and since every normal day lacks گروه نوازی, every cell differs and repeats its offerings.
- **Wanted:**
  - The teacher cell lists only what his normal sessions offer: no گروه نوازی, which lives on its reserved Thursday.
  - His normal days show no offerings line.
  - Thursday keeps its «گروه نوازی» line.
- **Fix:** build the row's offerings from the sessions that aren't reserved for a fixed-time Programme. A reserved session always names its Programme in its cell, as it does now. Keep the per-cell rule (shown only when different from the row) for a session that really offers less. Check the same thing on the phone layout of the schedule, and decide whether teacher, instrument and Programme pages (`week.session_runs`) need the same rule. Add a test with a teacher who has normal sessions plus one reserved session.
- **Built:** the row's offerings leave out reserved sessions. The phone layout and `session_runs` need no change: they have no row list, and each session or run names its own offerings.

## 4. Instrument photos: workflow

**On hold (2026-10-28):** build this after the owner has photographed the instruments. Nothing here can start without the originals.


- The owner shoots the instruments at the Academy in one session: landscape, the same light and background, the instrument in the left half (away from the hero copy), no flash, several takes of each.
- The originals come back to Claude, which crops them to 16:9 (at least 2400px wide) and applies **one shared colour grade** by script (warm, slightly muted, in tune with the dark ground and saffron accent), and hands back the finished files. **The owner uploads them in the admin; that is the only way they reach the live site.** Optionally, the same four also replace the `home-hero` photos in `seed_data`, so a fresh local database looks like production. `seed_data` is for local resets only, and `seed_sample_data` must never run on Runflare.
- AI image tools are for small clean-ups only (a cable, a sign), never for redrawing instruments: they get Persian instruments' strings and bodies wrong.
