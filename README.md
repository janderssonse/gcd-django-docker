# gcd-django-docker

This uses Docker and Docker Compose, which need to be installed first.

A plain `docker compose up` starts three services: mysql (db), memcached, and the django dev server (web), matching what production runs. Elasticsearch is the exception; it is optional and only starts with `--profile search`, see the search section below.

After cloning this repo into a directory, and editing the ports if needed, follow these steps:

1. install GCD code - `git clone https://github.com/GrandComicsDatabase/gcd-django.git`
1. optionally change the branch from beta to master, or use your development repo
1. build images - `docker compose build`
1. start services, or use -d in detached mode to see the logs - `docker compose up`
1. run migrations - `docker compose run web /usr/local/bin/python gcd-django/manage.py migrate`

On the first run the mysql setup needs time; compose waits for it via the db healthcheck before starting web. The migrate takes quite some minutes.

This will result in a running website without any data.
Check the names of your containers with `docker compose images`, one is for the db-server (use that as 'db_container_name') and one is for the website-server (use that as 'web_container_name').

To import data, login to the GCD and download a (current) dump from https://www.comics.org/download/.

After unzipping the dump, run the following with the name of the 'current_dump':  
`docker exec -i 'db_container_name' mysql -u gcd-django my-gcd-db -pdb-gcd < 'current_dump'`

To view the website, access http://127.0.0.1:8000/.

To load users into the system, first run the migrations again:  
 `docker compose run web /usr/local/bin/python gcd-django/manage.py migrate`
(note that we currently don't know why the migration needs to be done again) and then use  
`docker compose run web python gcd-django/manage.py loaddata gcd-django/apps/indexer/fixtures/users.yaml`
The three development users are (passwords in ()): `admin (admin)`, `editor (editme)`, and `dexter_1234 (test)`.

Files edited on the host are picked up by the running server directly. To get a shell use `docker exec -it 'web_container_name' bash`; after changing into `gcd-django` you can get a django shell with `python manage.py shell`.

The page cache lives in the memcached container and survives web restarts. Run `docker compose restart memcached` to clear it.

If doing development work on the code for editing, note that right now you cannot edit existing data, since we do not export the change history in the dump. But, you can add new data (with dexter_1234), approve it (with editor), and then edit the newly added data. 

We intend to add changesets for all the existing data to allow their editing in this development setup. As of now we support this for some object types. For that call:  
`export DJANGO_SETTINGS_MODULE=settings`  
`export PYTHONPATH=gcd-django`  
`python setup_initial_changesets.py`  

Doing this for all objects will take some time, so we limit it in the code to the first 500 IDs per object class. You can comment out objects that for now do not need to be edited in your dev environment, or change the limit, by editing the python-file.

To allow approvals to work, the statistics need to exist, for that run the following:  
`docker-compose run web python gcd-django/manage.py runscript reset_stats`

For search, start the optional elasticsearch container and set
USE_ELASTICSEARCH=1 in the web environment, for example:

    USE_ELASTICSEARCH=1 docker compose --profile search up -d

Elasticsearch needs the kernel setting vm.max_map_count to be at least
262144, or the container exits on start:

    sudo sysctl -w vm.max_map_count=262144

The database is reachable from the host at 127.0.0.1:3308 (user
gcd-django, password db-gcd).

To run the test suite, the app user needs privileges on the test
databases that pytest creates. New database volumes get these from
`mysql-init.sql` automatically; if your db volume predates that file,
grant them once with your existing root password:

    docker exec -i 'db_container_name' mysql -uroot -p'root-password' < mysql-init.sql
