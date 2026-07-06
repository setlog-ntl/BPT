# -*- coding: utf-8 -*-
"""
도입부 분석 — 통합 대시보드 생성기 (안전: 분석.html은 읽기만, 대시보드.html만 출력)
사용: python3 build_dashboard.py
영상 분석 추가 후 이 스크립트만 재실행하면 대시보드가 자동 반영됩니다.
"""
import os, re, datetime
from urllib.parse import quote
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "대시보드.html")

def find_files():
    out = []
    for dp, dirs, fns in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        segs = [] if rel == "." else rel.split(os.sep)
        if any(s.startswith("_") for s in segs):
            continue
        if "분석.html" in fns:
            out.append(os.path.join(dp, "분석.html"))
    return out

def g(pat, text, d=""):
    m = re.search(pat, text, re.S)
    return m.group(1).strip() if m else d

def strip(s):
    return re.sub(r"<[^>]+>", "", s).strip()

def parse(fp):
    with open(fp, encoding="utf-8") as f:
        t = f.read()
    title = strip(g(r"<h1[^>]*>(.*?)</h1>", t))
    score = int(g(r"--p:\s*(\d+)", t) or g(r"calc\(\s*(\d+)\s*\*\s*1%", t) or "0")
    grade = (g(r'class="grade"[^>]*>\s*([A-D])', t)
             or g(r"등급\s*(?:<[^>]+>\s*)*([A-D])\b", t) or "?")
    hook = strip(g(r"후크\s*유형</div>\s*<div class=\"val\">(.*?)</div>", t))
    channel = strip(g(r"채널\s*[·∙]\s*([^<(][^<]*)", t)) or "—"
    sub = strip(g(r'<p class="sub">(.*?)</p>', t))
    yt = g(r"(https://www\.youtube\.com/watch\?v=[\w\-]+)", t)
    rel = os.path.relpath(fp, ROOT).replace(os.sep, "/")
    parts = rel.split("/")
    if parts[0] == "키워드기획" and len(parts) >= 3:
        kwf = parts[1]
        kwnum = kwf.split("_")[0]
        kwname = kwf.split("_", 1)[1].replace("_", " ") if "_" in kwf else kwf
    else:
        kwnum, kwname = "99", "샘플 · 기타"
    vidf = parts[-2]
    mnum = re.match(r"(\d+)", vidf)
    vidnum = mnum.group(1) if mnum else "00"
    return dict(title=title, score=score, grade=grade, hook=hook, channel=channel,
                sub=sub, yt=yt, href=quote(rel, safe="/"),
                kwnum=kwnum, kwname=kwname, vidnum=vidnum)

def grade_color(gr):
    return {"A": "#16a34a", "B": "#d97706", "C": "#dc2626", "D": "#dc2626"}.get(gr, "#9ca3af")

def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

items = sorted([parse(f) for f in find_files()], key=lambda x: (x["kwnum"], x["vidnum"]))
total = len(items)
graded = [i["score"] for i in items if i["score"] > 0]
avg = round(sum(graded) / len(graded)) if graded else 0
gc = Counter(i["grade"] for i in items)
groups = OrderedDict()
for i in items:
    groups.setdefault((i["kwnum"], i["kwname"]), []).append(i)
kw_count = len([k for k in groups if k[0] != "99"])
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

