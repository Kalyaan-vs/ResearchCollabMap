import requests
import urllib.parse
import csv
import os

OPENALEX_WORKS_API = "https://api.openalex.org/works?search="
OUTPUT_FILE = "research_paper_collab.csv"


def get_exact_paper(title):
    """Fetch the exact research paper from OpenAlex."""
    encoded_title = urllib.parse.quote(title)
    response = requests.get(f"{OPENALEX_WORKS_API}{encoded_title}")

    if response.status_code != 200:
        print(f"⚠️ OpenAlex API Error: {response.status_code}")
        return None

    data = response.json()
    results = data.get("results", [])

    for result in results:
        result_title = result.get("title")

        if result_title and result_title.strip().lower() == title.strip().lower():
            return result  # Return only the exact match

    print("❌ No exact match found in OpenAlex.")
    return None


def get_paper_affiliation(title):
    """Extract authors and collaborating universities from the exact research paper."""
    paper = get_exact_paper(title)

    if not paper:
        return [], []  # Return empty lists if no match

    # Extract authors
    authors = [author.get("author", {}).get("display_name", "Unknown")
               for author in paper.get("authorships", [])]

    # Extract unique collaborating universities
    institutions = set()
    for author in paper.get("authorships", []):
        for institution in author.get("institutions", []):
            if institution and institution.get("display_name"):
                institutions.add(institution["display_name"])

    return authors, list(institutions)


def save_to_csv(title, authors, universities):
    """Save research paper title, authors, and collaborating universities to a CSV file."""
    file_exists = os.path.isfile(OUTPUT_FILE)

    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header only if file is newly created
        if not file_exists:
            writer.writerow(["Title", "Authors", "Collaborating Universities"])

        writer.writerow([title, ", ".join(authors), ", ".join(universities)])


# Example usage
title = input("Please Enter the title of theResearch Paper: ")
# title = "Reliability Criteria in Information Theory and in Statistical Hypothesis Testing"
authors, universities = get_paper_affiliation(title)

print("\n===== Research Paper Details =====")
print(f"📖 Title: {title}")
print(f"👥 Authors: {', '.join(authors) if authors else 'Unknown'}")
print(f"🏛️ Collaborating Universities: {', '.join(universities) if universities else 'Unknown'}")

if authors and universities:
    save_to_csv(title, authors, universities)  # Save the result to CSV
    print(f"✅ Saved to {OUTPUT_FILE}")
else:
    print("❌ No data found to save.")
