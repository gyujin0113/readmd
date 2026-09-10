#!/usr/bin/env python3
"""검색 의도별 안내 페이지 생성기. 실행: python3 scripts/build-guides.py → public/*.html, sitemap.xml"""
import json, datetime, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
TODAY = datetime.date.today().isoformat()

PAGES = [
  {
    "slug": "md-viewer",
    "title": "MD 뷰어 - 설치 없이 md 파일 바로 열기 | ReadMD",
    "desc": "md 뷰어를 찾고 계신가요? 파일을 창에 끌어다 놓으면 바로 읽힙니다. 설치·가입 없이 쓰는 무료 마크다운 뷰어, 편집과 PDF 저장까지.",
    "h1": "MD 뷰어, 설치 없이 바로 쓰기",
    "lead": "md 파일을 아래에 끌어다 놓으면 그 자리에서 읽힙니다. 프로그램 설치도, 회원가입도 없습니다.",
    "sections": [
      ("md 뷰어가 왜 필요한가요", """md 파일은 마크다운(Markdown)이라는 형식으로 쓴 텍스트 문서입니다. 더블클릭하면 메모장이나 텍스트 편집기로 열리는데, 그러면 <code>#</code>, <code>-</code>, <code>|</code> 같은 기호만 잔뜩 보이고 제목이나 표가 제대로 보이지 않습니다. 이 기호를 실제 서식으로 바꿔서 보여 주는 도구가 md 뷰어(마크다운 뷰어)입니다.<br><br>요즘은 ChatGPT나 Claude 같은 AI가 정리해 주는 문서, 개발 프로젝트의 README, 노션에서 내보낸 메모가 대부분 md 파일이라 뷰어가 하나쯤 필요합니다."""),
      ("ReadMD로 여는 방법", """<ol><li>이 페이지나 <a href="/">readmd.kr</a> 창 아무 곳에나 md 파일을 끌어다 놓습니다.</li><li>오른쪽에 제목, 목록, 표, 코드가 서식대로 보입니다. 왼쪽에는 원문이 있어서 바로 고칠 수 있습니다.</li><li>필요하면 <strong>.md 저장</strong>으로 고친 파일을 내려받거나, <strong>PDF</strong> 버튼으로 PDF로 저장합니다.</li></ol>여러 파일을 한 번에 끌어다 놓으면 탭으로 나뉘어 열립니다. 휴대폰 브라우저에서는 "열기" 버튼으로 파일을 고르면 됩니다."""),
      ("다른 md 뷰어와 다른 점", """<ul><li><strong>설치가 없습니다.</strong> VS Code나 Typora 같은 프로그램을 깔지 않아도 되고, 크롬 확장 프로그램도 필요 없습니다.</li><li><strong>파일이 서버로 가지 않습니다.</strong> 온라인 뷰어 대부분은 파일을 서버에 올려서 변환하는데, ReadMD는 브라우저 안에서만 처리합니다. 회사 문서를 열어도 됩니다.</li><li><strong>읽기만이 아니라 고칠 수 있습니다.</strong> 왼쪽에서 고치면 오른쪽에 바로 반영되고, 고친 파일을 다시 md로 저장합니다.</li><li><strong>표, 체크리스트, 코드 하이라이트, Mermaid 다이어그램</strong>까지 GitHub에서 보이는 그대로 보여 줍니다.</li><li><strong>무료이고 오픈소스</strong>입니다. 코드가 GitHub에 공개되어 있습니다.</li></ul>"""),
    ],
    "faq": [
      ("md 뷰어를 따로 설치해야 하나요?", "아니요. 브라우저에서 readmd.kr을 열고 파일을 끌어다 놓으면 끝입니다. 윈도우, 맥, 휴대폰 어디서나 됩니다."),
      ("파일이 외부로 전송되나요?", "아니요. 파일은 사용자의 브라우저 안에서만 읽히며 어떤 서버에도 올라가지 않습니다."),
      ("md 파일을 고칠 수도 있나요?", "네. 왼쪽 편집 창에서 고치면 오른쪽 미리보기에 바로 반영되고, .md 저장 버튼으로 내려받을 수 있습니다."),
      ("PDF나 워드로 바꿀 수 있나요?", "PDF는 PDF 버튼으로 바로 저장할 수 있습니다. HTML 내보내기도 됩니다. 워드(.docx) 변환은 준비 중입니다."),
    ],
  },
  {
    "slug": "md-file",
    "title": "MD 파일이란? md 파일 여는 법 (설치 없이 3초) | ReadMD",
    "desc": "md 파일은 마크다운 형식의 텍스트 문서입니다. 메모장으로 열면 기호만 보이는 이유와, 설치 없이 브라우저에서 md 파일을 제대로 여는 방법을 설명합니다.",
    "h1": "MD 파일이란? 여는 법까지 한 번에",
    "lead": "md 파일을 받았는데 열어 보니 기호만 잔뜩 보이셨나요? 아래에 파일을 끌어다 놓으면 제대로 보입니다.",
    "sections": [
      ("md 파일이란", """확장자가 <code>.md</code>인 파일은 <strong>마크다운(Markdown)</strong>으로 쓴 텍스트 문서입니다. 마크다운은 2004년에 만들어진 간단한 문서 규칙으로, 워드처럼 버튼을 눌러 서식을 주는 대신 기호로 표시합니다.<br><br><ul><li><code># 제목</code> → 큰 제목, <code>## 제목</code> → 작은 제목</li><li><code>- 항목</code> → 글머리 목록, <code>1. 항목</code> → 번호 목록</li><li><code>**굵게**</code> → <strong>굵게</strong>, <code>*기울임*</code> → <em>기울임</em></li><li><code>| 칸 | 칸 |</code> → 표, <code>- [ ] 할 일</code> → 체크리스트</li></ul>내용이 순수한 글자라서 용량이 작고, 어떤 프로그램에서도 열리고, GitHub·노션·옵시디언·ChatGPT·Claude가 모두 이 형식을 씁니다."""),
      ("메모장으로 열면 기호만 보이는 이유", """md 파일은 어디까지나 텍스트 파일이라 메모장이나 텍스트 편집기가 기본으로 열립니다. 그러면 <code>#</code>이나 <code>**</code> 같은 기호가 서식으로 바뀌지 않고 그대로 보입니다. 내용은 읽을 수 있지만 표가 깨지고 제목 구분이 안 됩니다.<br><br>서식대로 보려면 <strong>마크다운 뷰어</strong>로 열어야 합니다. 개발자는 VS Code 같은 편집기를 쓰지만, 그냥 읽기만 하려는 사람에게는 과합니다."""),
      ("설치 없이 md 파일 여는 법", """<ol><li>브라우저에서 <a href="/">readmd.kr</a>을 엽니다. 이 페이지에서도 됩니다.</li><li>md 파일을 창에 끌어다 놓습니다. 휴대폰에서는 "열기" 버튼을 누르고 파일을 고릅니다.</li><li>제목, 표, 목록, 코드가 서식대로 보입니다. 고칠 수도 있고, PDF로 저장할 수도 있습니다.</li></ol>파일은 브라우저 안에서만 처리되고 어디에도 업로드되지 않습니다."""),
      ("md 파일을 여는 다른 방법", """<ul><li><strong>VS Code</strong>: 무료 편집기. 파일을 연 뒤 미리보기 버튼을 누릅니다. 개발자라면 이미 있을 겁니다.</li><li><strong>Typora, Obsidian, MarkText</strong>: 설치형 마크다운 편집기. 자주 쓴다면 좋지만 한두 번 열어 보려고 깔기엔 무겁습니다.</li><li><strong>크롬 확장 프로그램</strong>: 브라우저에 설치하면 md 파일을 열 때 서식으로 보여 줍니다. 파일 접근 권한을 줘야 합니다.</li><li><strong>ReadMD</strong>: 설치 없이 브라우저에서 바로. 가끔 열어 보는 사람에게 가장 빠릅니다.</li></ul>"""),
    ],
    "faq": [
      ("md 파일은 위험한가요?", "아니요. 글자만 들어 있는 텍스트 파일이라 실행되지 않습니다. 워드 매크로 같은 위험이 없습니다."),
      ("md 파일을 워드나 한글로 바꿀 수 있나요?", "ReadMD에서 HTML로 내보낸 뒤 워드에서 열면 서식이 대부분 유지됩니다. PDF는 바로 저장됩니다."),
      ("md 파일은 어떻게 만드나요?", "메모장에 마크다운 규칙으로 쓰고 .md로 저장하면 됩니다. ReadMD의 '새 문서'에서 써서 저장해도 됩니다."),
      ("휴대폰에서도 열리나요?", "네. 휴대폰 브라우저에서 readmd.kr을 열고 '열기' 버튼으로 파일을 고르면 됩니다."),
    ],
  },
  {
    "slug": "md-to-pdf",
    "title": "마크다운 PDF 변환 - md 파일을 PDF로 저장 (설치 없이) | ReadMD",
    "desc": "md 파일을 PDF로 바꾸는 가장 쉬운 방법. 파일을 끌어다 놓고 PDF 버튼만 누르면 됩니다. 설치·가입·업로드 없이 브라우저에서 바로 변환.",
    "h1": "마크다운을 PDF로, 버튼 하나로",
    "lead": "md 파일을 아래에 끌어다 놓고 PDF 버튼을 누르면 미리보기에 보이는 그대로 PDF가 됩니다.",
    "sections": [
      ("md 파일을 PDF로 저장하는 방법", """<ol><li>md 파일을 이 페이지나 <a href="/">readmd.kr</a>에 끌어다 놓습니다.</li><li>오른쪽 미리보기에서 서식이 제대로 보이는지 확인합니다. 필요하면 왼쪽에서 고칩니다.</li><li>상단의 <strong>PDF</strong> 버튼을 누릅니다. 브라우저 인쇄 창이 열립니다.</li><li>대상(프린터)을 <strong>"PDF로 저장"</strong>으로 고르고 저장합니다.</li></ol>제목, 표, 목록, 코드 블록, 체크리스트가 화면에 보이는 그대로 PDF에 들어갑니다. 편집기와 버튼은 빠지고 문서만 인쇄됩니다."""),
      ("변환 사이트에 올리지 않아도 되는 이유", """마크다운 PDF 변환 사이트는 대부분 파일을 서버에 올려서 변환한 뒤 내려받게 합니다. 회사 문서나 계약 내용이 담긴 파일이라면 꺼림칙합니다.<br><br>ReadMD는 파일을 브라우저 안에서 서식으로 바꾸고, PDF는 브라우저의 인쇄 기능으로 만듭니다. 파일이 컴퓨터 밖으로 나가지 않습니다. 회원가입도, 하루 변환 횟수 제한도 없습니다."""),
      ("보기 좋게 뽑는 팁", """<ul><li>인쇄 창에서 <strong>여백</strong>을 "기본" 또는 "좁게"로 두면 A4 한 장에 더 많이 들어갑니다.</li><li>표가 넓으면 <strong>가로 방향</strong>으로 바꾸세요.</li><li><strong>배경 그래픽</strong> 옵션을 켜면 코드 블록의 회색 배경과 인용문 표시가 유지됩니다.</li><li>PDF 대신 HTML로 내보내면(HTML 버튼) 메일이나 메신저로 보냈을 때 받는 사람이 바로 열 수 있습니다.</li></ul>"""),
    ],
    "faq": [
      ("md를 PDF로 바꾸는 데 돈이 드나요?", "아니요. ReadMD는 무료이고 횟수 제한이 없습니다."),
      ("워드(docx)로도 바꿀 수 있나요?", "HTML로 내보낸 뒤 워드에서 열면 서식이 대부분 유지됩니다. 바로 .docx로 내보내는 기능은 준비 중입니다."),
      ("PDF에 편집기 화면도 같이 나오나요?", "아니요. 인쇄할 때는 미리보기 문서만 나오고 편집기와 버튼은 빠집니다."),
      ("휴대폰에서도 PDF로 저장되나요?", "네. 휴대폰 브라우저의 공유/인쇄 메뉴에서 PDF로 저장을 고르면 됩니다."),
    ],
  },
  {
    "slug": "chatgpt-md",
    "title": "ChatGPT·Claude가 준 md 파일 여는 법 (설치 없이) | ReadMD",
    "desc": "ChatGPT나 Claude가 다운로드해 준 .md 파일, 열어 보니 기호만 보이나요? 브라우저에 끌어다 놓으면 바로 제대로 읽히고 고칠 수 있습니다.",
    "h1": "ChatGPT·Claude가 준 md 파일, 바로 읽기",
    "lead": "AI가 만들어 준 .md 파일을 아래에 끌어다 놓으세요. 제목, 표, 체크리스트가 제대로 보입니다.",
    "sections": [
      ("AI는 왜 md 파일로 주나요", """ChatGPT, Claude, Gemini 같은 AI는 답변을 마크다운으로 씁니다. 제목은 <code>#</code>, 목록은 <code>-</code>, 표는 <code>|</code>로 표시하는 방식이라, 문서로 내보낼 때도 그대로 <code>.md</code> 파일이 됩니다. 채팅 화면에서는 예쁘게 보였는데 파일을 열면 기호만 보이는 이유가 이것입니다.<br><br>워드 파일로 달라고 하면 되지만, 표나 코드가 깨지는 경우가 많아서 md 파일 그대로 받아 뷰어로 여는 편이 깔끔합니다."""),
      ("받은 md 파일 여는 방법", """<ol><li>AI가 준 파일을 내려받습니다. 보통 <code>보고서.md</code>, <code>정리.md</code> 같은 이름입니다.</li><li>브라우저에서 <a href="/">readmd.kr</a>을 열고 파일을 끌어다 놓습니다. 이 페이지에서도 됩니다.</li><li>서식대로 보이면 그대로 읽고, 고칠 부분은 왼쪽에서 고칩니다.</li><li><strong>.md 저장</strong>으로 다시 내려받거나, <strong>PDF</strong>로 저장해서 공유합니다.</li></ol>Claude Code나 Cursor 같은 도구가 프로젝트 폴더에 만들어 주는 <code>README.md</code>, <code>PLAN.md</code> 같은 파일도 똑같이 열립니다."""),
      ("AI 문서를 다룰 때 편한 기능", """<ul><li><strong>여러 파일 동시 열기</strong>: 한 번에 만들어 준 문서 여러 개를 끌어다 놓으면 탭으로 나뉩니다.</li><li><strong>목차</strong>: 긴 보고서는 왼쪽 목차로 바로 이동합니다.</li><li><strong>Mermaid 다이어그램</strong>: AI가 그려 준 순서도·구조도가 그림으로 보입니다.</li><li><strong>체크리스트</strong>: 할 일 목록이 체크박스로 보입니다.</li><li><strong>서버 전송 없음</strong>: AI에게 물어본 회사 자료를 다시 어디에 올릴 필요가 없습니다.</li></ul>"""),
    ],
    "faq": [
      ("ChatGPT가 md 파일을 안 주고 화면에만 보여 줘요.", "\"이 내용을 .md 파일로 만들어서 다운로드 링크를 줘\"라고 요청하면 파일로 줍니다. 아니면 답변을 복사해서 ReadMD의 '새 문서'에 붙여 넣어도 됩니다."),
      ("Claude 아티팩트로 받은 md도 되나요?", "네. 내려받은 .md 파일을 끌어다 놓으면 됩니다."),
      ("AI가 준 파일을 고쳐서 다시 AI에게 줄 수 있나요?", "네. 왼쪽에서 고친 뒤 .md 저장으로 내려받아 다시 올리면 됩니다."),
      ("문서 내용이 어디로 전송되나요?", "아무 데도 가지 않습니다. 브라우저 안에서만 처리됩니다."),
    ],
  },
]

