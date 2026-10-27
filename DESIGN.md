---
name: Aramesh Music Academy
description: Teacher to student, «سینه به سینه»: framed stone panels on a warm near-black ground, saffron for the one way in.
colors:
  ground: "#17130f"
  ground-2: "#24201b"
  stone: "#ebe5dc"
  stone-soft: "#aba69e"
  ink-soft: "#57524d"
  field: "#f7f4ef"
  field-line: "#8c8780"
  saffron: "#e2a72e"
  saffron-deep: "#9a6c12"
  error: "#a8321f"
typography:
  display-l:
    fontFamily: "Amiri, Sahel, Times New Roman, serif"
    fontSize: "clamp(2.75rem, 1.6rem + 4.8vw, 4.75rem)"
    fontWeight: 700
    lineHeight: 1.25
  display-m:
    fontFamily: "Amiri, Sahel, Times New Roman, serif"
    fontSize: "clamp(2rem, 1.5rem + 2.1vw, 3.25rem)"
    fontWeight: 700
    lineHeight: 1.25
  display-s:
    fontFamily: "Amiri, Sahel, Times New Roman, serif"
    fontSize: "clamp(1.625rem, 1.38rem + 1.05vw, 2.25rem)"
    fontWeight: 700
    lineHeight: 1.25
  lead:
    fontFamily: "Sahel, Tahoma, Segoe UI, sans-serif"
    fontSize: "clamp(1.25rem, 1.12rem + 0.56vw, 1.5rem)"
    fontWeight: 400
    lineHeight: 1.7
  body:
    fontFamily: "Sahel, Tahoma, Segoe UI, sans-serif"
    fontSize: "clamp(1.125rem, 1.06rem + 0.28vw, 1.25rem)"
    fontWeight: 400
    lineHeight: 1.85
  small:
    fontFamily: "Sahel, Tahoma, Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.4
  label:
    fontFamily: "Sahel, Tahoma, Segoe UI, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 700
    lineHeight: 1.4
rounded:
  panel: "clamp(1.25rem, 0.9rem + 1.4vw, 1.75rem)"
  inner: "max(0.75rem, calc(var(--radius-panel) - 0.75rem))"
  pill: "999px"
spacing:
  "1": "0.25rem"
  "2": "0.5rem"
  "3": "0.75rem"
  "4": "1rem"
  "5": "1.5rem"
  "6": "2rem"
  "7": "3rem"
  "8": "4rem"
  "9": "6rem"
  "10": "10rem"
  frame: "clamp(0.75rem, 1.7vw, 1.5rem)"
  margin: "clamp(1rem, 3.3vw, 3rem)"
  section: "clamp(4rem, 8vw, 6rem)"
  panel-pad: "clamp(1.25rem, 4vw, 4rem)"
components:
  button-primary:
    backgroundColor: "{colors.saffron}"
    textColor: "{colors.ground}"
    typography: "{typography.body}"
    rounded: "{rounded.pill}"
    height: "50px"
  button-secondary:
    backgroundColor: "{colors.stone}"
    textColor: "{colors.ground}"
    typography: "{typography.body}"
    rounded: "{rounded.pill}"
    height: "50px"
  button-primary-on-saffron:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.stone}"
    rounded: "{rounded.pill}"
    height: "50px"
  panel:
    backgroundColor: "{colors.stone}"
    textColor: "{colors.ground}"
    rounded: "{rounded.panel}"
    padding: "{spacing.panel-pad}"
  band:
    backgroundColor: "{colors.saffron}"
    textColor: "{colors.ground}"
    rounded: "{rounded.panel}"
    padding: "{spacing.panel-pad}"
  tile:
    backgroundColor: "{colors.stone}"
    textColor: "{colors.ground}"
    rounded: "{rounded.inner}"
    height: "5.5rem"
  session-tile:
    backgroundColor: "{colors.ground-2}"
    textColor: "{colors.stone}"
    rounded: "{rounded.inner}"
    padding: "1rem 0.75rem"
  chip:
    textColor: "{colors.ground}"
    typography: "{typography.small}"
    rounded: "{rounded.pill}"
    height: "2rem"
  field:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ground}"
    rounded: "{rounded.inner}"
    padding: "0.5rem 1rem"
    height: "3.25rem"
  navbar:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.stone}"
    rounded: "{rounded.pill}"
    padding: "0.375rem"
---

# Design System: Aramesh Music Academy

## Overview

**Creative North Star: "سینه به سینه" (chest to chest)**

Persian music is handed down teacher to student, gusheh by gusheh. The site tells that as a sequence of framed panels on a warm near-black ground: every page is a short path from a real person to the next step (a Programme, an Instrument, the teacher who teaches it, the days they are in) and it ends at a door the Visitor can knock on, the saffron contact band. The idea lives in the order of the content and in one line of lineage under each teacher's name, never in ornament.

