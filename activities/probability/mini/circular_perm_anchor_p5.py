# activities/common/circular_permutation_p5.py
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "원순열 시각화 (p5.js, 경량)",
    "description": "한 자리를 고정(1번)하면 회전 동치가 제거되어 (n−1)! 이 되는 직관을 시각화합니다.",
    "order": 40,
}

def render():
    st.markdown("### 🔁 원순열 시각화 (경량판)")
    st.caption("바깥 원 = 현재 배치 · 안쪽 원 = 1번을 맨 위로 맞춘 정준형 배치")
    html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<style>
  body { margin:0; }
  #wrap { max-width: 880px; margin: 6px auto 0 auto; padding: 0 8px; font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, Arial; }
  #panel { display:flex; gap:10px; align-items:center; flex-wrap: wrap; margin-bottom:8px; }
  #panel > * { margin: 4px 0; }
  .kpi { display:flex; gap:16px; margin:6px 0 10px; color:#333;}
  .kpi .box { background:#f6f7fb; border:1px solid #dfe4f2; padding:6px 10px; border-radius:8px; }
  .legend { font-size: 13px; color:#555; margin-top:6px; }
</style>
</head>
<body>
<div id="wrap">
  <div id="panel">
    <label>사람 수 n:
      <input id="nSlider" type="range" min="3" max="12" value="6" />
      <span id="nVal">6</span>
    </label>
    <button id="btnShuffle">무작위 섞기</button>
    <button id="btnLeft">⟲ 좌회전</button>
    <button id="btnRight">⟳ 우회전</button>
  </div>

  <div class="kpi">
    <div class="box">선형 배치 수 <b id="linCnt">n!</b></div>
    <div class="box">서로 다른 원배치 수 <b id="cycCnt">(n−1)!</b></div>
  </div>

  <div class="legend">파란 링 = 사람 1번,  ⬆︎ = 시작 좌석,  바깥 원 = 현재 배치,  안쪽 원 = 1번을 맨 위로 맞춘 정준형</div>
</div>

<script>
let sketch = (p) => {
  const W = 860, H = 480;
  let cx, cy;
  let n = 6;
  let perm = []; // 현재 배치(전역 유지)

  // KPI DOM
  let $nSlider, $nVal, $linCnt, $cycCnt;

  p.setup = function(){
    const c = p.createCanvas(W, H);
    c.parent("wrap");
    cx = p.width/2; cy = 240;

    // 초기 perm
    resetPerm(n);

    // UI 바인딩
    $nSlider = document.getElementById("nSlider");
    $nVal    = document.getElementById("nVal");
    $linCnt  = document.getElementById("linCnt");
    $cycCnt  = document.getElementById("cycCnt");

    $nSlider.addEventListener("input", () => {
      n = parseInt($nSlider.value);
      $nVal.textContent = n;
      resetPerm(n);
      updateKPI();
    });

    document.getElementById("btnShuffle").addEventListener("click", () => {
      fisherYates(perm); // 제자리 셔플(상태 유지)
    });
    document.getElementById("btnLeft").addEventListener("click", () => rotateLeft(perm));
    document.getElementById("btnRight").addEventListener("click", () => rotateRight(perm));

    updateKPI();
  };

  function resetPerm(m){
    perm = Array.from({length:m}, (_,i)=>i+1);
  }
  function fisherYates(arr){
    for (let i=arr.length-1; i>0; i--){
      const j = Math.floor(Math.random()*(i+1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }
  function rotateLeft(arr){
    if (arr.length<=1) return;
    const x = arr.shift(); arr.push(x);
  }
  function rotateRight(arr){
    if (arr.length<=1) return;
    const x = arr.pop(); arr.unshift(x);
  }
  function factorial(k){
    let v=1; for (let i=2;i<=k;i++) v*=i; return v;
  }
  function updateKPI(){
    $linCnt.textContent = factorial(n).toLocaleString();
    $cycCnt.textContent = factorial(n-1).toLocaleString();
  }
  function canonicalOf(a){
    const b = a.slice();
    const idx = b.indexOf(1);
    for (let k=0;k<idx;k++) rotateLeft(b);
    return b;
  }

  function drawCircleLabels(centerX, centerY, radius, arr, highlightOne=true, startMark=true){
    p.push();
    p.translate(centerX, centerY);

    // 시작 좌석 표시(맨 위)
    if (startMark){
      p.stroke(180); p.strokeWeight(2);
      p.line(0, -radius-12, 0, -radius+6);
      p.noStroke(); p.fill(180);
      p.triangle(-5, -radius+6, 5, -radius+6, 0, -radius+14);
    }

    // 외곽 원
    p.noFill(); p.stroke(200); p.strokeWeight(2.2);
    p.circle(0,0, radius*2);

    // 점과 라벨
    p.textAlign(p.CENTER, p.CENTER);
    p.textSize(16);
    for (let i=0;i<arr.length;i++){
      const ang = -p.HALF_PI + i * (p.TWO_PI/arr.length);
      const x = radius*Math.cos(ang), y = radius*Math.sin(ang);

      p.noStroke(); p.fill(40);
      p.circle(x,y, 5);

      p.fill(30);
      p.text(arr[i], x, y-18);

      if (highlightOne && arr[i]===1){
        p.noFill(); p.stroke(40,130,255); p.strokeWeight(3);
        p.circle(x,y, 22);
      }
    }
    p.pop();
  }

  p.draw = function(){
    p.clear();
    p.background(255);

    // 제목
    p.fill(30); p.noStroke();
    p.textAlign(p.CENTER, p.CENTER);
    p.textSize(18);
    p.text("바깥: 현재 배치 / 안쪽: 1번을 맨 위로 회전시킨 정준형", p.width/2, 24);

    // 바깥(현재) & 안쪽(정준형) 원
    drawCircleLabels(cx, cy, 170, perm, true, true);
    const canon = canonicalOf(perm);
    drawCircleLabels(cx, cy, 105, canon, true, true);
  };
};
new p5(sketch);
</script>
</body>
</html>
    """
    components.html(html, height=520)
