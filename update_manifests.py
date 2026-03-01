import os
import json

def update_manifests():
    base_dir = "."
    promos_dir = os.path.join(base_dir, "PROMOS")
    mediums_dir = os.path.join(base_dir, "MEDIUMS")
    data_dir = os.path.join(base_dir, "data")
    
    # Supported extensions
    supported_exts = {'.webp', '.gif', '.jpg', '.jpeg', '.png', '.mp4', '.mp3', '.html'}
    
    def process_dir(source_dir, output_name):
        manifest = {}
        if not os.path.exists(source_dir):
            print(f"Error: {source_dir} does not exist.")
            return

        # Walk through the directory
        for category in os.listdir(source_dir):
            cat_path = os.path.join(source_dir, category)
            if os.path.isdir(cat_path):
                files = []
                for f in os.listdir(cat_path):
                    if any(f.lower().endswith(ext) for ext in supported_exts):
                        # Use relative path for web consumption
                        # Ensure web-safe paths (forward slashes)
                        rel_path = f"{os.path.basename(source_dir)}/{category}/{f}".replace('\\', '/')
                        files.append(rel_path)
                
                if files:
                    manifest[category] = sorted(files)

        # Save as JSON
        json_path = os.path.join(data_dir, f"{output_name}_manifest.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        print(f"Updated {json_path} with {len(manifest)} categories.")

        # Save as JS for fallback
        js_path = os.path.join(data_dir, f"{output_name}_manifest.js")
        with open(js_path, 'w', encoding='utf-8') as f:
            js_var = f"{output_name.upper()}_DATA"
            f.write(f"const {js_var} = {json.dumps(manifest, indent=2)};")
        print(f"Updated {js_path}")

    process_dir(promos_dir, "promos")
    process_dir(mediums_dir, "mediums")

if __name__ == "__main__":
    update_manifests()
