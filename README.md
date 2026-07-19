<img src=".docs/logo.png" width="64px" align="right"/>

# Fast App - API

![License](https://img.shields.io/github/license/avcaliani/fast-app?logo=apache&color=lightseagreen)
![#](https://img.shields.io/badge/python-3.10.x-yellow.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

My goal with this repository is an in-depth exploration of FastAPI internals, the async
execution model, and production-ready backend design.

Here is the **project structure** 👇

```bash
.
├── app/
│   ├── routers/         # 🚏 API route handlers.
│   ├── services/        # ⚙️ Business logic.
│   ├── utils/           # 🔧 Auth & MongoDB helpers.
│   └── models.py        # 📦 Pydantic models.
├── resources/
│   └── log-config.yml   # 📝 Uvicorn logging config.
├── static/               # 🖼️ Static files served by the API.
├── tests/                # ✅ Unit tests.
├── config.py             # ⚙️ Dynaconf settings loader.
├── main.py               # 🚀 FastAPI app entrypoint.
├── Dockerfile            # 🐋 Dockerfile for the API.
├── docker-compose.yml    # 🧩 MongoDB service for local dev.
└── settings.toml         # 📝 Dynaconf settings.
```

## Quick Start

Create your Python virtual environment...

```bash
# 👇 Setting PyEnv version
pyenv local 3.10.0

# 👇 Virtual Environment
python -m venv .venv \
  && source .venv/bin/activate \
  && python -m pip install --upgrade pip

# 👇 Dependencies
make install
```

Then, create a Dynaconf secrets file as follows.

```bash
echo "
[default]
TOKEN_SECRET_KEY = '$(openssl rand -hex 32)'
SECRET = '🚀'  # Dev Secret

[prod]
SECRET = '🤫'
" > .secrets.toml
```

The API uses MongoDB, so start it up with Docker Compose before running the app.

```bash
docker-compose up -d
```

Finally, start the API server.

> `APP_ENV` is an environment variable used by Dynaconf to indicate which profile should be used.

```bash
make run
```

After executing the previous command you are ready to access the API resources.

- API Home: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

![home](.docs/home.png)

### Example

Response **OK**...

```bash
curl -X 'GET' 'http://127.0.0.1:8000/emoji'
```

```json
{
  "lucky_emojis": [
    "🫐",
    "🥭"
  ],
  "secret": "🚀",
  "consulted_at": "2021-10-22T11:36:48.533441"
}
```

### Running with Docker

Alternatively, build and run the API itself in a container (still requires `.secrets.toml` and MongoDB running as above).

```bash
docker build -t fast-app-api .
docker run -p 8000:8000 --env APP_ENV=dev fast-app-api
```

### References

- [Fast API: docs](https://fastapi.tiangolo.com/)
- [pydantic: docs](https://pydantic-docs.helpmanual.io/)
- [Poetry CLI: docs](https://python-poetry.org/docs/cli/)
- [pre-commit: docs](https://pre-commit.com/)
- [MongoDB: Quick Start FastAPI](https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/)
- [Icon made by Strokeicon from IconFinder](https://www.iconfinder.com/icons/2191531/best_fast_flash_good_light_speed_icon)

> 💡 Fast API has an awesome documentation!
