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

    var announce = function () {
      document.dispatchEvent(new CustomEvent('sentinel:slidechange'));
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
      announce();          // the newly shown photograph gets framed

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
      if (e.target.closest('a') || e.target.closest('[data-drawer-close]')) {
        setDrawer(false);
        if (e.target.closest('[data-drawer-close]')) toggle.focus();
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !drawer.classList.contains('is-open')) return;
      setDrawer(false);
      toggle.focus();          // the focus comes back where it left
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

    /* ---- Figures that count up ----
       The element already holds its final value, so this only animates the
       text between zero and what is already there. Anything it cannot parse
       is left exactly as authored. */
    var counters = Array.prototype.slice.call(document.querySelectorAll('[data-count]'));
    if (counters.length) {
      var runCount = function (el) {
        var target = parseFloat(String(el.getAttribute('data-count')).replace(/[^0-9.\-]/g, ''));
        if (!isFinite(target)) return;
        var final = el.textContent;
        var prefix = (final.match(/^[^0-9]*/) || [''])[0];
        var suffix = (final.match(/[^0-9]*$/) || [''])[0];
        var dur = 1100, t0 = 0;
        var step = function (ts) {
          if (!t0) t0 = ts;
          var p = Math.min((ts - t0) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = prefix + Math.round(target * eased) + suffix;
          if (p < 1) requestAnimationFrame(step);
          else el.textContent = final;
        };
        requestAnimationFrame(step);
      };

      var countObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          countObserver.unobserve(entry.target);
          runCount(entry.target);
        });
      }, { threshold: 0.6 });

      counters.forEach(function (el) { countObserver.observe(el); });
    }

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

    // The same sweep on load and shortly after, so a visitor who never
    // scrolls, or an observer delivery that never arrives, cannot leave
    // content sitting invisible.
    window.addEventListener('load', sweep);
    setTimeout(sweep, 1200);
    setTimeout(sweep, 3500);
  }

  /* ---- Framing ----
     Each photograph that declares a subject box gets its crop chosen here,
     on the screen it is actually being shown on, rather than from a fixed
     object-position that can only be right at one width. */
  var framed = Array.prototype.slice.call(document.querySelectorAll('img[data-focus]'));

  if (framed.length) {
    var STEPS = 64;          /* 65 positions per axis */
    var PENALTY = 1000;      /* visibility beats centring */

    /* Anything painted over a photograph is an obstacle to steer around. */
    function obstaclesFor(frameRect, img) {
      var out = [];
      var marks = document.querySelectorAll('[data-obstacle]');
      for (var i = 0; i < marks.length; i++) {
        var el = marks[i];
        if (el.contains(img)) continue;              /* its own wrapper is not an obstacle */
        /* Only things in the same section are layered over it; rectangle
           overlap alone scored a copy column three sections away against a
           photograph it never touches. */
        if (el.closest('section') !== img.closest('section')) continue;
        var cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none' ||
            parseFloat(cs.opacity) < 0.08) continue;  /* a hidden slide's copy does not count */
        var r = el.getBoundingClientRect();
        if (!r.width || !r.height) continue;
        var x0 = Math.max(r.left, frameRect.left), y0 = Math.max(r.top, frameRect.top);
        var x1 = Math.min(r.right, frameRect.right), y1 = Math.min(r.bottom, frameRect.bottom);
        if (x1 <= x0 || y1 <= y0) continue;
        out.push({ x0: x0 - frameRect.left, y0: y0 - frameRect.top,
                   x1: x1 - frameRect.left, y1: y1 - frameRect.top });
      }
      return out;
    }

    function overlap(ax0, ay0, ax1, ay1, b) {
      var w = Math.min(ax1, b.x1) - Math.max(ax0, b.x0);
      var h = Math.min(ay1, b.y1) - Math.max(ay0, b.y0);
      return (w > 0 && h > 0) ? w * h : 0;
    }

    function frameOne(img) {
      var spec = img.getAttribute('data-focus');
      if (!spec) return;
      var box = spec.split(/\s+/).map(Number);
      if (box.length !== 4) return;
      var nw = img.naturalWidth, nh = img.naturalHeight;
      if (!nw || !nh) return;

      /* The layout box, never the hovered or drifting one: several of these
         photographs scale on hover or during the carousel, and framing must
         not follow that. */
      var r = img.getBoundingClientRect();
      var fw = img.offsetWidth || r.width, fh = img.offsetHeight || r.height;
      if (fw < 4 || fh < 4) return;

      var scale = Math.max(fw / nw, fh / nh);          /* cover */
      var dw = nw * scale, dh = nh * scale;
      var slackX = dw - fw, slackY = dh - fh;

      var sx0 = box[0] / 100 * dw, sy0 = box[1] / 100 * dh;
      var sx1 = box[2] / 100 * dw, sy1 = box[3] / 100 * dh;
      var sArea = Math.max((sx1 - sx0) * (sy1 - sy0), 1);

      // A ground is framed for visibility only. Its copy is laid over it
      // behind a scrim by design, and where the frame is wider than the file
      // there is no horizontal room to move the subject out from under it.
      var ground = img.closest('.secbg') !== null ||
                   img.closest('.hero__media') !== null ||
                   img.closest('.phero__media') !== null;
      var obs = ground ? [] : obstaclesFor(r, img);

      var bestX = 50, bestY = 50, best = Infinity;
      for (var i = 0; i <= STEPS; i++) {
        var px = i / STEPS;
        var ox = slackX > 0 ? -slackX * px : 0;
        for (var j = 0; j <= STEPS; j++) {
          var py = j / STEPS;
          var oy = slackY > 0 ? -slackY * py : 0;

          var bx0 = sx0 + ox, by0 = sy0 + oy, bx1 = sx1 + ox, by1 = sy1 + oy;

          /* How much of the subject falls outside the frame. */
          var insideW = Math.min(bx1, fw) - Math.max(bx0, 0);
          var insideH = Math.min(by1, fh) - Math.max(by0, 0);
          var inside = (insideW > 0 && insideH > 0) ? insideW * insideH : 0;
          var outside = (sArea - inside) / sArea;

          /* How much of it sits under something. */
          var covered = 0;
          for (var k = 0; k < obs.length; k++) covered += overlap(bx0, by0, bx1, by1, obs[k]);
          covered /= sArea;

          var cx = (bx0 + bx1) / 2 / fw - 0.5;
          var cy = (by0 + by1) / 2 / fh - 0.5;
          var cost = PENALTY * (outside + covered) + cx * cx + cy * cy;

          if (cost < best) { best = cost; bestX = px * 100; bestY = py * 100; }
          if (slackY <= 0) break;
        }
        if (slackX <= 0) break;
      }
      img.style.objectPosition = bestX.toFixed(2) + '% ' + bestY.toFixed(2) + '%';
    }

    var frameAll = function () {
      for (var i = 0; i < framed.length; i++) frameOne(framed[i]);
    };

    framed.forEach(function (img) {
      if (img.complete && img.naturalWidth) frameOne(img);
      else img.addEventListener('load', function () { frameOne(img); });
    });

    /* Re-run wherever the layout can change under it. */
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(frameAll);
    window.addEventListener('load', frameAll);
    setTimeout(frameAll, 1100);          /* after the reveals have settled */

    var rt;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(frameAll, 120);
    }, { passive: true });

    document.addEventListener('sentinel:slidechange', frameAll);

    window.__frameAll = frameAll;        /* the QA script calls this */
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
