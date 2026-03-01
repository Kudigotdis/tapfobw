import os
import json
import shutil

# Mapping prefix to folder name and main category
MAPPING = {
    "AccommProp": "Accommodation_Property",
    "Agric": "Agriculture",
    "Auto": "Automotive",
    "BabiesKids": "Babies_Kids",
    "BeautyGroom": "Beauty_Grooming",
    "BevLiquor": "Beverage_Liquor",
    "BizOffice": "Business_Office",
    "BooksPub": "Books_Publishing",
    "CargoDelivery": "Cargo_Delivery",
    "Clothing": "Clothing",
    "ClubsGroups": "Clubs_Groups",
    "Construct": "Building_Construction",
    "Crafts": "Crafts",
    "Cultural": "Cultural",
    "EduSchool": "Education_School",
    "Electro": "Electronics",
    "Embassy": "Embassy",
    "Events": "Events",
    "FabricTextile": "Fabric_Textile",
    "Fashion": "Fashion",
    "FastFood": "Fast_Food",
    "Film": "Film",
    "Finance": "Finance",
    "FuelTrans": "Fuel_Transport",
    "Gaming": "Gaming",
    "Groceries": "Groceries",
    "HealthMed": "Health_Medical",
    "HomeDecor": "Home_Decor",
    "Jobs": "Jobs",
    "MobileNet": "Mobile_Network",
    "Music": "Music",
    "PodcastsTV": "Podcasts_TV",
    "Resto": "Restaurant",
    "Security": "Security",
    "Sports": "Sports",
    "Tourism": "Tourism",
    "Transport": "Transport"
}

CATEGORY_NAMES = {
    "Accommodation_Property": "Accommodation & Property",
    "Agriculture": "Agriculture",
    "Automotive": "Automotive",
    "Babies_Kids": "Babies & Kids",
    "Beauty_Grooming": "Beauty & Grooming",
    "Beverage_Liquor": "Beverage & Liquor",
    "Business_Office": "Business & Office",
    "Books_Publishing": "Books & Publishing",
    "Cargo_Delivery": "Cargo & Delivery",
    "Clothing": "Clothing",
    "Clubs_Groups": "Clubs & Groups",
    "Building_Construction": "Building & Construction",
    "Crafts": "Crafts",
    "Cultural": "Cultural",
    "Education_School": "Education & School",
    "Electronics": "Electronics",
    "Embassy": "Embassy",
    "Events": "Events",
    "Fabric_Textile": "Fabric & Textile",
    "Fashion": "Fashion",
    "Fast_Food": "Fast Food",
    "Film": "Film",
    "Finance": "Finance",
    "Fuel_Transport": "Fuel & Transport",
    "Gaming": "Gaming",
    "Groceries": "Groceries",
    "Health_Medical": "Health & Medical",
    "Home_Decor": "Home & Decor",
    "Jobs": "Jobs",
    "Mobile_Network": "Mobile & Network",
    "Music": "Music",
    "Podcasts_TV": "Podcasts & TV",
    "Restaurant": "Restaurant",
    "Security": "Security",
    "Sports": "Sports",
    "Tourism": "Tourism",
    "Transport": "Transport"
}

PROMOS_DIR = "PROMOS"
MANIFEST_FILE = "campaigns_manifest.json"

def reorganize():
    # 1. Create subfolders
    for folder in MAPPING.values():
        os.makedirs(os.path.join(PROMOS_DIR, folder), exist_ok=True)
    
    os.makedirs(os.path.join(PROMOS_DIR, "Gaborone"), exist_ok=True)

    manifest = []

    # 2. Iterate and move files
    for filename in os.listdir(PROMOS_DIR):
        if not filename.startswith("TapFo_"):
            continue
            
        file_path = os.path.join(PROMOS_DIR, filename)
        if os.path.isdir(file_path):
            continue

        # Extract info from filename: TapFo_AccommProp2_DecWk1.jpg
        parts = filename.split("_")
        if len(parts) < 3:
            continue
            
        # Prefix part might contain the number: AccommProp2
        prefix_full = parts[1]
        # Separate name from number
        prefix_name = ""
        for char in prefix_full:
            if char.isdigit():
                break
            prefix_name += char
            
        time_part = parts[2].split(".")[0] # DecWk1
        month = time_part[:3] # Dec
        week = time_part[3:] # Wk1
        
        folder = MAPPING.get(prefix_name, "Other")
        if folder == "Other":
            os.makedirs(os.path.join(PROMOS_DIR, "Other"), exist_ok=True)

        target_path = os.path.join(PROMOS_DIR, folder, filename)
        shutil.move(file_path, target_path)
        
        # Build manifest entry
        entry = {
            "campaign_id": filename.split(".")[0],
            "asset_filename": filename,
            "asset_path": f"PROMOS/{folder}/{filename}",
            "main_category": CATEGORY_NAMES.get(folder, folder),
            "sub_categories": [CATEGORY_NAMES.get(folder, folder)], # Simplified for now
            "active_week": week,
            "active_month": month,
            "location": ["Botswana"],
            "business_name": "Various Businesses",
            "description": f"Special promotion for {CATEGORY_NAMES.get(folder, folder)} in {month} {week}."
        }
        manifest.append(entry)

    # 3. Handle Gaborone folder
    gab_dir = os.path.join(PROMOS_DIR, "Gaborone")
    if os.path.exists(gab_dir):
        for filename in os.listdir(gab_dir):
            if filename.startswith("TapFo_"):
                # Copy logic from above but with location tag
                parts = filename.split("_")
                if len(parts) < 3: continue
                
                prefix_full = parts[1]
                prefix_name = ""
                for char in prefix_full:
                    if char.isdigit(): break
                    prefix_name += char
                
                time_part = parts[2].split(".")[0]
                month = time_part[:3]
                week = time_part[3:]
                
                folder = MAPPING.get(prefix_name, "Other")
                entry = {
                    "campaign_id": filename.split(".")[0],
                    "asset_filename": filename,
                    "asset_path": f"PROMOS/Gaborone/{filename}",
                    "main_category": CATEGORY_NAMES.get(folder, folder),
                    "sub_categories": [CATEGORY_NAMES.get(folder, folder)],
                    "active_week": week,
                    "active_month": month,
                    "location": ["Gaborone"],
                    "business_name": "Gaborone Local Business",
                    "description": f"Gaborone specific promotion for {CATEGORY_NAMES.get(folder, folder)}."
                }
                manifest.append(entry)

    # 4. Save manifest
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Reorganization complete. {len(manifest)} items logged in {MANIFEST_FILE}")

if __name__ == "__main__":
    reorganize()
