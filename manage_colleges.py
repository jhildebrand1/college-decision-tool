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
    return ["Cost", "Support", "Adjustment", "Home", "Social", "Environment", "Weather", "Biology", "CLS", "Spirit", "Happiness", "Admissions"]

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

    print("\n3. Grade & Detail Metrics (replace <metric> with metric name):")
    metrics = get_metric_keys(data)
    for m in metrics:
        print(f"   - grades.{m}")
        print(f"   - details.{m}")
    print("\nExample usage: python manage_colleges.py --school UCLA --field location --value \"Los Angeles, CA\"")
    print("To rename a metric globally: python manage_colleges.py --rename-metric <OldName> <NewName>")
    print("To remove a section metric across all schools: python manage_colleges.py --remove-section <metric>")

def remove_section_globally(data, section_name):
    target = section_name.strip()
    print(f"\n⚠️ WARNING: You are about to completely remove the metric/section '{target}' (both grades.{target} and details.{target}) from ALL schools.")
    confirmation = input("Are you sure? Type 'yes' to proceed: ").strip()
    
    if confirmation != "yes":
        print("Operation cancelled. No changes were made.")
        return

    removed_count = 0
    for s in data.get("schools", []):
        modified = False
        if "grades" in s and target in s["grades"]:
            del s["grades"][target]
            modified = True
        if "details" in s and target in s["details"]:
            del s["details"][target]
            modified = True
        if modified:
            removed_count += 1

    if "metrics_descriptions" in data and target in data["metrics_descriptions"]:
        del data["metrics_descriptions"][target]

    save_data(data)
    print(f"Successfully removed section '{target}' from {removed_count} school(s).")

def rename_metric_globally(data, old_name, new_name):
    old_target = old_name.strip()
    new_target = new_name.strip()

    if not old_target or not new_target:
        print("Error: Both old and new metric names must be provided.")
        return

    print(f"\n⚠️ You are about to rename metric '{old_target}' to '{new_target}' across ALL schools and descriptions.")
    confirmation = input("Are you sure? Type 'yes' to proceed: ").strip()

    if confirmation != "yes":
        print("Operation cancelled. No changes were made.")
        return

    updated_count = 0
    for s in data.get("schools", []):
        modified = False
        if "grades" in s and old_target in s["grades"]:
            s["grades"][new_target] = s["grades"].pop(old_target)
            modified = True
        if "details" in s and old_target in s["details"]:
            s["details"][new_target] = s["details"].pop(old_target)
            modified = True
        if modified:
            updated_count += 1

    if "metrics_descriptions" in data and old_target in data["metrics_descriptions"]:
        data["metrics_descriptions"][new_target] = data["metrics_descriptions"].pop(old_target)

    save_data(data)
    print(f"Successfully renamed metric '{old_target}' to '{new_target}' for {updated_count} school(s).")

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

    save_data(data)

def main():
    parser = argparse.ArgumentParser(description="Manage college data JSON.")
    parser.add_argument("--add", metavar="CODE", help="Quickly add a new school code with empty/default template.")
    parser.add_argument("--list", action="store_true", help="List all schools in the database (or combine with --school or --field to query).")
    parser.add_argument("--metrics", action="store_true", help="List all evaluation metrics currently configured.")
    parser.add_argument("--fields", action="store_true", help="Display all editable fields and paths.")
    parser.add_argument("--school", metavar="CODE", help="Specify school code to view/edit.")
    parser.add_argument("--field", metavar="PATH", help="Specify field path to view/update (e.g., location, profile.topology, grades.biology).")
    parser.add_argument("--value", metavar="VAL", help="New value to assign when updating a field.")
    parser.add_argument("--remove-section", metavar="SECTION", help="Completely remove a metric section (grades and details) across all schools.")
    parser.add_argument("--rename-metric", nargs=2, metavar=("OLD", "NEW"), help="Rename a metric key globally across all schools.")
    args = parser.parse_args()

    data = load_data()

    if args.remove_section:
        remove_section_globally(data, args.remove_section)
        return

    if args.rename_metric:
        rename_metric_globally(data, args.rename_metric[0], args.rename_metric[1])
        return

    if args.fields:
        show_editable_fields(data)
        return

    if args.metrics:
        print("\n--- Current Evaluation Metrics ---")
        metrics = get_metric_keys(data)
        for m in metrics:
            desc = data.get("metrics_descriptions", {}).get(m, "No description found.")
            print(f"- {m}: {desc}")
        return

    # QUERY MODE: python manage_colleges.py --list --school <name>
    if args.list and args.school and not args.field:
        school_code = args.school.strip().upper()
        target_school = None
        for s in data["schools"]:
            if s["school"].upper() == school_code or s.get("profile", {}).get("full_name", "").upper() == school_code:
                target_school = s
                break
        
        if not target_school:
            print(f"Error: School '{args.school}' not found.")
            return

        print(f"\n--- Stats for {target_school['school']} ({target_school.get('profile', {}).get('full_name', '')}) ---")
        print(json.dumps(target_school, indent=2, ensure_ascii=False))
        return

    # QUERY MODE: python manage_colleges.py --list --field <path>
    if args.list and args.field and not args.school:
        path = args.field.strip()
        print(f"\n--- Querying Field: '{path}' across all schools ---")
        
        for s in data["schools"]:
            school_name = s['school']
            val = None
            
            if path.startswith("profile."):
                prof_key = path.split(".")[1]
                val = s.get("profile", {}).get(prof_key, "N/A")
            elif path.startswith("grades."):
                grade_key = path.split(".")[1]
                val = s.get("grades", {}).get(grade_key, "N/A")
            elif path.startswith("details."):
                detail_key = path.split(".")[1]
                val = s.get("details", {}).get(detail_key, "N/A")
            elif path in ["location", "enrollment", "school"]:
                val = s.get(path, "N/A")
            else:
                print(f"Error: Unknown field path '{path}'. Run with --fields to see available paths.")
                return
            
            print(f"  {school_name}: {val}")
        return

    # GENERAL LIST MODE: python manage_colleges.py --list
    if args.list:
        print("\n--- Current Schools ---")
        for s in data.get("schools", []):
            print(f"- {s['school']}: {s.get('profile', {}).get('full_name', '')} ({s.get('location', 'No location')})")
        return

    # UPDATE MODE: python manage_colleges.py --school <CODE> --field <PATH> --value <VAL>
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

        if path.startswith("profile."):
            prof_key = path.split(".")[1]
            if prof_key in target_school["profile"]:
                target_school["profile"][prof_key] = val
                save_data(data)
                print(f"Updated profile.{prof_key} for {school_code} to: {val}")
            else:
                print(f"Error: Profile key '{prof_key}' does not exist.")
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
        print(f"⚠️ WARNING: School '{school_code}' added with empty template fields.")
        return

    # Interactive menu if no CLI args passed
    while True:
        print("\n=== College Database Manager ===")
        print("1. Add New School (Interactive)")
        print("2. Edit Existing School")
        print("3. List All Schools")
        print("4. List All Metrics")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()
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
            print("\n--- Current Evaluation Metrics ---")
            metrics = get_metric_keys(data)
            for m in metrics:
                desc = data.get("metrics_descriptions", {}).get(m, "No description found.")
                print(f"- {m}: {desc}")
        elif choice == "5":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()