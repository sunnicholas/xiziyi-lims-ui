
import os

def generate_file(filename, ranges, active_menu):
    with open('preview-env/preview_v2.html', 'r') as f:
        lines = f.readlines()
    
    content = []
    for start, end in ranges:
        # Convert 1-based to 0-based
        # start is inclusive, end is inclusive
        content.extend(lines[start-1:end])
    
    # Update script
    new_content = "".join(content)
    
    # Update handleMenuSelect
    old_js = """        handleMenuSelect(index) {
          if (index.indexOf('record') === -1 && index.indexOf('report') === -1) {
             this.activeMenu = index;
          } else if (index === 'record-list' || index === 'report-list') {
             this.activeMenu = index;
          }
        },"""
    new_js = """        handleMenuSelect(index) {
          const map = {
            'business': 'preview_business.html',
            'assign': 'preview_assign.html',
            'record-list': 'preview_record.html',
            'audit': 'preview_audit.html',
            'report-list': 'preview_report.html'
          };
          if (map[index]) {
            window.location.href = map[index];
          }
        },"""
    
    new_content = new_content.replace(old_js, new_js)
    
    # Update activeMenu
    new_content = new_content.replace("activeMenu: 'business',", f"activeMenu: '{active_menu}',")
    
    with open(f'preview-env/{filename}', 'w') as f:
        f.write(new_content)
    print(f"Generated {filename}")

# Define ranges (1-based inclusive)
# 1-200: Header
# 201-270: Business Page
# 271-592: Assign Page
# 593-762: Record List
# 763-973: Record Entry
# 974-1073: Audit
# 1074-1230: Report
# 1233-1685: Dialogs 1-3 (Business)
# 1689-1840: Dialogs 4-5 (Assign/Track)
# 1842-End: Script

# Note: I am skipping the wrapper lines: 1231-1232, 1686-1688, 1841.
# Wait, 1231 is empty/comment? 1232 is template.
# 1686 is /template. 1687 is empty. 1688 is template.
# 1841 is /template.
# So keeping 1233-1685 and 1689-1840 effectively removes wrappers.

generate_file('preview_business.html', [
    (1, 270),
    (1229, 1230),
    (1233, 1685),
    (1689, 1840),
    (1842, 2759) # assuming file length
], 'business')

generate_file('preview_assign.html', [
    (1, 200),
    (271, 592),
    (1229, 1230),
    (1689, 1840),
    (1842, 2759)
], 'assign')

generate_file('preview_record.html', [
    (1, 200),
    (593, 973),
    (1229, 1230),
    (1842, 2759)
], 'record-list')

generate_file('preview_audit.html', [
    (1, 200),
    (974, 1073),
    (1229, 1230),
    (1842, 2759)
], 'audit')

generate_file('preview_report.html', [
    (1, 200),
    (1074, 1230),
    (1842, 2759)
], 'report-list')
