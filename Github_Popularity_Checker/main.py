from flask import Flask, abort
import multiprocessing
from flask import jsonify
import requests
from utility import validate_repository
from constants import timeout, GITHUB_ROOT_URL, SEARCH_ENDPOINT, DEFAULT_REPOSITORY, headers

app = Flask(__name__)


def github_call(params, github_api=GITHUB_ROOT_URL + SEARCH_ENDPOINT, headers=headers):
    global resp
    resp = requests.get(github_api, headers=headers, params=params)


def search_repo(params, timeout, headers=headers):
    """Spawn process to make the git api call and kill the thread after timeout."""
    p = multiprocessing.Process(target=github_call(params, GITHUB_ROOT_URL + SEARCH_ENDPOINT, headers, ))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.kill()
        print("Error in call search method")
        abort(404, description="Request Timed Out")


@app.route("/v1/checkRepo/<owner>/<repo_name>", methods=['GET'])
def check_repo(owner, repo_name):
    """API endpoint to fetch data(Stars,forks) for given repository from Github."""
    # Check if git repo name provided is valid
    str_url = validate_repository(owner,repo_name)
    params = {'q': 'repo:' + str_url, 'per_page': 1}

    # Call the git search api endpoint with timeout of the environment
    search_repo(params, timeout=timeout, headers=headers)
    json_response = resp.json()
    print(json_response)
    if resp.status_code != 200:
        if resp.status_code == 500:
            abort(500, description=json_response['errors'][0]['message'])
        elif resp.status_code == 408:
            abort(408, description=json_response['errors'][0]['message'])
        elif resp.status_code == 401:
            abort(401, description="Unauthorised access")
        elif resp.status_code == 403:
            abort(403, description="Forbidden Access Denied")
        elif resp.status_code == 422:
            abort(422, description="Invalid Repository  or Owner Name")
        resp_code = resp.status_code
        resp_message = json_response['message']
    else:
        num_forks = json_response['items'][0]['forks']
        num_stars = json_response['items'][0]['stargazers_count']
        score = num_stars * 1 + num_forks * 2
        resp_code = 200
        if score >= 500:
            resp_message = "Repository is popular."
        else:
            resp_message = "Repository is not popular."

    return jsonify(
        status_code=resp_code,
        content={"Response": resp_message}
    )


@app.route("/v1/healthCheck", methods=['GET'])
def validate_service():
    """API endpoint to check health of service"""
    params = {'q': 'repo:' + DEFAULT_REPOSITORY,
              'per_page': 1}
    search_repo(params, timeout=timeout, headers=headers)
    return jsonify(
        status_code=resp.status_code
    )


@app.route("/")
def root_endpoint():
    """Endpoints available for interaction"""
    return jsonify(
        status_code=200,
        content={"Publicly Available APIs": "/v1/healthCheck, /v1/checkRepo."
                 }
    )


if __name__ == '__main__':
    print("Application is running on Host: 127.0.0.1:5000")
    app.run()
