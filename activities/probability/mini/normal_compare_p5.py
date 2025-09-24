# activities/probability/mini/normal_compare_p5.py
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "정규분포 비교",
    "description": "평균(μ)과 표준편차(σ)를 조절하며 두 정규분포 곡선을 비교합니다.",
    "order": 50,
    "hidden": True,  # mini 폴더용: 사이드바 목록에서는 숨김
}

def render():
    st.subheader("정규분포 비교")
    st.caption("슬라이더로 μ, σ를 조절해 두 정규분포의 모양을 비교해 보세요.")

    components.html(
        """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
    <style>
      body{ margin:0; }
      #wrap{ max-width: 980px; margin: 0 auto; padding: 8px 12px 16px; }
      .row{ display:flex; gap:18px; flex-wrap:wrap; align-items: center; }
      .card{ border:1px solid #e5e7eb; border-radius:12px; padding:12px; }
      .col{ flex: 1 1 320px; }
      .sl{ display:flex; align-items:center; gap:10px; margin:6px 0; }
      .sl label{ width:70px; color:#111827; font: 600 13px/1.2 system-ui, -apple-system, Segoe UI, Roboto, Arial; }
      .sl output{ min-width:75px; text-align:right; color:#374151; }
      .title{ font:700 18px/1.2 system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 0 0 8px; }
      .cap{ color:#6b7280; font: 13px/1.35 system-ui, -apple-system, Segoe UI, Roboto, Arial; }
      canvas{ display:block; }
    </style>
  </head>
  <body>
    <div id="wrap">
      <div class="row">
        <div class="card col" id="panel-left">
          <div class="title">분포 ① (파랑)</div>
          <div class="sl"><label>μ₁</label><input id="mu1" type="range" min="-5" max="5" step="0.1" value="0"><output id="omu1">0.0</output></div>
          <div class="sl"><label>σ₁</label><input id="sg1" type="range" min="0.2" max="3" step="0.05" value="1"><output id="osg1">1.00</output></div>
          <div class="cap">파란 곡선은 평균과 표준편차를 위 슬라이더로 조절합니다.</div>
        </div>

        <div class="card col" id="panel-right">
          <div class="title">분포 ② (주황)</div>
          <div class="sl"><label>μ₂</label><input id="mu2" type="range" min="-5" max="5" step="0.1" value="1.5"><output id="omu2">1.5</output></div>
          <div class="sl"><label>σ₂</label><input id="sg2" type="range" min="0.2" max="3" step="0.05" value="0.7"><output id="osg2">0.70</output></div>
          <div class="cap">주황 곡선도 동일하게 조절할 수 있습니다.</div>
        </div>
      </div>

      <div class="card" style="margin-top:12px;">
        <div class="title">그래프</div>
        <div id="sketch"></div>
        <div class="cap">축 범위: x ∈ [-10, 10]. 범례는 현재 설정된 (μ, σ)를 표시합니다.</div>
      </div>
    </div>

    <script>
      const blue   = "#2563eb";  // indigo-600
      const orange = "#f97316";  // orange-500
      const grid   = "#e5e7eb";  // gray-200
      const axis   = "#374151";  // gray-700

      const P = {
        mu1: 0.0,  sigma1: 1.00,
        mu2: 1.5,  sigma2: 0.70,
        xmin: -10, xmax: 10
      };

      let p;            // p5 인스턴스
      let cnvW = 940;   // 캔버스 너비
      let cnvH = 420;   // 캔버스 높이
      const margin = {l: 56, r: 20, t: 36, b: 44};

      function normalPDF(x, mu, sigma){
        const a = 1.0 / (sigma * Math.sqrt(2*Math.PI));
        const z = (x - mu)/sigma;
        return a * Math.exp(-0.5 * z * z);
      }

      function setupUI(){
        const dom = (id) => document.getElementById(id);
        const upd = () => { p.redraw(); };

        const mu1 = dom("mu1"), sg1 = dom("sg1");
        const mu2 = dom("mu2"), sg2 = dom("sg2");
        const omu1 = dom("omu1"), osg1 = dom("osg1");
        const omu2 = dom("omu2"), osg2 = dom("osg2");

        const sync = () => {
          P.mu1 = parseFloat(mu1.value);    omu1.textContent = P.mu1.toFixed(1);
          P.sigma1 = parseFloat(sg1.value); osg1.textContent = P.sigma1.toFixed(2);
          P.mu2 = parseFloat(mu2.value);    omu2.textContent = P.mu2.toFixed(1);
          P.sigma2 = parseFloat(sg2.value); osg2.textContent = P.sigma2.toFixed(2);
          upd();
        };

        [mu1, sg1, mu2, sg2].forEach(el => {
          el.addEventListener("input", sync);
          el.addEventListener("change", sync);
        });
        sync();
      }

      function sketch(_p){
        p = _p;
        p.setup = function(){
          const holder = document.getElementById("sketch");
          const W = Math.min(holder.clientWidth || cnvW, cnvW);
          const H = cnvH;
          const c = p.createCanvas(W, H);
          c.parent("sketch");
          p.noLoop();
          setupUI();
        };

        p.windowResized = function(){
          const holder = document.getElementById("sketch");
          const W = Math.min(holder.clientWidth || cnvW, cnvW);
          p.resizeCanvas(W, cnvH);
          p.redraw();
        };

        function x2px(x){
          const L = margin.l, R = p.width - margin.r;
          return p.map(x, P.xmin, P.xmax, L, R, true);
        }
        function y2px(y){ // y ≥ 0
          const T = margin.t, B = p.height - margin.b;
          // y-축은 위가 0, 아래가 최대치가 되도록 반전
          // 표시용 최대 y는 두 분포의 최대치 중 큰 값에 약간 마진을 더함
          const ymax = getYMax() * 1.12;
          return p.map(y, 0, ymax, B, T, true);
        }

        function getYMax(){
          // 두 분포의 정점은 각각 x = μ에서 f(μ) = 1/(σ√(2π))
          const m1 = 1.0 / (P.sigma1 * Math.sqrt(2*Math.PI));
          const m2 = 1.0 / (P.sigma2 * Math.sqrt(2*Math.PI));
          return Math.max(m1, m2);
        }

        function drawGridAndAxes(){
          p.background(255);
          const L = margin.l, R = p.width - margin.r;
          const T = margin.t, B = p.height - margin.b;

          // grid x
          p.stroke(grid); p.strokeWeight(1);
          const ticks = [];
          for(let t=-10; t<=10; t+=2){ ticks.push(t); }
          for(const t of ticks){
            const xx = x2px(t);
            p.line(xx, T, xx, B);
          }
          // grid y (4등분)
          const ymax = getYMax()*1.12;
          for(let k=1;k<=4;k++){
            const yv = ymax * k/4;
            const yy = y2px(yv);
            p.line(L, yy, R, yy);
          }

          // axes
          p.stroke(axis); p.strokeWeight(1.2);
          p.line(L, B, R, B);     // x-axis
          p.line(L, B, L, T);     // y-axis

          // x ticks & labels
          p.fill(axis); p.noStroke(); p.textAlign(p.CENTER, p.TOP);
          p.textSize(12);
          for(const t of ticks){
            const xx = x2px(t);
            p.stroke(axis);
            p.line(xx, B, xx, B+4);
            p.noStroke();
            p.text(t.toString(), xx, B+6);
          }

          // y ticks & labels
          p.textAlign(p.RIGHT, p.CENTER);
          for(let k=1;k<=4;k++){
            const yv = ymax * k/4;
            const yy = y2px(yv);
            p.stroke(axis); p.line(L-4, yy, L, yy);
            p.noStroke(); p.text(yv.toFixed(2), L-8, yy);
          }

          // legend (수정된 버전)
          drawLegend();
        }

        function drawLegend(){
          const Lx = margin.l;
          const Ly = margin.t - 2;

          const s1 = `μ₁=${P.mu1.toFixed(2)}, σ₁=${P.sigma1.toFixed(2)}`;
          const s2 = `μ₂=${P.mu2.toFixed(2)}, σ₂=${P.sigma2.toFixed(2)}`;

          p.textSize(12);
          p.noStroke();
          p.fill(0);
          p.textAlign(p.LEFT, p.BOTTOM);

          // blue
          p.stroke(blue);
          p.strokeWeight(3);
          p.line(Lx, Ly-6, Lx+18, Ly-6);
          p.noStroke(); p.fill(0);
          p.text(`  ${s1}`, Lx+22, Ly);

          // orange
          const offsetX = 210;
          p.stroke(orange);
          p.strokeWeight(3);
          p.line(Lx+offsetX, Ly-6, Lx+offsetX+18, Ly-6);
          p.noStroke(); p.fill(0);
          p.text(`  ${s2}`, Lx+offsetX+22, Ly);
        }

        function drawCurve(colorHex, mu, sigma){
          p.noFill();
          p.stroke(colorHex);
          p.strokeWeight(2);

          const L = margin.l, R = p.width - margin.r;
          const step = Math.max(1, Math.floor((R-L)/400)); // 해상도 조절
          let first = true;

          for(let px=L; px<=R; px+=step){
            const x = p.map(px, L, R, P.xmin, P.xmax);
            const y = normalPDF(x, mu, sigma);
            const py = y2px(y);
            if(first){ p.beginShape(); first=false; }
            p.vertex(px, py);
          }
          p.endShape();
        }

        p.draw = function(){
          drawGridAndAxes();
          drawCurve(blue,   P.mu1, P.sigma1);
          drawCurve(orange, P.mu2, P.sigma2);
        };
      }

      new p5(sketch);
    </script>
  </body>
</html>
        """,
        height=660,
    )
