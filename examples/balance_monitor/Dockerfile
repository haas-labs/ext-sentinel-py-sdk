FROM ext/sentinel/base:0.3.0


RUN echo "[INFO] Creating sentinel user" \
        && adduser -D -u 1000 -s /usr/local/bin/fish sentinel \
        && echo 'sentinel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

# Add repository code
WORKDIR /opt/sentinel/

USER sentinel

# Copy Balance Monitor code
COPY . /opt/sentinel/

ENTRYPOINT [ "sentinel" ]
