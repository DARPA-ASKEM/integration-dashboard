from python:3.11

RUN pip install --no-cache-dir poetry==1.5.1

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY README.md README.md
COPY dashboard dashboard

RUN poetry install

ENV AWS_ACCESS_KEY_ID notprovided
ENV AWS_SECRET_ACCESS_KEY notprovided
ENV BUCKET notprovided
ENV SKEMA_RS_URL http://skema-rs.staging.terarium.ai
ENV TA1_UNIFIED_URL https://api.askem.lum.ai
ENV MIT_TR_URL http://3.83.68.208

EXPOSE 8501
CMD poetry run poe ui
