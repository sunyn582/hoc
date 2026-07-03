import json

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
questions = json.loads(content[json_start:json_end])

# Show first 10 questions
for q in questions[:10]:
    print(f'=== Q{q["id"]} ===')
    print(f'Text: {q["text"][:150]}')
    for i, o in enumerate(q['opts']):
        print(f'  {i}. {o[:100]}')
    print()

# Show questions that still have issues
print('=' * 60)
print('REMAINING ISSUES:')
print('=' * 60)
for q in questions:
    for field_name, field_val in [('text', q['text'])] + [(f'opt{i}', o) for i, o in enumerate(q['opts'])]:
        if '6' in field_val and not any(x in field_val for x in ['256', '80', '443', '22', '21', '3306']):
            print(f'Q{q["id"]} {field_name}: ...{field_val[:80]}... [HAS 6]')
        if 'é' in field_val:
            idx = field_val.index('é')
            ctx = field_val[max(0,idx-10):idx+15]
            print(f'Q{q["id"]} {field_name}: ...{ctx}... [HAS é]')
        if '8' in field_val and field_val.strip('8') != field_val:
            # Only flag 8 used in non-numeric context
            for m in __import__('re').finditer(r'[a-zA-Z]8', field_val):
                print(f'Q{q["id"]} {field_name}: ...{field_val[max(0,m.start()-5):m.end()+10]}... [HAS 8 in word]')
