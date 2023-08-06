import requests
from datetime import datetime, timedelta
import time

from rohub import settings


def valid_to(exp_time):
    """
    Helper function that calculates expiration time for a token.
    :param exp_time: int -> expiration time in seconds.
    :return:
    """
    if exp_time:
        now = datetime.now()
        return now + timedelta(0, exp_time)
    else:
        print('Unable to calculate expiration time. Expected expiration time'
              ' in seconds. Received None value.')


def is_valid(token_type):
    """
    Function that checks if given token is still valid.
    :param token_type: str -> token type.
    :return: boolean -> True if valid, False otherwise.
    """
    if token_type.lower() == "access":
        if settings.ACCESS_TOKEN_VALID_TO:
            now = datetime.now()
            time_difference = settings.ACCESS_TOKEN_VALID_TO - now
            if time_difference.days < 0:
                return False
            else:
                return True
        else:
            print("Missing information regarding token expiration time. Consider logging again!")
    elif token_type.lower() == "refresh":
        if settings.REFRESH_TOKEN_VALID_TO:
            now = datetime.now()
            time_difference = settings.REFRESH_TOKEN_VALID_TO - now
            if time_difference.days < 0:
                return False
            else:
                return True
        else:
            print("Missing information regarding token expiration time. Consider logging again!")
    else:
        print("Token type not recognized! Supported values are access and refresh.")


def get_request(url, use_token=False):
    """
    Function that performs get request with error handling.
    :param url: str -> url.
    :param use_token: boolean -> if True the token will be passed into headers.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    try:
        if use_token:
            headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
            r = requests.get(url=url, headers=headers, timeout=settings.TIMEOUT)
        else:
            r = requests.get(url=url, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError as e:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=settings.API_URL + "research-areas/", timeout=settings.TIMEOUT)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def get_file_request(url, use_token=False, application_type=None):
    """
    Function that performs get request with error handling.
    :param url: str -> url.
    :param use_token: boolean -> if True the token will be passed into headers.
    :param application_type: str -> application type that should be passed in headers.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    try:
        if use_token:
            if application_type:
                headers = {"Authorization": f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}",
                           "Accept": f"application/{application_type}"}
            else:
                headers = {"Authorization": f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
            r = requests.get(url=url, headers=headers, timeout=settings.TIMEOUT, stream=True)
        else:
            if application_type:
                headers = {"Accept": f"application/{application_type}"}
                r = requests.get(url=url, headers=headers, timeout=settings.TIMEOUT, stream=True)
            else:
                r = requests.get(url=url, timeout=settings.TIMEOUT, stream=True)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError as e:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=settings.API_URL + "research-areas/", timeout=settings.TIMEOUT)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def post_request(url, data):
    """
    Function that performs post request with error handling.
    :param url: str -> url.
    :param data: dict -> input data.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    try:
        r = requests.post(url=url, headers=headers, data=data, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError as e:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=settings.API_URL + "research-areas/", timeout=settings.TIMEOUT)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def post_request_with_file(url, file):
    """
    Function that performs post request for uploading file with error handling.
    :param url: str -> url.
    :param file: str -> path to the zip file.
    :return: Response object -> response
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    files = {'file': open(file, 'rb')}
    try:
        r = requests.post(url=url, headers=headers, files=files, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError as e:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=settings.API_URL + "research-areas/", timeout=settings.TIMEOUT)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def post_request_with_data_and_file(url, file, data):
    """
    Function that performs post request for uploading file with error handling.
    :param url: str -> url.
    :param file: str -> path to the zip file.
    :param data: dict -> input data.
    :return: Response object -> response
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    files = {'file': open(file, 'rb')}
    try:
        r = requests.post(url=url, headers=headers, data=data, files=files, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError as e:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=settings.API_URL + "research-areas/", timeout=settings.TIMEOUT)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def delete_request(url):
    """
    Function that performs delete request with error handling.
    :param url: str -> url.
    :return: Response object -> response
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    try:
        r = requests.delete(url=url, headers=headers, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError as e:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=settings.API_URL + "research-areas/", timeout=settings.TIMEOUT)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def put_request(url, data, use_token=False):
    """
    Function that performs put request with error handling.
    :param url: str -> url.
    :param use_token: boolean -> if True the token will be passed into headers.
    :param data: dict -> input data.
    :return: Response object -> response
    """
    r = None   # initialize request as empty
    try:
        if use_token:
            headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
            r = requests.put(url=url, data=data, headers=headers, timeout=settings.TIMEOUT)
        else:
            r = requests.put(url=url, data=data, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError as e:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=settings.API_URL + "research-areas/", timeout=settings.TIMEOUT)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def check_for_status(job_url):
    """
    Helper function that makes a number of retries in order to check
    the status of the request.
    :param job_url: str -> url for the request.
    :return: boolean -> if True the status was validate, False otherwise.
    """
    for retry in range(0, settings.RETRIES):
        time.sleep(settings.SLEEP_TIME)
        job_r = get_request(url=job_url, use_token=True)
        job_content = job_r.json()
        job_status = job_content['status']
        if job_status == "SUCCESS":
            print(job_content["output"])
            return True
    print(job_content["output"])
    return False


def get_available_enums():
    """
    Helper function for accessing all available enums in the service.
    :return: JSON -> response with dictionary of all available enums.
    """
    r = get_request(url=settings.API_URL + "enums/")
    if r:
        r_json = r.json()
        return r_json


def get_available_licenses():
    """
    Helper function that acquires all available licenses that can be used in the service.
    :returns list -> list containing all available licenses.
    """
    current_page = 1
    r = get_request(url=settings.API_URL + f"search/licenses/?page={current_page}")
    content = r.json()
    results = [record["identifier"] for record in content["results"]]

    while content["next"] is not None:
        current_page += 1
        r = get_request(url=settings.API_URL + f"search/licenses/?page={current_page}")
        content = r.json()
        results.extend([record["identifier"] for record in content["results"]])
    return results


def search_for_user_id(username):
    """
    Helper function for extracting user_id based on the username.
    :param username: str -> Rohub's username.
    :return: str -> Rohub's user id.
    """
    r = get_request(url=settings.API_URL + "users/")
    if r:
        r_json = r.json()
        try:
            results = r_json["results"]
            user_id = [result for result in results if result["username"] == username]
            if user_id:
                if len(user_id) != 1:
                    print("More than one user with the same username was found. Be careful, the retrieved"
                          " ID may not be exactly what you were looking for!")
                return user_id[0]["identifier"]
            else:
                print(f"User with username: {username} was not found!")
                return
        except KeyError as e:
            print(e)
            return
