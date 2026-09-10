#!/usr/bin/env python3
"""첫 화면 예시 문서를 정적 HTML로 index.html에 심는다(자바스크립트를 못 읽는 검색 봇용).
실행: python3 scripts/prerender.py  (헤드리스 Chrome 필요)"""
import subprocess, re, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
IDX = ROOT / "public" / "index.html"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=8000", "--dump-dom", f"file://{IDX}"],
                     capture_output=True, text=True).stdout
m = re.search(r'<article class="md" id="md">([\s\S]*?)</article>', dom)
assert m, "article not found in dumped DOM"
inner = m.group(1)
# Mermaid SVG는 원문으로 되돌린다 (JS가 다시 그림)
inner = re.sub(r'<pre class="mermaid"[^>]*data-src="([^"]*)"[^>]*>[\s\S]*?</pre>',
               lambda mm: '<pre class="mermaid">' + mm.group(1) + '</pre>', inner)
inner = re.sub(r'\s*data-processed="true"', '', inner)
src = IDX.read_text(encoding="utf-8")
new = re.sub(r'<article class="md" id="md">[\s\S]*?</article>', lambda _: '<article class="md" id="md">' + inner + '</article>', src, count=1)
IDX.write_text(new, encoding="utf-8")
print(f"prerendered {len(inner):,} chars into index.html")
