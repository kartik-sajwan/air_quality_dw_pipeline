import requests
import time
from loguru import logger
from typing import List, Dict, Optional, Generator
import re


class APIHelper:
  def __init__(self, base_url: str, retries: int = 3,
               backoff_factor: float = 1, timeout: int = 10):
    self.base_url = base_url.rstrip('/')
    self.session = requests.Session()
    self.retries = retries
    self.backoff_factor = backoff_factor
    self.timeout = timeout

  def stream_api_pages(self,
                       endpoint: str,
                       api_key: str,
                       params: Optional[Dict] = None,
                       page_size: int = 1000) -> Generator[Dict, None, None]:
    """Perform a GET request and return pages from API endpoint"""
    page = 1
    more_pages = True
    query_params = params.copy() if params else {}
    url = f"{self.base_url}/{endpoint.lstrip('/')}"
    headers = {"X-API-Key": api_key} if api_key else {}
    while more_pages:
      query_params.update({"page": page, "limit": page_size})

      try:
        logger.info(f"Fetching {url} page={page}, limit={page_size}")
        response = self.session.get(
            url, params=query_params, headers=headers, timeout=self.timeout)

        rem_rate_limit = int(response.headers.get(
            "x-ratelimit-remaining"))
        rate_limit_reset_sec = int(
            response.headers.get("x-ratelimit-reset"))

        if rem_rate_limit == 0:
          logger.warning(
              f"Rate limit exhausted. Sleeping for {rate_limit_reset_sec} seconds...")
          time.sleep(rate_limit_reset_sec * self.backoff_factor)
          continue

        response.raise_for_status()
        data = response.json()

        yield data

        is_more_pages = data.get("meta").get("found")
        is_more_pages = int(str(is_more_pages).replace(">", "")) if isinstance(
            is_more_pages, str) else is_more_pages

        if is_more_pages < page_size:
          more_pages = False
        else:
          page += 1
      except requests.HTTPError as err:
        logger.error(f"Error while fetching page {page} from {url}: {err}")
      except requests.exceptions.RequestException as err:
        logger.error(f"Failed to fetch page {page} from {url}: {err}")
      finally:
        self.session.close()
