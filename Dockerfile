# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.7-slim

ENV PORT 5000
EXPOSE 5000 80 8000 2222

# Install ssh & dos2unix
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && apt-get install -y --no-install-recommends dos2unix \
	&& echo "root:Docker!" | chpasswd \
    && mkdir -p /run/sshd

COPY sshd_config /etc/ssh/
RUN dos2unix /etc/ssh/sshd_config

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

# Add code
WORKDIR /app
COPY ./application /app/application
COPY ./blueprints /app/blueprints
COPY wsgi.py /app/wsgi.py

RUN find . -type f -print0 | xargs -0 dos2unix

# Add entrypoint script
COPY docker-init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/docker-init.sh
RUN dos2unix /usr/local/bin/docker-init.sh

# Remove dos2unix
RUN apt-get --purge remove -y dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Start container
CMD gunicorn -b 0.0.0.0:$PORT --workers 1 --timeout 600 wsgi:app
