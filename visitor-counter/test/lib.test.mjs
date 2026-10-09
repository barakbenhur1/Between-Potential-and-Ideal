import test from 'node:test';
import assert from 'node:assert/strict';
import { utcDay, visitorKey, countIsDue, isLikelyBot, secureEqual, DAY_MS } from '../lib.mjs';

test('UTC day boundary', () => {
  assert.equal(utcDay(new Date('2026-10-10T00:05:00Z')), '2026-10-10');
});

test('fingerprints are deterministic, salted and never raw IPs', () => {
  const x = visitorKey('test-secret', '203.0.113.1', 'Example Browser');
  assert.equal(x.length, 64);
  assert.equal(x, visitorKey('test-secret', '203.0.113.1', 'Example Browser'));
  assert.notEqual(x, visitorKey('different-secret', '203.0.113.1', 'Example Browser'));
  assert.notEqual(x, visitorKey('test-secret', '203.0.113.2', 'Example Browser'));
  assert.equal(visitorKey('test-secret', '', 'Example Browser'), null);
});

test('count once per rolling 24 hours', () => {
  const now = new Date('2026-10-10T12:00:00Z');
  const cutoff = new Date(now.getTime() - DAY_MS);
  assert.equal(countIsDue(null, cutoff), true);
  assert.equal(countIsDue({lastCountedAt:new Date(now.getTime() - DAY_MS + 1000)}, cutoff), false);
  assert.equal(countIsDue({lastCountedAt:new Date(now.getTime() - DAY_MS)}, cutoff), true);
});

test('common bots and empty clients are excluded', () => {
  assert.equal(isLikelyBot('Googlebot/2.1'), true);
  assert.equal(isLikelyBot('curl/8.0'), true);
  assert.equal(isLikelyBot('Mozilla/5.0 Safari/605'), false);
  assert.equal(isLikelyBot(''), true);
});

test('constant-time secret comparison supports unequal values', () => {
  assert.equal(secureEqual('abc', 'abc'), true);
  assert.equal(secureEqual('abc', 'abcd'), false);
  assert.equal(secureEqual('abc', 'abd'), false);
});
