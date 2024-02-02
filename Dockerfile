FROM python:3.10-slim

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install --yes --no-install-recommends \
      curl=7.88.1-10+deb12u5 \
      gcc=4:12.2.0-3 \
      libsqlite3-dev=3.40.1-2 \
      nano=7.2-1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a user and group with specific UID and GID
RUN groupadd -g 1001 app && \
    useradd -u 1001 -g app -s /bin/false -m app

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1
RUN pip install --upgrade pip==23.3.2

COPY requirements.txt .
# TODO: Install requirements in a separate stage and copy to the main
RUN pip install --requirement requirements.txt && \
    rm requirements.txt

COPY src/ /app

# Change ownership of the /app directory to the app user
RUN chown -R app:app /app

ARG PORT=5006
ENV PORT ${PORT}
ARG LIVENESS_ENDPOINT=health
ENV LIVENESS_ENDPOINT ${LIVENESS_ENDPOINT}

ENTRYPOINT ["/bin/bash", "-o", "pipefail", "-c", "panel serve app.py --admin --liveness --liveness-endpoint ${LIVENESS_ENDPOINT} --port ${PORT}"]

HEALTHCHECK CMD curl --fail http://localhost/${LIVENESS_ENDPOINT}:${PORT} || exit 1
