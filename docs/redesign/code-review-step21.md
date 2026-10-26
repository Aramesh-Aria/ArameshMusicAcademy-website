# Step 21: `/code-review` on `re-design-ui`

Run on 2026-10-27 over `git diff main...HEAD` (merge-base `49db43e`, 48 commits), as two separate reviews: Standards
(CLAUDE.md, CONTEXT.md, `docs/adr/`, and a Fowler smell baseline) and Spec (this brief, Gate 1 and Gate 2). Nothing
was changed in this step; the findings go to Phase E and the owner. The hard claims below were checked by hand.

## Standards

**Breaches of a documented standard**

1. `apps/contact/templates/captcha/widgets/captcha.html` is a per-app template. CLAUDE.md: templates are "project-level
   under `templates/` (not per-app)". Move it to `templates/captcha/widgets/captcha.html`.
2. CONTEXT.md lists "offering" under *Avoid* (for Programme). The display rule is named with it:
   - `Offerings` and `ClassSession.offerings()` in `apps/schedules/models.py`;
   - `display_offerings` in `apps/schedules/admin.py`;
   - `show_offerings` and `row.offerings` in the templates.

   Either rename it, or record in CONTEXT.md that "offerings" means "what a session lists", not a kind of Programme.
3. CONTEXT.md lists "Album" under *Avoid* (for GalleryPage). The CSS classes `.album` and `.album-grid` and the
   `templates/gallery/_subpage.html` comments use it.
4. CLAUDE.md is behind the code. The "Image processing on save" list leaves out `Programme` and `Instrument`, and the
   `SITE_MAP_*` settings aren't among the hardcoded ones. The `seed_worst_case` command was added at step 19.

**Smells (judgement calls)**

- **Possible duplicated code.** The same steps (read the old row, compare file names, `process_image`, `.update()` the
  stored name) repeat in Programme, Instrument, Teacher, SitePageContent, GalleryPage and GalleryImage `save()`.
  One helper in `core.image_utils` would hold it.
- **Possible primitive obsession / repeated switches.** `instruments_shown == ALL` stands in for "private lessons" in:
  - `programmes/models.py`, `programmes/views.py`;
  - `programme_detail.html`, as the raw strings `'all'` and `'children_only'`.
- **More string constants.**
  - `limit_choices_to={'kind': 'fixed_time'}` in `schedules/models.py` doesn't use `Programme.Kind`.
  - `Today.state` is a free string.
  - `phones[1]` means "mobile" by its position.
- **Possible duplicated code.** "A teacher's active Programmes" is filtered in Python twice, and `Teacher` has no
  `.active()` queryset, unlike ClassSession, Programme, FAQ and GalleryPage.
- **Hidden rule.** `director = home_teachers[0]` in `pages/views.py`.
- **Stale static.** Seven old hashed `site.<hash>.css` copies are committed under `public/static/assets/css/`. Only
  `site.116ca8232052.css` is in the manifest.

## Spec

**Missing or partial**

1. **Step 14 cleanup.** Gate 2: "delete them at step 14", and step 9 said to keep `mockups/components.html` "until
   step 14". Still in the tree:
   - `prototype-buttons.html`, `prototype-hero.html`, `prototype-home-hero.html`
   - `components.html`
   - `mockups/img/hero-*.jpg`

**Not asked for**

2. **Models and migrations.** None beyond the brief and the Gate 1 yeses. The one recorded deviation is from step 7:
   Nasim Haghi's Saturday session has بلز and فلوت as its Instruments. The output doesn't change.
3. **Persian copy with no recorded approval:**
   - «از زبان خانواده‌ها» (home testimonials heading);
   - the note on private-lesson Programme pages, «روز و ساعت هر کلاس را با استاد و آموزشگاه هماهنگ می‌کنید؛ …»;
   - «سازهای این دوره» and «استادان این دوره»;
   - the «امروز» strip's `over`, `closed` and `before` lines, and «… و N مورد دیگر».
4. **The separator in the schedule display rule.** §1 gives the rule as «پیانو، گیتار … · تئوری و سلفژ», and step 13
   left « · » as "a question for step 19 or the owner". Step 19 changed it to «؛» because the dot reads as ۰. It needs
   the owner's yes, or a revert.

**Implemented, but looks wrong**

5. **Friday line.** Gate 1 §3.1 says its hours come from `SITE_HOURS`. The line uses the first session's start
   (`next_from` in `week.py`), which gives 12 in the seed while the published hours say 10. This is the same conflict
   as owner question 1 in `critique-step17.md`.
6. **Contact success.** Gate 1's line «پیام شما رسید. همکاران ما در ساعات کاری با شما تماس می‌گیرند.» isn't used. The
   page keeps the pass-1 sentence, which still offers a reply by email, although email is now optional and the
   Academy calls back.
7. **Home headline.** The headline is option A («موسیقی، در فضایی آرام»). The log doesn't record which option the
   owner picked at Gate 1.

## Summary

- **Standards:** 4 breaches and 7 smells. The worst is the avoided term "offering" naming the schedule display rule.
- **Spec:** 7 findings. The worst is copy shipped without approval (items 3, 4 and 6).
