-- 워커의 30초 중복 검사(INSERT ... WHERE NOT EXISTS visitor/path/ts)가 매 페이지뷰마다
-- 테이블 전체를 읽던 것을 인덱스 조회로 바꾼다. D1 무료 한도(일 500만 행 읽기) 보호용.
CREATE INDEX IF NOT EXISTS idx_pageviews_visitor_path_ts ON pageviews(visitor, path, ts);
