from rohub import utils
from rohub import settings
from rohub import rohub


class ResearchObject(object):
    def __init__(self, title=None, research_areas=None, description=None, access_mode=None,
                 ros_type=None, template=None, owner=None, editors=None,
                 readers=None, creation_mode=None, identifier=None, post_request=True):
        if self._is_valid():
            # Main.
            self.valid_research_areas = []
            self.available_enums = None
            self.roi_response_content = {}

            if post_request:
                # Required attributes
                self.title = str(title)
                self.research_areas = self._get_valid_research_areas(research_areas=research_areas)
                # Optional attributes with default value.
                if description:
                    self.description = str(description)
                else:
                    self.description = None
                if owner:
                    self.owner = str(owner)
                else:
                    self.owner = None
                if access_mode:
                    self.access_mode = self._validate_and_set_access_mode(access_mode=str(access_mode))
                else:
                    self.access_mode = None
                if ros_type:
                    self.ros_type = self._validate_and_set_ros_type(ros_type=str(ros_type))
                else:
                    self.ros_type = None
                if template:
                    self.template = self._validate_and_set_template(template=str(template))
                else:
                    self.template = None
                if editors:
                    self.editors = list(editors)
                else:
                    self.editors = None
                if readers:
                    self.readers = list(readers)
                else:
                    self.readers = None
                if creation_mode:
                    self.creation_mode = self._validate_and_set_creation_mode(
                        creation_mode=str(creation_mode))
                else:
                    self.creation_mode = None

                # Crating new Research Object.
                self._post_research_object()
            else:
                self.__identifier = identifier
                # Loading existing Research Object.
                self._load_research_object()

            # Updating required attributes with values from the response.
            self.title = self.roi_response_content.get("title")
            self.research_areas = self.roi_response_content.get("research_areas")

            # Updating optional attributes with values from the response.
            self.description = self.roi_response_content.get("description")
            self.access_mode = self.roi_response_content.get("access_mode")
            self.ros_type = self.roi_response_content.get("type")
            self.template = self.roi_response_content.get("template")
            self.owner = self.roi_response_content.get("owner")
            self.editors = self.roi_response_content.get("editors")
            self.readers = self.roi_response_content.get("readers")
            self.creation_mode = self.roi_response_content.get("creation_mode")

            # ReadOnly attributes; will be updated after request post.
            self.__identifier = self.roi_response_content.get("identifier")
            self.__shared_link = self.roi_response_content.get("shared_link")
            self.__status = self.roi_response_content.get("status")
            self.__created = self.roi_response_content.get("created")
            self.__creator = self.roi_response_content.get("creator")
            self.__modificator = self.roi_response_content.get("modificator")
            self.__modified = self.roi_response_content.get("modified")
            self.__importer = self.roi_response_content.get("importer")
            self.__rating = self.roi_response_content.get("rating")
            self.__number_of_ratings = self.roi_response_content.get("number_of_ratings")
            self.__number_of_likes = self.roi_response_content.get("number_of_likes")
            self.__number_of_dislikes = self.roi_response_content.get("number_of_dislikes")
            self.__quality = self.roi_response_content.get("quality")
            self.__size = self.roi_response_content.get("size")
            self.__doi = self.roi_response_content.get("doi")
            self.__api_link = self.roi_response_content.get("api_link")

            # Full Meta-Data.
            self.created_by = None
            self.metadata = None
            self.contributors_credits = None
            self.authors_credits = None
            self.number_of_all_aggregates = None
            self.number_of_resources = None
            self.original_created_on = None
            self.parent_ro = None
            self.contributed_by = None
            self.number_of_views = None
            self.number_of_forks = None
            self.authored_by = None
            self.snapshotter = None
            self.user_liked = None
            self.cloned = None
            self.archived = None
            self.contributors = None
            self.geolocation = None
            self.read_only = None
            self.created_on = None
            self.credits = None
            self.forker = None
            self.number_of_downloads = None
            self.number_of_folders = None
            self.original_created_by = None
            self.golden = None
            self.archiver = None
            self.forked = None
            self.number_of_events = None
            self.modified_on = None
            self.sketch = None
            self.user_rate = None
            self.modified_by = None
            self.original_creator_name = None
            self.imported = None
            self.snapshotted = None
            self.number_of_archives = None
            self.quality_calculated_on = None
            self.user_disliked = None
            self.number_of_snapshots = None
            self.number_of_annotations = None
            self.number_of_comments = None

            # Other Attributes.
            self.content = None
            self.geolocation_response_content = None
            self.folders_response_content = None
            self.resource_upload_response_content = None
            self.annotations_response_content = None
            self.fork_response_content = None
            self.snapshot_response_content = None
            self.archive_response_content = None
            self.delete_response_content = None
            self.delete_folder_response_content = None
            self.delete_resource_response_content = None
            self.delete_annotation_response_content = None
            self.internal_resource_response_content = None
            self.external_resource_response_content = None
            self.update_response_content = None
            self.full_metadata_response_content = None
            self.show_publication_response_content = None

            # Curated data.
            self.annotations = None

            if post_request:
                print(f"Research Object was successfully created with id = {self.identifier}")
            else:
                print(f"Research Object was successfully loaded with id = {self.identifier}")
        else:
            print('Token is no longer valid! Use login function to generate a new one!')

    def __str__(self):
        return f"Research Object with ID: {self.identifier}"

    def __repr__(self):
        return f"ResearchObject(identifier={self.identifier}, post_request=False)"

    ###############################################################################
    #              Properties.                                                    #
    ###############################################################################
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = str(value)

    @property
    def research_areas(self):
        return self.__research_areas

    @research_areas.setter
    def research_areas(self, value):
        self.__research_areas = self._get_valid_research_areas(research_areas=value)

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if value:
            self.__description = str(value)
        else:
            self.__description = None

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        if value:
            self.__owner = str(value)
        else:
            self.__owner = None

    @property
    def access_mode(self):
        return self.__access_mode

    @access_mode.setter
    def access_mode(self, value):
        if value:
            self.__access_mode = self._validate_and_set_access_mode(access_mode=str(value))
        else:
            self.__access_mode = None

    @property
    def ros_type(self):
        return self.__ros_type

    @ros_type.setter
    def ros_type(self, value):
        if value:
            self.__ros_type = self._validate_and_set_ros_type(ros_type=str(value))
        else:
            self.__ros_type = None

    @property
    def template(self):
        return self.__template

    @template.setter
    def template(self, value):
        if value:
            self.__template = self._validate_and_set_template(template=str(value))
        else:
            self.__template = None

    @property
    def editors(self):
        return self.__editors

    @editors.setter
    def editors(self, value):
        if value:
            self.__editors = list(value)
        else:
            self.__editors = None

    @property
    def readers(self):
        return self.__readers

    @readers.setter
    def readers(self, value):
        if value:
            self.__readers = list(value)
        else:
            self.__readers = None

    @property
    def creation_mode(self):
        return self.__creation_mode

    @creation_mode.setter
    def creation_mode(self, value):
        if value:
            self.__creation_mode = self._validate_and_set_creation_mode(creation_mode=str(value))
        else:
            self.__creation_mode = None

    @property
    def identifier(self):
        return self.__identifier

    @identifier.setter
    def identifier(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def shared_link(self):
        return self.__shared_link

    @shared_link.setter
    def shared_link(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def created(self):
        return self.__created

    @created.setter
    def created(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def creator(self):
        return self.__creator

    @creator.setter
    def creator(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def modificator(self):
        return self.__modificator

    @modificator.setter
    def modificator(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def modified(self):
        return self.__modified

    @modified.setter
    def modified(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def importer(self):
        return self.__importer

    @importer.setter
    def importer(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def number_of_ratings(self):
        return self.__number_of_ratings

    @number_of_ratings.setter
    def number_of_ratings(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def number_of_likes(self):
        return self.__number_of_likes

    @number_of_likes.setter
    def number_of_likes(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def number_of_dislikes(self):
        return self.__number_of_dislikes

    @number_of_dislikes.setter
    def number_of_dislikes(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def quality(self):
        return self.__quality

    @quality.setter
    def quality(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def doi(self):
        return self.__doi

    @doi.setter
    def doi(self, value):
        raise AttributeError('This is a read-only attribute!')

    @property
    def api_link(self):
        return self.__api_link

    @api_link.setter
    def api_link(self, value):
        raise AttributeError('This is a read-only attribute!')

    ###############################################################################
    #              Main Methods.                                                  #
    ###############################################################################

    @staticmethod
    def _is_valid():
        """
        Semi-Private function that checks if current token is still valid.
        :return: boolean -> True if valid, False otherwise.
        """
        return utils.is_valid(token_type="access")

    def _get_available_enums(self):
        """
        Semi-private function that acquired all available enums.
        """
        self.available_enums = utils.get_available_enums()

    def _post_research_object(self):
        """
        Semi-private function that creates post request for a research object given
        required and optional parameters.
        """
        data = {"title": self.title,
                "research_areas": self.research_areas,
                "description": self.description,
                "access_mode": self.access_mode,
                "type": self.ros_type,
                "template": self.template,
                "owner": self.owner,
                "editors": self.editors,
                "readers": self.readers,
                "creation_mode": self.creation_mode}
        data = {key: value for key, value in data.items() if value is not None}
        if self._is_valid():
            r = utils.post_request(url=settings.API_URL + "ros/", data=data)
            self.roi_response_content = r.json()
        else:
            msg = "Your current access token is either missing or expired, please log into" \
                  " rohub again"
            raise SystemExit(msg)

    def _load_research_object(self):
        """
        Semi-private function that creates get request for existing Research Object.
        """
        if self._is_valid():
            self.roi_response_content = rohub.search_ros_by_id(identifier=self.identifier)
        else:
            msg = "Your current access token is either missing or expired, please log into" \
                  " rohub again"
            raise SystemExit(msg)

    def get_content(self):
        """
        Function that updates content information for the Research Object.
        """
        self.content = rohub.ros_content(identifier=self.identifier)

    def load_full_metadata(self):
        """
        Function that updates full meta information for the Research Object.
        """
        self.full_metadata_response_content = rohub.ros_full_metadata(identifier=self.identifier)
        self.created_by = self.full_metadata_response_content.get("created_by")
        self.metadata = self.full_metadata_response_content.get("metadata")
        self.contributors_credits = self.full_metadata_response_content.get("contributors_credits")
        self.authors_credits = self.full_metadata_response_content.get("authors_credits")
        self.number_of_all_aggregates = self.full_metadata_response_content.get("number_of_all_aggregates")
        self.number_of_resources = self.full_metadata_response_content.get("number_of_resources")
        self.original_created_on = self.full_metadata_response_content.get("original_created_on")
        self.parent_ro = self.full_metadata_response_content.get("parent_ro")
        self.contributed_by = self.full_metadata_response_content.get("contributed_by")
        self.number_of_views = self.full_metadata_response_content.get("number_of_views")
        self.number_of_forks = self.full_metadata_response_content.get("number_of_forks")
        self.authored_by = self.full_metadata_response_content.get("authored_by")
        self.snapshotter = self.full_metadata_response_content.get("snapshotter")
        self.user_liked = self.full_metadata_response_content.get("user_liked")
        self.cloned = self.full_metadata_response_content.get("cloned")
        self.archived = self.full_metadata_response_content.get("archived")
        self.contributors = self.full_metadata_response_content.get("contributors")
        self.geolocation = self.full_metadata_response_content.get("geolocation")
        self.read_only = self.full_metadata_response_content.get("read_only")
        self.created_on = self.full_metadata_response_content.get("created_on")
        self.credits = self.full_metadata_response_content.get("credits")
        self.forker = self.full_metadata_response_content.get("forker")
        self.number_of_downloads = self.full_metadata_response_content.get("number_of_downloads")
        self.number_of_folders = self.full_metadata_response_content.get("number_of_folders ")
        self.original_created_by = self.full_metadata_response_content.get("original_created_by")
        self.golden = self.full_metadata_response_content.get("golden")
        self.archiver = self.full_metadata_response_content.get("archiver")
        self.forked = self.full_metadata_response_content.get("forked")
        self.number_of_events = self.full_metadata_response_content.get("number_of_events")
        self.modified_on = self.full_metadata_response_content.get("modified_on")
        self.sketch = self.full_metadata_response_content.get("sketch")
        self.user_rate = self.full_metadata_response_content.get("user_rate")
        self.modified_by = self.full_metadata_response_content.get("modified_by")
        self.original_creator_name = self.full_metadata_response_content.get("original_creator_name")
        self.imported = self.full_metadata_response_content.get("imported")
        self.snapshotted = self.full_metadata_response_content.get("snapshotted")
        self.number_of_archives = self.full_metadata_response_content.get("number_of_archives")
        self.quality_calculated_on = self.full_metadata_response_content.get("quality_calculated_on")
        self.user_disliked = self.full_metadata_response_content.get("user_disliked")
        self.number_of_snapshots = self.full_metadata_response_content.get("number_of_snapshots")
        self.number_of_annotations = self.full_metadata_response_content.get("number_of_annotations")
        self.number_of_comments = self.full_metadata_response_content.get("number_of_comments")

    def show_metadata(self):
        """
        Function that shows basic metadata information acquired from the API.
        :return: JSON -> response with content of the metadata for Research Object.
        """
        return self.roi_response_content

    def show_full_metadata(self):
        """
        Function that shows full metadata information acquired from the API.
        :return: JSON -> response with content of the metadata for Research Object.
        """
        if self.full_metadata_response_content:
            return self.full_metadata_response_content
        else:
            print("To access full metadata for the object, please use load_full_metadata method first followed"
                  " by the current method to display it.")

    def add_geolocation(self, body_specification_json=None):
        """
        Function that adds geolocation to the Research Object.
        :param body_specification_json: path to JSON file or Python serializable object that
        will be converted into JSON.
        :return: JSON -> response with content of the Research Object.
        """
        self.geolocation_response_content = rohub.ros_add_geolocation(identifier=self.identifier,
                                                                      body_specification_json=body_specification_json)
        return self.geolocation_response_content

    def add_folders(self, name, description=None, parent_folder=None):
        """
        Function that adds folders to the Research Object.
        :param name: str -> name of the folder.
        :param description: str -> description.
        :param parent_folder: str -> name of the parent folder.
        :return: JSON -> response with content of the Research Object.
        """
        self.folders_response_content = rohub.ros_add_folders(identifier=self.identifier,
                                                              name=name,
                                                              description=description,
                                                              parent_folder=parent_folder)
        return self.folders_response_content

    def add_resource_from_zip(self, path_to_zip):
        """
        Function that adds resource from zip package to the Research Object.
        :param path_to_zip: path to the zip package that will be uploaded.
        :return: JSON -> response from the upload endpoint.
        """
        self.resource_upload_response_content = rohub.ros_upload_resources(identifier=self.identifier,
                                                                           path_to_zip=path_to_zip)
        return self.resource_upload_response_content

    def add_internal_resource(self, res_type, file_path, title=None, folder=None, description=None):
        """
        Function that adds internal resource.
        :param res_type: str -> resource type.
        :param file_path: str -> path to the resource file.
        :param title: str -> title.
        :param folder: str -> folder id.
        :param description: description: str -> description.
        :return: JSON -> response with content of the Resource.
        """
        self.internal_resource_response_content = rohub.ros_add_internal_resource(identifier=self.identifier,
                                                                                  res_type=res_type,
                                                                                  file_path=file_path,
                                                                                  title=title,
                                                                                  folder=folder,
                                                                                  description=description)
        return self.internal_resource_response_content

    def add_external_resource(self, res_type, url, title=None, folder=None, description=None):
        """
        Function that adds external resource.
        :param res_type: str -> resource type.
        :param url: str -> url to the resource.
        :param title: str -> title.
        :param folder: str -> folder id.
        :param description: str -> description.
        :return: JSON -> response with content of the Resource.
        """
        self.external_resource_response_content = rohub.ros_add_external_resource(identifier=self.identifier,
                                                                                  res_type=res_type,
                                                                                  input_url=url,
                                                                                  title=title,
                                                                                  folder=folder,
                                                                                  description=description)
        return self.external_resource_response_content

    def add_annotations(self, resources=None, body_specification_json=None):
        """
        Function that adds geolocation to the Research Object.
        :param resources: list -> list of resources.
        :param body_specification_json: path to JSON file or Python serializable object that
        will be converted into JSON.
        :return: JSON -> response with content of the Research Object.
        """
        self.annotations_response_content = rohub.ros_add_annotations(identifier=self.identifier,
                                                                      resources=resources,
                                                                      body_specification_json=body_specification_json)
        return self.annotations_response_content

    def add_triple(self, the_subject, the_predicate, the_object, annotation_id, object_class=None):
        """
        Function that adds triple to the annotations while validating that annotations exists within
        called Research Object.
        :param the_subject: the_subject: str -> subject.
        :param the_predicate: the_predicate: str -> predicate.
        :param the_object: the_object: str -> object.
        :param annotation_id: annotation_id: str -> annotation's id.
        :param object_class: object_class: str -> object's class.
        :return: JSON -> response with content of the triple.
        """
        if not self.annotations:
            self.show_annotations()
        # validating if annotations belongs to the current ros.
        validated_annotations = [result for result in self.annotations if result["identifier"] == annotation_id]
        if not validated_annotations:
            print(f"Annotation with given id {annotation_id} doesn't belong to the research object "
                  f"you are currently working with!")
        else:
            if len(validated_annotations) > 1:
                print("Unexpected behaviour, more than one annotation with the same id belongs to the"
                      " current Research Object! Please be aware of that.")
            r = rohub.ros_add_triple(the_subject=the_subject, the_predicate=the_predicate,
                                     the_object=the_object, annotation_id=annotation_id, object_class=object_class)
            return r

    def add_author(self, predicate=None, user=None, display_name=None):
        """
        Function that adds author to the Research Object.
        :param predicate: str -> predicate.
        :param user: Rohub's user ID (mutually exclusive with display_name!)
        :param display_name: str -> author name, for cases where author is not a Rohub user
        (mutually exclusive with user!)
        :return: JSON -> response with content.
        """
        return rohub.ros_add_author(identifier=self.identifier, predicate=predicate, user=user,
                                    display_name=display_name)

    def add_contributor(self, predicate=None, user=None, display_name=None):
        """
        Function that adds contributor to the Research Object.
        :param predicate: str -> predicate.
        :param user: Rohub's user ID (mutually exclusive with display_name!)
        :param display_name: str -> author name, for cases where author is not a Rohub user
        (mutually exclusive with user!)
        :return: JSON -> response with content.
        """
        return rohub.ros_add_contributor(identifier=self.identifier, predicate=predicate,
                                         user=user, display_name=display_name)

    def add_copyright(self, predicate=None, user=None, display_name=None):
        """
        Function that adds copyright to the Research Object.
        :param predicate: str -> predicate.
        :param user: Rohub's user ID (mutually exclusive with display_name!)
        :param display_name: str -> author name, for cases where author is not a Rohub user
        (mutually exclusive with user!)
        :return: JSON -> response with content.
        """
        return rohub.ros_add_copyright(identifier=self.identifier, predicate=predicate,
                                       user=user, display_name=display_name)

    def add_funding(self, grant_identifier, grant_name, funder_name, grant_title=None, funder_doi=None):
        """
        Function that adds funding information to the current Research Object.
        NOTE: two auxiliary functions can be used to get some examples for funders and grants
        from the Zenodo database, respectively:
            - zenodo_show_funders()
            - zenodo_show_grants()
        check docstrings for usage details.
        :param grant_identifier: str -> grant's id.
        :param grant_name: str -> grant's name.
        :param funder_name: str -> funder's name.
        :param grant_title: str -> grant's title.
        :param funder_doi: str -> funder's doi.
        :return: JSON -> response with content.
        """
        return rohub.ros_add_funding(identifier=self.identifier, grant_name=grant_name, funder_name=funder_name,
                                     grant_identifier=grant_identifier, grant_title=grant_title,
                                     funder_doi=funder_doi)

    def add_license(self, license_id):
        """
        Function that adds license information to the current Research Object.
        :param license_id: str -> license id.
        :return: JSON -> response with content.
        """
        return rohub.ros_add_license(ros_id=self.identifier, license_id=license_id)

    def fork(self, title=None, description=None, create_doi=None, publication_services=None):
        """
        Function that creates a Research Object's fork.
        :param title: str ->  title for the Research Object.
        :param description: str -> description.
        :param create_doi: boolean -> doi is created if True, False otherwise.
        :param publication_services: list -> name of the service.
        :return: str -> id of forked Research Object.
        """
        self.fork_response_content = rohub.ros_fork(identifier=self.identifier,
                                                    description=description,
                                                    create_doi=create_doi,
                                                    title=title,
                                                    publication_services=publication_services)
        return self.fork_response_content

    def snapshot(self, title=None, description=None, create_doi=None, publication_services=None):
        """
        Function that creates a Research Object's snapshot.
        :param title: str ->  title for the Research Object.
        :param description: str -> description.
        :param create_doi: boolean -> doi is created if True, False otherwise.
        :param publication_services: list -> name of the service.
        :return: str -> id of snapshot.
        """
        self.snapshot_response_content = rohub.ros_snapshot(identifier=self.identifier,
                                                            description=description,
                                                            create_doi=create_doi,
                                                            title=title,
                                                            publication_services=publication_services)
        return self.snapshot_response_content

    def archive(self, title=None, description=None, create_doi=None, publication_services=None):
        """
        Function that creates a Research Object's snapshot.
        :param title: str ->  title for the Research Object.
        :param description: str -> description.
        :param create_doi: boolean -> doi is created if True, False otherwise.
        :param publication_services: list -> name of the service..
        :return: str -> id of archived Research Object.
        """
        self.archive_response_content = rohub.ros_snapshot(identifier=self.identifier,
                                                           description=description,
                                                           create_doi=create_doi,
                                                           title=title,
                                                           publication_services=publication_services)
        return self.archive_response_content

    def delete(self):
        """
        Function that deletes a Research Object.
        :return: JSON -> response.
        """
        self.delete_response_content = rohub.ros_delete(identifier=self.identifier)
        return self.delete_response_content

    def delete_folder(self, folder_id):
        """
        Function that deletes folder from the Research Object.
        :param folder_id: str -> folder's id.
        :return: JSON -> response.
        """
        self.delete_folder_response_content = rohub.ros_delete_folder(folder_identifier=folder_id)
        return self.delete_folder_response_content

    def delete_resource(self, resource_id):
        """
        Function that deletes resource from the Research Object.
        :param resource_id: str -> resource id.
        :return: JSON -> response.
        """
        self.delete_resource_response_content = rohub.ros_delete_resource(resource_identifier=resource_id)
        return self.delete_resource_response_content

    def delete_annotation(self, annotation_id):
        """
        Function that deletes annotations from the Research Object.
        :param annotation_id: str -> annotation id.
        :return: JSON -> response.
        """
        self.delete_annotation_response_content = rohub.ros_delete_annotation(annotation_identifier=annotation_id)
        return self.delete_annotation_response_content

    def update(self):
        """
        Function for updating Research Object in the service.
        :return: JSON -> response.
        """
        self.update_response_content = rohub.ros_update(identifier=self.identifier,
                                                        title=self.title,
                                                        research_areas=self.research_areas,
                                                        description=self.description,
                                                        access_mode=self.access_mode,
                                                        ros_type=self.ros_type,
                                                        template=self.template,
                                                        owner=self.owner,
                                                        editors=self.editors,
                                                        readers=self.readers,
                                                        creation_mode=self.creation_mode)
        return self.update_response_content

    def show_publication(self):
        """
        Function that shows publication details for a Research Object.
        :return: JSON -> response.
        """
        self.show_publication_response_content = rohub.ros_show_publications(identifier=self.identifier)
        return self.show_publication_response_content

    def show_valid_research_areas(self):
        """
        Function for displaying all valid research areas.
        :return: list -> list with valid research areas.
        """
        return self.valid_research_areas

    def show_valid_access_modes(self):
        """
        Function for displaying all valid access modes.
        :return: list -> list with valid access modes.
        """
        if not self.available_enums:
            self._get_available_enums()
        return self.available_enums["ro_access_mode"]

    def show_valid_ros_types(self):
        """
        Function for displaying all valid ros types.
        :return: list -> list with valid ros types.
        """
        if not self.available_enums:
            self._get_available_enums()
        return self.available_enums["ro_type"]

    def show_valid_templates(self):
        """
        Function for displaying all valid templates.
        :return: list -> list with valid templates.
        """
        if not self.available_enums:
            self._get_available_enums()
        return self.available_enums["ro_template"]

    def show_valid_creation_modes(self):
        """
        Function for displaying all valid creation modes.
        :return: list -> list with valid creation modes.
        """
        if not self.available_enums:
            self._get_available_enums()
        return self.available_enums["ro_creation_mode"]

    def show_valid_resource_types(self):
        """
        Function for displaying all valid resource types.
        :return: list -> list with valid resource types.
        """
        if not self.available_enums:
            self._get_available_enums()
        return self.available_enums["resource_type"]

    def show_valid_publication_services(self):
        """
        Function for displaying all valid publication services.
        :return: list -> list with valid publication services.
        """
        if not self.available_enums:
            self._get_available_enums()
        return self.available_enums["publication_service"]

    def show_annotations(self):
        """
        Function for displaying all annotations connected to the Research Object.
        :return: list -> useful information from annotations response.
        """
        data = rohub.ros_show_annotations(identifier=self.identifier)
        self.annotations = data
        return self.annotations

    def show_triples(self, annotation_id):
        """
        Function for displaying all triples related to specific annotation while validating
        that annotation is related to the Research Object that was called.
        :param annotation_id: str -> annotation's id.
        :return: list -> useful information regarding triples.
        """
        if not self.annotations:
            self.show_annotations()
        # validating if annotations belongs to the current ros.
        validated_annotations = [result for result in self.annotations if result["identifier"] == annotation_id]
        if not validated_annotations:
            print(f"Annotation with given id {annotation_id} doesn't belong to the research object "
                  f"you are currently working with!")
        else:
            if len(validated_annotations) > 1:
                print("Unexpected behaviour, more than one annotation with the same id belongs to the"
                      " current Research Object! Please be aware of that.")
            data = rohub.ros_show_triples(identifier=annotation_id)
            return data

    def show_authors(self):
        """
        Function for displaying list of authors for current Research Object.
        :return: list -> list of details for each author.
        """
        return rohub.ros_show_authors(identifier=self.identifier)

    def show_contributors(self):
        """
        Function for displaying list of contributors for current Research Object.
        :return: list -> list of details for each contributor.
        """
        return rohub.ros_show_contributors(identifier=self.identifier)

    def show_copyright(self):
        """
        Function for displaying list of copyright for current Research Object.
        :return: list -> list of details for copyrights.
        """
        return rohub.ros_show_copyright(identifier=self.identifier)

    def show_funding(self):
        """
        Function for displaying list of funding for current Research Object.
        :return: list -> list of details for funding.
        """
        return rohub.ros_show_funding(identifier=self.identifier)

    def show_license(self):
        """
        Function for displaying license for the current Research Object.
        :return: JSON -> response.
        """
        return rohub.ros_show_license(identifier=self.identifier)

    def export_to_rocrate(self, filename=None, path=None, use_format=settings.EXPORT_TO_ROCRATE_DEFAULT_FORMAT):
        """
        Function for downloading Research Object meta-data as RO-crate.
        :param filename: str -> name for the file that will be acquired (without extension).
        If not provided username will be used instead.
        :param path: path: str -> path where file should be downloaded. Default is cwd.
        :param use_format: use_format: str -> format choice. Either json-ld or zip.
        """
        rohub.ros_export_to_rocrate(identifier=self.identifier, filename=filename, path=path,
                                    use_format=use_format)

    ###############################################################################
    #              Required Attributes methods.                                   #
    ###############################################################################

    def _get_valid_research_areas(self, research_areas):
        """
        Semi private function that validates user's input for research areas.
        :param research_areas: list -> list of research areas provided by the user.
        :return: list -> list of valid research areas.
        """
        if isinstance(research_areas, list):
            if not self.valid_research_areas:
                r = utils.get_request(url=settings.API_URL + "research-areas/")
                if r:
                    r_json = r.json()
                    results = r_json['results']
                    for result in results:
                        self.valid_research_areas.append(result['name'])

            research_areas = [area.capitalize() for area in research_areas]
            research_areas = set(research_areas).intersection(self.valid_research_areas)
            return list(research_areas)
        else:
            msg = f"Aborting: research_areas parameter should be a list and not {type(research_areas)}!"
            raise SystemExit(msg)

    ###############################################################################
    #              Optional Attributes methods.                                   #
    ###############################################################################

    def _validate_and_set_access_mode(self, access_mode):
        """
        Semi-private function for validating and setting access mode attribute.
        :param access_mode: str -> access
        :return: str -> access mode value.
        """
        if not self.available_enums:
            self._get_available_enums()
        try:
            valid_access_modes = self.available_enums["ro_access_mode"]
            if access_mode.upper() not in valid_access_modes:
                raise ValueError(f'access mode has to be one of {valid_access_modes}')
            return access_mode.upper()
        except KeyError as e:
            print("Wasn't able to validate values for access_mode. Leaving it"
                  " empty as per default. Please try adjust this using generated"
                  " ResearchObject later.")
            print(e)
            return None

    def _validate_and_set_ros_type(self, ros_type):
        """
        Semi-private function for validating and setting ros type attribute.
        :param ros_type: str -> ros type.
        :return: str -> ros type value.
        """
        if not self.available_enums:
            self._get_available_enums()
        try:
            valid_ros_type = self.available_enums["ro_type"]
            if ros_type.title() not in valid_ros_type:
                raise ValueError(f'ros type has to be one of {valid_ros_type}')
            return ros_type.title()
        except KeyError as e:
            print("Wasn't able to validate values for ros_type. Leaving it"
                  " empty as per default. Please try adjust this using generated"
                  " ResearchObject later.")
            print(e)
            return None

    def _validate_and_set_template(self, template):
        """
        Semi-private function for validating and setting template attribute.
        :param template: str -> template type.
        :return: str -> template value.
        """
        if not self.available_enums:
            self._get_available_enums()
        try:
            valid_templates = self.available_enums["ro_template"]
            if template.title() not in valid_templates:
                raise ValueError(f'template has to be one of {valid_templates}')
            return template.title()
        except KeyError as e:
            print("Wasn't able to validate values for template. Leaving it"
                  " empty as per default. Please try adjust this using generated"
                  " ResearchObject later.")
            print(e)
            return None

    def _validate_and_set_creation_mode(self, creation_mode):
        """
        Semi-private function for validating and setting template attribute.
        :param creation_mode: str -> creation mode.
        :return: str -> creation mode value.
        """
        if not self.available_enums:
            self._get_available_enums()
        try:
            valid_creation_modes = self.available_enums["ro_creation_mode"]
            if creation_mode.upper() not in valid_creation_modes:
                raise ValueError(f'template has to be one of {valid_creation_modes}')
            return creation_mode.upper()
        except KeyError as e:
            print("Wasn't able to validate values for creation mode. Leaving it"
                  " empty as per default. Please try adjust this using generated"
                  " ResearchObject later.")
            print(e)
            return None
