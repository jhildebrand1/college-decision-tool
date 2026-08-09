import json
import os
import argparse

JSON_FILE = "college_data.json"

def load_data():
    if not os.path.exists(JSON_FILE):
        return {"metrics_descriptions": {}, "schools": []}
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully saved changes to {JSON_FILE}!")

def get_metric_keys(data):
    if data.get("metrics_descriptions"):
        return list(data["metrics_descriptions"].keys())
    elif data.get("schools"):
        return list(data["schools"][0].get("grades", {}).keys())
    return ["Cost", "Difficulty", "Support", "Adjustment", "Home", "Social", "Environment", "Weather", "Biology", "CLS", "Spirit", "Happiness", "Admissions"]

def show_editable_fields(data):
    print("\n--- Editable Fields Reference Guide ---")
    print("1. Root Fields:")
    print("   - location")
    print("   - enrollment")
    
    print("\n2. Profile Fields (under 'profile'):")
    sample_prof = data["schools"][0]["profile"] if data.get("schools") else {
        "full_name": "", "photo_1": "", "photo_2": "", "photo_3": "",
        "video_url": "", "topology": "", "airport_distance": "", "transit_options": "",
        "neighborhood_vibe": "", "housing_status": "", "medical_access": "",
        "link_admissions": "", "link_bio_dept": "", "link_official_site": "",
        "school_logo": "", "link_appily": ""
    }
    for key in sample_prof.keys():
        print(f"   - profile.{key}")

    print("\n3. Grade & Detail Metrics (replace <metric> with metric name, e.g., biology):")
    metrics = get_metric_keys(data)
    for m in metrics:
        print(f"   - grades.{m}")
        print(f"   - details.{m}")
    print("\nExample usage: python script.py --school UCLA --field location --value \"Los Angeles, CA\"")
    print("Example usage for metrics: python script.py --school UCLA --field grades.biology --value A")

def add_school_interactive(data):
    print("\n--- Add New School (Interactive) ---")
    school_code = input("Enter School Code (e.g., UCLA): ").strip().upper()
    if not school_code:
        print("Error: School code cannot be empty.")
        return

    for s in data["schools"]:
        if s["school"].upper() == school_code:
            print(f"Warning: School '{school_code}' already exists! Use edit instead.")
            return

    full_name = input("Enter Full School Name: ").strip()
    location = input("Enter Location (e.g., Los Angeles, CA): ").strip()
    enrollment = input("Enter Enrollment (number): ").strip()

    metrics = get_metric_keys(data)
    grades, details = {}, {}
    print("\nEnter grades (A-F) and details (press Enter for defaults):")
    for m in metrics:
        grades[m] = input(f"  [{m}] Grade (default C): ").strip().upper() or "C"
        details[m] = input(f"  [{m}] Details: ").strip() or f"No details provided yet for {m}."

    print("\nEnter Profile / Media Info (Press Enter to skip):")
    profile = {
        "full_name": full_name or school_code,
        "photo_1": input("  Photo 1 URL: ").strip(),
        "photo_2": input("  Photo 2 URL: ").strip(),
        "photo_3": input("  Photo 3 URL: ").strip(),
        "video_url": input("  Video Embed URL: ").strip(),
        "topology": input("  Campus Topology: ").strip(),
        "airport_distance": input("  Airport Distance: ").strip(),
        "transit_options": input("  Transit Options: ").strip(),
        "neighborhood_vibe": input("  Neighborhood Vibe: ").strip(),
        "housing_status": input("  Housing Status: ").strip(),
        "medical_access": input("  Medical Access: ").strip(),
        "link_admissions": input("  Admissions Link: ").strip(),
        "link_bio_dept": input("  Bio Dept Link: ").strip(),
        "link_official_site": input("  Official Site Link: ").strip(),
        "school_logo": input("  School Logo URL: ").strip(),
        "link_appily": input("  Appily Link: ").strip()
    }

    missing = []
    if not full_name: missing.append("full_name")
    if not location: missing.append("location")
    if not profile["school_logo"]: missing.append("school_logo")
    if missing:
        print(f"\n⚠️ WARNING: The following fields were left empty: {', '.join(missing)}")

    new_school = {
        "school": school_code,
        "location": location or "Unknown",
        "enrollment": enrollment or "0",
        "profile": profile,
        "grades": grades,
        "details": details
    }

    data["schools"].append(new_school)
    save_data(data)

