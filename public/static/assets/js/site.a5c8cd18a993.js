/*
  Aramesh Music Academy: small vanilla modules, loaded with defer.
  Each one does nothing when its markup is absent, and every page reads fine without this file.
*/

// Motion tokens from site.css, so scripted motion keeps the same curves and honours reduced motion.
const motion = {
  ms: (name) => parseFloat(getComputedStyle(document.documentElement).getPropertyValue(name)) || 0,
  ease: (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim() || 'ease-out',
};

// Right to left, the next item lies to the left: ArrowLeft steps forward, ArrowRight back.
const arrowStep = { ArrowLeft: 1, ArrowRight: -1 };

// iOS Safari applies :active on touch only when a touchstart listener exists; this one lets every press state show.
document.addEventListener('touchstart', () => {}, { passive: true });

// Phone menu: a modal <dialog>, so the browser holds focus inside it and Escape closes it.
(() => {
  const menu = document.getElementById('site-menu');
  const openers = document.querySelectorAll('[data-menu-open]');
  if (!menu || typeof menu.showModal !== 'function' || !openers.length) return;

  let opener = null;
  const setExpanded = (value) => openers.forEach((el) => el.setAttribute('aria-expanded', value));

  openers.forEach((el) => {
    el.hidden = false;
    el.addEventListener('click', () => {
      opener = el;
      menu.showModal();
      setExpanded('true');
    });
  });

  menu.addEventListener('close', () => {
    setExpanded('false');
    opener?.focus();
  });
  menu.querySelectorAll('[data-menu-close]').forEach((el) => el.addEventListener('click', () => menu.close()));

  // Following a link to the page already shown would leave the sheet over it.
  menu.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (link && link.pathname === location.pathname && link.hash === '') menu.close();
  });

  // Rotating a tablet into the desktop layout closes the sheet.
  matchMedia('(min-width: 56.3125em)').addEventListener('change', (event) => {
    if (event.matches && menu.open) menu.close();
  });
})();

// The week (`[data-week]`): day tabs over the day panels. Without JS every day shows under its own heading.
(() => {
  document.querySelectorAll('[data-week]').forEach((week) => {
    const tablist = week.querySelector('[data-week-tabs]');
    if (!tablist) return;
    const tabs = [...tablist.querySelectorAll('[role="tab"]')];
    const title = week.querySelector('[data-week-title]');
    // Each day becomes a tab panel, labelled by its tab instead of its own heading.
    tabs.forEach((tab) => {
      const panel = document.getElementById(tab.getAttribute('aria-controls'));
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
      panel.querySelector('.day-heading').hidden = true;
    });
    week.classList.add('is-tabbed');

    // The struck day: an ink copy of the tabs, clipped to the selected one. Moving the clip moves the
    // fill and the stone-coloured label together, so the block slides instead of jumping.
    const struck = tablist.cloneNode(true);
    struck.removeAttribute('role');
    struck.removeAttribute('aria-labelledby');
    struck.removeAttribute('data-week-tabs');
    struck.setAttribute('aria-hidden', 'true');
    struck.inert = true;
    struck.className += ' days-struck';
    struck.querySelectorAll('[id]').forEach((el) => el.removeAttribute('id'));
    struck.querySelectorAll('button').forEach((el) => {
      ['role', 'aria-controls', 'aria-selected', 'aria-label'].forEach((a) => el.removeAttribute(a));
      el.tabIndex = -1;
    });
    tablist.append(struck);

    const strike = (tab) => {
      const list = tablist.getBoundingClientRect();
      const box = tab.getBoundingClientRect();
      struck.style.clipPath = `inset(${box.top - list.top}px ${list.right - box.right}px ${list.bottom - box.bottom}px ${box.left - list.left}px)`;
    };
    const current = () => tabs.find((t) => t.getAttribute('aria-selected') === 'true');
    // First placement is instant; only later changes travel.
    strike(current());
    requestAnimationFrame(() => struck.classList.add('is-ready'));
    // A resize (or the short-label switch) re-places the block at once rather than letting it trail behind.
    new ResizeObserver(() => {
      const ready = struck.classList.contains('is-ready');
      struck.classList.remove('is-ready');
      strike(current());
      if (ready) requestAnimationFrame(() => struck.classList.add('is-ready'));
    }).observe(tablist);

    const show = (tab) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute('aria-selected', on);
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (title) title.textContent = tab.hasAttribute('data-today') ? 'امروز در آموزشگاه' : `${tab.dataset.label} در آموزشگاه`;
    };
    show(current());

    const select = (tab, focus) => {
      show(tab);
      // Arrow keys move the block and swap the day at once; only a click or tap slides and fades.
      struck.classList.toggle('is-ready', !focus);
      week.classList.toggle('is-swapping', !focus);
      strike(tab);
      if (focus) tab.focus();
    };

    tablist.addEventListener('click', (event) => {
      const tab = event.target.closest('[role="tab"]');
      if (tab) select(tab, false);
    });

    // A pressed tab shrinks; its ink twin shrinks with it, since that is the label the visitor sees.
    const twins = [...struck.querySelectorAll('button')];
    tablist.addEventListener('pointerdown', (event) => {
      const twin = twins[tabs.indexOf(event.target.closest('[role="tab"]'))];
      if (!twin) return;
      twin.classList.add('is-pressed');
      // Whichever ends the press, up or cancel, removes both listeners.
      const press = new AbortController();
      const release = () => { twin.classList.remove('is-pressed'); press.abort(); };
      addEventListener('pointerup', release, { signal: press.signal });
      addEventListener('pointercancel', release, { signal: press.signal });
    });

    tablist.addEventListener('keydown', (event) => {
      const i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      const next = event.key in arrowStep ? i + arrowStep[event.key] : { Home: 0, End: tabs.length - 1 }[event.key];
      if (next === undefined) return;
      event.preventDefault();
      select(tabs[(next + tabs.length) % tabs.length], true);
    });
  });
})();

