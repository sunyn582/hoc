import json, re

# Load Vietnamese dictionary
with open(r'D:\Uni\hoc\viet_dict.txt', 'r', encoding='utf-8') as f:
    DICT_WORDS = set(line.strip() for line in f if line.strip())

# Build mapping from ASCII form -> Vietnamese form
# e.g., "dung" -> set(["dùng", "dụng", "dừng", "dũng", "dưng", "dụng"])
ASCII_TO_VIET = {}
for w in DICT_WORDS:
    ascii_form = w.lower()
    # Remove all diacritics from Vietnamese characters
    ascii_form = ascii_form.replace('à', 'a').replace('á', 'a').replace('ả', 'a').replace('ã', 'a').replace('ạ', 'a')
    ascii_form = ascii_form.replace('ă', 'a').replace('ằ', 'a').replace('ắ', 'a').replace('ẳ', 'a').replace('ẵ', 'a').replace('ặ', 'a')
    ascii_form = ascii_form.replace('â', 'a').replace('ầ', 'a').replace('ấ', 'a').replace('ẩ', 'a').replace('ẫ', 'a').replace('ậ', 'a')
    ascii_form = ascii_form.replace('đ', 'd')
    ascii_form = ascii_form.replace('è', 'e').replace('é', 'e').replace('ẻ', 'e').replace('ẽ', 'e').replace('ẹ', 'e')
    ascii_form = ascii_form.replace('ê', 'e').replace('ề', 'e').replace('ế', 'e').replace('ể', 'e').replace('ễ', 'e').replace('ệ', 'e')
    ascii_form = ascii_form.replace('ì', 'i').replace('í', 'i').replace('ỉ', 'i').replace('ĩ', 'i').replace('ị', 'i')
    ascii_form = ascii_form.replace('ò', 'o').replace('ó', 'o').replace('ỏ', 'o').replace('õ', 'o').replace('ọ', 'o')
    ascii_form = ascii_form.replace('ô', 'o').replace('ồ', 'o').replace('ố', 'o').replace('ổ', 'o').replace('ỗ', 'o').replace('ộ', 'o')
    ascii_form = ascii_form.replace('ơ', 'o').replace('ờ', 'o').replace('ớ', 'o').replace('ở', 'o').replace('ỡ', 'o').replace('ợ', 'o')
    ascii_form = ascii_form.replace('ù', 'u').replace('ú', 'u').replace('ủ', 'u').replace('ũ', 'u').replace('ụ', 'u')
    ascii_form = ascii_form.replace('ư', 'u').replace('ừ', 'u').replace('ứ', 'u').replace('ử', 'u').replace('ữ', 'u').replace('ự', 'u')
    ascii_form = ascii_form.replace('ỳ', 'y').replace('ý', 'y').replace('ỷ', 'y').replace('ỹ', 'y').replace('ỵ', 'y')
    
    if ascii_form not in ASCII_TO_VIET:
        ASCII_TO_VIET[ascii_form] = []
    ASCII_TO_VIET[ascii_form].append(w)

# For words with multiple matches, prioritize common security terms
SECURITY_PRIORITY = [
    'dụng',  # sử dụng
    'dùng',  # người dùng
    'mạng',  # an ninh mạng
    'tính',  # tính năng
    'nào',   # thế nào
    'được',  # được
    'của',   # của
    'các',   # các
    'và',    # và
    'là',    # là
    'một',   # một
    'có',    # có
    'như',   # như
    'với',   # với
    'hoặc',  # hoặc
    'cho',   # cho
    'trên',  # trên
    'thông', # thông tin
    'tấn',   # tấn công
    'công',  # tấn công
    'phần',  # phần mềm
    'thiết', # thiết bị
    'kiểm',  # kiểm tra
    'bảo',   # bảo mật
    'dữ',    # dữ liệu
    'liệu',  # dữ liệu
    'ứng',   # ứng dụng
    'qua',   # qua
    'tại',   # tại
]

def pick_best_word(ascii_word, candidates):
    """Pick the best Vietnamese word from candidates for context"""
    if len(candidates) == 1:
        return candidates[0]
    
    # Check security priority first
    for p in SECURITY_PRIORITY:
        if p in candidates:
            return p
    
    # Default: pick the one with most diacritics (most specific)
    return max(candidates, key=lambda w: sum(1 for c in w if ord(c) > 127))

# Load quiz
with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
questions = json.loads(content[json_start:json_end])

def fix_text(text):
    """Fix missing diacritics in Vietnamese text using dictionary"""
    words = text.split(' ')
    new_words = []
    for w in words:
        # Skip if word has no letters
        if not any(c.isalpha() for c in w):
            new_words.append(w)
            continue
        
        # Check if word already has Vietnamese diacritics
        has_diacritics = any(ord(c) > 127 for c in w if c.isalpha())
        
        if not has_diacritics:
            # Word is pure ASCII - look for dictionary match
            key = w.lower().strip('.,;:!?()[]{}"\'')
            suffix = w[len(key):] if key in w else ''
            
            if key in ASCII_TO_VIET:
                candidates = ASCII_TO_VIET[key]
                if len(candidates) == 1:
                    # Exactly one match
                    replacement = candidates[0]
                    # Preserve case
                    if w[0].isupper():
                        replacement = replacement[0].upper() + replacement[1:]
                    new_words.append(replacement + suffix)
                    continue
                elif len(candidates) > 1:
                    # Multiple matches - pick best
                    replacement = pick_best_word(key, candidates)
                    if w[0].isupper():
                        replacement = replacement[0].upper() + replacement[1:]
                    new_words.append(replacement + suffix)
                    continue
        
        # Keep original word
        new_words.append(w)
    
    return ' '.join(new_words)

# Apply to all questions
for q in questions:
    q['text'] = fix_text(q['text'])
    for i in range(len(q['opts'])):
        q['opts'][i] = fix_text(q['opts'][i])

# Save back
new_json_str = json.dumps(questions, ensure_ascii=False)
old_json = content[json_start:json_end]
new_content = content[:json_start] + new_json_str + content[json_end:]

with open(r'D:\Uni\hoc\quiz.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done! Fixed missing diacritics using Vietnamese dictionary.')
