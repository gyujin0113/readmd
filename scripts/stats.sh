#!/usr/bin/env bash
# 사용: scripts/stats.sh [일수]  (기본 7일) — readmd.kr 방문 통계
set -e
cd "$(dirname "$0")/.."
DAYS=${1:-7}
# 워커 필터 도입(2026-09-11) 이전에 남은 비정상 경로·중복 행은 조회 단계에서 제외
PAGES="'/','/md-viewer','/md-file','/md-to-pdf','/chatgpt-md'"
V="WITH v AS (SELECT a.* FROM pageviews a WHERE a.path IN ($PAGES) AND NOT EXISTS (SELECT 1 FROM pageviews b WHERE b.id<a.id AND b.visitor=a.visitor AND b.path=a.path AND (julianday(a.ts)-julianday(b.ts))*86400 < 30))"
Q() { npx -y wrangler@4 d1 execute readmd-stats --remote --json --command "$1" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); r=d[0]['results'] if isinstance(d,list) else d.get('result',[{}])[0].get('results',[]); print('\n'.join(' | '.join(str(v) for v in row.values()) for row in r) or '(없음)')"; }
echo "== 최근 ${DAYS}일 일별: 날짜 | 페이지뷰 | 방문자 =="
Q "$V SELECT day, COUNT(*) AS views, COUNT(DISTINCT visitor) AS visitors FROM v WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY day ORDER BY day DESC"
echo; echo "== 유입 출처 (상위 10) =="
Q "$V SELECT COALESCE(referrer,'(직접/북마크)') AS ref, COUNT(*) AS views FROM v WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY ref ORDER BY views DESC LIMIT 10"
echo; echo "== 국가 =="
Q "$V SELECT COALESCE(country,'?') AS c, COUNT(*) AS views FROM v WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY c ORDER BY views DESC LIMIT 8"
echo; echo "== 기기 =="
Q "$V SELECT device, COUNT(*) AS views FROM v WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY device"
echo; echo "== 경로별 =="
Q "$V SELECT path, COUNT(*) AS views, COUNT(DISTINCT visitor||day) AS visitors FROM v WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY path ORDER BY views DESC"
echo; echo "== 누적 =="
Q "$V SELECT COUNT(*) AS total_views, COUNT(DISTINCT visitor||day) AS total_visitor_days, MIN(day) AS since FROM v"
