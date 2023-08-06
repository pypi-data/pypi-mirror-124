# Standard library imports
import os
import zipfile
import json
import shutil

# Third party imports
import requests

# Internal imports
from rohub import settings, utils, memo
from rohub.ResearchObject import ResearchObject
from rohub._version import __version__


###############################################################################
#              Main Methods.                                                  #
###############################################################################

def login(username, password):
    """
    Function that handles access token generation and results in saving token information.
    :param username: str -> username.
    :param password: str -> password.
    """
    url = settings.KEYCLOAK_URL
    settings.USERNAME = username
    settings.PASSWORD = password
    data = {'client_id': settings.KEYCLOAK_CLIENT_ID,
            'username': settings.USERNAME,
            'password': settings.PASSWORD,
            'grant_type': settings.GRANT_TYPE}
    try:
        r = requests.post(url, data=data, timeout=settings.TIMEOUT)
        r.raise_for_status()
        r_json = r.json()
        settings.ACCESS_TOKEN = r_json.get('access_token')
        settings.ACCESS_TOKEN_VALID_TO = utils.valid_to(exp_time=r_json.get('expires_in'))
        settings.REFRESH_TOKEN = r_json.get('refresh_token')
        settings.REFRESH_TOKEN_VALID_TO = utils.valid_to(exp_time=r_json.get('refresh_expires_in'))
        settings.TOKEN_TYPE = r_json.get('token_type')
        settings.SESSION_STATE = r_json.get('session_state')
        print(f"Logged successfully as {username}.")
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        print(e.response.text)
    except requests.exceptions.ConnectionError as e:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url, data=data, timeout=settings.TIMEOUT)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def whoami():
    """
    Function that returns information about the user that is currently logged in.
    :return: str -> username.
    """
    if settings.USERNAME:
        return settings.USERNAME
    else:
        return "Currently not logged in!"


def version():
    """
    Displays the current package version.
    :return str -> information regarding package version.
    """
    return f"You are currently using package {__version__}."


def set_retries(number_of_retries):
    """
    Function for setting up number of retries.
    :param number_of_retries: int -> number of retries
    """
    if not isinstance(number_of_retries, int):
        print(f"number_of_retries has to be an integer, not {type(number_of_retries)}!")
    else:
        settings.RETRIES = number_of_retries
        print(f"number of retries is now changed to {settings.RETRIES}.")


def set_sleep_time(sleep_time):
    """
    Function for setting up sleep time.
    :param sleep_time: int -> sleep time in seconds.
    """
    if not isinstance(sleep_time, int):
        print(f"sleep_time has to be an integer, not {type(sleep_time)}!")
    else:
        settings.SLEEP_TIME = sleep_time
        print(f"sleep_time is now changed to {settings.SLEEP_TIME}.")


def owned():
    """
    Function that is getting a list of Research Objects owned by the current user.
    :return JSON -> response containing list of Research Objects that belongs to a
    current user.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + "ros/owned/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def is_job_success(job_id):
    """
    Helper function for checking if job succeeded.
    :param job_id: str -> job's id.
    :return: JSON -> response containing job response object.
    """
    job_url = settings.API_URL + f"jobs/{job_id}/"
    job_r = utils.get_request(url=job_url, use_token=True)
    job_content = job_r.json()
    job_status = job_content['status']
    if job_status == "SUCCESS":
        return job_content
    else:
        job_success = utils.check_for_status(job_url=job_url)
        if job_success:
            # updating response after success.
            job_r = utils.get_request(url=job_url, use_token=True)
            job_content = job_r.json()
            return job_content
        else:
            msg = "Couldn't validate if uploading ended up with a success!"
            raise SystemExit(msg)


def show_user_id(username=None):
    """
    Function that shows user's id in rohub based on the username.
    :param username: str -> username. By default search for currently logged user.
    :return: str -> user's id.
    """
    if utils.is_valid(token_type="access"):
        if not username:
            url = settings.API_URL + "users/whoami/"
            r = utils.get_request(url=url, use_token=True)
            content = r.json()
            try:
                user_id = content["identifier"]
            except KeyError as e:
                print("Ups... something went wrong. Couldn't read user's id from response.")
                print(e)
                return
        else:
            user_id = utils.search_for_user_id(username=username)
        return user_id
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


###############################################################################
#              ROS main methods.                                              #
###############################################################################


def search_ros_by_id(identifier):
    """
    Function that makes a query for Research Object based on given id.
    :param identifier: str -> Research Object's id.
    :return: JSON -> response containing Research Object for requested id.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_create(title, research_areas, description=None, access_mode=None,
               ros_type=None, template=None, owner=None, editors=None,
               readers=None, creation_mode=None):
    """
    Function that creates new Research Object.
    :param title: str -> title for the Research Object.
    :param research_areas: list -> list of research areas connected to the ResearchObject.
    :param description: str -> ResearchObject's description.
    :param access_mode: str -> ResearchObject's access mode.
    :param ros_type: str -> ResearchObject's type.
    :param template: str -> ResearchObject's template.
    :param owner: str -> ResearchObject's owner.
    :param editors: list -> ResearchObject's list of editors.
    :param readers: list -> ResearchObject's list of readers.
    :param creation_mode: str -> ResearchObject's creation mode.
    :return: ResearchObject class instance.
    """
    return ResearchObject.ResearchObject(title=title, research_areas=research_areas,
                                         description=description, access_mode=access_mode,
                                         ros_type=ros_type, template=template, owner=owner,
                                         editors=editors, readers=readers, creation_mode=creation_mode,
                                         post_request=True)


