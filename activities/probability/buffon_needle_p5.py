# activities/probability/buffon_needle_p5.py
import streamlit as st
import streamlit.components.v1 as components
from utils import page_header

META = {
    "title": "뷔퐁의 바늘문제",
    "description": "평행선 위로 바늘을 떨어뜨려 π를 추정하는 고전적 시뮬레이션.",
    "order": 60,
}

def render():
    page_header("뷔퐁의 바늘 실험 (p5.js)", "평행선 교차 확률로 π 추정", "🪡", top_rule=True)

    st.markdown(
        """
        - 바늘 길이 **L**, 선 간격 **d**(두 평행선 사이의 거리), 투척 횟수 **n**을 정한 뒤 바늘을 무작위로 떨어뜨립니다.  
        - 교차 횟수를 **hits**라 할 때, 고전적 설정(**L ≤ d**)에서는 아래 관계로 π를 추정할 수 있습니다.  
        """,
        unsafe_allow_html=True,
    )
    
    st.latex(
    r"P(\text{교차})=\frac{2L}{\pi d},\qquad \Rightarrow\quad "
    r"\pi \approx \frac{2L\cdot n}{\text{hits}\cdot d}"
    )
    
    st.markdown(
        """ 
        - **Run Live**(한 개씩), **Run Fast**(묶음), **Auto/Pause**(자동 반복)을 지원합니다.
        """,
        unsafe_allow_html=True,
    )
    

    # p5.js 스케치: iframe 내부에서 글로벌 모드로 실행되도록 캡슐화
    html = r'''
    <div id="buffon-holder" style="width:100%;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
    <script>
    // === 원본 로직을 최대한 유지하면서 반응형/레이아웃만 보완 ===
    let needleInput, spacingInput, lengthInput;
    let runLiveBtn, runFastBtn, resetBtn, autoBtn, pauseBtn;

    let lineSpacing = 100;
    let needleLength = 80;

    let numNeedles = 0;
    let hits = 0;
    let currentNeedle = 0;
    let currentTarget = 0;
    let simulateLive = true;
    let simulationRunning = false;
    let autoRunning = false;

    let piHistory = [];
    let yLine1 = 0;
    let yLine2 = 0;
    let yCenterMin = 0;
    let yCenterMax = 0;

    // 반응형 캔버스
    let canvasW = 900;
    let canvasH = 520;
    function fitSize() {
      const holder = document.getElementById('buffon-holder');
      const w = (holder && holder.clientWidth) ? holder.clientWidth : (window.innerWidth - 32);
      canvasW = Math.min(w, 1100);
      canvasH = 520;
    }

    function setup() {
      fitSize();
      const c = createCanvas(canvasW, canvasH);
      c.parent('buffon-holder');
      textFont('Arial');
      textStyle(NORMAL);
      textSize(25);

      needleInput = createInput('100');
      needleInput.size(100);

      spacingInput = createInput('100');
      spacingInput.size(100);

      lengthInput = createInput('80');
      lengthInput.size(100);

      runLiveBtn = createButton('Run Live');
      runLiveBtn.mousePressed(() => {
        simulateLive = true;
        startSimulation();
      });

      runFastBtn = createButton('Run Fast');
      runFastBtn.mousePressed(() => {
        simulateLive = false;
        startSimulation();
        while (simulationRunning && currentNeedle < currentTarget) {
          dropNeedle();
        }
        simulationRunning = false;
      });

      resetBtn = createButton('Reset');
      resetBtn.mousePressed(resetSim);

      autoBtn = createButton('Auto');
      autoBtn.mousePressed(() => { autoRunning = true; simulateLive = false; });

      pauseBtn = createButton('Pause');
      pauseBtn.mousePressed(() => { autoRunning = false; });

      layoutControls();
    }

    function windowResized() {
      fitSize();
      resizeCanvas(canvasW, canvasH);
      layoutControls();
    }

    function layoutControls() {
      // 상단 좌측에 입력 3개, 우측에 버튼 3+2
      const left = 20;
      const top = 12;

      needleInput.position(left + 10, top);
      spacingInput.position(left + 160, top);
      lengthInput.position(left + 310, top);

      runLiveBtn.position(left + 460, top);
      runFastBtn.position(left + 550, top);
      resetBtn.position(left + 640, top);

      autoBtn.position(left + 460, top + 35);
      pauseBtn.position(left + 550, top + 35);
    }

    function draw() {
      drawLines();

      if (simulateLive && simulationRunning && currentNeedle < currentTarget) {
        dropNeedle();
      } else if (simulateLive && simulationRunning && currentNeedle >= currentTarget) {
        simulationRunning = false;
      }

      if (autoRunning && !simulationRunning) {
        simulateLive = false;
        startSimulation();
        while (simulationRunning && currentNeedle < currentTarget) {
          dropNeedle();
        }
        simulationRunning = false;
      }

      showPi();
      drawGraph();

      // 경고: L > d 에서는 고전식 P = 2L/(π d)가 정확하지 않음을 알림
      const L = needleLength, d = lineSpacing;
      if (L > d) {
        noStroke();
        fill(255, 245, 225);
        rect(18, 178, 520, 28);
        fill(180, 90, 0);
        textSize(16);
        text('주의: L > d 인 경우 고전식 P = (2L)/(π d)는 근사/참고용입니다.', 22, 198);
      }
    }

    function drawLines() {
      background(255);
      stroke(0);
      strokeWeight(4);
      yLine1 = height / 2;
      yLine2 = yLine1 + lineSpacing;
      yCenterMin = yLine1;
      yCenterMax = yLine2;

      line(0, yLine1, width, yLine1);
      line(0, yLine2, width, yLine2);

      fill(0);
      textFont('Verdana');
      textStyle(NORMAL);
      textSize(20);
      text('n', 35, 75);
      text('d (20~200)', 160, 75);
      text('L (10~180)', 330, 75);
    }

    function dropNeedle() {
      let theta = random(PI);
      let yOffset = random(lineSpacing / 2);
      let hit = yOffset <= (needleLength / 2.0) * sin(theta);

      let xCenter = random(width);
      let yCenter = random(yCenterMin, yCenterMax);
      let dx = (needleLength / 2.0) * cos(theta);
      let dy = (needleLength / 2.0) * sin(theta);

      let x1 = xCenter - dx;
      let y1 = yCenter - dy;
      let x2 = xCenter + dx;
      let y2 = yCenter + dy;

      stroke(hit ? color(0, 150, 0) : color(150, 0, 0));
      strokeWeight(1);
      line(x1, y1, x2, y2);

      if (hit) hits++;
      currentNeedle++;
      numNeedles++;

      if (hits > 0) {
        let piEstimate = (2.0 * needleLength * numNeedles) / (hits * lineSpacing);
        piHistory.push(piEstimate);
      }
    }

    function startSimulation() {
      currentTarget = int(needleInput.value());
      lineSpacing = constrain(int(spacingInput.value()), 20, 200);
      needleLength = constrain(int(lengthInput.value()), 10, 180);
      currentNeedle = 0;
      simulationRunning = true;
    }

    function resetSim() {
      hits = 0;
      currentNeedle = 0;
      numNeedles = 0;
      piHistory = [];
      simulationRunning = false;
      autoRunning = false;
      redraw();
    }

    function showPi() {
      fill(0);
      textFont('Verdana');
      textStyle(NORMAL);
      textSize(18);
      if (hits > 0) {
        let piEstimate = (2.0 * needleLength * numNeedles) / (hits * lineSpacing);
        let mathProb = (2.0 * needleLength) / (PI * lineSpacing);
        let statProb = hits / numNeedles;
        text('(2 × L) / (π × d): ' + nf(mathProb, 1, 6), 20, 130);
        text('π ≈ ' + nf(piEstimate, 1, 6), width - 260, 130);
        text('statistical probability (' + hits + ' / ' + numNeedles + ') = ' + nf(statProb, 1, 6), 20, 160);
      }
    }

    function drawGraph() {
      if (piHistory.length < 2) return;
      fill(255);
      noStroke();
      let gx = width - 260, gy = 250, gw = 230, gh = 200;
      rect(gx, gy, gw, gh);
      noFill();
      stroke(0);
      strokeWeight(1);
      rect(gx, gy, gw, gh);
      line(gx, gy+gh, gx+gw, gy+gh);
      line(gx, gy, gx, gy+gh);

      stroke(200, 0, 0);
      strokeWeight(1);
      let yPi = map(PI, 2.5, 4.0, gy+gh, gy);
      line(gx, yPi, gx+gw, yPi);

      stroke(0, 100, 255);
      strokeWeight(1);
      beginShape();
      for (let i = 0; i < piHistory.length; i++) {
        let x = map(i, 0, piHistory.length, gx, gx+gw);
        let y = map(constrain(piHistory[i], 2.5, 4.0), 2.5, 4.0, gy+gh, gy);
        vertex(x, y);
      }
      endShape();

      fill(0);
      textFont('Verdana');
      textStyle(NORMAL);
      textSize(14);
      text('π', gx+gw-12, yPi - 4);
      text('Estimate', gx+6, gy-10);
      text('#', gx-14, gy+gh+6);
    }
    </script>
    '''

    components.html(html, height=580, scrolling=False)
