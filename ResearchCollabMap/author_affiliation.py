import requests


def get_orcid_affiliation(author_name):
    """Fetch the institution of an author from ORCID"""
    query_url = f"https://pub.orcid.org/v3.0/search/?q=given-names:{author_name}"
    headers = {"Accept": "application/json"}

    response = requests.get(query_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "result" in data:
            for result in data["result"]:
                orcid_id = result["orcid-identifier"]["path"]
                profile_url = f"https://pub.orcid.org/v3.0/{orcid_id}"

                profile_response = requests.get(profile_url, headers=headers)
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()

                    # Check if "activities-summary" and "employments" exist
                    if "activities-summary" in profile_data:
                        employments = profile_data["activities-summary"].get("employments", {})
                        if "employment-summary" in employments and employments["employment-summary"]:
                            institution = employments["employment-summary"][0]["organization"]["name"]
                            return institution

    return "Unknown Institution"


# Example usage:
author = "Michael Ley"
institution = get_orcid_affiliation(author)
print(f"Author: {author}, Institution: {institution}")
