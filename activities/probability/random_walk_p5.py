# activities/probability/random_walk_p5.py
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "랜덤워크 (p5.js)",
    "description": "p5.js로 2D 랜덤워크를 시각화합니다. 경로/걸음 수, 줌(확대), 점/선 두께를 조절해 보세요.",
    "order": 50,
    "hidden": False,   # mini 폴더에 있으면 폴더 기준으로 숨김 처리됩니다.
}

def render():
    st.markdown("### 2D 랜덤워크 (p5.js)")

    components.html(
        """
<!doctype html>
<html><head>
<meta charset="utf-8"/>
<script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
<style>
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,'Apple SD Gothic Neo','Noto Sans KR','NanumGothic',sans-serif;margin:0;}
  #wrap{max-width:1100px;margin:0 auto;}
  .ui{display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:10px 12px;}
  .pill{padding:4px 8px;border-radius:999px;background:#f1f5f9;border:1px solid #e2e8f0;font-size:12px;}
  .muted{color:#64748b}
  .ui input[type=range]{width:160px}
  .ui input[type=number]{width:90px}
  button{padding:6px 10px;border:1px solid #d1d5db;background:#fff;border-radius:8px;cursor:pointer}
  canvas{display:block;margin:8px auto;border:1px solid #e5e7eb;border-radius:12px;box-shadow:0 1px 5px rgba(0,0,0,.04);}
</style>
</head>
<body>
<div id="wrap">
  <div class="ui">
    <span class="pill">경로 <input id="paths" type="number" min="1" max="200" step="1" value="30"></span>
    <span class="pill">걸음 <input id="steps" type="number" min="10" max="5000" step="10" value="800"></span>
    <span class="pill">줌 <input id="zoom" type="range" min="50" max="300" value="100"> <span id="zoom_val" class="muted">100%</span></span>
    <span class="pill">점 크기 <input id="dotSize" type="range" min="0" max="12" value="3"> <span id="dot_val" class="muted">3</span></span>
    <span class="pill">선 두께 <input id="lineW" type="range" min="1" max="6" value="1"> <span id="lw_val" class="muted">1</span></span>
    <label class="pill"><input id="showDots" type="checkbox" checked> 모든 발자국 표시</label>
    <button id="drawBtn">다시 그리기</button>
  </div>
</div>

<script>
  // ----- 설정값 -----
  let W = 900, H = 600;         // 캔버스 크기 (원하면 여기 숫자만 바꿔도 됩니다)
  let pathsData = [];           // 사전 계산된 경로 저장
  let zoom = 1, dotSize = 3, lineW = 1, showDots = true;

  function randAng(){ return Math.random()*Math.PI*2; }

  function genData(nPaths, nSteps){
    pathsData = new Array(nPaths);
    for(let i=0;i<nPaths;i++){
      let xs = new Float32Array(nSteps+1);
      let ys = new Float32Array(nSteps+1);
      let x=0, y=0; xs[0]=0; ys[0]=0;
      for(let s=1;s<=nSteps;s++){
        const a = randAng();
        x += Math.cos(a); y += Math.sin(a);
        xs[s]=x; ys[s]=y;
      }
      pathsData[i] = {x:xs, y:ys};
    }
  }

  function drawAll(){
    clear();
    background(255);
    translate(W/2, H/2);
    scale(zoom);

    // 선 두께는 줌과 무관하게 보이도록 보정
    stroke(0,0,0,80);
    strokeWeight(lineW/zoom);
    noFill();

    for(const p of pathsData){
      beginShape();
      for(let i=0;i<p.x.length;i++){
        vertex(p.x[i], p.y[i]);
      }
      endShape();

      if(showDots && dotSize>0){
        fill(0,0,0,70); noStroke();
        const r = dotSize/zoom; // 줌과 무관하게 점 크기 유지
        for(let i=0;i<p.x.length;i++){
          circle(p.x[i], p.y[i], r);
        }
        noFill();
      }
    }
  }

  // p5 인스턴스
  new p5((sk)=>{
    sk.setup = ()=>{
      const c = sk.createCanvas(W, H);
      sk.noLoop();           // draw 루프 끄고 필요할 때만 그리기
      genData(30, 800);      // 초기 데이터
      drawAll();
    };
    sk.draw = ()=>{};
  });

  // ----- UI 바인딩 -----
  const $ = (id)=>document.getElementById(id);
  function refresh(){
    zoom     = $('zoom').value/100;
    dotSize  = parseFloat($('dotSize').value);
    lineW    = parseFloat($('lineW').value);
    showDots = $('showDots').checked;

    $('zoom_val').textContent = Math.round(zoom*100)+'%';
    $('dot_val').textContent  = dotSize;
    $('lw_val').textContent   = lineW;

    window.redraw();  // p5 글로벌
    drawAll();
  }

  ['zoom','dotSize','lineW','showDots'].forEach(id=>{
    $(id).addEventListener('input', refresh);
  });

  $('drawBtn').addEventListener('click', ()=>{
    const nP = Math.max(1, Math.min(200, parseInt($('paths').value||30)));
    const nS = Math.max(10, Math.min(5000, parseInt($('steps').value||800)));
    genData(nP, nS);
    refresh();
  });

  // 마우스 휠로 줌 (편의)
  document.addEventListener('wheel', (e)=>{
    const canvas = document.querySelector('canvas');
    if(!canvas) return;
    if(!canvas.matches(':hover')) return; // 캔버스 위에서만
    e.preventDefault();
    let v = parseInt($('zoom').value);
    v += (e.deltaY<0 ? 10 : -10);
    v = Math.max(50, Math.min(300, v));
    $('zoom').value = v;
    refresh();
  }, {passive:false});

  // 최초 상태 표시
  refresh();
</script>
</body></html>
        """,
        height=760,
    )