CSS = r"""
:root{--panel:#fff;--ink:#1f2430;--muted:#6b7280;--line:#e7e9f0;--brand:#4f46e5;--brand2:#7c3aed;--ok:#16a34a;--warn:#d97706;--bad:#dc2626;--soft:#f5f6fb;}
*{box-sizing:border-box}
body{margin:0;background:#eef0f6;color:var(--ink);font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic","Segoe UI",system-ui,sans-serif;line-height:1.6}
.wrap{max-width:1180px;margin:0 auto;padding:28px 20px 64px}
.hero{background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 60%,#0ea5e9 130%);color:#fff;border-radius:22px;padding:30px 34px;box-shadow:0 18px 40px -18px rgba(79,70,229,.6)}
.hero .kicker{font-size:13px;letter-spacing:.12em;text-transform:uppercase;opacity:.85;margin:0 0 8px}
.hero h1{margin:0;font-size:27px;font-weight:800;letter-spacing:-.01em}
.hero p{margin:10px 0 0;opacity:.92;font-size:15px}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px}
.stat{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.25);border-radius:14px;padding:10px 16px;min-width:96px}
.stat b{display:block;font-size:24px;font-weight:800;line-height:1.1}
.stat span{font-size:12px;opacity:.9}
.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:22px 2px 6px}
.toolbar input{flex:1;min-width:200px;border:1px solid var(--line);border-radius:11px;padding:11px 14px;font:inherit;background:#fff}
.seg{display:flex;gap:6px;flex-wrap:wrap}
.fbtn{appearance:none;border:1px solid var(--line);background:#fff;color:#4b5563;font:inherit;font-weight:700;font-size:13px;padding:9px 14px;border-radius:10px;cursor:pointer}
.fbtn.active{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;border-color:transparent}
.kwsec{margin-top:26px}
.kwh{display:flex;align-items:center;gap:10px;margin:0 2px 14px}
.kwh h2{font-size:17px;margin:0;color:#3730a3}
.kwh .cnt{font-size:12.5px;color:var(--muted);background:#eef0fb;border:1px solid #e0e7ff;border-radius:999px;padding:2px 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}
.card{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px 18px 16px;box-shadow:0 6px 20px -16px rgba(15,18,34,.5);transition:.15s;overflow:hidden}
.card:hover{transform:translateY(-3px);box-shadow:0 16px 30px -18px rgba(79,70,229,.5);border-color:#c7d2fe}
.card .stretch{position:absolute;inset:0;z-index:1}
.card .top{display:flex;gap:14px;align-items:flex-start}
.ring{flex:0 0 auto;width:60px;height:60px;border-radius:50%;display:grid;place-items:center;position:relative}
.ring::before{content:"";position:absolute;inset:6px;background:#fff;border-radius:50%}
.ring .n{position:relative;font-weight:800;font-size:18px}
.ttl{flex:1;min-width:0}
.ttl h3{margin:0 0 3px;font-size:15px;font-weight:700;line-height:1.35}
.ttl .ch{font-size:12.5px;color:var(--muted)}
.gbadge{position:absolute;top:14px;right:14px;z-index:2;font-weight:800;font-size:12px;color:#fff;border-radius:8px;padding:2px 9px}
.hook{margin:12px 0 0;font-size:12.5px;color:#4338ca;background:#eef0fb;border:1px solid #e0e7ff;border-radius:8px;padding:5px 10px;display:inline-block}
.desc{margin:10px 0 0;font-size:12.5px;color:#5b6270;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.acts{display:flex;gap:8px;margin-top:14px;position:relative;z-index:2}
.acts a{font-size:12.5px;font-weight:700;text-decoration:none;border-radius:9px;padding:7px 12px;border:1px solid var(--line)}
.acts .open{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;border-color:transparent}
.acts .yt{background:#fff;color:#b91c1c;border-color:#fecaca}
footer{margin-top:34px;color:var(--muted);font-size:12.5px;text-align:center;line-height:1.8}
footer a{color:var(--brand)}
.empty{display:none;text-align:center;color:var(--muted);padding:40px;font-size:14px}
@media(max-width:560px){.hero h1{font-size:21px}.grid{grid-template-columns:1fr}}
"""