CSS = """
:root{--bg:#f3f4f7;--surface:#fff;--surface-2:#eaecf1;--line:#d8dbe3;--ink:#1b1f27;--ink-2:#4b5262;--ink-3:#7a8194;--accent:#2f56d9;--accent-ink:#fff;--accent-soft:#e6ecfb;--code-bg:#f0f2f6;--sans:"IBM Plex Sans KR","Apple SD Gothic Neo","Noto Sans KR",system-ui,sans-serif;--mono:"IBM Plex Mono","SF Mono",Menlo,monospace;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121419;--surface:#1a1d24;--surface-2:#22262f;--line:#2e333e;--ink:#e7e9ef;--ink-2:#aab0be;--ink-3:#737a8a;--accent:#7d9bff;--accent-ink:#0f1320;--accent-soft:#25304f;--code-bg:#252a34;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#121419;--surface:#1a1d24;--surface-2:#22262f;--line:#2e333e;--ink:#e7e9ef;--ink-2:#aab0be;--ink-3:#737a8a;--accent:#7d9bff;--accent-ink:#0f1320;--accent-soft:#25304f;--code-bg:#252a34;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.75}
a{color:var(--accent)}
.top{display:flex;align-items:center;gap:10px;padding:10px 20px;background:var(--surface);border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:8px;font-weight:700;color:inherit;text-decoration:none}
.mark{width:24px;height:22px;border-radius:6px;background:var(--accent);color:var(--accent-ink);display:grid;place-items:center;font-family:var(--mono);font-size:10px;font-weight:600}
.top .cta{margin-left:auto}
.cta{display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:8px;background:var(--accent);color:var(--accent-ink);text-decoration:none;font-weight:600;white-space:nowrap}
.cta:hover{filter:brightness(1.08)}
main{max-width:720px;margin:0 auto;padding:36px 20px 80px}
h1{font-size:2rem;line-height:1.25;letter-spacing:-.02em;margin:0 0 12px;text-wrap:balance}
.lead{font-size:1.1rem;color:var(--ink-2);margin:0 0 20px}
.drop{border:2px dashed var(--line);border-radius:14px;padding:28px 20px;text-align:center;background:var(--surface);cursor:pointer;margin:0 0 36px;transition:.15s}
.drop:hover,.drop.on{border-color:var(--accent);background:var(--accent-soft)}
.drop b{display:block;font-size:1.15rem;margin-bottom:4px}.drop span{color:var(--ink-3);font-size:.95rem}
h2{font-size:1.35rem;margin:36px 0 10px;letter-spacing:-.01em}
h3{font-size:1.05rem;margin:22px 0 6px}
ol,ul{padding-left:1.4em}li{margin:.3em 0}
code{font-family:var(--mono);font-size:.9em;background:var(--code-bg);padding:.1em .35em;border-radius:4px}
.faq details{border-top:1px solid var(--line);padding:10px 0}.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;font-weight:600}.faq p{margin:8px 0 0;color:var(--ink-2)}
.bottom{margin-top:44px;padding:24px;border-radius:14px;background:var(--surface);border:1px solid var(--line);text-align:center}
.bottom p{margin:0 0 12px;color:var(--ink-2)}
nav.more{margin-top:36px;font-size:.92rem;color:var(--ink-3)}nav.more a{margin-right:12px}
footer{text-align:center;color:var(--ink-3);font-size:.85rem;padding:20px}
input[type=file]{display:none}
"""

