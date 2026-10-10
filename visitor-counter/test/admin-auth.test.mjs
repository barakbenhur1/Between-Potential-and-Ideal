import test from 'node:test';
import assert from 'node:assert/strict';
import { issueSession, verifySession, findCookie, loginAllowedOrigin, getRecentDays, SESSION_MS } from '../admin-auth.mjs';

const salt = 'a'.repeat(64);
const secret = 'b'.repeat(48);
const now = Date.UTC(2026, 9, 10, 8, 0, 0);

test('admin session is signed, expires, and rotates with password', () => {
  const cookie = issueSession(salt, secret, now);
  assert.equal(verifySession(cookie, salt, secret, now + 10_000), true);
  assert.equal(verifySession(cookie, salt, secret, now + SESSION_MS), false);
  assert.equal(verifySession(cookie, salt, 'changed-token', now + 10_000), false);
  assert.equal(verifySession(cookie, 'different-salt', secret, now + 10_000), false);
  assert.equal(verifySession(cookie.slice(0, -1) + (cookie.endsWith('f') ? 'e' : 'f'), salt, secret, now + 10_000), false);
  assert.equal(verifySession('bad', salt, secret, now), false);
});

test('reads only named cookie', () => {
  assert.equal(findCookie('other=x; __Host-bpi_admin=token; third=y', '__Host-bpi_admin'), 'token');
  assert.equal(findCookie('admin=wrong', '__Host-bpi_admin'), null);
});

test('login requires precise same-origin browser request', () => {
  const origin = 'https://bpi-visitor-counter.onrender.com';
  assert.equal(loginAllowedOrigin(origin, origin), true);
  assert.equal(loginAllowedOrigin('https://evil.example', origin), false);
  assert.equal(loginAllowedOrigin(undefined, origin), false);
});

test('UTC daily series includes zero-visit days and week boundaries', () => {
  const result = getRecentDays(new Date('2026-10-10T00:05:00Z'), [
    {_id:'2026-10-04',visits:1}, {_id:'2026-10-09',visits:3}, {_id:'2026-10-10',visits:2}
  ]);
  assert.equal(result.length, 7);
  assert.deepEqual(result.map(r => r.date), ['2026-10-04','2026-10-05','2026-10-06','2026-10-07','2026-10-08','2026-10-09','2026-10-10']);
  assert.deepEqual(result.map(r => r.visits), [1,0,0,0,0,3,2]);
});
