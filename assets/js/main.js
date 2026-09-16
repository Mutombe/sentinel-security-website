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
