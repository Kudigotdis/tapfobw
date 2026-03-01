import re
import os

file_path = r'c:\Users\Kudzanai\Documents\2025\App Developments\TapFo\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check for .search-bar occurrences
search_bar_matches = [m.start() for m in re.finditer(r'.search-bar', content)]
print(f"Found {len(search_bar_matches)} occurrences of .search-bar")
for pos in search_bar_matches:
    start = max(0, pos - 50)
    end = min(len(content), pos + 200)
    print(f"--- Occurrence at {pos} ---\n{content[start:end]}\n")

# Check for .ql-trapezoid occurrences
ql_matches = [m.start() for m in re.finditer(r'.ql-trapezoid', content)]
print(f"Found {len(ql_matches)} occurrences of .ql-trapezoid")
for pos in ql_matches:
    start = max(0, pos - 50)
    end = min(len(content), pos + 200)
    print(f"--- Occurrence at {pos} ---\n{content[start:end]}\n")

# Check for .cursor-placeholder occurrences
cursor_matches = [m.start() for m in re.finditer(r'.cursor-placeholder', content)]
print(f"Found {len(cursor_matches)} occurrences of .cursor-placeholder")
for pos in cursor_matches:
    start = max(0, pos - 50)
    end = min(len(content), pos + 200)
    print(f"--- Occurrence at {pos} ---\n{content[start:end]}\n")

# Check for navigateToPage definition
nav_def_matches = [m.start() for m in re.finditer(r'function navigateToPage', content)]
print(f"Found {len(nav_def_matches)} definitions of navigateToPage")
