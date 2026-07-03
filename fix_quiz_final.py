import json, re

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
questions = json.loads(content[json_start:json_end])

# ---- STEP 1: Character-level substitutions (100% safe) ----
CHAR_FIXES = [
    # 6 substitution (6 surrounded by letters = ô/ổ)
    (r'(?<=[a-zA-Z])6(?=[a-zA-Z\s,.]|$)', 'ô'),
    # 6 at start of word followed by letter
    (r'\b6(?=[a-z])', 'ổ'),
    # 16 as a word = lỗ
    (r'\b16\b', 'lỗ'),
]

def char_fix(text):
    for pattern, repl in CHAR_FIXES:
        text = re.sub(pattern, repl, text)
    return text

# ---- STEP 2: Safe phrase replacements (verified exact matches) ----
SAFE_PHRASES = {
    # These are verified exact matches from the actual quiz data
    'mô hinh': 'mô hình',
    'Mô hinh': 'Mô hình',
    'mô hnh': 'mô hình',
    'Mô hnh': 'Mô hình',
    'Nguyên tac': 'Nguyên tắc',
    'Nguyễn tắc': 'Nguyên tắc',
    'nguyên tac': 'nguyên tắc',
    'nguyên tắc': 'nguyên tắc',
    'Quyên tối': 'Quyền tối',
    'quyên tối': 'quyền tối',
    'hệ thống': 'hệ thống',
    'hệ thông': 'hệ thống',
    'bảo mật': 'bảo mật',
    'bảo mặt': 'bảo mật',
    'tền tệ': 'tiền tệ',
    'tần công': 'tấn công',
    'tần cộng': 'tấn công',
}

def phrase_fix(text):
    for old, new in SAFE_PHRASES.items():
        if old in text:
            text = text.replace(old, new)
    return text

# ---- STEP 3: Dictionary-based fix (conservative - only unambiguous matches) ----
with open(r'D:\Uni\hoc\viet_dict.txt', 'r', encoding='utf-8') as f:
    DICT_WORDS = set(line.strip() for line in f if line.strip())

def strip_diacritics(w):
    w = w.lower()
    replacements = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'đ': 'd',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    }
    for old, new in replacements.items():
        w = w.replace(old, new)
    return w

# Build unambiguous mapping: ascii -> viet (only when exactly one match)
ASCII_TO_VIET = {}
for w in DICT_WORDS:
    key = strip_diacritics(w)
    if key not in ASCII_TO_VIET:
        ASCII_TO_VIET[key] = []
    ASCII_TO_VIET[key].append(w)

AMBIGUOUS_KEYS = {k for k, v in ASCII_TO_VIET.items() if len(v) > 1}
UNAMBIGUOUS_MAP = {k: v[0] for k, v in ASCII_TO_VIET.items() if len(v) == 1}

# Common Vietnamese words that should NOT be auto-fixed (preserve original)
SKIP_WORDS = {'an', 'hoa', 'co', 'mo', 'to', 'so', 'lo', 'no', 'the', 'my', 'by', 'or', 'of', 'in', 'on', 'at', 'it', 'is', 'be'}

def dict_fix_word(word):
    """Fix a single word if it's an unambiguous match in the dictionary"""
    if not word or len(word) < 2:
        return word
    if word.lower() in SKIP_WORDS:
        return word
    
    key = strip_diacritics(word)
    if key in UNAMBIGUOUS_MAP:
        replacement = UNAMBIGUOUS_MAP[key]
        # Preserve case
        if word[0].isupper():
            replacement = replacement[0].upper() + replacement[1:]
        return replacement
    return word

def dict_fix(text):
    words = text.split(' ')
    result = []
    for w in words:
        # Extract leading/trailing punctuation
        prefix = ''
        suffix = ''
        while w and not w[0].isalpha():
            prefix += w[0]
            w = w[1:]
        while w and not w[-1].isalpha():
            suffix = w[-1] + suffix
            w = w[:-1]
        
        if w:
            fixed = dict_fix_word(w)
            result.append(prefix + fixed + suffix)
        else:
            result.append(prefix + suffix)
    return ' '.join(result)

# ---- Apply all fixes ----
for q in questions:
    # Apply character-level fixes first
    q['text'] = char_fix(q['text'])
    # Apply safe phrase fixes  
    q['text'] = phrase_fix(q['text'])
    # Apply conservative dictionary fix
    q['text'] = dict_fix(q['text'])
    
    for i in range(len(q['opts'])):
        q['opts'][i] = char_fix(q['opts'][i])
        q['opts'][i] = phrase_fix(q['opts'][i])
        q['opts'][i] = dict_fix(q['opts'][i])

# Save
new_json_str = json.dumps(questions, ensure_ascii=False)
old_json = content[json_start:json_end]
with open(r'D:\Uni\hoc\quiz.html', 'w', encoding='utf-8') as f:
    f.write(content[:json_start] + new_json_str + content[json_end:])

print('Done!')
