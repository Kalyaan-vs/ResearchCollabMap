import requests
import csv
import time

# Input and Output CSV Files
INPUT_FILE = "research_paper_collab.csv"
OUTPUT_FILE = "university_locations.csv"
OPENALEX_API = "https://api.openalex.org/institutions"

# Cache to store already fetched locations
location_cache = {}

# Manually corrected locations (use real lat/lon)
manual_corrections = {
    "Institute for Informatics and Automation Problems": (40.1809, 44.5150),
    "National Academy of Sciences of Armenia": (40.1792, 44.5125)
}


def read_university_names():
    """Reads the collaborating universities from the CSV file."""
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            universities = set()  # Avoid duplicates
            for row in reader:
                universities.update(row["Collaborating Universities"].split(", "))
            return list(universities)  # Return unique list of universities
    except Exception as e:
        print(f"❌ Error reading {INPUT_FILE}: {e}")
        return []


def get_university_location(university_name):
    """Fetch university details from OpenAlex API with caching & manual corrections."""
    # Check manual corrections first
    if university_name in manual_corrections:
        return manual_corrections[university_name]

    if university_name in location_cache:
        return location_cache[university_name]

    params = {"filter": f"display_name.search:{university_name}"}
    try:
        response = requests.get(OPENALEX_API, params=params, timeout=5)  # 5s timeout
        if response.status_code == 200:
            data = response.json()
            if "results" in data and data["results"]:
                result = data["results"][0]  # Take the first match
                latitude = result.get("geo", {}).get("latitude", "N/A")
                longitude = result.get("geo", {}).get("longitude", "N/A")

                # Cache the result
                location_cache[university_name] = (latitude, longitude)
                return latitude, longitude
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Request error for {university_name}: {e}")

    return "N/A", "N/A"


def write_university_locations(universities):
    """Writes university locations to CSV efficiently and logs duplicates."""
    seen_locations = {}

    # Truncate file before writing
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["University", "Latitude", "Longitude"])  # Write header

    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for university in universities:
            lat, lon = get_university_location(university)

            # Log duplicate coordinates
            if (lat, lon) in seen_locations:
                print(
                    f"⚠️ Possible duplicate location for {university}: {lat}, {lon} (Same as {seen_locations[(lat, lon)]})")
            else:
                seen_locations[(lat, lon)] = university

            writer.writerow([university, lat, lon])
            print(f"✅ Fetched: {university} -> Lat: {lat}, Lon: {lon}")
            time.sleep(0.5)  # Reduce delay slightly


universities = read_university_names()
if universities:
    write_university_locations(universities)
    print(f"\n✅ University locations saved to {OUTPUT_FILE}")
else:
    print("⚠️ No universities found to process.")
