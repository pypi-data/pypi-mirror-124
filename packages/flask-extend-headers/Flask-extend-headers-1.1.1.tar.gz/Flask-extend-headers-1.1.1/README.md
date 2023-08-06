# flask-extend-headers

Flask extend headers module for API versioning.

[![PyPI version](https://badge.fury.io/py/flask-extend-headers.svg)](https://badge.fury.io/py/flask-extend-headers)

## Description

Custom header routing for versioning your Flask API.

## Features

* Use it as a decorator
* Return with different views based on the custom header you set

## Documentation

### Installation

```bash
pip install flask-extend-headers
```

### Quickstart

Below is an example of two API endpoints with different URL with version:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/api/v2/users')
def usersv2():
    return "usersv2", 200

@app.route('/api/v1/users')
def users():
    return "users", 200

if __name__ == '__main__':
    app.run()
```

We could change this implementation using `flask_extend_headers` and specifying the version in the `headers`

```python
from flask import Flask
from flask_extend_headers import ExtendHeaders

app = Flask(__name__)

app.config["EXTEND_HEADERS_KEY"] = "accept-version"

extend_headers = ExtendHeaders(app)

def usersv2():
    return "usersv2", 200

@app.route('/api/users')
@extend_headers.register(
    extensions={
        "application/v2": usersv2,
    },
    default="application/v1"
)
def users():
    return "users", 200

if __name__ == '__main__':
    app.run()
```

If we call this API it'll return a `406`:

```bash
> curl http://localhost:5000/api/users -I
HTTP/1.0 406 NOT ACCEPTABLE
Content-Type: text/html; charset=utf-8
Content-Length: 350
Server: Werkzeug/2.0.2 Python/3.9.6
Date: Mon, 18 Oct 2021 19:33:46 GMT
```

If we add the headers it'll return `users`:

```bash
> curl http://localhost:5000/api/users -I -H "Accept-Version: application/v1"
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 5
Server: Werkzeug/2.0.2 Python/3.9.6
Date: Mon, 18 Oct 2021 19:34:55 GMT
```

If we modify the headers it'll return `usersv2`
```bash
> curl http://localhost:5000/api/users -I -H "Accept-Version: application/v2"
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 5
Server: Werkzeug/2.0.2 Python/3.9.6
Date: Mon, 18 Oct 2021 19:35:48 GMT
```


### Fallback on view

If you have a new version of a view but you want to fallback in a view without a specified version:

```python
def usersv2():
    return "usersv2", 200

@app.route('/api/users')
@extend_headers.register(
    extensions={
        "application/v2": usersv2,
    }
)
def users():
    return "users", 200
```

If we call the endpoint without headers it'll return the fallback view `users`:

```bash
> curl http://localhost:5000/api/users -I
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 5
Server: Werkzeug/2.0.2 Python/3.9.6
Date: Mon, 18 Oct 2021 19:42:05 GMT
```

If we call the endpoint specifying headers it'll return `usersv2`:

```bash
> curl http://localhost:5000/api/users -I -H "Accept-Version: application/v2"
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 7
Server: Werkzeug/2.0.2 Python/3.9.6
Date: Mon, 18 Oct 2021 19:42:36 GMT
```

## Testing

Install `poetry` and execute `pytest-cov`

```bash
pip install poetry
poetry install
poetry run pytest --cov=flask_extend_headers tests
```

## License

MIT
