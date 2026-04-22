# activities/common/mini/equation_history_flash.py
"""
방정식 해법의 역사 – 인터랙티브 플래시 스토리 (초상화·YouTube·애니메이션)
이차방정식 → 삼·사차방정식 쟁탈전 → 5차 방정식의 비가해성
"""
import streamlit as st
import streamlit.components.v1 as components
import base64
import mimetypes
from pathlib import Path
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "방정식역사플래시"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 방정식 역사 스토리를 읽고 아래 질문에 답해 보세요**"},
    {"key": "인상깊은인물",
     "label": "세 파트에 등장한 수학자 중 가장 인상 깊었던 인물과 그 이유를 써 보세요.",
     "type": "text_area", "height": 100},
    {"key": "카르다노타르탈리아",
     "label": "카르다노가 타르탈리아와의 약속을 어기고 해법을 공개한 것에 대해 어떻게 생각하나요? 수학적 발견에서 윤리와 공유의 가치란 무엇일까요?",
     "type": "text_area", "height": 100},
    {"key": "아벨갈루아비교",
     "label": "아벨과 갈루아는 모두 젊은 나이에 5차 방정식의 비가해성을 증명했지만 매우 다른 삶을 살았습니다. 두 사람의 공통점과 차이점을 써 보세요.",
     "type": "text_area", "height": 100},
    {"key": "수학사느낀점",
     "label": "방정식의 역사를 통해 수학이 어떻게 발전해 왔는지 한 문장으로 정리해 보세요.",
     "type": "text_area", "height": 80},
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",         "type": "text_area", "height": 90},
]

META = {
    "title":       "📜 방정식 해법의 역사",
    "description": "이차방정식부터 5차 방정식 비가해성까지, 수학자들의 드라마틱한 도전과 좌절을 인터랙티브 스토리로 만납니다.",
    "order":       35,
}

