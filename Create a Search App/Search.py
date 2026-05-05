from typing import List

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

# TODO(developer): Uncomment these variables before running the sample.
# project_id = "YOUR_PROJECT_ID"
# location = "YOUR_LOCATION" # Values: "global"
# engine_id = "YOUR_ENGINE_ID"
data_store_ids = ["YOUR_DATA_STORE_ID"]

def create_engine_sample(
    project_id: str, location: str, engine_id: str, data_store_id: List[str]) -> str:
    # For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.EngineServiceClient(client_options=client_options)

    # The full resource name of the collection
    # e.g. projects/{project}/locations/{location}/collections/default_collection
    parent = client.collection_path(
        project_id=project_id, 
        location=location, 
        collection_id="default_collection",
    )

    engine = discoveryengine.Engine(
        display_name="Test Engine",
        # Options: GENERIC, MEDIA, HEALTHCARE_FHIR
        industry_vertical=discoveryengine.Engine.IndustryVertical.GENERIC,
        # Options: SOLUTION_TYPE_RECOMMENDATION, SOLUTION_TYPE_SEARCH, SOLUTION_TYPE_CHAT, SOLUTION_TYPE_GENERATIVE_CHAT
        solution_type=discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH,
        # For search app only
        search_engine_config=discoveryengine.Engine.SearchEngineConfig(
            # Options: SEARCH_TIER_STANDARD, SEARCH_TIER_ENTERPRISE
            search_tier=discoveryengine.SearchTier.SEARCH_TIER_EnTERPRISE,
            # Options: SEARCH_ADD_ON_LLM, SEARCH_ADD_ON_UNSPECIFIED
            search_add_ons=[discoveryengine.SearchAddOn.SEARCH_ADD_ON_LLM],
        ),
        # For generic recommendation apps only
        # similar_documents_config=discoverengine.Engine.SimilarDocumentEngineConfig,
        data_store_ids=data_store_ids,
    )

    request = discoveryengine.CreateEngineRequest(
        parent=parent,
        engine=engine,
        engine_id=engine_id,
    )

    # Make the request
    operation = client.create_engine(request=request)

    print(f"Waiting for operation to complete:{operation.operation.name}")
    response = operation.result()

    # After the operation is complete,
    # get information from operation metadata
    metadata = discoveryengine.CreateEngineMetadata(operation.metadata)
    
    # Handle the response
    print(response)
    print(metadata)

    return operation.operation.name