def ros_load(identifier):
    """
    Function that loads existing Research Object into Python class.
    :param identifier: str -> ResearchObject's identifier.
    :return: ResearchObject class instance.
    """
    return ResearchObject.ResearchObject(identifier=identifier, post_request=False)


def ros_content(identifier):
    """
    Function that retrieves content of the Research Object based on the id.
    :param identifier: str -> Research Object's id.
    :return: JSON -> response with content of the Research Object.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/content/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_full_metadata(identifier):
    """
    Function that retrieves full metadata of the Research Object based on id.
    :param identifier: str -> Research Object's id.
    :return: JSON -> response with full metadata of the Research Object.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/full/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_fork(identifier, title=None, description=None, create_doi=None, publication_services=None):
    """
    Function that creates a Research Object's fork.
    :param identifier: str -> Research Object's id.
    :param title: str ->  title for the Research Object.
    :param description: str -> description.
    :param create_doi: boolean -> doi is created if True, False otherwise.
    :param publication_services: list -> name of the service.
    :return: str -> id for forked Research Object.
    """
    if create_doi:
        if not isinstance(create_doi, bool):
            msg = f"create_doi parameter has to be a boolean type, not a {type(create_doi)}"
            raise SystemExit(msg)
    if publication_services:
        if not memo.service_enums:
            memo.service_enums = utils.get_available_enums()
        available_enums = memo.service_enums
        try:
            available_services = available_enums["publication_service"]
            publication_services = [s.upper() for s in publication_services if s.upper() in available_services]
            if len(publication_services) == 0:
                publication_services = None
        except KeyError as e:
            print(f"Couldn't validate publication_services value! Omitting this parameter.")
            print(e)
            publication_services = None
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/evolution/"
        data = {"status": "FORK",
                "title": title,
                "description": description,
                "create_doi": create_doi,
                "publication_services": publication_services}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        job_id = content["identifier"]
        if job_id:
            fork_response = is_job_success(job_id=job_id)
            forked_results = fork_response.get("results")
            if forked_results:
                forked_ros_id = forked_results.split("/")[-2]
                return forked_ros_id
        else:
            msg = "Incorrect job response, couldn't validate if file was uploaded or not."
            raise SystemExit(msg)


