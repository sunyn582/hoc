# -*- coding: utf-8 -*-
import re

with open("D:\\Uni\\hoc\\SQA_clean.md", "r", encoding="utf-8") as f:
    content = f.read()

# Split into lines
lines = content.split("\n")

current_group = ""
results = {}

for line in lines:
    if line.startswith("## Group"):
        current_group = line.replace("## ", "").strip()
        results[current_group] = []
    elif "### C" in line:
        m = re.search(r"### [Cc]\w+ (\d+)", line)
        if m and current_group:
            results[current_group].append(m.group(1))

out = []
for g, qs in results.items():
    sorted_qs = sorted(qs, key=int)
    out.append(g + ": " + str(len(qs)) + " cau")
    out.append("  Ma so: " + ", ".join(sorted_qs))
    out.append("")

all_qs = sorted(set(sum(results.values(), [])), key=int)
out.append("Tong so cau (khong trung): " + str(len(all_qs)))
out.append("Tat ca ma so: " + ", ".join(all_qs))
out.append("")

# Find duplicates across groups
from collections import Counter
flat = sum(results.values(), [])
dupes = {k: v for k, v in Counter(flat).items() if v > 1}
if dupes:
    out.append("=== CAU XUAT HIEN O NHIEU GROUP ===")
    for q, count in sorted(dupes.items()):
        groups = [g for g, qs in results.items() if q in qs]
        out.append(f"  Cau {q}: {count} lan -> {', '.join(groups)}")

with open("D:\\Uni\\hoc\\question_check.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Done! Check question_check.txt")
