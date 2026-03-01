import re

file_path = r'c:\Users\Kudzanai\Documents\2025\App Developments\TapFo\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def find_lines(pattern):
    results = []
    for i, line in enumerate(lines):
        if pattern in line:
            results.append((i + 1, line.strip()))
    return results

print("--- .search-bar ---")
for l, content in find_lines(".search-bar"):
    print(f"L{l}: {content}")

print("\n--- .ql-trapezoid ---")
for l, content in find_lines(".ql-trapezoid"):
    print(f"L{l}: {content}")

print("\n--- .cursor-placeholder ---")
for l, content in find_lines(".cursor-placeholder"):
    print(f"L{l}: {content}")

print("\n--- navigateToPage ---")
for l, content in find_lines("function navigateToPage"):
    print(f"L{l}: {content}")

print("\n--- app-shell max-width ---")
for l, content in find_lines("max-width: 500px"):
    print(f"L{l}: {content}")
