# activities/probability/random_walk_p5.py
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "랜덤워크 (p5.js)",
    "description": "2D 랜덤워크를 p5.js로 실시간/즉시 모드로 시각화합니다. 경로·걸음·속도·줌·선/점 크기 조절 가능.",
    "order": 50,
    "hidden": False,
}

def render():
    st.markdown("### 2D 랜덤워크 (p5.js)")
    components.html(
        """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
  <style>
    body{margin:0}
    #wrap{max-width:1100px;margin:0 auto;padding:8px 10px 14px}
    .ui{font:14px ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial;display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px}
    .pill{background:#f3f4f6;border:1px solid #e5e7eb;padding:6px 10px;border-radius:8px}
    .pill input{width:90px}
    .btn{cursor:pointer;border:1px solid #d1d5db;background:#fff;border-radius:8px;padding:6px 12px}
    .btn:active{transform:translateY(1px)}
    #status{font-size:13px;color:#374151;margin-left:auto}
    canvas{display:block}
  </style>
</head>
<body>
  <div id="wrap">
    <div class="ui">
      <span class="pill">경로 <input id="paths" type="number" min="1" max="200" value="10"></span>
      <span class="pill">걸음 <input id="steps" type="number" min="10" max="20000" value="1000"></span>
      <span class="pill">속도(스텝/프레임) <input id="speed" type="number" min="1" max="500" value="10"></span>
      <span class="pill">줌 <input id="zoom" type="number" min="0.2" max="10" step="0.1" value="1.1"></span>
      <span class="pill">선두께 <input id="line" type="number" min="1" max="6" value="1"></span>
      <span class="pill">점크기 <input id="dot" type="number" min="0" max="10" value="2"></span>
      <span class="pill">Trace 길이 <input id="trace" type="number" min="50" max="5000" value="400"></span>
      <span class="pill">모드
        <select id="mode">
          <option value="live" selected>라이브</option>
          <option value="instant">즉시</option>
        </select>
      </span>
      <button id="reset" class="btn">리셋</button>
      <button id="clear" class="btn">캔버스 지우기</button>
      <button id="pause" class="btn">일시정지</button>
      <button id="resume" class="btn">재개</button>
      <span id="status"></span>
    </div>
    <div id="sketch-holder"></div>
    <noscript>p5.js 실행을 위해 브라우저의 자바스크립트를 허용해 주세요.</noscript>
  </div>

<script>
const sketch = (p)=>{
  let W = 1000, H = 660;
  let paths=10, steps=1000, speed=10, zoom=1.1, lineW=1, dot=2, traceKeep=400;
  let mode="live";
  let running=true, stepLeft=0;
  let walkers=[], colors=[];
  let lastDrawnSteps=0;

  const get = (id) => document.getElementById(id);
  function readUI(){
    paths = clamp(parseInt(get('paths').value||10), 1, 200);
    steps = clamp(parseInt(get('steps').value||1000), 10, 20000);
    speed = clamp(parseInt(get('speed').value||10), 1, 500);
    zoom  = clamp(parseFloat(get('zoom').value||1.1), 0.2, 10);
    lineW = clamp(parseInt(get('line').value||1), 1, 6);
    dot   = clamp(parseInt(get('dot').value||2), 0, 10);
    traceKeep = clamp(parseInt(get('trace').value||400), 50, 5000);
    mode = get('mode').value;
  }
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));

  function init(){
    readUI();
    walkers = [];
    colors = [];
    for(let i=0;i<paths;i++){
      walkers.push({x:0,y:0,trail:[]});
      // 각 경로마다 옅은 HSL 색상
      const h = (i*47)%360;
      colors.push(`hsla(${h},70%,35%,0.8)`);
    }
    stepLeft = steps;
    running = true;
    lastDrawnSteps = 0;
    p.background(255);
  }

  p.setup=()=>{
    const holder = get('sketch-holder');
    const pw = holder.clientWidth || 1000;
    W = Math.min(1000, pw);
    const cnv = p.createCanvas(W, H);
    cnv.parent('sketch-holder');
    p.pixelDensity(1);
    p.background(255);
    init();

    get('reset').onclick=init;
    get('clear').onclick=()=>{ p.background(255); };
    get('pause').onclick=()=>{ running=false; };
    get('resume').onclick=()=>{ running=true; };
    ['paths','steps','speed','zoom','line','dot','trace','mode'].forEach(id=>{
      get(id).addEventListener('change', ()=>{ readUI(); if(id==='paths'||id==='steps') init(); });
    });
  };

  p.windowResized=()=>{
    const holder = get('sketch-holder');
    const pw = holder.clientWidth || 1000;
    W = Math.min(1000, pw);
    p.resizeCanvas(W, H);
  };

  function stepOnce(w){
    const ang = Math.random()*Math.PI*2;
    const nx = w.x + Math.cos(ang);
    const ny = w.y + Math.sin(ang);
    // 방금 이동한 선분만 그리기 → 도형처럼 보이지 않음
    p.strokeWeight(lineW);
    p.line(w.x, w.y, nx, ny);
    if(dot>0){ p.noStroke(); p.fill(0,0,0,130); p.circle(nx, ny, dot); }
    // trail 관리 (필요 시 다시 그릴 때 사용)
    w.trail.push({x:nx, y:ny});
    if(w.trail.length>traceKeep) w.trail.shift();
    w.x = nx; w.y = ny;
  }

  function redrawAllFromTrail(){
    // 캔버스를 지우고 모든 trail을 다시 얇게 그림 (즉시모드 끝난 뒤 모양 확인용)
    p.background(255);
    p.push(); p.translate(W/2, H/2); p.scale(zoom);
    for(let i=0;i<walkers.length;i++){
      p.stroke(colors[i]); p.noFill(); p.strokeWeight(lineW);
      const t = walkers[i].trail;
      for(let k=1;k<t.length;k++){
        p.line(t[k-1].x, t[k-1].y, t[k].x, t[k].y);
      }
      if(dot>0 && t.length){
        p.noStroke(); p.fill(0,0,0,130); p.circle(t[t.length-1].x, t[t.length-1].y, dot);
      }
    }
    p.pop();
  }

  p.draw=()=>{
    p.push();
    p.translate(W/2, H/2);
    p.scale(zoom);

    if(mode==='instant' && running){
      // 모든 스텝을 즉시 계산 후 한 번에 재그림
      for(let s=0; s<stepLeft; s++){
        for(let i=0;i<walkers.length;i++){
          p.stroke(colors[i]);
          stepOnce(walkers[i]);
        }
      }
      stepLeft = 0;
      running = false;
      // 즉시 모드는 전체가 한꺼번에 그려져 캔버스가 누적되므로,
      // 필요하면 정리용 재그림 함수를 호출할 수도 있음.
    }else if(mode==='live' && running){
      // 프레임마다 speed 만큼만 움직임 → 진짜 “걷는” 느낌
      const iter = Math.min(speed, stepLeft);
      for(let s=0; s<iter; s++){
        for(let i=0;i<walkers.length;i++){
          p.stroke(colors[i]);
          stepOnce(walkers[i]);
        }
        stepLeft--;
        if(stepLeft<=0){ running=false; break; }
      }
    }
    p.pop();

    // 상태 표시
    const done = steps - stepLeft;
    if(done!==lastDrawnSteps){
      get('status').textContent = `진행 ${done}/${steps} · 경로 ${paths}개 · 속도 ${speed}/f · 줌 ${zoom.toFixed(2)} · 선 ${lineW} · 점 ${dot}`;
      lastDrawnSteps = done;
    }
  };
};

new p5(sketch, document.body);
</script>
</body>
</html>
        """,
        height=720,
        scrolling=True,
    )
