# Notelist
Notelist is a tag based note taking REST API written in Python and based on the
Flask framework.

Main features:

- Users, notebooks and notes management
- JWT based authentication
- MongoDB, DynamoDB or a local JSON file for the data storage

#### Project information:
- Version: 0.7.3
- Author: Jose A. Jimenez (jajimenezcarm@gmail.com)
- License: MIT License
- Repository: https://github.com/jajimenez/notelist

## How to install

You can download and install Notelist CLI from the **PyPI** repository with
**PIP**:

```bash
pip install notelist
```

## How to build

To generate the **built package** and the **source archive**, run the following
commands (the *wheel* Python package is required for generating the built
package):

```bash
python setup.py bdist_wheel sdist
```

## How to run

To run Notelist, you can set the following **environment variables**:

**Main variables:**

- `FLASK_APP`:<br>
Its value must be the Notelist package name (`notelist`) if you are running the
API through the Python package once its installed or the path to the API source
code directory (`src/notelist`) if you are running the API through the project
directory.

- `NL_SECRET_KEY`:<br>
The Secret Key is used for storing session information specific to a user from
one request to the next. Its value must be a **random** sequence of characters
and must be kept **secret**.

- `NL_DB_SYS`:<br>
Database system (`mongodb`, `dynamodb` or `localst`). `localst` (local JSON
file) should be used only for testing purposes.

- `NL_ALLOW_ORIG` (optional):<br>
Value of the **Access-Control-Allow-Origin** response header. The value of this
header determines which host is allow to make requests to the API from a
front-end application (from JavaScript code).<br><br>
If this API is used through a front-end application and the API and the
front-end application are in the same host, then it's not needed to set this
header. If the API and the front-end are in different hosts, then the header
must be set to the host of the front-end application (starting with
"https://").<br><br>
The value `*` for the header allows a front-end from any host to make requests
to the API but this is not recommended and is not supported by all browsers.

- `NL_ROOT_DOC` (optional):<br>
If its value is `1`, the root route (`/`) returns a documentation page. If its
value is `0` (default), the root route returns a 404 error response.

**MongoDB variables (only if `NL_DB_SYS` is `mongodb`):**

- `NL_MONGODB_URI`:<br>
MongoDB URI (e.g. `mongodb://username:password@localhost:27017`).

- `NL_MONGODB_DB`:<br>
MongoDB database name (e.g. `notelist`).

- `NL_MONGODB_US_COL`<br>
MongoDB users collection name (e.g. `users`).

- `NL_MONGODB_NB_COL`<br>
MongoDB notebooks collection name (e.g. `notebooks`).

- `NL_MONGODB_NO_COL`<br>
MongoDB notes collection name (e.g. `notes`).

- `NL_MONGODB_BL_COL`<br>
MongoDB block list collection name (e.g. `blocklist`). This collection stores
temporary data about revoked access tokens.

**DynamoDB variables (only if `NL_DB_SYS` is `dynamodb`):**

- `NL_DYNAMODB_AWS_ENDPOINT` (optional):<br>
AWS endpoint URL (e.g. `http://localhost:8000`).

- `NL_DYNAMODB_AWS_REGION` (optional):<br>
AWS region name (e.g. `eu-west-1`).

- `NL_DYNAMODB_AWS_ACCESS_KEY_ID` (optional):<br>
AWS Access Key ID.

- `NL_DYNAMODB_AWS_SECRET_ACCESS_KEY` (optional):<br>
AWS Secret Access Key.

- `NL_DYNAMODB_AWS_SESSION_TOKEN` (optional):<br>
AWS Session Token.

- `NL_DYNAMODB_US_TAB`<br>
DynamoDB users table name (e.g. `users`).

- `NL_DYNAMODB_NB_TAB`<br>
DynamoDB notebooks table name (e.g. `notebooks`).

- `NL_DYNAMODB_NO_TAB`<br>
DynamoDB notes table name (e.g. `notes`).

- `NL_DYNAMODB_BL_TAB`<br>
DynamoDB block list table name (e.g. `blocklist`). This table stores
temporary data about revoked access tokens.

**Local Storage variables (only if `NL_DB_SYS` is `localst`):**

- `NL_LOCALST_PATH`:<br>
JSON file path (e.g. `maindb.json`).

Once the environment variables are set, you can **create a user** by running:

```bash
flask user create <username> <password> <admin> <enabled> <full-name> <e-mail> 
```

- admin = `0` (default) or `1`
- enabled = `0` (default) or `1` (if value is 0, the user won't be able to log
  in)
- Example for an administrator user: `flask user create admin somepassword 1 1`

