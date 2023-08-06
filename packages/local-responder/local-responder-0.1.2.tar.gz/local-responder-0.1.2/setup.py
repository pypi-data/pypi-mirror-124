# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['local_responder']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'local-responder',
    'version': '0.1.2',
    'description': 'A asynchronous temporary web server to repond to requests',
    'long_description': '# Local Responder\n\nLocal Responder is a helper function that creates a simple web server with just\none view that has only one purpose, to return simple data.\n\nThis is created just for the purpose of using in tests, to mock out an API in a\nvery simple manner.\n\n## Usage\n\nYou can import the `respond` function and use it as an asynchronous context manager\n\n```python\nimport asyncio\nimport aiohttp\nfrom local_responder import respond\n\n\nasync def func() -> None:\n    async with aiohttp.ClientSession() as session:\n        async with respond(\n            json={"status": "OK"},\n            path="/health",\n            method="get",\n            status_code=200,\n        ):\n            response = await session.get("http://localhost:5000/health")\n\n            data = await response.json()\n\n            assert data == {"status": "OK"}\n            assert response.status == 200\n\n        async with respond(\n            json={"status": "Error"},\n            path="/health",\n            method="get",\n            status_code=500,\n        ):\n            response = await session.get("http://localhost:5000/health")\n\n            data = await response.json()\n\n            assert data == {"status": "Error"}\n            assert response.status == 500\n\n\nif __name__ == "__main__":\n    asyncio.run(func())\n\n```\n\nThe context manager will raise an error if a request is made to an undefined\npath or using an unsupported method.\n\nYou need to provide one of `json`, `text` or `body` for the view to return, the\nother arguments are all optional, defaulting to creating a `GET` view with a\nstatus code 200 and listen on port 5000.\n',
    'author': 'Axel',
    'author_email': 'dev@absalon.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ikornaselur/local-responder',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
