# -*- coding: utf-8 -*-
# 재사용 엔진: python3 _genkw.py <ROOT_mountpath> <datamodule>
# self-contained (다른 gen 모듈 import 안 함). 새 파일만 생성. SOP 준수.
import os, html, sys, importlib

def esc(s): return html.escape(s, quote=False)

CSS = """  :root{--panel:#fff;--ink:#1f2430;--muted:#6b7280;--line:#e7e9f0;--brand:#4f46e5;--brand2:#7c3aed;--ok:#16a34a;--warn:#d97706;--bad:#dc2626;--na:#9ca3af;--soft:#f5f6fb;--chip:#eef0fb;}
  *{box-sizing:border-box}
  body{margin:0;background:#eef0f6;color:var(--ink);font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic","Segoe UI",system-ui,sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased;}
  .wrap{max-width:980px;margin:0 auto;padding:28px 20px 60px;}
  .hero{background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 60%,#0ea5e9 130%);color:#fff;border-radius:20px;padding:30px 32px;box-shadow:0 18px 40px -18px rgba(79,70,229,.6);}
  .hero .kicker{font-size:13px;letter-spacing:.12em;text-transform:uppercase;opacity:.85;margin:0 0 8px}
  .hero h1{margin:0;font-size:24px;line-height:1.3;font-weight:800;letter-spacing:-.01em}
  .hero .sub{margin:10px 0 0;opacity:.92;font-size:15px}
  .chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
  .chip{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.25);padding:5px 11px;border-radius:999px;font-size:12.5px}
  .chip a{color:#fff;text-decoration:underline}
  section{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:24px 26px;margin-top:20px;box-shadow:0 6px 20px -16px rgba(15,18,34,.4)}
  h2{font-size:15px;letter-spacing:.02em;margin:0 0 16px;display:flex;align-items:center;gap:9px;color:#3730a3;text-transform:uppercase}
  h2 .n{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:7px;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;font-size:12px;font-weight:700}
  .grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
  .card{background:var(--soft);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
  .card .lab{font-size:12px;color:var(--muted);font-weight:600;margin-bottom:4px}.card .val{font-size:15px;font-weight:600}
  .verdict{display:flex;gap:18px;align-items:center;background:linear-gradient(135deg,#eef2ff,#faf5ff);border:1px solid #e0e7ff;border-radius:14px;padding:16px 20px;margin-bottom:18px;flex-wrap:wrap}
  .score-ring{flex:0 0 auto;width:104px;height:104px;border-radius:50%;background:conic-gradient(var(--ok) calc(var(--p)*1%), #e5e7eb 0);display:grid;place-items:center;position:relative}
  .score-ring::before{content:"";position:absolute;inset:11px;background:#fff;border-radius:50%}
  .score-ring .num{position:relative;text-align:center;line-height:1.05}.score-ring .num b{font-size:30px;font-weight:800;color:#111}.score-ring .num small{display:block;font-size:11px;color:var(--muted)}
  .grade{font-weight:800;color:var(--ok)}
  .verdict .vtxt{flex:1;min-width:220px}.verdict .vtxt h3{margin:0 0 4px;font-size:18px}.verdict .vtxt p{margin:0;color:#4b5563;font-size:14px}
  .srow{display:grid;grid-template-columns:170px 28px 1fr 54px;gap:10px;align-items:center;padding:9px 0;border-top:1px dashed var(--line)}
  .srow:first-of-type{border-top:0}.srow .nm{font-weight:600;font-size:14px}
  .bar{height:10px;border-radius:6px;background:#edeef4;overflow:hidden}.bar>i{display:block;height:100%;border-radius:6px}
  .b-ok>i{background:linear-gradient(90deg,#22c55e,#16a34a)}.b-warn>i{background:linear-gradient(90deg,#fbbf24,#d97706)}
  .b-bad>i{background:linear-gradient(90deg,#f87171,#dc2626)}
  .pts{text-align:right;font-variant-numeric:tabular-nums;font-weight:700;color:#374151;font-size:13px}.badge{font-size:15px;text-align:center}
  table{width:100%;border-collapse:collapse;font-size:13.5px}
  th,td{text-align:left;padding:10px 10px;border-bottom:1px solid var(--line);vertical-align:top}
  th{background:var(--soft);color:#4b5563;font-size:12px;text-transform:uppercase}
  td .tt,.tt{font-variant-numeric:tabular-nums;font-weight:700;color:#3730a3;white-space:nowrap}
  .flow{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
  .step{background:#fff;border:1.5px solid #e0e7ff;border-radius:10px;padding:7px 12px;font-size:13px;font-weight:600}
  .arrow{color:#c4b5fd;font-weight:800}.step.hook{border-color:#fbbf24;background:#fffbeb}.step.turn{border-color:#34d399;background:#ecfdf5}
  .cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}.mini h4{margin:0 0 8px;font-size:13px;color:#3730a3}
  ul.tight{margin:0;padding-left:18px}ul.tight li{margin:5px 0;font-size:13.5px}
  .note{background:#fff7ed;border:1px solid #fed7aa;border-left:4px solid #f97316;border-radius:12px;padding:16px 18px}.note h3{margin:0 0 8px;font-size:14px;color:#9a3412}.note a{color:#9a3412}
  .ok-i{color:var(--ok);font-weight:700}.no-i{color:var(--bad);font-weight:700}.na-i{color:var(--na);font-weight:700}
  footer{margin-top:26px;color:var(--muted);font-size:12.5px;text-align:center;line-height:1.8}footer a{color:var(--brand)}
  .tabs{display:flex;gap:8px;margin-top:18px;flex-wrap:wrap}
  .tab-btn{appearance:none;border:1px solid var(--line);background:#fff;color:#4b5563;font:inherit;font-weight:700;font-size:14px;padding:10px 18px;border-radius:11px;cursor:pointer;box-shadow:0 4px 14px -10px rgba(15,18,34,.5)}
  .tab-btn:hover{border-color:#c7d2fe;color:#3730a3}.tab-btn.active{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;border-color:transparent}
  .tab-panel{display:none}.tab-panel.active{display:block;animation:fade .2s ease}
  @keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
  .script-head{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin:2px 2px 14px}
  .script-head .hint{font-size:12.5px;color:var(--muted)}
  .copybtn{appearance:none;border:1px solid #c7d2fe;background:#eef2ff;color:#3730a3;font:inherit;font-weight:700;font-size:12.5px;padding:8px 14px;border-radius:9px;cursor:pointer}
  .script{background:#fff;border:1px solid var(--line);border-radius:14px;padding:6px 6px}
  .unit{padding:16px 20px;border-bottom:1px solid #eef0f6}.unit:last-child{border-bottom:0}
  .unit .uhd{display:flex;align-items:baseline;gap:10px;margin-bottom:8px;flex-wrap:wrap}
  .unit .time{font-weight:800;font-size:14px;color:#3730a3;font-variant-numeric:tabular-nums}
  .unit .utag{font-size:12px;font-weight:700;color:#6d28d9;background:#f5f3ff;border:1px solid #ede9fe;border-radius:7px;padding:2px 9px}
  .unit .ln{display:flex;gap:9px;margin:5px 0;font-size:14px;line-height:1.75}
  .unit .ln .k{flex:0 0 40px;color:var(--muted);font-weight:700}
  .unit .ln.script-line .k{color:var(--brand)}.unit .ln.script-line .v{font-weight:600}
  .unit .ln .v{flex:1}
  .sl{margin:0;padding:0;list-style:none}.sl li{display:flex;gap:12px;padding:6px 2px;border-bottom:1px solid #f1f2f7;font-size:13.5px}.sl li:last-child{border-bottom:0}.sl .tt{flex:0 0 46px}
  @media(max-width:680px){.grid,.cols{grid-template-columns:1fr}.srow{grid-template-columns:120px 24px 1fr 46px}.hero h1{font-size:20px}.wrap{padding:16px 12px 48px}section{padding:18px 16px}}
  @media print{body{background:#fff}section,.hero{box-shadow:none}.tabs{display:none}.tab-panel{display:block!important}}"""

