
const text = {
  he: {
    dir: "rtl",
    langButton: "English",
    navRead: "קריאה",
    navDownloads: "קבצים",
    navContact: "תגובה",
    visitorLabel: "מבקרים באתר",
    visitorNote: "נספר בערך פעם ביום לכל דפדפן",
    visitorLoading: "…",
    visitorUnavailable: "מונה לא זמין"
  },
  en: {
    dir: "ltr",
    langButton: "עברית",
    navRead: "Read",
    navDownloads: "Files",
    navContact: "Respond",
    visitorLabel: "Site visitors",
    visitorNote: "Counted about once per browser per day",
    visitorLoading: "…",
    visitorUnavailable: "Counter unavailable"
  }
};
let currentLang = localStorage.getItem("bpai-lang") || "he";
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));
let visitorValue = null;

function applyLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("bpai-lang", lang);
  document.documentElement.lang = lang;
  document.documentElement.dir = text[lang].dir;
  $$('[data-lang-block]').forEach((block) => {
    block.hidden = block.getAttribute('data-lang-block') !== lang;
  });
  $$('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (text[lang][key]) el.textContent = text[lang][key];
  });
  const langButton = $('#langButton');
  if (langButton) langButton.textContent = text[lang].langButton;
  renderVisitorCounter();
}

function formatVisitorNumber(value) {
  const parsed = Number(value);
  if (Number.isFinite(parsed)) {
    return new Intl.NumberFormat(currentLang === 'he' ? 'he-IL' : 'en-US').format(parsed);
  }
  return value || text[currentLang].visitorUnavailable;
}

function getCounterValue(payload) {
  if (!payload || typeof payload !== 'object') return null;
  const candidates = [payload.value, payload.count, payload.data, payload.Count, payload.counter, payload.result];
  for (const candidate of candidates) {
    if (typeof candidate === 'number' || typeof candidate === 'string') return candidate;
    if (candidate && typeof candidate === 'object') {
      const nested = [candidate.value, candidate.count, candidate.data, candidate.Count];
      for (const nestedCandidate of nested) {
        if (typeof nestedCandidate === 'number' || typeof nestedCandidate === 'string') return nestedCandidate;
      }
    }
  }
  return null;
}

function renderVisitorCounter() {
  const count = $('#visitorCount');
  if (!count) return;
  count.textContent = visitorValue ? formatVisitorNumber(visitorValue) : text[currentLang].visitorLoading;
}

async function loadVisitorCounter() {
  const namespace = 'between-potential-and-ideal';
  const counterName = 'site-visits';
  const storageKey = 'bpai-counted-at-v1';
  const oneDay = 24 * 60 * 60 * 1000;
  const now = Date.now();
  const lastCounted = Number(localStorage.getItem(storageKey) || 0);
  const shouldIncrement = !lastCounted || now - lastCounted > oneDay;
  const action = shouldIncrement ? '/up' : '';
  try {
    const response = await fetch(`https://api.counterapi.dev/v1/${namespace}/${counterName}${action}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Counter failed: ${response.status}`);
    const payload = await response.json();
    const value = getCounterValue(payload);
    if (value === null || value === undefined || value === '') throw new Error('Counter value missing');
    visitorValue = String(value);
    if (shouldIncrement) localStorage.setItem(storageKey, String(now));
  } catch (error) {
    visitorValue = text[currentLang].visitorUnavailable;
  }
  renderVisitorCounter();
}

document.addEventListener('DOMContentLoaded', () => {
  applyLanguage(currentLang);
  const langButton = $('#langButton');
  if (langButton) {
    langButton.addEventListener('click', () => applyLanguage(currentLang === 'he' ? 'en' : 'he'));
  }
  loadVisitorCounter();
});
