from flask import abort


def validate_repository(owner,repo_name):
    # maximum repository name as per documentation should not be more than 100
    if len(repo_name) > 100:
        abort(status_code=400,
              description="Provided Repository name is not correct.Please provide a valid repository name.")

    return owner + "/" + repo_name
