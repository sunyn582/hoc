import re, json

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
json_str = content[json_start:json_end]
questions = json.loads(json_str)

# Targeted fixes for remaining issues
def apply_fixes(text):
    fixes = {
        # é still remaining
        'kién trúc': 'kiến trúc',
        'Kién trúc': 'Kiến trúc',
        'một cách': 'một cách',
        'mét ': 'một ',
        'Mét ': 'Một ',
        'biến hình': 'Biến hình',
        'Bién': 'Biến',
        'bién': 'biến',
        'diét ': 'diệt ',
        'diét': 'diệt',
        'tién ': 'tiền ',
        'tiến': 'tiến',
        'tiên': 'tiên',
        'Tién': 'Tiền',
        'hiéu hóa': 'hiệu hóa',
        'hiéu biết': 'hiểu biết',
        'hiéu': 'hiệu',
        'diéu': 'điều',
        'diều': 'điều',
        'diễu': 'điều',
        'khiến': 'khiến',
        'quét': 'quét',  # no change needed
        'té ': 'tế ',
        'thực té': 'thực tế',
        'thệng': 'thống',
        'hệng': 'hổng',
        'hệ thống': 'hệ thống',
        'bổé': 'bổ',
        '6 at': 'ồ ạt',
        'điều kién': 'điều kiện',
        'công cu': 'công cụ',
        'tiền ao': 'tiền ảo',
        'tồng tién': 'tổng tiền',
        'cơng': 'cổng',
        'đểi': 'đối',
        'thệ ': 'thể ',
        'các tién trình': 'các tiến trình',
        'tien trinh': 'tiến trình',
        'tien trình': 'tiến trình',
        'tien trinh': 'tiến trình',
        'doi tién': 'đòi tiền',
        'đòi tién': 'đòi tiền',
        'tien ao': 'tiền ảo',
        'quét lỗ': 'quét lỗ',
        'ma nguồn': 'mã nguồn',
        'dinh ky': 'định kỳ',
        'hau dau': 'hầu đầu',
        'thông thường': 'thông thường',
        'mang ma': 'mạng mã',
        'lỗ hệng': 'lỗ hổng',
        'lỗ hông': 'lỗ hổng',
        'file b...': 'file bằng...',
        'tĩnh': 'tĩnh',
        'thông tin': 'thông tin',
        'bao gdm': 'bao gồm',
        'gồm': 'gồm',
        'Lién quan': 'Liên quan',
    }
    
    for old, new in fixes.items():
        if old in text:
            text = text.replace(old, new)
    
    return text

# Apply to all questions
for q in questions:
    q['text'] = apply_fixes(q['text'])
    for i in range(len(q['opts'])):
        q['opts'][i] = apply_fixes(q['opts'][i])

# Re-serialize and write back
new_json_str = json.dumps(questions, ensure_ascii=False)
old_json = content[json_start:json_end]
new_content = content[:json_start] + new_json_str + content[json_end:]

with open(r'D:\Uni\hoc\quiz.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done!')
