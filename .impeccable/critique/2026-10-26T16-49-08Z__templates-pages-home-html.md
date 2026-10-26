---
target: current site (pass 1 baseline)
total_score: 19
max_score: 36
na_heuristics: 7
p0_count: 1
p1_count: 3
target_identity: "file:/Users/aria/Documents/ArameshMusicAcademy-website/templates/pages/home.html"
target_fingerprint: "sha256:f54041b8d101aa126d810764c1a7a5b569c9bb286c88e1b4b8fcd0dc1b317f5a"
target_path: /Users/aria/Documents/ArameshMusicAcademy-website/templates/pages/home.html
timestamp: 2026-10-26T16-49-08Z
slug: templates-pages-home-html
---
# Baseline critique: the first-pass site (before pass 2)

Method: dual-agent (A: design review · B: detector + browser), 2026-10-26, on the seeded site at 1440×900 and 390×844. Screenshots: [screenshots/pass1-baseline/](screenshots/pass1-baseline/). This is the "before" for the final report.

## Design health score

| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of system status | 3 | Today is marked in the schedule and the nav; at 21:30 "today" still lists sessions that ended, with no "closed now" state. |
| 2 | Match system / real world | 2 | Latin digits for times and phones (against the owner's decision); the About text is raw pasted copy. |
| 3 | User control and freedom | 3 | Simple nav and a breadcrumb; empty gallery pages are dead ends. |
| 4 | Consistency and standards | 2 | Thursday hours 10–14 in the footer vs. the 10–19 ensemble session; four unlabelled phone numbers. |
| 5 | Error prevention | 2 | The form requires email and makes phone optional, backwards for parents who want a call. |
| 6 | Recognition rather than recall | 3 | No Instrument or Programme index: "who teaches tar?" means scanning 11 rows. |
| 7 | Flexibility and efficiency | n/a | Persuade surface; the sticky mobile call bar is the one accelerator. |
| 8 | Aesthetic and minimalist design | 2 | Minimal tipped into monotone: the same paper sheet on green everywhere, greyscale photos. |
| 9 | Error recovery | 1 | Empty bio renders «.»; empty gallery shows a blank plate; custom 404 not verified with DEBUG off. |
| 10 | Help and documentation | 1 | No FAQ; a parent's pre-contact questions go unanswered. |
| **Total** | | **19/36** | Poor-to-acceptable band |

## Design specificity verdict

**LLM assessment:** not category-interchangeable but under-expressed. The printed-programme idea is real (paper sheet, Amiri, the live «امروز در آموزشگاه» tabs, jade only on the call), but all its specificity is typographic, none sensory. Every photo is forced to greyscale, so the santur, the paisley vest and the instruments lose their warmth, and the empty rooms read as vacant. Against Ethos it lacks an immersive photographic moment; against RAM it lacks a "what can I learn" entry (Programmes, Instruments).

**Deterministic scan:** 62 CLI findings. The 21 in live templates are all `design-system-color` false positives (the scanner could not resolve `{% static %}` and saw default black). The other 41 are in the unused `templates/corebiz_raw/`. The in-browser detector found **no anti-patterns** on home, teachers, schedule, gallery and contact; zero console errors and zero failed requests.

## What's working

1. Contact is always within reach without pushing: header phone, the sticky تماس / مسیر bar on phones, a per-teacher call line.
2. The «امروز در آموزشگاه» live schedule is specific and accessible (real tabs). Pass 2 keeps it as its live thing.
3. Persian type is set with care: generous Amiri body, no broken joins, documented AA contrast.

## Priority issues

- **[P0] Contact data is ambiguous.** Four unlabelled numbers, Latin digits, phone optional on the form, Thursday hours that contradict the schedule. Fix: one primary number for every call action, label or demote the rest, Persian digits (tel: links stay ASCII), phone required and email optional, reconcile Thursday. → `/impeccable clarify`, `/impeccable harden`.
- **[P1] Greyscale drains the warmth.** The owner's "not premium" complaint. Fix: drop the global greyscale, grade warm, lead with one large photographic moment. → covered by the pass-2 direction.
- **[P1] No "what can I learn" entry.** Fix: Programme cards and an Instrument grid on home, Programme and Instrument pages. → covered by ADR-0002 and the Gate 1 models.
- **[P1] Edge cases leak.** `home-hero` shows publicly with its admin description; empty categories are blank tiles; «.» for an empty bio; grey square for a missing portrait; the Google map renders grey in Iran. → `/impeccable harden`; partly covered by the brief.
- **[P2] Monotone composition, arbitrary hierarchy.** Every section the same sheet; an oversized portrait of one teacher implies a ranking; About is a raw list. → `/impeccable layout`, `/impeccable typeset`.

## Persona red flags

- **Tehran parent on a phone at 21:30:** the first screen is a timetable with no face; "today" still lists finished sessions; four numbers and no idea which answers now; the map is grey; the form needs an email and a hard captcha; no answer to "from what age?".
- **Adult learner after tar or Persian voice:** can only find teachers by name; two teachers have no photo or bio; no audio or video; the site never says every lesson is private.
- **Less digital Visitor:** small grey secondary text, a hard captcha, low-affordance underlined links beside one solid button.

## Minor observations

Header phone isolated at the far end; tiny «همهٔ اساتید» links far from their headings; the schedule repeats the same instrument string in every cell; the scalloped edge is on every sheet; an orphaned fifth gallery tile; Latin digits in the teacher count and the footer year; a long mobile menu with all four numbers.

## Questions to consider

1. If آرامش means calm, why does the site feel stern? Is calm closer to warm low light and wood than to cold paper on bottle-green?
2. Would a parent rather see a timetable or a child's hands on a santur in the first three seconds?
3. Should the site show one phone number? What do four say to a nervous first-time caller?
