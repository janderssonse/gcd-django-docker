# gcd-django-docker

This repository contains a local Docker Compose environment for
[`gcd-django`](https://github.com/GrandComicsDatabase/gcd-django). The Django
application is a separate repository and is cloned into `./gcd-django` during
setup.

Docker and Docker Compose are required. Run the commands below from the root of
this repository.

## Setup

Clone the application source into the directory expected by the Docker build:

```bash
git clone https://github.com/GrandComicsDatabase/gcd-django.git gcd-django
```

The clone uses the `beta` branch by default. To use `master` instead:

```bash
git -C gcd-django switch master
```

Build the web image, start the services, and create the database schema:

```bash
docker compose build
docker compose up -d
docker compose run --rm web python gcd-django/manage.py migrate
```

The first MySQL startup can take a few minutes. Compose waits for its health
check before starting the web service. The site is available at
http://127.0.0.1:8000/.

View the web logs with:

```bash
docker compose logs -f web
```

## Editing the Application

The `gcd-django/` directory contains the application source. Edit files there
with the editor and Git tools on the host.

Compose mounts that directory at `/code/gcd-django` in the `web` container,
where Django runs. The image includes `vim` for editing inside the container:

```bash
docker compose exec web bash
cd gcd-django
vim path/to/file
```

Both workflows edit the same checkout. Changes made in the container appear in
`./gcd-django` on the host and remain after the container is removed. The
development server detects changes from either workflow and reloads
automatically. Rebuild the image only when `gcd-django/requirements.txt`
changes.

## Importing Data

Download and extract a current database dump from
https://www.comics.org/download/, then import it with:

```bash
docker compose exec -T db mysql -u gcd-django -pdb-gcd my-gcd-db < current_dump
```

Run migrations after the import and load the development users:

```bash
docker compose run --rm web python gcd-django/manage.py migrate
docker compose run --rm web python gcd-django/manage.py loaddata gcd-django/apps/indexer/fixtures/users.yaml
```

The users are `admin` (`admin`), `editor` (`editme`), and `dexter_1234`
(`test`).

Downloaded dumps do not include the change history needed to edit existing
records. Newly added records can be edited normally. To create development
changesets for the supported record types, run:

```bash
docker compose exec web env DJANGO_SETTINGS_MODULE=settings PYTHONPATH=gcd-django python setup_initial_changesets.py
```

The script processes the first 500 records of each supported type. Rebuild
statistics before testing approvals:

```bash
docker compose run --rm web python gcd-django/manage.py runscript reset_stats
```

## Useful Commands

Open a Django shell:

```bash
docker compose exec web python gcd-django/manage.py shell
```

Stop the services without deleting the database volume:

```bash
docker compose down
```

Elasticsearch is not included, so full-text search is unavailable.
