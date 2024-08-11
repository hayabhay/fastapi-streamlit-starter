# FastAPI Streamlit Starter

---

This is a simple template repo to create new projects that use FastAPI and Streamlit.
It also includes a simple Dockerfile to bundle the FastAPI and Streamlit apps together for development and deployment as needed.

## Quickstart

To get started, clone the repo and install the dependencies:

```bash
$ git clone
$ poetry install --with dev
```

> Note: Streamlit is only available in dev mode which is set in the `pyproject.toml` file. This is to keep the production API container as small as possible. Feel free to change this as needed.


Then, you can start the FastAPI development server with:

```bash
$ cd api
$ poetry run uvicorn main:app --reload
```

And the Streamlit development server with:

```bash
$ cd ui
$ poetry run streamlit run main.py
```

### Docker

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

## Links

- [Documentation](docs/index.md)
- [Issues](https://github.com/hayabhay/fastapi-streamlit-starter/issues)
- [History](docs/history.md)
- [Contributing Guide](docs/contributing.md)
- [License](LICENSE)(MIT)
