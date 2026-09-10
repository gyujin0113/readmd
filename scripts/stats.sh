#!/usr/bin/env bash
# 사용: scripts/stats.sh [일수]  (기본 7일) — readmd.kr 방문 통계
set -e
cd "$(dirname "$0")/.."
DAYS=${1:-7}
Q() { npx -y wrangler@4 d1 execute readmd-stats --remote --json --command "$1" | python3 -c "import sys,json; r=json.load(sys.stdin)[0]['results']; print('\n'.join(' | '.join(str(v) for v in row.values()) for row in r) or '(없음)')"; }
echo "== 최근 ${DAYS}일 일별: 날짜 | 페이지뷰 | 방문자 =="
Q "SELECT day, COUNT(*) AS views, COUNT(DISTINCT visitor) AS visitors FROM pageviews WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY day ORDER BY day DESC"
echo; echo "== 유입 출처 (상위 10) =="
Q "SELECT COALESCE(referrer,'(직접/북마크)') AS ref, COUNT(*) AS views FROM pageviews WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY ref ORDER BY views DESC LIMIT 10"
echo; echo "== 국가 =="
Q "SELECT COALESCE(country,'?') AS c, COUNT(*) AS views FROM pageviews WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY c ORDER BY views DESC LIMIT 8"
echo; echo "== 기기 =="
Q "SELECT device, COUNT(*) AS views FROM pageviews WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY device"
echo; echo "== 누적 =="
Q "SELECT COUNT(*) AS total_views, COUNT(DISTINCT visitor||day) AS total_visitor_days, MIN(day) AS since FROM pageviews"
