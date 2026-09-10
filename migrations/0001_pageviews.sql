CREATE TABLE IF NOT EXISTS pageviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,            -- ISO 8601 UTC
  day TEXT NOT NULL,           -- YYYY-MM-DD (KST)
  path TEXT NOT NULL,
  referrer TEXT,               -- 유입 출처 도메인만 (경로 제외)
  country TEXT,
  device TEXT,                 -- mobile | desktop
  visitor TEXT NOT NULL        -- 날짜별 익명 해시 (IP+UA+날짜), 원본 저장 안 함
);
CREATE INDEX IF NOT EXISTS idx_pageviews_day ON pageviews(day);
CREATE INDEX IF NOT EXISTS idx_pageviews_ref ON pageviews(referrer);
