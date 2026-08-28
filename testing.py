import os
from dotenv import load_dotenv
load_dotenv()
serp = os.getenv("SERP_API_KEY")

from serpapi import GoogleSearch

params = {
    "engine": "google_shopping",
    "q": "coffee",
    "api_key": serp
}

search = GoogleSearch(params)
results = search.get_dict()
shopping_results = results.get("shopping_results", [])

print(results)
print(shopping_results)