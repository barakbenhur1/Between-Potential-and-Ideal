/**
 * First-party page visit signal. The server stores only a short-lived,
 * salted hash and deduplicates visits within a rolling 24-hour window.
 * This signal is best-effort; it does not replace server access logs.
 */
(() => {
  'use strict';

  try {
    if (window.location.origin !== 'https://between-potential-and-ideal.onrender.com') return;
    if (navigator.globalPrivacyControl === true) return;

    const send = () => {
      try {
        fetch('https://bpi-visitor-counter.onrender.com/collect', {
          method: 'POST',
          mode: 'cors',
          credentials: 'omit',
          keepalive: true,
          cache: 'no-store'
        }).catch(() => {});
      } catch {
        // Analytics must never interfere with the site.
      }
    };

    if (document.prerendering) {
      document.addEventListener('prerenderingchange', send, { once: true });
    } else if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', send, { once: true });
    } else {
      send();
    }
  } catch {
    // Never interrupt site rendering due to optional analytics.
  }
})();
