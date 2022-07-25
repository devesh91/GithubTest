import requests
from main import search_repo
import sys
import unittest
from constants import timeout, headers

API_URL = "http://127.0.0.1:5000"

class TestClass(unittest.TestCase):

    def test_check_repo_negative(self):
        "API testing to check response for invalid repository Name"
        owner = "kurtCobain"
        repo_name = "qwertyupofapofajfklja"
        params = {'q': 'repo:' + owner + "/" + repo_name, 'per_page': 1}
        url = "{}/v1/checkRepo/{}/{}".format(API_URL, owner, repo_name)
        resp = requests.get(url, headers=headers, params=params)
        self.assertEqual(422, resp.status_code)

    def test_popular_repo_check(self):
        "Test to check whether popular repository are captured correctly"
        owner = "CoreyMSchafer"
        repo_name = "dotfiles"  # popular repository
        params = {'q': 'repo:' + owner + "/" + repo_name, 'per_page': 1}
        url = "{}/v1/checkRepo/{}/{}".format(API_URL, owner, repo_name)
        resp = requests.get(url, headers=headers, params=params)

        api_response = resp.json()
        self.assertEqual("Repository is popular.", api_response['content']['Response'])

    def test_unpopular_repo_check(self):
        "Test to check whether not popular repository are captured correctly"
        owner = "devesh91"  # not a popular repository
        repo_name = "BasicBookStore"
        params = {'q': 'repo:' + owner + "/" + repo_name, 'per_page': 1}
        url = "{}/v1/checkRepo/{}/{}".format(API_URL, owner, repo_name)
        resp = requests.get(url, headers=headers, params=params)

        api_response = resp.json()
        self.assertEqual("Repository is not popular.", api_response['content']['Response'])

    def test_timeout(self):
        owner = "CoreyMSchafer"
        repo_name = "dotfiles"
        params = {'q': 'repo:' + owner + "/" + repo_name, 'per_page': 1}
        return_code = None
        try:
            self.assertEqual(return_code, search_repo(params, timeout))
        except():
            return_code = sys.exc_info()[1].status_code
            self.assertEqual(return_code, 408)


if __name__ == '__main__':
    unittest.main()
