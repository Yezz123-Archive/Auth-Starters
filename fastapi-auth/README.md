# FastAPI Auth

A ready to use authentication system developed using FastAPI framework.

## Installation

- Setup your virtual environment:

``` bash
virtualenv venv && source venv/bin/activate

pip install -r requirements.txt
```

- Now Copy the `.env.sample` file to `.env` and fill in the values.

## Usage

- This code exposes the following endpoints:

- `/api/register/`
- `/api/login/`
- `/api/valid/`

- To test **register** endpoint, run:

``` bash
    curl -X POST "http://localhost:8000/api/register/?username={USERNAME}&password={PASSWORD}" -H  "accept: application/json" -d ""
```

- To test **login** endpoint, run:

``` bash
    curl -X POST "http://localhost:8000/api/login/?username={USERNAME}&password={PASSWORD}" -H  "accept: application/json" -d ""
```
