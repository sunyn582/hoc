import re, json

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
json_str = content[json_start:json_end]
questions = json.loads(json_str)
print(f'Total questions in HTML: {len(questions)}')
print()

for q in questions[:5]:
    print(f'ID: {q["id"]}')
    print(f'Text: {q["text"]}')
    for i, opt in enumerate(q["opts"]):
        print(f'  {i}: {opt}')
    print(f'Answer: {q["answer"]}')
    print()
