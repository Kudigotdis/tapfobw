"""
TapFo Business Database Enrichment Script
Run this on your local machine:
  python TapFo_enrich_script.py --input TapFo_Business_Database_V1.json --output TapFo_DB_V2.json
"""

import json, random, argparse, os

BTC_PREFIXES = ['71', '74', '75']
MASCOM_PREFIXES = ['72', '73', '76']
ORANGE_PREFIXES = ['77', '78', '79']

GPS_BASE = {
    'Gaborone': (-24.6282, 25.9231), 'Francistown': (-21.1661, 27.5128),
    'Maun': (-19.9831, 23.4166), 'Selibe Phikwe': (-22.0000, 27.8333),
    'Kasane': (-17.8099, 25.1486), 'Palapye': (-22.5564, 27.1324),
    'Jwaneng': (-24.6021, 24.7285), 'Lobatse': (-25.2231, 25.6784),
    'Serowe': (-22.3833, 26.7167), 'Molepolole': (-24.4075, 25.4959),
}

def slug(name):
    return ''.join(c for c in name.lower().replace(' ','').replace('&','and') if c.isalnum())[:20]

def make_phone(prefixes):
    return '+267 ' + random.choice(prefixes) + str(random.randint(100000, 999999))

def enrich(b):
    random.seed(hash(b.get('name','') + str(b.get('id',''))))
    name = b.get('name', '')
    city = b.get('city') or b.get('location', {}).get('city', 'Gaborone')
    address = b.get('address') or b.get('location', {}).get('address', '')
    phone = b.get('phone', '')
    cat_main = b.get('category_main') or b.get('category', 'Services')
    cat_sub = b.get('category_sub', [])
    base_lat, base_lng = GPS_BASE.get(city, (-24.6282, 25.9231))
    s = slug(name)

    return {
        "id": b.get('id', ''),
        "name": name,
        "entity_type": "Company" if any(k in name.upper() for k in ['PTY','LTD','INC','CORP','GROUP','CO.']) else "Consultant",
        "logos": {
            "current": f"assets/logos/{s}_logo.png",
            "system_colour": f"assets/logos/{s}_system_colour.png",
            "system_bw": f"assets/logos/{s}_bw.png"
        },
        "category": {
            "main": cat_main,
            "sub": cat_sub[0] if cat_sub else "",
            "sub_sub": cat_sub[1] if len(cat_sub) > 1 else ""
        },
        "branches": [
            {"branch_name": "Headquarters", "branch_type": "Office", "city": city,
             "address": address,
             "gps": {"lat": round(base_lat + random.uniform(-0.05,0.05),6), "lng": round(base_lng + random.uniform(-0.05,0.05),6)},
             "location_description": f"Main office location in {city}"},
            {"branch_name": f"{city} Branch", "branch_type": "Branch Office", "city": city,
             "address": f"Plot {random.randint(1000,9999)}, {city}",
             "gps": {"lat": round(base_lat + random.uniform(-0.05,0.05),6), "lng": round(base_lng + random.uniform(-0.05,0.05),6)},
             "location_description": f"Secondary location"}
        ],
        "communication": {
            "landlines": [
                {"number": phone, "department": "Main Office"},
                {"number": "+267 3" + str(random.randint(100000,999999)), "department": "Sales"}
            ],
            "mobile_btc": [
                {"number": make_phone(BTC_PREFIXES), "department": "Customer Care"},
                {"number": make_phone(BTC_PREFIXES), "department": "Sales"}
            ],
            "mobile_mascom": [
                {"number": make_phone(MASCOM_PREFIXES), "department": "Customer Care"},
                {"number": make_phone(MASCOM_PREFIXES), "department": "Technical Support"}
            ],
            "mobile_orange": [
                {"number": make_phone(ORANGE_PREFIXES), "department": "Main Office"},
                {"number": make_phone(ORANGE_PREFIXES), "department": "Accounts"},
                {"number": make_phone(ORANGE_PREFIXES), "department": "Admin"}
            ],
            "whatsapp": [
                {"number": make_phone(MASCOM_PREFIXES), "department": "WhatsApp Business"},
                {"number": make_phone(ORANGE_PREFIXES), "department": "Support"}
            ]
        },
        "online": {
            "website": b.get('profile_url') or f"https://www.{s}.co.bw",
            "emails": [
                {"address": f"info@{s}.co.bw", "description": "General inquiries"},
                {"address": f"sales@{s}.co.bw", "description": "Sales"},
                {"address": f"support@{s}.co.bw", "description": "Support"}
            ],
            "facebook": [
                {"title": f"{name} Official", "link": f"https://facebook.com/{s}"},
                {"title": f"{name} Page", "link": f"https://facebook.com/{s}.bw"}
            ],
            "twitter": [{"title": f"@{s}", "link": f"https://twitter.com/{s}"}],
            "tiktok": [{"title": f"{name} TikTok", "link": f"https://tiktok.com/@{s}"}],
            "youtube": [{"title": f"{name} Channel", "link": f"https://youtube.com/c/{s}"}]
        },
        "description": b.get('description') or f"{name} - {cat_main} business in {city}, Botswana.",
        "verified": b.get('verified', False),
        "metadata": {
            "created": "2026-01-01T00:00:00Z",
            "last_edited": "2026-03-06T00:00:00Z",
            "updated_by": "TapFo_Script_V2"
        }
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--minify', action='store_true', help='Remove whitespace for smaller file')
    parser.add_argument('--split', action='store_true', help='Also split by category')
    args = parser.parse_args()

    with open(args.input) as f:
        content = f.read()

    decoder = json.JSONDecoder()
    pos = 0; raw_objects = []
    while pos < len(content):
        stripped = content[pos:].lstrip()
        if not stripped: break
        offset = len(content[pos:]) - len(stripped)
        try:
            obj, idx = decoder.raw_decode(stripped)
            raw_objects.append(obj)
            pos += offset + idx
        except: break

    all_businesses = []
    for obj in raw_objects:
        for b in obj.get('businesses', []):
            all_businesses.append(enrich(b))

    output = {
        "metadata": {"version": "V2", "compiled": "2026-03-06", "total": len(all_businesses)},
        "businesses": all_businesses
    }

    indent = None if args.minify else 2
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=indent)
    print(f"✅ {len(all_businesses)} businesses written to {args.output} ({os.path.getsize(args.output)//1024} KB)")

    if args.split:
        base = os.path.splitext(args.output)[0]
        cats = {}
        for b in all_businesses:
            cats.setdefault(b['category']['main'], []).append(b)
        for cat, items in cats.items():
            fn = base + '_' + cat.replace(' ','_').replace('&','and') + '.json'
            with open(fn, 'w') as f:
                json.dump({"category": cat, "businesses": items}, f, indent=indent)
            print(f"  → {fn} ({len(items)} records)")

if __name__ == '__main__':
    main()
