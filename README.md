# Django-Task-Tracker
This repository contains a backend for learning platform built with Django Rest Framework.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Tests](#tests)
- [Docker](#docker-compose)
- [API](#api)
- [Tools](#technologies-and-frameworks)
- [Contributions](#contributions)
- [License](#license)


## Overview

## Features

## Installation
### Running project locally
1. Clone the repository

   `git clone https://github.com/Ewa-Anna/backend-learning-platform`

2. Change the directory

   `cd backend`

3. Install dependencies

   `pip install -r requirements.txt`

4. Apply database migrations

   `python manage.py makemigrations`

   `python manage.py migrate`

5. Run the project

   `python manage.py runserver`

Project will run on http://127.0.0.1:8000/


### docker-compose
Building Docker Image
<br>
` docker-compose build `
<br>
Running Docker Container
<br>
` docker-compose up -d `


## API

All endpoints with methods are available under http://127.0.0.1:8000/swagger/

## Tests


## Technologies and frameworks

- Backend
    
    [![Python](https://skillicons.dev/icons?i=python)](https://skillicons.dev) 
    [![Django](https://skillicons.dev/icons?i=django)](https://skillicons.dev)
    - Django Rest Framework
    - drf-yasg

- Databases
    - For Dev

        [![SQLite](https://skillicons.dev/icons?i=sqlite)](https://skillicons.dev)
    - For Prod
    
        [![PostgreSQL](https://skillicons.dev/icons?i=postgres)](https://skillicons.dev)

- Other

    [![VisualStudio](https://skillicons.dev/icons?i=vscode)](https://skillicons.dev)
    [![Docker](https://skillicons.dev/icons?i=docker)](https://skillicons.dev)
    [![Postman](https://skillicons.dev/icons?i=postman)](https://skillicons.dev)


## Contributions
Contributions are welcome! Feel free to fork the repository, make changes, and submit pull requests for review.

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
