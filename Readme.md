#Database migration with zero downtime

December 28, 2015

Adi Levin

#Setup

###Install dependencies

- [Install Python 2.7](https://www.python.org/downloads/)

- [Install MongoDB](https://docs.mongodb.org/manual/)

- Start a MongoDB instance by running
>`mongod`

- [Get greenlet package](https://pypi.python.org/pypi/greenlet) for Python
>`pip install greenlet`

- [Install gevent](http://www.gevent.org/) as the WSGI server

###Setup Python project

- Clone the repository
 
- Run tests
> `python run_all_tests.py`