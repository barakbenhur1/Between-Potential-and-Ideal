import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const script = readFileSync(new URL('../../site/assets/bpi-visitor-counter-v1.js', import.meta.url), 'utf8');
const loader = readFileSync(new URL('../../site/assets/runtime-performance-v1.js', import.meta.url), 'utf8');

function run({ origin = 'https://between-potential-and-ideal.onrender.com', gpc = false, state = 'complete', prerender = false } = {}) {
  const calls = [];
  const listeners = new Map();
  const sandbox = {
    window: { location: { origin } },
    navigator: { globalPrivacyControl: gpc },
    document: {
      readyState: state,
      prerendering: prerender,
      addEventListener(event, fn, options) {
        listeners.set(event, { fn, options });
      }
    },
    fetch(url, options) {
      calls.push({ url, options });
      return Promise.resolve({ ok: true });
    }
  };
  vm.runInNewContext(script, sandbox);
  return { calls, listeners };
}

test('existing analytics module loads the visit signal before the vendor bundle', () => {
  assert.match(loader.slice(0, 100), /^import '\.\/bpi-visitor-counter-v1\.js';/);
});

test('counts page view with credential-free best-effort POST', () => {
  const { calls } = run();
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, 'https://bpi-visitor-counter.onrender.com/collect');
  assert.equal(calls[0].options.method, 'POST');
  assert.equal(calls[0].options.credentials, 'omit');
  assert.equal(calls[0].options.keepalive, true);
});

test('defers while loading and prerendered', () => {
  const loading = run({state:'loading'});
  assert.equal(loading.calls.length, 0);
  assert.equal(loading.listeners.get('DOMContentLoaded').options.once, true);
  loading.listeners.get('DOMContentLoaded').fn();
  assert.equal(loading.calls.length, 1);

  const prerender = run({prerender:true});
  assert.equal(prerender.calls.length, 0);
  assert.equal(prerender.listeners.get('prerenderingchange').options.once, true);
  prerender.listeners.get('prerenderingchange').fn();
  assert.equal(prerender.calls.length, 1);
});

test('does not record another origin or global privacy control requests', () => {
  assert.equal(run({origin:'http://localhost:8080'}).calls.length, 0);
  assert.equal(run({gpc:true}).calls.length, 0);
});
