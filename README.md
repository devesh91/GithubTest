#Github Popularity Checker

**Problem Statement:** To build a Solution to fetch Github repository information  and check it's populaity based on forks and stars

**Solution Overview**
The solution is built using the consumable API provided by Github. This application calls Github API server to fetch data for a given Repository. Based on this data(Forks, Stars) popularity score is calculated using below formula:

score = num_stars * 1 + num_forks * 2

The Repository is a popular if it's score is greater then or equal to 500 , otherwise its not a popular repository. The API's are named version v1, so that for future release it can be renamed. 


**Tech Stack:**
Backend Programming Language: Python (Version: 3.9.2)
API Framework: Flask
Authentication: Access Token (Generated for self using Github App, OAuth can also be used)
Documentation: Postman
Python Libraries: Requests, multiprocessing

**API Description:**

HTTP Method:GET

API 1: v1/healthCheck: API endpoint to check if the service is available & accessible in less than 0.5 seconds.
API 2: v1/checkRepo: API endpoint to fetch data(Stars,forks) for given repository from Github and check if its popular or not
API 3: /: show all available API for application

**Pre-conditions**
Input String would either be in form owner/repository or https//www.github.com/owner/repository

**How to run the Solution:**
Install Requirements 
pip install -r requirements.txt

**To Run the application server**
python Github_Popularity_Checker/main.py

 **To Run Test Cases**
python test.py

**To access documentation:**
https//www.github.com>/docs

**Scope of Improvements:**
HTML pages to show User-Friendly Exception Handling e.g small html template to display repo not found.
Implemenation of JWT token with customisable expiry Time.
Exhasutive Automatic Test cases can be added to provide good test coverage.
To access the Webpage from UI, simple front-end could have been developed.

