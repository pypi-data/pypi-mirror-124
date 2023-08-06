# Let users know if they're missing any of our hard dependencies
hard_dependencies = (["requests"])
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies

# MAIN IMPORTS
from rohub.rohub import login
from rohub.rohub import whoami
from rohub.rohub import version
from rohub.rohub import set_retries
from rohub.rohub import set_sleep_time
from rohub.rohub import owned
from rohub.rohub import is_job_success
from rohub.rohub import show_user_id
# ROS MAIN IMPORTS
from rohub.rohub import search_ros_by_id
from rohub.rohub import ros_create
from rohub.rohub import ros_load
from rohub.rohub import ros_content
from rohub.rohub import ros_full_metadata
from rohub.rohub import ros_fork
from rohub.rohub import ros_snapshot
from rohub.rohub import ros_archive
from rohub.rohub import ros_show_publications
from rohub.rohub import ros_show_triple_details
from rohub.rohub import ros_show_annotations
from rohub.rohub import ros_show_triples
from rohub.rohub import ros_show_authors
from rohub.rohub import ros_show_contributors
from rohub.rohub import ros_show_copyright
from rohub.rohub import ros_show_funding
from rohub.rohub import ros_show_license
from rohub.rohub import ros_export_to_rocrate
# ROS ADD IMPORTS
from rohub.rohub import ros_add_geolocation
from rohub.rohub import ros_add_folders
from rohub.rohub import ros_add_annotations
from rohub.rohub import ros_add_internal_resource
from rohub.rohub import ros_add_external_resource
from rohub.rohub import ros_add_triple
from rohub.rohub import ros_add_author
from rohub.rohub import ros_add_contributor
from rohub.rohub import ros_add_copyright
from rohub.rohub import ros_add_funding
from rohub.rohub import ros_add_license
# ROS UPLOAD IMPORTS
from rohub.rohub import ros_upload
from rohub.rohub import ros_upload_resources
# ROS DELETE IMPORTS
from rohub.rohub import ros_delete
from rohub.rohub import ros_delete_folder
from rohub.rohub import ros_delete_resource
from rohub.rohub import ros_delete_annotation
# ROS UPDATE IMPORTS
from rohub.rohub import ros_update
# AUXILIARY
from rohub.rohub import zenodo_show_funders
from rohub.rohub import zenodo_show_grants
from rohub.rohub import show_available_licenses

__all__ = [
    "login",
    "whoami",
    "version",
    "set_retries",
    "set_sleep_time",
    "owned",
    "is_job_success",
    "search_ros_by_id",
    "ros_create",
    "ros_load",
    "ros_content",
    "ros_full_metadata",
    "ros_fork",
    "ros_archive",
    "ros_show_publications",
    "ros_add_geolocation",
    "ros_add_folders",
    "ros_add_annotations",
    "ros_add_internal_resource",
    "ros_add_external_resource",
    "ros_upload",
    "ros_upload_resources",
    "ros_delete",
    "ros_delete_folder",
    "ros_delete_resource",
    "ros_delete_annotation",
    "ros_update",
    "ros_add_triple",
    "ros_show_triple_details",
    "ros_show_annotations",
    "ros_show_triples",
    "ros_export_to_rocrate",
    "ros_add_author",
    "show_user_id",
    "ros_show_authors",
    "ros_add_contributor",
    "ros_show_contributors",
    "ros_show_copyright",
    "ros_add_copyright",
    "ros_show_funding",
    "ros_add_funding",
    "zenodo_show_funders",
    "zenodo_show_grants",
    "ros_add_license",
    "show_available_licenses"
]
