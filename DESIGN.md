---
name: Aramesh Music Academy
description: The Academy's printed programme, set in Amiri on cool paper sheets laid over a green-black ground.
colors:
  ground: "#12201b"
  on-ground: "#e4e7df"
  on-ground-soft: "#b9c1b7"
  paper: "#e9ece5"
  paper-struck: "#dde2da"
  ink: "#12201b"
  ink-soft: "#45524c"
  rule: "#d3d8cf"
  jade: "#0e7a64"
  jade-lifted: "#3fb393"
  on-jade: "#ffffff"
  field: "#ffffff"
  error-red: "#9a2f1d"
typography:
  display:
    fontFamily: "Amiri, Noto Naskh Arabic, Times New Roman, serif"
    fontSize: "clamp(2.75rem, 1.4rem + 5vw, 5rem)"
    fontWeight: 700
    lineHeight: 1.2
  headline:
    fontFamily: "Amiri, Noto Naskh Arabic, Times New Roman, serif"
    fontSize: "clamp(2.125rem, 1.5rem + 1.8vw, 3rem)"
    fontWeight: 700
    lineHeight: 1.2
  title:
    fontFamily: "Amiri, Noto Naskh Arabic, Times New Roman, serif"
    fontSize: "clamp(1.375rem, 1.25rem + 0.5vw, 1.6875rem)"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "Amiri, Noto Naskh Arabic, Times New Roman, serif"
    fontSize: "1.3125rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Amiri, Noto Naskh Arabic, Times New Roman, serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  none: "0"
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
  margin: "clamp(1rem, 3.3vw, 3rem)"
  gutter: "clamp(0.75rem, 1.7vw, 1.5rem)"
  section: "clamp(6rem, 11vw, 10rem)"
  sheet-pad: "clamp(1.25rem, 3.9vw, 3.5rem)"
components:
  button-call:
    backgroundColor: "{colors.jade}"
    textColor: "{colors.on-jade}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    padding: "0.55em 1.3em 0.65em"
    height: "3rem"
  button-paper:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    padding: "0.55em 1.3em 0.65em"
    height: "3rem"
  button-paper-hover:
    backgroundColor: "{colors.paper-struck}"
  sheet:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "{spacing.sheet-pad}"
  day-tab:
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
  day-tab-struck:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  field:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.5rem 0.75rem"
    height: "3rem"
  photo-plate-empty:
    backgroundColor: "{colors.paper-struck}"
    textColor: "{colors.ink-soft}"
---

# Design System: Aramesh Music Academy

## Overview

**Creative North Star: "The Programme" (برنامه)**

The site is the Academy's own printed programme: sheets of cool paper laid on a deep green-black ground, listing who teaches this week, when, and on which instruments. The references are the *Golha* radio listings and 1960s–70s Tehran concert programmes, which set time, performer and instrument in plain columns and let the typesetting carry the dignity. Every page is a sheet or a set of sheets. Structure comes from the 12-column grid and the paper's edge, never from boxes, cards or ornament.

The world is quiet on purpose: آرامش means calm. Hierarchy comes from one Naskh family at two weights and five sizes, and from colour changes by whole chapters. A section turns to paper or stays on the ground; accents are never sprinkled across a neutral page. Imagery goes through one darkroom process (monochrome on paper), so the admin's mixed phone snapshots read as one commissioned set.

Motion is "printed paper, handled". The struck day slides, photos develop out of the paper tone, sheets are set down once on load, and later sections settle as they scroll in. Everything is short and ease-out, nothing is hidden without JavaScript, and reduced motion keeps only short fades.

**Key Characteristics:**
- Dark ground, paper sheets, one jade action.
- One typeface (Amiri) at 400 and 700, set large, right to left.
- Square corners everywhere: paper is cut, not rounded.
- Every photo in monochrome, at the ratio the upload pipeline gives it.
- The live schedule (the struck day) is the signature, built only from real ClassSession data.

## Colors

Five colours, each with only the lighter or darker steps it needs for contrast: green-black, cool paper, jade, white, and an error red.

