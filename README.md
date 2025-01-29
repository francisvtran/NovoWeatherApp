
# Novogradac Weather Application

This project displays the high and low temperature for any U.S. location (with a ZIP code) in an intuitive and easy to understand way.

It is built on Django and SQLite to maintain an efficient, minimal, and lightweight setup. 

The OpenWeatherMap's Current Weather API is integrated seamlessly for accurate and up-to-date weather information across the United States.

The app has been designed with a balance between usability and efficient resource use in mind. Efforts have been taken to both reduce API calls and still allow users to access often-searched queries through caching and form validation.



## Setup and Installation

1. Clone this GitHub repository using either the link or with GitHub Desktop.

```bash
  npm install my-project
  cd my-project
```

2. Next, 
    
## Run Locally

Once in the project directory, use:

```bash
python manage.py runserver
```
to start the server.

You should be all set to start inputting ZIP codes and seeing weather in different locations!
## Running Tests

To run all tests, run the following command

```bash
python manage.py test
```

For specific test files, run these commands

```bash
python manage.py test weather.tests.test_forms
python manage.py test weather.tests.test_views
python manage.py test weather.tests.test_models
python manage.py test weather.tests.test_api

```
## Documentation

[Documentation](https://linktodocumentation)

