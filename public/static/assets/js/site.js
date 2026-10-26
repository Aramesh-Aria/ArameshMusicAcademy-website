/*
  Aramesh Music Academy: small vanilla modules, loaded with defer.
  Each one does nothing when its markup is absent, and every page reads fine without this file.
*/

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

// The week (`[data-week]`): day tabs over the day panels. Without JS only today's panel shows.
(() => {
  document.querySelectorAll('[data-week]').forEach((week) => {
    const tablist = week.querySelector('[data-week-tabs]');
    if (!tablist) return;
    const tabs = [...tablist.querySelectorAll('[role="tab"]')];
    const title = week.querySelector('[data-week-title]');
    tablist.hidden = false;

    const select = (tab, focus) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute('aria-selected', on);
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (title) title.textContent = tab.hasAttribute('data-today') ? 'امروز در آموزشگاه' : `${tab.dataset.label} در آموزشگاه`;
      if (focus) tab.focus();
    };

    // With no day marked today (a clock mismatch), open on the first day.
    if (!tabs.some((t) => t.getAttribute('aria-selected') === 'true')) select(tabs[0], false);

    tablist.addEventListener('click', (event) => {
      const tab = event.target.closest('[role="tab"]');
      if (tab) select(tab, false);
    });

    // Right to left: ArrowLeft moves to the next day, ArrowRight to the previous one.
    tablist.addEventListener('keydown', (event) => {
      const i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      const next = { ArrowLeft: i + 1, ArrowRight: i - 1, Home: 0, End: tabs.length - 1 }[event.key];
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
  const probe = document.createElement('dialog');
  if (!links.length || typeof probe.showModal !== 'function') return;

  const icon = (id) => `<svg class="icon" aria-hidden="true"><use href="#${id}"></use></svg>`;
  const box = document.createElement('dialog');
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

  const show = (i) => {
    index = (i + group.length) % group.length;
    const link = group[index];
    const thumb = link.querySelector('img');
    img.classList.add('is-loading');
    img.onload = () => img.classList.remove('is-loading');
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

  // Right to left: ArrowLeft moves to the next photo, ArrowRight to the previous one.
  box.addEventListener('keydown', (event) => {
    const step = { ArrowLeft: 1, ArrowRight: -1 }[event.key];
    if (!step || group.length < 2) return;
    event.preventDefault();
    show(index + step);
  });

  // A tap on the dark ground around the photo closes it.
  box.querySelector('.lightbox-stage').addEventListener('click', (event) => {
    if (event.target !== img) box.close();
  });

  // Swipe: a horizontal drag of 50px or more changes the photo; in RTL a drag to the right brings the next one.
  let startX = null;
  let startY = 0;
  img.addEventListener('pointerdown', (event) => { startX = event.clientX; startY = event.clientY; });
  img.addEventListener('pointerup', (event) => {
    if (startX === null || group.length < 2) return;
    const dx = event.clientX - startX;
    const dy = event.clientY - startY;
    startX = null;
    if (Math.abs(dx) >= 50 && Math.abs(dx) > Math.abs(dy)) show(index + (dx > 0 ? 1 : -1));
  });
  img.addEventListener('pointercancel', () => { startX = null; });
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
    poster.replaceWith(frame);
    frame.focus();
  });
})();

// Forms: the error summary takes focus after a failed submit, and the captcha can ask for a new image.
(() => {
  document.querySelector('[data-form-summary]')?.focus();

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
