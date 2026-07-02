# -*- coding: utf-8 -*-
import json

with open("D:\\Uni\\hoc\\quiz_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

questions_json = json.dumps(data["questions"], ensure_ascii=False)
dist_json = json.dumps(data["distribution"], ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quiz SQA - 50 Cau</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',Tahoma,sans-serif;background:#f0f4f8;color:#333;min-height:100vh;display:flex;justify-content:center;padding:20px}
.container{max-width:800px;width:100%}
h1{text-align:center;color:#1a56db;margin:20px 0;font-size:1.5em}
#info{text-align:center;color:#666;margin-bottom:20px;font-size:0.9em}
#startScreen,#resultScreen{text-align:center;background:white;border-radius:12px;padding:40px 30px;box-shadow:0 2px 12px rgba(0,0,0,0.08);margin-top:40px}
#startScreen h2,#resultScreen h2{margin-bottom:15px;color:#1a56db}
#startScreen p{margin-bottom:25px;color:#666;line-height:1.6}
.btn{background:#1a56db;color:white;border:none;padding:12px 32px;border-radius:8px;font-size:1em;cursor:pointer;transition:background .2s}
.btn:hover{background:#1648c0}
.btn:disabled{background:#94a3b8;cursor:not-allowed}
#quizArea{display:none}
#progress{display:flex;align-items:center;gap:12px;margin-bottom:15px;flex-wrap:wrap}
#progressBar{flex:1;height:8px;background:#e2e8f0;border-radius:4px;overflow:hidden;min-width:100px}
#progressFill{height:100%;background:#1a56db;border-radius:4px;transition:width .3s}
#qCounter{font-size:.85em;color:#666;white-space:nowrap}
#card{background:white;border-radius:12px;padding:25px;box-shadow:0 2px 12px rgba(0,0,0,0.08)}
#qBadge{display:inline-block;background:#e8f0fe;color:#1a56db;padding:4px 12px;border-radius:12px;font-size:.8em;margin-bottom:12px}
#qText{font-size:1.05em;line-height:1.6;margin-bottom:20px}
.opt{display:block;width:100%;text-align:left;padding:12px 16px;margin:6px 0;border:2px solid #e2e8f0;border-radius:8px;background:white;cursor:pointer;font-size:.95em;transition:all .15s}
.opt:hover:not(.disabled){border-color:#93c5fd;background:#f0f7ff}
.opt.selected{border-color:#1a56db;background:#e8f0fe}
.opt.correct{border-color:#16a34a;background:#dcfce7}
.opt.wrong{border-color:#dc2626;background:#fee2e2}
.opt.disabled{cursor:default;opacity:.85}
#nav{display:flex;justify-content:space-between;align-items:center;margin-top:20px;gap:10px}
#nav .btn{padding:10px 24px;font-size:.9em}
#qDots{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:15px}
.dot{width:22px;height:22px;border-radius:50%;border:2px solid #cbd5e1;background:white;cursor:pointer;font-size:.65em;display:flex;align-items:center;justify-content:center;transition:all .15s}
.dot.answered{border-color:#1a56db;background:#dbeafe}
.dot.correct{border-color:#16a34a;background:#bbf7d0}
.dot.wrong{border-color:#dc2626;background:#fecaca}
.dot.current{border-width:3px;border-color:#1a56db;transform:scale(1.1)}
#resultScreen{display:none}
.score{font-size:2.5em;font-weight:bold;color:#1a56db;margin:15px 0}
.score-detail{color:#666;margin-bottom:20px;line-height:1.6}
#reviewList{text-align:left;margin-top:20px;max-height:400px;overflow-y:auto}
.reviewItem{padding:12px;border-bottom:1px solid #e2e8f0}
.reviewItem:last-child{border-bottom:none}
.reviewItem .rq{font-weight:600;margin-bottom:4px}
.reviewItem .ra{font-size:.9em;color:#666}
.reviewItem .ra.c{color:#16a34a}
.reviewItem .ra.w{color:#dc2626}
@media(max-width:600px){
body{padding:10px}
#card{padding:16px}
.opt{padding:10px 12px;font-size:.9em}
#qDots{gap:3px}
.dot{width:18px;height:18px;font-size:.55em}
}
</style>
</head>
<body>
<div class="container">
<h1>&#x1F4DA; Quiz SQA - 50 C&#x00E2;u</h1>
<div id="info">Ch&#x1ECD;n ng&#x1EAB;u nhi&#xEA;n: G1(10)+G2(15)+G3(3)+G4(5)+G5(12)+G6(5)</div>

<div id="startScreen">
  <h2>&#x1F3AF; B&#x1EAF;t &#x111;&#x1EA7;u l&#xE0;m b&#xE0;i</h2>
  <p>50 c&#x00E2;u tr&#x1EAF;c nghi&#x1EC7;m ng&#x1EAB;u nhi&#xEA;n<br>t&#x1EEB; ng&#x00E2;n h&#xE0;ng c&#x00E2;u h&#x1ECF;i SQA.</p>
  <button class="btn" onclick="startQuiz()">&#x25B6; L&#xE0;m b&#xE0;i ngay</button>
</div>

<div id="quizArea">
  <div id="qDots"></div>
  <div id="progress">
    <span id="qCounter">1 / 50</span>
    <div id="progressBar"><div id="progressFill"></div></div>
  </div>
  <div id="card">
    <div id="qBadge"></div>
    <div id="qText"></div>
    <div id="options"></div>
    <div id="nav">
      <button class="btn" id="prevBtn" onclick="prevQ()">&#x25C0; Tr&#x1B0;&#x1EDB;c</button>
      <button class="btn" id="nextBtn" onclick="nextQ()">Sau &#x25B6;</button>
    </div>
  </div>
</div>

<div id="resultScreen">
  <h2>&#x1F3C6; K&#x1EBF;t qu&#x1EA3;</h2>
  <div class="score" id="scoreDisplay">0/50</div>
  <div class="score-detail" id="scoreDetail"></div>
  <button class="btn" onclick="startQuiz()">&#x1F504; L&#xE0;m l&#x1EA1;i</button>
  <div id="reviewList"></div>
</div>
</div>

<script>
var ALL_QUESTIONS = """ + questions_json + """;
var DIST = """ + dist_json + """;

var quiz = [];
var answers = [];
var currentIdx = 0;

function shuffle(arr) {
  for (var i = arr.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
  return arr;
}

function pickQuestions() {
  var grouped = {};
  for (var qi = 0; qi < ALL_QUESTIONS.length; qi++) {
    var q = ALL_QUESTIONS[qi];
    if (!grouped[q.group]) grouped[q.group] = [];
    grouped[q.group].push(q);
  }
  var selected = [];
  for (var g in DIST) {
    var pool = grouped[g] || [];
    shuffle(pool);
    var need = DIST[g];
    for (var i = 0; i < Math.min(need, pool.length); i++) {
      selected.push(pool[i]);
    }
  }
  shuffle(selected);
  return selected;
}

function startQuiz() {
  quiz = pickQuestions();
  answers = [];
  for (var i = 0; i < quiz.length; i++) answers.push(-1);
  currentIdx = 0;
  document.getElementById('startScreen').style.display = 'none';
  document.getElementById('resultScreen').style.display = 'none';
  document.getElementById('quizArea').style.display = 'block';
  renderDots();
  renderQ();
}

function renderDots() {
  var container = document.getElementById('qDots');
  container.innerHTML = '';
  for (var i = 0; i < quiz.length; i++) {
    var dot = document.createElement('div');
    dot.className = 'dot' + (i === currentIdx ? ' current' : '');
    if (answers[i] >= 0) dot.classList.add('answered');
    dot.textContent = i + 1;
    dot.onclick = (function(idx) { return function() { goToQ(idx); }; })(i);
    container.appendChild(dot);
  }
}

function updateDots() {
  var dots = document.querySelectorAll('.dot');
  for (var i = 0; i < dots.length; i++) {
    var dot = dots[i];
    dot.className = 'dot';
    if (answers[i] >= 0) dot.classList.add('answered');
    if (i === currentIdx) dot.classList.add('current');
  }
}

function renderQ() {
  var q = quiz[currentIdx];
  if (!q) return;
  
  document.getElementById('qBadge').textContent = 'Cau ' + q.id + ' | Nhom ' + q.group + ' | ' + q.diff;
  document.getElementById('qText').textContent = q.text;
  document.getElementById('qCounter').textContent = (currentIdx + 1) + ' / ' + quiz.length;
  document.getElementById('progressFill').style.width = ((currentIdx + 1) / quiz.length * 100) + '%';
  
  var container = document.getElementById('options');
  container.innerHTML = '';
  
  var selected = answers[currentIdx];
  for (var i = 0; i < q.opts.length; i++) {
    var btn = document.createElement('button');
    btn.className = 'opt';
    if (selected >= 0) {
      btn.classList.add('disabled');
      if (i === q.answer) btn.classList.add('correct');
      if (i === selected && i !== q.answer) btn.classList.add('wrong');
    } else {
      btn.onclick = (function(idx) { return function() { selectOpt(idx); }; })(i);
    }
    btn.textContent = (i + 1) + '. ' + q.opts[i];
    container.appendChild(btn);
  }
  
  document.getElementById('prevBtn').disabled = currentIdx === 0;
  document.getElementById('nextBtn').textContent = currentIdx === quiz.length - 1 ? 'Xem ket qua \u25B6' : 'Sau \u25B6';
  updateDots();
}

function selectOpt(i) {
  if (answers[currentIdx] >= 0) return;
  answers[currentIdx] = i;
  renderQ();
}

function nextQ() {
  if (currentIdx < quiz.length - 1) {
    currentIdx++;
    renderQ();
  } else {
    showResult();
  }
}

function prevQ() {
  if (currentIdx > 0) {
    currentIdx--;
    renderQ();
  }
}

function goToQ(i) {
  if (i >= 0 && i < quiz.length) {
    currentIdx = i;
    renderQ();
  }
}

function showResult() {
  document.getElementById('quizArea').style.display = 'none';
  document.getElementById('resultScreen').style.display = 'block';
  
  var correct = 0;
  var details = [];
  
  for (var i = 0; i < quiz.length; i++) {
    var q = quiz[i];
    var isCorrect = answers[i] === q.answer;
    if (isCorrect) correct++;
    details.push({
      id: q.id,
      text: q.text,
      userAns: answers[i],
      correctAns: q.answer,
      isCorrect: isCorrect,
      opts: q.opts
    });
  }
  
  document.getElementById('scoreDisplay').textContent = correct + ' / ' + quiz.length;
  var pct = Math.round(correct / quiz.length * 100);
  document.getElementById('scoreDetail').textContent = 'Ti le dung: ' + pct + '%';
  
  var list = document.getElementById('reviewList');
  list.innerHTML = '<h3 style="margin:20px 0 10px">Chi tiet cau hoi:</h3>';
  
  for (var i = 0; i < details.length; i++) {
    var d = details[i];
    var div = document.createElement('div');
    div.className = 'reviewItem';
    var status = d.isCorrect ? '\u2705' : '\u274C';
    var userText = d.userAns >= 0 ? d.opts[d.userAns] : '(chua tra loi)';
    div.innerHTML = '<div class="rq">' + status + ' Cau ' + d.id + ': ' + d.text + '</div>' +
      '<div class="ra ' + (d.isCorrect ? 'c' : 'w') + '">Dap an cua ban: ' + userText + '</div>' +
      (!d.isCorrect ? '<div class="ra c">Dap an dung: ' + d.opts[d.correctAns] + '</div>' : '');
    list.appendChild(div);
  }
}

document.getElementById('prevBtn').disabled = true;
</script>
</body>
</html>"""

with open("D:\\Uni\\hoc\\quiz.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done! quiz.html created")
