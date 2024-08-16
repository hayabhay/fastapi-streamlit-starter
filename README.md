# FastAPI Streamlit Starter

---

This is a simple template repo to create new projects that use FastAPI and Streamlit.
It also includes a simple Dockerfile to bundle the FastAPI and Streamlit apps together for development and deployment as needed.

## Quickstart

This project uses [Poetry](https://python-poetry.org/) for dependency management and [Docker](https://www.docker.com/) for containerization.

Poetry can be installed using the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Make sure poetry is in the PATH variable after installation. Example: `export PATH=$PATH:$HOME/.local/bin` if poetry is installed in the user's home directory.

Now, you can clone the repo and install the dependencies:

```bash
$ git clone
$ poetry install --with dev
```

The `--with dev` flag is used to install the development dependencies as well. This is needed to run the Streamlit app.

> Note: Streamlit is only available in dev mode which is set in the `pyproject.toml` file. This is to keep the production API container as small as possible. Feel free to change this as needed.


Then, you can start the FastAPI development server with:

```bash
$ cd api
$ poetry run uvicorn main:app --reload
```

And the Streamlit development UI with:

```bash
$ cd ui
$ poetry run streamlit run main.py
```

### Docker - Local Development

To run the FastAPI and Streamlit apps together in a Docker container, you can use the included `Dockerfile`:

```bash
$ docker build --target dev --tag myapp-dev .
$ docker run -p 8000:8000 -p 8501:8501 fastapi-streamlit-starter
```

The above paradigm is meant for development purposes.

For production, you can use the `Dockerfile` with the `prod` target:

```bash
$ docker build --target prod --tag myapp-prod .
```

This will create a smaller image with only the FastAPI app and its dependencies. Streamlit & its dependencies are not included in the production image since it can significantly increase the image size especially if not shared by the FastAPI app.

## Deployment

These are instructions for deploying the container on Google Cloud Run.
You can also use more bare-metal solutions like Kubernetes etc. and/or other cloud providers.

### Google Cloud Run


#### Google SDK Setup

0.1. This assumes you have a Google Cloud account and have the `gcloud` CLI installed.
If not, you can follow the instructions [here](https://cloud.google.com/sdk/docs/install).
If you do, update it to the latest version:

```bash
$ gcloud components update
```

You may have to authenticate with your Google Cloud account:

```bash
$ gcloud auth login
```

0.2. Create a new google cloud project either from the GUI or using the CLI:

```bash
$ gcloud projects create my-project
```

0.3. Set the project as the default project:

```bash
$ gcloud config set project my-project
```

Note: If you have multiple projects, you can switch between them using the above command. Be weary of the project you are currently using to avoid accidental pushes to the wrong project.


#### Google Project Setup

1.1. Enable the Cloud Run API (you can do this from the GUI as well) - this is needed to to deploy the container.

```bash
$ gcloud services enable run.googleapis.com
```

1.2. Enable the Artifact Registry API - this is needed to push the container to the Google Artifact Registry.

```bash
$ gcloud services enable artifactregistry.googleapis.com
```

Note: You can also use Google Cloud Build to build and push the container to the registry. This is a more automated way of doing things. You can find more information [here](https://cloud.google.com/cloud-build/docs/quickstart-docker).


1.3 Set up secrets manager - this is needed to store secrets like API keys etc.

- Enable the Secret Manager API:
```bash
$ gcloud services enable secretmanager.googleapis.com
```

- Create a secrets file
```bash
gcloud secrets create <secret-id> --replication-policy="automatic"
```

- Add the `.env` to the secrets
```bash
gcloud secrets versions add <secret-id> --data-file=.env
```

NOTE: The service account that runs the Cloud Run service needs to have the `Secret Manager Secret Accessor` role to access the secrets. This can be done on the GCP Console in the IAM & Admin section or using the CLI

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member=serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL \
    --role=roles/secretmanager.secretAccessor
```

#### Build & Push Container

2.1. Build the container image:

```bash
$ docker build --target prod --tag gcr.io/my-project/myapp-prod .
```

2.2. Push the container image to the Google Artifact Registry:

```bash
$ docker push gcr.io/my-project/myapp-prod
```

#### Deploy Container

3.1. Deploy the container to Google Cloud Run:

```bash
$ gcloud run deploy my-fastapi-app \
    --image gcr.io/my-fastapi-project/myapp-prod \
    --platform managed \
    --region <region> \
    --allow-unauthenticated
```

Configurations like region, autoscaling, instance size etc. can be set as needed. You can find more information [here](https://cloud.google.com/sdk/gcloud/reference/run/deploy).

3.2. Once the deployment is complete, you will get a URL where the container is deployed. You can access the FastAPI app from this URL.

3.3. You can also set up a custom domain for the Cloud Run service. You can find more information [here](https://cloud.google.com/run/docs/mapping-custom-domains).

#### Cleanup

4.1. To delete the Cloud Run service:

```bash
$ gcloud run services delete my-fastapi-app
```

4.2. To delete the container image from the Google Artifact Registry:

```bash
$ gcloud container images delete gcr.io/my-project/myapp-prod
```

4.3. To delete the Google Cloud project:

```bash
$ gcloud projects delete my-project
```

> Note: To launch Streamlit to GCP, you can use the same process as above but build with the `ui` target instead of the `prod` target. The server address must be explicitly set to the GCR URL for the fastapi app in the Streamlit app and relevant permissions to send/receive data from the FastAPI app must be set.

## Links

- [Documentation](docs/index.md)
- [Issues](https://github.com/hayabhay/fastapi-streamlit-starter/issues)
- [History](docs/history.md)
- [Contributing Guide](docs/contributing.md)
- [License](LICENSE)(MIT)
