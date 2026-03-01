import json
import random
import re
from datetime import datetime, timedelta

# ==============================================
# Configuration
# ==============================================
INPUT_FILE = "TapFo_Business_Database_V1.json"   # Path to the input file
OUTPUT_PREFIX = "enriched_businesses"             # Prefix for output files
CHUNK_SIZE = 250
START_OFFSET = 250                                 # Skip first 250 businesses
TOTAL_NEEDED = 784                                 # Number of businesses to process

# Mapping of city to landline prefix (first 2-3 digits) and approximate GPS
CITY_PREFIX = {
    "Gaborone": ("3", {"lat": -24.654, "lng": 25.908}),
    "Francistown": ("2", {"lat": -21.170, "lng": 27.508}),
    "Maun": ("6", {"lat": -19.983, "lng": 23.417}),
    "Palapye": ("4", {"lat": -22.546, "lng": 27.125}),
    "Serowe": ("4", {"lat": -22.387, "lng": 26.711}),
    "Molepolole": ("5", {"lat": -24.407, "lng": 25.495}),
    "Lobatse": ("5", {"lat": -25.219, "lng": 25.677}),
    "Kasane": ("6", {"lat": -17.817, "lng": 25.150}),
    "Jwaneng": ("5", {"lat": -24.601, "lng": 24.728}),
    "Selebi-Phikwe": ("2", {"lat": -21.978, "lng": 27.843}),
    "Kanye": ("5", {"lat": -24.982, "lng": 25.335}),
    "Mochudi": ("3", {"lat": -24.384, "lng": 26.149}),
    "Ramotswa": ("3", {"lat": -24.871, "lng": 25.870}),
    "Ghanzi": ("6", {"lat": -21.697, "lng": 21.646}),
    "Tutume": ("2", {"lat": -20.491, "lng": 27.042}),
    "Bobonong": ("2", {"lat": -21.966, "lng": 28.422}),
    "Tsabong": ("5", {"lat": -26.050, "lng": 22.450}),
    "Orapa": ("2", {"lat": -21.287, "lng": 25.366}),
    "Letlhakane": ("2", {"lat": -21.414, "lng": 25.594}),
    "Mahalapye": ("4", {"lat": -23.104, "lng": 26.814}),
    "Thamaga": ("5", {"lat": -24.720, "lng": 25.537}),
    "Tlokweng": ("3", {"lat": -24.659, "lng": 25.979}),
    "Mogoditshane": ("3", {"lat": -24.627, "lng": 25.870}),
    "Phakalane": ("3", {"lat": -24.564, "lng": 25.932}),
    "Broadhurst": ("3", {"lat": -24.639, "lng": 25.921}),
    "Gaborone West": ("3", {"lat": -24.644, "lng": 25.891}),
    "Riverwalk": ("3", {"lat": -24.651, "lng": 25.903}),
    "Fairgrounds": ("3", {"lat": -24.660, "lng": 25.898}),
    "Kgale View": ("3", {"lat": -24.672, "lng": 25.883}),
    "Tsetsebjwe": ("2", {"lat": -21.744, "lng": 28.139}),
    "Moshupa": ("5", {"lat": -24.780, "lng": 25.419}),
    "Otse": ("5", {"lat": -25.020, "lng": 25.740}),
    "Gabane": ("3", {"lat": -24.666, "lng": 25.782}),
    "Gumare": ("6", {"lat": -19.367, "lng": 22.167}),
    "Nata": ("2", {"lat": -20.215, "lng": 26.187}),
    "Gweta": ("2", {"lat": -20.211, "lng": 25.244}),
    "Kazungula": ("6", {"lat": -17.787, "lng": 25.274}),
    "Pandamatenga": ("6", {"lat": -18.543, "lng": 25.633}),
    "Mmadinare": ("2", {"lat": -21.873, "lng": 27.750}),
    "Tonota": ("2", {"lat": -21.441, "lng": 27.480}),
    "Sowa Town": ("2", {"lat": -20.564, "lng": 26.224}),
    "Goodhope": ("5", {"lat": -25.467, "lng": 25.433}),
    "Mabutsane": ("5", {"lat": -24.483, "lng": 24.983}),
    "Marapong": ("2", {"lat": -21.450, "lng": 27.467}),
    "Mosetse": ("2", {"lat": -20.750, "lng": 26.667}),
    "Sebina": ("2", {"lat": -20.867, "lng": 27.250}),
    "Tuli Block": ("2", {"lat": -22.133, "lng": 29.117}),
    "Okavango Delta": ("6", {"lat": -19.283, "lng": 22.900}),
    "Deception Valley": ("6", {"lat": -21.417, "lng": 23.833}),
    "Central Kalahari Game Reserve": ("6", {"lat": -21.833, "lng": 23.750}),
    "Moremi Game Reserve": ("6", {"lat": -19.250, "lng": 23.500}),
    "Chobe National Park": ("6", {"lat": -18.667, "lng": 24.500}),
    "Makgadikgadi Pans": ("2", {"lat": -20.750, "lng": 25.500}),
    "Kgalagadi": ("5", {"lat": -26.500, "lng": 21.500}),
}