JS = """
(function(){
  const drop=document.getElementById('drop'), input=document.getElementById('file');
  const OK=/\\.(md|markdown|mdx|txt)$/i;
  async function go(list){
    const f=Array.from(list).find(x=>OK.test(x.name)||/^text\\//.test(x.type));
    if(!f){alert('.md, .markdown, .txt 파일만 열 수 있습니다.');return;}
    const text=await f.text();
    try{localStorage.setItem('readmd.handoff',JSON.stringify({name:f.name,text}));}catch(e){}
    location.href='/';
  }
  drop.addEventListener('click',()=>input.click());
  input.addEventListener('change',()=>go(input.files));
  let d=0;
  window.addEventListener('dragenter',e=>{if(e.dataTransfer&&Array.from(e.dataTransfer.types).includes('Files')){d++;drop.classList.add('on');}});
  window.addEventListener('dragleave',()=>{if(--d<=0){d=0;drop.classList.remove('on');}});
  window.addEventListener('dragover',e=>e.preventDefault());
  window.addEventListener('drop',e=>{e.preventDefault();d=0;drop.classList.remove('on');if(e.dataTransfer.files.length)go(e.dataTransfer.files);});
})();
"""

def page(p):
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]}
    sections = "\n".join(f"<h2>{html.escape(h)}</h2>\n<p>{body}</p>" for h,body in p["sections"])
    faq = "\n".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in p["faq"])
    more = " · ".join(f'<a href="/{o["slug"]}">{html.escape(o["h1"])}</a>' for o in PAGES if o["slug"]!=p["slug"])
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p["title"])}</title>
<meta name="description" content="{html.escape(p["desc"])}">
<link rel="canonical" href="https://readmd.kr/{p["slug"]}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ReadMD">
<meta property="og:title" content="{html.escape(p["h1"])}">
<meta property="og:description" content="{html.escape(p["desc"])}">
<meta property="og:url" content="https://readmd.kr/{p["slug"]}">
<meta property="og:image" content="https://readmd.kr/og.png">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
</head>
<body>
<header class="top">
  <a class="brand" href="/"><span class="mark">MD</span><span>ReadMD</span></a>
  <a class="cta" href="/">md 파일 바로 열기</a>
