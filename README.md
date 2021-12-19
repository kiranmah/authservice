# authservice

Authentication application to be used in a microservice architecture. Check out the project's [documentation](http://kiranmah.github.io/authservice/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up -d
```

Application set to run in debug mode by default, to test in production mode, the docker-compose.yml should be adjusted such that an additional environment variable is added to the `web` service.

```docker
 - DJANGO_CONFIGURATION=Production
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Test

Start the dev server for local development:
```bash
docker-compose up -d
```

Run the following command to execute tests

```bash
docker-compose run --rm web python manage.py test
```

[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)