_HTML = """\
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&family=Noto+Sans+KR:wght@400;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#0d0d1a;color:#e8e0d0;overflow-x:hidden;}
#bg-cv{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;}
.wr{position:relative;z-index:1;}
.main-title{text-align:center;padding:26px 18px 8px;}
.main-title h1{font-family:'Noto Serif KR',serif;font-size:1.85rem;
  background:linear-gradient(135deg,#f5d76e,#e8a44d,#c9605e);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px;}
.main-title p{color:#9a8fa0;margin-top:5px;font-size:.87rem;}
.prog-wrap{max-width:380px;margin:10px auto 0;}
.pb-lbl{display:flex;justify-content:space-between;font-size:.75rem;color:#7a7088;margin-bottom:3px;}
.pb-track{background:rgba(255,255,255,.06);border-radius:10px;height:6px;}
.pb-fill{height:6px;border-radius:10px;background:linear-gradient(90deg,#f5d76e,#e8a44d);transition:width .8s ease;}
.nav-tabs{display:flex;justify-content:center;gap:8px;padding:14px 14px 0;flex-wrap:wrap;}
.nav-tab{padding:9px 17px;border-radius:30px;border:2px solid #444;background:transparent;
  color:#9a8fa0;cursor:pointer;font-size:.86rem;font-family:'Noto Sans KR',sans-serif;transition:all .3s;}
.nav-tab:hover{border-color:#f5d76e;color:#f5d76e;}
.nav-tab.active{background:#f5d76e;border-color:#f5d76e;color:#1a1020;font-weight:700;}
.part{display:none;padding:16px 16px 34px;max-width:900px;margin:0 auto;}
.part.active{display:block;animation:fadeIn .4s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.ph{text-align:center;margin-bottom:18px;padding:16px;border-radius:13px;
  background:linear-gradient(135deg,rgba(255,255,255,.04),rgba(255,255,255,.01));
  border:1px solid rgba(255,255,255,.08);}
.ph-num{font-size:.72rem;letter-spacing:3px;color:#9a8fa0;margin-bottom:5px;}
.ph-title{font-family:'Noto Serif KR',serif;font-size:1.55rem;font-weight:700;}
.ph-sub{color:#9a8fa0;margin-top:6px;font-size:.87rem;line-height:1.6;}
/* 인물 그리드 */
.cg{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:11px;margin-bottom:18px;}
.cc{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:12px;
  padding:13px 9px;text-align:center;cursor:pointer;transition:all .3s;position:relative;overflow:hidden;}
.cc::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;
  background:var(--ac,#f5d76e);transform:scaleX(0);transition:transform .3s;}
.cc:hover::after,.cc.sel::after{transform:scaleX(1);}
.cc:hover,.cc.sel{border-color:var(--ac,#f5d76e);transform:translateY(-3px);}
/* 초상화 */
.pw{width:82px;height:102px;margin:0 auto 9px;border-radius:8px;overflow:hidden;
  border:2px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);
  display:flex;align-items:center;justify-content:center;}
.pw img{width:100%;height:100%;object-fit:cover;object-position:top;
  filter:sepia(.25) contrast(1.05);transition:filter .3s;}
.cc:hover .pw img,.cc.sel .pw img{filter:sepia(0) contrast(1.1);}
.pe{font-size:2.5rem;}
.cn{font-weight:700;font-size:.86rem;color:#f0e8d8;margin-bottom:3px;}
.cen{font-size:.67rem;color:#6a6078;margin-bottom:4px;}
.ce{font-size:.69rem;color:var(--ac,#f5d76e);font-weight:700;}
/* 상세 */
.cd{display:none;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:12px;padding:19px;margin-bottom:16px;animation:fadeIn .3s;}
.cd.show{display:block;}
.cdi{display:flex;gap:15px;flex-wrap:wrap;}
.dp{flex-shrink:0;width:96px;height:125px;border-radius:9px;overflow:hidden;border:2px solid rgba(255,255,255,.14);}
.dp img{width:100%;height:100%;object-fit:cover;object-position:top;filter:sepia(.15);}
.dpe{width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:3rem;background:rgba(255,255,255,.04);}
.dt{flex:1;min-width:160px;}
.dt h3{font-family:'Noto Serif KR',serif;font-size:1rem;color:#f5d76e;margin-bottom:8px;}
.dt p{line-height:1.8;color:#c0b8c8;font-size:.87rem;}
.hl{color:#f5d76e;font-weight:700;}
.qt{border-left:3px solid var(--ac,#f5d76e);padding:7px 12px;margin:9px 0;
  color:#d0c8d8;font-style:italic;background:rgba(245,215,110,.05);border-radius:0 8px 8px 0;
  font-size:.84rem;line-height:1.7;}
/* 배틀 */
.ba{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
  border-radius:13px;padding:18px;margin:14px 0;}
.br{display:flex;align-items:flex-start;justify-content:space-around;gap:13px;flex-wrap:wrap;}
.bc{text-align:center;flex:1;min-width:95px;}
.bp{width:72px;height:92px;margin:0 auto 8px;border-radius:8px;overflow:hidden;border:2px solid rgba(255,255,255,.14);}
.bp img{width:100%;height:100%;object-fit:cover;object-position:top;}
.bpe{width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:2.1rem;background:rgba(255,255,255,.04);}
.bn{font-weight:700;font-size:.86rem;color:#f0e8d8;}
.bep{font-size:.68rem;color:#7a7088;margin-bottom:4px;}
.bb{display:inline-block;padding:3px 8px;border-radius:10px;font-size:.68rem;font-weight:700;margin-top:3px;}
.win{background:rgba(100,200,100,.15);color:#90e890;border:1px solid #64b464;}
.lose{background:rgba(220,80,80,.15);color:#e89090;border:1px solid #dc5050;}
.vc{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;padding-top:14px;}
.vt{font-size:1.6rem;font-weight:900;color:#f5d76e;animation:vsp 1.5s infinite;text-shadow:0 0 16px rgba(245,215,110,.4);}
@keyframes vsp{0%,100%{transform:scale(1)}50%{transform:scale(1.13)}}
.bd{text-align:center;font-size:.8rem;color:#9a8fa0;max-width:280px;margin:10px auto 0;line-height:1.7;}
/* 타임라인 */
.tl{margin-bottom:14px;}
.ts{display:flex;gap:12px;opacity:0;transform:translateX(-16px);transition:all .5s ease;}
.ts.vis{opacity:1;transform:translateX(0);}
.tdc{display:flex;flex-direction:column;align-items:center;}
.td{width:30px;height:30px;border-radius:50%;background:var(--ac,#f5d76e);color:#1a1020;
  font-weight:700;font-size:.78rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.tl2{width:2px;flex:1;background:rgba(255,255,255,.08);margin:3px 0;min-height:12px;}
.tc{flex:1;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
  border-radius:10px;padding:12px 14px;margin-bottom:9px;}
.tc:hover{border-color:rgba(255,255,255,.18);background:rgba(255,255,255,.06);}
.ty{font-size:.72rem;color:var(--ac,#f5d76e);font-weight:700;margin-bottom:3px;}
.tt{font-weight:700;font-size:.9rem;color:#f0e8d8;margin-bottom:4px;}
.tdesc{font-size:.84rem;color:#a0989e;line-height:1.75;}
/* 수식 */
.mb{background:rgba(255,255,255,.03);border:1px solid rgba(245,215,110,.2);
  border-radius:11px;padding:15px;margin:12px 0;text-align:center;}
.mbl{font-size:.73rem;color:#9a8fa0;margin-bottom:6px;letter-spacing:1px;}
.mbf{font-size:1.05rem;color:#f5d76e;font-family:Georgia,serif;letter-spacing:.5px;line-height:1.6;}
.mbd{font-size:.8rem;color:#9a8fa0;margin-top:6px;line-height:1.6;}
/* 관계도 */
.rm{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:12px;
  padding:15px;margin:12px 0;text-align:center;}
.rm .rl{font-size:.76rem;color:#9a8fa0;margin-bottom:9px;}
.rr{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:5px;font-size:.82rem;}
.ri{padding:4px 11px;border-radius:15px;border:1px solid;}
.ra{color:#555;font-size:.77rem;}
/* 비교 테이블 */
.ct{width:100%;border-collapse:collapse;font-size:.84rem;}
.ct th{padding:8px;border-bottom:1px solid rgba(255,255,255,.1);font-weight:400;color:#9a8fa0;text-align:left;}
.ct td{padding:8px;border-bottom:1px solid rgba(255,255,255,.05);color:#c0b8c8;}
.ctr{text-align:center;}
/* 퀴즈 */
.qb{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
  border-radius:12px;padding:18px;margin:14px 0;}
.qb h4{font-size:.9rem;color:#f5d76e;margin-bottom:11px;font-weight:700;}
.qq{font-size:.88rem;color:#d0c8d8;margin-bottom:10px;line-height:1.6;}
.opts{display:flex;flex-direction:column;gap:6px;}
.opt{padding:8px 13px;border-radius:7px;border:1px solid rgba(255,255,255,.1);background:transparent;
  color:#c0b8c8;cursor:pointer;text-align:left;font-family:'Noto Sans KR',sans-serif;font-size:.84rem;transition:all .2s;}
.opt:hover{border-color:#f5d76e;color:#f5d76e;background:rgba(245,215,110,.05);}
.opt.correct{background:rgba(100,200,100,.15);border-color:#64c864;color:#90e890;}
.opt.wrong{background:rgba(220,80,80,.15);border-color:#dc5050;color:#e89090;}
.qfb{margin-top:8px;font-size:.84rem;line-height:1.7;display:none;padding:9px 12px;
  border-radius:7px;background:rgba(255,255,255,.04);}
.qfb.show{display:block;animation:fadeIn .3s;}
.qfb.ok{color:#90e890;}.qfb.fail{color:#e89090;}
/* 내비 */
.nb{display:flex;justify-content:center;gap:9px;margin-top:22px;flex-wrap:wrap;}
.btn{padding:10px 22px;border-radius:26px;border:none;font-family:'Noto Sans KR',sans-serif;
  font-size:.87rem;font-weight:700;cursor:pointer;transition:all .3s;}
.btn-n{background:linear-gradient(135deg,#f5d76e,#e8a44d);color:#1a1020;}
.btn-n:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(245,215,110,.3);}
.btn-p{background:transparent;border:2px solid #555;color:#999;}
.btn-p:hover{border-color:#999;color:#ccc;}
/* 마무리 */
.fn{text-align:center;padding:22px 16px;background:linear-gradient(135deg,rgba(199,125,255,.05),rgba(245,215,110,.05));
  border:1px solid rgba(255,255,255,.08);border-radius:13px;margin:14px 0;}
.fn h3{font-size:1rem;font-family:'Noto Serif KR',serif;font-weight:700;color:#f0e8d8;margin:8px 0;}
.fn p{font-size:.85rem;color:#9a8fa0;line-height:1.9;}
@media(max-width:900px){
  #p2-grid{grid-template-columns:repeat(2,minmax(130px,210px)) !important;max-width:460px !important;}
}
@media(max-width:580px){
  .main-title h1{font-size:1.38rem;}
  .ph-title{font-size:1.28rem;}
  .cg{grid-template-columns:repeat(2,1fr);}
  #p2-grid{grid-template-columns:repeat(1,minmax(130px,230px)) !important;max-width:240px !important;}
}
</style>
</head>
<body>
<canvas id="bg-cv"></canvas>
<div class="wr">

<div class="main-title">
  <h1>방정식 해법의 역사</h1>
  <p>수천 년에 걸친 수학자들의 도전, 좌절, 그리고 승리의 이야기</p>
  <div class="prog-wrap">
    <div class="pb-lbl"><span>진행률</span><span id="prog-text">0 / 3 파트</span></div>
    <div class="pb-track"><div class="pb-fill" id="pb-fill" style="width:0%"></div></div>
  </div>
</div>
<div class="nav-tabs">
  <button class="nav-tab active" onclick="showPart(1)">&#9312; 이차방정식의 역사</button>
  <button class="nav-tab" onclick="showPart(2)">&#9313; 삼&#xB7;사차방정식 쟁탈전</button>
  <button class="nav-tab" onclick="showPart(3)">&#9314; 5차 방정식의 벽</button>
</div>

<!-- PART1 -->
<div class="part active" id="part1" style="--ac:#7ec8e3">
<div class="ph"><div class="ph-num">PART 01</div>
<div class="ph-title" style="background:linear-gradient(135deg,#7ec8e3,#a0d8ef);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">이차방정식의 역사</div>
<div class="ph-sub">기원전 바빌로니아부터 이슬람 황금시대까지<br>수천 년에 걸친 이차방정식 풀이의 여정</div></div>

<div style="font-size:.79rem;color:#7a7088;margin-bottom:8px;text-align:center;">&#128070; 인물 카드를 클릭해 자세한 이야기를 읽어보세요</div>
<div class="cg" style="grid-template-columns:repeat(auto-fit,minmax(150px,220px));justify-content:center;">
  <div class="cc" style="--ac:#7ec8e3" onclick="selChar('p1','dioph',this)">
    <div class="pw"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Diophantus-cover.jpg/200px-Diophantus-cover.jpg" alt="디오판토스" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="pe" style="display:none">&#128208;</div></div>
    <div class="cn">디오판토스</div><div class="cen">Diophantus</div><div class="ce">3세기 그리스</div>
  </div>
  <div class="cc" style="--ac:#7ec8e3" onclick="selChar('p1','hyp',this)">
    <div class="pw"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Hypatia_portrait.png/200px-Hypatia_portrait.png" alt="히파티아" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="pe" style="display:none">&#127775;</div></div>
    <div class="cn">히파티아</div><div class="cen">Hypatia</div><div class="ce">4~5세기 그리스</div>
  </div>
  <div class="cc" style="--ac:#7ec8e3" onclick="selChar('p1','alkh',this)">
    <div class="pw"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Al-Khwarizmi_portrait.jpg/200px-Al-Khwarizmi_portrait.jpg" alt="알콰리즈미" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="pe" style="display:none">&#128218;</div></div>
    <div class="cn">알콰리즈미</div><div class="cen">Al-Khwarizmi</div><div class="ce">8~9세기 페르시아</div>
  </div>
</div>

<div class="cd" id="p1-dioph"><div class="cdi">
  <div class="dp"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Diophantus-cover.jpg/200px-Diophantus-cover.jpg" alt="디오판토스" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="dpe" style="display:none">&#128208;</div></div>
  <div class="dt" style="--ac:#7ec8e3"><h3>&#128208; 디오판토스 (약 3세기, 알렉산드리아)</h3>
  <p><span class="hl">대수학의 아버지</span>로 불리는 그리스 수학자. 저서 <em>Arithmetica</em>에서 기호를 사용해 방정식을 표현한 최초의 수학자 중 하나입니다.</p>
  <div class="qt">묘비의 수수께끼: "소년기 1/6, 청년기 1/12, 결혼 후 1/7..." &#8594; 풀면 84세!</div></div>
</div></div>

<div class="cd" id="p1-hyp"><div class="cdi">
  <div class="dp"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Hypatia_portrait.png/200px-Hypatia_portrait.png" alt="히파티아" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="dpe" style="display:none">&#127775;</div></div>
  <div class="dt" style="--ac:#7ec8e3"><h3>&#127775; 히파티아 (360?~415, 알렉산드리아)</h3>
  <p>역사 기록에 남은 <span class="hl">최초의 여성 수학자</span>. 디오판토스의 <em>Arithmetica</em>에 주석을 달아 이차방정식 이론을 계승&#183;발전시켰습니다.</p>
  <div class="qt">"진실을 알고 싶다면, 지식을 향한 갈망을 끄지 마라."</div></div>
</div></div>

<div class="cd" id="p1-alkh"><div class="cdi">
  <div class="dp"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Al-Khwarizmi_portrait.jpg/200px-Al-Khwarizmi_portrait.jpg" alt="알콰리즈미" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="dpe" style="display:none">&#128218;</div></div>
  <div class="dt" style="--ac:#7ec8e3"><h3>&#128218; 알콰리즈미 (780~850, 바그다드)</h3>
  <p>바그다드 <span class="hl">지혜의 집</span>에서 활동한 페르시아 수학자. 이차방정식을 6가지 유형으로 체계화했습니다.</p>
  <div class="mb" style="margin:10px 0;text-align:left;"><div class="mbl">어원을 바꾼 두 단어</div>
  <div class="mbf" style="font-size:.92rem;text-align:left;line-height:2.1;">Al-Khwarizmi &#8594; <span style="color:#90e8d8">Algorithm</span><br>책 제목 Al-Jabr &#8594; <span style="color:#90e8d8">Algebra</span></div></div>
  <div class="qt">"이 책은 사람들이 모든 거래에서 수를 이용할 때 필요한 것을 담는다."</div></div>
</div></div>

<div class="mb"><div class="mbl">2차 방정식 근의 공식</div>
<div class="mbf">x = (&#8722;b &#177; &#8730;(b&#178;&#8722;4ac)) / 2a</div>
<div class="mbd">기원전 2000년 바빌로니아 점토판에서 시작해 알콰리즈미의 체계화를 거쳐 완성되었습니다.</div></div>

<div class="qb"><h4>&#129513; 확인 퀴즈</h4>
<div class="qq">오늘날 <strong>Algebra(대수학)</strong>라는 단어의 직접 어원이 된 것은?</div>
<div class="opts">
  <button class="opt" data-ans="w" data-qid="q1" data-fb="&#10060; Al-Kitab은 책 전체 제목의 시작 부분입니다. 어원은 Al-Jabr입니다.">&#9312; 알콰리즈미 책 제목의 첫 단어 Al-Kitab</button>
  <button class="opt" data-ans="c" data-qid="q1" data-fb="&#9989; 정확합니다! Al-Jabr가 Algebra의 어원입니다. 알콰리즈미의 이름 자체는 Algorithm의 어원이 되었습니다.">&#9313; 알콰리즈미 책 제목의 Al-Jabr</button>
  <button class="opt" data-ans="w" data-qid="q1" data-fb="&#10060; Arithmetica는 디오판토스의 저서입니다.">&#9314; 디오판토스의 저서 Arithmetica</button>
  <button class="opt" data-ans="w" data-qid="q1" data-fb="&#10060; Algorithm은 알콰리즈미의 이름에서 온 단어입니다. Algebra는 그의 책 제목에서 왔습니다.">&#9315; 알콰리즈미의 이름 Al-Khwarizmi</button>
</div><div class="qfb" id="fb-q1"></div></div>

<div class="nb"><button class="btn btn-n" onclick="showPart(2)">&#9313; 삼&#xB7;사차방정식 쟁탈전 &#8594;</button></div>
</div>

<!-- PART2 -->
<div class="part" id="part2" style="--ac:#f5d76e">
<div class="ph"><div class="ph-num">PART 02</div>
<div class="ph-title" style="background:linear-gradient(135deg,#f5d76e,#e8a44d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">삼&#xB7;사차방정식 쟁탈전</div>
<div class="ph-sub">16세기 이탈리아, 수학자들이 명예를 걸고 벌인 공개 대결<br>비밀, 배신, 그리고 수학사에서 가장 드라마틱한 이야기</div></div>

<div style="font-size:.79rem;color:#7a7088;margin-bottom:8px;text-align:center;">&#128070; 인물 카드를 클릭해 자세한 이야기를 읽어보세요</div>
<div id="p2-grid" class="cg" style="grid-template-columns:repeat(4,minmax(130px,210px));justify-content:center;max-width:980px;margin:0 auto 18px;">
  <div class="cc" style="--ac:#c8a040" onclick="selChar('p2','ferro',this)">
    <div class="pw"><div class="pe">&#127963;</div></div>
    <div class="cn">페로</div><div class="cen">Scipione del Ferro</div><div class="ce">16세기 볼로냐</div>
  </div>
  <div class="cc" style="--ac:#e8a44d" onclick="selChar('p2','tartag',this)">
    <div class="pw"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Nicolo_Tartaglia.jpg/200px-Nicolo_Tartaglia.jpg" alt="타르탈리아" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="pe" style="display:none">&#9876;</div></div>
    <div class="cn">타르탈리아</div><div class="cen">Tartaglia</div><div class="ce">1500~1557 브레샤</div>
  </div>
  <div class="cc" style="--ac:#f5d76e" onclick="selChar('p2','cardano',this)">
    <div class="pw"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Girolamo_Cardano_%28colour%29.jpg/200px-Girolamo_Cardano_%28colour%29.jpg" alt="카르다노" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="pe" style="display:none">&#9877;</div></div>
    <div class="cn">카르다노</div><div class="cen">Cardano</div><div class="ce">1501~1576 밀라노</div>
  </div>
  <div class="cc" style="--ac:#90d8f0" onclick="selChar('p2','ferrari',this)">
    <div class="pw"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Lodovico_ferrari.jpg/200px-Lodovico_ferrari.jpg" alt="페라리" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="pe" style="display:none">&#127942;</div></div>
    <div class="cn">페라리</div><div class="cen">Ferrari</div><div class="ce">1522~1565 볼로냐</div>
  </div>
</div>

<div class="cd" id="p2-ferro"><div class="cdi">
  <div class="dp"><div class="dpe">&#127963;</div></div>
  <div class="dt" style="--ac:#c8a040"><h3 style="color:#c8a040">&#127963; 페로 (Scipione del Ferro, ~1526)</h3>
  <p>볼로냐 대학의 수학 교수. 삼차방정식 <span class="hl">x&#179; + ax + b = 0</span> 형태의 해법을 최초로 발견. 당시 해법은 <span class="hl">개인의 재산</span>이었고, 죽기 직전 제자 피오르에게만 비밀을 전수했습니다.</p></div>
</div></div>

<div class="cd" id="p2-tartag"><div class="cdi">
  <div class="dp"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Nicolo_Tartaglia.jpg/200px-Nicolo_Tartaglia.jpg" alt="타르탈리아" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="dpe" style="display:none">&#9876;</div></div>
  <div class="dt" style="--ac:#e8a44d"><h3 style="color:#e8a44d">&#9876; 타르탈리아 (말더듬이, 1500~1557)</h3>
  <p>어릴 때 프랑스 군의 칼에 다쳐 말을 더듬게 되어 별명이 생겼습니다. 독립적으로 삼차방정식 해법을 발견하고 <span class="hl">피오르와의 공개 대결에서 30:0 완승</span>. 그러나 카르다노에게 비밀을 전수한 뒤 배신당하고, 가난 속에 외롭게 세상을 떠났습니다.</p>
  <div class="qt">"나는 단지 비밀을 지켜달라는 약속만을 바랐습니다."</div></div>
</div></div>

<div class="cd" id="p2-cardano"><div class="cdi">
  <div class="dp"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Girolamo_Cardano_%28colour%29.jpg/200px-Girolamo_Cardano_%28colour%29.jpg" alt="카르다노" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="dpe" style="display:none">&#9877;</div></div>
  <div class="dt" style="--ac:#f5d76e"><h3>&#9877; 카르다노 (Girolamo Cardano, 1501~1576)</h3>
  <p>밀라노의 유명 의사. 1545년 <span class="hl">Ars Magna</span>에 삼차방정식 해법을 발표합니다. 삼촌&#183;동료 독살, 장남 처형, 종교재판 투옥 등 파란만장한 삶.</p>
  <div class="qt">"비밀은 인정받지 못한 채로 영원히 잠들 수도 있습니다."</div></div>
</div></div>

<div class="cd" id="p2-ferrari"><div class="cdi">
  <div class="dp"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Lodovico_ferrari.jpg/200px-Lodovico_ferrari.jpg" alt="페라리" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="dpe" style="display:none">&#127942;</div></div>
  <div class="dt" style="--ac:#90d8f0"><h3 style="color:#90d8f0">&#127942; 페라리 (Lodovico Ferrari, 1522~1565)</h3>
  <p>카르다노의 제자. 삼차방정식 해법을 응용해 <span class="hl">사차방정식</span>까지 풀어내는 데 성공. 43세의 젊은 나이에 의문의 죽음을 맞았습니다.</p></div>
</div></div>

<div class="tl" id="tl2">
<div class="ts" style="--ac:#c8a040"><div class="tdc"><div class="td" style="background:#c8a040">1</div><div class="tl2"></div></div>
<div class="tc"><div class="ty">16세기 초 &#183; 볼로냐</div><div class="tt">&#127963; 페로의 발견과 비밀 전수</div>
<div class="tdesc">페로가 삼차방정식 해법을 발견하지만 비밀로 간직합니다. 죽기 직전 제자 피오르에게만 전수합니다.</div></div></div>
<div class="ts" style="--ac:#e8a44d"><div class="tdc"><div class="td" style="background:#e8a44d">2</div><div class="tl2"></div></div>
<div class="tc"><div class="ty">1535년 &#183; 공개 수학 대결</div><div class="tt">&#9876; 피오르 vs 타르탈리아</div>
<div class="tdesc">각자 30문제씩 내고 푸는 대결 &#8212; 타르탈리아 <strong>30 : 0</strong> 완승!</div></div></div>
<div class="ts" style="--ac:#f5d76e"><div class="tdc"><div class="td" style="background:#f5d76e">3</div><div class="tl2"></div></div>
<div class="tc"><div class="ty">1539년 &#183; 밀라노</div><div class="tt">&#129309; 카르다노의 설득과 배신</div>
<div class="tdesc">카르다노는 "절대 발표하지 않겠다"는 약속으로 해법을 전수받습니다. 그러나 1545년 <em>Ars Magna</em>에 발표합니다.</div></div></div>
<div class="ts" style="--ac:#90d8f0"><div class="tdc"><div class="td" style="background:#90d8f0;color:#1a1020">4</div></div>
<div class="tc"><div class="ty">1545년 &#183; Ars Magna</div><div class="tt">&#127942; 페라리, 사차방정식까지 완성</div>
<div class="tdesc">카르다노의 제자 페라리가 사차방정식까지 풀어냅니다. 1&#8776;4차 방정식 해법이 완성됩니다.</div></div></div>
</div>

<!-- 배틀 씬 -->
<div class="ba">
  <div style="text-align:center;font-size:.77rem;color:#7a7088;margin-bottom:13px;">&#9876; 1535년 &#8212; 피오르 vs 타르탈리아 공개 수학 대결</div>
  <div class="br">
    <div class="bc">
      <div class="bp" style="background:rgba(220,80,80,.1);border-color:#c86450;"><div class="bpe">&#129489;&#8205;&#127979;</div></div>
      <div class="bn">피오르</div><div class="bep">페로의 제자</div>
      <div class="bb lose" id="fior-badge" style="opacity:0">0 / 30</div>
    </div>
    <div class="vc">
      <div class="vt">VS</div>
      <button class="btn btn-n" style="padding:6px 15px;font-size:.79rem;" id="battle-btn" onclick="runBattle()">&#9654; 대결 시작!</button>
      <div id="battle-result" style="font-size:.82rem;color:#f5d76e;text-align:center;margin-top:6px;display:none;"></div>
    </div>
    <div class="bc">
      <div class="bp" style="background:rgba(100,180,100,.1);border-color:#64b464;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Nicolo_Tartaglia.jpg/200px-Nicolo_Tartaglia.jpg" alt="타르탈리아" style="width:100%;height:100%;object-fit:cover;object-position:top;"
          onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="bpe" style="display:none">&#9876;</div>
      </div>
      <div class="bn">타르탈리아</div><div class="bep">브레샤의 수학자</div>
      <div class="bb win" id="tartag-badge" style="opacity:0">30 / 30 &#127941;</div>
    </div>
  </div>
  <div class="bd" id="btl-desc" style="display:none">말을 더듬는 핸디캡에도 불구하고 기적 같은 역전승! 이 승리가 카르다노의 관심을 끌게 됩니다&#8230;</div>
</div>

<div class="mb"><div class="mbl">카르다노 공식 &#8212; 삼차방정식의 근의 공식 (1545)</div>
<div class="mbf">x = &#8731;(&#8722;q/2 + &#8730;((q/2)&#178;+(p/3)&#179;)) + &#8731;(&#8722;q/2 &#8722; &#8730;((q/2)&#178;+(p/3)&#179;))</div>
<div class="mbd">삼차방정식 x&#179;+px+q=0 (2차항 소거 후)<br>300년간 풀리지 않던 문제가 16세기 이탈리아에서 드라마틱하게 정복되었습니다!</div></div>

<div class="rm"><div class="rl">&#128202; 삼&#xB7;사차방정식 역사 인물 관계도</div>
<div class="rr">
  <span class="ri" style="background:rgba(200,160,64,.15);border-color:#c8a040;color:#f5d76e">페로</span>
  <span class="ra">&#8594;제자&#8594;</span>
  <span class="ri" style="background:rgba(200,100,80,.12);border-color:#c86450;color:#e89090">피오르</span>
  <span class="ra">&#9876;패배</span>
  <span class="ri" style="background:rgba(100,180,100,.12);border-color:#64b464;color:#90e890">타르탈리아&#10003;</span>
  <span class="ra">&#8594;전수&#8594;</span>
  <span class="ri" style="background:rgba(245,215,110,.12);border-color:#f5d76e;color:#f5d76e">카르다노</span>
  <span class="ra">&#8594;제자&#8594;</span>
  <span class="ri" style="background:rgba(100,150,220,.12);border-color:#6496dc;color:#90b8f0">페라리(4차)</span>
</div></div>

<div class="qb"><h4>&#129513; 확인 퀴즈</h4>
<div class="qq">1535년 공개 수학 대결, 피오르 vs 타르탈리아의 결과는?</div>
<div class="opts">
  <button class="opt" data-ans="w" data-qid="q2" data-fb="&#10060; 피오르는 타르탈리아의 문제를 하나도 풀지 못했습니다.">&#9312; 피오르가 타르탈리아의 문제를 모두 풀어 승리했다</button>
  <button class="opt" data-ans="c" data-qid="q2" data-fb="&#9989; 정확합니다! 타르탈리아는 피오르가 낸 삼차방정식 30문제를 모두 해결했지만, 피오르는 하나도 못 풀었습니다. 완전한 30:0 완승!">&#9313; 타르탈리아가 30문제 모두 해결하여 30:0 완승했다</button>
  <button class="opt" data-ans="w" data-qid="q2" data-fb="&#10060; 무승부는 없었습니다.">&#9314; 무승부로 끝났다</button>
  <button class="opt" data-ans="w" data-qid="q2" data-fb="&#10060; 카르다노는 이 대결에 직접 참여하지 않았습니다.">&#9315; 카르다노가 두 사람을 모두 이겼다</button>
</div><div class="qfb" id="fb-q2"></div></div>

<div class="nb">
  <button class="btn btn-p" onclick="showPart(1)">&#8592; &#9312; 이차방정식의 역사</button>
  <button class="btn btn-n" onclick="showPart(3)">&#9314; 5차 방정식의 벽 &#8594;</button>
</div>
</div>

<!-- PART3 -->
<div class="part" id="part3" style="--ac:#c77dff">
<div class="ph"><div class="ph-num">PART 03</div>
<div class="ph-title" style="background:linear-gradient(135deg,#c77dff,#9b50e0);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">5차 방정식의 벽</div>
<div class="ph-sub">300년간의 도전 끝에 &#8220;풀 수 없음&#8221;을 증명한 두 천재<br>아벨과 갈루아의 비극적이고 위대한 이야기</div></div>

<div class="tc" style="margin-bottom:16px;border-color:rgba(199,125,255,.3);">
<div class="ty">1545~1800년대 &#183; 300년간의 도전</div>
<div class="tt">&#128274; 아무도 풀지 못한 5차 방정식</div>
<div class="tdesc">1차~4차까지 해법이 완성된 후 수학자들은 <strong>5차 방정식의 근의 공식</strong>을 찾기 시작했습니다. 그러나 300년이 지나도 성공하지 못했습니다. 이유는 단 하나 &#8212; <strong>그런 공식이 애초에 존재하지 않았기 때문</strong>이었습니다.</div></div>

<div style="font-size:.79rem;color:#7a7088;margin-bottom:8px;text-align:center;">&#128070; 인물 카드를 클릭해 자세한 이야기를 읽어보세요</div>
<div class="cg" style="grid-template-columns:1fr 1fr;max-width:440px;margin:0 auto 16px;">
  <div class="cc" style="--ac:#c77dff" onclick="selChar('p3','abel',this)">
    <div class="pw"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Niels_Henrik_Abel.jpg/200px-Niels_Henrik_Abel.jpg" alt="아벨" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="pe" style="display:none">&#127475;&#127476;</div></div>
    <div class="cn">아벨</div><div class="cen">Niels Henrik Abel</div><div class="ce">1802~1829 노르웨이</div>
  </div>
  <div class="cc" style="--ac:#c77dff" onclick="selChar('p3','galois',this)">
    <div class="pw"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/%C3%89variste_galois.jpg/200px-%C3%89variste_galois.jpg" alt="갈루아" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="pe" style="display:none">&#127467;&#127479;</div></div>
    <div class="cn">갈루아</div><div class="cen">&#201;variste Galois</div><div class="ce">1811~1832 프랑스</div>
  </div>
</div>

<div class="cd" id="p3-abel"><div class="cdi">
  <div class="dp"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Niels_Henrik_Abel.jpg/200px-Niels_Henrik_Abel.jpg" alt="아벨" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="dpe" style="display:none">&#127475;&#127476;</div></div>
  <div class="dt" style="--ac:#c77dff"><h3 style="color:#c77dff">&#127475;&#127476; 아벨 (Niels Henrik Abel, 1802~1829)</h3>
  <p>알코올 중독 아버지, 무책임한 어머니 아래 형제들을 홀로 부양하면서 연구했습니다. <span class="hl">21살</span>에 5차 방정식 대수적 해법 불가능을 증명. 베를린 대학 교수 임명장이 도착하기 <span class="hl">이틀 전</span> 결핵으로 사망. 향년 27세.</p>
  <div class="qt">"나는 18살에 5차 방정식을 푼 것으로 알았습니다. 그러나 틀렸습니다. 그 틀림이 올바른 길로 이끌었습니다."</div></div>
</div></div>

<div class="cd" id="p3-galois"><div class="cdi">
  <div class="dp"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/%C3%89variste_galois.jpg/200px-%C3%89variste_galois.jpg" alt="갈루아" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"><div class="dpe" style="display:none">&#127467;&#127479;</div></div>
  <div class="dt" style="--ac:#c77dff"><h3 style="color:#c77dff">&#127467;&#127479; 갈루아 (&#201;variste Galois, 1811~1832)</h3>
  <p>에꼴 폴리테크닉 두 번 낙방, 아버지 자살, 혁명 운동 참여로 투옥. <span class="hl">19살</span>에 군론(Group Theory)으로 5차 이상의 비가해성 완전 증명. 결투 전날 밤 편지 곳곳에 <span class="hl">&#8220;시간이 없다&#8221;</span>고 적었습니다. 향년 21세.</p>
  <div class="qt">"나에게는 시간이 없다."<br><span style="font-size:.77rem;">&#8212; 결투 전날 밤 편지, 1832년 5월</span></div></div>
</div></div>

<div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:16px;margin:12px 0;overflow-x:auto;">
  <div style="font-size:.77rem;color:#9a8fa0;margin-bottom:9px;text-align:center;">&#128202; 아벨 vs 갈루아 비교</div>
  <table class="ct">
    <thead><tr><th>항목</th><th class="ctr" style="color:#c77dff">아벨</th><th class="ctr" style="color:#c77dff">갈루아</th></tr></thead>
    <tbody>
      <tr><td>국적</td><td class="ctr">&#127475;&#127476; 노르웨이</td><td class="ctr">&#127467;&#127479; 프랑스</td></tr>
      <tr><td>증명 나이</td><td class="ctr">21세</td><td class="ctr">19세</td></tr>
      <tr><td>사망 나이</td><td class="ctr">27세 (결핵)</td><td class="ctr">21세 (결투)</td></tr>
      <tr><td>접근 방법</td><td class="ctr">직접 불가능 증명</td><td class="ctr">군론(Group Theory)</td></tr>
      <tr><td>사후 인정</td><td class="ctr">크렐 저널 게재</td><td class="ctr">11년 후 리우빌이 발표</td></tr>
    </tbody>
  </table>
</div>

<!-- 갈루아 편지 타이핑 -->
<div style="background:linear-gradient(135deg,rgba(30,10,50,.8),rgba(20,10,40,.8));
  border:1px solid rgba(199,125,255,.25);border-radius:13px;padding:20px;margin:13px 0;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;right:0;font-size:6rem;opacity:.04;line-height:1;pointer-events:none">&#127769;</div>
  <div style="font-size:.75rem;color:#9a8fa0;margin-bottom:8px;letter-spacing:1px;">1832년 5월 29일 &#8212; 결투 전날 밤</div>
  <div id="letter-text" style="font-size:.88rem;line-height:1.9;color:#c0b0d8;font-style:italic;min-height:68px;"></div>
  <button class="btn btn-n" style="margin-top:11px;padding:7px 16px;font-size:.79rem;" onclick="typeGaloisLetter()">&#9993; 갈루아의 편지 읽기</button>
</div>

<div class="mb" style="border-color:rgba(199,125,255,.3);">
<div class="mbl">5차 이상 방정식의 비가해성</div>
<div class="mbf" style="color:#c77dff;font-size:1rem;">일반적인 5차 이상 방정식은<br>+, &#8722;, &#215;, &#247;, &#8730; 만으로 해를 구할 수 없다.</div>
<div class="mbd">공식이 어려운 것이 아니라, 그런 공식 자체가 존재하지 않습니다.<br>아벨(21세)과 갈루아(19세)가 수학사에 이 진실을 새겼습니다.</div></div>

<div class="qb"><h4>&#129513; 확인 퀴즈</h4>
<div class="qq">갈루아가 5차 방정식의 비가해성 증명에 도입한 새로운 수학 개념은?</div>
<div class="opts">
  <button class="opt" data-ans="w" data-qid="q3" data-fb="&#10060; 복소수 이론은 카르다노 시대에도 사용되었습니다.">&#9312; 복소수 이론</button>
  <button class="opt" data-ans="w" data-qid="q3" data-fb="&#10060; 미적분의 기본정리는 뉴턴&#183;라이프니츠의 업적입니다.">&#9313; 미적분의 기본정리</button>
  <button class="opt" data-ans="c" data-qid="q3" data-fb="&#9989; 정확합니다! 갈루아는 군(Group)이라는 새로운 대수 구조를 도입해 방정식의 대수적 가해성 여부를 완전히 판단하는 이론을 세웠습니다. 현대 추상대수학의 출발점입니다!">&#9314; 군론 (Group Theory)</button>
  <button class="opt" data-ans="w" data-qid="q3" data-fb="&#10060; 행렬 이론은 이후 케일리 등이 발전시켰습니다.">&#9315; 행렬 이론</button>
</div><div class="qfb" id="fb-q3"></div></div>

<div class="fn">
  <div>&#11088;</div>
  <h3>수학은 혼자가 아닌 역사가 만든다</h3>
  <p>바빌로니아의 점토판에서 시작해, 알콰리즈미의 체계화를 거쳐,<br>
  이탈리아 수학자들의 치열한 대결을 지나,<br>
  아벨과 갈루아가 27살&#183;21살의 짧은 생애로 완성한 여정.<br><br>
  <strong style="color:#f5d76e;">우리가 오늘 배우는 방정식은 수천 년의 인류의 노고가 담긴 결정체입니다.</strong></p>
</div>

<div class="nb"><button class="btn btn-p" onclick="showPart(2)">&#8592; &#9313; 삼&#xB7;사차방정식 쟁탈전</button></div>
</div>

</div>
<script>
let W,H;
const pts=Array.from({length:60},()=>({x:Math.random()*1920,y:Math.random()*1200,
  r:Math.random()*1.4+.3,s:Math.random()*.25+.08,o:Math.random()*.5+.1,d:Math.random()>.5?1:-1}));

function initBgCanvas(){
  const cv=document.getElementById('bg-cv');
  if(!cv){return;}
  const cx=cv.getContext('2d');
  if(!cx){return;}
  function rsz(){W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}
  rsz();
  window.addEventListener('resize',rsz);
  (function fr(){
    cx.clearRect(0,0,W,H);
    pts.forEach(p=>{p.o+=.004*p.d;if(p.o>.6||p.o<.05)p.d*=-1;p.y+=p.s;
      cx.beginPath();cx.arc(p.x%W,p.y%H,p.r,0,Math.PI*2);cx.fillStyle='rgba(200,180,255,'+p.o+')';cx.fill();
    });
    requestAnimationFrame(fr);
  })();
}

const visited=new Set([1]);
function updateProg(){
  const pb=document.getElementById('pb-fill');
  const pt=document.getElementById('prog-text');
  if(pb){pb.style.width=Math.round(visited.size/3*100)+'%';}
  if(pt){pt.textContent=visited.size+' / 3 파트';}
}

// CSP/iframe 정책으로 inline onclick이 막히는 환경 대비
function wireFallbackHandlers(){
  document.querySelectorAll('.nav-tab').forEach((btn, i)=>{
    btn.addEventListener('click', ()=>showPart(i+1));
  });

  document.querySelectorAll('.cc').forEach((card)=>{
    const oc = card.getAttribute('onclick') || '';
    const m = oc.match(/selChar\\('([^']+)'\\s*,\\s*'([^']+)'\\s*,\\s*this\\)/);
    if(m){
      card.addEventListener('click', ()=>selChar(m[1], m[2], card));
    }
  });

  document.querySelectorAll('button[onclick]').forEach((btn)=>{
    const oc = btn.getAttribute('onclick') || '';

    let m = oc.match(/showPart\\((\\d+)\\)/);
    if(m){
      btn.addEventListener('click', ()=>showPart(Number(m[1])));
      return;
    }

    if(oc.indexOf('runBattle()') >= 0){
      btn.addEventListener('click', ()=>runBattle());
      return;
    }

    if(oc.indexOf('typeGaloisLetter()') >= 0){
      btn.addEventListener('click', ()=>typeGaloisLetter());
    }
  });
}

let tl2done=false;
function showPart(n){
  document.querySelectorAll('.part').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active'));
  const part=document.getElementById('part'+n);
  const tab=document.querySelectorAll('.nav-tab')[n-1];
  if(part){part.classList.add('active');}
  if(tab){tab.classList.add('active');}
  visited.add(n);updateProg();
  if(n===2&&!tl2done)setTimeout(animTL,200);
  try{window.scrollTo({top:0,behavior:'smooth'});}catch(e){}
}
function animTL(){tl2done=true;document.querySelectorAll('#tl2 .ts').forEach((s,i)=>setTimeout(()=>s.classList.add('vis'),i*220));}

function selChar(pid,cid,card){
  const n=pid.replace('p','');
  document.querySelectorAll('#part'+n+' .cc').forEach(c=>c.classList.remove('sel'));
  card.classList.add('sel');
  document.querySelectorAll('#part'+n+' .cd').forEach(d=>d.classList.remove('show'));
  const panel=document.getElementById(pid+'-'+cid);
  if(panel){panel.classList.add('show');panel.scrollIntoView({behavior:'smooth',block:'nearest'});}
}

let battleDone=false;
function runBattle(){
  if(battleDone)return;battleDone=true;
  const btn=document.getElementById('battle-btn');
  btn.disabled=true;btn.textContent='\u2694\ufe0f \ub300\uacb0 \uc911\u2026';
  let step=0;
  const iv=setInterval(()=>{step++;const tb=document.getElementById('tartag-badge');tb.style.opacity='1';tb.textContent=step+' / 30 \U0001F3C5';
    if(step>=30){clearInterval(iv);document.getElementById('fior-badge').style.opacity='1';
      document.getElementById('battle-result').style.display='block';
      document.getElementById('battle-result').innerHTML='\U0001F3C6 \ud0c0\ub974\ud0c8\ub9ac\uc544 \uc644\uc2b9! <strong>30 : 0</strong>';
      document.getElementById('btl-desc').style.display='block';btn.textContent='\u2705 \uc644\ub8cc';}
  },60);
}

function bindQuiz(){
  document.querySelectorAll('.opt').forEach(btn=>{
    btn.addEventListener('click',function(){
      const qid=this.dataset.qid;
      document.querySelectorAll('.opt[data-qid="'+qid+'"]').forEach(b=>b.classList.remove('correct','wrong'));
      this.classList.add(this.dataset.ans==='c'?'correct':'wrong');
      const fb=document.getElementById('fb-'+qid);
      if(fb){fb.innerHTML=this.dataset.fb;fb.className='qfb show '+(this.dataset.ans==='c'?'ok':'fail');}
    });
  });
}

const gLetter=`"친구에게,

나는 5차 이상의 방정식을 왜 대수적으로 풀 수 없는가에 대해
완전히 새로운 이론을 발견했습니다.
시간이 없다… 시간이 없다…
이 편지를 가우스와 야코비에게 전해 달라.

— Évariste Galois, 1832년 5월 29일 새벽"`;
let typeIv=null,typeIdx=0;
function typeGaloisLetter(){
  const el=document.getElementById('letter-text');
  if(typeIv){clearInterval(typeIv);el.innerHTML='';typeIdx=0;}
  const txt=gLetter;
  typeIv=setInterval(()=>{if(typeIdx>=txt.length){clearInterval(typeIv);return;}typeIdx++;el.innerHTML=txt.slice(0,typeIdx).replace(/\\n/g,'<br>');},28);
}

// 초기화 중 일부가 실패해도 클릭 기능은 유지되도록 분리
try{wireFallbackHandlers();}catch(e){console.error(e);}
try{bindQuiz();}catch(e){console.error(e);}
try{updateProg();}catch(e){console.error(e);}
try{initBgCanvas();}catch(e){console.error(e);}
</script>
</body>
</html>
"""


