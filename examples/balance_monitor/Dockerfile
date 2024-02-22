FROM ext/sentinel/base:v0.3.0

ENV SENTINEL_SDK_PKG="ext_sentinel_py_sdk-0.3.5.post8+git.ec42de5a.dirty-py3-none-any.whl"

COPY ${SENTINEL_SDK_PKG} /tmp

RUN echo "[INFO] Install Sentinel Python SDK" \
        && pip install --break-system-packages /tmp/${SENTINEL_SDK_PKG} \
    && echo "[INFO] Creating sentinel user" \
        && adduser -D -u 1000 -s /usr/local/bin/fish sentinel \
        && echo 'sentinel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

# Add repository code
WORKDIR /opt/sentinel/

USER sentinel

# Copy Attack Detector SDK code
COPY . /opt/sentinel/

ENTRYPOINT [ "sentinel" ]
