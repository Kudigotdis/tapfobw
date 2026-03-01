import re
import json
import ast
import os

def extract_json_from_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    extracted_data = []
    
    # 1. Look for JSON blocks
    json_pattern = re.compile(r'```json\s*(.*?)\s*```', re.DOTALL)
    json_blocks = json_pattern.findall(content)
    for block in json_blocks:
        try:
            data = json.loads(block)
            if isinstance(data, list): extracted_data.extend(data)
            elif isinstance(data, dict): extracted_data.append(data)
        except: pass

    # 2. Look for Javascript blocks (tourism format)
    js_pattern = re.compile(r'```javascript\s*(.*?)\s*```', re.DOTALL)
    js_blocks = js_pattern.findall(content)
    for block in js_blocks:
        # Normalize: find the array part [...]
        start_idx = block.find('[')
        end_idx = block.rfind(']')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            data_str = block[start_idx:end_idx+1]
            # Basic cleanup: remove comments and fix keys
            data_str = re.sub(r'//.*', '', data_str)
            data_str = re.sub(r'(\w+):', r'"\1":', data_str)
            try:
                data = json.loads(data_str)
                if isinstance(data, list): extracted_data.extend(data)
            except: pass
            
    return extracted_data

def normalize_event(e):
    # Support both Tourism and Soccer schemas
    name = e.get('event_name') or e.get('eventName') or e.get('name')
    date = e.get('start_date') or e.get('date') or (e.get('dates', {}).get('startDate') if isinstance(e.get('dates'), dict) else None)
    venue = e.get('venue_name') or e.get('venue') or (e.get('venue', {}).get('primary') if isinstance(e.get('venue'), dict) else None)
    cat = e.get('botswana_tourism_category') or e.get('category') or e.get('activityType') or e.get('mizano_category')
    desc = e.get('description') or e.get('tagline') or e.get('desc')
    featured = e.get('featured', False)
    
    if not name or not date: return None
    
    # Simple date normalization
    date_str = str(date).split('T')[0]
    
    return {
        "name": name,
        "date": date_str,
        "venue": venue,
        "category": cat,
        "description": desc,
        "featured": featured
    }

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = [
        os.path.join(root_dir, 'ORDER THESE', 'BOTSWANA_2026_EVENTS_DATABASE.md'),
        os.path.join(root_dir, 'ORDER THESE', 'TAPFO_EVENTS_DATABASE_2026.md')
    ]
    
    all_events = []
    for f in files:
        if os.path.exists(f):
            all_events.extend(extract_json_from_md(f))
    
    # Normalize and deduplicate (by name and date)
    normalized_events = []
    seen = set()
    for e in all_events:
        norm = normalize_event(e)
        if norm:
            key = f"{norm['name']}_{norm['date']}"
            if key not in seen:
                normalized_events.append(norm)
                seen.add(key)

    # Organize Month-wise for data/ JS output
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    events_by_month = {m: [] for m in months}
    
    count = 0
    for e in normalized_events:
        try:
            month_match = re.search(r'-(\d{2})-', e['date'])
            if month_match:
                month_idx = int(month_match.group(1)) - 1
                if 0 <= month_idx < 12:
                    events_by_month[months[month_idx]].append(e)
                    count += 1
        except: continue

    # Outputs
    outputs = [
        (os.path.join(root_dir, 'data', 'events_2026.json'), json.dumps(events_by_month, indent=2)),
        (os.path.join(root_dir, 'data', 'events_2026.js'), f"window.EVENTS_DATA_2026 = {json.dumps(events_by_month, indent=2)};"),
        (os.path.join(root_dir, 'events_manifest.json'), json.dumps(normalized_events, indent=2))
    ]

    for path, content in outputs:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {path}")

    print(f"Successfully processed {count} unique events.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
