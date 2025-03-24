# Open WebUI

https://github.com/open-webui/open-webui


## pip 安装

```bash
pip install open-webui

mkdir ~/open-webui
cd ~/open-webui
open-webui serve
open-webui serve --port=3030
```

```text
Loading WEBUI_SECRET_KEY from file, not provided as an environment variable.
Generating a new secret key and saving it to ~/open-webui/.webui_secret_key
Loading WEBUI_SECRET_KEY from ~/open-webui/.webui_secret_key
Running migrations
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.

Fetching 30 files: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████| 30/30 [00:00<00:00, 28187.53it/s]
INFO:     Started server process [43531]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 8080): address already in use
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.

INFO:     Uvicorn running on http://127.0.0.1:3030 (Press CTRL+C to quit)
```

## Quick Start with Docker

```bash
docker run -d -p 3030:8080 -v ~/.open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```