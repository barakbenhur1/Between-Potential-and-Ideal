/* V127 — stable helper only.
   Do not mutate, reorder, append, or relabel the tab bar at runtime.
   This avoids header jumps, broken clicks, and language-switch jumps. */
(function(){
  'use strict';

  function cleanHref(a){
    return (a && a.getAttribute('href') || '').split('?')[0].split('#')[0].toLowerCase();
  }

  function normalizeFileTargets(){
    Array.from(document.querySelectorAll('a[href]')).forEach(function(a){
      var h = cleanHref(a);
      var isArchive = h.indexOf('/files/') !== -1 || h.indexOf('../../files/') === 0 || h.indexOf('../files/') === 0 || h.indexOf('files/') === 0;
      if (!isArchive || !/\.(html|pdf|docx|md|txt)$/.test(h)) return;
      a.setAttribute('target', '_blank');
      var rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
      ['noopener','noreferrer'].forEach(function(token){ if (rel.indexOf(token) === -1) rel.push(token); });
      a.setAttribute('rel', rel.join(' '));
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', normalizeFileTargets);
  else normalizeFileTargets();
})();
