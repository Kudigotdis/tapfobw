import json
import re
import os

def parse_tourism_events(content):
    events = []
    # Find all javascript arrays of events like const JANUARY_2026_EVENTS = [...];
    # We'll use a regex to find the blocks and then try to parse them.
    # Actually, since it's MD with JS code blocks, we can look for ```javascript sections.
    
    blocks = re.findall(r'```javascript\s*(.*?)\s*```', content, re.DOTALL)
    for block in blocks:
        if '_2026_EVENTS = [' in block:
            # Clean up the block to make it valid JSON
            # Remove "const NAME = " and ";"
            json_text = re.sub(r'const\s+\w+\s*=\s*', '', block)
            json_text = json_text.strip().rstrip(';')
            
            # Fix keys (add quotes) and remove comments
            json_text = re.sub(r'//.*', '', json_text)
            # This is a bit risky for complex JS objects, but since they are simple:
            # Add quotes to keys
            json_text = re.sub(r'(\w+):', r'"\1":', json_text)
            
            try:
                data = json.loads(json_text)
                if isinstance(data, list):
                    for item in data:
                        # Normalize keys to event_name, start_date, category, village_town, etc.
                        normalized = {
                            "id": item.get("event_id"),
                            "name": item.get("event_name"),
                            "date": item.get("start_date"),
                            "end_date": item.get("end_date"),
                            "venue": item.get("venue_name"),
                            "location": item.get("village_town") or item.get("district"),
                            "category": item.get("botswana_tourism_category"),
                            "mizano_cat": item.get("mizano_category"),
                            "desc": item.get("description"),
                            "type": "tourism",
                            "featured": item.get("featured", False)
                        }
                        events.append(normalized)
            except Exception as e:
                print(f"Error parsing tourism block: {e}")
                
    return events

def parse_soccer_events(content):
    events = []
    # Soccer MD has blocks for individual events and a compact list
    blocks = re.findall(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    for block in blocks:
        try:
            data = json.loads(block)
            if isinstance(data, dict) and "eventID" in data:
                # Individual event
                normalized = {
                    "id": data.get("eventID"),
                    "name": data.get("eventName"),
                    "date": data.get("dates", {}).get("startDate"),
                    "end_date": data.get("dates", {}).get("endDate"),
                    "venue": data.get("venue", {}).get("primary"),
                    "location": data.get("region"),
                    "category": "Sports",
                    "mizano_cat": "sports",
                    "desc": data.get("tagline"),
                    "type": "soccer",
                    "featured": data.get("mizanoIntegration", {}).get("activityState") == "active_now"
                }
                events.append(normalized)
            elif isinstance(data, list):
                # Compact list
                for item in data:
                    if "eventID" in item:
                        # Some list items have dates as a string "2026-04-04/19"
                        date_raw = item.get("dates", "")
                        start_date = date_raw.split('/')[0] if '/' in date_raw else date_raw
                        
                        normalized = {
                            "id": item.get("eventID"),
                            "name": item.get("eventName"),
                            "date": start_date,
                            "end_date": None, # Complex to parse all variants
                            "venue": item.get("region"),
                            "location": item.get("region"),
                            "category": "Sports",
                            "mizano_cat": "sports",
                            "desc": f"Sponsored by {item.get('sponsor')}",
                            "type": "soccer",
                            "featured": False
                        }
                        events.append(normalized)
        except Exception as e:
            pass # Skip non-event JSON or malformed blocks

    return events

def main():
    tourism_path = r'c:\Users\Kudzanai\Documents\2025\App Developments\TapFo\ORDER THESE\BOTSWANA_2026_EVENTS_DATABASE.md'
    soccer_path = r'c:\Users\Kudzanai\Documents\2025\App Developments\TapFo\ORDER THESE\TAPFO_EVENTS_DATABASE_2026.md'
    
    all_events = []
    
    if os.path.exists(tourism_path):
        with open(tourism_path, 'r', encoding='utf-8') as f:
            all_events.extend(parse_tourism_events(f.read()))
            
    if os.path.exists(soccer_path):
        with open(soccer_path, 'r', encoding='utf-8') as f:
            all_events.extend(parse_soccer_events(f.read()))
            
    # Sort by date
    all_events.sort(key=lambda x: x['date'] if x['date'] else '9999-99-99')
    
    output_path = r'c:\Users\Kudzanai\Documents\2025\App Developments\TapFo\events_manifest.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_events, f, indent=2)
        
    print(f"Generated events manifest with {len(all_events)} items.")

if __name__ == "__main__":
    main()
