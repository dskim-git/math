# activities/probability/monty_hall_extended_p5.py
from pathlib import Path
import base64
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "몬티홀 문제(확장)",
    "description": "문과 자동차의 개수를 바꿔가며 '유지/교체' 전략을 실험해 보세요.",
    "order": 121,
}

def _img_to_data_uri(path: Path) -> str:
    """로컬 이미지를 data URI(base64)로 변환 (없으면 빈 문자열)"""
    if not path.exists():
        return ""
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"

def render():
    st.subheader("확장된 몬티홀 시뮬레이터")
    st.caption("문/자동차 수를 조절하고, 공개 후 유지/교체 전략의 승률을 비교합니다.")

    # 이미지 경로 (확률과통계 과목 아래 자산 폴더)
    here = Path(__file__).parent
    goat_uri = _img_to_data_uri(here / "monty_hall_assets" / "goat.png")
    car_uri  = _img_to_data_uri(here / "monty_hall_assets" / "car.png")
    if not goat_uri or not car_uri:
        st.warning("⚠️ 이미지가 없습니다. `activities/probability/monty_hall_assets/` 폴더에 goat.png, car.png 를 넣어주세요.")

    # f-string의 중괄호 충돌을 피하려고 플레이스홀더 방식 사용
    html_template = r"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
  <style>
    html,body { margin:0; padding:0; overflow:hidden; font-family:sans-serif; }
  </style>
</head>
<body>
<script>
let goatImg, carImg;

let chosenDoor = -1;
let carDoors = [];
let revealed = false;
let revealedDoor = -1;
let decisionMade = false;
let playerSwitched = false;
let showResult = false;

let switchWins = 0;
let stayWins = 0;
let simulations = 0;
let showStats = false;
let lastSim = "";

let isAutoPlay = false;
let autoSwitch = true;
let autoInterval = 30;
let autoTimer = 0;
let autoCount = 0;
let autoMax = 100;
let autoWinCount = 0;
let autoLossCount = 0;

let BUTTON_HEIGHT = 40;
let CANVAS_WIDTH = 1200;
let CANVAS_HEIGHT = 820; // 하단 텍스트 여유

let selectedSimCount = 0;
let strategySelection = false;

let doorOpenProgress = [];
let doorRevealed = [];

let numDoors = 3;
let numCars = 1;

function preload() {
  // 로컬 파일 대신 data URI 사용
  const goatURI = "__GOAT__";
  const carURI  = "__CAR__";
  if (goatURI) goatImg = loadImage(goatURI);
  if (carURI)  carImg  = loadImage(carURI);
}

function setup() {
  createCanvas(CANVAS_WIDTH, CANVAS_HEIGHT);
  textFont("sans-serif", 24);
  resetGame();
}

function drawSliders() {
  fill(0);
  textSize(16);
  textAlign(LEFT, CENTER);
  text("Number of Doors: " + numDoors, 100, 670);
  text("Number of Cars: " + numCars, 600, 670);

  fill(200);
  rect(100, 690, 200, 20);
  rect(600, 690, 200, 20);

  let doorPos = map(numDoors, 3, 10, 100, 300);
  let carPos = map(numCars, 1, numDoors - 1, 600, 800);

  fill(50);
  ellipse(doorPos, 700, 20, 20);
  ellipse(carPos, 700, 20, 20);
}

