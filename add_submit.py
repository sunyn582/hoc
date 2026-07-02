with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_nav = '''    <div id="nav">
      <button class="btn" id="prevBtn" onclick="prevQ()">◀ Trước</button>
      <button class="btn" id="nextBtn" onclick="nextQ()">Sau ▶</button>
    </div>'''

new_nav = '''    <div id="nav">
      <button class="btn" id="prevBtn" onclick="prevQ()">◀ Trước</button>
      <button class="btn" id="submitBtn" onclick="submitQuiz()" style="background:#dc2626">📝 Nộp bài</button>
      <button class="btn" id="nextBtn" onclick="nextQ()">Sau ▶</button>
    </div>'''

if old_nav in content:
    content = content.replace(old_nav, new_nav)
    print('Nav updated')
else:
    print('Nav not found. Checking actual content...')
    idx = content.find('id="nav"')
    if idx >= 0:
        print(repr(content[idx:idx+300]))
    else:
        print('id="nav" not found at all')

with open(r'D:\Uni\hoc\quiz.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Done! {len(content)} bytes')
