// http → https, www → apex 강제 전환 + HSTS, 그리고 D1에 익명 방문 기록.
// 나머지는 정적 자산(public/) 그대로 서빙.
const BOT_RE = /bot|crawl|spider|slurp|curl|wget|python|httpclient|headless|lighthouse|preview|facebookexternalhit|kakaotalk-scrap|monitor/i;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.protocol === 'http:' || url.hostname === 'www.readmd.kr') {
      url.protocol = 'https:';
      if (url.hostname === 'www.readmd.kr') url.hostname = 'readmd.kr';
      return Response.redirect(url.toString(), 301);
    }

    const res = await env.ASSETS.fetch(request);
    const headers = new Headers(res.headers);
    headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');

    if (shouldLog(request, res, url)) ctx.waitUntil(logView(request, env, url).catch(() => {}));
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
  },
};

function shouldLog(request, res, url) {
  if (request.method !== 'GET' || res.status !== 200 || !env_ok(url)) return false;
  const accept = request.headers.get('accept') || '';
  if (!accept.includes('text/html')) return false;
  const ua = request.headers.get('user-agent') || '';
  if (!ua || BOT_RE.test(ua)) return false;
  return true;
}
function env_ok(url) { return url.hostname === 'readmd.kr' || url.hostname.endsWith('.workers.dev'); }

async function logView(request, env, url) {
  const ua = request.headers.get('user-agent') || '';
  const ip = request.headers.get('cf-connecting-ip') || '';
  const now = new Date();
  const kst = new Date(now.getTime() + 9 * 3600 * 1000);
  const day = kst.toISOString().slice(0, 10);
  let referrer = null;
  try { const r = request.headers.get('referer'); if (r) { const h = new URL(r).hostname; if (h !== url.hostname) referrer = h; } } catch (e) {}
  const device = /Mobi|Android|iPhone|iPad/i.test(ua) ? 'mobile' : 'desktop';
  const country = (request.cf && request.cf.country) || null;
  const visitor = await sha256(`${day}|${ip}|${ua}|readmd-salt-2026`);
  await env.DB.prepare(
    'INSERT INTO pageviews (ts, day, path, referrer, country, device, visitor) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)'
  ).bind(now.toISOString(), day, url.pathname, referrer, country, device, visitor.slice(0, 16)).run();
}

async function sha256(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}
