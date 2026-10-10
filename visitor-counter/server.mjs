import http from 'node:http';
import { readFileSync } from 'node:fs';
import { MongoClient } from 'mongodb';
import {
  DAY_MS, RETAIN_MS, utcDay, visitorKey, countIsDue, isLikelyBot, secureEqual
} from './lib.mjs';
import {
  issueSession, verifySession, findCookie, getRecentDays, loginAllowedOrigin,
  SESSION_MS
} from './admin-auth.mjs';

const mongoUri = process.env.MONGODB_URI;
const salt = process.env.VISITOR_HASH_SALT;
const statsToken = process.env.STATS_ADMIN_TOKEN;
const allowedOrigin = process.env.ALLOWED_ORIGIN || 'https://between-potential-and-ideal.onrender.com';
const port = Number(process.env.PORT || 10000);
const adminOrigin = process.env.ADMIN_ORIGIN || 'https://bpi-visitor-counter.onrender.com';
const adminCookie = '__Host-bpi_admin';
const adminHtml = readFileSync(new URL('./dashboard.html', import.meta.url), 'utf8');
const adminJs = readFileSync(new URL('./dashboard.js', import.meta.url), 'utf8');
const adminCss = readFileSync(new URL('./dashboard.css', import.meta.url), 'utf8');

if (!mongoUri || !salt || salt.length < 32 || !statsToken || statsToken.length < 24) {
  console.error('Missing MONGODB_URI or strong VISITOR_HASH_SALT / STATS_ADMIN_TOKEN.');
  process.exit(1);
}

const mongo = new MongoClient(mongoUri, {
  maxPoolSize: 5,
  serverSelectionTimeoutMS: 10000
});

function reply(res, status, payload, origin = null, extraHeaders = {}) {
  const headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
    'X-Frame-Options': 'DENY',
    ...extraHeaders
  };
  if (origin === allowedOrigin) {
    headers['Access-Control-Allow-Origin'] = allowedOrigin;
    headers['Vary'] = 'Origin';
  }
  res.writeHead(status, headers);
  res.end(JSON.stringify(payload));
}

function extractClientIP(req) {
  // Render populates X-Forwarded-For. Do not log or store the raw IP.
  const forwarded = req.headers['x-forwarded-for'];
  const value = Array.isArray(forwarded) ? forwarded[0] : forwarded;
  return (typeof value === 'string' ? value.split(',')[0].trim() : '') ||
    req.socket.remoteAddress || '';
}

function authorized(req) {
  const header = req.headers.authorization || '';
  return header.startsWith('Bearer ') && secureEqual(header.slice(7), statsToken);
}

function serveAdminAsset(res, contentType, content, isHtml = false) {
  const headers = {
    'Content-Type': contentType,
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
    'X-Frame-Options': 'DENY'
  };
  if (isHtml) {
    headers['Content-Security-Policy'] =
      "default-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'; connect-src 'self'; script-src 'self'; style-src 'self'";
    headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive';
  }
  res.writeHead(200, headers);
  res.end(content);
}

async function readSmallJson(req) {
  if (!String(req.headers['content-type'] || '').startsWith('application/json')) {
    throw new Error('invalid-content-type');
  }
  if (Number(req.headers['content-length'] || 0) > 2048) {
    throw new Error('body-too-large');
  }
  let text = '';
  for await (const chunk of req) {
    text += chunk.toString('utf8');
    if (text.length > 2048) throw new Error('body-too-large');
  }
  return JSON.parse(text);
}

function adminAuthorized(req) {
  const value = findCookie(req.headers.cookie, adminCookie);
  return verifySession(value, salt, statsToken);
}

function cookieString(value, maxAge) {
  return `${adminCookie}=${value}; Path=/; Max-Age=${maxAge}; HttpOnly; Secure; SameSite=Strict`;
}

