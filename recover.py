import os
import re

file_path = r'c:\Users\Kudzanai\Documents\2025\App Developments\TapFo\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Identify key points
# Search cursor wrap start
search_start = content.find('<div class="search-cursor-wrap">')
# Trapezoid start
trap_start = content.find('<div class="ql-trapezoid"')
# About start
about_start = content.find('<div class="page" id="page-about">')
# End markers at the bottom
end_body_marker = '</div><!-- end #body-level -->' # Note: I may have broken this in the diff
if end_body_marker not in content:
    end_body_marker = '<!-- end #body-level -->'

# We will reconstruct everything from About start to the end.
# But first, fix the search cursor wrap.
prefix = content[:about_start]
# The search cursor wrap was missing its </div>
if '<div class="search-cursor-wrap">' in prefix:
    # Find the end of the search overlay and add its closing div + search wrap closing div
    # Actually, I'll just search for where the search block ends before Quick Links.
    ql_comment = '<!-- ══ QUICK LINKS'
    idx_ql_comment = prefix.find(ql_comment)
    if idx_ql_comment != -1:
        # Reconstruct the search part to be safe
        search_block = prefix[search_start:idx_ql_comment]
        # Ensure it has exactly two closing </div>s before the comment
        # We'll just replace the whole prefix part from search_start to idx_ql_comment
        pass

# Fixed Blocks
about_block = """          <div class="page" id="page-about">
            <div class="top-bar">
              <button class="back-btn" onclick="goBack()">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="var(--navy)">
                  <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
                </svg>
              </button>
              <span class="top-brand">About TapFo</span>
              <span></span>
            </div>
            <div class="body-scroll">
              <div style="padding:24px 16px;">
                <div class="logo-circle"
                  style="margin:0 auto 20px;width:120px;height:120px;background:var(--navy);border-radius:50%;">
                  <img src="assets/icons/TapFo_Logo_White.png" alt="TapFo Logo" style="width:80px; height:80px;">
                </div>
                <h2 style="text-align:center;color:var(--navy);font-size:24px;margin-bottom:8px;">TapFo.bw</h2>
                <p style="text-align:center;color:var(--grey-text);font-size:14px;margin-bottom:24px;">Version 1.01.267
                </p>

                <div class="profile-section-card">
                  <div class="profile-section-header">Our Mission</div>
                  <div style="padding:16px;font-size:15px;color:var(--body-text);line-height:1.7;">
                    TapFo is Botswana's offline-first business directory and community platform. We believe every business
                    — no matter how small — deserves to be found, trusted, and connected to the community it serves. TapFo
                    everything.
                  </div>
                </div>

                <div class="profile-section-card">
                  <div class="profile-section-header">What We Do</div>
                  <div style="padding:16px;">
                    <div style="margin-bottom:14px;">
                      <div style="font-size:15px;font-weight:700;color:var(--dark-text);margin-bottom:4px;">📂 Business
                        Directory</div>
                      <div style="font-size:14px;color:var(--body-text);">Find businesses in your neighbourhood — works
                        offline.</div>
                    </div>
                    <div style="margin-bottom:14px;">
                      <div style="font-size:15px;font-weight:700;color:var(--dark-text);margin-bottom:4px;">📣 Weekly
                        Promos</div>
                      <div style="font-size:14px;color:var(--body-text);">Browse promotional content from local businesses.
                      </div>
                    </div>
                    <div style="margin-bottom:14px;">
                      <div style="font-size:15px;font-weight:700;color:var(--dark-text);margin-bottom:4px;">⭐ Trusted</div>
                      <div style="font-size:14px;color:var(--body-text);">Build your personal list of trusted local
                        businesses.</div>
                    </div>
                    <div>
                      <div style="font-size:15px;font-weight:700;color:var(--dark-text);margin-bottom:4px;">📝 Notes & Items
                      </div>
                      <div style="font-size:14px;color:var(--body-text);">Save and track products, services and price
                        information.</div>
                    </div>
                  </div>
                </div>

                <div style="text-align:center;margin-top:24px;padding-bottom:24px;">
                  <div style="font-size:14px;color:var(--grey-text);">© 2026 TapFo.bw · All rights reserved</div>
                  <div style="font-size:14px;color:var(--grey-text);margin-top:4px;">Made with ❤️ for Botswana</div>
                </div>
              </div>
            </div>
            <nav class="bottom-nav">
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
            </nav>
          </div>
"""

