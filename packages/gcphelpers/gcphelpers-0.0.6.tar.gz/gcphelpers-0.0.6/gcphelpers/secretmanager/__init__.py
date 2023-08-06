from google.cloud import secretmanager

# Access a secret from Google Secret Manager
# @args:
# - secretRef: A Secret Manager secret name
# - project: GCP project name or project ID
# - version (optional): Define a specific version to use, otherwise use latest
def access_secret_manager_secret(secretRef, project, version="latest"):
    client   = secretmanager.SecretManagerServiceClient()
    secret   = f"projects/{project}/secrets/{secretRef}/versions/{version}"

    try:
        response = client.access_secret_version(request={
            "name": secret
        })
    except Exception as e:
        return e

    return response.payload.data.decode("UTF-8")