def ros_snapshot(identifier, title=None, description=None, create_doi=None, publication_services=None):
    """
    Function that creates a Research Object's snapshot.
    :param identifier: str -> Research Object's id.
    :param title: str ->  title for the Research Object.
    :param description: str -> description.
    :param create_doi: boolean -> doi is created if True, False otherwise.
    :param publication_services: list -> name of the service.
    :return: str -> id of snapshot.
    """
    if create_doi:
        if not isinstance(create_doi, bool):
            msg = f"create_doi parameter has to be a boolean type, not a {type(create_doi)}"
            raise SystemExit(msg)
    if publication_services:
        if not memo.service_enums:
            memo.service_enums = utils.get_available_enums()
        available_enums = memo.service_enums
        try:
            available_services = available_enums["publication_service"]
            publication_services = [s.upper() for s in publication_services if s.upper() in available_services]
            if len(publication_services) == 0:
                publication_services = None
        except KeyError as e:
            print(f"Couldn't validate publication_services value! Omitting this parameter.")
            print(e)
            publication_services = None
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/evolution/"
        data = {"status": "SNAPSHOT",
                "title": title,
                "description": description,
                "create_doi": create_doi,
                "publication_services": publication_services}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        job_id = content["identifier"]
        if job_id:
            snapshot_response = is_job_success(job_id=job_id)
            snapshot_results = snapshot_response.get("results")
            if snapshot_results:
                snapshot_ros_id = snapshot_results.split("/")[-2]
                return snapshot_ros_id
        else:
            msg = "Incorrect job response, couldn't validate if file was uploaded or not."
            raise SystemExit(msg)


def ros_archive(identifier, title=None, description=None, create_doi=None, publication_services=None):
    """
    Function that creates a Research Object's archive.
    :param identifier: str -> Research Object's id.
    :param title: str ->  title for the Research Object.
    :param description: str -> description.
    :param create_doi: boolean -> doi is created if True, False otherwise.
    :param publication_services: list -> name of the service.
    :return: id of archived Research Object
    """
    if create_doi:
        if not isinstance(create_doi, bool):
            msg = f"create_doi parameter has to be a boolean type, not a {type(create_doi)}"
            raise SystemExit(msg)
    if publication_services:
        if not memo.service_enums:
            memo.service_enums = utils.get_available_enums()
        available_enums = memo.service_enums
        try:
            available_services = available_enums["publication_service"]
            publication_services = [s.upper() for s in publication_services if s.upper() in available_services]
            if len(publication_services) == 0:
                publication_services = None
        except KeyError as e:
            print(f"Couldn't validate publication_services value! Omitting this parameter.")
            print(e)
            publication_services = None
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/evolution/"
        data = {"status": "ARCHIVE",
                "title": title,
                "description": description,
                "create_doi": create_doi,
                "publication_services": publication_services}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        job_id = content["identifier"]
        if job_id:
            archive_response = is_job_success(job_id=job_id)
            archive_results = archive_response.get("results")
            if archive_results:
                archive_ros_id = archive_results.split("/")[-2]
                return archive_ros_id
        else:
            msg = "Incorrect job response, couldn't validate if file was uploaded or not."
            raise SystemExit(msg)


def ros_show_publications(identifier):
    """
    Function that shows publication details for a certain publication id.
    :param identifier: str -> publication's id.
    :return: list -> useful information from publications response.
    """
    url = settings.API_URL + f"ros/{identifier}/publications/"
    r = utils.get_request(url=url, use_token=False)
    content = r.json()
    results = content.get("results")
    publications = []
    for result in results:
        publications.append({"doi": result.get("doi"),
                             "storage": result.get("storage"),
                             "url": result.get("url")})
    return publications


def ros_show_triple_details(identifier):
    """
    Function that shows details for specific triple.
    :param identifier: str -> triple's id.
    :return: JSON response with triple details.
    """
    url = settings.API_URL + f"triples/{identifier}"
    r = utils.get_request(url=url, use_token=False)
    content = r.json()
    return content


