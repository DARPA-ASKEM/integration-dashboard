from python:3.11

RUN pip install --no-cache-dir poetry==1.5.1

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY README.md README.md
COPY dashboard dashboard

RUN poetry install

EXPOSE 8501
CMD poetry run poe ui