The shape language is Ethos-led and was pinned by the brief: large-radius stone panels inset from the edge, pill buttons, a floating rounded navbar, a full-height framed hero that crossfades the Academy's own photos. It is calm on purpose (آرامش means calm): one accent, two typefaces, two radii, and motion that is slow where it carries content and quick where it answers a hand. The one live thing is the «امروز» strip in the hero, built from the real timetable in Tehran time.

The rejected look is the category's catalogue of instruments with a "register now" button, cream paper with a warm accent, and the santur drawn as decoration on everything.

**Key Characteristics:**
- A warm near-black ground; stone panels where reading happens; saffron only for the way in.
- Amiri 700 for display, Sahel for everything else, Persian digits everywhere, no letter-spacing.
- Two radii (the panel's, nested inside it, and full pills), nothing in between.
- The Academy's own photos in nested rounded frames; text alone where there is no photo.
- Content is visible on first paint; motion never gates it.

## Colors

Four colours (ground, stone, saffron, error) plus only the steps of them that contrast needs. Every pair is measured.

### Primary
- **Saffron** (#e2a72e): the call pill in the navbar and hero, the contact band (one saffron field per page), active and current states, focus rings on the ground, today's marker. Dark text on it (ink on saffron 8.6:1); on the ground it reads at 8.6:1.
- **Deep Saffron** (#9a6c12): saffron where it marks something on stone (an underline, a dot), since saffron itself is 1.7:1 there. 3.7:1, so never used for text.

### Neutral
- **Ground** (#17130f): the page, the navbar and the footer. It is also the ink on stone and on saffron (one token, two jobs).
- **Raised Ground** (#24201b): a dark tile on the ground: session tiles, empty photo plates. Stone on it is 12.9:1.
- **Stone** (#ebe5dc): reading panels, cards and tiles, and the text colour on the ground (14.8:1). Kept greyer than cream.
- **Soft Stone** (#aba69e): secondary text on the ground (7.6:1).
- **Soft Ink** (#57524d): secondary text on stone (6.2:1).
- **Field** (#f7f4ef) and **Field Line** (#8c8780): form fields on stone; the edge measures 3.3:1.
- **Brick** (#a8321f): form errors only (5.3:1 on stone).

### Named Rules
**The Surface-Role Rule.** Components read `--surface`, `--text`, `--text-soft`, `--mark` and `--focus`, never raw colours. `.on-stone` and `.band` flip the roles, so a component never asks where it sits.

**The One Field Rule.** Saffron fills at most one large area per page: the contact band. Everywhere else it is a pill, a dot, an underline or a ring.

## Typography

**Display Font:** Amiri 700 (with Sahel, Times New Roman, serif)
**Body Font:** Sahel 400 and 700, the FD cut with Persian digits (with Tahoma, Segoe UI, sans-serif)

**Character:** a Naskh with real stroke contrast for what is said once and large, over a clear Persian sans for everything read or tapped. Tahoma is the fallback because every Windows and macOS has it and it sits close to Sahel, so the swap barely moves the text.

### Hierarchy
- **Display L** (Amiri 700, 44–76px, 1.25): the page's one `h1`.
- **Display M** (Amiri 700, 32–52px, 1.25): section heads.
- **Display S** (Amiri 700, 26–36px, 1.25): card titles, teacher names.
- **Lead** (Sahel 400, 20–24px, 1.7): the sentence under a page's headline.
- **Body** (Sahel 400, 18–20px, 1.85 on the ground and 1.8 on stone): running text, buttons, nav. Measure 36em, about 85 Persian characters.
- **Small** (Sahel 400, 16px): meta, captions, chips, small buttons.
- **Label** (Sahel 700, 14px): a short label above a heading or a group, in saffron on the ground and soft ink on stone.

### Named Rules
**The No-Tracking Rule.** Letter-spacing stays 0 at every size: tracking breaks the joins. Ethos's tracked uppercase eyebrows become short Sahel 700 labels.

**The Persian Digits Rule.** Numbers are Persian through the font (Sahel FD), never converted by hand; `tel:` links keep ASCII digits for the dialler.

## Layout

The ground shows round every panel by `--frame` (12–24px). A panel pads its content by `--panel-pad` (20–64px); panels and their content blocks are separated by `--section` (64–96px). Text inside a panel keeps to `--measure`.

Breakpoints are in em, so they follow the reader's font size: 56.25em (900px) swaps the navbar's links for «منو» and a round call button and stacks splits; 37.5em (600px) turns teacher and Programme rows into sideways rails with the next card peeking, pairs Instrument tiles and session tiles; 22.5em (360px) gives each Instrument tile a full row. Grids are `auto-fill` with `minmax(min(100%, …), 1fr)`, so nothing overflows between breakpoints.

RTL throughout: logical properties only (`inline-start`, `block-end`), and the next item in a rail or slideshow arrives from the left.

## Elevation & Depth

Flat by default. Depth comes from tone: stone panels on the ground, raised-ground tiles on the ground, a frame inside a panel. The one shadow is the floating sheet of a dropdown (`0 1.25rem 2.5rem -1rem rgb(0 0 0 / 0.55)`). The hero's photo carries a side and bottom scrim of the ground colour, held dark as far as the copy reaches.

**The Tone-Not-Shadow Rule.** A surface is lifted by changing its colour, not by casting a shadow; the dropdown is the only exception because it floats over content.

## Shapes

Exactly two radii: the panel's (20px on phones, 28px on desktop) and full round for pills. Anything nested in a panel takes the panel's radius minus its inset (`--radius-inner`, at least 12px), so corners stay concentric. Photos sit in `.frame`s with that nested radius and a light multiply of the ground, never a filter that changes faces.

The one shape from the subject is the santur's trapezoid body, cropped large off a corner at low contrast. It appears where a photo is missing and a picture is still wanted: the about panel, the Instrument page's type tile and notices. Instrument tiles without a photo are text alone.

**The Two-Radius Rule.** No 8–16px "soft" corner anywhere; it is a panel, something nested in one, or a pill.

## Components

### Buttons («Disc»)
- **Shape:** a 50px pill, label first, the icon in a 40px disc at the end (36px at the small size).
- **Primary:** saffron pill, ground disc with a saffron icon. On the saffron band it inverts: ground pill, saffron disc.
- **Secondary:** stone pill on the ground, an ink-tint pill on stone, with a dark disc.
- **Quiet:** text with a 2px saffron underline (deep saffron on stone) and a bare arrow that nudges 4px.
- **States:** on hover the arrow slides out leftwards and its twin slides in (260ms), the phone icon tilts −14°; press scales to 0.97 (120ms); focus is a 3px ring in `--focus`; `aria-busy` swaps the glyph for a spinner and blocks a second send.

### Panels, cards and tiles
- **Panel:** stone, `--radius-panel`, `--panel-pad`; a split panel puts text beside a framed photo and drops the media slot when there is none.
- **Programme card:** stone, its photos crossfading in a 3:2 frame, an age chip on the corner, the title as the link with the whole card as its target. With no photo the card is its text, set at the foot.
- **Instrument tile (RAM):** the name and a chevron, its photo flush to the far edge; text-only until a photo is uploaded.
- **Session tile:** raised ground, the days in bold («شنبه تا سه‌شنبه» when neighbouring days match), the hours, the teacher, what is taught.
- **Teacher card:** a square portrait (Amiri initials on a stone plate when missing), the name in Amiri, instruments in bold, one line of lineage, the days.

### Chips
- A 32px pill, Small type, the surface tinted 9% towards the text colour; on a photo, a saffron dot before the label.

### Inputs / Fields
- **Style:** field fill, a 1px field-line edge, `--radius-inner`, at least 52px tall and 16px text (no zoom on phones).
- **Focus:** a 2px ring in `--focus`, the edge turns ink.
- **Error:** a brick edge and inset line, the message under the field and in a summary that links each field.

### Navigation
- **Navbar:** a sticky ground pill floating 12px from the top: the saffron logo, five links (دوره‌ها and گالری open stone dropdowns that grow from their trigger), and the saffron call pill. The current page gets a saffron-deep dot. Under 900px: the logo, «منو» and a round saffron call button that never leaves the screen; «منو» opens a full-screen sheet.
- **Footer:** the address with the Neshan route, the phone answering hours, the two phones, a page list, the saffron logo across the width, then © and social links.

### The contact band
The one saffron field on a page: a headline and the two ways in (call, send a message). The facts live in the footer just below.

### «امروز در آموزشگاه»
A small dark pill in the hero's far corner (under the hero on phones), from the real timetable in Tehran time: before, during and after today's classes, and on closed days when the Academy opens next. Server-rendered; it links to the schedule.

## Do's and Don'ts

### Do:
- **Do** use the surface roles (`--surface`, `--text`, `--mark`, `--focus`) and let `.on-stone` flip them.
- **Do** hide a section that has no content (testimonials, FAQ, an empty album's grid) rather than show it empty.
- **Do** end every page with a way on: the band, a schedule link, or back up a level.
- **Do** keep motion on `transform` and `opacity` (plus `clip-path` for the day strike), on the motion tokens, with reduced motion zeroing everything that travels.
- **Do** write Persian copy only from real facts, with the owner's approval.

### Don't:
- **Don't** letter-space Persian, or set Amiri below Display S.
- **Don't** add a third radius, a second saffron field on one page, or saffron text on stone.
- **Don't** draw the santur as a pattern or on the dark ground; it stands in for a missing picture only.
- **Don't** hide content until a script or an observer reveals it.
- **Don't** invent testimonials, counts, awards or claims, or show prices or booking.