# Default GPS if city not found
DEFAULT_GPS = {"lat": -24.654, "lng": 25.908}

# Categories mapping – based on original category_main or inferred from name
MAIN_CATEGORIES = [
    "Accommodation", "Agriculture", "Automotive", "Construction", "Education",
    "Electronics", "Entertainment", "Finance", "Food", "Furniture & Home",
    "Government", "Health", "Legal", "Media", "Mining", "Retail", "Security",
    "Services", "Technology", "Telecommunications", "Transport"
]

SUB_CATEGORIES = {
    "Accommodation": ["Hotel", "Lodge", "Guest House", "Safari Camp", "Bed & Breakfast"],
    "Agriculture": ["Farming", "Agribusiness", "Livestock", "Crops", "Aquaculture"],
    "Automotive": ["Car Dealership", "Auto Repair", "Parts Supplier", "Panel Beating", "Tyres"],
    "Construction": ["Building Contractor", "Civil Engineering", "Quantity Surveyor", "Architect", "Plant Hire"],
    "Education": ["School", "Training Centre", "University", "Vocational", "Nursery"],
    "Electronics": ["Consumer Electronics", "Repair", "Components", "Audio Visual"],
    "Entertainment": ["Cinema", "Events", "Nightlife", "Sports", "Arts"],
    "Finance": ["Bank", "Insurance", "Investment", "Microfinance", "Accounting"],
    "Food": ["Restaurant", "Butchery", "Bakery", "Catering", "Food Processing"],
    "Furniture & Home": ["Furniture Retail", "Home Decor", "Office Furniture", "Custom Made"],
    "Government": ["Ministry", "Council", "Regulatory Body", "Public Service", "Embassy"],
    "Health": ["Hospital", "Clinic", "Pharmacy", "Laboratory", "Optometry"],
    "Legal": ["Law Firm", "Attorney", "Conveyancing", "Notary", "Legal Aid"],
    "Media": ["Publishing", "Broadcasting", "Advertising", "Photography", "Digital Media"],
    "Mining": ["Diamond Mining", "Quarry", "Mineral Exploration", "Mining Services"],
    "Retail": ["Supermarket", "Clothing Store", "Hardware", "General Dealer", "Wholesaler"],
    "Security": ["Security Guards", "Alarm Systems", "CCTV", "Risk Management", "Cash in Transit"],
    "Services": ["Consulting", "Cleaning", "Logistics", "Recruitment", "Maintenance"],
    "Technology": ["IT Services", "Software", "Telecom", "Networking", "Electronics"],
    "Telecommunications": ["Mobile Network", "ISP", "Telecom Equipment", "Satellite"],
    "Transport": ["Freight", "Courier", "Taxi", "Removals", "Logistics"]
}

