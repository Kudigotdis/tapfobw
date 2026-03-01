import json
import os

def convert():
    json_path = r'C:\Users\Kudzanai\Documents\2025\App Developments\TapFo\data\botswana_events_2026.json'
    js_path = r'C:\Users\Kudzanai\Documents\2025\App Developments\TapFo\data\botswana_events_2026.js'
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write("window.BOTSWANA_EVENTS_2026 = ")
            json.dump(data, f, indent=2)
            f.write(";")
        
        print(f"Successfully converted {json_path} to {js_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    convert()
