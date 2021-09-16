# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Warning: A port below 1024 has been exposed. This requires the image to run
# as a root user which is not a best practice.
# For more information, please refer to https://aka.ms/vscode-docker-python-user-rights
EXPOSE 80

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY . /app

# Install pip requirements
RUN cd /app && python3 -m pip install -r requirements.txt
WORKDIR /app/src

# During debugging, this entry point will be overridden. For more information,
# please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3", "main.py"]