SUB_SUB_CATEGORIES = {
    "Car Dealership": ["New Cars", "Used Cars", "Luxury Vehicles"],
    "Auto Repair": ["Mechanical", "Electrical", "Diagnostics"],
    "Parts Supplier": ["Engine Parts", "Brakes", "Suspension"],
    "Panel Beating": ["Spray Painting", "Dent Removal"],
    "Tyres": ["New Tyres", "Retreading", "Wheel Alignment"],
    "Bank": ["Retail Banking", "Corporate Banking", "Treasury"],
    "Insurance": ["Life Insurance", "Short-term Insurance", "Health Insurance"],
    "Investment": ["Asset Management", "Stockbroking", "Wealth Management"],
    "Microfinance": ["Personal Loans", "Business Loans"],
    "Accounting": ["Tax", "Audit", "Payroll"],
    "Restaurant": ["Fast Food", "Fine Dining", "Takeaway"],
    "Butchery": ["Fresh Meat", "Processed Meat"],
    "Bakery": ["Bread", "Cakes", "Pastries"],
    "Catering": ["Event Catering", "Corporate Catering"],
    "Food Processing": ["Milling", "Dairy", "Beverages"],
    "Furniture Retail": ["Living Room", "Bedroom", "Office"],
    "Home Decor": ["Curtains", "Carpets", "Lighting"],
    "Ministry": ["Policy", "Administration"],
    "Council": ["Municipal Services", "Planning"],
    "Regulatory Body": ["Licensing", "Compliance"],
    "Hospital": ["General", "Private", "Specialist"],
    "Clinic": ["General Practice", "Dental", "Physiotherapy"],
    "Pharmacy": ["Retail", "Hospital Pharmacy"],
    "Laboratory": ["Pathology", "Research"],
    "Law Firm": ["Corporate Law", "Family Law", "Litigation"],
    "Attorney": ["Conveyancing", "Debt Collection"],
    "Publishing": ["Books", "Magazines", "Directories"],
    "Broadcasting": ["TV", "Radio"],
    "Advertising": ["Print", "Digital", "Outdoor"],
    "Diamond Mining": ["Exploration", "Extraction"],
    "Quarry": ["Stone", "Sand", "Gravel"],
    "Supermarket": ["Grocery", "Fresh Produce", "Household"],
    "Clothing Store": ["Menswear", "Womenswear", "Children"],
    "Hardware": ["Tools", "Building Materials", "Paint"],
    "General Dealer": ["Convenience Store", "Spaza Shop"],
    "Wholesaler": ["FMCG", "Bulk Supplies"],
    "Security Guards": ["Manned Guarding", "Patrol"],
    "Alarm Systems": ["Installation", "Monitoring"],
    "CCTV": ["Installation", "Maintenance"],
    "Consulting": ["Business", "Management", "Technical"],
    "Cleaning": ["Commercial", "Residential", "Industrial"],
    "Logistics": ["Freight", "Warehousing", "Distribution"],
    "Recruitment": ["Permanent", "Temporary", "Executive Search"],
    "IT Services": ["Hardware", "Software", "Support"],
    "Software": ["Development", "ERP", "Mobile Apps"],
    "Telecom": ["Mobile", "Fixed Line", "Internet"],
    "Mobile Network": ["Prepaid", "Postpaid", "Data"],
    "ISP": ["Broadband", "Fibre", "Wireless"],
    "Freight": ["Road", "Air", "Sea"],
    "Courier": ["Domestic", "International"],
    "Taxi": ["Local", "Airport Transfers"],
    "Removals": ["Domestic", "International"],
}

# ==============================================
# Helper functions
# ==============================================
def normalize_city(city_str):
    """Map various area names to a known city for prefix lookup."""
    city_str = city_str.strip()
    # Direct match
    if city_str in CITY_PREFIX:
        return city_str
    # Try case-insensitive
    for key in CITY_PREFIX:
        if key.lower() == city_str.lower():
            return key
    # If contains Gaborone
    if "Gaborone" in city_str:
        return "Gaborone"
    if "Francistown" in city_str:
        return "Francistown"
    if "Maun" in city_str:
        return "Maun"
    # Default
    return "Gaborone"

def generate_landline(city):
    """Generate a valid 7-digit landline number with +267 prefix."""
    prefix_info = CITY_PREFIX.get(normalize_city(city), CITY_PREFIX["Gaborone"])
    prefix = prefix_info[0]
    # Ensure prefix is appropriate (e.g., "3" -> 3xx xxxx)
    if len(prefix) == 1:
        # Generate second digit (0-9) and third digit (0-9) to make XXX
        second = random.randint(0, 9)
        third = random.randint(0, 9)
        main = f"{prefix}{second}{third}"
    else:
        main = prefix
    suffix = f"{random.randint(1000, 9999)}"
    return f"+267 {main} {suffix}"

def generate_mobile():
    """Generate an 8-digit mobile number starting with 7x."""
    prefix = random.choice(["71", "72", "73", "74", "75", "76", "77"])
    suffix = random.randint(100000, 999999)
    return f"+267 {prefix}{suffix}"

def generate_whatsapp():
    """Generate a WhatsApp number (usually mobile)."""
    return generate_mobile()

def extract_original_phone(phone_str):
    """Parse original phone string if present; return None if not valid."""
    if not phone_str:
        return None
    # Remove non-digits
    digits = re.sub(r'\D', '', phone_str)
    if len(digits) == 7:
        return f"+267 {digits[:3]} {digits[3:]}"
    elif len(digits) == 8 and digits.startswith('7'):
        return f"+267 {digits}"
    elif len(digits) == 11 and digits.startswith('267'):
        return f"+267 {digits[3:6]} {digits[6:]}"
    return None

