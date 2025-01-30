
# Novogradac Weather Application

This project displays the high and low temperature for any US location (with a 5-digit ZIP code) in an intuitive and easy to understand way.

It is built on Django and SQLite to maintain an efficient, minimal, and lightweight setup. SQLite was especially suited for this smaller application and quick iterative development.

The OpenWeatherMap's Current Weather API is integrated seamlessly for accurate and up-to-date weather information across the United States.

The app has been designed with a balance between usability and efficient resource use in mind. Efforts have been taken to both reduce API calls and still allow users to access often-searched queries through caching and form validation.



## Setup and Installation

1. Clone this GitHub repository using the URL or with GitHub Desktop.

2. Go to the directory where the project is installed.

2. Next, run 
```bash
pip install -r requirements.txt
```
or run
```bash
pipenv install
```
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

```
## Documentation

[NovoWeatherApp Documentation](https://github.com/francisvtran/NovoWeatherApp/blob/main/Novogradac_Take_Home_Assessment_Documentation.pdf)

