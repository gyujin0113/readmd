# 마크뷰(MarkView) 설계 — 2026-09-09

## 목적
Claude/GPT가 만들어 주는 `.md` 파일을 VS Code 없이 편하게 읽고, 가볍게 고치고, 다시 저장하는 도구.
"홈페이지가 됐든 뭐가 됐든" → 빌드 없는 **단일 HTML 웹앱**으로 결정. 로컬에서 더블클릭해도 열리고, 정적 호스팅(Cloudflare Pages 등)에 그대로 올릴 수 있으며, claude.ai 아티팩트로도 게시 가능.

## 사용자 흐름
1. 브라우저에 `.md` 파일을 드래그해서 놓거나(여러 개 가능) "열기" 버튼으로 선택.
2. 왼쪽 편집기에서 원문을 수정하면 오른쪽 미리보기에 즉시 반영(GitHub/VS Code 미리보기 스타일).
3. 편집기와 미리보기 스크롤 동기화, 가운데 구분선 드래그로 폭 조절, 편집기만/분할/미리보기만 전환.
4. 왼쪽 목차(outline)로 긴 문서 이동.
5. `.md`로 저장(Cmd+S), HTML 내보내기, 인쇄/PDF.
6. 열어 둔 파일과 수정 내용은 localStorage에 저장되어 새로고침해도 유지.

## 구성 요소 (모두 index.html 안)
- **상태**: `files[]`(id, name, text, savedText), `activeId`, `view`(split|editor|preview), `theme`.
- **렌더 파이프라인**: marked(GFM) → 커스텀 renderer(heading id 부여, mermaid 코드블록을 `<pre class="mermaid">`로) → DOMPurify → highlight.js → mermaid(필요할 때만 지연 로드).
- **저장**: 아티팩트 안에서는 `claude.use("downloads")`, 그 외에는 `<a download>`.
- **의존성(cdnjs, 버전 고정)**: marked 12.0.2, highlight.js 11.9.0, dompurify 3.1.6, mermaid 10.9.1. 스타일은 전부 인라인.

## 범위 밖 (v1)
KaTeX 수식, 폴더 전체 열기, 클라우드 동기화, 협업.

## 검증
- 로컬 파일을 헤드리스 브라우저로 열어 렌더/드롭/저장 경로 확인.
- 아티팩트 게시 후 다운로드 capability 동작 확인.