def generate_email(business_name, domain="co.bw"):
    """Generate an email from business name."""
    name = re.sub(r'[^a-zA-Z0-9]', '', business_name.lower())
    if not name:
        name = "info"
    return f"{name}@{domain}"

def generate_website(business_name):
    """Generate a website URL."""
    slug = re.sub(r'[^a-zA-Z0-9]', '', business_name.lower())
    if not slug:
        slug = "business"
    return f"https://www.{slug}.co.bw"

def generate_gps(city):
    """Return approximate GPS coordinates for the city."""
    prefix_info = CITY_PREFIX.get(normalize_city(city), CITY_PREFIX["Gaborone"])
    base = prefix_info[1]
    # Add small random offset
    lat = base["lat"] + random.uniform(-0.02, 0.02)
    lng = base["lng"] + random.uniform(-0.02, 0.02)
    return f"{lat:.6f}, {lng:.6f}"

def get_entity_type(name):
    """Guess if business is a company or consultant."""
    if any(kw in name.lower() for kw in ["consult", "attorney", "lawyer", "freelance", "dr ", "prof "]):
        return "Consultant"
    return "Company"

def infer_main_category(original_cat, name):
    """Determine main category from original or name."""
    if original_cat and original_cat != "General Business":
        return original_cat
    # Simple name-based inference
    name_lower = name.lower()
    for cat in MAIN_CATEGORIES:
        if cat.lower() in name_lower:
            return cat
    # Default to Services
    return "Services"

def generate_categories(business):
    """Generate main, sub, sub_sub categories."""
    main = infer_main_category(business.get("category_main") or business.get("category"), business["name"])
    sub_list = SUB_CATEGORIES.get(main, ["General"])
    sub = random.choice(sub_list)
    sub_sub_list = SUB_SUB_CATEGORIES.get(sub, [])
    sub_sub = random.choice(sub_sub_list) if sub_sub_list else None
    return {"main": main, "sub": sub, "sub_sub": sub_sub}

def generate_description(business):
    """Generate a plausible description."""
    name = business["name"]
    city = business.get("city", business.get("location", {}).get("city", "Botswana"))
    cat = business.get("category_main") or business.get("category", "Services")
    desc = f"{name} is a leading provider of {cat.lower()} services in {city}. "
    desc += "With a commitment to quality and customer satisfaction, we have been serving the community for years. "
    desc += "Our team of experienced professionals ensures that every project is completed to the highest standards. "
    desc += "We pride ourselves on our integrity, reliability, and innovative solutions. "
    desc += "Contact us today to learn more about how we can help you achieve your goals."
    return desc

def generate_contact_ledger(business):
    """Generate the full contact ledger with multiple entries."""
    city = business.get("city", business.get("location", {}).get("city", "Gaborone"))
    # Use original phone if available
    original_phone = business.get("phone")
    landline_number = extract_original_phone(original_phone) if original_phone else generate_landline(city)
    mobile1 = generate_mobile()
    mobile2 = generate_mobile()
    whatsapp1 = generate_whatsapp()
    whatsapp2 = generate_whatsapp()
    email1 = generate_email(business["name"])
    email2 = generate_email(business["name"], domain="bw")
    website = generate_website(business["name"])
    gps = generate_gps(city)

    call_numbers = []
    # Land line entries
    call_numbers.append({
        "type": "Land Line",
        "department": "Main Office",
        "number": landline_number,
        "description": "General inquiries"
    })
    call_numbers.append({
        "type": "Land Line",
        "department": "Sales",
        "number": generate_landline(city),
        "description": "Sales department"
    })
    # Mobile operator entries (BTC, Mascom, Orange) – we'll use mobile numbers
    call_numbers.append({
        "type": "BTC",
        "department": "Support",
        "number": mobile1,
        "description": "BTC mobile support"
    })
    call_numbers.append({
        "type": "Mascom",
        "department": "Customer Care",
        "number": mobile2,
        "description": "Mascom line"
    })
    call_numbers.append({
        "type": "Orange",
        "department": "Technical",
        "number": generate_mobile(),
        "description": "Orange technical support"
    })

    whatsapp = [
        {"department": "Sales", "number": whatsapp1, "description": "WhatsApp Business"},
        {"department": "Support", "number": whatsapp2, "description": "Customer support via WhatsApp"}
    ]

    email = [
        {"department": "General", "email": email1, "description": "General inquiries"},
        {"department": "Sales", "email": email2, "description": "Sales team"}
    ]

    websites = [website]

    gps_coordinates = [
        {"branch_name": "Headquarters", "coordinates": gps, "description": "Main office location"}
    ]

    return {
        "call_numbers": call_numbers,
        "whatsapp": whatsapp,
        "email": email,
        "websites": websites,
        "gps_coordinates": gps_coordinates
    }

