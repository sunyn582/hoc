import re, json

with open(r'D:\Uni\hoc\quiz.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by question using regex
blocks = re.split(r'\n(?=Câu\s+\d+\s*:)', text.strip())

questions = []
answer_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

for block in blocks:
    lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
    if not lines:
        continue

    # Parse first line: "Câu N: ..."
    m = re.match(r'^Câu\s+(\d+)\s*:\s*(.*)', lines[0])
    if not m:
        continue
    qid = m.group(1)
    qtext = m.group(2)
    
    opts = []
    answer = -1
    
    for line in lines[1:]:
        # Check for answer
        m = re.match(r'^Đáp\s*án\s*:\s*([A-D])', line)
        if m:
            answer = answer_map[m.group(1)]
            continue
        
        # Check for option
        m = re.match(r'^([A-D])\.\s*(.*)', line)
        if m:
            opts.append(m.group(2))
            continue
        
        # Continuation: append to last thing
        if opts:
            opts[-1] += ' ' + line
        else:
            qtext += ' ' + line
    
    # Clean up whitespace in opts
    opts = [' '.join(o.split()) for o in opts]
    qtext = ' '.join(qtext.split())
    
    questions.append({
        'id': qid,
        'text': qtext,
        'opts': opts,
        'answer': answer
    })

questions.sort(key=lambda q: int(q['id']))

print(f'Parsed {len(questions)} questions')

# Validate
for q in questions:
    if q['answer'] < 0:
        print(f'WARN: Question {q["id"]} has no answer!')
    if len(q['opts']) != 4:
        print(f'WARN: Question {q["id"]} has {len(q["opts"])} options (expected 4)')

# Save to JSON
with open(r'D:\Uni\hoc\quiz_data.json', 'w', encoding='utf-8') as f:
    json.dump({'questions': questions}, f, ensure_ascii=False, indent=2)
print('Saved to quiz_data.json')

# Generate markdown
md_lines = []
md_lines.append('# Quiz ATTT - 150 câu hỏi An toàn thông tin')
md_lines.append('')
for q in questions:
    md_lines.append(f'## Câu {q["id"]}')
    md_lines.append('')
    md_lines.append(q['text'])
    md_lines.append('')
    abc = ['A', 'B', 'C', 'D']
    for i, opt in enumerate(q['opts']):
        marker = '(*)' if i == q['answer'] else '( )'
        md_lines.append(f'- {marker} {abc[i]}. {opt}')
    md_lines.append('')
    md_lines.append(f'  Đáp án đúng: **{abc[q["answer"]]}**')
    md_lines.append('')
    md_lines.append('---')
    md_lines.append('')

with open(r'D:\Uni\hoc\quiz.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))
print('Saved to quiz.md')

# Generate HTML questions
html_questions = []
for q in questions:
    html_q = {
        'id': q['id'],
        'text': q['text'],
        'opts': q['opts'],
        'answer': q['answer']
    }
    html_questions.append(html_q)

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

start = html_content.index('ALL_QUESTIONS')
json_start = html_content.index('[', start)
json_end = html_content.index('];', json_start) + 1

new_json_str = json.dumps(html_questions, ensure_ascii=False)
new_html = html_content[:json_start] + new_json_str + html_content[json_end:]

# Update counter references
count = len(questions)
new_html = new_html.replace('150 câu hỏi', f'{count} câu hỏi')
new_html = new_html.replace('/ 150', f'/ {count}')

with open(r'D:\Uni\hoc\quiz.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print(f'Saved to quiz.html ({count} questions)')

# Verify
print()
print('First question:')
print(json.dumps(html_questions[0], ensure_ascii=False, indent=2))
print()
print('Last question:')
print(json.dumps(html_questions[-1], ensure_ascii=False, indent=2))
