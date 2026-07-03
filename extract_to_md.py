import re, json

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
json_str = content[json_start:json_end]
questions = json.loads(json_str)

lines = []
lines.append('# Quiz ATTT - 150 câu hỏi An toàn thông tin')
lines.append('')
lines.append('> File này được extract từ PDF gốc. Chữ Tiếng Việt bị thiếu dấu/sai. Hãy sửa lại cho đúng.')
lines.append('')

for q in questions:
    lines.append(f'## Câu {q["id"]}')
    lines.append('')
    lines.append(q['text'])
    lines.append('')
    abc = ['A', 'B', 'C', 'D']
    for i, opt in enumerate(q['opts']):
        marker = '(*)' if i == q['answer'] else '( )'
        lines.append(f'- {marker} {abc[i]}. {opt}')
    lines.append('')
    lines.append(f'  Đáp án đúng: **{abc[q["answer"]]}**')
    lines.append('')
    lines.append('---')
    lines.append('')

with open(r'D:\Uni\hoc\quiz.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Done! Wrote {len(questions)} questions to quiz.md')
