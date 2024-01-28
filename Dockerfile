FROM python:3.10-slim

WORKDIR /app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

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
