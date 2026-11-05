#!/usr/bin/env bash
# 원격 D1(readmd-stats)에 미적용 마이그레이션을 적용하고 통계를 한 번 출력한다.
# D1 무료 한도 초과(code 7500)면 RETRY_MAX회까지 RETRY_WAIT초 간격으로 재시도한다.
# 사용: scripts/d1-migrate-remote.sh   (env: RETRY_MAX=6 RETRY_WAIT=600)
set -u
cd "$(dirname "$0")/.."
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
RETRY_MAX=${RETRY_MAX:-6}; RETRY_WAIT=${RETRY_WAIT:-600}
notify() { osascript -e "display notification \"$2\" with title \"readmd D1\" subtitle \"$1\"" >/dev/null 2>&1 || true; }
for i in $(seq 1 "$RETRY_MAX"); do
  echo "== $(date '+%F %T') migrations apply (try $i/$RETRY_MAX)"
  out=$(npx -y wrangler@4 d1 migrations apply readmd-stats --remote 2>&1 | grep -v -Ei 'Experimental|trace-warnings|ES Module')
  echo "$out"
  if echo "$out" | grep -q 'code: 7500'; then
    echo "   D1 한도 아직 초과 — ${RETRY_WAIT}s 후 재시도"; sleep "$RETRY_WAIT"; continue
  fi
  if echo "$out" | grep -qiE 'ERROR'; then
    notify "실패" "migrations apply 오류 — ~/Library/Logs/readmd-d1-migrate.log 확인"; exit 1
  fi
  echo "== $(date '+%F %T') stats 7d"
  bash scripts/stats.sh 7
  notify "완료" "인덱스 적용 + 통계 조회 성공"
  exit 0
done
notify "실패" "D1 한도가 ${RETRY_MAX}회 재시도 후에도 초과 상태"
exit 1