JS = """document.querySelectorAll('.tab-btn').forEach(function(b){b.addEventListener('click',function(){document.querySelectorAll('.tab-btn').forEach(function(x){x.classList.remove('active')});document.querySelectorAll('.tab-panel').forEach(function(x){x.classList.remove('active')});b.classList.add('active');document.getElementById('tab-'+b.dataset.tab).classList.add('active');window.scrollTo({top:0,behavior:'smooth'});});});
function grab(sel){var out=[];document.querySelectorAll(sel).forEach(function(s){var t=s.querySelector('.time, .tt');var v=s.querySelector('.script-line .v')||s.querySelector('span:last-child');var tg=s.querySelector('.utag');out.push((t?t.textContent.trim()+'  ':'')+(tg?'['+tg.textContent.trim()+'] ':'')+(v?v.textContent.trim():''));});return out.join('\\n');}
function cp(btn,sel){if(!btn)return;btn.addEventListener('click',function(){var text=grab(sel);var lbl=btn.textContent;var d=function(){btn.textContent='\\u2713 \\ubcf5\\uc0ac\\ub428';setTimeout(function(){btn.textContent=lbl;},1500);};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(d);}else{var ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(ta);d();}});}
cp(document.getElementById('copyScript'),'#tab-script .unit');
cp(document.getElementById('copyRaw'),'#tab-raw .sl li');"""

