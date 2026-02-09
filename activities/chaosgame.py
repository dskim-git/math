import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="Chaos Game Puzzle", layout="centered")

st.title("🎮 The Chaos Game (BU Edition)")
st.markdown("""
이 게임은 보스턴 대학교(BU)의 카오스 게임을 재현한 것입니다.  
**목표:** 현재 점을 꼭짓점 버튼을 눌러 이동시켜 초록색 타겟 영역 안에 넣으세요!
""")

# 앞서 만든 HTML/JS 코드를 변수에 담습니다.
chaos_game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body { background-color: #f0f0f0; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; overflow: hidden; }
        .container { background: white; padding: 20px; border-radius: 15px; text-align: center; width: 100%; }
        canvas { border: 1px solid #ccc; background-color: #fff; max-width: 100%; height: auto; }
        .controls, .vertex-btns { display: flex; gap: 10px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
        button { padding: 10px 15px; cursor: pointer; border: none; border-radius: 5px; background: #4a90e2; color: white; font-weight: bold; }
        button.red { background: #e74c3c; }
        button.blue { background: #3498db; }
        button.green { background: #2ecc71; }
        .score-board { display: flex; gap: 30px; font-size: 1.1em; font-weight: bold; justify-content: center; }
        .status { color: #e67e22; height: 24px; margin: 10px 0; font-weight: bold; }
    </style>
</head>
<body>
<div class="container">
    <div class="controls">
        <button onclick="setDifficulty(2)">Easy</button>
        <button onclick="setDifficulty(3)">Medium</button>
        <button onclick="setDifficulty(4)">Hard</button>
    </div>
    <div class="score-board">
        <div>Score: <span id="currentScore">0</span></div>
        <div>Target Step: <span id="bestScore">4</span></div>
    </div>
    <canvas id="gameCanvas" width="500" height="420"></canvas>
    <div class="vertex-btns">
        <button class="red" onclick="move(0)">Red</button>
        <button class="blue" onclick="move(1)">Blue</button>
        <button class="green" onclick="move(2)">Green</button>
    </div>
    <div class="status" id="statusMsg"></div>
    <button onclick="initGame()" style="background: #34495e;">Restart</button>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    let level = 2;
    const vertices = [{x: 250, y: 40, color: '#e74c3c'}, {x: 50, y: 380, color: '#3498db'}, {x: 450, y: 380, color: '#2ecc71'}];
    let currentPos = {x: 450, y: 380}, targetTriangle = [], score = 0, gameOver = false;

    function getTriangles(v1, v2, v3, depth) {
        if (depth === 0) return [[v1, v2, v3]];
        let m1 = {x: (v1.x + v2.x)/2, y: (v1.y + v2.y)/2}, m2 = {x: (v2.x + v3.x)/2, y: (v2.y + v3.y)/2}, m3 = {x: (v3.x + v1.x)/2, y: (v3.y + v1.y)/2};
        return [...getTriangles(v1, m1, m3, depth-1), ...getTriangles(m1, v2, m2, depth-1), ...getTriangles(m3, m2, v3, depth-1)];
    }

    function initGame() {
        score = 0; gameOver = false;
        document.getElementById('currentScore').innerText = score;
        document.getElementById('statusMsg').innerText = "";
        let allTriangles = getTriangles(vertices[0], vertices[1], vertices[2], level);
        targetTriangle = allTriangles[Math.floor(Math.random() * allTriangles.length)];
        currentPos = {x: vertices[2].x, y: vertices[2].y};
        draw();
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#2ecc71'; ctx.globalAlpha = 0.5;
        ctx.beginPath(); ctx.moveTo(targetTriangle[0].x, targetTriangle[0].y); ctx.lineTo(targetTriangle[1].x, targetTriangle[1].y); ctx.lineTo(targetTriangle[2].x, targetTriangle[2].y); ctx.fill();
        ctx.globalAlpha = 1.0;
        vertices.forEach(v => { ctx.fillStyle = v.color; ctx.beginPath(); ctx.arc(v.x, v.y, 8, 0, Math.PI*2); ctx.fill(); });
        ctx.fillStyle = 'black'; ctx.beginPath(); ctx.arc(currentPos.x, currentPos.y, 5, 0, Math.PI*2); ctx.fill();
    }

    function move(vIdx) {
        if (gameOver) return;
        currentPos.x = (currentPos.x + vertices[vIdx].x) / 2;
        currentPos.y = (currentPos.y + vertices[vIdx].y) / 2;
        score++; document.getElementById('currentScore').innerText = score;
        draw();
        if (isInside(currentPos, targetTriangle)) {
            document.getElementById('statusMsg').innerText = "🎉 Success!";
            gameOver = true;
        }
    }

    function isInside(p, tri) {
        let [p0, p1, p2] = tri;
        let A = 0.5 * (-p1.y * p2.x + p0.y * (-p1.x + p2.x) + p0.x * (p1.y - p2.y) + p1.x * p2.y);
        let s = (p0.y * p2.x - p0.x * p2.y + (p2.y - p0.y) * p.x + (p0.x - p2.x) * p.y) * (A < 0 ? -1 : 1);
        let t = (p0.x * p1.y - p0.y * p1.x + (p0.y - p1.y) * p.x + (p1.x - p0.x) * p.y) * (A < 0 ? -1 : 1);
        return s > 0 && t > 0 && (s + t) < 2 * Math.abs(A);
    }

    function setDifficulty(l) { level = l; document.getElementById('bestScore').innerText = l + 2; initGame(); }
    initGame();
</script>
</body>
</html>
"""

# 스트림릿 컴포넌트로 HTML 삽입
components.html(chaos_game_html, height=650)
