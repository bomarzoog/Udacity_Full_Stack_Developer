# Casting Agency Capstone

Casting Agency API is the Udacity Full Stack NanoDegree Capstone Project.

Casting Agency API models a company that is responsible for creating movies and managing and assigning actors to those movies.
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the root directory of this project and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

After installing the dependencies, execute the bash file `setup.sh` to set the user jwts, auth0 credentials and the remote database url by naviging to the root directory of this project and running:

```bash
source setup.sh
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Database Setup

With Postgres server running, create a new database load the backup in `casting_agency.psql` provided file by running from the project directory:

```bash
./setup.sh

pg_ctl -D /usr/local/var/postgres stop
pg_ctl -D /usr/local/var/postgres start

psql -U postgres < db_setup.sql
psql casting_agency  < casting_agency.psql

```

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource not found."
}
```

The API will return three error types with multiple different error messages when requests fail:
- 401: Authorization header is expected.
- 401: Authorization header must start with "Bearer".
- 401: Token not found.
- 401: Authorization header must be bearer token.
- 401: Authorization malformed.
- 401: Token expired.
- 401: Incorrect claims. Please, check the audience and issuer.

- 403: Permission denied.

- 422: Unprocessable.

- 404: Resource Not Found.

### Endpoints

#### GET '/actors'
- Fetches a paginated list of actors.
- Request Arguments: offset: 1(default), limit: 30(default).
- Returns: list of actors ordered by id.
```

{
  'success': True,
  'actors': [
    {
      id: 1,
      name: 'Actor 1',
      age: 30,
      gender: 'male'
    }
  ]
}
```

#### GET '/movies'
- Fetches a paginated list of movies.
- Request Arguments: offset: 1(default), limit: 30(default).
- Returns: list of movies ordered by id.
```
{
  'success': True,
  'movies': [
    {
      id: 1,
      title: 'New Movie 1',
      release_date: '2021-10-1 04:22'
      category: 'Action'
    }
  ]
}
```

#### POST '/actors'
- Create a new actor.
- Request Arguments: { name: String, age: Integer, gender: String }.
- Returns: An object with `success: True` and the new actor inside an array.
```
{
  'success': True,
  'actor': 
    {
      id: 2,
      name: 'Actor 2',
      age: 28,
      gender: 'Female'
    }
}
```

#### POST '/movies'
- Create a new movie.
- Request Arguments: { title: String, category: String, release_date: DateTime }.
- Returns: An object with `success: True` and the new movie inside an array.
```
{
  'success': True,
  'movie': 
    {
      id: 2,
      title: 'New Movie 2',
      release_date: '2022-10-1 04:22'
      category: 'fiction'
    }
}
```

#### Patch '/actors/<actor_id>'
- Update an actor.
- Request Arguments: { name: String, age: Integer, gender: String }.
- Returns: An object with `success: True` and the updated actor inside an array.
```
{
  'success': True,
  'actor': 
    {
      id: 1,
      name: 'Updated Actor',
      age: 50,
      gender: 'Male'
    }
}
```

#### Patch '/movies/<movie_id>'
- Update a movie.
- Request Arguments: { title: String, category: String, release_date: DateTime }.
- Returns: An object with `success: True` and the updated movie inside an array.
```
{
  'success': True,
  'movie': 
    {
      id: 1,
      title: 'Updated Movie 1',
      release_date: '2030-10-1 04:22'
      catgeory: 'Action'
    }
}
```

#### DELETE '/actors/<actor_id>'
- Removes an actor from the database.
- Request Parameters: question id slug.
- Returns: An object with `success: True` and the id of the deleted actor
```
{
  'success': True,
  'id': 1
}
```

#### DELETE '/movies/<movie_id>'
- Removes a movie from the database.
- Request Parameters: question id slug.
- Returns: An object with `success: True` and the id of the deleted movie
```
{
  'success': True,
  'id': 1
}
```

## Testing

#### Running tests locally
To run the tests from ./test_app.py, first make sure you have ran and executed the setup.sh file to set the enviorment.

After setting the enviorment start your local postgress server:
```bash

./setup.sh

pg_ctl -D /usr/local/var/postgres stop
pg_ctl -D /usr/local/var/postgres start

psql -U postgres < db_setup.psql
psql casting_agency  < casting_agency.psql
```

Then run the follwing commands to run the tests:
```
pytest test_app.py
```

All 22 tests should pass:

```
====================================================================== test session starts ======================================================================
platform darwin -- Python 3.7.3, pytest-7.1.1, pluggy-1.0.0
rootdir: /Users/admin/Capstone_2
collected 22 items                                                                                                                                              
test_app.py ......................    

================================================================ 22 passed, 25 warnings in 2.79s ================================================================

```


## Heroku Deployment

```
Casting_Agency API can be accessed on heroku on: https://fsnd-capstone-bomarzoog.herokuapp.com/

```

### Heroku Test Example

#### Request
```
 curl https://fsnd-capstone-bomarzoog.herokuapp.com/movies -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijd5SHU3UmVadzFIYkgxcGNKY3BUbyJ9.eyJpc3MiOiJodHRwczovL2Rldi12eHFudmJ0aC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI1ODc5NTNjN2E1Y2UwMDY4NTE0MDQ5IiwiYXVkIjoiZnNuZC1jYXBzdG9uZSIsImlhdCI6MTY1MDA1NjgzOCwiZXhwIjoxNjUwMTQzMjM2LCJhenAiOiJOVmZXa1phZ2tOa0t0UFp2bUR5Y2R3Tks2Y3pydDZ5SCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.ZBKgEq9O_O4hKO_IVQ3VpZ2oyQ6KedarEyX9DPs96C1GwMxKmYVCfohYvEwx82m1I10lqSCypMocLxbzVEX2gTV9s5DyUlTqsCa1CrYHVrxmikPTeDUCBkc9nDLnBqcVxi5fR06sO6nGZm2AZOkEkXm7_rJAGftIYmLdGd3JEXWBp4TrdCdD_kI96KHwHe8sLXTpH6J-5MDLCz7PCLHqI0o_hCRtGSOYFbDHNhipGhjweDSNucSBHI9pYQZsbYNGNlZ1l1gOshvJhMMLFyhUSNJ9m8cvdpNWemM8Xfz4PzoBo7vuRmbmnwJ01U9trPveWUFJYCv3NqzFqXqSyU0CZw'
 
 
 ```

 #### Response
```
 {
  "movies": [
    {
      "category": "Action",
      "id": 1,
      "release_date": "2019-11-11",
      "title": "movie1"
    },
    {
      "category": "fiction",
      "id": 2,
      "release_date": "2020-11-11",
      "title": "movie2"
    },
    {
      "category": "horror",
      "id": 3,
      "release_date": "2020-11-11",
      "title": "movie3"
    },
    {
      "category": "history",
      "id": 4,
      "release_date": "2021-11-11",
      "title": "movie4"
    }
  ],
  "success": true,
  "total": 4
}
```