import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 주사위 실험(애니메이션)",
    "description": "주사위를 굴려 경험확률을 수집하고 이론확률과 비교합니다. (1개/2개 주사위, 조건 선택, 자동 연속 굴리기 지원)",
    "order": 999999,       # 맨 뒤로
    "hidden": True,        # 미니는 숨김
}

HTML = """
<div id="dice-mini-root" style="max-width:980px;margin:0 auto;">
  <style>
    .dm-card{border:1px solid #e5e7eb;border-radius:14px;padding:12px 14px;margin:8px 0;background:#fff;}
    .dm-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
    .dm-row > *{flex:0 0 auto}
    .dm-label{font-weight:600;margin-right:8px}
    .dm-num{font-variant-numeric: tabular-nums}
    .dm-badge{display:inline-block;padding:2px 8px;border-radius:999px;background:#eef2ff;border:1px solid #c7d2fe;font-size:12px}
    .dm-btn{padding:8px 12px;border-radius:10px;border:1px solid #d1d5db;background:#f8fafc;cursor:pointer}
    .dm-btn:active{transform:translateY(1px)}
    .dm-btn.primary{background:#2563eb;color:#fff;border-color:#1e40af}
    .dm-btn.warn{background:#fee2e2;border-color:#fecaca}
    .dm-select,.dm-input{padding:6px 8px;border-radius:8px;border:1px solid #d1d5db;background:#fff}
    .hint{color:#6b7280;font-size:13px}
    canvas{display:block}
  </style>

  <div class="dm-card">
    <div class="dm-row">
      <span class="dm-label">🎯 모드</span>
      <select id="modeSel" class="dm-select">
        <option value="one">주사위 1개</option>
        <option value="two">주사위 2개(합)</option>
      </select>

      <span class="dm-label">🎛 이벤트</span>
      <select id="eventSel" class="dm-select">
        <option value="odd">[1개] 홀수</option>
        <option value="prime">[1개] 소수(2,3,5)</option>
        <option value="eq6">[1개] 6</option>
        <option value="ge4">[1개] ≥ 4</option>
        <option value="custom">[1개] 사용자 정의(체크)</option>
        <option value="sum7">[2개] 합=7</option>
        <option value="sumX">[2개] 합=X</option>
        <option value="sumGE">[2개] 합≥X</option>
        <option value="doubles">[2개] 더블</option>
        <option value="atleast6">[2개] 최소 하나 6</option>
      </select>

      <span id="eventParamWrap" style="display:none;">
        <span class="dm-label">X</span>
        <input id="eventX" type="number" class="dm-input" value="9" min="2" max="12" style="width:72px;">
      </span>

      <span id="customSetWrap" style="display:none;">
        <span class="dm-label">포함 눈</span>
        <span class="hint">(아래 체크)</span>
      </span>
    </div>

    <div class="dm-row" id="customChecks" style="display:none;">
      <label><input type="checkbox" class="faceCk" value="1">1</label>
      <label><input type="checkbox" class="faceCk" value="2">2</label>
      <label><input type="checkbox" class="faceCk" value="3">3</label>
      <label><input type="checkbox" class="faceCk" value="4">4</label>
      <label><input type="checkbox" class="faceCk" value="5">5</label>
      <label><input type="checkbox" class="faceCk" value="6">6</label>
    </div>

    <div class="dm-row">
      <span class="dm-label">속도</span>
      <input id="speed" type="range" min="1" max="100" value="40">
      <span class="hint">느림 ← → 빠름</span>

      <span class="dm-label">한 번에</span>
      <input id="bulk" type="number" class="dm-input" value="1" min="1" max="1000" style="width:80px;">
    </div>

    <div class="dm-row">
      <button id="rollOnce" class="dm-btn primary">한 번 굴리기</button>
      <button id="autoToggle" class="dm-btn">자동 시작</button>
      <button id="rollBulkBtn" class="dm-btn">한 번에 N회</button>
      <button id="resetBtn" class="dm-btn warn">초기화</button>
      <span class="dm-badge">실험 목적: 경험확률 vs 이론확률 비교, 대수의 법칙 체험</span>
    </div>
  </div>

  <div class="dm-card">
    <div class="dm-row">
      <div><span class="dm-label">총 시행</span> <span id="tot" class="dm-num">0</span></div>
      <div><span class="dm-label">이벤트 적중</span> <span id="hits" class="dm-num">0</span></div>
      <div><span class="dm-label">경험확률</span> <span id="pEmp" class="dm-num">-</span></div>
      <div><span class="dm-label">이론확률</span> <span id="pTh" class="dm-num">-</span></div>
    </div>
  </div>

  <div class="dm-card">
    <div class="dm-row" style="align-items:flex-start;">
      <div>
        <div class="dm-label">🎲 주사위 애니메이션</div>
        <div id="p5holder"></div>
        <div class="hint">굴리는 동안 빠르게 면이 바뀌고, 멈추면 최종 눈이 확정돼요.</div>
      </div>
      <div style="flex:1;">
        <div class="dm-label">📈 분포(막대)</div>
        <canvas id="hist" width="520" height="240" style="border:1px solid #e5e7eb;border-radius:10px;"></canvas>
        <div class="hint" id="histHint">주사위 1개: 눈(1~6) 분포 / 2개: 합(2~12) 분포</div>
      </div>
    </div>
  </div>
</div>

<!-- p5.js -->
<script src="https://cdn.jsdelivr.net/npm/p5@1.7.0/lib/p5.min.js"></script>
<script>
(function(){
  const el = (id)=>document.getElementById(id);
  const modeSel = el("modeSel");
  const eventSel = el("eventSel");
  const eventParamWrap = el("eventParamWrap");
  const eventX = el("eventX");
  const customSetWrap = el("customSetWrap");
  const customChecks = el("customChecks");
  const speed = el("speed");
  const bulk = el("bulk");
  const rollOnce = el("rollOnce");
  const autoToggle = el("autoToggle");
  const rollBulkBtn = el("rollBulkBtn");
  const resetBtn = el("resetBtn");
  const totEl = el("tot");
  const hitsEl = el("hits");
  const pEmpEl = el("pEmp");
  const pThEl = el("pTh");
  const histCanvas = el("hist");
  const histCtx = histCanvas.getContext("2d");
  const holder = el("p5holder");

  // 상태
  let mode = "one";                 // "one" | "two"
  let rolling = false;
  let auto = false;
  let animTick = 0;
  let animMax = 18;

  // 집계
  let total = 0, hits = 0;
  let counts1 = Array(6).fill(0);     // 1개 주사위
  let counts2 = Array(13).fill(0);    // 합 0~12 (2~12만 사용)

  // 커스텀 이벤트(1개 모드)
  let customFaces = new Set();

  function rand1to6(){ return 1 + Math.floor(Math.random()*6); }

  function theoreticalP(){
    if(mode==="one"){
      const ev = eventSel.value;
      if(ev==="odd") return 3/6;
      if(ev==="prime") return 3/6;            // 2,3,5
      if(ev==="eq6") return 1/6;
      if(ev==="ge4") return 3/6;              // 4,5,6
      if(ev==="custom") return customFaces.size/6 || 0;
      return 0;
    }else{
      const ev = eventSel.value;
      const totalOut = 36;
      if(ev==="sum7"){ return 6/36; }
      if(ev==="doubles"){ return 6/36; }
      if(ev==="atleast6"){ return 11/36; }    // 1 - (5/6)^2
      if(ev==="sumX"){
        const X = +eventX.value;
        if(X<2 || X>12) return 0;
        const ways = waysToSum(X);
        return ways/36;
      }
      if(ev==="sumGE"){
        const X = +eventX.value;
        let cnt=0;
        for(let s=Math.max(2,X); s<=12; s++) cnt += waysToSum(s);
        return cnt/36;
      }
      return 0;
    }
  }

  function waysToSum(s){ // 두 주사위 합의 경우의 수
    if(s<2 || s>12) return 0;
    return s<=7 ? (s-1) : (13-s);
  }

  function eventHit(vals){
    if(mode==="one"){
      const d = vals[0];
      const ev = eventSel.value;
      if(ev==="odd") return (d%2===1);
      if(ev==="prime") return (d===2||d===3||d===5);
      if(ev==="eq6") return d===6;
      if(ev==="ge4") return d>=4;
      if(ev==="custom") return customFaces.has(d);
      return false;
    }else{
      const d1=vals[0], d2=vals[1], s=vals[2];
      const ev = eventSel.value;
      if(ev==="sum7") return s===7;
      if(ev==="doubles") return d1===d2;
      if(ev==="atleast6") return (d1===6 || d2===6);
      if(ev==="sumX") return s===+eventX.value;
      if(ev==="sumGE") return s>=+eventX.value;
      return false;
    }
  }

  function updateStats(vals){
    total++;
    if(mode==="one"){
      counts1[vals[0]-1]++;
    }else{
      counts2[vals[2]]++; // 2..12
    }
    if(eventHit(vals)) hits++;
    renderStats();
    drawHist();
  }

  function renderStats(){
    const pEmp = total>0 ? (hits/total) : 0;
    const pTh = theoreticalP();
    totEl.textContent = total.toLocaleString();
    hitsEl.textContent = hits.toLocaleString();
    pEmpEl.textContent = (total>0 ? pEmp.toFixed(4) : "-");
    pThEl.textContent = (pTh>0 ? pTh.toFixed(4) : "-");
  }

  function drawHist(){
    const ctx = histCtx;
    ctx.clearRect(0,0,histCanvas.width,histCanvas.height);
    const W = histCanvas.width, H = histCanvas.height;
    ctx.fillStyle="#f8fafc";
    ctx.fillRect(0,0,W,H);

    // 축 여백
    const left=42, right=10, top=14, bottom=36;
    const innerW = W - left - right;
    const innerH = H - top - bottom;

    // 데이터
    let labels, data, thData=null;
    if(mode==="one"){
      labels = [1,2,3,4,5,6];
      data = labels.map(v => counts1[v-1]);
      // 이론: 1/6 균등
      if(total>0){ thData = labels.map(_ => total/6); }
    }else{
      labels = [2,3,4,5,6,7,8,9,10,11,12];
      data = labels.map(s => counts2[s]);
      if(total>0){
        thData = labels.map(s => total * (waysToSum(s)/36));
      }
    }

    const maxVal = Math.max(1, ...data, ...(thData||[0]));
    const yMax = maxVal * 1.15;

    // y축 눈금
    ctx.strokeStyle="#d1d5db";
    ctx.fillStyle="#6b7280";
    ctx.lineWidth=1;
    const ticks = 4;
    ctx.beginPath();
    for(let i=0;i<=ticks;i++){
      const y = top + innerH - (innerH*(i/ticks));
      ctx.moveTo(left, y);
      ctx.lineTo(W-right, y);
      const val = Math.round(yMax*(i/ticks));
      ctx.fillText(String(val), 4, y+4);
    }
    ctx.stroke();

    const n = labels.length;
    const gap = 6;
    const barW = (innerW - gap*(n-1)) / n;

    // bars
    for(let i=0;i<n;i++){
      const v = data[i];
      const h = innerH * (v / yMax);
      const x = left + i*(barW + gap);
      const y = top + innerH - h;
      ctx.fillStyle="#60a5fa";
      ctx.fillRect(x,y,barW,h);
      // 라벨
      ctx.fillStyle="#111827";
      ctx.textAlign="center";
      ctx.fillText(String(labels[i]), x+barW/2, H-16);
    }

    // 이론선
    if(thData){
      ctx.strokeStyle="#ef4444";
      ctx.lineWidth=2;
      ctx.beginPath();
      for(let i=0;i<n;i++){
        const v = thData[i];
        const y = top + innerH - (innerH*(v/yMax));
        const x = left + i*(barW + gap) + barW/2;
        if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
      }
      ctx.stroke();
      ctx.textAlign="left";
      ctx.fillStyle="#ef4444";
      ctx.fillText("이론 곡선", W-90, 14);
      ctx.textAlign="center";
    }
  }

  // p5 스케치 (주사위 애니메이션)
  let sketch = (p)=>{
    let w=280, h=200;
    p.setup = ()=>{
      let c = p.createCanvas(w,h);
      c.parent(holder);
      p.frameRate(60);
      p.textFont("sans-serif");
    };

    function drawDie(cx,cy,size,face){
      // 외곽
      p.noStroke();
      p.fill(250);
      p.rectMode(p.CENTER);
      p.rect(cx,cy,size,size,16);
      p.stroke(220);
      p.noFill();
      p.rect(cx,cy,size,size,16);

      // pip 좌표
      const r = size*0.14;
      const offs = size*0.25;
      const dots = {
        1: [[0,0]],
        2: [[-offs,-offs],[offs,offs]],
        3: [[-offs,-offs],[0,0],[offs,offs]],
        4: [[-offs,-offs],[offs,-offs],[-offs,offs],[offs,offs]],
        5: [[-offs,-offs],[offs,-offs],[0,0],[-offs,offs],[offs,offs]],
        6: [[-offs,-offs],[offs,-offs],[-offs,0],[offs,0],[-offs,offs],[offs,offs]],
      }[face] || [[0,0]];
      p.noStroke();
      p.fill(20);
      for(const [dx,dy] of dots){
        p.circle(cx+dx, cy+dy, r);
      }
    }

    let d1=1, d2=1;

    p.draw = ()=>{
      p.background(255);
      // 애니메이션 중엔 얼굴이 빠르게 바뀜
      if(rolling){
        animTick++;
        if(animTick>=animMax){
          // 확정 굴림
          if(mode==="one"){
            d1 = rand1to6();
            drawDie(w*0.5,h*0.55,120,d1);
            updateStats([d1]);
          }else{
            d1 = rand1to6();
            d2 = rand1to6();
            drawDie(w*0.35,h*0.55,108,d1);
            drawDie(w*0.65,h*0.55,108,d2);
            updateStats([d1,d2,d1+d2]);
          }
          rolling=false;
        }else{
          // 회전 효과: 랜덤 면
          const f1 = rand1to6();
          const f2 = rand1to6();
          if(mode==="one"){
            drawDie(w*0.5,h*0.55,120,f1);
          }else{
            drawDie(w*0.35,h*0.55,108,f1);
            drawDie(w*0.65,h*0.55,108,f2);
          }
        }
      }else{
        // 정지면 표시
        if(mode==="one"){
          drawDie(w*0.5,h*0.55,120,d1);
        }else{
          drawDie(w*0.35,h*0.55,108,d1);
          drawDie(w*0.65,h*0.55,108,d2);
        }
      }

      // 상단 정보
      p.fill(17);
      p.noStroke();
      p.textSize(16);
      p.textAlign(p.CENTER,p.CENTER);
      p.text(mode==="one" ? "주사위 1개" : "주사위 2개", w/2, 18);

      // 자동 롤링
      if(auto && !rolling){
        // 속도에 따라 대기 프레임 조절
        const spd = +speed.value; // 1..100
        animMax = Math.max(6, Math.round(26 - spd*0.18)); // 빠를수록 animMax 작게
        roll();
      }
    };
  };
  new p5(sketch);

  function roll(){
    if(rolling) return;
    rolling = true;
    animTick = 0;
  }

  function rollBulk(n){
    // 애니메이션 생략, 결과만 빠르게 집계
    if(mode==="one"){
      for(let i=0;i<n;i++){
        const d = rand1to6();
        counts1[d-1]++; total++; if(eventHit([d])) hits++;
      }
    }else{
      for(let i=0;i<n;i++){
        const d1=rand1to6(), d2=rand1to6();
        const s=d1+d2; counts2[s]++; total++; if(eventHit([d1,d2,s])) hits++;
      }
    }
    renderStats();
    drawHist();
  }

  // UI 이벤트
  modeSel.addEventListener("change", ()=>{
    mode = modeSel.value;
    reset(false);
    histHint.textContent = mode==="one" ? "주사위 1개: 눈(1~6) 분포" : "2개: 합(2~12) 분포";
    updateParamVisibility();
    renderStats();
    drawHist();
  });

  function updateParamVisibility(){
    const ev = eventSel.value;
    eventParamWrap.style.display = (ev==="sumX"||ev==="sumGE") ? "" : "none";
    const isCustom = (ev==="custom");
    customSetWrap.style.display = isCustom ? "" : "none";
    customChecks.style.display = isCustom ? "" : "none";
  }
  eventSel.addEventListener("change", ()=>{
    updateParamVisibility();
    renderStats();
    drawHist();
  });
  eventX.addEventListener("input", ()=>{ renderStats(); drawHist(); });

  document.querySelectorAll(".faceCk").forEach(ck=>{
    ck.addEventListener("change", (e)=>{
      const v = +e.target.value;
      if(e.target.checked) customFaces.add(v); else customFaces.delete(v);
      renderStats(); drawHist();
    });
  });

  rollOnce.addEventListener("click", ()=> roll());
  rollBulkBtn.addEventListener("click", ()=>{
    const n = Math.max(1, Math.min(10000, +bulk.value||1));
    rollBulk(n);
  });
  autoToggle.addEventListener("click", ()=>{
    auto = !auto;
    autoToggle.textContent = auto ? "자동 정지" : "자동 시작";
  });
  resetBtn.addEventListener("click", ()=> reset(true));

  function reset(clearFaces){
    total=0; hits=0; counts1.fill(0); counts2.fill(0);
    rolling=false; animTick=0;
    if(clearFaces){ customFaces.clear(); document.querySelectorAll(".faceCk").forEach(c=> c.checked=false); }
    renderStats(); drawHist();
  }

  // 초기 UI 세팅
  updateParamVisibility();
  renderStats(); drawHist();
})();
</script>
"""

