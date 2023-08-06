[![PyPI](https://img.shields.io/pypi/v/flask-pyctuator?color=green&style=plastic)](https://pypi.org/project/flask-pyctuator/)
[![build](https://github.com/SolarEdgeTech/flasl-pyctuator/workflows/build/badge.svg)](https://github.com/SolarEdgeTech/flask-pyctuator/)

# Flask Pyctuator Extension
A [Flask extension](https://flask.palletsprojects.com/en/2.0.x/extensions/) that uses [Pyctuator](https://github.com/SolarEdgeTech/pyctuator) to enable [Spring Boot Admin](https://github.com/codecentric/spring-boot-admin) (SBA) to monitor health, configuration, log-file and resource-usage of a Flask application.

Please see [Pyctuator](https://github.com/SolarEdgeTech/pyctuator) for the complete documentation and **note** that the some features such as monitoring memory/disk usage **require instlaling of additional modules**. 


# Quick Start
1. Install Flask and the flask-pyctuator extension using your favorite python package manager
2. Start a local SBA (Spring Boot Admin) server using Dockers:
   ```sh
   docker run --rm -p 8080:8080 --add-host=host.docker.internal:host-gateway michayaak/spring-boot-admin:2.2.3-1
   ```
3. Open SBA's main page, http://localhost:8080, in your browser
4. Run the following Flask application:
   ```python
   from flask import Flask
   from flask_pyctuator.flask_pyctuator import FlaskPyctuator
   
   app = Flask("Flask App with Pyctuator")
   
   
   @app.route("/")
   def hello():
     return "Hello World!"
   
   
   FlaskPyctuator(
     app,
     pyctuator_endpoint_url="http://host.docker.internal:5000/pyctuator",
   )
   
   app.run(debug=False, port=5000, host="0.0.0.0")
   ```