cards_html = []
for (kwnum, kwname), lst in groups.items():
    cards = []
    for i in lst:
        col = grade_color(i["grade"])
        ring = "background:conic-gradient(%s %d%%,#e5e7eb 0)" % (col, i["score"])
        yt = ('<a class="yt" href="%s" target="_blank" rel="noopener">▶ 영상</a>' % esc(i["yt"])) if i["yt"] else ""
        hook_html = ('<span class="hook">%s</span>' % esc(i["hook"])) if i["hook"] else ""
        cards.append(
            '<div class="card" data-t="%s" data-g="%s">'
            '<a class="stretch" href="%s"></a>'
            '<span class="gbadge" style="background:%s">%s</span>'
            '<div class="top"><div class="ring" style="%s"><span class="n" style="color:%s">%d</span></div>'
            '<div class="ttl"><h3>%s. %s</h3><div class="ch">%s</div></div></div>'
            '%s<div class="desc">%s</div>'
            '<div class="acts"><a class="open" href="%s">분석 열기</a>%s</div></div>'
            % (esc((i["title"] + " " + i["channel"] + " " + i["hook"]).lower()), i["grade"],
               i["href"], col, i["grade"], ring, col, i["score"],
               i["vidnum"], esc(i["title"]), esc(i["channel"]),
               hook_html, esc(i["sub"]), i["href"], yt))
    cards_html.append(
        '<section class="kwsec"><div class="kwh"><h2>%s. %s</h2>'
        '<span class="cnt">%d편</span></div><div class="grid">%s</div></section>'
        % (kwnum, esc(kwname), len(lst), "".join(cards)))

html_doc = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>도입부 분석 대시보드 — 그럼에도 불구하고</title><style>%s</style></head><body>
<div class="wrap">
<header class="hero"><p class="kicker">그럼에도 불구하고 · readtree · 영상 도입부 분석</p>
<h1>📊 도입부 분석 통합 대시보드</h1>
<p>키워드별 레퍼런스 영상의 도입부(30초~1분) 후크·화면·자막 분석. 카드를 클릭하면 분석 페이지가 열립니다.</p>
<div class="stats">
<div class="stat"><b>%d</b><span>분석 영상</span></div>
<div class="stat"><b>%d</b><span>키워드</span></div>
<div class="stat"><b>%d</b><span>평균 점수</span></div>
<div class="stat"><b>%d / %d / %d</b><span>A / B / C·D</span></div>
</div></header>
<div class="toolbar">
<input id="q" type="search" placeholder="🔎 제목·채널·후크 검색…" oninput="flt()">
<div class="seg">
<button class="fbtn active" data-f="all" onclick="setF(this)">전체</button>
<button class="fbtn" data-f="A" onclick="setF(this)">A</button>
<button class="fbtn" data-f="B" onclick="setF(this)">B</button>
<button class="fbtn" data-f="C" onclick="setF(this)">C·D</button>
</div></div>
%s
<div class="empty" id="empty">검색 결과가 없습니다.</div>
<footer>마지막 갱신 %s · 기준 <a href="%s">작업지침서</a> · <a href="%s">실행 플레이북</a><br>
영상 분석을 추가한 뒤 <code>_scripts/build_dashboard.py</code>를 다시 실행하면 이 대시보드가 자동 갱신됩니다.</footer>
</div>
<script>
var curF="all";
function setF(b){document.querySelectorAll('.fbtn').forEach(function(x){x.classList.remove('active')});b.classList.add('active');curF=b.dataset.f;flt();}
function flt(){var q=(document.getElementById('q').value||'').toLowerCase().trim();var any=0;
document.querySelectorAll('.card').forEach(function(c){
var okT=!q||c.dataset.t.indexOf(q)>-1;
var gg=c.dataset.g;var okG=curF=='all'||gg==curF||(curF=='C'&&(gg=='C'||gg=='D'));
var show=okT&&okG;c.style.display=show?'':'none';if(show)any++;});
document.querySelectorAll('.kwsec').forEach(function(s){var v=0;s.querySelectorAll('.card').forEach(function(c){if(c.style.display!='none')v++;});s.style.display=v?'':'none';});
document.getElementById('empty').style.display=any?'none':'block';}
</script>
</body></html>""" % (CSS, total, kw_count, avg,
                     gc.get("A", 0), gc.get("B", 0), gc.get("C", 0) + gc.get("D", 0),
                     "\n".join(cards_html), now, quote("작업지침서.md"), quote("실행_플레이북.md"))

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html_doc)
print("OK wrote", OUT)
print("total=%d avg=%d kw=%d A=%d B=%d C/D=%d ?=%d" % (
    total, avg, kw_count, gc.get("A", 0), gc.get("B", 0), gc.get("C", 0) + gc.get("D", 0), gc.get("?", 0)))
