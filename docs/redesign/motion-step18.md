# Step 18: `/review-animations` and `/animation-performance`

Run on 2026-10-27 over all motion in `static_dev/assets/css/site.css` and `static_dev/assets/js/site.js`, against the
skills' `STANDARDS.md`. Frame timings were measured on the `DEBUG=False` server in Playwright's Chromium with the CPU
throttled 4× (a desktop stand-in for a mid-range phone's CPU, not its GPU).

## Review: findings table

| Before | After | Why |
| --- | --- | --- |
| `.crossfade > img` and `.card .frame img`: `opacity var(--dur-fade) ease-in-out` (`site.css:480`, `:541`) | `opacity var(--dur-fade) var(--ease-fade)`, a new token `cubic-bezier(0.37, 0, 0.63, 1)` (sine in-out) | Built-in easings are too weak to be a decision. The strong `--ease-in-out` would make a 1.2s photo fade lurch in its middle; a sine curve lets the incoming photo arrive evenly over the opaque outgoing one. |
| `.hero__titles > span`: `opacity 400ms var(--ease-out)` (`site.css:1328`) | `opacity var(--dur-move) var(--ease-out)` (260ms) | Over the 300ms UI budget with no reason, and a literal outside the token set. |
| `::view-transition-old/new(root)`: `200ms ease` (`site.css:1664`) | `var(--dur-state) var(--ease-out)` (160ms; 80ms under reduced motion) | Built-in `ease` on a page swap, and a literal. The page crossfade is opacity only, so reduced motion keeps a short beat of it. |

## Verdict

**Performance.** `.accordion details::details-content` animates `block-size` (`site.css:948`), a layout property. Kept: it
is the only way to open a disclosure without scaling its text, it plays on a rare, deliberate click, and the FAQ is
short. The field's `border-color` (`site.css:1007`) repaints one input on focus; a state change, not continuous motion.

**Interruptibility and timing.** Correct as built: the day-tab strike is a `clip-path` transition that retargets mid-way,
and arrow keys skip it (no motion on a keyboard action); the lightbox swipe follows the finger with `transform` written
straight to the image and settles on a sampled spring that a new touch cancels; the menu sheet opens at 260ms and the
lightbox closes faster than it opens.

**Origin and cohesion.** The dropdown grows from its trigger (`transform-origin: top right`, from `scale(0.97)`), nothing
starts from `scale(0)`, and the slow motion (1.2s crossfades, the 600ms photo zoom on hover, the 70s marquee) is all
ambient content, never an answer to a hand.

**Accessibility.** Reduced motion zeroes every travelling duration, keeps short fades, stops the hero from cycling and
lays the marquee out still; every hover effect sits inside `@media (hover: hover) and (pointer: fine)`. The button's
busy spinner keeps turning under reduced motion: it is status, not decoration.

**Approve** after the three fixes above.

## Performance: inventory and causes

| Element | Driver | Properties | Plays during |
| --- | --- | --- | --- |
| Hero and Programme card crossfades | CSS transition | `opacity` | idle, after `load` (photos fetched a turn ahead) |
| Hero bar clock | CSS keyframes | `transform: scaleX` | idle |
| Card, teacher and album hover zoom | CSS transition | `transform` | hover |
| Presses (buttons, cards, tiles) | CSS transition | `transform`, `background-color` | press |
| Marquee | CSS keyframes | `transform`, paused off screen | idle |
| Dropdown, menu sheet, lightbox | CSS transition, `@starting-style` | `opacity`, `transform` | click |
| Day-tab strike | CSS transition | `clip-path` | click |
| Lightbox swipe | pointer events + WAAPI | `transform`, `opacity` | drag |
| Page navigation | View Transitions | `opacity`, group `transform` | navigation (browser-driven, off the main thread) |
| FAQ accordion | CSS transition | `block-size` | click |

No `transition: all`, no animated CSS variable, no animated `blur()`, no `will-change` (none needed), no state written per
frame. The only layout property is the accordion, kept above.

Measured at 4× CPU, 1440 wide (hero, hover) and 390 (schedule, menu):

| Motion | Frames | p50 | p95 | Worst | Over 33ms |
| --- | --- | --- | --- | --- | --- |
| Hero crossfade, 8s across a slide change | 481 | 16.7ms | 17.6ms | 17.7ms | 0 |
| Programme card hover zoom | 91 | 16.7 | 17.5 | 17.6 | 0 |
| Day-tab strike, two clicks | 92 | 16.7 | 17.5 | 17.7 | 0 |
| Menu sheet open | 62 | 16.7 | 17.6 | 17.7 | 0 |

Verified from code and a throttled desktop recording; a 120Hz phone over remote debugging was not available.
