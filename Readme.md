#Database migration with zero downtime

December 28, 2015

Adi Levin

#Setup

###Install dependencies

- [Install Python 2.7](https://www.python.org/downloads/)

- [Install MongoDB](https://docs.mongodb.org/manual/)

- Start a MongoDB instance by running
>`mongod`

- [Installl greenlet package](https://pypi.python.org/pypi/greenlet), a prerequisite for gevent
>`pip install greenlet`

- [Install gevent](http://www.gevent.org/) as the WSGI server

- [Install latest version of NGINX](http://nginx.org/en/download.html) which we use as a reverse proxy, to 
switch between different application versions without downtime 

###Setup Python project

- Clone the repository

- Run tests
> `python -m unittest discover -s test`

###Setup reverse proxy

- Copy nginx/nginx.conf to the conf subfolder in the nginx folder
 
- Run NGINX
> start nginx

###Run application
 
- Open a command-line in the db-migration folder

- Set PYTHONPATH to the current directory
> `set PYTHONPATH=.` (on Windows)
 
- Run the application on port 8000
> `python main/main.py 8000`

###Start web clients

- Open `web-clients/user-console/index.html` in a browser

- Open `web-clients/automatic-agent/index.html` in a browser

