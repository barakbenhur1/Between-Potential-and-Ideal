import http from 'node:http';
import { MongoClient } from 'mongodb';
import {
  DAY_MS, RETAIN_MS, utcDay, visitorKey, countIsDue, isLikelyBot, secureEqual
} from './lib.mjs';

const mongoUri = process.env.MONGODB_URI;
const salt = process.env.VISITOR_HASH_SALT;
const statsToken = process.env.STATS_ADMIN_TOKEN;
const allowedOrigin = process.env.ALLOWED_ORIGIN || 'https://between-potential-and-ideal.onrender.com';
const port = Number(process.env.PORT || 10000);

if (!mongoUri || !salt || salt.length < 32 || !statsToken || statsToken.length < 24) {
  console.error('Missing MONGODB_URI or strong VISITOR_HASH_SALT / STATS_ADMIN_TOKEN.');
  process.exit(1);
}

const mongo = new MongoClient(mongoUri, {
  maxPoolSize: 5,
  serverSelectionTimeoutMS: 10000
});

function reply(res, status, payload, origin = null) {
  const headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff'
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

async function main() {
  await mongo.connect();
  const db = mongo.db('bpi_analytics');
  const visitors = db.collection('visitor_dedupe');
  const daily = db.collection('daily_visits');
  await visitors.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });

  const server = http.createServer(async (req, res) => {
    const path = (req.url || '/').split('?')[0];
    const origin = req.headers.origin;

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
        const now = new Date();
        const today = utcDay(now);
        const weekStart = utcDay(new Date(now.getTime() - 6 * DAY_MS));
        const [todayDoc, weekDocs, totals] = await Promise.all([
          daily.findOne({ _id: today }),
          daily.find({ _id: { $gte: weekStart } }).toArray(),
          daily.aggregate([{ $group: { _id: null, visits: { $sum: '$visits' } } }]).toArray()
        ]);
        return reply(res, 200, {
          ok: true,
          metric: 'rolling-24h-deduplicated visits, UTC daily buckets',
          today: Number(todayDoc?.visits || 0),
          last7Days: weekDocs.reduce((sum, item) => sum + Number(item.visits || 0), 0),
          totalSinceInstallation: Number(totals[0]?.visits || 0)
        });
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