def bar_cls(pct): return 'b-ok' if pct>=70 else ('b-warn' if pct>=50 else 'b-bad')

TPL = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<style>
%(css)s
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <p class="kicker">키워드 기획 · 도입부 원고 분석 · %(kw)s</p>
    <h1>%(hero_h1)s</h1>
    <p class="sub">%(sub)s</p>
    <div class="chips">%(chips)s</div>
  </header>

  <nav class="tabs">
    <button class="tab-btn active" data-tab="report">📊 분석 리포트</button>
    <button class="tab-btn" data-tab="script">📝 대본 타임라인</button>
    <button class="tab-btn" data-tab="raw">📜 원문</button>
  </nav>

  <div class="tab-panel active" id="tab-report">
    <section>
      <h2><span class="n">1</span> 한 줄 요약 &amp; 후크 점수</h2>
      <div class="verdict"><div class="score-ring" style="--p:%(score)d"><div class="num"><b>%(score)d</b><small>/100</small></div></div>
        <div class="vtxt"><h3>등급 <span class="grade">%(grade)s</span></h3><p>%(verdict_p)s</p></div></div>
      <div class="grid">
%(cards)s
      </div>
    </section>
    <section><h2><span class="n">2</span> 30초 후크 룰 채점</h2>
%(rule_rows)s
      <p style="margin:14px 0 0;font-size:13px;color:var(--muted)">%(rule_note)s</p></section>
    <section><h2><span class="n">3</span> 후크 구조 흐름</h2>
      <div class="flow">%(flow)s</div></section>
    <section><h2><span class="n">4</span> 도입부 타임라인 — 음성 × 화면 × 연출</h2>
      <table><thead><tr><th>구간</th><th>음성(요지)</th><th>화면/컷</th><th>번인 자막</th></tr></thead><tbody>
%(tl_rows)s
      </tbody></table>
      <p style="margin:10px 0 0;font-size:12.5px;color:var(--muted)">%(tl_note)s</p></section>
    <section><h2><span class="n">5</span> 차용 포인트 (그럼에도 불구하고)</h2>
      <div class="cols"><div class="mini"><h4>연출·구성 차용</h4><ul class="tight">%(bdir)s</ul></div>
      <div class="mini"><h4>우리 채널용 제목 변형안</h4><ul class="tight">%(btit)s</ul></div></div></section>
    <section><h2><span class="n">6</span> 채널 적합도 4축</h2>
      <table><thead><tr><th>축</th><th>해당</th><th>메모</th></tr></thead><tbody>
%(fit_rows)s
      </tbody></table>
      <p style="margin:12px 0 0;font-size:13px;color:var(--muted)">%(fit_note)s</p></section>
    <section><div class="note"><h3>⚙️ 대본·캡처 상태</h3>
      <p style="margin:0;font-size:13px">%(status_note)s</p></div></section>
  </div>

  <div class="tab-panel" id="tab-script">
    <section>
      <h2><span class="n">📝</span> 대본 타임라인 — 맥락 단위 원고 분석</h2>
      <div class="script-head"><span class="hint">유튜브 스크립트 패널 원문을 내용 최대 유지·오타/비문만 보정 → 맥락 단위 구분 → 구분별 대본 / 화면 / 자막</span><button class="copybtn" id="copyScript">⧉ 정리본 복사</button></div>
      <div class="script">
%(units)s
      </div>
      <p style="margin:10px 4px 0;font-size:12px;color:var(--muted)">※ 대본은 유튜브 <b>스크립트 표시 패널 원문</b>에서 오타·비문만 최소 보정. 원문 그대로는 <b>📜 원문</b> 탭.</p>
    </section>
  </div>

  <div class="tab-panel" id="tab-raw">
    <section>
      <h2><span class="n">📜</span> 원문 — 유튜브 스크립트 패널 그대로</h2>
      <div class="script-head"><span class="hint">YouTube '스크립트 표시' 패널 원문(자동자막, 오탈자 포함) — 손대지 않고 보존</span><button class="copybtn" id="copyRaw">⧉ 원문 복사</button></div>
      <ul class="sl">
%(raw)s
      </ul>
      <p style="margin:10px 4px 0;font-size:12px;color:var(--muted)">%(raw_note)s</p>
    </section>
  </div>

  <footer>키워드 기획 분석 · 2026-06-16 · 기준 <a href="../../../작업지침서.md">작업지침서</a> · <a href="../../../도입부분석_통합지침_(코워크용).md">통합지침</a><br>출처: <a href="%(url)s">YouTube — %(ch)s</a> · 썸끝 정답=좋음 · 내부 기획·학습용</footer>
