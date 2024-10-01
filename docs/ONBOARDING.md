### onboarding

- clone the repo
#### local setup
- check that you have Python 3.10 or 3.11 locally installed and working
- check that you have Postgres locally up and running
  - recommended on Macs: use/install [Postgres.app](https://postgresapp.com/) which is a full featured database-in-an-app
  - also recommended on Macs: [Postico](https://eggerapps.at/postico2/) which is a local database GUI
- create a local database
  - recommended on Macs: start Postgres.app, open Postico, connect to localhost with all of the defaults (your computer's username, no password, localhost, port 5432), create a database named `nycnoise`
- duplicate `.env.example` to `.env` and fill out the values
- create a python virtual environment to store/manage the project's dependencies locally:
  - create the virtual environment: `python3 -m venv venv`
  - activate it: `source venv/bin/activate`
  - for windows, this might be either `venv/Scripts/activate`, `./venv/Scripts/Activate.ps1` or, when using git bash: `source venv/Scripts/activate`
  - your terminal should now have a `(venv)` prefix -- this means you're in the virtual environment
- install the dependencies with the venv activated: `pip install -r requirements.txt`
- install pre-commit hooks: `pre-commit install` -- this will run autoformatting and tests on commit
- (see below for the following steps)

#### devcontainer setup
- [Docker](https://www.docker.com/products/docker-desktop/) has to be installed 
- [VSCode](https://code.visualstudio.com/Download) (recommended) [setup](https://code.visualstudio.com/docs/devcontainers/containers#_installation)
  - (alternative) [IntelliJ](https://www.jetbrains.com/help/idea/connect-to-devcontainer.html) 
  - (alternative) run devcontainer via [cli](https://code.visualstudio.com/docs/devcontainers/devcontainer-cli#_development-containers) (need to expose ports manually)
- open a project in a devcontaier
- create a database named **nycnoise** ` psql -c "CREATE DATABASE nycnoise"`

#### almost there! finally...
- run the migrations: `python manage.py migrate`
  - if this works, that means that Django can talk to your local database. that's really great!
  - if you have trouble here - it could be due to the Postgres server not running or the database doesn't exist, or the connection string in `.env` is wrong
  - for windows: if you're getting a password error, try changing the USER in the .env document to USER:Password@
  - if you already had passwords set for all users, make sure Password in the DATABASE_URL is the password for USER
- create a superuser: `python manage.py createsuperuser`
  - locally, I recommend `admin`/`admin` (username/password) and a made up email like `a@a.ca`
  - you will get a warning about the bad password :-) ignore it :-) (it's fine for local development)
  - for Windows: you might need to use `winpty python manage.py createsuperuser` instead
- run the server: `python manage.py runserver`
  - you should be able to visit http://localhost:8000 and see the site
  - you should be able to visit http://localhost:8000/admin and log in with the superuser you just created
- you're all set!
