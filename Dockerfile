FROM python:3.9.5

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.6

COPY . /usr/app/
WORKDIR /usr/app/

# install
RUN echo "---> Install poetry" && \
    curl -sSL "https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py" | python - && \
    ln -s "${HOME}"/.poetry/bin/poetry /usr/bin/poetry && \
    poetry config virtualenvs.create false && \
    poetry install && \
  echo "---> Cleaning up" && \
    rm -rf /tmp/*

CMD ["python3", "main.py"]