def ros_show_annotations(identifier):
    """
    Function that shows all available annotations for given Research Object.
    :param identifier: str -> Research Object's id.
    :return: list -> useful information from annotations response.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/annotations/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        results = content.get("results")
        annotations = []
        for result in results:
            annotations.append({"identifier": result.get("identifier"),
                                "name": result.get("name"),
                                "filename": result.get("filename"),
                                "created": result.get("created"),
                                "creator": result.get("creator")})
        return annotations
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_show_triples(identifier):
    """
    Function that shows all triples related to specific annotation.
    :param identifier: str -> annotation's id.
    :return: list -> useful information regarding triples.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"annotations/{identifier}/body/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        results = content.get("results")
        triples = []
        for result in results:
            triples.append({"identifier": result.get("identifier"),
                            "subject": result.get("subject"),
                            "predicate": result.get("predicate"),
                            "object": result.get("object"),
                            "created_by": result.get("created_by"),
                            "created_on": result.get("created_on")})
        return triples
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_show_authors(identifier):
    """
    Function for displaying authors for given Research Object.
    :param identifier: str -> str -> Research Object's id.
    :return: JSON response with authors details.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/authors/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_show_contributors(identifier):
    """
    Function for displaying contributors for given Research Object.
    :param identifier: str -> str -> Research Object's id.
    :return: JSON response with authors details.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/contributors/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_show_copyright(identifier):
    """
    Function for displaying copyright for given Research Object.
    :param identifier: str -> str -> Research Object's id.
    :return: JSON response with copyright details.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/copyright/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_show_funding(identifier):
    """
    Function for displaying funding information for given Research Object.
    :param identifier: str -> str -> Research Object's id.
    :return: JSON response with funding details.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/funding/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_show_license(identifier):
    """
    Function for displaying license information for given Research Object.
    :param identifier: identifier: str -> str -> Research Object's id.
    :return: JSON response with funding details.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/license/"
        r = utils.get_request(url=url, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_export_to_rocrate(identifier, filename=None, path=None, use_format=settings.EXPORT_TO_ROCRATE_DEFAULT_FORMAT):
    """
    Function for downloading Research Object meta-data as RO-crate.
    :param identifier: str -> Research Object's id.
    :param filename: str -> name for the file that will be acquired (without extension).
    If not provided username will be used instead.
    :param path: str -> path where file should be downloaded. Default is cwd.
    :param use_format: str -> format choice. Either json-ld or zip.
    """
    if not filename:
        filename = settings.USERNAME
    if path:
        os.makedirs(path, exist_ok=True)
        full_path = os.path.join(path, filename)
    else:
        full_path = os.path.join(filename)
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/crate/download/"
        if use_format == "json-ld":
            r = utils.get_file_request(url=url, use_token=True)
            with open(f'{full_path}.jsonld', 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            del r
            if path:
                print(f"File was successfully downloaded into {path}.")
            else:
                print(f"File was successfully downloaded.")
        elif use_format == "zip":
            r = utils.get_file_request(url=url, use_token=True, application_type="zip")
            with open(f'{full_path}.zip', 'wb') as out_file:
                out_file.write(r.content)
            del r
            if path:
                print(f"File was successfully downloaded into {path}.")
            else:
                print(f"File was successfully downloaded.")
        else:
            print(f"Incorrect use_format. Has to be one of: json-ld, zip. Instead {use_format} was passed.")
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


###############################################################################
#              ROS add methods.                                               #
###############################################################################


def ros_add_geolocation(identifier, body_specification_json=None):
    """
    Function that adds geolocation to the existing Research Object.
    :param identifier: str -> Research Object's id.
    :param body_specification_json: path to JSON file or Python serializable object that
    will be converted into JSON.
    :return: JSON -> response with content of the Research Object.
    """
    if body_specification_json:
        if isinstance(body_specification_json, str):
            if os.path.isfile(body_specification_json):
                file = open(body_specification_json)
                body_specification_json = file.read()
        elif isinstance(body_specification_json, (dict, list)):
            body_specification_json = json.dumps(body_specification_json)
        else:
            print(f"Unexpected type of body_specification_json parameter. {type(body_specification_json)} was passed and"
                  f" string (path to file) or dictionary was expected!. Leaving body_specification_json value empty.")
            body_specification_json = None
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/geolocation/"
        data = {"ro": identifier,
                "body_specification_json": body_specification_json}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_folders(identifier, name, description=None, parent_folder=None):
    """
    Function that adds folders to the existing Research Object.
    :param identifier: str -> Research Object's id.
    :param name: str -> name of the folder.
    :param description: str -> description.
    :param parent_folder: str -> name of the parent folder.
    :return: JSON -> response with content of the Research Object.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/folders/"
        data = {"ro": identifier,
                "name": name,
                "description": description,
                "parent_folder": parent_folder}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_annotations(identifier, resources=None, body_specification_json=None):
    """
    Function that adds annotations to the existing Research Object.
    :param identifier: str -> Research Object's id.
    :param resources list -> list of Research Object's resources.
    :param body_specification_json: path to JSON file or Python serializable object that
    will be converted into JSON.
    :return: JSON -> response with content of the Research Object.
    """
    if body_specification_json:
        if isinstance(body_specification_json, str):
            if os.path.isfile(body_specification_json):
                file = open(body_specification_json)
                body_specification_json = file.read()
        elif isinstance(body_specification_json, (dict, list)):
            body_specification_json = json.dumps(body_specification_json)
        else:
            print(f"Unexpected type of body_specification_json parameter. {type(body_specification_json)} was passed and"
                  f" string (path to file) or dictionary was expected!. Leaving body_specification_json value empty.")
            body_specification_json = None
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/annotations/"
        print(body_specification_json)
        data = {"ro": identifier,
                "resources": resources,
                "body_specification_json": body_specification_json}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_internal_resource(identifier, res_type, file_path, title=None, folder=None, description=None):
    """
    Function that adds internal resource to the existing Research Object.
    :param identifier: str -> Research Object's id.
    :param res_type: str -> resource type.
    :param file_path: str -> path to the resource file.
    :param title: str -> title.
    :param folder: str -> folder id.
    :param description: str -> description.
    :return: JSON -> response with content of the Resource.
    """
    if not memo.service_enums:
        memo.service_enums = utils.get_available_enums()
    available_enums = memo.service_enums
    try:
        available_res_types = available_enums["resource_type"]
        if res_type not in available_res_types:
            msg = f"Incorrect resource type. Must be one of: {available_res_types}"
            raise SystemExit(msg)
    except KeyError as e:
        msg = f"Couldn't validate resource_type value!"
        raise SystemExit(msg)
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/resources/"
        data = {"ro": identifier,
                "folder": folder,
                "type": res_type,
                "title": title,
                "description": description}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request_with_data_and_file(url=url, data=data, file=file_path)
        content = r.json()
        return {"identifier": content.get("identifier"),
                "title": content.get("title"),
                "folder": content.get("folder"),
                "ros": content.get("ros"),
                "description": content.get("description"),
                "url": content.get("url"),
                "name": content.get("name"),
                "filename": content.get("filename"),
                "path": content.get("path"),
                "size": content.get("size"),
                "download_url": content.get("download_url"),
                "type": content.get("type"),
                "doi": content.get("doi"),
                "read_only": content.get("read_only"),
                "cloned": content.get("cloned"),
                "api_link": content.get("api_link")}
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_external_resource(identifier, res_type, input_url, title=None, folder=None, description=None):
    """
    Function that adds external resource to the existing Research Object.
    :param identifier: str -> Research Object's id.
    :param res_type: str -> resource type.
    :param input_url: str -> url to the resource.
    :param title: str -> title.
    :param folder: str -> folder id.
    :param description: str -> description.
    :return: JSON -> response with content of the Resource.
    """
    if not memo.service_enums:
        memo.service_enums = utils.get_available_enums()
    available_enums = memo.service_enums
    try:
        available_res_types = available_enums["resource_type"]
        if res_type not in available_res_types:
            msg = f"Incorrect resource type. Must be one of: {available_res_types}"
            raise SystemExit(msg)
    except KeyError as e:
        msg = f"Couldn't validate resource_type value!"
        raise SystemExit(msg)
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/resources/"
        data = {"ro": identifier,
                "folder": folder,
                "type": res_type,
                "title": title,
                "url": input_url,
                "description": description}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return {"identifier": content.get("identifier"),
                "title": content.get("title"),
                "folder": content.get("folder"),
                "ros": content.get("ros"),
                "description": content.get("description"),
                "url": content.get("url"),
                "name": content.get("name"),
                "filename": content.get("filename"),
                "path": content.get("path"),
                "size": content.get("size"),
                "download_url": content.get("download_url"),
                "type": content.get("type"),
                "doi": content.get("doi"),
                "read_only": content.get("read_only"),
                "cloned": content.get("cloned"),
                "api_link": content.get("api_link")}
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_triple(the_subject, the_predicate, the_object, annotation_id, object_class=None):
    """
    Function that adds triple to the given annotation.
    :param the_subject: str -> subject.
    :param the_predicate: str -> predicate.
    :param the_object: str -> object.
    :param annotation_id: str -> annotation's id.
    :param object_class: str -> object's class.
    :return: JSON -> response with content of the triple.
    """
    if object_class:
        if not memo.service_enums:
            memo.service_enums = utils.get_available_enums()
        available_enums = memo.service_enums
        try:
            available_object_classes = available_enums["triple_object_class"]
            if object_class not in available_object_classes:
                msg = f"Incorrect object class. Must be one of: {available_object_classes}"
                raise SystemExit(msg)
        except KeyError as e:
            msg = f"Couldn't validate object_class value!"
            raise SystemExit(msg)
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + "triples/"
        data = {"subject": the_subject,
                "predicate": the_predicate,
                "object": the_object,
                "object_class": object_class,
                "annotation": annotation_id}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_author(identifier, predicate=None, user=None, display_name=None):
    """
    Function that adds author to the Research Object.
    :param identifier: str -> Research Object's id.
    :param predicate: str -> predicate.
    :param user: str -> Rohub's user ID (mutually exclusive with display_name!)
    :param display_name: str -> author name, for cases where author is not a Rohub user
    (mutually exclusive with user!)
    :return: JSON -> response with content.
    """
    if user and display_name:
        print("User and display_name parameters are mutually exclusive! Read doc-string to make yourself familiar"
              " with the usage.")
        return
    if not user and not display_name:
        print("Either user or display_name parameter has to be provided. Please check doc-string for usage details.")
        return
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/authors/"
        data = {"ro": identifier,
                "predicate": predicate,
                "user": user,
                "display_name": display_name}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_contributor(identifier, predicate=None, user=None, display_name=None):
    """
    Function that adds contributor to the Research Object.
    :param identifier: str -> Research Object's id.
    :param predicate: str -> predicate.
    :param user: str -> Rohub's user ID (mutually exclusive with display_name!)
    :param display_name: str -> author name, for cases where author is not a Rohub user
    (mutually exclusive with user!)
    :return: JSON -> response with content.
    """
    if user and display_name:
        print("User and display_name parameters are mutually exclusive! Read doc-string to make yourself familiar"
              " with the usage.")
        return
    if not user and not display_name:
        print("Either user or display_name parameter has to be provided. Please check doc-string for usage details.")
        return
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/contributors/"
        data = {"ro": identifier,
                "predicate": predicate,
                "user": user,
                "display_name": display_name}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_copyright(identifier, predicate=None, user=None, display_name=None):
    """
    Function that adds copyright to the Research Object.
    :param identifier: str -> Research Object's id.
    :param predicate: str -> predicate.
    :param user: str -> Rohub's user ID (mutually exclusive with display_name!)
    :param display_name: str -> author name, for cases where author is not a Rohub user
    (mutually exclusive with user!)
    :return: JSON -> response with content.
    """
    if user and display_name:
        print("User and display_name parameters are mutually exclusive! Read doc-string to make yourself familiar"
              " with the usage.")
        return
    if not user and not display_name:
        print("Either user or display_name parameter has to be provided. Please check doc-string for usage details.")
        return
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/copyright/"
        data = {"ro": identifier,
                "predicate": predicate,
                "user": user,
                "display_name": display_name}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_funding(identifier, grant_identifier, grant_name, funder_name, grant_title=None, funder_doi=None):
    """
    Function that adds funding information to the Research Object.
    NOTE: two auxiliary functions can be used to get some examples for funders and grants
    from the Zenodo database, respectively:
        - zenodo_show_funders()
        - zenodo_show_grants()
    check docstrings for usage details.
    :param identifier: str -> Research Object's identifier.
    :param grant_identifier: str -> grant's id.
    :param grant_name: str -> grant's name.
    :param funder_name: str -> funder's name.
    :param grant_title: str -> grant's title.
    :param funder_doi: str -> funder's doi.
    :return: JSON -> response with content.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/funding/"
        data = {"grant_identifier": grant_identifier,
                "grant_name": grant_name,
                "grant_title": grant_title,
                "funder_doi": funder_doi,
                "funder_name": funder_name}
        data = {key: value for key, value in data.items() if value is not None}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_add_license(ros_id, license_id):
    """
    Function that adds license information to the Research Object.
    :param ros_id: str -> Research Object's id.
    :param license_id: str -> license id.
    :return: JSON -> response with content.
    """
    if not memo.licenses:
        memo.licenses = utils.get_available_licenses()
    if license_id not in memo.licenses:
        print("Incorrect license_id! You can check all available license options by running "
              " show_available_licenses().")
        return
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{ros_id}/license/"
        data = {"identifier": license_id}
        r = utils.post_request(url=url, data=data)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


###############################################################################
#              ROS upload methods.                                            #
###############################################################################


def ros_upload(path_to_zip):
    """
    Function that enables uploading zip archive in order to create a new ResearchObject.
    :param path_to_zip: str -> path to the zip package that will be uploaded.
    :return: JSON -> response from the upload endpoint.
    """
    if os.path.isfile(path_to_zip):
        if zipfile.is_zipfile(path_to_zip):
            if utils.is_valid(token_type="access"):
                url = settings.API_URL + f"ros/upload/"
                r = utils.post_request_with_file(url=url, file=path_to_zip)
                content = r.json()
                job_id = content['identifier']
                if job_id:
                    return is_job_success(job_id=job_id)
                else:
                    msg = "Incorrect job response, couldn't validate if file was uploaded or not."
                    raise SystemExit(msg)
            else:
                msg = "Your current access token is either missing or expired, please log into" \
                      " rohub again"
                raise SystemExit(msg)
        else:
            print("The file that was provided is not a real zip file! "
                  "Pleas try again with proper zip file.")
    else:
        print("Zip file doesn't exist! Please make sure passed path is correct!")


def ros_upload_resources(identifier, path_to_zip):
    """
    Function that enables uploading zip archive in order to create a new resource fo the ResearchObject.
    :param identifier: str -> Research Object's id.
    :param path_to_zip: str -> path to the zip package that will be uploaded.
    :return: JSON -> response from the upload endpoint.
    """
    if os.path.isfile(path_to_zip):
        if zipfile.is_zipfile(path_to_zip):
            if utils.is_valid(token_type="access"):
                url = settings.API_URL + f"ros/{identifier}/resources/upload/"
                r = utils.post_request_with_file(url=url, file=path_to_zip)
                content = r.json()
                job_id = content['identifier']
                if job_id:
                    return is_job_success(job_id=job_id)
                else:
                    msg = "Incorrect job response, couldn't validate if file was uploaded or not."
                    raise SystemExit(msg)
            else:
                msg = "Your current access token is either missing or expired, please log into" \
                      " rohub again"
                raise SystemExit(msg)
        else:
            print("The file that was provided is not a real zip file! "
                  "Pleas try again with proper zip file.")
    else:
        print("Zip file doesn't exist! Please make sure passed path is correct!")

###############################################################################
#              ROS delete methods.                                            #
###############################################################################


def ros_delete(identifier):
    """
    Function that deletes a Research Object with given id.
    :param identifier: str -> Research Object's id.
    :return: JSON -> response from the delete endpoint.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/"
        r = utils.delete_request(url=url)
        content = r.json()
        job_id = content['identifier']
        if job_id:
            return is_job_success(job_id=job_id)
        else:
            msg = "Incorrect job response, couldn't validate if file was uploaded or not."
            raise SystemExit(msg)
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_delete_folder(folder_identifier):
    """
    Function that deletes a folder within given Research Object.
    :param folder_identifier: str -> folder identifier.
    :return: JSON -> response from the delete endpoint.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"folders/{folder_identifier}/"
        r = utils.delete_request(url=url)
        if r.status_code != 204:
            content = r.json()
            return content
        else:
            print("Resource successfully deleted!")
            return
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_delete_resource(resource_identifier):
    """
    Function that deletes a resource within given Research Object.
    :param resource_identifier: str -> resource identifier.
    :return: JSON -> response from the delete endpoint.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"resources/{resource_identifier}/"
        r = utils.delete_request(url=url)
        if r.status_code != 204:
            content = r.json()
            return content
        else:
            print("Resource successfully deleted!")
            return
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


