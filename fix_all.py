import os
import re

file_path = r'c:\Users\Kudzanai\Documents\2025\App Developments\TapFo\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Flattern pills: remove .ql-trap-row wrappers in the homepage
# We find the quick links section in the home page only.
home_page_start = content.find('<div class="page" id="page-home">')
ql_trap_start = content.find('<div class="ql-trapezoid"', home_page_start)
ql_trap_end = content.find('<!-- ══ QUICK LINKS', ql_trap_start) # Safe end marker

if ql_trap_start != -1 and ql_trap_end != -1:
    ql_section = content[ql_trap_start:ql_trap_end]
    # Remove all instances of <div class="ql-trap-row"> and </div> from this section
    # Use re.sub to handle any whitespace inside the tags
    cleaned_ql = re.sub(r'<div class="ql-trap-row".*?>', '', ql_section)
    cleaned_ql = cleaned_ql.replace('</div>', '')
    # Put back the outer trapezoid div and its gap/flex styles
    # Wait, cleaned_ql removed the outer closing </div> too!
    # Let's be more precise.
    
    # Actually, let's just use re.findall to get all the pills.
    pills = re.findall(r'<button class="ql-trap-pill".*?</button>', ql_section, re.DOTALL)
    new_ql_section = '<div class="ql-trapezoid" style="margin-top:20px; display:flex; flex-wrap:wrap; justify-content:center; gap:8px;">\\n'
    for pill in pills:
        new_ql_section += '                    ' + pill.strip() + '\\n'
    new_ql_section += '                  </div>\\n                '
    
    content = content[:ql_trap_start] + new_ql_section + content[ql_trap_end:]

# 2. Fix About page card visibility
# Increase shadow and add a distinct background color if needed, but white card on grey background is better.
# Wait, the About page scroll area needs a background that isn't white to make white cards pop.
# #page-about .body-scroll should be #f5f5f5
content = content.replace('#page-about {', '#page-about { background: #f5f5f5;') # If it exists
# Or just add a style rule
css_addition = """
    #page-about { background: #f7f9fb; }
    .profile-section-card {
      background: #ffffff;
      margin: 16px;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.06);
      border: 1px solid rgba(0,0,0,0.08);
      overflow: hidden;
    }
    .profile-section-header {
      background: #fbfbfb;
      padding: 12px 16px;
      font-size: 14px;
      font-weight: 800;
      color: var(--navy);
      border-bottom: 1px solid rgba(0,0,0,0.05);
    }
"""
# Insert this CSS.
style_end = content.find('</style>')
if style_end != -1:
    content = content[:style_end] + css_addition + content[style_end:]

# 3. Fix Media Query for Mobile Background
# Ensure body is white on mobile.
content = re.sub(r'html,\\s*body\\s*\{\\s*height: 100%;\\s*background: #ffffff;', 'html, body { height: 100%; background: #ffffff !important;', content)
# Ensure the grey surround media query works
content = content.replace('@media (min-width: 500px)', '@media (min-width: 501px)')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Final cleanup complete.")