To run Notelist on a **local development** server (**not** for a production
environment) from the Python package installed, run the following command:

```bash
flask run
```

Alternatively, you can run Notelist through the `run.py` script in the API
source code directory (`src/notelist`):

```bash
cd src
python run.py
```

To run Notelist in a **production** environment, you should do it through a
**WSGI** server (e.g. Gunicorn). You can install **Gunicorn** through the
`requirements_pro.txt` file:

```bash
pip install -r requirements_pro.txt
```

Once you have both Notelist and Gunicorn installed, you can run Notelist
through Gunicorn running the following command (in this example we set 1 worker
process listening to connections from outside our computer on port 5000):

```bash
gunicorn -b 0.0.0.0:5000 notelist:app
```

## How to run with Docker

You can run a Docker container with Notelist. For example, the following
command downloads the Docker image from the Docker Hub repository and runs a
container from the image using a single JSON file stored in the container:

```bash
docker container run --name notelist -d -p 5000:5000 \
-e NL_SECRET_KEY="<key>" \
-e NL_ROOT_DOC=1 \
-e NL_DB_SYS=localst \
-e NL_LOCALST_PATH=/home/notelist.json \
jajim/notelist:0.7.3
```

Where `<key>` must be a long random sequence of characters and must be kept
secret.

Using a single JSON file for the data storage should be only for testing
purposes. For production use, you should run a container which uses MongoDB or
DynamoDB.

Once the container is running, you can create a user with the following
command:

```bash
docker container exec -it notelist create-user <username> <password> <admin> <enabled> <name> <email>
```

- admin: `0` (default) or `1`
- enabled: `0` (default) or `1` (if it's 0, the user won't be able to log in)
- Example for an administrator user: `docker container exec -it notelist
create-user admin pw_example 1 1`

## How to run with Docker Compose

The easiest way to try Notelist is by using **Docker Compose** to run a
container for the API and a MongoDB container for the data storage. To create
and run the containers, run the following command from the same directory of
the `docker-compose.yml` file (the project directory):

```bash
docker compose up -d
```

Once the containers are running, you can create, for example, an administrator
user with this command:

```bash
docker container exec -it notelist-api create-user admin somepassword 1 1
```

## How to run the unit tests

To run all the unit tests, run the following command from the project
directory:

```bash
python -m unittest discover test
```

Read the `test/env.py` file for information about how to run MongoDB and
DynamoDB integration tests.

## Documentation

You can find the documentation of all the operations of the API by running the
API with the  `NL_ROOT_DOC` environment variable set to `1` and navigating to
the root route (`/`) in a browser.

## DynamoDB tables definition

If you use DynamoDB as the database system for Notelist, you need to create the
tables before running the API. The following is the definition of each table
(you can set any name for the tables).

### users

- Partition key: `id` (string)
- Global index:
  - Name: `username_index`
  - Partition key: `username` (string)

### notebooks

- Partition key: `id` (string)
- Global index 1:
  - Name: `user_id_index`
  - Partition key: `user_id` (string)
- Global index 2:
  - Name: `user_id_name_index`
  - Partition key: `user_id` (string)
  - Sort key: `name` (string)

### notes

- Partition key: `id` (string)
- Global index:
  - Name: `notebook_id_index`
  - Partition key: `notebook_id` (string)

### blocklist

- Partition key: `id` (string)
- Field to enable TTL with: `expiration`.

## Request examples

The following are some examples of requests to the Notelist API with the `curl`
command assuming that the API is running on our local computer and listening on
port 5000.

Log in:

```bash
curl -X 'POST' 'http://localhost:5000/auth/login' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"username": "<username>", "password": "<password>"}'
```

Create a notebook:

```bash
curl -X 'POST' 'http://localhost:5000/notebooks/notebook' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <access_token>' \
-d '{"name": "Example Notebook"}'
```

Create a note:

```bash
curl -X 'POST' 'http://localhost:5000/notes/note' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <access_token>' \
-d '{"notebook_id": "<notebook_id>", "archived": false, "title": "Example Note", "body": "This is a test note", tags: ["tag_name_1", "tag_name_2"]}'
```

Get the notes of a notebook by a filter:

```bash
curl -X 'POST' 'http://localhost:5000/notes/notes/<notebook_id>' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <access_token>' \
-d '{"archived": false, "tags": ["tag_name_1", "tag_name_2"]}'
```

Search for notebooks and notes that match a given text:

```bash
curl -X 'GET' 'http://localhost:5000/search/<search>' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <access_token>'
```

Log out:

```bash
curl -X 'GET' 'http://localhost:5000/auth/logout' \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <access_token>'
```