def generate_social_media(business):
    """Generate social media links."""
    slug = re.sub(r'[^a-zA-Z0-9]', '', business["name"].lower())
    if not slug:
        slug = "business"
    facebook = [
        {"title": "Facebook Page", "link": f"https://facebook.com/{slug}", "description": "Follow us on Facebook"}
    ]
    twitter = [
        {"title": "X (Twitter)", "link": f"https://twitter.com/{slug}", "description": "Latest updates"}
    ]
    tiktok = [
        {"title": "TikTok", "link": f"https://tiktok.com/@{slug}", "description": "Watch our videos"}
    ]
    youtube = [
        {"title": "YouTube Channel", "link": f"https://youtube.com/@{slug}", "description": "Subscribe for content"}
    ]
    return {
        "facebook": facebook,
        "twitter": twitter,
        "tiktok": tiktok,
        "youtube": youtube
    }

def generate_metadata(business):
    """Generate system metadata."""
    # Use established year if present, else random
    est = business.get("established")
    if est:
        creation = datetime(est, 1, 1).isoformat()
    else:
        creation = datetime(random.randint(2010, 2023), random.randint(1,12), random.randint(1,28)).isoformat()
    last_edited = datetime.now().isoformat()
    return {
        "creation_date": creation,
        "last_edited_date": last_edited,
        "user_attribution": "System Admin"
    }

def enrich_business(biz):
    """Take a raw business dict and return enriched one."""
    # Ensure we have consistent fields
    name = biz.get("name", "Unknown")
    city = biz.get("city") or biz.get("location", {}).get("city", "Gaborone")
    address = biz.get("address") or biz.get("location", {}).get("address", "")
    original_id = biz.get("id")

    categories = generate_categories(biz)
    description = generate_description(biz)
    entity_type = get_entity_type(name)
    contact_ledger = generate_contact_ledger(biz)
    social = generate_social_media(biz)
    metadata = generate_metadata(biz)

    enriched = {
        "id": original_id,
        "name": name,
        "city": city,
        "address": address,
        "categories": categories,
        "description": description,
        "entity_type": entity_type,
        "contact_ledger": contact_ledger,
        "social_media": social,
        "metadata": metadata
    }
    return enriched

# ==============================================
# Parse input file and extract all businesses
# ==============================================
def load_all_businesses(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The file contains multiple JSON objects concatenated.
    # We'll split by "{\n  \"metadata\"" and reconstruct.
    # A simpler approach: use a JSON parser that can handle multiple objects.
    # We'll find all JSON objects by scanning for top-level braces.
    businesses = []
    # This is a naive split; for production, use a streaming parser.
    # We'll assume the file is well-formed with objects separated by newline.
    # We'll split by '}\n\n{' or similar.
    # But here we'll manually separate the known objects.
    # Actually, we can use json.loads for each object by finding the start of each.
    # For brevity, we'll assume we have a list of JSON strings.
    # Let's do a simple split on '}\n\n{' after ensuring we add back the braces.
    parts = content.split('}\n\n{')
    for i, part in enumerate(parts):
        if i == 0:
            part += '}'
        else:
            part = '{' + part
        try:
            obj = json.loads(part)
            if "businesses" in obj:
                businesses.extend(obj["businesses"])
        except:
            pass
    return businesses

def main():
    all_businesses = load_all_businesses(INPUT_FILE)
    print(f"Total businesses loaded: {len(all_businesses)}")

    # Skip first 250
    start = START_OFFSET
    end = start + TOTAL_NEEDED
    selected = all_businesses[start:end]
    print(f"Selected {len(selected)} businesses (index {start} to {end-1})")

    # Enrich each
    enriched_list = []
    for biz in selected:
        enriched_list.append(enrich_business(biz))

    # Output in chunks
    for i in range(0, len(enriched_list), CHUNK_SIZE):
        chunk = enriched_list[i:i+CHUNK_SIZE]
        output_file = f"{OUTPUT_PREFIX}_part_{i//CHUNK_SIZE + 1}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, indent=2, ensure_ascii=False)
        print(f"Written {len(chunk)} businesses to {output_file}")

    # Also output the full combined file
    with open(f"{OUTPUT_PREFIX}_all.json", 'w', encoding='utf-8') as f:
        json.dump(enriched_list, f, indent=2, ensure_ascii=False)
    print("Done.")

if __name__ == "__main__":
    main()