howto_block = """
          <!-- ══════════════════════════════════════
     HOW TO USE PAGE
══════════════════════════════════════ -->
          <div class="page" id="page-howto">
            <div class="top-bar">
              <button class="back-btn" onclick="goBack()">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="var(--navy)">
                  <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
                </svg>
              </button>
              <span class="top-brand">How To Use</span>
              <span></span>
            </div>
            <div class="body-scroll">
              <div style="padding:16px;">
                <div id="howto-list"></div>
              </div>
            </div>
            <nav class="bottom-nav">
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
            </nav>
          </div>
"""

menu_block = """
          <!-- ══════════════════════════════════════
     MAIN MENU OVERLAY
══════════════════════════════════════ -->
          <div id="overlay-menu">
            <div class="menu-header" onclick="closeMenu();showPage('profile')" style="cursor:pointer;">
              <div class="menu-avatar"
                style="width:70px; height:70px; border-radius:50%; background:var(--white); display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:28px; font-weight:700; color:var(--navy);">
                ?</div>
              <div class="menu-header-text">
                <div class="menu-profile-name"
                  style="color:var(--white); font-size:20px; font-weight:700; margin-bottom:2px;">Your Profile</div>
                <div class="menu-profile-handle" style="color:rgba(255,255,255,0.6); font-size:14px;">@handle</div>
                <div
                  style="margin-top:8px; font-size:11px; color:rgba(255,255,255,0.4); text-transform:uppercase; letter-spacing:0.05em;">
                  View Wallet & Caps</div>
              </div>
            </div>

            <div class="menu-body">
              <div class="menu-label-row">
                <div class="menu-label-icon">
                  <span style="background:var(--grey-text);"></span>
                  <span style="background:var(--grey-text);"></span>
                  <span style="background:var(--grey-text);"></span>
                </div>
                <span class="menu-label-text">Menu</span>
              </div>
              <div class="menu-divider"></div>

              <div class="menu-items">
                <button class="menu-item" onclick="closeMenu();showPage('profile')">
                  <div class="menu-item-circle" style="background:#0d1b2a;">
                    <svg viewBox="0 0 24 24">
                      <path
                        d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" />
                    </svg>
                  </div>
                  <span class="menu-item-label">Profile</span>
                </button>

                <button class="menu-item" onclick="closeMenu();showPage('accounts')">
                  <div class="menu-item-circle" style="background:#0d1b2a;">
                    <svg viewBox="0 0 24 24">
                      <path
                        d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" />
                    </svg>
                  </div>
                  <span class="menu-item-label">Accounts</span>
                </button>

                <button class="menu-item" onclick="closeMenu();showPage('sums')">
                  <div class="menu-item-circle" style="background:#0d1b2a;">
                    <svg viewBox="0 0 24 24">
                      <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
                    </svg>
                  </div>
                  <span class="menu-item-label">Sums</span>
                </button>

                <button class="menu-item" onclick="closeMenu();showPage('trusted')">
                  <div class="menu-item-circle" style="background:#0d1b2a;">
                    <svg viewBox="0 0 24 24">
                      <path
                        d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
                    </svg>
                  </div>
                  <span class="menu-item-label">Trusted</span>
                </button>

                <button class="menu-item" onclick="closeMenu();showPage('history')">
                  <div class="menu-item-circle" style="background:#0d1b2a;">
                    <svg viewBox="0 0 24 24">
                      <path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z" />
                    </svg>
                  </div>
                  <span class="menu-item-label">History</span>
                </button>

                <button class="menu-item" onclick="closeMenu();showPage('howto')">
                  <div class="menu-item-circle" style="background:#0d1b2a;">
                    <svg viewBox="0 0 24 24">
                      <path d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.25 3-5 3-5 0-2.21-1.79-4-4-4z" />
                    </svg>
                  </div>
                  <span class="menu-item-label">How To Use</span>
                </button>
              </div>
            </div>

            <div class="menu-footer">
              <button class="menu-version-btn" onclick="closeMenu();showPage('changelog')">Version 1.01.267</button>
              <span class="menu-footer-text">© 2026 TapFo.bw</span>
            </div>

            <nav class="bottom-nav menu-bottom-nav">
              <button class="menu-btn" onclick="closeMenu()">
                <img src="assets/icons/Menu_Button_White.png" alt="Close Menu" style="width:24px; height:24px;">
              </button>
              <div class="nav-links" style="color:var(--white);">
                <button class="nav-link" onclick="closeMenu();navigateToPage('home')">Directory</button>
                <span class="nav-dot">●</span>
                <button class="nav-link" onclick="closeMenu();navigateToPage('promos')">Promos</button>
                <span class="nav-dot">●</span>
                <button class="nav-link" onclick="closeMenu();navigateToPage('events')">Events</button>
              </div>
              <div class="nav-spacer"></div>
              <button class="list-biz-btn" onclick="showToast('List Business coming soon!')">List Business</button>
            </nav>
          </div>
"""