async function main() {
  await mongo.connect();
  const db = mongo.db('bpi_analytics');
  const visitors = db.collection('visitor_dedupe');
  const daily = db.collection('daily_visits');
  await visitors.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });

  async function loadStats() {
    const now = new Date();
    const today = utcDay(now);
    const weekStart = utcDay(new Date(now.getTime() - 6 * DAY_MS));
    const [todayDoc, weekDocs, totals] = await Promise.all([
      daily.findOne({ _id: today }),
      daily.find({ _id: { $gte: weekStart } }).toArray(),
      daily.aggregate([{ $group: { _id: null, visits: { $sum: '$visits' } } }]).toArray()
    ]);
    const days = getRecentDays(now, weekDocs);
    return {
      ok: true,
      metric: 'rolling-24h-deduplicated visits, UTC daily buckets',
      today: Number(todayDoc?.visits || 0),
      last7Days: days.reduce((sum, item) => sum + item.visits, 0),
      totalSinceInstallation: Number(totals[0]?.visits || 0),
      days
    };
  }


  const server = http.createServer(async (req, res) => {
    const path = (req.url || '/').split('?')[0];
    const origin = req.headers.origin;


    // Private administration UI. Secrets never appear in the HTML, JS, or URLs.
    if (req.method === 'GET' && (path === '/admin' || path === '/admin/')) {
      return serveAdminAsset(res, 'text/html; charset=utf-8', adminHtml, true);
    }
    if (req.method === 'GET' && path === '/admin/app.js') {
      return serveAdminAsset(res, 'text/javascript; charset=utf-8', adminJs);
    }
    if (req.method === 'GET' && path === '/admin/style.css') {
      return serveAdminAsset(res, 'text/css; charset=utf-8', adminCss);
    }

    if (req.method === 'POST' && path === '/admin/login') {
      if (!loginAllowedOrigin(origin, adminOrigin)) return reply(res, 403, { error: 'Forbidden' });
      try {
        const input = await readSmallJson(req);
        if (typeof input?.token !== 'string' || !secureEqual(input.token, statsToken)) {
          return reply(res, 401, { error: 'Unauthorized' });
        }
        const session = issueSession(salt, statsToken);
        return reply(res, 200, { ok: true }, null, {
          'Set-Cookie': cookieString(session, Math.floor(SESSION_MS / 1000))
        });
      } catch {
        return reply(res, 400, { error: 'Invalid request' });
      }
    }

    if (req.method === 'POST' && path === '/admin/logout') {
      if (!loginAllowedOrigin(origin, adminOrigin)) return reply(res, 403, { error: 'Forbidden' });
      return reply(res, 200, { ok: true }, null, {
        'Set-Cookie': cookieString('', 0)
      });
    }

    if (req.method === 'GET' && path === '/admin/stats') {
      if (!adminAuthorized(req)) return reply(res, 401, { error: 'Unauthorized' });
      try {
        return reply(res, 200, await loadStats());
      } catch (err) {
        console.error('Admin stats failed:', err.message);
        return reply(res, 503, { error: 'Unavailable' });
      }
    }

    if (req.method === 'GET' && path === '/health') {
      return reply(res, 200, { ok: true, storage: 'mongodb' });
    }

    if (req.method === 'OPTIONS' && path === '/collect') {
      if (origin !== allowedOrigin) return reply(res, 403, { ok: false });
      res.writeHead(204, {
        'Access-Control-Allow-Origin': allowedOrigin,
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'Vary': 'Origin'
      });
      return res.end();
    }

    if (req.method === 'POST' && path === '/collect') {
      if (origin !== allowedOrigin) return reply(res, 403, { ok: false });
      if (Number(req.headers['content-length'] || 0) > 1024) {
        return reply(res, 413, { ok: false }, origin);
      }

      req.resume();
      const agent = String(req.headers['user-agent'] || '');
      if (isLikelyBot(agent)) return reply(res, 204, { ok: true }, origin);

      const fingerprint = visitorKey(salt, extractClientIP(req), agent);
      if (!fingerprint) return reply(res, 204, { ok: true }, origin);

      try {
        const now = new Date();
        const cutoff = new Date(now.getTime() - DAY_MS);
        const before = await visitors.findOneAndUpdate(
          { _id: fingerprint },
          [{
            $set: {
              lastCountedAt: {
                $cond: [
                  { $lte: [{ $ifNull: ['$lastCountedAt', new Date(0)] }, cutoff] },
                  now,
                  '$lastCountedAt'
                ]
              },
              expiresAt: new Date(now.getTime() + RETAIN_MS)
            }
          }],
          { upsert: true, returnDocument: 'before' }
        );

        const counted = countIsDue(before, cutoff);
        if (counted) {
          await daily.updateOne(
            { _id: utcDay(now) },
            { $inc: { visits: 1 }, $setOnInsert: { createdAt: now } },
            { upsert: true }
          );
        }
        return reply(res, 204, { ok: true }, origin);
      } catch (err) {
        console.error('Counter write failed:', err.message);
        return reply(res, 503, { ok: false }, origin);
      }
    }

    if (req.method === 'GET' && path === '/stats') {
      if (!authorized(req)) return reply(res, 401, { error: 'Unauthorized' });
      try {
        return reply(res, 200, await loadStats());
      } catch (err) {
        console.error('Stats read failed:', err.message);
        return reply(res, 503, { error: 'Unavailable' });
      }
    }

    return reply(res, 404, { error: 'Not found' });
  });

  server.listen(port, '0.0.0.0', () => {
    console.log('Visitor counter ready on port ' + port);
  });

  const close = async () => {
    server.close();
    await mongo.close();
    process.exit(0);
  };
  process.on('SIGTERM', close);
  process.on('SIGINT', close);
}

main().catch(err => {
  console.error('Counter failed to start:', err.message);
  process.exit(1);
});