function draw() {
  background(255);
  textAlign(CENTER, CENTER);
  textSize(24);

  drawButton(width / 2 - 250, 30, "Reset");
  drawButton(width / 2 + 50, 30, isAutoPlay ? "Stop Auto" : "Auto Play");

  drawSimulationButtons();
  drawSliders();

  let startX = (width - (numDoors * 100 + (numDoors - 1) * 20)) / 2;
  for (let i = 0; i < numDoors; i++) {
    let x = startX + i * 120;
    fill(i === chosenDoor ? color(180, 220, 255) : 240);
    rect(x, 200, 100, 200, 20);
    fill(0);
    text("Door " + (i + 1), x +28, 420);

    if (doorRevealed[i]) {
      doorOpenProgress[i] = min(1, doorOpenProgress[i] + 0.05);
      let img = carDoors.includes(i) ? carImg : goatImg;
      if (img) {
        imageMode(CENTER);
        image(img, x + 50, 300, 100 * doorOpenProgress[i], 100 * doorOpenProgress[i]);
      }
    }
  }

  if (showResult) {
    fill(0);
    textSize(32);
    text(carDoors.includes(chosenDoor) ? "🎉 You won a Car!" : "🐐 You got a Goat!", width / 3, 460);
    textSize(24);
  }

  if (revealed && !decisionMade && !isAutoPlay) {
    fill(200);
    rect(width / 2 - 200, 500, 150, 50);
    rect(width / 2 + 50, 500, 150, 50);
    fill(0);
    text("Stay", width / 2 - 140, 525);
    text("Switch", width / 2 + 105, 525);
  }

  if (showStats) {
    fill(0);
    text("Simulation (" + lastSim + "):", width / 3, 550);
    let wins = lastSim.includes("Switch") ? switchWins : stayWins;
    let winRate = (wins / simulations) * 100;
    text("Wins: " + wins + " / " + simulations + " (" + winRate.toFixed(2) + "%)", width / 3, 580);
  }

  if (autoCount > 0) {
    fill(0);
    textSize(20);
    let currentRate = autoWinCount / autoCount * 100;
    text("AutoPlay: " + autoCount + " games", width / 3, 610);
    text("Wins: " + autoWinCount + " / Losses: " + autoLossCount + " (" + currentRate.toFixed(2) + "%)", width / 3, 635);
  }

  if (isAutoPlay) {
    autoTimer++;
    if (autoTimer >= autoInterval) {
      autoTimer = 0;
      playOneAutoGame(autoSwitch);
    }
  }
}

function drawButton(x, y, label) {
  fill(180);
  rect(x, y, 200, BUTTON_HEIGHT);
  fill(0);
  textSize(18);
  text(label, x + 100, y + BUTTON_HEIGHT / 2);
}

function drawSimulationButtons() {
  fill(200);
  rect(100, 90, 100, 40);
  rect(220, 90, 100, 40);
  rect(340, 90, 100, 40);
  rect(460, 90, 140, 40);
  fill(0);
  text("10", 150, 110);
  text("100", 270, 110);
  text("1000", 390, 110);
  text("10000", 530, 110);

  if (strategySelection) {
    fill(180);
    rect(620, 90, 80, 40);
    rect(720, 90, 80, 40);
    fill(0);
    text("Stay", 660, 110);
    text("Switch", 760, 110);
  }
}

function resetGame() {
  chosenDoor = -1;
  revealed = false;
  revealedDoor = -1;
  decisionMade = false;
  playerSwitched = false;
  showResult = false;
  showStats = false;
  selectedSimCount = 0;
  strategySelection = false;
  autoTimer = 0;
  doorOpenProgress = new Array(numDoors).fill(0);
  doorRevealed = new Array(numDoors).fill(false);

  carDoors = [];
  while (carDoors.length < numCars) {
    let newCar = int(random(numDoors));
    if (!carDoors.includes(newCar)) {
      carDoors.push(newCar);
    }
  }
}