// Disclosure menus (<details data-disclosure>): Escape, an outside click, or focus leaving closes them.
(() => {
  const disclosures = [...document.querySelectorAll('details[data-disclosure]')];
  if (!disclosures.length) return;

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    disclosures.forEach((d) => {
      if (!d.open) return;
      d.open = false;
      d.querySelector('summary').focus();
    });
  });

  document.addEventListener('click', (event) => {
    disclosures.forEach((d) => {
      if (d.open && !d.contains(event.target)) d.open = false;
    });
  });

  disclosures.forEach((d) => {
    d.addEventListener('focusout', (event) => {
      if (d.open && event.relatedTarget && !d.contains(event.relatedTarget)) d.open = false;
    });
  });
})();

// Lightbox: links with `data-lightbox="<group>"` open their photo in a modal <dialog>. Without JS they open the file.
(() => {
  const links = [...document.querySelectorAll('a[data-lightbox]')];
  const box = document.createElement('dialog');
  if (!links.length || typeof box.showModal !== 'function') return;

  const icon = (id) => `<svg class="icon" aria-hidden="true"><use href="#${id}"></use></svg>`;
  box.className = 'lightbox';
  box.setAttribute('aria-label', 'تصویر');
  box.innerHTML = `
    <div class="lightbox-bar">
      <p class="lightbox-count num ltr" aria-live="polite"></p>
      <button type="button" class="lightbox-close" data-close>${icon('i-close')}بستن</button>
    </div>
    <div class="lightbox-stage"><img alt=""></div>
    <div class="lightbox-foot">
      <p class="lightbox-caption"></p>
      <div class="lightbox-nav">
        <button type="button" class="lightbox-prev" aria-label="تصویر قبلی">${icon('i-chevron')}</button>
        <button type="button" class="lightbox-next" aria-label="تصویر بعدی">${icon('i-chevron')}</button>
      </div>
    </div>`;
  document.body.append(box);

  const img = box.querySelector('img');
  const count = box.querySelector('.lightbox-count');
  const caption = box.querySelector('.lightbox-caption');
  const nav = box.querySelector('.lightbox-nav');
  let group = [];
  let index = 0;

  const show = (i, fade = true) => {
    index = (i + group.length) % group.length;
    const link = group[index];
    const thumb = link.querySelector('img');
    if (fade) img.classList.add('is-loading');
    img.onload = img.onerror = () => img.classList.remove('is-loading');
    img.src = link.href;
    img.alt = thumb?.alt || '';
    caption.textContent = link.dataset.caption || '';
    count.textContent = group.length > 1 ? `${index + 1} / ${group.length}` : '';
  };

  links.forEach((link) => link.addEventListener('click', (event) => {
    event.preventDefault();
    group = links.filter((l) => l.dataset.lightbox === link.dataset.lightbox);
    nav.hidden = group.length < 2;
    show(group.indexOf(link));
    box.showModal();
  }));

  // Focus returns to the photo last shown, so the visitor picks up where they stopped.
  box.addEventListener('close', () => group[index]?.focus());
  box.querySelector('[data-close]').addEventListener('click', () => box.close());
  box.querySelector('.lightbox-next').addEventListener('click', () => show(index + 1));
  box.querySelector('.lightbox-prev').addEventListener('click', () => show(index - 1));

  box.addEventListener('keydown', (event) => {
    const step = arrowStep[event.key];
    if (!step || group.length < 2) return;
    event.preventDefault();
    show(index + step);
  });

  // A tap on the dark ground around the photo closes it.
  box.querySelector('.lightbox-stage').addEventListener('click', (event) => {
    if (event.target !== img) box.close();
  });

  // Swipe: the photo follows the finger. A drag past 50px or a flick swaps it, otherwise it springs back.
  // In RTL the next photo lies to the left, so a drag to the right brings it in.
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let drag = null;
  let swapping = false;

  const settle = (dx) => img.animate(
    [{ transform: `translateX(${dx}px)` }, { transform: 'none' }],
    { duration: motion.ms('--dur-spring'), easing: motion.ease('--ease-spring') },
  );

  const swap = async (dx) => {
    swapping = true;
    try {
      const step = dx > 0 ? 1 : -1;
      const next = group[(index + step + group.length) % group.length];
      const preload = new Image();
      preload.src = next.href;
      const out = img.animate(
        [{ transform: `translateX(${dx}px)` }, { transform: `translateX(${dx > 0 ? 60 : -60}%)`, opacity: 0 }],
        { duration: motion.ms('--dur-swap'), easing: motion.ease('--ease-out'), fill: 'forwards' },
      );
      await Promise.all([out.finished, preload.decode().catch(() => {})]);
      show(index + step, false);
      out.cancel();
      img.animate(
        [{ transform: `translateX(${dx > 0 ? -30 : 30}%)`, opacity: 0 }, { transform: 'none', opacity: 1 }],
        { duration: motion.ms('--dur-move'), easing: motion.ease('--ease-out') },
      );
    } finally {
      swapping = false;
    }
  };

  img.addEventListener('pointerdown', (event) => {
    // One finger only: a second one (a pinch) or a swipe during a swap is left alone.
    if (group.length < 2 || drag || swapping || !event.isPrimary) return;
    // Caught mid spring-back: stop it and carry on from where the photo is now, not from the centre.
    const caught = new DOMMatrix(getComputedStyle(img).transform).m41;
    img.getAnimations().forEach((animation) => animation.cancel());
    drag = { id: event.pointerId, x: event.clientX - caught, y: event.clientY, t: event.timeStamp, dx: caught, live: false };
    if (caught) img.style.transform = `translateX(${caught}px)`;
  });
  img.addEventListener('pointermove', (event) => {
    if (drag?.id !== event.pointerId) return;
    drag.dx = event.clientX - drag.x;
    const dy = event.clientY - drag.y;
    if (!drag.live && Math.abs(drag.dx) > 6 && Math.abs(drag.dx) > Math.abs(dy)) {
      drag.live = true;
      img.setPointerCapture(event.pointerId);
    }
    if (drag.live && !reduce.matches) img.style.transform = `translateX(${drag.dx}px)`;
  });
  img.addEventListener('pointerup', (event) => {
    if (drag?.id !== event.pointerId) return;
    const { dx, t, live } = drag;
    drag = null;
    img.style.transform = '';
    // A photo caught mid spring-back and let go without a drag finishes springing back.
    if (!live) { if (dx && !reduce.matches) settle(dx); return; }
    const flick = Math.abs(dx) / Math.max(event.timeStamp - t, 1) > 0.11;
    if (Math.abs(dx) >= 50 || flick) {
      if (reduce.matches) show(index + (dx > 0 ? 1 : -1));
      else swap(dx);
    } else if (!reduce.matches) {
      settle(dx);
    }
  });
  img.addEventListener('pointercancel', (event) => {
    if (drag?.id !== event.pointerId) return;
    if (drag.live && !reduce.matches) settle(drag.dx);
    drag = null;
    img.style.transform = '';
  });
  img.draggable = false;
})();

