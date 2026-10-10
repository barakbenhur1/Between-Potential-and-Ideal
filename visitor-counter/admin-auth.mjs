import { createHmac, randomBytes, timingSafeEqual } from 'node:crypto';

export const SESSION_HOURS = 8;
export const SESSION_MS = SESSION_HOURS * 60 * 60 * 1000;

function sessionKey(salt, adminToken) {
  return createHmac('sha256', salt)
    .update('bpi-admin-session-v1\0')
    .update(adminToken)
    .digest();
}

function signature(key, message) {
  return createHmac('sha256', key).update(message).digest('hex');
}

export function issueSession(salt, adminToken, now = Date.now()) {
  const expiration = now + SESSION_MS;
  const nonce = randomBytes(16).toString('hex');
  const payload = `${expiration}.${nonce}`;
  return `${payload}.${signature(sessionKey(salt, adminToken), payload)}`;
}

export function verifySession(value, salt, adminToken, now = Date.now()) {
  if (typeof value !== 'string' || value.length > 200) return false;
  const match = /^(\d{13})\.([a-f0-9]{32})\.([a-f0-9]{64})$/.exec(value);
  if (!match) return false;
  const expiresAt = Number(match[1]);
  if (!Number.isSafeInteger(expiresAt) || expiresAt <= now || expiresAt > now + SESSION_MS) return false;
  const payload = `${match[1]}.${match[2]}`;
  const expected = Buffer.from(signature(sessionKey(salt, adminToken), payload), 'hex');
  const actual = Buffer.from(match[3], 'hex');
  return timingSafeEqual(expected, actual);
}

export function findCookie(header, name) {
  if (typeof header !== 'string' || header.length > 8192) return null;
  for (const part of header.split(';')) {
    const trimmed = part.trim();
    if (trimmed.startsWith(name + '=')) return trimmed.slice(name.length + 1);
  }
  return null;
}

export function loginAllowedOrigin(origin, expected) {
  return origin === expected;
}

export function getRecentDays(now, dayDocs, count = 7) {
  const dayIndex = new Map(dayDocs.map(doc => [doc._id, Number(doc.visits || 0)]));
  const start = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  return Array.from({ length: count }, (_, index) => {
    const date = new Date(start - (count - index - 1) * 86_400_000).toISOString().slice(0, 10);
    return { date, visits: dayIndex.get(date) || 0 };
  });
}