# Extract the rest of the file correctly
# Everything from Quick Links onwards is nested. 
# We'll extract each page by its ID and clean it up.

def extract_page(html, page_id):
    start_tag = f'<div class="page" id="{page_id}">'
    if page_id == 'toast': start_tag = '<div class="toast" id="toast"></div>'
    if page_id == 'profile-drawer': start_tag = '<div class="profile-drawer-overlay"'
    
    start_idx = html.find(start_tag)
    if start_idx == -1: return ""
    
    # Take from start_idx to the next major page or script tag
    # This is rough but should work for extraction.
    markers = ['<div class="page"', '<div id="overlay-menu"', '<div class="toast"', '<div class="profile-drawer-overlay"', '<script>', '</body>']
    end_idx = len(html)
    for m in markers:
        m_idx = html.find(m, start_idx + len(start_tag))
        if m_idx != -1 and m_idx < end_idx:
            end_idx = m_idx
            
    content = html[start_idx:end_idx].strip()
    # Remove extra levels of indentation (regex for leading spaces > 10)
    lines = content.split('\\n')
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(re.sub(r'^ {12,}', '          ', line))
    return '\\n'.join(cleaned_lines)

ql_content = extract_page(content, 'page-quicklinks')
trusted_content = extract_page(content, 'page-trusted')
sums_content = extract_page(content, 'page-sums')
items_content = extract_page(content, 'page-items')
history_content = extract_page(content, 'page-history')
wonda_content = extract_page(content, 'page-wonda')
accounts_content = extract_page(content, 'page-accounts')
toast_content = extract_page(content, 'toast')
drawer_content = extract_page(content, 'profile-drawer')

# Scripts part
script_start = content.find('<script>')
script_content = content[script_start:]

# FINAL RECONSTRUCTION
final_html = content[:about_start]
# Fix the search overlap closing tags in the prefix if needed
# (Assuming it's okay for now, we'll fix later if not)

final_html += about_block
final_html += howto_block
final_html += menu_block
final_html += "\\n          " + ql_content + "\\n"
final_html += "\\n          " + trusted_content + "\\n"
final_html += "\\n          " + sums_content + "\\n"
final_html += "\\n          " + items_content + "\\n"
final_html += "\\n          " + history_content + "\\n"
final_html += "\\n          " + wonda_content + "\\n"
final_html += "\\n          " + accounts_content + "\\n"
final_html += "\\n          " + toast_content + "\\n"
final_html += "\\n          " + drawer_content + "\\n"

# Re-add the closing tags for app and app-shell which were nested out
final_html += "\\n        </div><!-- end #body-level -->\\n      </div><!-- end #app -->\\n    </div><!-- end #app-shell -->\\n"

final_html += script_content

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Recovery complete.")