// Video facade: a poster link (`data-video`) becomes the YouTube or Aparat player only when clicked,
// so no third-party frame loads with the page. Without JS the link opens the video on its own site.
(() => {
  document.addEventListener('click', (event) => {
    const poster = event.target.closest('a[data-video]');
    if (!poster || event.metaKey || event.ctrlKey || event.shiftKey) return;
    event.preventDefault();

    const src = new URL(poster.dataset.video);
    if (poster.dataset.videoPlatform === 'youtube') src.searchParams.set('autoplay', '1');
    const frame = document.createElement('iframe');
    frame.src = src;
    frame.title = poster.querySelector('.video-poster-title')?.textContent || '';
    frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    // The player paints a moment after it is inserted; it fades in from the frame instead of flashing.
    frame.classList.add('is-loading');
    const reveal = () => frame.classList.remove('is-loading');
    frame.addEventListener('load', reveal, { once: true });
    setTimeout(reveal, 1500);
    poster.replaceWith(frame);
    frame.focus();
  });
})();

// Forms: the error summary takes focus after a failed submit, the submit button shows it is sending (and a
// second press can't send twice), and the captcha can ask for a new image.
(() => {
  document.querySelector('[data-form-summary]')?.focus();

  document.querySelectorAll('form').forEach((form) => {
    const button = form.querySelector('button[type="submit"][data-busy-label]');
    if (!button) return;
    const label = button.querySelector('.btn__label');
    const idle = label.textContent;
    form.addEventListener('submit', (event) => {
      if (button.getAttribute('aria-busy') === 'true') {
        event.preventDefault();
        return;
      }
      button.setAttribute('aria-busy', 'true');
      label.textContent = button.dataset.busyLabel;
    });
    // Coming back to the page from the history restores it as it was left: idle again.
    addEventListener('pageshow', () => {
      button.removeAttribute('aria-busy');
      label.textContent = idle;
    });
  });

  document.querySelectorAll('[data-captcha-refresh]').forEach((button) => {
    const field = button.closest('.field');
    const image = field.querySelector('[data-captcha-image]');
    const key = field.querySelector('input[type="hidden"]');
    const answer = field.querySelector('input:not([type="hidden"])');
    button.hidden = false;

    button.addEventListener('click', async () => {
      button.disabled = true;
      try {
        const response = await fetch(button.dataset.captchaRefresh, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
        if (!response.ok) return;
        const data = await response.json();
        image.src = data.image_url;
        key.value = data.key;
        answer.value = '';
        answer.focus();
      } finally {
        button.disabled = false;
      }
    });
  });
})();

// A stacked photo waiting in `data-src` (the template gives a src to the first only, since "lazy" would still
// fetch the hidden ones lying in view) gets its file, and its smaller copies from `data-srcset`.
const fetchPhoto = (photo) => {
  if (!photo.dataset.src) return;
  if (photo.dataset.srcset) {
    photo.srcset = photo.dataset.srcset;
    delete photo.dataset.srcset;
  }
  photo.src = photo.dataset.src;
  delete photo.dataset.src;
};

// Crossfade (`.crossfade`): show photo `index` of a stack. The outgoing photo is held opaque under the incoming
// one until the fade has covered it (see site.css), then let go.
const crossfadeTo = (stack, index) => {
  const photos = [...stack.children];
  // Before the first turn the first photo shows by default, so it is the one leaving.
  const leaving = photos.find((photo) => photo.classList.contains('is-active')) || photos[0];
  const next = photos[index % photos.length];
  stack.setAttribute('data-cycling', '');
  fetchPhoto(next);
  // Fetch the photo after this one too, so it has arrived before its turn; on the first turn, not until the
  // page has loaded, so it never competes with the first photo.
  const after = photos[(index + 1) % photos.length];
  if (document.readyState === 'complete') fetchPhoto(after);
  else addEventListener('load', () => fetchPhoto(after), { once: true });
  if (leaving === next) { next.classList.add('is-active'); return; }
  photos.forEach((photo) => photo.classList.remove('is-leaving'));
  leaving.classList.remove('is-active');
  leaving.classList.add('is-leaving');
  setTimeout(() => leaving.classList.remove('is-leaving'), motion.ms('--dur-fade'));
  next.classList.add('is-active');
};

// Home hero (`[data-hero]`): the rooms' photos take turns. The active bar's fill animation is the clock, so
// hover, focus inside the hero, the hero leaving the screen or the tab hiding all pause it where it is.
// Reduced motion keeps the first photo and shows no bars.
(() => {
  const hero = document.querySelector('[data-hero]');
  const stack = hero?.querySelector('.hero__slides');
  if (!stack || stack.children.length < 2 || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const titles = [...hero.querySelectorAll('.hero__titles > span')];
  const bars = [...hero.querySelectorAll('.hero__bar')];
  let current = 0;

  const show = (index) => {
    current = index % bars.length;
    crossfadeTo(stack, current);
    titles.forEach((title, k) => title.classList.toggle('is-active', k === current));
    bars.forEach((bar, k) => {
      bar.classList.remove('is-active');
      bar.classList.toggle('is-done', k < current);
    });
    void bars[current].offsetWidth;   // restart the fill on the new active bar
    bars[current].classList.add('is-active');
  };

  const holds = new Set();
  const hold = (reason, on) => {
    if (on) holds.add(reason); else holds.delete(reason);
    hero.toggleAttribute('data-paused', holds.size > 0);
  };

  hero.addEventListener('animationend', (event) => {
    if (event.animationName === 'hero-fill') show(current + 1);
  });
  hero.addEventListener('pointerenter', (event) => { if (event.pointerType === 'mouse') hold('hover', true); });
  hero.addEventListener('pointerleave', () => hold('hover', false));
  hero.addEventListener('focusin', () => hold('focus', true));
  hero.addEventListener('focusout', (event) => { if (!hero.contains(event.relatedTarget)) hold('focus', false); });
  new IntersectionObserver(([entry]) => hold('offscreen', !entry.isIntersecting), { threshold: 0.25 }).observe(hero);
  document.addEventListener('visibilitychange', () => hold('hidden', document.hidden));

  hero.setAttribute('data-cycling', '');
  show(0);
})();

// Programme cards: a card with more than one photo shows the next ones while a mouse rests on it, and goes back
// to its first photo when the mouse leaves. Touch and reduced motion keep the first photo.
(() => {
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('.programme-card .crossfade').forEach((stack) => {
    if (stack.children.length < 2) return;
    const card = stack.closest('.programme-card');
    let current = 0;
    let timer;
    card.addEventListener('pointerenter', () => {
      crossfadeTo(stack, current = 1);
      timer = setInterval(() => crossfadeTo(stack, current = (current + 1) % stack.children.length), motion.ms('--dur-fade') + 900);
    });
    card.addEventListener('pointerleave', () => {
      clearInterval(timer);
      crossfadeTo(stack, current = 0);
    });
  });
})();

// Testimonials marquee: the drift stops while it is off the screen, so it isn't animating for nothing all visit.
(() => {
  const marquee = document.querySelector('.marquee');
  if (!marquee) return;
  new IntersectionObserver(([entry]) => marquee.toggleAttribute('data-paused', !entry.isIntersecting)).observe(marquee);
})();
