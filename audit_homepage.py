import re

file_path = r'c:\Users\Kudzanai\Documents\2025\App Developments\TapFo\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Audit for specific targets to find ALL occurrences
targets = ['.search-bar', '.ql-trapezoid', '.ql-trap-pill', '.cursor-placeholder', '#app-shell', '#page-home']

for target in targets:
    matches = [m.start() for m in re.finditer(re.escape(target), content)]
    print(f"--- {target} ({len(matches)} matches) ---")
    for pos in matches:
        start = max(0, pos - 40)
        end = min(len(content), pos + 160)
        snippet = content[start:end].replace('\n', '\\n')
        print(f"Pos {pos}: {snippet}")

# Check for navigation function definitions
nav_functions = ['function navigateWithSwipe', 'function navigateToPage', 'function showPage']
for func in nav_functions:
    matches = [m.start() for m in re.finditer(func, content)]
    print(f"--- {func} ({len(matches)} matches) ---")
    for pos in matches:
        start = max(0, pos - 20)
        end = min(len(content), pos + 100)
        print(f"Pos {pos}: {content[start:end]}")
