FROM python:3.12.9

WORKDIR /app

COPY ./requirements.txt ./

RUN  pip install -r requirements.txt

COPY ./ollama_llamaindex_rga.py ./

CMD ["streamlit", "run", "--server.address", "0.0.0.0", "--server.port","8501", "./ollama_llamaindex_rga.py"]

# docker build -t ollama-llamaindex-rga .
# docker run -e OLLAMA_BASE_URL=http://host.docker.internal:11434  --rm -p 8501:8501  --name ollama-llamaindex-rga ollama-llamaindex-rga
# docker run -e OLLAMA_BASE_URL=http://host.docker.internal:11434 -d -p 8501:8501  --name ollama-llamaindex-rga ollama-llamaindex-rga