</header>
<main>
  <h1>{html.escape(p["h1"])}</h1>
  <p class="lead">{html.escape(p["lead"])}</p>
  <div class="drop" id="drop" role="button" tabindex="0"><b>여기에 md 파일을 끌어다 놓으세요</b><span>또는 클릭해서 파일 선택 · 설치 없음 · 서버 전송 없음</span></div>
  <input type="file" id="file" accept=".md,.markdown,.mdx,.txt,text/markdown,text/plain">
  {sections}
  <h2>자주 묻는 질문</h2>
  <div class="faq">{faq}</div>
  <div class="bottom"><p>파일을 끌어다 놓기만 하면 됩니다. 설치도 가입도 없습니다.</p><a class="cta" href="/">md 파일 바로 열기</a></div>
  <nav class="more">더 알아보기: {more} · <a href="https://github.com/gyujin0113/readmd" target="_blank" rel="noopener">GitHub</a></nav>
</main>
<footer>© 2026 ReadMD · 주식회사 쓰리앤디 · MIT 오픈소스</footer>
<script>{JS}</script>
</body>
</html>
"""

for p in PAGES:
    (PUB / f'{p["slug"]}.html').write_text(page(p), encoding="utf-8")
    print("wrote", p["slug"] + ".html")

urls = ["https://readmd.kr/"] + [f'https://readmd.kr/{p["slug"]}' for p in PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(
    f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{"1.0" if u.endswith("/") else "0.8"}</priority></url>' for u in urls) + "\n</urlset>\n"
(PUB / "sitemap.xml").write_text(sm, encoding="utf-8")
print("wrote sitemap.xml")
