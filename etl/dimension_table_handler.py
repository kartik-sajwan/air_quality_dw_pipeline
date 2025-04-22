
from utils.api_utils import APIHelper
from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getenv("API_BASE_URL")
api_key = os.getenv("OPENAQ_API_KEY")


def main():

  api = APIHelper(base_url)

  for page in api.stream_api_pages("locations", api_key, params={"order_by": "id", "sort_order": "asc", "countries_id": "9"}, page_size=100):
      results = page["results"]
      print(f"Fetched {len(results)} results")


if __name__ == "__main__":
   main()
