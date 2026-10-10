# MongoDB visitor counter

A minimal, separate Node server for **Between Potential and Ideal**.
It never changes the Render static site's HTML, design, routes or hosting.

## Status

Preparation only. Deployment requires a MongoDB Atlas cluster, a dedicated
`readWrite` DB user, secure Render environment variables and a separate
Web Service. **Do not point production pages at this service until /health and
/stats are verified.**


## Private analytics dashboard

Once the Node service is deployed, open:

`https://bpi-visitor-counter.onrender.com/admin`

The dashboard displays today's count (UTC), the last 7 UTC calendar days, a
daily chart, and the total since installation. It requires the existing
`STATS_ADMIN_TOKEN` from **Render → bpi-visitor-counter → Environment**.
Never paste the token into a URL, repository or chat.

The login form sends the token to the backend using a same-origin HTTPS POST.
The response sets an 8-hour signed `__Host-bpi_admin` cookie with
`HttpOnly; Secure; SameSite=Strict`. It is invalidated if the admin token or
visitor salt rotates; the logout button expires the browser cookie. The secret
is **never** saved in localStorage/sessionStorage or embedded in frontend
HTML or JavaScript. Admin JSON requests require a valid session; the
existing `/stats` Bearer-token endpoint remains supported.

The HTML is served by the **counter service**, not the Render static site,
so it can use same-origin, secure cookies without exposing a cross-origin
private statistics endpoint. No external JavaScript, fonts or trackers are
loaded by the dashboard. The admin route has a restrictive Content Security
Policy and a no-index directive. Admin pages are not linked in public
navigation. The dashboard does not generate a visitor count itself.

**Deployment note:** Check that Render's `bpi-visitor-counter` service
actually deploys the updated branch/commit. It was initially configured to
track `feature/mongodb-visitor-counter`, not `main`. Update its tracked
branch to `main` in Render settings when possible to avoid drift.

## Privacy and counting

- Only accepts a first-party browser request with
  `Origin: https://between-potential-and-ideal.onrender.com`.
- Uses a server-side HMAC of IP + truncated User-Agent. Raw IP and User-Agent
  are not stored in MongoDB by this application.
- A repeat request with the same estimated identity within a **rolling 24-hour
  period** does not count again.
- An index deletes deduplication identities 72 hours after the latest hit.
- A separate collection stores daily aggregate counts permanently.
- Simple bot User-Agents are excluded; no identity method is fully accurate.
  Shared NATs, VPNs, IP changes and spoofed headers may affect estimates.
- Stats requires `Authorization: Bearer <STATS_ADMIN_TOKEN>`.
- This is **server-side persistence**, not server-side observation of HTML
  requests: the current site is a Render Static Site. It will need a small
  first-party JS event sender on each page. Users who disable JavaScript or
  block that sender may still not be measured. Counting every HTML request
  requires serving the site behind a server/proxy.

## Required Render environment variables (never commit their values)

```
MONGODB_URI=<Atlas SRV connection URI for a dedicated least-privilege user>
VISITOR_HASH_SALT=<random secret, at least 32 characters>
STATS_ADMIN_TOKEN=<random secret, at least 24 characters>
ALLOWED_ORIGIN=https://between-potential-and-ideal.onrender.com
```

Use a long random salt and token, and keep them in Render's environment
settings only. Do not paste secrets in chat, source code or issue comments.

## Development

```bash
cd visitor-counter
npm install
npm test
npm start
```

With the service configured, test:

```bash
curl -s https://<counter-service>.onrender.com/health
curl -H "Authorization: Bearer $STATS_ADMIN_TOKEN" \
  https://<counter-service>.onrender.com/stats
```

## Rollout

1. Create Atlas database access with a dedicated `readWrite` user restricted
   to `bpi_analytics`; restrict network access as appropriate for the Render
   instance.
2. Create a separate Render Node Web Service from this repository:
   build command `cd visitor-counter && npm install --omit=dev`;
   start command `node visitor-counter/server.mjs`.
3. Set the four environment variables, verify `/health` and `/stats`.
4. Only then add the first-party page event sender on a separate reviewed
   change. Existing Cloudflare instrumentation can remain in place; do not
   call either system's number an exact count of people.
5. Keep the Admin token private; a public statistics page needs a different,
   intentionally scoped endpoint.

Daily counters are UTC buckets; deduplication is a rolling 24-hour period,
not a calendar-day identity. Stats start at the actual first recorded visit,
not at the historical start of the site.
