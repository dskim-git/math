# activities/common/circular_permutation_p5.py
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "원순열 시각화 (p5.js)",
    "description": "한 사람(1번)을 기준으로 회전 동치를 제거하면 (n−1)! 이 되는 이유를 시각화합니다.",
    "order": 40,
}

def render():
    st.markdown("### 🔁 원순열 시각화")
    st.caption("바깥 원: 현재 배치 · 안쪽 원: 사람 1번을 맨 위로 회전시킨 ‘정준형’ 배치 · 아래: 회전 동치 전부(썸네일)")

    html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<style>
  body { margin:0; }
  .ui { font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, Arial; font-size:14px; }
  #wrap { max-width: 980px; margin: 6px auto 0 auto; padding: 0 8px; }
  #panel { display:flex; gap:8px; align-items:center; flex-wrap: wrap; margin-bottom:8px; }
  #panel > * { margin: 4px 0; }
  .kpi { display:flex; gap:20px; margin:6px 0 10px; color:#333;}
  .kpi .box { background:#f6f7fb; border:1px solid #dfe4f2; padding:8px 10px; border-radius:8px; }
  .legend { font-size: 13px; color:#555; margin-top:6px; }
  canvas { outline: none; }
</style>
</head>
<body>
<div id="wrap" class="ui">
  <div id="panel">
    <label>사람 수 n:
      <input id="nSlider" type="range" min="3" max="12" value="6" />
      <span id="nVal">6</span>
    </label>
    <button id="btnShuffle">무작위 섞기</button>
    <button id="btnLeft">⟲ 좌회전</button>
    <button id="btnRight">⟳ 우회전</button>
    <label style="margin-left:6px;">
      <input id="chkGallery" type="checkbox" checked />
      회전 동치 모두 보기(썸네일)
    </label>
  </div>

  <div class="kpi">
    <div class="box">선형 배치 수 <b id="linCnt">n!</b></div>
    <div class="box">서로 다른 원배치 수 <b id="cycCnt">(n−1)!</b></div>
  </div>

  <div class="legend">파란 링 = 사람 1번,  ⬆︎ = 시작 좌석,  바깥 원 = 현재 배치,  안쪽 원 = 1번을 맨 위로 맞춘 정준형</div>
</div>

<script>
let sketch = (p) => {
  let W = 960, H = 740;     // 전체 높이를 늘리면 썸네일까지 공간 증가
  let cx, cy;
  let perm = [];            // 현재 배치
  let n = 6;
  let showGallery = true;

  // UI 엘리먼트 참조
  let $nSlider, $nVal, $linCnt, $cycCnt, $chkGallery;

  p.setup = function () {
    let c = p.createCanvas(W, H);
    c.parent("wrap");
    cx = p.width/2; cy = 250;

    // 초기 perm
    resetPerm(n);

    // DOM
    $nSlider = document.getElementById("nSlider");
    $nVal    = document.getElementById("nVal");
    $linCnt  = document.getElementById("linCnt");
    $cycCnt  = document.getElementById("cycCnt");
    $chkGallery = document.getElementById("chkGallery");

    $nSlider.addEventListener("input", () => {
      n = parseInt($nSlider.value);
      $nVal.textContent = n;
      resetPerm(n);
      updateKPI();
    });

    document.getElementById("btnShuffle").addEventListener("click", () => {
      fisherYates(perm);   // 확실한 제자리 셔플
    });
    document.getElementById("btnLeft").addEventListener("click", () => {
      rotateLeft(perm);
    });
    document.getElementById("btnRight").addEventListener("click", () => {
      rotateRight(perm);
    });
    $chkGallery.addEventListener("change", () => {
      showGallery = $chkGallery.checked;
    });

    updateKPI();
  };

  function resetPerm(m) {
    perm = Array.from({length:m}, (_,i)=>i+1);
  }

  function fisherYates(arr) {
    for (let i = arr.length-1; i>0; i++){
      const j = Math.floor(Math.random()*(i+1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }
  function rotateLeft(arr){
    if (arr.length<=1) return;
    const x = arr.shift();
    arr.push(x);
  }
  function rotateRight(arr){
    if (arr.length<=1) return;
    const x = arr.pop();
    arr.unshift(x);
  }

  function factorial(k){
    let v = 1;
    for (let i=2;i<=k;i++) v*=i;
    return v;
  }
  function updateKPI(){
    $linCnt.textContent = factorial(n).toLocaleString();
    $cycCnt.textContent = factorial(n-1).toLocaleString();
  }

  // 정준형(1번을 맨 위로 오도록 회전시킨 배열)을 생성
  function canonicalOf(a){
    const b = a.slice();
    const idx = b.indexOf(1);
    // idx가 0이 되도록 왼쪽으로 회전
    for (let k=0;k<idx;k++) rotateLeft(b);
    return b;
  }

  // 원을 그리는 유틸
  function drawCircleLabels(centerX, centerY, radius, arr, highlightOne=true, startMark=true){
    p.push();
    p.translate(centerX, centerY);

    // 시작 좌석(맨 위) 마크
    if (startMark){
      p.stroke(180); p.strokeWeight(2);
      p.line(0, -radius-12, 0, -radius+6);
      p.noStroke(); p.fill(180); p.triangle(-5, -radius+6, 5, -radius+6, 0, -radius+14);
    }

    // 테두리
    p.noFill(); p.stroke(200); p.strokeWeight(2.2);
    p.circle(0,0, radius*2);

    // 라벨
    p.textAlign(p.CENTER, p.CENTER);
    p.textSize(16);
    for (let i=0;i<arr.length;i++){
      const ang = -p.HALF_PI + i * (p.TWO_PI/arr.length);
      const x = radius*Math.cos(ang);
      const y = radius*Math.sin(ang);
      // 점
      p.noStroke(); p.fill(40);
      p.circle(x,y, 5);
      // 숫자
      p.fill(30);
      p.text(arr[i], x, y-18);
      // 1번 링
      if (highlightOne && arr[i]===1){
        p.noFill(); p.stroke(40,130,255); p.strokeWeight(3);
        p.circle(x,y, 22);
      }
    }
    p.pop();
  }

  // 회전을 정준형으로 맞추기 위한 각도(시각화)
  function rotationOffsetAngle(arr){
    const idx = arr.indexOf(1);
    return idx * (p.TWO_PI / arr.length);
  }

  p.draw = function () {
    p.clear();
    p.background(255);

    // 제목
    p.fill(30); p.noStroke();
    p.textAlign(p.CENTER, p.CENTER);
    p.textSize(18);
    p.text("바깥: 현재 배치 / 안쪽: 1번을 맨 위로 회전시킨 정준형", p.width/2, 22);

    // 바깥 원(현재)
    drawCircleLabels(cx, cy, 170, perm, true, true);

    // 안쪽 원(정준형)
    const canon = canonicalOf(perm);
    drawCircleLabels(cx, cy, 105, canon, true, true);

    // 회전량 시각화(주황 화살표)
    const ang = rotationOffsetAngle(perm);
    p.push();
    p.translate(cx, cy);
    p.stroke(255,140,0); p.strokeWeight(3);
    p.noFill();
    p.arc(0,0, 190*2,190*2, -p.HALF_PI, -p.HALF_PI + ang, {open:true});
    // 화살표 머리
    const hx = 190*Math.cos(-p.HALF_PI+ang), hy = 190*Math.sin(-p.HALF_PI+ang);
    p.fill(255,140,0); p.noStroke();
    p.triangle(hx,hy, hx-10*Math.cos(-p.HALF_PI+ang-0.3), hy-10*Math.sin(-p.HALF_PI+ang-0.3),
                    hx-10*Math.cos(-p.HALF_PI+ang+0.3), hy-10*Math.sin(-p.HALF_PI+ang+0.3));
    p.pop();

    // 썸네일 갤러리(회전 동치)
    if (showGallery){
      const topY = 390;           // 갤러리 시작 y
      const cell = 120;           // 셀 크기
      const cols = Math.floor(p.width / cell);
      const r = 36;
      p.fill(40); p.noStroke();
      p.textAlign(p.LEFT, p.CENTER);
      p.textSize(14);
      p.text("회전 동치(현재 배치의 n가지 회전):", 14, topY-18);

      // 각 회전 상태를 작은 원으로
      let tmp = perm.slice();
      for (let k=0; k<n; k++){
        const col = k % cols;
        const row = Math.floor(k / cols);
        const cx2 = 20 + col*cell + cell/2;
        const cy2 = topY + row*cell + cell/2;

        // 테두리
        p.noFill(); p.stroke(210); p.strokeWeight(1.6);
        p.circle(cx2, cy2, r*2);

        // 시작좌석 표시
        p.stroke(180); p.strokeWeight(2);
        p.line(cx2, cy2-r-8, cx2, cy2-r+4);

        // 점/숫자
        p.textAlign(p.CENTER, p.CENTER);
        p.textSize(12);
        for (let i=0;i<n;i++){
          const ang2 = -p.HALF_PI + i*(p.TWO_PI/n);
          const x = cx2 + r*Math.cos(ang2);
          const y = cy2 + r*Math.sin(ang2);
          p.noStroke(); p.fill(40);
          p.circle(x,y,3.5);
          p.fill(30);
          p.text(tmp[i], x, y-12);
          if (tmp[i]===1){
            p.noFill(); p.stroke(40,130,255); p.strokeWeight(2);
            p.circle(x,y, 16);
          }
        }

        // 다음 회전
        rotateLeft(tmp);
      }
    }
  };
};
new p5(sketch);
</script>
</body>
</html>
    """
    components.html(html, height=820)
