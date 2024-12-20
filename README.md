# D'hondt Calculation System 

Web based D'hondt Calculation System for allocating seats in parliaments among federal states, or in proportional representation among political parties.
For more information please [read the article](https://en.wikipedia.org/wiki/D%27Hondt_method).


## Projects Components


### Web server and API

This project was developed based on Python [Flask](https://flask.palletsprojects.com/en/stable/) web application framework for API and web server.

In addition to Flask, [Marsmallow](https://flask-marshmallow.readthedocs.io/en/latest/) (an object serialization/deserialization library) is used to validate both received parameters and answers.

Flask is running in a single service using docker container.


### Database

The project use OR [PosgreSQL](https://www.postgresql.org/) as **RDBMS**. 

The project use [SQLAlchemy](https://www.sqlalchemy.org/) as Python SQL Toolkit and Object Relational Mapper (ORM) along with [Alembic](https://alembic.sqlalchemy.org/en/latest/) as migration tool. 

 
## API Definition

The project provides the OpenAPI specification file (src/web/dhondt.yaml) where the API is described.

To see the specification click in the following link [API Specification](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/est3bf/dhondt/refs/heads/master/src/web/dhondt.yaml) 


## Database Schema Definition


<p align="center">
  <img src="doc/dhondt_db.png">
  <br/>
</p>


## How to use
 
### Using utils.sh commands helper

We can use utils.sh to easily build, run application and testing the API.
This file contains many bash alias commands to perform all things

1. Sourcing the helper commands
   First we need to include the helpers commands executing in the root folder 
   ```
    $ source utils.sh
    ```

2. **Building and running application**
   To build and run the application stopping containers previously executed:
   1. **For production**:   
     ```
     $ drest
     ```
   2. **For debuging**:   
     ```
     $ drest_dev
     ```
    
3. **Stoping container**
   To stop all containers:
   ```
   $ downd
   ```
   or
   ```
   $ dod
   ```

4. **Executing unit and CI tests**
    When we use those commands to execute tests we can see at the end the execution report.
   1. __Execute Unit tests__
     ```
     $ execute_unit_testing
     ```
   2. __Execute CI tests__
     ```
     $ execute_ci_testing
     ```
5. **Backup Database**
   We can backup and restore the database. A new folder **db_data** is created to store files.
   Each time that a new backup is created (executed), a new folder is created (named with the time) to store the information.
   **Note** Do not remove or delete this folder until execute the restore command. All data will be lost deleting the folder.
    1. __Backup__
     ```
     $ bkp_data
     ```
    2. __Restore the database__****
     The following command will restore the last backuped database. 
     ```
     $ restore_last_data
     ```
    3. __Clear database__
     If we want to clear all database information (delete the entirely volumen) we can execute the following command:
     ```
     $ clear_db
     ```
     **Warning!** Don't forget backup the database before execute this command or all information will be lost. 
     


### Manually build and run containers

We build the repo images using docker compose.
The following is for build and run manually using docker commands.

1. **Getting docker running**.**
    **Note:** do not forget to add your user to docker group:
    ```
    $ sudo adduser youruser docker**
    ```
2. **Building the image**:
   1. __For production__:
        ```
        $ docker compose -f .gci/docker-compose.yml  -p [project name] build dhondt
        ```
        [project name] is the project name which the image and container will have.
        For example:
        ```
        $ docker compose -f .gci/docker-compose.yml  -p msa_dhondt build dhondt
        ```
    2. __For debug__:
        ```
        $ docker compose -f .gci/docker-compose.yml  -f .gci/docker-compose-dev.yml -p [project name] build dhondt
        ```
        [project name] is the project name which the image and container will have.
        For example:
        ```
        $ docker compose -f .gci/docker-compose.yml  -f .gci/docker-compose-dev.yml -p msa_dhondt build dhondt
        ```
    3. __For unit-testing__:
        ```
        $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p [project name] build dhondt unit_testing 
        ```
        [project name] is the project name which the image and container will have.
        For example:
        ```
        $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p msa_dhondt build dhondt unit_testing         
        ```
    4. __For ci-testing__:
        ```
        $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile ci_test -p [project name] build dhondt ci_testing 
        ```
        [project name] is the project name which the image and container will have.
        For example:
        ```
       $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile ci_test -p [project name] build dhondt ci_testing          
        ```

    5. __Create docker volume for database__
        ```
        $ docker volume create data_postgres
        ```
        
3. **Running containers**:
   1. __For production__:
        ```
        $ docker compose -f .gci/docker-compose.yml  -p [project name] up -d 
        ```
        [project name] is the project name which the image and container will have.
        For example:
        ```
        $ docker compose -f .gci/docker-compose.yml  -p msa_dhondt up -d 
        ```
    2. __For debug__:
        ```
        $ docker compose -f .gci/docker-compose.yml  -f .gci/docker-compose-dev.yml -p [project name] build dhondt
        ```
        [project name] is the project name which the image and container will have.
        For example:
        ```
        $ docker compose -f .gci/docker-compose.yml  -f .gci/docker-compose-dev.yml -p msa_dhondt up -d
        ```
    3. __For unit-testing__:
        ```
        $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p [project name] up -d 
        ```
        [project name] is the project name which the image and container will have.
        For example:
        ```
        $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile unit_test -p msa_dhondt up -d        
        ```
    4. __For ci-testing__:
        ```
        $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile ci_test -p [project name] up -d 
        ```
        [project name] is the project name which the image and container will have.
        For example:
        ```
        $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml --profile ci_test -p msa_dhondt up -d         
        ```

4. **Stoping containers**
    ```
    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml -p [project name] down 
    ```
    [project name] is the project name which the image and container will have.
    For example:
    ```
    $ docker compose -f .gci/docker-compose.yml -f .gci/docker-compose-dev.yml -f .gci/docker-compose-testing.yml  -p msa_dhondt down
    ```

