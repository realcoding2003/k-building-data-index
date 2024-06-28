import unittest
from unittest.mock import patch

import requests

from src.common.utils import call_api, create_directory_if_not_exists


class TestUtils(unittest.TestCase):
    @patch('src.common.utils.requests.get')
    def test_call_api_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'value'}

        url = 'http://fakeurl.com/api'
        response = call_api(url)

        self.assertEqual(response, {'key': 'value'})
        mock_get.assert_called_once_with(url, timeout=2)

    @patch('src.common.utils.requests.get')
    def test_call_api_failure(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("API Error")

        url = 'http://fakeurl.com/api'
        with self.assertRaises(requests.exceptions.HTTPError):
            call_api(url, retries=1)  # Set retries to 1 to avoid multiple retry attempts in the test

        self.assertEqual(mock_get.call_count, 2)  # 1 initial call + 1 retry

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_create_directory_if_not_exists(self, mock_exists, mock_makedirs):
        directory = 'test_directory'

        create_directory_if_not_exists(directory)

        mock_exists.assert_called_once_with(directory)
        mock_makedirs.assert_called_once_with(directory, exist_ok=True)

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=True)
    def test_create_directory_already_exists(self, mock_exists, mock_makedirs):
        directory = 'existing_directory'

        create_directory_if_not_exists(directory)

        mock_exists.assert_called_once_with(directory)
        mock_makedirs.assert_not_called()


if __name__ == '__main__':
    unittest.main()
