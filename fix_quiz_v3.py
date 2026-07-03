import json

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
questions = json.loads(content[json_start:json_end])

# Third pass: targeted fixes for remaining issues
fixes = [
    # Exact string replacements verified from context
    ('Sử dung mét bức', 'Sử dụng một bức'),
    ('mét bức tường', 'một bức tường'),
    ('mét ca nhân', 'một cá nhân'),
    ('vào mét ca', 'vào một cá'),
    ('La mét hoạt', 'Là một hoạt'),
    ('mét hoạt động', 'một hoạt động'),
    ('chi lam một', 'chỉ làm một'),
    
    ('kién trúc', 'kiến trúc'),
    ('kién', 'kiến'),
    
    ('các tién trình', 'các tiến trình'),
    ('các tién trinh', 'các tiến trình'),
    ('tién trinh trai', 'tiến trình trái'),
    ('những khau dau tién', 'những khâu đầu tiên'),
    ('khau dau tién', 'khâu đầu tiên'),
    ('dat tién về', 'đắt tiền về'),
    ('dao tién ao', 'đào tiền ảo'),
    ('đào tién', 'đào tiền'),
    ('doi tién', 'đòi tiền'),
    ('tồng tién', 'tống tiền'),
    ('phương tién lưu', 'phương tiện lưu'),
    
    ('thực té', 'thực tế'),
    
    ('biến hình', 'Biến hình'),
    ('Bién dich', 'Biên dịch'),
    
    ('diét virus', 'diệt virus'),
    
    ('Vô hiéu hóa', 'Vô hiệu hóa'),
    ('thiếu hiéu biết', 'thiếu hiểu biết'),
    ('hiéu biết va', 'hiểu biết và'),
    
    ('điều kién', 'điều kiện'),
    ('điều kiện', 'điều kiện'),  # no-op protection
    
    ('cy thệ vào', 'cụ thể vào'),
    ('trai phệp', 'trái phép'),
    
    ('Tan cong 6 at', 'Tấn công ồ ạt'),
    ('6 at, gay', 'ồ ạt, gây'),
    
    ('lỗ hệng mang', 'lỗ hổng mạng'),
    ('lỗ hệng tw', 'lỗ hổng tự'),
    ('lỗ hệng', 'lỗ hổng'),
    
    ('thực hiện', 'thực hiện'),  # no-op, already correct
    
    ('bao gdm', 'bao gồm'),
    ('quét dinh ky', 'quét định kỳ'),
    
    ('bổé sung', 'bổ sung'),
    
    ('cơng dang', 'cổng đang'),
    ('Quét cơng (Port', 'Quét cổng (Port'),
    
    ('thông thường', 'thông thường'),  # no-op
    
]

count = 0
for q in questions:
    old_text = q['text']
    for old, new in fixes:
        if old in q['text']:
            q['text'] = q['text'].replace(old, new)
    if q['text'] != old_text:
        count += 1
    
    for i in range(len(q['opts'])):
        old_opt = q['opts'][i]
        for old, new in fixes:
            if old in old_opt:
                q['opts'][i] = q['opts'][i].replace(old, new)

print(f'Touched {count} questions')

new_json_str = json.dumps(questions, ensure_ascii=False)
old_json = content[json_start:json_end]
with open(r'D:\Uni\hoc\quiz.html', 'w', encoding='utf-8') as f:
    f.write(content[:json_start] + new_json_str + content[json_end:])

print('Done!')
