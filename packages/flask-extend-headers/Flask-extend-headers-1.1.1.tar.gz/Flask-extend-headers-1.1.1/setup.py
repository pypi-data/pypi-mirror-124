# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_extend_headers']

package_data = \
{'': ['*']}

install_requires = \
['flask>=0.12.2']

setup_kwargs = {
    'name': 'flask-extend-headers',
    'version': '1.1.1',
    'description': 'Flask extend headers module for API versioning.',
    'long_description': '# flask-extend-headers\n\nFlask extend headers module for API versioning.\n\n[![PyPI version](https://badge.fury.io/py/flask-extend-headers.svg)](https://badge.fury.io/py/flask-extend-headers)\n\n## Description\n\nCustom header routing for versioning your Flask API.\n\n## Features\n\n* Use it as a decorator\n* Return with different views based on the custom header you set\n\n## Documentation\n\n### Installation\n\n```bash\npip install flask-extend-headers\n```\n\n### Quickstart\n\nBelow is an example of two API endpoints with different URL with version:\n\n```python\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route(\'/api/v2/users\')\ndef usersv2():\n    return "usersv2", 200\n\n@app.route(\'/api/v1/users\')\ndef users():\n    return "users", 200\n\nif __name__ == \'__main__\':\n    app.run()\n```\n\nWe could change this implementation using `flask_extend_headers` and specifying the version in the `headers`\n\n```python\nfrom flask import Flask\nfrom flask_extend_headers import ExtendHeaders\n\napp = Flask(__name__)\n\napp.config["EXTEND_HEADERS_KEY"] = "accept-version"\n\nextend_headers = ExtendHeaders(app)\n\ndef usersv2():\n    return "usersv2", 200\n\n@app.route(\'/api/users\')\n@extend_headers.register(\n    extensions={\n        "application/v2": usersv2,\n    },\n    default="application/v1"\n)\ndef users():\n    return "users", 200\n\nif __name__ == \'__main__\':\n    app.run()\n```\n\nIf we call this API it\'ll return a `406`:\n\n```bash\n> curl http://localhost:5000/api/users -I\nHTTP/1.0 406 NOT ACCEPTABLE\nContent-Type: text/html; charset=utf-8\nContent-Length: 350\nServer: Werkzeug/2.0.2 Python/3.9.6\nDate: Mon, 18 Oct 2021 19:33:46 GMT\n```\n\nIf we add the headers it\'ll return `users`:\n\n```bash\n> curl http://localhost:5000/api/users -I -H "Accept-Version: application/v1"\nHTTP/1.0 200 OK\nContent-Type: text/html; charset=utf-8\nContent-Length: 5\nServer: Werkzeug/2.0.2 Python/3.9.6\nDate: Mon, 18 Oct 2021 19:34:55 GMT\n```\n\nIf we modify the headers it\'ll return `usersv2`\n```bash\n> curl http://localhost:5000/api/users -I -H "Accept-Version: application/v2"\nHTTP/1.0 200 OK\nContent-Type: text/html; charset=utf-8\nContent-Length: 5\nServer: Werkzeug/2.0.2 Python/3.9.6\nDate: Mon, 18 Oct 2021 19:35:48 GMT\n```\n\n\n### Fallback on view\n\nIf you have a new version of a view but you want to fallback in a view without a specified version:\n\n```python\ndef usersv2():\n    return "usersv2", 200\n\n@app.route(\'/api/users\')\n@extend_headers.register(\n    extensions={\n        "application/v2": usersv2,\n    }\n)\ndef users():\n    return "users", 200\n```\n\nIf we call the endpoint without headers it\'ll return the fallback view `users`:\n\n```bash\n> curl http://localhost:5000/api/users -I\nHTTP/1.0 200 OK\nContent-Type: text/html; charset=utf-8\nContent-Length: 5\nServer: Werkzeug/2.0.2 Python/3.9.6\nDate: Mon, 18 Oct 2021 19:42:05 GMT\n```\n\nIf we call the endpoint specifying headers it\'ll return `usersv2`:\n\n```bash\n> curl http://localhost:5000/api/users -I -H "Accept-Version: application/v2"\nHTTP/1.0 200 OK\nContent-Type: text/html; charset=utf-8\nContent-Length: 7\nServer: Werkzeug/2.0.2 Python/3.9.6\nDate: Mon, 18 Oct 2021 19:42:36 GMT\n```\n\n## Testing\n\nInstall `poetry` and execute `pytest-cov`\n\n```bash\npip install poetry\npoetry install\npoetry run pytest --cov=flask_extend_headers tests\n```\n\n## License\n\nMIT\n',
    'author': 'Luis Emilio Moreno',
    'author_email': 'emilio@touchof.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lemiliomoreno/flask-extend-headers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
