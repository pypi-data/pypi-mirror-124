# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bareasgi_cors']

package_data = \
{'': ['*']}

install_requires = \
['bareasgi>=4.0,<5.0']

setup_kwargs = {
    'name': 'bareasgi-cors',
    'version': '4.1.0',
    'description': 'CORS support for bareasgi',
    'long_description': "# bareASGI-cors\n\nCORS support for [bareASGI](http://github.com/rob-blackbourn/bareasgi) (read the\n[docs](https://rob-blackbourn.github.io/bareASGI-cors/))\n\n## Usage\n\nSimply create the `CORSMiddleware` class and put is as the first middleware.\n\n```python\nimport json\nimport uvicorn\nfrom bareasgi import (\n    Application,\n    text_reader,\n    text_writer\n)\nfrom bareasgi_cors import CORSMiddleware\n\nasync def get_info(request):\n    text = json.dumps(request.info)\n    return HttpResponse(200, [(b'content-type', b'application/json')], text_writer(text))\n\n\nasync def set_info(request):\n    text = await text_reader(request.body)\n    data = json.loads(text)\n    request.info.update(data)\n    return HttpResponse(204)\n\n# Create the CORS middleware class\ncors_middleware = CORSMiddleware()\n\n# Use the CORS middleware as the first middleware.\napp = Application(info={'name': 'Michael Caine'}, middlewares=[cors_middleware])\n\napp.http_router.add({'GET'}, '/info', get_info)\napp.http_router.add({'POST', 'OPTIONS'}, '/info', set_info)\n\nuvicorn.run(app, port=9010)\n```\n\n## The POST method\n\nIn the above example an OPTION method is included with the POST. This\nis always required with a POST as a browser will try first with an OPTION.\n",
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/bareASGI-cors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
