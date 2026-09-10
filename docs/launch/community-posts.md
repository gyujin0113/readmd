# ReadMD 출시 소개글 초안

공통 원칙: 문제 → 만든 이유 → GIF/스크린샷 → 링크 → "오픈소스, 의견 환영". 링크는 글당 한 번. 홍보 티 내지 않기.
첨부: `og.png` 또는 15초 사용 GIF(파일 드롭 → 편집 → 저장).

---

## 1. GeekNews (news.hada.io) — 제목 + 본문

**제목**: ReadMD - AI가 만들어 준 .md 파일을 설치 없이 바로 읽는 마크다운 뷰어

**본문**:
Claude, ChatGPT가 결과물을 .md 파일로 주는 일이 많아졌는데, 막상 열어 보려면 VS Code를 켜야 해서 불편했습니다. 앱스토어에도 쓸 만한 뷰어가 별로 없어서 브라우저용으로 하나 만들었습니다.

- .md 파일을 창에 끌어다 놓으면 바로 열림 (여러 개 동시, 탭 전환)
- 왼쪽 편집 / 오른쪽 GitHub 스타일 미리보기, 스크롤 동기화
- 표·체크리스트·코드 하이라이트·Mermaid 지원
- .md 저장, HTML 내보내기, PDF(인쇄)
- 파일은 브라우저 안에서만 처리, 서버 전송 없음
- 빌드 없이 HTML 파일 하나, MIT 오픈소스

https://readmd.kr
GitHub: https://github.com/gyujin0113/readmd

부족한 점이나 있었으면 하는 기능 알려 주시면 반영하겠습니다.

---

## 2. 클리앙 (팁과강좌 또는 자유게시판)

**제목**: 클로드/챗GPT가 주는 md 파일 편하게 보려고 뷰어 하나 만들었습니다 (무료, 설치 없음)

**본문**:
요즘 AI가 정리해 주는 문서가 죄다 .md 파일이잖아요. 근데 이걸 보려면 VS Code 깔거나 메모장으로 열어서 #### 기호 보면서 읽어야 해서 답답하더라고요.

그래서 브라우저에서 바로 열리는 뷰어를 만들었습니다.

[스크린샷/GIF]

- 파일을 창에 끌어다 놓으면 끝. 설치, 회원가입 없음
- 왼쪽에서 고치면 오른쪽에 바로 반영
- 표, 체크박스, 코드, 다이어그램 다 나옴
- 고친 건 .md로 다시 저장, 필요하면 PDF로도
- 올린 파일은 서버로 안 갑니다. 브라우저 안에서만 처리돼서 회사 문서 열어도 됩니다

readmd.kr

오픈소스라 코드도 다 공개돼 있고요, 불편한 점 말씀해 주시면 고치겠습니다.

---

## 3. 네이버 카페 / 블로그 (비개발자용, "사용법" 톤)

**제목**: 챗GPT가 준 md 파일 여는 법 (설치 없이 3초)

**본문**:
챗GPT나 클로드한테 문서 정리를 시키면 ".md 파일"로 다운로드되는 경우가 있죠. 더블클릭하면 메모장으로 열리고 기호만 잔뜩 보여서 당황하셨을 겁니다.

md는 "마크다운"이라는 문서 형식인데, 전용 뷰어로 열어야 제목·표·목록이 제대로 보입니다.

가장 쉬운 방법은 브라우저에서 readmd.kr 에 접속해서 파일을 창에 끌어다 놓는 겁니다. 설치도 가입도 필요 없고, 파일이 어디로 업로드되지 않아서 개인 문서도 괜찮습니다.

[스크린샷: 드롭 전/후]

내용을 고칠 수도 있고, 고친 걸 다시 .md로 저장하거나 PDF로 뽑을 수도 있습니다.

---

## 4. Threads / X (짧은 글)

AI가 만들어 준 .md 파일, 열 때마다 VS Code 켜기 귀찮아서 브라우저 뷰어 만들었습니다.
끌어다 놓으면 끝. 서버 전송 없음. 무료·오픈소스.
readmd.kr

---

## 5. Show HN (영문, 선택)

**Title**: Show HN: ReadMD – A zero-install browser viewer/editor for .md files from AI chats

**Text**:
I kept getting .md files from Claude/ChatGPT and had to open VS Code just to read them. ReadMD is a single HTML file: drop a .md, edit on the left, GitHub-style preview on the right, save back as .md/HTML/PDF. Files never leave the browser (no upload). Supports GFM tables, task lists, highlight.js, Mermaid. MIT licensed. Feedback welcome.

https://readmd.kr — https://github.com/gyujin0113/readmd

---

## 올리는 순서 (제안)

| 일차 | 채널 | 목적 |
|---|---|---|
| D+0 | GeekNews | 개발자 피드백, 버그 조기 발견 |
| D+1 | 클리앙 | 대중 반응, 트래픽 |
| D+3 | Threads, 커리어리, 디스콰이엇 | 2차 확산 |
| D+7 | 네이버 카페(챗GPT/클로드 사용자 모임), 블로그 글 2~3개 | 검색 유입(장기) |
| D+14 | Show HN, Product Hunt (선택) | 해외 |

첫 주에 들어온 요청 중 작은 것 2~3개를 바로 반영하고 원글에 "반영했습니다" 댓글 달기.
