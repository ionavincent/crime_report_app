[![Build Status](https://travis-ci.org/ionavincent/crime_report_app.svg?branch=master)](https://travis-ci.org/ionavincent/crime_report_app)

# Crime Report App

A simple REST API and web app to query, filter and sort crime reports from
[https://data.police.uk/data/](https://data.police.uk/data/).

The REST API is written in Python using Flask and SQLAlchemy.

## Running the App

The app is setup to run in a docker container. After cloning the repo, you
can start it by running
`make docker-run ZIP_FILE=data.zip` from the project directory where `data.zip` is a ZIP file downloaded from [https://data.police.uk/data/](https://data.police.uk/data/).

*Note*: The ZIP file has to reside in the project directory.

Once the app is running, the web app can be accessed at:

[http://127.0.0.1:8080/view](http://127.0.0.1:8080/view)

The swagger docs for the API can be accessed at:

[http://127.0.0.1:8080/#!/reports/get_report_collection](http://127.0.0.1:8080/#!/reports/get_report_collection)

## Running the Tests

The tests can be run from the project root directory with `make test`