</div>
<script>
%(js)s
</script>
</body>
</html>"""

def build(v):
    chips = "".join('<span class="chip">%s</span>'%esc(c) for c in v['chips'])
    chips += '<span class="chip"><a href="%s">▶ 원본 영상</a></span>'%v['url']
    cards = "".join('<div class="card"><div class="lab">%s</div><div class="val">%s</div></div>'%(esc(a),esc(b)) for a,b in v['cards'])
    rule_rows=""
    for nm,icon,pct,pts in v['rule']:
        rule_rows+='      <div class="srow"><span class="nm">%s</span><span class="badge">%s</span><span class="bar %s"><i style="width:%d%%"></i></span><span class="pts">%s</span></div>\n'%(esc(nm),icon,bar_cls(pct),pct,esc(pts))
    flow="".join('<span class="step %s">%s</span>%s'%(cls,esc(txt),('<span class="arrow">→</span>' if i<len(v['flow'])-1 else '')) for i,(cls,txt) in enumerate(v['flow']))
    tl_rows=""
    for t,voice,screen,cap in v['timeline']:
        tl_rows+='        <tr><td><span class="tt">%s</span></td><td>%s</td><td>%s</td><td>%s</td></tr>\n'%(esc(t),esc(voice),screen,esc(cap))
    bdir="".join('<li>%s</li>'%esc(x) for x in v['borrow_dir'])
    btit="".join('<li>%s</li>'%esc(x) for x in v['borrow_titles'])
    fit_rows=""
    for axis,yn,memo in v['fit']:
        cls={'Y':'ok-i','N':'no-i'}.get(yn,'na-i')
        fit_rows+='        <tr><td>%s</td><td><span class="%s">%s</span></td><td>%s</td></tr>\n'%(esc(axis),cls,yn,esc(memo))
    units=""
    for t,tag,script,screen,cap in v['units']:
        units+='        <div class="unit">\n          <div class="uhd"><span class="time">%s</span><span class="utag">%s</span></div>\n          <div class="ln script-line"><span class="k">대본</span><span class="v">%s</span></div>\n          <div class="ln"><span class="k">화면</span><span class="v">%s</span></div>\n          <div class="ln"><span class="k">자막</span><span class="v">%s</span></div>\n        </div>\n'%(esc(t),esc(tag),esc(script),esc(screen),esc(cap))
    raw="".join('        <li><span class="tt">%s</span><span>%s</span></li>\n'%(esc(t),esc(x)) for t,x in v['raw'])
    return TPL%dict(title=esc(v['title']),kw=esc(v['keyword']),hero_h1=esc(v['hero_h1']),sub=esc(v['sub']),
        chips=chips,score=v['score'],grade=esc(v['grade']),verdict_p=esc(v['verdict_p']),cards=cards,
        rule_rows=rule_rows,rule_note=esc(v['rule_note']),flow=flow,tl_rows=tl_rows,tl_note=v['tl_note'],
        bdir=bdir,btit=btit,fit_rows=fit_rows,fit_note=esc(v['fit_note']),status_note=v['status_note'],
        units=units,raw=raw,raw_note=esc(v['raw_note']),url=v['url'],ch=esc(v['ch_short']),css=CSS,js=JS)

def main():
    ROOT=sys.argv[1]; mod=sys.argv[2]
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    data=importlib.import_module(mod)
    for v in data.VIDEOS:
        d=os.path.join(ROOT, v['folder']); os.makedirs(os.path.join(d,'captures'),exist_ok=True)
        with open(os.path.join(d,'분석.html'),'w',encoding='utf-8') as f: f.write(build(v))
        with open(os.path.join(d,'transcript.md'),'w',encoding='utf-8') as f:
            f.write("# %s\n\n- 채널: %s\n- URL: %s\n- 길이: %s\n\n## 도입부 원문 (스크립트 패널, 자동자막 오탈자 보존)\n\n"%(v['hero_h1'],v['ch_short'],v['url'],v['len']))
            for t,x in v['raw']: f.write("- `%s` %s\n"%(t,x))
        with open(os.path.join(d,'captures','_수동캡처_가이드.md'),'w',encoding='utf-8') as f:
            f.write("# 수동 캡처 가이드 — %s\n\n> 환경 제약(백그라운드 탭 디코드 스로틀)으로 도입부 영상 프레임 자동 캡처가 막혀, 화면/자막은 ◻(보완 예정)으로 둡니다.\n> 아래 `&t=` 링크로 직접 이동해 Win+Shift+S로 캡처하면 됩니다.\n\n"%v['hero_h1'])
            for sec,lab in v['cap_points']: f.write("- %s : %s&t=%ds\n"%(lab, v['url'], sec))
    with open(os.path.join(ROOT,'README.md'),'w',encoding='utf-8') as f: f.write(data.README)
    print("DONE", mod, len(data.VIDEOS))

if __name__=='__main__': main()
