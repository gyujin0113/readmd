-- 신규/재방문 집계용. 사람을 구별하는 ID 없이, 브라우저가 기억한 "마지막 방문일"에서 파생한 값만 저장.
-- 하루 1행 (방문자 해시는 pageviews와 같은 날짜별 해시 — 같은 날 중복 방지에만 사용).
CREATE TABLE IF NOT EXISTS visits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  day TEXT NOT NULL,           -- YYYY-MM-DD (KST)
  is_return INTEGER NOT NULL,  -- 1 = 전에 온 적 있음, 0 = 첫 방문
  week_first INTEGER NOT NULL, -- 1 = 이번 주(월요일 시작, KST) 첫 방문
  gap_days INTEGER,            -- 마지막 방문 후 경과 일수 (첫 방문이면 NULL)
  visitor TEXT NOT NULL        -- 날짜별 익명 해시 (IP+UA+날짜)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_visits_day_visitor ON visits(day, visitor);
