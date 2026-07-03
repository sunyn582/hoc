import re, json

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
questions = json.loads(content[json_start:json_end])

print(f'Total questions: {len(questions)}')
print()

# Find all text quality issues
for q in questions:
    text = q['text']
    issues = []
    
    # Pattern: letter+6 or 6+letter (shorthand for ô/ơ/ổ etc.)
    for m in re.finditer(r'(?:[a-zA-Z][68]|[68][a-zA-Z]|\b[68]\b)', text):
        issues.append('6/8:' + m.group().strip())
    
    # Check for wrongly-encoded Vietnamese chars
    # é used instead of ê, ệ, ể etc.
    for m in re.finditer(r'\w*[éắ]\w*', text):
        issues.append('diacritic:' + m.group())
    
    if issues:
        print(f'Q{q["id"]}: {text[:120]}')
        for iss in issues:
            print(f'   >> {iss}')
        print()

# Also show some sample options with issues
print('=' * 60)
print('SAMPLE OPTIONS WITH ISSUES:')
print('=' * 60)
count = 0
for q in questions:
    for i, opt in enumerate(q['opts']):
        if count >= 30:
            break
        has_issue = False
        for m in re.finditer(r'(?:[a-zA-Z][68]|[68][a-zA-Z]|\b[68]\b)', opt):
            has_issue = True
            break
        if has_issue:
            print(f'Q{q["id"]} opt{i}: {opt[:120]}')
            count += 1
    if count >= 30:
        break
