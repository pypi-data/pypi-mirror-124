# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_pyctuator']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1,<2.0', 'pyctuator>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'flask-pyctuator',
    'version': '0.1.1',
    'description': 'Flask Extension for using Pyctuator to enable Spring Boot Admin (SBA) to monitor the application, see https://github.com/SolarEdgeTech/pyctuator',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/flask-pyctuator?color=green&style=plastic)](https://pypi.org/project/flask-pyctuator/)\n[![build](https://github.com/SolarEdgeTech/flask-pyctuator/workflows/build/badge.svg)](https://github.com/SolarEdgeTech/flask-pyctuator/)\n\n# Flask Pyctuator Extension\nA [Flask extension](https://flask.palletsprojects.com/en/2.0.x/extensions/) that uses [Pyctuator](https://github.com/SolarEdgeTech/pyctuator) to enable [Spring Boot Admin](https://github.com/codecentric/spring-boot-admin) (SBA) to monitor health, configuration, log-file and resource-usage of a Flask application.\n\nPlease see [Pyctuator](https://github.com/SolarEdgeTech/pyctuator) for the complete documentation and **note** that the some features such as monitoring memory/disk usage **require instlaling of additional modules**. \n\n\n# Quick Start\n1. Install Flask and the flask-pyctuator extension using your favorite python package manager\n2. Start a local SBA (Spring Boot Admin) server using Dockers:\n   ```sh\n   docker run --rm -p 8080:8080 --add-host=host.docker.internal:host-gateway michayaak/spring-boot-admin:2.2.3-1\n   ```\n3. Open SBA\'s main page, http://localhost:8080, in your browser\n4. Run the following Flask application:\n   ```python\n   from flask import Flask\n   from flask_pyctuator.flask_pyctuator import FlaskPyctuator\n   \n   app = Flask("Flask App with Pyctuator")\n   \n   \n   @app.route("/")\n   def hello():\n     return "Hello World!"\n   \n   \n   FlaskPyctuator(\n     app,\n     pyctuator_endpoint_url="http://host.docker.internal:5000/pyctuator",\n   )\n   \n   app.run(debug=False, port=5000, host="0.0.0.0")\n   ```\n\nSee the complete example and project file in the `example` folder.\n',
    'author': 'michael.yak',
    'author_email': 'michael.yakobi@solaredge.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SolarEdgeTech/flask-pyctuator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
