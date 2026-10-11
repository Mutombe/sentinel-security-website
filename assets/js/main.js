/* Sentinel Security Technology — site interactions */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Header: absolute over the hero, then pinned + solid once past the top bar ---- */
  var header = document.querySelector('.header');
  var topbar = document.querySelector('.topbar');
  var toTop = document.querySelector('.to-top');

  function onScroll() {
    var y = window.scrollY;
    var trigger = topbar ? topbar.offsetHeight : 0;
    if (header) {
      var pinned = y > trigger + 10;
      header.classList.toggle('header--fixed', pinned);
      header.classList.toggle('header--solid', pinned);
    }
    if (toTop) toTop.classList.toggle('is-visible', y > 700);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }

  /* ---- The group panel ----
     Opens on hover with a pointer, on click or Enter otherwise, and the link
     still goes to the group page either way. */
  var megaBtn = document.querySelector('[data-mega]');
  var mega = document.getElementById('mega');

  if (megaBtn && mega) {
    var megaHost = megaBtn.closest('.nav__has-mega');
    var closeTimer = null;

    function setMega(open) {
      clearTimeout(closeTimer);
      mega.classList.toggle('is-open', open);
      megaBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    function closeSoon() {
      clearTimeout(closeTimer);
      closeTimer = setTimeout(function () { setMega(false); }, 180);
    }

    if (window.matchMedia('(hover: hover)').matches) {
      megaHost.addEventListener('mouseenter', function () { setMega(true); });
      megaHost.addEventListener('mouseleave', closeSoon);
      mega.addEventListener('mouseenter', function () { setMega(true); });
      mega.addEventListener('mouseleave', closeSoon);
    }

    megaBtn.addEventListener('focus', function () { setMega(true); });
    megaBtn.addEventListener('click', function (e) {
      if (mega.classList.contains('is-open')) return;   // second tap follows the link
      if (!window.matchMedia('(hover: hover)').matches) {
        e.preventDefault();
        setMega(true);
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setMega(false);
    });
    document.addEventListener('focusin', function (e) {
      if (!mega.contains(e.target) && !megaHost.contains(e.target)) setMega(false);
    });
    document.addEventListener('click', function (e) {
      if (!mega.contains(e.target) && !megaHost.contains(e.target)) setMega(false);
    });
    window.addEventListener('scroll', function () { setMega(false); }, { passive: true });
  }

  /* ---- Hero ----
     Three company panels over three photographs, picked by a named tab row.
     Only the first slide ships a source; the rest attach after load so the
     first frame never competes with the stylesheet or the fonts.

     The tabs follow the ARIA tabs pattern: arrow keys move between them, and
     the inactive panels are hidden with visibility, which also takes their
     links out of the tab order. */
  var hero = document.querySelector('[data-hero]');

  if (hero) {
    var slides = Array.prototype.slice.call(hero.querySelectorAll('.hero__slide'));
    var panels = Array.prototype.slice.call(hero.querySelectorAll('.hero__panel'));
    var tabs = Array.prototype.slice.call(hero.querySelectorAll('[data-hero-tab]'));
    var index = 0;
    var timer = null;
    var DWELL = 7000;
    hero.style.setProperty('--hero-dwell', (DWELL / 1000) + 's');
    // Panels only animate once the first frame is on screen, so the panel that
    // ships active never fades itself in.
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { hero.classList.add('hero--ready'); });
    });

    var attachRest = function () {
      hero.querySelectorAll('img[data-src]').forEach(function (img) {
        if (img.getAttribute('data-srcset')) img.srcset = img.getAttribute('data-srcset');
        img.src = img.getAttribute('data-src');
        img.removeAttribute('data-src');
        img.removeAttribute('data-srcset');
      });
    };

    var show = function (next, focusTab) {
      next = (next + panels.length) % panels.length;
      if (next === index) return;

      slides[index].classList.remove('is-active');
      panels[index].classList.remove('is-active');
      tabs[index].classList.remove('is-active');
      tabs[index].setAttribute('aria-selected', 'false');
      tabs[index].tabIndex = -1;

      index = next;

      slides[index].classList.add('is-active');
      panels[index].classList.add('is-active');
      tabs[index].classList.add('is-active');
      tabs[index].setAttribute('aria-selected', 'true');
      tabs[index].tabIndex = 0;
      if (focusTab) tabs[index].focus();

      // Restart the drift and the progress rail on what just became visible.
      [slides[index].querySelector('img'), tabs[index].querySelector('.hero__tab-rail i')]
        .forEach(function (el) {
          if (!el) return;
          el.style.animation = 'none';
          void el.offsetWidth;
          el.style.animation = '';
        });
    };

    var stop = function () {
      if (timer) { clearInterval(timer); timer = null; }
      hero.classList.add('hero--paused');
    };
    var start = function () {
      hero.classList.remove('hero--paused');
      if (timer || reduceMotion || panels.length < 2) return;
      timer = setInterval(function () { show(index + 1); }, DWELL);
    };
    var restart = function () { stop(); start(); };

    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { show(i); restart(); });
      tab.addEventListener('keydown', function (e) {
        var k = e.key;
        if (k !== 'ArrowRight' && k !== 'ArrowLeft' && k !== 'Home' && k !== 'End') return;
        e.preventDefault();
        var to = k === 'Home' ? 0
               : k === 'End' ? tabs.length - 1
               : k === 'ArrowRight' ? i + 1 : i - 1;
        show(to, true);
        restart();
      });
    });

    // Reading beats advancing: hovering or tabbing into the hero holds it.
    hero.addEventListener('mouseenter', stop);
    hero.addEventListener('mouseleave', start);
    hero.addEventListener('focusin', stop);
    hero.addEventListener('focusout', function (e) {
      if (!hero.contains(e.relatedTarget)) start();
    });

    if (document.readyState === 'complete') attachRest();
    else window.addEventListener('load', attachRest, { once: true });

    if (!reduceMotion) {
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (e) { e.isIntersecting ? start() : stop(); });
        }, { threshold: 0.12 }).observe(hero);
      } else {
        start();
      }
      document.addEventListener('visibilitychange', function () {
        document.hidden ? stop() : start();
      });
    }
  }

  /* ---- Mobile drawer ---- */
  var toggle = document.querySelector('.nav-toggle');
  var drawer = document.querySelector('.drawer');

  function setDrawer(open) {
    if (!toggle || !drawer) return;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    drawer.classList.toggle('is-open', open);
    document.body.classList.toggle('is-locked', open);
  }

  if (toggle && drawer) {
    toggle.addEventListener('click', function () {
      setDrawer(toggle.getAttribute('aria-expanded') !== 'true');
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) setDrawer(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setDrawer(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 980) setDrawer(false);
    });
  }

  /* ---- WhatsApp widget ----
     One button that asks which conversation you want before it hands you to
     WhatsApp, rather than guessing. Closes on Escape, on an outside click and
     once an option is taken. */
  var wa = document.querySelector('[data-wa]');
  var waToggle = document.querySelector('[data-wa-toggle]');

  if (wa && waToggle) {
    var setWa = function (open) {
      wa.classList.toggle('is-open', open);
      waToggle.setAttribute('aria-expanded', String(open));
      waToggle.setAttribute('aria-label', open ? 'Close WhatsApp options' : 'Contact us on WhatsApp');
      if (open) {
        var first = wa.querySelector('.wa__opt');
        if (first) first.focus();
      }
    };

    waToggle.addEventListener('click', function (e) {
      e.stopPropagation();
      setWa(waToggle.getAttribute('aria-expanded') !== 'true');
    });

    wa.addEventListener('click', function (e) {
      if (e.target.closest('.wa__opt')) setWa(false);
    });

    document.addEventListener('click', function (e) {
      if (!wa.contains(e.target)) setWa(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || waToggle.getAttribute('aria-expanded') !== 'true') return;
      setWa(false);
      waToggle.focus();
    });

    // Keep tabbing inside the panel while it is open.
    wa.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || waToggle.getAttribute('aria-expanded') !== 'true') return;
      var items = wa.querySelectorAll('.wa__opt, .wa__toggle');
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* ---- Scroll reveal ---- */
  var revealables = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
  if (!('IntersectionObserver' in window) || reduceMotion) {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var pending = revealables.slice();

    var reveal = function (el) {
      el.classList.add('is-in');
      var i = pending.indexOf(el);
      if (i > -1) pending.splice(i, 1);
      revealObserver.unobserve(el);
    };

    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) reveal(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    revealables.forEach(function (el) {
      // Stagger siblings that share a parent for a cascading entrance.
      if (!el.style.getPropertyValue('--d')) {
        var sibs = Array.prototype.filter.call(el.parentNode.children, function (c) {
          return c.hasAttribute('data-reveal');
        });
        var idx = sibs.indexOf(el);
        el.style.setProperty('--d', (idx > 0 ? Math.min(idx, 5) * 85 : 0) + 'ms');
      }
      revealObserver.observe(el);
    });

    // Safety net: a fast flick or End key can scroll past an element between two
    // IntersectionObserver deliveries, which would strand it invisible forever.
    var sweeping = false;
    var sweep = function () {
      sweeping = false;
      if (!pending.length) return;
      var limit = window.innerHeight * 0.92;
      pending.slice().forEach(function (el) {
        if (el.getBoundingClientRect().top < limit) reveal(el);
      });
    };
    window.addEventListener('scroll', function () {
      if (sweeping || !pending.length) return;
      sweeping = true;
      requestAnimationFrame(sweep);
    }, { passive: true });
  }

  /* ---- Accordion ---- */
  document.querySelectorAll('.acc__btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      if (panel) panel.setAttribute('data-open', String(!open));
    });
  });

  /* ---- Contact form (no backend yet — hands off to the visitor's mail client) ---- */
  var form = document.querySelector('[data-contact-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var lines = [
        'Name: ' + (data.get('name') || ''),
        'Company: ' + (data.get('company') || '—'),
        'Email: ' + (data.get('email') || ''),
        'Phone: ' + (data.get('phone') || ''),
        'Service: ' + (data.get('service') || ''),
        'Site location: ' + (data.get('location') || '—'),
        '',
        String(data.get('message') || '')
      ];
      var href = 'mailto:info@sentinel.co.zw'
        + '?subject=' + encodeURIComponent('Website enquiry — ' + (data.get('service') || 'General'))
        + '&body=' + encodeURIComponent(lines.join('\n'));

      var status = form.querySelector('.form-status');
      if (status) {
        status.textContent = 'Opening your email app with the enquiry ready to send. If nothing happens, email info@sentinel.co.zw directly.';
        status.classList.add('is-visible');
      }
      window.location.href = href;
    });
  }

  /* ---- Current year ---- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
