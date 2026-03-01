import os
import json

def generate_manifest(base_dir):
    manifest = {}
    if not os.path.exists(base_dir):
        print(f"Error: Directory {base_dir} does not exist.")
        return manifest

    for entry in os.scandir(base_dir):
        if entry.is_dir():
            category = entry.name
            images = []
            for file in os.scandir(entry.path):
                if file.is_file() and file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    # Store relative path from the app root
                    # The app will likely load as PROMOS/Category/Filename
                    images.append(f"PROMOS/{category}/{file.name}")
            manifest[category] = images
    return manifest

def main():
    base_dir = r"C:\Users\Kudzanai\Documents\2025\App Developments\TapFo\PROMOS"
    output_path = r"C:\Users\Kudzanai\Documents\2025\App Developments\TapFo\data\promos_manifest.json"
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    manifest = generate_manifest(base_dir)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Successfully generated promo manifest with {len(manifest)} categories at {output_path}")

if __name__ == "__main__":
    main()
