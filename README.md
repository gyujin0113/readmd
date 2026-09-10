# ReadMD

**https://readmd.kr** — `.md` 파일을 설치 없이 브라우저에서 바로 읽고, 고치고, 저장하는 무료 마크다운 뷰어.

Claude, ChatGPT 같은 AI가 만들어 주는 `.md` 파일을 VS Code 없이 편하게 보려고 만들었습니다.
파일은 **브라우저 안에서만** 처리되며 어떤 서버로도 전송되지 않습니다.

## 기능

- `.md` 파일 드래그 앤 드롭으로 열기 (여러 개 동시, 탭 전환)
- 왼쪽 편집 · 오른쪽 미리보기 (GitHub / VS Code 스타일), 스크롤 동기화, 폭 조절
- 편집 / 분할 / 미리보기 모드, 목차(outline) 패널
- GFM 표·체크리스트·각주, 코드 하이라이트, Mermaid 다이어그램
- `.md` 저장(⌘S), HTML 내보내기, 인쇄 / PDF 저장
- 다크 · 라이트 테마, 열어 둔 문서 자동 보관(localStorage)

## 구조

빌드 도구 없이 `public/index.html` 파일 하나로 동작합니다. 로컬에서 그냥 더블클릭해도 열립니다.

| 라이브러리 | 용도 |
|---|---|
| [marked](https://github.com/markedjs/marked) 12 | Markdown → HTML |
| [DOMPurify](https://github.com/cure53/DOMPurify) 3 | HTML 살균 |
| [highlight.js](https://highlightjs.org/) 11 | 코드 하이라이트 |
| [Mermaid](https://mermaid.js.org/) 10 | 다이어그램 (필요할 때만 로드) |

## 배포

Cloudflare Workers 정적 자산(Static Assets) 호스팅입니다. `src/worker.js`는 http→https, www→apex 리디렉션과 HSTS 헤더만 담당합니다.

```bash
npx wrangler deploy
```

## 기여

버그 제보, 기능 제안, PR 모두 환영합니다. [Issues](https://github.com/gyujin0113/readmd/issues)에 남겨 주세요.

## 라이선스

[MIT](LICENSE) © 2026 주식회사 쓰리앤디

## 방문 통계

외부 분석 스크립트 없이, Worker가 HTML 요청마다 D1(`readmd-stats`)에 익명 기록을 남깁니다.
저장하는 것: 시각, 경로, 유입 출처 도메인, 국가, 기기 종류, 날짜별 익명 해시(IP·UA·날짜를 해시한 값, 원본 저장 안 함). 쿠키를 쓰지 않습니다.

```bash
scripts/stats.sh        # 최근 7일
scripts/stats.sh 30     # 최근 30일
```
