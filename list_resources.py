from google.cloud import asset_v1
import sys

def list_resources(project_id):
    client = asset_v1.AssetServiceClient()
    parent = f"projects/{project_id}"
    
    # List all resources in the project
    response = client.search_all_resources(request={"scope": parent})
    
    print(f"{'Asset Type':<40} | {'Name'}")
    print("-" * 80)
    for resource in response:
        print(f"{resource.asset_type:<40} | {resource.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python list_resources.py <PROJECT_ID>")
        sys.exit(1)
    
    project_id_arg = sys.argv[1]
    list_resources(project_id_arg)