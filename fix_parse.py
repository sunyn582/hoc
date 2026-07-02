# -*- coding: utf-8 -*-
import re

with open("D:\\Uni\\hoc\\Ngân hàng câu hỏi_SQA_06_2026.md", "r", encoding="utf-8") as f:
    raw = f.read()

raw = re.sub(r"## Page \d+\s*", "", raw)
raw = re.sub(r"\n+", " ", raw)
raw = re.sub(r"[ \t]+", " ", raw)
raw = raw.strip()

META_RE = r"\b(DE|TB|KHO)\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?"

header_end = raw.find("II. Nội dung các câu hỏi trắc nghiệm")
header_text = raw[:header_end].strip() if header_end > 0 else ""
questions_text = raw[header_end:] if header_end > 0 else raw

out_lines = [
    "# Ngân hàng câu hỏi SQA", "",
    "## Thông tin đề thi", "",
    header_text.replace("Học phần:", "**Học phần:**").replace("Được/không", "\\\nĐược/không"), "",
]

# Find group boundaries - use Group N. at start of line as marker
group_starts = list(re.finditer(r"Group \d+\.", questions_text))

for gi in range(len(group_starts)):
    g_start = group_starts[gi].start()
    g_end = group_starts[gi+1].start() if gi+1 < len(group_starts) else len(questions_text)
    g_text = questions_text[g_start:g_end].strip()
    
    # Extract group header (everything up to the first 3-digit question number)
    first_q = re.search(r"\b\d{3}\s", g_text)
    if first_q:
        gheader = g_text[:first_q.start()].strip()
        gcontent = g_text[first_q.start():].strip()
    else:
        gheader = g_text
        gcontent = ""
    
    out_lines.append("---")
    out_lines.append(f"## {gheader}")
    out_lines.append("")
    
    # Split by End and process each question
    question_parts = gcontent.split("End")
    for part in question_parts:
        part = part.strip()
        if not part or len(part) < 5:
            continue
        
        # Use search() instead of match() to find question numbers anywhere
        m = re.search(r"(\d{3})\s+(.*)", part)
        if not m:
            continue
        
        qnum = m.group(1)
        rest = m.group(2)
        
        diff_code = ""
        dm = re.search(r"\b(DE|TB|KHO)\b", rest)
        if dm:
            diff_code = dm.group(1)
            rest = re.sub(META_RE, "", rest, count=1)
        
        diff_map = {"DE": "Dễ", "TB": "Trung Bình", "KHO": "Khó"}
        diff_label = diff_map.get(diff_code, "")
        rest = rest.strip()
        
        opt_spans = []
        search_from = 0
        for opt_num in [1, 2, 3, 4]:
            pattern = r"(\s)(" + str(opt_num) + r")\s+"
            om = re.search(pattern, rest[search_from:])
            if om:
                start = search_from + om.start(1)
                end = search_from + om.end()
                opt_spans.append((opt_num, start, end))
                search_from = end
            else:
                break
        
        if len(opt_spans) == 4:
            qtext = rest[:opt_spans[0][1]].strip()
            out_lines.append(f"### Câu {qnum} ({diff_label})")
            out_lines.append("")
            out_lines.append(qtext)
            out_lines.append("")
            for j in range(4):
                num, start, end_sp = opt_spans[j]
                next_start = opt_spans[j+1][1] if j < 3 else len(rest)
                opt_text = rest[end_sp:next_start].strip()
                is_correct = "*" in opt_text
                opt_text = opt_text.replace("*", "").strip()
                if is_correct:
                    out_lines.append(f"- **[{num}] {opt_text}** ✅")
                else:
                    out_lines.append(f"- [{num}] {opt_text}")
            out_lines.append("")
        else:
            out_lines.append(f"### Câu {qnum} ({diff_label})")
            out_lines.append("")
            out_lines.append(rest)
            out_lines.append("")

with open("D:\\Uni\\hoc\\SQA_clean.md", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print("Done!")
