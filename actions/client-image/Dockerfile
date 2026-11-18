FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1 AS product

ARG COMPONENT
ARG WHEEL_SHA256
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
COPY *.whl /build/
RUN set -eu; \
    case "$COMPONENT" in cli) executable=lightnow ;; proxy) executable=lightnow-proxy ;; *) exit 1 ;; esac; \
    set -- /build/*.whl; test "$#" -eq 1; \
    echo "$WHEEL_SHA256  $1" | sha256sum -c -; \
    root="/client-bundle/$COMPONENT"; mkdir -p "$root/dependencies"; \
    python -m venv "/opt/$COMPONENT"; pip="/opt/$COMPONENT/bin/pip"; \
    "$pip" download --no-cache-dir --only-binary=:all: --dest "$root/dependencies" "$1"; \
    "$pip" install --no-cache-dir --no-index --find-links "$root/dependencies" "$1"; \
    "$pip" check; mv "$1" "$root/"; \
    rm "$root/dependencies/$(basename "$1")"; \
    (cd "$root" && sha256sum ./*.whl dependencies/*.whl > SHA256SUMS); \
    ln -s "/opt/$COMPONENT/bin/$executable" "/usr/local/bin/$executable"; \
    useradd --create-home --uid 1000 featurestack
LABEL org.opencontainers.image.source="https://github.com/lightnow-ai/lightnow-${COMPONENT}" \
      ai.lightnow.client.component="${COMPONENT}" \
      ai.lightnow.client.wheel.sha256="${WHEEL_SHA256}"
USER 1000:1000
WORKDIR /home/featurestack

FROM product AS cli
CMD ["lightnow"]

FROM product AS proxy
EXPOSE 8080
CMD ["lightnow-proxy"]
