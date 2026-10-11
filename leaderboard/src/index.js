// Global leaderboard for Balloon of Pee vs. Platoon of Bees.
//   GET  /scores  -> { top: [{ rank, id, name, score }] }      (top 10, score in seconds)
//   POST /scores  { name, score } -> { id, top }               (saves a run, returns the new top 10)

const ALLOWED_ORIGINS = [
  'https://aingebritson.github.io',
  'http://localhost:8765',
  'http://127.0.0.1:8765',
];
const TOP_N = 10;
const MAX_NAME = 10;
const MAX_SCORE = 3600; // an hour dry is not humanly possible
const NAME_PATTERN = /^[A-Z0-9 .!?'_-]+$/; // arcade-style characters only

function corsHeaders(origin) {
  const headers = {
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    Vary: 'Origin',
  };
  if (ALLOWED_ORIGINS.includes(origin)) headers['Access-Control-Allow-Origin'] = origin;
  return headers;
}

function json(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...corsHeaders(origin) },
  });
}

async function topScores(env) {
  const { results } = await env.DB
    .prepare('SELECT id, name, score_tenths FROM scores ORDER BY score_tenths DESC, id ASC LIMIT ?')
    .bind(TOP_N)
    .all();
  return results.map((r, i) => ({ rank: i + 1, id: r.id, name: r.name, score: r.score_tenths / 10 }));
}

function cleanName(raw) {
  if (typeof raw !== 'string') return null;
  const name = raw.normalize('NFKC').replace(/\s+/g, ' ').trim().toUpperCase();
  if (!name || [...name].length > MAX_NAME || !NAME_PATTERN.test(name)) return null;
  return name;
}

// A short one-way hash of the player's IP address, so raw addresses are never stored.
async function ipHash(request) {
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode('bopvpob:' + ip));
  return [...new Uint8Array(digest)].slice(0, 8).map((b) => b.toString(16).padStart(2, '0')).join('');
}

async function saveScore(request, env, origin) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Send the score as JSON.' }, 400, origin);
  }
  const name = cleanName(body && body.name);
  if (!name) return json({ error: 'Use up to 10 letters, numbers or spaces.' }, 400, origin);
  const score = Number(body && body.score);
  if (!Number.isFinite(score) || score <= 0 || score > MAX_SCORE) {
    return json({ error: "That score isn't possible." }, 400, origin);
  }

  const ip = await ipHash(request);
  const recent = await env.DB
    .prepare("SELECT COUNT(*) AS n FROM scores WHERE ip_hash = ? AND created_at > datetime('now', '-10 seconds')")
    .bind(ip)
    .first('n');
  if (recent > 0) return json({ error: 'Too fast. Wait a few seconds and try again.' }, 429, origin);

  const result = await env.DB
    .prepare('INSERT INTO scores (name, score_tenths, ip_hash) VALUES (?, ?, ?)')
    .bind(name, Math.round(score * 10), ip)
    .run();
  return json({ id: result.meta.last_row_id, top: await topScores(env) }, 201, origin);
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const { pathname } = new URL(request.url);
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders(origin) });
    if (pathname !== '/scores') return json({ error: 'Not found.' }, 404, origin);
    if (request.method === 'GET') return json({ top: await topScores(env) }, 200, origin);
    if (request.method === 'POST') return saveScore(request, env, origin);
    return json({ error: 'Method not allowed.' }, 405, origin);
  },
};
