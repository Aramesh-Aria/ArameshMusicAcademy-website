# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Primary:** parents researching music lessons for their children. They're comparing academies, often on a phone, and want to know who would teach their child, when classes run, and how to get in touch.
- **Secondary:** adult learners choosing an instrument or a teacher for themselves.

The site calls both of them the **Visitor** (see `CONTEXT.md`).

## Product Purpose

An informational site for آموزشگاه موسیقی آرامش (Aramesh Music Academy) in Tehran. Success is a **Conversion**: the Visitor contacts the Academy by the form, by phone or by visiting in person. Online enrollment, payment, student accounts and portals are out of scope by design.

## Positioning

- **Persian classical heritage.** The Academy is led by مسعود آرامش, a santur player and composer with more than 40 years of activity. It is strong in Persian classical instruments and voice (سنتور، تار، سه‌تار، تنبک، دف، آواز ایرانی), and also teaches piano, violin, guitar, accordion, hang drum, cajón and children's music.
- **A calm, personal atmosphere.** True to its name (آرامش means calm), it's a quiet, personal place rather than a large institute.

## Operating Context

- **Content:** staff manage all content in the Django admin (Jazzmin): teachers, instruments, the weekly ClassSession schedule, gallery pages, images and videos, testimonials, and page text for home, about and schedule.
- **Images:** admin uploads of unpredictable quality, resized on save (portraits 1:1 at 600, covers 3:2 at 900, page heroes 3:2 at 1200, gallery images inside 1920 at their original ratio, mostly portrait 3:4 today).
- **Network:** Visitors are in Iran, where Google services and YouTube are often filtered or slow. The Google Maps embed stays, with a Neshan link as a backup. Videos come from Aparat or YouTube.

## Capabilities and Constraints

- **Stack:** Django 5.2 server-rendered templates, Persian RTL (`lang="fa" dir="rtl"`), plain CSS and small vanilla JS. No frontend build step. Static files go through `collectstatic` into the committed `public/static/`, served by WhiteNoise.
- **Backend is the source of truth.** Models, URL names, view context keys and form fields stay as they are unless a change is approved.
- **Numbers:** phones, times and numbers stay in Latin digits.
- **Gallery:** exactly two levels, category then album.
- **Contact form:** django-simple-captcha protects it. A mail failure never blocks the Visitor.

## Brand Commitments

- **Name:** آموزشگاه موسیقی آرامش.
- **Voice:** warm and respectful. Polite «شما», plain-spoken, like a teacher talking to a parent at the front desk. Not salesy and not stiffly formal.

## Evidence on Hand

- **Live content** (aramesh-academy.ir): 11 teachers with real bios (two are empty today), the weekly schedule, About text, and 13 photos of the Academy's space.
- **Coming:**
  - The Academy holds student concerts, so concert photos and videos will join the gallery.
  - Better photos can be uploaded once the design shows what's needed.
  - Real parent testimonials will be collected.
- **Never fabricate** testimonials, student counts, awards or other claims. Until real quotes exist, the testimonial section must look complete with zero or one quote.

## Product Principles

1. **Every page leads calmly toward contact.** A phone number, the address, opening hours or the form is always within reach, and never pushed.
2. **Teachers are the proof.** Parents choose a person, so teachers and their instruments get the most care.
3. **Heritage, lived in, not decorated.** The Persian classical tradition shows through real instruments, people and concerts, not ornamental clichés.
4. **Built for the content the admin actually provides:** empty bios, missing photos, any image ratio, no testimonials.

## Accessibility & Inclusion

- WCAG AA contrast and full keyboard navigation with visible focus.
- Labeled form fields.
- Correct RTL behavior, with a reading experience designed for Persian text.
