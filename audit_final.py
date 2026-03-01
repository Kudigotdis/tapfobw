import re

file_path = r'c:\Users\Kudzanai\Documents\2025\App Developments\TapFo\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def audit(pattern):
    print(f"\n--- Searching for: {pattern} ---")
    for i, line in enumerate(lines):
        if pattern in line:
            print(f"L{i+1}: {line.strip()}")

targets = ['.search-bar {', '.ql-trapezoid', '.ql-trap-pill', '.cursor-placeholder', '#app-shell', '#page-home', 'function navigateToPage', 'function navigateWithSwipe']
for t in targets:
    audit(t)