function mousePressed() {
  if (mouseY > 690 && mouseY < 710) {
    if (mouseX > 100 && mouseX < 300) {
      numDoors = constrain(round(map(mouseX, 100, 300, 3, 10)), 3, 10);
      numCars = min(numCars, numDoors - 1);
      resetGame();
      return;
    } else if (mouseX > 600 && mouseX < 800) {
      numCars = constrain(round(map(mouseX, 600, 800, 1, numDoors - 1)), 1, numDoors - 1);
      resetGame();
      return;
    }
  }

  if (mouseY > 30 && mouseY < 70) {
    if (mouseX > width / 2 - 250 && mouseX < width / 2 - 50) {
      resetGame();
      return;
    } else if (mouseX > width / 2 + 50 && mouseX < width / 2 + 250) {
      isAutoPlay = !isAutoPlay;
      if (isAutoPlay) {
        autoCount = 0;
        autoWinCount = 0;
        autoLossCount = 0;
        autoTimer = 0;
        autoSwitch = true;
        showStats = false;
        resetGame();
      }
      return;
    }
  }

  if (!strategySelection && mouseY > 90 && mouseY < 130) {
    if (mouseX > 100 && mouseX < 200) selectedSimCount = 10;
    else if (mouseX > 220 && mouseX < 320) selectedSimCount = 100;
    else if (mouseX > 340 && mouseX < 440) selectedSimCount = 1000;
    else if (mouseX > 460 && mouseX < 600) selectedSimCount = 10000;
    if (selectedSimCount > 0) strategySelection = true;
    return;
  }

  if (strategySelection && mouseY > 90 && mouseY < 130) {
    if (mouseX > 620 && mouseX < 700) {
      simulateGames(selectedSimCount, false);
      strategySelection = false;
      selectedSimCount = 0;
      return;
    } else if (mouseX > 720 && mouseX < 800) {
      simulateGames(selectedSimCount, true);
      strategySelection = false;
      selectedSimCount = 0;
      return;
    }
  }

  if (chosenDoor === -1 && !isAutoPlay) {
    let startX = (width - (numDoors * 100 + (numDoors - 1) * 20)) / 2;
    for (let i = 0; i < numDoors; i++) {
      let x = startX + i * 120;
      if (mouseX > x && mouseX < x + 100 && mouseY > 200 && mouseY < 400) {
        chosenDoor = i;
        revealGoatDoor();
      }
    }
  }

  if (revealed && !decisionMade && !isAutoPlay) {
    if (mouseX > width / 2 - 200 && mouseX < width / 2 - 50 && mouseY > 500 && mouseY < 550) {
      decisionMade = true;
      playerSwitched = false;
      showResult = true;
      revealAllDoors();
    } else if (mouseX > width / 2 + 50 && mouseX < width / 2 + 200 && mouseY > 500 && mouseY < 550) {
      decisionMade = true;
      playerSwitched = true;
      let candidates = [];
      for (let i = 0; i < numDoors; i++) {
        if (i !== chosenDoor && i !== revealedDoor) {
          candidates.push(i);
        }
      }
      chosenDoor = int(random(candidates));
      showResult = true;
      revealAllDoors();
    }
  }
}

function revealGoatDoor() {
  revealed = true;
  for (let i = 0; i < numDoors; i++) {
    if (!carDoors.includes(i) && i !== chosenDoor) {
      revealedDoor = i;
      doorRevealed[i] = true;
      break;
    }
  }
}

function revealAllDoors() {
  for (let i = 0; i < numDoors; i++) {
    doorRevealed[i] = true;
  }
}

function simulateGames(trials, switchMode) {
  let wins = 0;
  for (let i = 0; i < trials; i++) {
    let carSet = [];
    while (carSet.length < numCars) {
      let candidate = int(random(numDoors));
      if (!carSet.includes(candidate)) carSet.push(candidate);
    }
    let choice = int(random(numDoors));
    let reveal = -1;
    for (let i2 = 0; i2 < numDoors; i2++) {
      if (!carSet.includes(i2) && i2 !== choice) {
        reveal = i2;
        break;
      }
    }
    if (switchMode) {
      let candidates = [];
      for (let i3 = 0; i3 < numDoors; i3++) {
        if (i3 !== choice && i3 !== reveal) {
          candidates.push(i3);
        }
      }
      choice = int(random(candidates));
    }
    let win = carSet.includes(choice);
    if (win) wins++;
  }
  if (switchMode) {
    switchWins = wins;
    lastSim = "Switch";
  } else {
    stayWins = wins;
    lastSim = "Stay";
  }
  simulations = trials;
  showStats = true;
}

function playOneAutoGame(switchMode) {
  resetGame();
  let choice = int(random(numDoors));
  let reveal = -1;
  for (let i = 0; i < numDoors; i++) {
    if (!carDoors.includes(i) && i !== choice) {
      reveal = i;
      break;
    }
  }
  if (switchMode) {
    let candidates = [];
    for (let i = 0; i < numDoors; i++) {
      if (i !== choice && i !== reveal) {
        candidates.push(i);
      }
    }
    choice = int(random(candidates));
  }
  let win = carDoors.includes(choice);
  if (win) autoWinCount++; else autoLossCount++;
  autoCount++;
  chosenDoor = choice;
  revealedDoor = reveal;
  revealed = true;
  decisionMade = true;
  playerSwitched = switchMode;
  showResult = true;
  revealAllDoors();
  if (autoCount >= autoMax) {
    isAutoPlay = false;
    simulations = autoMax;
    lastSim = switchMode ? "Switch (Auto)" : "Stay (Auto)";
    switchWins = switchMode ? autoWinCount : 0;
    stayWins = switchMode ? 0 : autoWinCount;
    showStats = true;
  }
}
</script>
</body>
</html>
    """

    html = html_template.replace("__GOAT__", goat_uri).replace("__CAR__", car_uri)
    components.html(html, height=880, scrolling=False)
