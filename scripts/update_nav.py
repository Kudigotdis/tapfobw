import re

def update_index_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the new bottom nav structure
    new_nav = '''<nav class="bottom-nav">
          <button class="menu-btn" onclick="openMenu()">
            <img src="assets/icons/Menu_Button_grey.png" alt="Menu" style="width:24px; height:24px;">
          </button>
          <div class="nav-links">
            <button class="nav-link" id="nav-directory" onclick="navigateToPage('home')">Directory</button>
            <span class="nav-dot">●</span>
            <button class="nav-link" id="nav-promos" onclick="navigateToPage('promos')">Promos</button>
          </div>
          <div class="nav-spacer"></div>
          <button class="engage-btn" onclick="showToast('Engage feature coming soon!')">Engage</button>
        </nav>'''

    # Pattern to match any <nav class="bottom-nav">...</nav> block
    # This handles different white-space and internal content
    pattern = re.compile(r'<nav class="bottom-nav">.*?</nav>', re.DOTALL)
    
    # We want to replace all occurrences.
    # Note: Some might already be updated, but replacing them with the exact same content is fine.
    updated_content = pattern.sub(new_nav, content)

    # Also remove the standalone events page div
    # Pattern for <div class="page" id="page-events" ...> until the next closing page div or similar
    # Actually, it's safer to target the specific block if possible.
    event_page_pattern = re.compile(r'<!-- Page: Events -->.*?<div class="page" id="page-events".*?</div>', re.DOTALL)
    # The events page has a lot of internal divs, so the non-greedy .*? might stop at the first </div>.
    # I'll look for the specific structure I saw earlier.
    
    # Let's try to remove it by its ID and surrounding markers.
    # The Events page was followed by Location Filter page usually.
    
    # Safer way to remove the events page:
    # It starts with <!-- Page: Events --> and ends before <!-- ══════════════ LOCATION FILTER PAGE ══════════════ -->
    parts = re.split(r'<!-- Page: Events -->', updated_content)
    if len(parts) > 1:
        # parts[1] contains the events page and everything after it.
        # Find the next major section start.
        sub_parts = re.split(r'<!-- ══════════════════════════════════════\s+LOCATION FILTER PAGE', parts[1])
        if len(sub_parts) > 1:
            updated_content = parts[0] + '<!-- ══════════════════════════════════════\n     LOCATION FILTER PAGE' + sub_parts[1]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"Successfully updated bottom navigation and removed events page in {filepath}")

if __name__ == "__main__":
    update_index_html(r'C:\Users\Kudzanai\Documents\2025\App Developments\TapFo\index.html')
