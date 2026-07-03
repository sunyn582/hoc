import json, re

with open(r'D:\Uni\hoc\quiz.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('ALL_QUESTIONS')
json_start = content.index('[', start)
json_end = content.index('];', json_start) + 1
questions = json.loads(content[json_start:json_end])

# Step 1: Character-level fixes
def step1_char(text):
    text = re.sub(r'(?<=[a-zA-Z])6(?=[a-zA-Z\s,.\])]|$)', 'ô', text)
    text = re.sub(r'\b6(?=[a-z])', 'ổ', text)
    text = re.sub(r'\b16\b', 'lỗ', text)
    text = re.sub(r'é', 'ê', text)
    return text

# Step 2: Phrase-level overrides (where step1 is wrong)
def step2_phrase(text):
    # Process longer phrases first to avoid partial matches
    overrides = [
        # téi -> tối
        ('têi', 'tối'), ('Têi', 'Tối'),
        # tổng tiền
        ('tổng tông', 'tổng tổng'),  # safety
        ('tông', 'tổng'), ('Tông', 'Tổng'),
        # tồn tại
        ('tôn tai', 'tồn tại'), ('Tôn tai', 'Tồn tại'),
        ('tên tai', 'tồn tại'), ('Tên tai', 'Tồn tại'),
        # tồn
        ('tên', 'tồn'), ('Tên', 'Tồn'),
        # tốt
        ('tết nhất', 'tốt nhất'), ('Tết nhất', 'Tốt nhất'),
        ('tết', 'tốt'), ('Tết', 'Tốt'),
        # phổ biến
        ('phê biến', 'phổ biến'), ('Phê biến', 'Phổ biến'),
        ('phê', 'phổ'), ('Phê', 'Phổ'),
        # không
        ('khêng', 'không'), ('Khêng', 'Không'),
        # hổng
        ('hêng', 'hổng'), ('Hêng', 'Hổng'),
        # hóa
        ('hêa', 'hóa'), ('Hêa', 'Hóa'),
        # thể/thế
        ('thê nào', 'thế nào'), ('Thê nào', 'Thế nào'),
        ('thê', 'thể'), ('Thê', 'Thể'),
        # nguồn
        ('nguên gốc', 'nguồn gốc'),
        ('nguên', 'nguồn'), ('Nguên', 'Nguồn'),
        # điểm
        ('diêm', 'điểm'), ('Diêm', 'Điểm'),
        # tiền/tiến
        ('tổng tiên', 'tổng tiền'),
        ('tống tiên', 'tống tiền'),
        ('đòi tiên', 'đòi tiền'),
        ('tiên ảo', 'tiền ảo'),
        ('tiên trinh', 'tiến trình'),
        ('tiên trình', 'tiến trình'),
        ('tiên tới', 'tiến tới'),
        # mềm
        ('phần mêm', 'phần mềm'),
        ('mêm', 'mềm'), ('Mêm', 'Mềm'),
        # chiến lược
        ('chiên lược', 'chiến lược'),
        ('chiên l', 'chiến l'),
        # chính sách
        ('chính sạch', 'chính sách'),
        # như
        (' như ', ' như '),
        # là (with spaces)
        (' la ', ' là '),
        (' la,', ' là,'),
        (' la.', ' là.'),
        # và (with spaces)
        (' va ', ' và '),
        (' va,', ' và,'),
        (' va.', ' và.'),
        # của (with spaces)
        (' cua ', ' của '),
        (' cua,', ' của,'),
        (' cua.', ' của.'),
    ]
    # Sort by length descending
    overrides.sort(key=lambda x: -len(x[0]))
    for old, new in overrides:
        if old in text:
            text = text.replace(old, new)
    return text

def step2_phrase(text):
    for old, new in STEP2:
        if old in text:
            text = text.replace(old, new)
    return text

# Step 3: Missing diacritics via dictionary (conservative)
with open(r'D:\Uni\hoc\viet_dict.txt', 'r', encoding='utf-8') as f:
    dict_words = set(line.strip() for line in f if line.strip())

def strip_all(w):
    w = w.lower()
    for a, b in [('à','a'),('á','a'),('ả','a'),('ã','a'),('ạ','a'),
                  ('ă','a'),('ằ','a'),('ắ','a'),('ẳ','a'),('ẵ','a'),('ặ','a'),
                  ('â','a'),('ầ','a'),('ấ','a'),('ẩ','a'),('ẫ','a'),('ậ','a'),
                  ('đ','d'),
                  ('è','e'),('é','e'),('ẻ','e'),('ẽ','e'),('ẹ','e'),
                  ('ê','e'),('ề','e'),('ế','e'),('ể','e'),('ễ','e'),('ệ','e'),
                  ('ì','i'),('í','i'),('ỉ','i'),('ĩ','i'),('ị','i'),
                  ('ò','o'),('ó','o'),('ỏ','o'),('õ','o'),('ọ','o'),
                  ('ô','o'),('ồ','o'),('ố','o'),('ổ','o'),('ỗ','o'),('ộ','o'),
                  ('ơ','o'),('ờ','o'),('ớ','o'),('ở','o'),('ỡ','o'),('ợ','o'),
                  ('ù','u'),('ú','u'),('ủ','u'),('ũ','u'),('ụ','u'),
                  ('ư','u'),('ừ','u'),('ứ','u'),('ử','u'),('ữ','u'),('ự','u'),
                  ('ỳ','y'),('ý','y'),('ỷ','y'),('ỹ','y'),('ỵ','y')]:
        w = w.replace(a, b)
    return w

# Build unambiguous mapping
ascii_to_viet = {}
for w in dict_words:
    k = strip_all(w)
    if k not in ascii_to_viet:
        ascii_to_viet[k] = []
    ascii_to_viet[k].append(w)

unambiguous = {k: v[0] for k, v in ascii_to_viet.items() if len(v) == 1}

# Common English words to never touch
ENGLISH = {'an', 'is', 'in', 'on', 'at', 'to', 'by', 'of', 'or', 'for', 'the', 
           'and', 'be', 'it', 'as', 'no', 'so', 'if', 'but', 'not', 'are',
           'was', 'can', 'all', 'any', 'has', 'had', 'its', 'may', 'new',
           'web', 'key', 'way', 'use', 'get', 'set', 'run', 'pin', 'top',
           'one', 'two', 'six', 'out', 'end', 'act', 'own', 'old', 'see',
           'man', 'men', 'air', 'age', 'who', 'why', 'how', 'far', 'non',
           'post', 'port', 'file', 'code', 'data', 'Base', 'SQL', 'DOM',
           'URL', 'API', 'CPU', 'RAM', 'ROM', 'DoS', 'DNS', 'LAN', 'WAN',
           'VPN', 'WAF', 'SOC', 'CEO', 'CFO', 'CIO', 'CISO',
           'Security', 'Firewall', 'Server', 'Client', 'Access',
           'Control', 'Management', 'Policy', 'Standard', 'Network',
           'Gateway', 'Router', 'Switch', 'Proxy', 'Agent',
           'Attack', 'Protocol', 'Gateway', 'System', 'Service',
           'Encryption', 'Decryption', 'Authentication', 'Authorization',
           'Confidentiality', 'Integrity', 'Availability',
           'Certificate', 'Authority', 'Signature', 'Token',
           'Session', 'Cookie', 'Domain', 'Certificate',
           'Exploit', 'Vulnerability', 'Risk', 'Threat',
           'Active', 'Passive', 'Direct', 'Indirect', 'Internal',
           'External', 'Physical', 'Logical', 'Virtual',
           'Private', 'Public', 'Shared', 'Dedicated',
           'Static', 'Dynamic', 'Runtime', 'Compile',
           'Source', 'Binary', 'Executable', 'Library',
           'Testing', 'Scanning', 'Monitoring', 'Auditing',
           'Policy', 'Standard', 'Procedure', 'Guideline',
           'Recovery', 'Backup', 'Restore', 'Failover',
           'Version', 'Release', 'Deployment', 'Pipeline',
           'Notification', 'Alert', 'Warning', 'Critical',
           'Layer', 'Level', 'Tier', 'Phase',
           'Mode', 'State', 'Status', 'Config',
           'Default', 'Custom', 'Manual', 'Automatic',
}

# Vietnamese function words that are often ambiguous
VIET_AMBIGUOUS = {'co', 'mo', 'to', 'so', 'lo', 'no', 'ho', 'do', 'vo', 'bo',
                  'ca', 'la', 'da', 'xa', 'sa', 'ga', 'ha', 'ba', 'ma', 'na',
                  'cua', 'dua', 'tua', 'sua', 'lua', 'nua',
                  'qua', 'toa', 'soa', 'loa', 'hoa', 'noa',
                  'tay', 'may', 'hay', 'say', 'bay', 'cay',
                  'tai', 'mai', 'hai', 'bai', 'cai', 'dai',
                  'lam', 'cam', 'sam', 'tam', 'nam', 'dam',
                  'tan', 'san', 'man', 'dan', 'lan', 'can',
                  'tin', 'hin', 'min', 'sin', 'din', 'lin',
                  'tinh', 'minh', 'linh', 'sinh', 'dinh',
                  'thu', 'chu', 'nhu', 'khu', 'phu',
                  'the', 'che', 'khe', 'nhe',
                  'tra', 'cha', 'kha', 'nha', 'pha'}

def step3_dict(text):
    words = text.split(' ')
    result = []
    for w in words:
        pre = ''
        post = ''
        while w and not w[0].isalpha():
            pre += w[0]
            w = w[1:]
        while w and not w[-1].isalpha():
            post = w[-1] + post
            w = w[:-1]
        
        if w:
            low = w.lower()
            if low in unambiguous and low not in ENGLISH and low not in VIET_AMBIGUOUS and len(low) >= 3:
                repl = unambiguous[low]
                if w[0].isupper():
                    repl = repl[0].upper() + repl[1:]
                result.append(pre + repl + post)
            else:
                result.append(pre + w + post)
        else:
            result.append(pre + post)
    return ' '.join(result)

# Apply
for q in questions:
    q['text'] = step3_dict(step2_phrase(step1_char(q['text'])))
    for i in range(len(q['opts'])):
        q['opts'][i] = step3_dict(step2_phrase(step1_char(q['opts'][i])))

new_json = json.dumps(questions, ensure_ascii=False)
with open(r'D:\Uni\hoc\quiz.html', 'w', encoding='utf-8') as f:
    f.write(content[:json_start] + new_json + content[json_end:])

print('Done!')