def ros_delete_annotation(annotation_identifier):
    """
    Function that deletes an annotation within given Research Object.
    :param annotation_identifier: str -> resource identifier.
    :return: JSON -> response from the delete endpoint.
    """
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"annotations/{annotation_identifier}/"
        r = utils.delete_request(url=url)
        if r.status_code != 204:
            content = r.json()
            return content
        else:
            print("Resource successfully deleted!")
            return
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


###############################################################################
#              ROS put methods.                                               #
###############################################################################

def ros_update(identifier, title, research_areas, description=None, access_mode=None,
               ros_type=None, template=None, owner=None, editors=None,
               readers=None, creation_mode=None):
    """
    Function for updating Research Object.
    :param identifier: str -> Research Object's identifier.
    :param title: str -> title for the Research Object.
    :param research_areas: list -> list of research areas connected to the ResearchObject.
    :param description: str -> ResearchObject's description.
    :param access_mode: str -> ResearchObject's access mode.
    :param ros_type: str -> ResearchObject's type.
    :param template: str -> ResearchObject's template.
    :param owner: str -> ResearchObject's owner.
    :param editors: list -> ResearchObject's list of editors.
    :param readers: list -> ResearchObject's list of readers.
    :param creation_mode: str -> ResearchObject's creation mode.
    :return: JSON -> response from the put endpoint.
    """
    data = {"title": title,
            "research_areas": research_areas,
            "description": description,
            "access_mode": access_mode,
            "type": ros_type,
            "template": template,
            "owner": owner,
            "editors": editors,
            "readers": readers,
            "creation_mode": creation_mode}
    data = {key: value for key, value in data.items() if value is not None}
    if utils.is_valid(token_type="access"):
        url = settings.API_URL + f"ros/{identifier}/"
        r = utils.put_request(url=url, data=data, use_token=True)
        content = r.json()
        return content
    else:
        msg = "Your current access token is either missing or expired, please log into" \
              " rohub again"
        raise SystemExit(msg)


