import json
import logging
import requests


def call_api(_url, retries=3):
    """Makes an API call to the given URL and returns the JSON response."""
    try:
        _response = requests.get(_url, timeout=2)
        _response.raise_for_status()
        try:
            return _response.json()
        except json.JSONDecodeError as e:
            logging.error(f"_response.json() : {_url}\n{_response.text}\n{e}\n")
            if retries > 0:
                return call_api(_url, retries - 1)
            raise
    except requests.exceptions.Timeout:
        if retries > 0:
            return call_api(_url, retries - 1)
        raise
    except Exception as e:
        logging.error(f"Exception : {_url}\n{_response.text if '_response' in locals() else 'No response'}\n{e}\n")
        if retries > 0:
            return call_api(_url, retries - 1)
        raise
