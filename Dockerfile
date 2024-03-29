FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y dos2unix

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8000

# Convenience line to convert CRLF to LF for running on Windows in easy fashion
RUN find . -type f -print0 | xargs -0 dos2unix && apt-get --purge remove -y dos2unix

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - auth.wsgi:application
