from python:3.11

RUN pip install --no-cache-dir poetry==1.5.1
RUN poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY README.md README.md
RUN poetry install --no-root

COPY dashboard dashboard
RUN poetry install --only-root

COPY .streamlit .streamlit
COPY outputs outputs
ENV AWS_ACCESS_KEY_ID notprovided
ENV AWS_SECRET_ACCESS_KEY notprovided
ENV BUCKET notprovided

EXPOSE 8501
CMD poetry run poe ui
