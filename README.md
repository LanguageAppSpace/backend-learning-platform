# Learning Platform


## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Tests](#tests)
- [API](#api)
- [Tools](#technologies-and-frameworks)
- [Contributions](#contributions)
- [License](#license)


## Overview
<div style="text-align: justify;">
The backend for learning platform, developed using Django Rest Framework (DRF), serves as the foundation for a robust educational tool. This repository encapsulates the core functionalities essential for managing and delivering educational content efficiently. Leveraging Django's powerful features and DRF's API capabilities, the platform facilitates seamless interaction between users and educational resources.
</div>


## Features
Basic User Functionality
<br>
<div style="text-align: justify;">
The basic user functionality provides essential features for managing user accounts within the application. Users can easily register new accounts using a secure registration form, which collects necessary information such as username, email address, and password. The registration process includes validation to ensure data integrity and security. Once registered, users can log in securely using their credentials, granting them access to personalized content and features. User authentication is handled using industry-standard security practices, protecting user data from unauthorized access.
</div>
<br>
Flashcards Functionality
<br>
<div style="text-align: justify;">
The flashcards functionality enriches the user experience by offering a comprehensive toolset for learning and practicing with digital flashcards. Users can create and manage lessons, organizing them based on topics or categories of interest. Within each lesson, users can add custom flashcards, each containing two sides: one for the prompt and the other for the answer. The application tracks user progress automatically, providing insights into which flashcards have been learned or require further review. This progress tracking helps users optimize their study sessions and achieve learning objectives efficiently.
</div>


## Installation

### Running project locally
<ol>
1. Clone the repository
<br>
<code>git clone https://github.com/ewasol/backend-learning-platform</code>
<br>
2. Change the directory
<br>
<code>cd backend</code>
<br>
3. Install dependencies
<br>
<code>pip install -r requirements.txt</code>
<br>
4. Apply database migrations
<br>
<code>python manage.py makemigrations</code>
<br>
<code>python manage.py migrate</code>
<br>
5. Run the project
<br>
<code>python manage.py runserver</code>
<br>
</ol>
Project will run on http://127.0.0.1:8000/


## API

All endpoints with methods are available under http://127.0.0.1:8000/swagger/


## Tests

Move to backend folder
<br>
` python manage.py backend `
<br>
Run all tests
<br>
` python manage.py test `


## Technologies and frameworks

- Backend
    
    [![Python](https://skillicons.dev/icons?i=python)](https://skillicons.dev) 
    [![Django](https://skillicons.dev/icons?i=django)](https://skillicons.dev)

    - Django Rest Framework

    - drf-yasg

- Databases

    - MySQL
    
        [![MySQL](https://skillicons.dev/icons?i=mysql)](https://skillicons.dev)

- Other

    [![PyCharm](https://skillicons.dev/icons?i=pycharm)](https://skillicons.dev)
    [![Postman](https://skillicons.dev/icons?i=postman)](https://skillicons.dev)


## Contributions
Contributions are welcome! Feel free to fork the repository, make changes, and submit pull requests for review.


## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
