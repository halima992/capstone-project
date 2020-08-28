# capstone-project

The project is a Casting Agency Specifications. the purpose of this project is managing movies and actors by production new movies. Beside that, selecting actors and assign them to certain movies. moreover that, we can delete or made modification in actors or movies. hence, we have three users in this application
> Assistant: can view actors and movies

> Director:can view and update actors and movies.Beside that,can insert and delete actors only

> Producer:can view , update , delete , and insert both of actors and movies.

The technical purposes is to applied what is learning in Full stack program such as :
* Architecting a relational database 
* Using SQLAlchemy to process database queries
* Artirceting API and following RESTful principles
* Handling error and test API end point
* Enabling Role Based Authentication and roles-based access control
* Using Auth0 as third-party to configure authentication and roles-based access control
* finally deployment this application in heroku 

The URL of this application -> https://capstoneproject2.herokuapp.com/

# starting and setup

## for running this application in local machine 
1.  open terminal and directory of project
2. run `bash pip install -r requirements.txt`
3. set up **DATABASE_URL** in commad line by `bash set DATABASE_URL={DATABASE_URL} ` **note** for mac `export` not `set`
4. set up  authentication and roles at auth0.the permissions in this project categorized into 3 categories according to roles
  * ASSISTANT 
   ```bash 
   'get:actors'
   'get:movies'
   ```
  * DIRECTOR 
   ```bash 
     'get:actors'
     'get:movies'
     'post:actors'
     'delete:actors'
     'patch:actors'
     'patch:movies'
   ```
  * PRODUCER 
   ```bash 
     'get:actors'
     'get:movies'
     'post:actors'
     'post:movies'
     'delete:actors'
     'delete:movies'
     'patch:actors'
     'patch:movies'
   ```
     *note* the token jwt for three roles ```assistant```,```director``` and ```producer``` are saved in setup.sh , you also need to `setup ```API_AUDIENCE``` , ```ALGORITHMS```,and ```AUTH0_DOMAIN```as you doing with database
4. Set up FLASK_APP and run it
    ```bash
    export FLASK_APP=app.py
    run flask
    ```
5. running the test 

    To run test run the following :

    ```bash
    dropdb capstone_test
    createdb capstone_test
    psql capstone_test < capstone.psql
    export three tokens `ASSISTANT`,`DIRECTOR` and `PRODUCER`
    python test_app.py
    ```
    *note* `createdb` and `dropdb` doesn't work on Windows directly .So rather than using `CREATE DATABASE`, and `DROP database` in `psql `command. Also this command `psql capstone_test < capstone.psql` in windows should specific owner like this  `psql -U postgres capstone_test < capstone.psql`
# Endpoint

The endpoints in this project as following:

- ## GET /actors

    **In general** return list of actors
```bash
{
    "actors": [
        {
            "actor": "Jene Leavy",
            "gender": "Female",
            "id": 1,
            "movie": "Don't Breathe"
        },
        {
            "actor": "Dylan Minnete",
            "gender": "Male",
            "id": 2,
            "movie": "Don't Breathe"
        },
        {
            "actor": "Erasmo Carols",
            "gender": "Male",
            "id": 3,
            "movie": "Airplane Mode"
        },
        {
            "actor": "Larissa Manolean",
            "gender": "Female",
            "id": 4,
            "movie": "Airplane Mode"
        },
        {
            "actor": "Nick Purcha",
            "gender": "Male",
            "id": 5,
            "movie": "Dangerous Lies"
        },
        {
            "actor": "Kate Winslet",
            "gender": "Female",
            "id": 6,
            "movie": "The Dressmaker"
        }
    ],
    "success": true
}
```
- ## GET /movies

    **In general** return list of movies

```bash
{
    "movies": [
        {
            "catogry": "Drama",
            "id": 1,
            "movie": "The Dressmaker"
        },
        {
            "catogry": "Horror",
            "id": 2,
            "movie": "Jason Voorhees"
        },
        {
            "catogry": "Horror",
            "id": 3,
            "movie": "Don't Breathe"
        },
        {
            "catogry": "Drama",
            "id": 4,
            "movie": "Airplane Mode"
        },
        {
            "catogry": "Drama",
            "id": 5,
            "movie": "Dangerous Lies"
        }
    ],
    "success": true
}

 ```

## DELETE /actors/ <int:id>

**In general** Return deleted actor 

```bash
{
  "Deleted": 5,
  "success": true
}
```

## DELETE /movies/ <int:id>

**In general** Return deleted movie 

```bash
{
  "Deleted": 3,
  "success": true
}
```
## POST /actors

**In general** Return  success true for posting new actor

```bash
{
  "success": true
}
```
## POST /movies

**In general** Return  success true for posting new movie

```bash
{
  "success": true
}
```

## PATCH /actors/ <int:id>

**In general** Return  modifed actor 

```bash
{
    "actor": [
        {
            "actor": "rayen Badian",
            "gender": "Male",
            "id": 9,
            "movie": "The Godfather"
        }
    ],
    "success": true
}
```
## PATCH /movies/ <int:id>

**In general** Return  modifed movie 

```bash
{
    "movie": [
        {
            "catogry": "Romantic",
            "id": 7,
            "movie": "All the Bright Places2"
        }
    ],
    "success": true
}
```

# Erorr handler

 erros also returned as json not  html For example as following in bad request:

```bash
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```


The API will return diffrent types of errors:

1. 400 –> bad request
2. 404 –> not found
3. 422 –> unprocessable
4. 500 -> internal server error

# Deployment
for running app in Heroku we need to follow set of steps as following:
1. Install Heroku
2. saveig our package requirements by using command 

```bash

    pip freeze > requirements.txt

```
*note*: with any installation you should update by this command.

3. touch Profile and install gunicorn package
  * install gunicorn by command
    ```bash
     pip install gunicorn
     ```
 * houseing app in app.py by this instruction Procfile

    ```bash
        web: gunicorn app:app
    ```
4.  Install the following package
    ```bash
        pip install flask_script
        pip install flask_migrate
        pip install psycopg2-binary
    ```
5. doing local migration
 ```bash   
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
```
6. Creating Heroku app
```bash  
    heroku create name_of_your_app
```
7. Adding git remote for Heroku to local repository
```bash  
    git remote add heroku heroku_git_url
```
8. Add postgresql  for database
```bash  
    heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
```
9. Add all the Variables in Heroku by click Reveal Config Vars
```bash
    DATABASE_URL
    AUTH0_DOMAIN
    ALGORITHMS
    API_AUDIENCE
    ASSISTANT
    DIRECTOR
    PRODUCER
```
10. Push to Heroku
```bash
    git push heroku master
```
11. Run Migrations for database in Heroku 
```bash
    heroku run python manage.py db upgrade --app name_of_your_application
```