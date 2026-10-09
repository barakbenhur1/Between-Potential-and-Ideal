import { createHmac, timingSafeEqual } from 'node:crypto';

export const DAY_MS = 24 * 60 * 60 * 1000;
export const RETAIN_MS = 72 * 60 * 60 * 1000;

export function utcDay(date) {
  return date.toISOString().slice(0, 10);
}

export function visitorKey(salt, ip, userAgent) {
  if (!salt || !ip || !userAgent) return null;
  return createHmac('sha256', salt)
    .update(ip)
    .update('\0')
    .update(userAgent.slice(0, 512))
    .digest('hex');
}

export function countIsDue(previous, cutoff) {
  if (!previous || !(previous.lastCountedAt instanceof Date)) return true;
  return previous.lastCountedAt.getTime() <= cutoff.getTime();
}

export function isLikelyBot(userAgent) {
  return !userAgent || /bot|crawl|spider|headless|lighthouse|curl|wget|python-requests|uptime|monitor/i.test(userAgent);
}

export function secureEqual(a, b) {
  if (!a || !b) return false;
  const left = Buffer.from(a);
  const right = Buffer.from(b);
  if (left.length !== right.length) return false;
  return timingSafeEqual(left, right);
}
