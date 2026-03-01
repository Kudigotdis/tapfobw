import json
import os

def merge_events():
    base_dir = r'C:\Users\Kudzanai\Documents\2025\App Developments\TapFo\data'
    file1 = os.path.join(base_dir, 'events_2026.json')
    file2 = os.path.join(base_dir, 'botswana_events_2026.json')
    output_json = os.path.join(base_dir, 'botswana_events_2026.json') # Overwrite with merged
    output_js = os.path.join(base_dir, 'botswana_events_2026.js')

    months_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    
    # Structure of merged will follow botswana_events_2026.json format
    merged_data = {
        "database_meta": {
            "version": "1.1",
            "name": "Merged Botswana 2026 Events",
            "description": "Unified events database with duplicates removed",
            "last_updated": "2026-02-25T01:30:00Z"
        },
        "events_by_month": {m: {"events": []} for m in months_list}
    }

    seen_events = set() # (name.lower(), date)

    def process_file(filepath):
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found.")
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle different structures
        if "events_by_month" in data:
            # Format: botswana_events_2026.json
            for month, content in data["events_by_month"].items():
                m_key = month.lower()
                if m_key in merged_data["events_by_month"]:
                    for e in content.get("events", []):
                        name = (e.get("event_name") or e.get("name", "")).strip()
                        date = e.get("start_date") or e.get("date", "")
                        key = (name.lower(), date)
                        if key not in seen_events:
                            # Normalize field names for the UI to be consistent
                            normalized = e.copy()
                            normalized["name"] = name
                            normalized["date"] = date
                            merged_data["events_by_month"][m_key]["events"].append(normalized)
                            seen_events.add(key)
        else:
            # Format: events_2026.json (Month keys with list of events)
            for month, events in data.items():
                m_key = month.lower()
                if m_key in merged_data["events_by_month"]:
                    for e in events:
                        name = (e.get("name") or e.get("event_name", "")).strip()
                        date = (e.get("date") or e.get("start_date", "")).strip()
                        key = (name.lower(), date)
                        if key not in seen_events:
                            normalized = e.copy()
                            normalized["name"] = name
                            normalized["date"] = date
                            merged_data["events_by_month"][m_key]["events"].append(normalized)
                            seen_events.add(key)

    # Process files (file2 first as it has more detail)
    process_file(file2)
    process_file(file1)

    # Sort events in each month by date
    for m in months_list:
        merged_data["events_by_month"][m]["events"].sort(key=lambda x: x.get("start_date", "9999-99-99"))

    # Save output
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2)

    with open(output_js, 'w', encoding='utf-8') as f:
        f.write(f"window.BOTSWANA_EVENTS_2026 = {json.dumps(merged_data, indent=2)};")

    print(f"Merge complete. Total unique events: {len(seen_events)}")

if __name__ == "__main__":
    merge_events()