def render():
    st.header("🎲 미니: 주사위 실험(애니메이션)")
    st.caption("주사위를 1개/2개로 굴려 경험확률을 모으고 이론값과 비교합니다. 자동 연속 실행/맞춤 이벤트/히스토그램 제공.")

    components.html(HTML, height=680, scrolling=False)

    with st.expander("수업용 가이드 / 미션", expanded=False):
        st.markdown(
            """
            **활동 목적**  
            - 주사위 실험을 통해 **경험확률과 이론확률**을 비교하고, 시행 횟수에 따른 수렴(대수의 법칙)을 체감합니다.  
            - 2개 주사위의 **합 분포(2~12)**를 관찰하고, 이론 분포와의 차이를 시각적으로 확인합니다.  
            
            **권장 진행 순서**  
            1) 모드 **주사위 1개**: 이벤트를 `홀수`, `소수`, `=6`, `≥4` 등으로 바꿔가며 자동 실행으로 경험확률이 이론값에 가까워지는지 확인  
            2) 모드 **주사위 2개(합)**: `합=7`, `합=X`, `합≥X`, `더블`, `최소 하나 6` 등 다양한 사건으로 비교  
            3) **사용자 정의(1개)**: 포함할 눈을 직접 체크하여 임의 사건의 이론값(선택면/6)과 경험값 비교  
            
            **팁**  
            - `한 번에 N회`로 대량 집계를 빠르게 수행하고, `자동 시작`으로 부드러운 애니메이션 체험을 제공합니다.  
            - 히스토그램의 **빨간 선**은 이론 기대도수(현재 시행 수 × 이론확률)입니다.
            """
        )