###############################################################################
#              Auxiliary methods.                                             #
###############################################################################

def zenodo_show_funders(number_of_results=settings.ZENODO_FUNDER_RESULTS_DEFAULT):
    """
    Function for displaying list of funders that is available through the Zenodo.
    :param number_of_results: int -> number of first x results that should be displayed. Up to 100.
    :return: dict containing selected information.
    """
    if int(number_of_results) > 100:
        number_of_results = 100   # 100 is max!
    elif int(number_of_results) < 1:
        number_of_results = 1  # 1 is min !
    base_url = settings.ZENODO_FUNDERS_URL
    url = base_url + f"?sort=bestmatch&page=1&size={number_of_results}"
    r = utils.get_request(url=url, use_token=False)
    content = r.json()
    results = {}
    counter = 1
    while counter <= number_of_results:
        for hit in content["hits"]["hits"]:
            api_url = hit.get("links").get("self")
            acronym = hit.get("metadata").get("acronyms")
            identifiers = hit.get("metadata").get("identifiers")
            name = hit.get("metadata").get("name")
            doi = hit.get("metadata").get("doi")
            results.update({counter: {"api_url": api_url,
                                      "acronym": acronym,
                                      "identifiers": identifiers,
                                      "name": name,
                                      "doi": doi
                                      }})
            counter += 1
    return results


