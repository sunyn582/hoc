import json

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
questions = json.loads(content[json_start:json_end])

# Show questions 4-15
for q in questions[3:15]:
    print(f'=== Q{q["id"]} ===')
    print(f'{q["text"][:200]}')
    for i, o in enumerate(q['opts']):
        print(f'  {i}: {o[:150]}')
    print()
