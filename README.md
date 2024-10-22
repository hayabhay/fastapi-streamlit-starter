# FastAPI Streamlit Starter

---

This is a simple template repo to create new projects that use FastAPI and Streamlit.
It also includes a simple Dockerfile to bundle the FastAPI and Streamlit apps together for development and deployment as needed.

This uses -
1. [`pip-tools`](https://github.com/jazzband/pip-tools) for dependency management. Initially, [Poetry](https://python-poetry.org/) was used but it was a hellish nightmare especially for ML projects.
2. `ruff` as a lightweight linter/formatter to `black`, `flake8` & `isort`.
3. `pre-commit` hooks to run `ruff` & other checks before committing.
4. `.github` workflows for CI/CD.

For local, non-containerized dev, `pyenv` with `virtualenv` is recommended.

## Quickstart

First, clone the repo:

```bash
git clone <repo-url>
```

Create a virtual environment using `pyenv` & `virtualenv`:

```bash
pyenv install 3.12.5
pyenv virtualenv 3.12.5 fapi
pyenv activate fapi
```

Now install the dependencies:

```bash
pip install -r requirements.txt
```

For dev mode, requirements files can be generated & installed with `pip-compile` & `pip-sync`:

```bash
pip-compile requirements/main.in -o requirements.txt
pip-compile requirements/dev.in -c requirements.txt -o requirements-dev.txt
pip-sync requirements.txt requirements-dev.txt
```

Alternatively, `invoke` can be used to trigger the above commands (invoke must be installed first):

```bash
pip install invoke
invoke install --dev
```

Then, you can start the FastAPI development server with:

```bash
cd api
uvicorn main:app --reload
```

And the Streamlit development UI with:

```bash
cd ui
streamlit run 01_🏠_Home.py
```

## Docker - Local Development

To run the FastAPI and Streamlit apps together in a Docker container, you can use the included `Dockerfile`:

```bash
docker build --target dev --tag myapp-dev .
docker run -p 8000:8000 -p 8501:8501 myapp-dev
```

The above paradigm is meant for development purposes.

For production, you can use the `Dockerfile` with the `api` target that only includes the FastAPI app:

```bash
docker build --target api --tag myapp-api .
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
gcloud components update
```

You may have to authenticate with your Google Cloud account:

```bash
gcloud auth login
```

0.2. Create a new google cloud project either from the GUI or using the CLI:

```bash
gcloud projects create my-project
```

0.3. Set the project as the default project:

```bash
gcloud config set project my-project
```

Note: If you have multiple projects, you can switch between them using the above command. Be weary of the project you are currently using to avoid accidental pushes to the wrong project.


#### Google Project Setup

1.1. Enable the Cloud Run API (you can do this from the GUI as well) - this is needed to to deploy the container.

```bash
gcloud services enable run.googleapis.com
```

1.2. Enable the Artifact Registry API - this is needed to push the container to the Google Artifact Registry.

```bash
gcloud services enable artifactregistry.googleapis.com
```

Note: You can also use Google Cloud Build to build and push the container to the registry. This is a more automated way of doing things. You can find more information [here](https://cloud.google.com/cloud-build/docs/quickstart-docker).


1.3 Set up secrets manager - this is needed to store secrets like API keys etc.

- Enable the Secret Manager API:
```bash
gcloud services enable secretmanager.googleapis.com
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
docker build --target prod --tag gcr.io/my-project/myapp-prod .
```

2.2. Push the container image to the Google Artifact Registry:

```bash
docker push gcr.io/my-project/myapp-prod
```

#### Deploy Container

3.1. Deploy the container to Google Cloud Run:

```bash
gcloud run deploy my-fastapi-app \
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
gcloud run services delete my-fastapi-app
```

4.2. To delete the container image from the Google Artifact Registry:

```bash
gcloud container images delete gcr.io/my-project/myapp-prod
```

4.3. To delete the Google Cloud project:

```bash
gcloud projects delete my-project
```

> Note: To launch Streamlit to GCP, you can use the same process as above but build with the `ui` target instead of the `prod` target. The server address must be explicitly set to the GCR URL for the fastapi app in the Streamlit app and relevant permissions to send/receive data from the FastAPI app must be set.

## Links

- [Documentation](docs/index.md)
- [Issues](https://github.com/hayabhay/fastapi-streamlit-starter/issues)
- [History](docs/history.md)
- [Contributing Guide](docs/contributing.md)
- [License](LICENSE)(MIT)
