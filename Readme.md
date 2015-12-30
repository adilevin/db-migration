#Safe Database Migration Pattern Without Downtime

Adi Levin, December 28, 2015

#Introduction

This is a demonstration of the safe database migration pattern introduced by 
Aviran Mordo in [his blog post](http://www.aviransplace.com/2015/12/15/safe-database-migration-pattern-without-downtime/).
We start by running the application on top of [SQLite](https://www.sqlite.org/), 
and we follow Aviran Mordo's 8 steps to migrate to [MongoDB](https://www.mongodb.org/), 
without downtime.

#The 8 steps for a safe migration

For a more complete description of the pattern, please go to 
[Aviran Mordo's blog post](http://www.aviransplace.com/2015/12/15/safe-database-migration-pattern-without-downtime/).

1. Deploy new database into production
2. Add new data access object in the app to write to the new database
3. Start writing to the new database but use the old one as primary
4. Read from both databases
5. Make the new database the primary
6. Stop writing to the old database
7. Migrate data from the old database to the new one
8. Delete the old data access object

#What's included in this repository

1. Flask application, in folders *main, data_access_objects, model*, and unit tests in *test*.
2. HTML + Javascript + CSS for the user console and automatic task producer, in folder *main/static*
3. An initial NGINX configuration file in folder *nginx*
4. The *spawn.bat* to spawn a running instance of the application at a given port (on Windows)

#Setup

###Install dependencies

- [Install Python 2.7](https://www.python.org/downloads/)

- [Install MongoDB](https://docs.mongodb.org/manual/)

- [Install greenlet package](https://pypi.python.org/pypi/greenlet), a prerequisite for gevent
>`pip install greenlet`

- [Install gevent](http://www.gevent.org/) as the WSGI server

- [Install NGINX](http://nginx.org/en/download.html) which we use as a reverse proxy, to 
switch application versions without downtime 

###Setup databases

- Start a MongoDB instance by running
>`mongod`

- Prepare an SQLite production environment by creating a folder where the application will place the sqlite production
database
> `mkdir c:\sqlite`

###Setup Python project

- Clone the repository

- Run tests from the repository root folder
> `python -m unittest discover -s test`

###Setup reverse proxy

- Copy <repository_root>/nginx/nginx.conf to the conf subfolder in the nginx installation folder. It routes traffic from port 5000 to port 8000.
 
- Run NGINX
> start nginx

###Run application on port 8000
 
- Open a command-line in the db-migration folder

 > `set PYTHONPATH=.` (on Windows)

 > `python main/main.py 8000`

- Open a user console ([localhost:5000](http://localhost:5000)) 

- Open an automatic task producer ([localhost:5000/static/taskProducer.html](localhost:5000/static/taskProducer.html))

#The user console

This is a ToDo application, where users can see their remaining tasks and mark them as done, by clicking checkboxes.
For the user console, open [http://localhost:5000](http://localhost:5000) when the app is running.
The page also displays the server configuration and refreshes it every 3 seconds. The server configuration panel
will change its color when the configuration changes.

To refresh the task list, you must hit the refresh button.

![](images/user_console.png)

#The automatic task producer

In addition, we have a web page that automatically produces tasks for two users, Bill and Jane, and marks them
 as done. For the automatic task producer, 
 open [http://localhost:5000/static/taskProducer.html](http://localhost:5000/static/taskProducer.html)
 when the app is running.
 
 The "Start"/"Stop" button can be used to start and stop task generation.
 This page also displays the same server configuration panel as the user console.

![](images/automatic_producer.png)
