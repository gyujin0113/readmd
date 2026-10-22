#!/usr/bin/env bash
# 사용: scripts/stats.sh [일수]  (기본 7일) — readmd.kr 방문 통계
set -e
cd "$(dirname "$0")/.."
DAYS=${1:-7}
# 워커 필터 도입(2026-09-11) 이전에 남은 비정상 경로·중복 행은 조회 단계에서 제외
PAGES="'/','/md-viewer','/md-file','/md-to-pdf','/chatgpt-md'"
V="WITH v AS (SELECT a.* FROM pageviews a WHERE a.path IN ($PAGES) AND NOT EXISTS (SELECT 1 FROM pageviews b WHERE b.id<a.id AND b.visitor=a.visitor AND b.path=a.path AND (julianday(a.ts)-julianday(b.ts))*86400 < 30))"
# API 오류를 "(없음)"으로 삼키지 않도록: 실패 시 최대 3회 재시도 후 오류 메시지 출력
RETRIES=3
FMT="import sys,json
try: d=json.load(sys.stdin)
except Exception: sys.exit(2)
if isinstance(d,dict) and 'error' in d:
    e=d['error']; print('ERROR: '+'; '.join([e.get('text','')]+[n.get('text','') for n in e.get('notes',[])]), file=sys.stderr); sys.exit(1)
r=d[0]['results'] if isinstance(d,list) else d.get('result',[{}])[0].get('results',[])
print('\n'.join(' | '.join(str(v) for v in row.values()) for row in r) or '(없음)')"
Q() {
  local out err i
  for i in $(seq 1 $RETRIES); do
    if out=$(npx -y wrangler@4 d1 execute readmd-stats --remote --json --command "$1" 2>/dev/null | python3 -c "$FMT" 2>&1); then
      echo "$out"; return 0
    fi
    err=$out; sleep 2
  done
  echo "(조회 실패 ${RETRIES}회: ${err:-wrangler 응답이 JSON이 아님 — 로그인/네트워크 확인})"
}
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
echo; echo "== 신규/재방문 (일별, 2026-10-22~ 집계): 날짜 | 방문자 | 처음 | 다시 온 사람 =="
Q "SELECT day, COUNT(*), SUM(is_return=0), SUM(is_return) FROM visits WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY day ORDER BY day DESC"
echo; echo "== 주간 재방문자 (월요일 시작): 주 | 다시 온 사람 | 방문자 =="
Q "SELECT date(day, '-' || ((CAST(strftime('%w', day) AS INTEGER) + 6) % 7) || ' days') AS week, SUM(is_return AND week_first), SUM(week_first) FROM visits WHERE day >= date('now','+9 hours','-${DAYS} days') GROUP BY week ORDER BY week DESC"
echo; echo "== 재방문 간격: 며칠 만에 | 횟수 =="
Q "SELECT CASE WHEN gap_days=1 THEN '1일(연속)' WHEN gap_days<=7 THEN '2~7일' WHEN gap_days<=30 THEN '8~30일' ELSE '31일+' END AS g, COUNT(*) FROM visits WHERE is_return=1 AND day >= date('now','+9 hours','-${DAYS} days') GROUP BY g ORDER BY MIN(gap_days)"
echo; echo "== 누적 =="
Q "$V SELECT COUNT(*) AS total_views, COUNT(DISTINCT visitor||day) AS total_visitor_days, MIN(day) AS since FROM v"
