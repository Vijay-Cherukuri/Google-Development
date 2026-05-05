# WARNING: The following action, if not in simulation mode, will disable billing
# for the project, potentially stopping all services and causing outages.
# Ensure thorough testing and understanding before enabling live deactivation.

import base64
import json
import os
import urllib.request

from cloudevents.http.event import CloudEvent
import functions_framework

from google.api_core import exceptions
from google.cloud import billing_v1
from google.cloud import logging

billing_client = billing_v1.CloudBillingClient()

def get_project_id() -> str:
    """Retrieves the Google Cloud Project ID.
    
    This function first attempts to get the project ID from the
    'GOOGLE_CLOUD_PROJECT' environment variable. If the environment
    variable is not set or is None, it then attempts to retrieve the
    project ID from the Google Cloud metadata server.
    
    Returns:
        str: The Google Cloud Project ID.
        
    Raises:
        ValueError: If the project ID cannot be determined either from
                    the environment variable or the metadata server.
    """

    # Read the environment variable, usually set manually
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id is not None:
        return project_id
    
    # Otherwise, get the 'project-id'' from the Metadata server.
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    request = urllib.request.Request(url)
    request.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(request).read().decode()

    if project_id is None:
        raise ValueError("project-id metadata not found.")
    
    return project_id

@functions_framework.cloud_event
def stop_billing(cloud_event: CloudEvent) -> None:
    # TODO(developer): As stoping billing is a destructive action
    # for your project, change the following constant to False
    # after you validate with a test budget.
    