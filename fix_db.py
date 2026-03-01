import json
import os

def fix_business_db():
    src = 'data/TapFo_Business_Database_V1.json'
    dst_json = 'data/TapFo_Business_Database_V1_Fixed.json'
    dst_js = 'data/TapFo_Business_Database_V1.js'
    
    if not os.path.exists(src):
        print(f"Source file {src} not found.")
        return

    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()

    objs = []
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(content):
        # Skip whitespace
        while pos < len(content) and content[pos].isspace():
            pos += 1
        if pos >= len(content):
            break
        try:
            obj, skip = decoder.raw_decode(content[pos:])
            objs.append(obj)
            pos += skip
        except json.JSONDecodeError as e:
            print(f"JSON decode error at position {pos + e.pos}: {e.msg}")
            break

    if not objs:
        print("No JSON objects found.")
        return

    merged = {
        'metadata': objs[-1].get('metadata', {}),
        'businesses': []
    }
    
    seen_ids = set()
    for obj in objs:
        for biz in obj.get('businesses', []):
            biz_id = biz.get('id')
            if biz_id not in seen_ids:
                merged['businesses'].append(biz)
                seen_ids.add(biz_id)

    # Sort businesses by name for better UX
    merged['businesses'].sort(key=lambda x: x.get('name', '').lower())

    with open(dst_json, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2)
    
    with open(dst_js, 'w', encoding='utf-8') as f:
        f.write(f"const BIZ_DATABASE = {json.dumps(merged)};")

    print(f"Fixed database saved to {dst_json} and {dst_js}")
    print(f"Total businesses: {len(merged['businesses'])}")

if __name__ == "__main__":
    fix_business_db()
