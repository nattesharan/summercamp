## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
* Python3.6 and MySql
```

### Installing

A step by step series of examples that tell you how to get the project up and running

#### Using Python

* Create a virtual environment using `virtualenv name`

* Navigate to the project dir and then do `pip install -r requirements.txt` . This should get all the requirements installed

* run `python manage.py create_categories` and `python manage.py create_roles` these should populate user roles and activity categories.

* Start the server with `python manage.py runserver` and run `pytest` if you want to run tests.