### Primary
- **Wordmark Jade** (#0e7a64): the call to action (the tap-to-call button and the phone bar) and focus rings on paper. Taken from the Academy's teal Nastaliq wordmark. White on jade is 5.3:1.
- **Jade Lifted for Night** (#3fb393): the same jade lifted to 6.5:1 for focus rings on the dark ground. Never used as a fill.

### Neutral
- **Green-Black Ground** (#12201b): the page itself, header and footer. It doubles as **Ink** on paper (14.1:1).
- **Moonlit Text** (#e4e7df): text on the ground (13.5:1).
- **Soft Moonlit Text** (#b9c1b7): meta, captions and counts on the ground (9.1:1).
- **Cool Paper** (#e9ece5): every sheet. It is cool, not cream; cream would read as nostalgic wedding stationery.
- **Struck Paper** (#dde2da): a struck row, today's schedule column, and the empty photo plate behind a loading or missing image.
- **Soft Ink** (#45524c): secondary text on paper (6.9:1; 6.2:1 on Struck Paper).
- **Rule** (#d3d8cf): the one hairline, between schedule and performer rows.
- **Field White** (#ffffff): form fields on paper, and text on jade.
- **Error Red** (#9a2f1d): form errors only, on paper (6.3:1).

### Named Rules
**The Chapter Rule.** Colour changes by whole chapters. A section is either paper or ground, and a sheet flips the surface, text and focus roles together, so a component never asks where it sits.

**The One Voice Rule.** Jade marks the call to action and focus, nothing else. If a page shows jade in more than one call, one of them is wrong.

## Typography

**Display Font:** Amiri (with Noto Naskh Arabic, Times New Roman, serif)
**Body Font:** Amiri, the same family
**Label Font:** Amiri, the same family

**Character:** one Naskh family with real stroke contrast, set the way a programme is typeset: in one face, with size and weight doing all the work. Amiri ships only 400 and 700, so there is no 600. Its small x-height reads about a size below a sans at the same pixel size, so everything runs large.

The fonts are self-hosted woff2 files, subset into a Persian file (about 43 KB per weight) and a Latin file, with `font-display: swap`. Phones, times and other numbers use Latin digits; the street address keeps its Persian digits.

### Hierarchy
- **Display** (700, 44–80px fluid, 1.2): the page's single `h1`.
- **Headline** (700, 34–48px fluid, 1.2): section heads and performer names on the teachers page.
- **Title** (700, 22–27px fluid, 1.2): leads, names in the programme, buttons.
- **Body** (400, 21px, 1.6): running text, set to a 34em measure.
- **Label** (400 or 700, 18px): captions, meta, times, form labels, counts.

### Named Rules
**The Two Weights Rule.** Hierarchy uses 400 and 700 only. Never fake a middle weight or add a second family.

**The Tall Letters Rule.** Headings keep 1.2 leading. Amiri's alef-madda and deep descenders collide at 1.0.

## Layout

- **The grid:** one 12-column grid with a fluid gutter (12–24px) inside a fluid outer margin (16–48px). Every section places its parts on that grid. Below 56.25em the grid collapses to a single column, and each phone layout is designed for the phone rather than squeezed.
- **Rhythm:** chapters are 96–160px apart (the `section` step). Inside a sheet, the padding runs 20–56px.
- **Breakpoints:** two: 37.5em (600px) for small adjustments, and 56.25em / 56.3125em (900px) for the main switch between phone and desktop.
- **Direction:** everything starts on the right. Logical properties are used throughout, so nothing is mirrored by hand. "Forward" arrows point left.
- **Header:** not sticky; paper doesn't follow you around. On the phone, a fixed bottom bar carries the call and route actions instead.

## Elevation & Depth

The system is flat. Depth comes from the paper/ground contrast and from a sheet's punched tear-off edge, not from shadows. The one shadow belongs to the gallery dropdown, which really does float over the page.

### Shadow Vocabulary
- **Floating sheet** (`box-shadow: 0 1.25rem 2.5rem -1rem rgb(0 0 0 / 0.55)`): the gallery menu panel only.

### Named Rules
**The Flat Paper Rule.** Surfaces at rest have no shadow. If something isn't floating over other content, it has no shadow.

## Shapes

- **Corners:** square everywhere (radius 0). That includes buttons, fields, sheets, photos, focus rings and dialogs.
- **The tear:** one sheet per page at most may carry the punched tear-off edge at its foot, 10px of half-circle perforation in paper colour.
- **Rules:** a single hairline in the Rule colour separates rows. There are no outlined boxes and no card borders.

## Components

### Buttons
Pressed like a key: square, solid, no outline.
- **Shape:** square (0).
- **Call** (jade): white text on Wordmark Jade, 700 at Title size, at least 48px tall. It is the only primary action.
- **Paper:** ink text on Cool Paper. It is used on the ground for secondary actions such as the route link, and turns to Struck Paper on hover.
- **States:** on press it scales to 0.97 over 120ms. Hover darkens jade by 14%, and only on devices that can hover. Focus shows a 3px jade ring with a 3px offset.

### Sheets
- **Background:** Cool Paper with Ink text, flipping the surface roles for everything inside.
- **Padding:** 20–56px, fluid.
- **Edge:** square, with an optional torn foot (see Shapes). There is no border and no shadow.

### Day tabs and the programme (signature)
All seven days always sit in one row. The chosen day is struck forward: an ink block slides between days over 220ms with ease-in-out, drawn as a clipped ink copy of the tab row, so the colour change is exact. Friday stays visible, marked تعطیل (closed). Below the tabs, the programme lists time, teacher (as a link) and instruments in measured columns, and the rows fade over 140ms when the day changes. The arrow keys follow RTL (← is the next day), and Home and End jump to the ends. On the phone the day names shorten to their first letter.

### Fields
- **Style:** Field White on paper, a 1px Soft Ink border, square, at least 48px tall, Latin fields aligned to the right edge.
- **Focus:** a 2px jade outline with the border turning jade.
- **Error:** a red border plus a 1px inset, a 700 red message under the field, and a summary block with a 4px red start border that takes focus.

### Photo plates
Every image is printed in monochrome (grayscale with 1.06 contrast) on a Struck Paper plate at its pipeline ratio: portraits 1:1, covers 3:2, gallery photos at their own ratio in balanced columns. An image that is still loading develops out of the paper tone over 600ms, once. A missing portrait shows the person's initials in Soft Ink on the plate. On hover, a gallery plate lifts its brightness slightly.

### Navigation
The wordmark sits at the start, then the pages, with the phone number at the end. The current page is underlined at 2px, and hover underlines at 1px. The gallery is a disclosure opening a floating sheet of categories and their albums, and Escape closes it. On the phone, a full-screen menu on the ground opens from «منو», closes with Escape, and returns focus to its toggle.

### Lightbox
A full-screen frame on the ground. The photo follows the finger on swipe, decides on distance or velocity, and springs back otherwise; the spring is 560ms with 1.5% overshoot. The arrow keys move between photos, Escape closes it, and focus returns to the photo that opened it.

## Do's and Don'ts

### Do:
- **Do** put content on a paper sheet or directly on the ground; pick one per section.
- **Do** keep jade for the call and focus only.
- **Do** set text sizes from the five type steps and gaps from the space scale. The exceptions are a few fluid display sizes that work like pictures (the initials on a portrait plate, the 404 numeral, a single long letter, the hero's «امروز در آموزشگاه» title, and the names in the home teacher plates); keep them within the Headline-to-Display range.
- **Do** show every photo in monochrome at the ratio the upload pipeline gives it, with the initials plate as the fallback.
- **Do** keep motion short and ease-out (120–220ms for UI) and interruptible. Anything that travels uses transform or opacity. Hover and state changes may fade colour or filter, and the struck day uses clip-path. Reduced motion keeps short fades.
- **Do** keep all seven days visible wherever the week appears.

### Don't:
- **Don't** round a corner, outline a box, or add a card border.
- **Don't** add a shadow to anything that doesn't float.
- **Don't** introduce a second typeface or a weight other than 400 and 700.
- **Don't** add AOS-style fade-ups, or hide content until JavaScript runs.
- **Don't** use emoji anywhere in templates.
- **Don't** load fonts, icons or scripts from a CDN; everything is self-hosted for when Iran's internet is cut.