def edit_school_interactive(data):
    print("\n--- Edit Existing School ---")
    schools = data["schools"]
    if not schools:
        print("No schools found in database.")
        return

    print("Available schools:")
    for i, s in enumerate(schools):
        print(f"  {i+1}. {s['school']} ({s.get('profile', {}).get('full_name', s['school'])})")

    choice = input("Select school number to edit: ").strip()
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(schools):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    school = schools[idx]
    print(f"\nEditing: {school['school']} - {school.get('profile', {}).get('full_name', '')}")
    print("Leave blank to keep existing value.")

    school["location"] = input(f"Location [{school.get('location', '')}]: ").strip() or school.get('location', '')
    school["enrollment"] = input(f"Enrollment [{school.get('enrollment', '')}]: ").strip() or school.get('enrollment', '')

    if "profile" not in school: school["profile"] = {}
    prof = school["profile"]
    for key in prof:
        val = input(f"  Profile [{key}] [{prof.get(key, '')}]: ").strip()
        if val: prof[key] = val

    metrics = get_metric_keys(data)
    if "grades" not in school: school["grades"] = {}
    if "details" not in school: school["details"] = {}

    print("\nEdit Metrics:")
    for m in metrics:
        curr_g = school["grades"].get(m, "C")
        curr_d = school["details"].get(m, "")
        new_g = input(f"  [{m}] Grade [{curr_g}]: ").strip().upper()
        if new_g: school["grades"][m] = new_g
        new_d = input(f"  [{m}] Detail [{curr_d[:30]}...]: ").strip()
        if new_d: school["details"][m] = new_d

    missing = []
    if not school.get("location"): missing.append("location")
    if not prof.get("school_logo"): missing.append("school_logo")
    if missing:
        print(f"\n⚠️ WARNING: The following key fields are still empty: {', '.join(missing)}")

    save_data(data)

def main():
    parser = argparse.ArgumentParser(description="Manage college data JSON.")
    parser.add_argument("--add", metavar="CODE", help="Quickly add a new school code with empty/default template.")
    parser.add_argument("--list", action="store_true", help="List all schools in the database.")
    parser.add_argument("--fields", action="store_true", help="Display all editable fields and paths.")
    parser.add_argument("--school", metavar="CODE", help="Specify school code to edit via command line.")
    parser.add_argument("--field", metavar="PATH", help="Specify field path to update (e.g., location, profile.topology, grades.biology).")
    parser.add_argument("--value", metavar="VAL", help="New value to assign to the specified field.")
    args = parser.parse_args()

    data = load_data()

    if args.fields:
        show_editable_fields(data)
        return

    if args.list:
        print("\n--- Current Schools ---")
        for s in data.get("schools", []):
            print(f"- {s['school']}: {s.get('profile', {}).get('full_name', '')} ({s.get('location', 'No location')})")
        return

    if args.school and args.field and args.value is not None:
        school_code = args.school.strip().upper()
        target_school = None
        for s in data["schools"]:
            if s["school"].upper() == school_code:
                target_school = s
                break
        
        if not target_school:
            print(f"Error: School '{school_code}' not found.")
            return

        path = args.field.strip()
        val = args.value.strip()

        # Handle dot notations (e.g., profile.topology, grades.biology, details.biology)
        if path.startswith("profile."):
            prof_key = path.split(".")[1]
            if prof_key in target_school["profile"]:
                target_school["profile"][prof_key] = val
                save_data(data)
                print(f"Updated profile.{prof_key} for {school_code} to: {val}")
            else:
                print(f"Error: Profile key '{prof_key}' does not exist. Use --fields to check valid fields.")
        elif path.startswith("grades."):
            grade_key = path.split(".")[1]
            target_school.setdefault("grades", {})[grade_key] = val.upper()
            save_data(data)
            print(f"Updated grades.{grade_key} for {school_code} to: {val.upper()}")
        elif path.startswith("details."):
            detail_key = path.split(".")[1]
            target_school.setdefault("details", {})[detail_key] = val
            save_data(data)
            print(f"Updated details.{detail_key} for {school_code} to: {val}")
        elif path in ["location", "enrollment"]:
            target_school[path] = val
            save_data(data)
            print(f"Updated {path} for {school_code} to: {val}")
        else:
            print(f"Error: Unknown field path '{path}'. Run with --fields to see available fields.")
        return

    if args.add:
        school_code = args.add.strip().upper()
        for s in data["schools"]:
            if s["school"].upper() == school_code:
                print(f"Error: School '{school_code}' already exists.")
                return
        
        metrics = get_metric_keys(data)
        grades = {m: "C" for m in metrics}
        details = {m: f"No details provided yet for {m}." for m in metrics}
        profile = {
            "full_name": school_code, "photo_1": "", "photo_2": "", "photo_3": "",
            "video_url": "", "topology": "", "airport_distance": "", "transit_options": "",
            "neighborhood_vibe": "", "housing_status": "", "medical_access": "",
            "link_admissions": "", "link_bio_dept": "", "link_official_site": "",
            "school_logo": "", "link_appily": ""
        }
        
        new_school = {
            "school": school_code,
            "location": "Unknown",
            "enrollment": "0",
            "profile": profile,
            "grades": grades,
            "details": details
        }
        data["schools"].append(new_school)
        save_data(data)
        print(f"⚠️ WARNING: School '{school_code}' added with empty/default template fields. Remember to fill them in!")
        return

    # Interactive menu if no CLI args passed
    while True:
        print("\n=== College Database Manager ===")
        print("1. Add New School (Interactive)")
        print("2. Edit Existing School")
        print("3. List All Schools")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ").strip()
        data = load_data()

        if choice == "1":
            add_school_interactive(data)
        elif choice == "2":
            edit_school_interactive(data)
        elif choice == "3":
            print("\n--- Current Schools ---")
            for s in data.get("schools", []):
                print(f"- {s['school']}: {s.get('profile', {}).get('full_name', '')} ({s.get('location', 'No location')})")
        elif choice == "4":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()