def zenodo_show_grants(number_of_results=settings.ZENODO_GRANT_RESULTS_DEFAULT):
    """
    Function for displaying list of grants that is available through the Zenodo.
    :param number_of_results: int -> number of first x results that should be displayed. Up to 100.
    :return: dict containing selected information.
    """
    if int(number_of_results) > 100:
        number_of_results = 100   # 100 is max!
    elif int(number_of_results) < 1:
        number_of_results = 1  # 1 is min !
    base_url = settings.ZENODO_GRANTS_URL
    url = base_url + f"?sort=bestmatch&page=1&size={number_of_results}"
    r = utils.get_request(url=url, use_token=False)
    content = r.json()
    results = {}
    counter = 1
    while counter <= number_of_results:
        for hit in content["hits"]["hits"]:
            api_url = hit.get("links").get("self")
            acronym = hit.get("metadata").get("acronym")
            identifiers = hit.get("metadata").get("identifiers")
            title = hit.get("metadata").get("title")
            funder = hit.get("metadata").get("funder").get("name")
            results.update({counter: {"api_url": api_url,
                                      "acronym": acronym,
                                      "identifiers": identifiers,
                                      "title": title,
                                      "funder": funder
                                      }})
            counter += 1
    return results


def show_available_licenses():
    """
    Function that shows all available options for the license id that can be used in ros_add_license method.
    :return: list -> list of all available licenses.
    """
    if not memo.licenses:
        memo.licenses = utils.get_available_licenses()
    return memo.licenses
