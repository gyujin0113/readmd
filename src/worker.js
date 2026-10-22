// http → https, www → apex 강제 전환 + HSTS, 그리고 D1에 익명 방문 기록.
// 나머지는 정적 자산(public/) 그대로 서빙.
const PAGES = new Set(['/', '/md-viewer', '/md-file', '/md-to-pdf', '/chatgpt-md']);
// 알려진 크롤러·스캐너·HTTP 라이브러리 UA. 실제 브라우저는 모두 "Mozilla/"로 시작하므로 그 외는 전부 제외.
const BOT_RE = /bot|crawl|spider|slurp|scan|scrapy|curl|wget|python|java|go-http|okhttp|axios|node-fetch|undici|httpclient|libwww|php|ruby|perl|headless|phantom|selenium|puppeteer|playwright|lighthouse|pagespeed|preview|facebookexternalhit|kakaotalk-scrap|monitor|uptime|pingdom|semrush|ahrefs|mj12|dataprovider|bytespider|petalbot|yandex|baidu|sogou|360spider|gptbot|claudebot|ccbot|anthropic|openai|perplexity|censys|shodan|zgrab|masscan|nmap|nuclei|nikto|expanse|palo alto/i;
// 신규/재방문 비콘(public/v.js) 수신 경로. 본문은 { last: 'YYYY-MM-DD' | '' } 하나뿐.
const VISIT_PATH = '/api/v';
const MAX_BEACON_BYTES = 200;
// 중복 집계 방지: 같은 방문자가 같은 경로를 이 시간(초) 안에 다시 열면 기록하지 않음 (새로고침·이중 요청 스캐너)
const DEDUP_SECONDS = 30;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.protocol === 'http:' || url.hostname === 'www.readmd.kr') {
      url.protocol = 'https:';
      if (url.hostname === 'www.readmd.kr') url.hostname = 'readmd.kr';
      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname === VISIT_PATH) {
      if (request.method === 'POST' && env_ok(url) && isHuman(request)) {
        // 응답 후에는 요청 본문을 읽을 수 없으므로 먼저 읽고 기록은 백그라운드로
        const text = await request.text().catch(() => '');
        ctx.waitUntil(logVisit(request, env, text).catch(() => {}));
      }
      return new Response(null, { status: 204 });
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
  if (!PAGES.has(url.pathname)) return false;
  const accept = request.headers.get('accept') || '';
  if (!accept.includes('text/html')) return false;
  if (!isHuman(request)) return false;
  // 최신 브라우저는 페이지 이동 시 Sec-Fetch-Dest: document 를 보냄. 헤더가 있는데 값이 다르면 스크립트/스캐너.
  const dest = request.headers.get('sec-fetch-dest');
  if (dest && dest !== 'document') return false;
  return true;
}
function isHuman(request) {
  const ua = request.headers.get('user-agent') || '';
  if (!ua.startsWith('Mozilla/') || BOT_RE.test(ua)) return false;
  // Cloudflare가 검증한 봇(검색엔진 등)은 UA 문자열과 무관하게 제외
  if (request.cf && request.cf.botManagement && request.cf.botManagement.verifiedBot) return false;
  return true;
}
function env_ok(url) { return url.hostname === 'readmd.kr' || url.hostname.endsWith('.workers.dev'); }

// KST 날짜와 날짜별 익명 방문자 해시 (원본 IP·UA는 저장하지 않음)
async function visitorOf(request, now) {
  const ua = request.headers.get('user-agent') || '';
  const ip = request.headers.get('cf-connecting-ip') || '';
  const day = new Date(now.getTime() + 9 * 3600 * 1000).toISOString().slice(0, 10);
  const visitor = (await sha256(`${day}|${ip}|${ua}|readmd-salt-2026`)).slice(0, 16);
  return { day, visitor, ua };
}

async function logView(request, env, url) {
  const now = new Date();
  const { day, visitor, ua } = await visitorOf(request, now);
  let referrer = null;
  try { const r = request.headers.get('referer'); if (r) { const h = new URL(r).hostname; if (h !== url.hostname) referrer = h; } } catch (e) {}
  const device = /Mobi|Android|iPhone|iPad/i.test(ua) ? 'mobile' : 'desktop';
  const country = (request.cf && request.cf.country) || null;
  // DEDUP_SECONDS 안에 같은 방문자·경로 기록이 있으면 INSERT 자체를 건너뜀 (단일 문장, 경쟁 조건 최소화)
  await env.DB.prepare(
    `INSERT INTO pageviews (ts, day, path, referrer, country, device, visitor)
     SELECT ?1, ?2, ?3, ?4, ?5, ?6, ?7
     WHERE NOT EXISTS (SELECT 1 FROM pageviews WHERE visitor = ?7 AND path = ?3 AND ts >= ?8)`
  ).bind(now.toISOString(), day, url.pathname, referrer, country, device, visitor,
         new Date(now.getTime() - DEDUP_SECONDS * 1000).toISOString()).run();
}

async function logVisit(request, env, text) {
  if (text.length > MAX_BEACON_BYTES) return;
  let last = '';
  try { last = String(JSON.parse(text).last || ''); } catch (e) { return; }
  if (last && !/^\d{4}-\d{2}-\d{2}$/.test(last)) return;
  const now = new Date();
  const { day, visitor } = await visitorOf(request, now);
  if (last >= day) return; // 미래/오늘 날짜는 시계 오차·조작 — 버림
  const gap = last ? Math.round((Date.parse(day) - Date.parse(last)) / 86400000) : null;
  const weekStart = mondayOf(day);
  const weekFirst = !last || last < weekStart ? 1 : 0;
  // 같은 날 같은 방문자는 1행만 (UNIQUE(day, visitor))
  await env.DB.prepare(
    `INSERT OR IGNORE INTO visits (day, is_return, week_first, gap_days, visitor) VALUES (?1, ?2, ?3, ?4, ?5)`
  ).bind(day, last ? 1 : 0, weekFirst, gap, visitor).run();
}

// 'YYYY-MM-DD'가 속한 주의 월요일
function mondayOf(day) {
  const d = new Date(day + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7));
  return d.toISOString().slice(0, 10);
}

async function sha256(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}