_ASSET_DIR = Path(__file__).resolve().parents[3] / "assets" / "commonmath" / "equation_history"


def _img_data_uri(filename: str) -> str:
  path = _ASSET_DIR / filename
  if not path.exists():
    return ""
  mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
  b64 = base64.b64encode(path.read_bytes()).decode("ascii")
  return f"data:{mime};base64,{b64}"


_PORTRAIT_DATA = {
  "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Diophantus-cover.jpg/200px-Diophantus-cover.jpg": _img_data_uri("dioph.jpg"),
  "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Hypatia_portrait.png/200px-Hypatia_portrait.png": _img_data_uri("hypatia.jpg"),
  "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Al-Khwarizmi_portrait.jpg/200px-Al-Khwarizmi_portrait.jpg": _img_data_uri("alkhwarizmi.jpg"),
  "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Nicolo_Tartaglia.jpg/200px-Nicolo_Tartaglia.jpg": _img_data_uri("tartaglia.jpg"),
  "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Girolamo_Cardano_%28colour%29.jpg/200px-Girolamo_Cardano_%28colour%29.jpg": _img_data_uri("cardano.jpg"),
  "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Lodovico_ferrari.jpg/200px-Lodovico_ferrari.jpg": _img_data_uri("ferrari.jpg"),
  "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Niels_Henrik_Abel.jpg/200px-Niels_Henrik_Abel.jpg": _img_data_uri("abel.jpg"),
  "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/%C3%89variste_galois.jpg/200px-%C3%89variste_galois.jpg": _img_data_uri("galois.jpg"),
}

for _src, _data_uri in _PORTRAIT_DATA.items():
  if _data_uri:
    _HTML = _HTML.replace(_src, _data_uri)


def render():
    st.markdown("## 📜 방정식 해법의 역사")
    st.caption("이차방정식부터 5차 방정식 비가해성까지, 수학자들의 드라마틱한 도전과 좌절을 만나 보세요.")

    import streamlit.components.v1 as components
    components.html(_HTML, height=2100, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
