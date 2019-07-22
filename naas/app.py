#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
 app.py
 Author: Brett Lykins (lykinsbd@gmail.com)
 Description: Main app setup/config
"""

import logging

from flask import Flask
from flask_restful import Api
from naas.config import app_configure
from naas.library.errorhandlers import api_error_generator
from naas.resources.root import HelloWorld
from naas.resources.healthcheck import HealthCheck
from naas.resources.send_commands import GetResults, SendCommands


app = Flask(__name__)

# Setup your app
app.config["JSON_SORT_KEYS"] = False

app_configure(app)

# Setup logging:
logger = logging.getLogger("NAAS")
logger.propagate = False  # fix duplicate messages
if not logger.handlers:
    logger.setLevel(logging.INFO)
    stderr_handler = logging.StreamHandler()
    normal_formatter = logging.Formatter("%(levelname)s - %(message)s")
    stderr_handler.setFormatter(normal_formatter)
    logger.addHandler(stderr_handler)

# Get the error handling dict
api_errors = api_error_generator()

# Instantiate your API
api = Api(app, errors=api_errors, catch_all_404s=True)

# Add resources (wrappers for Flask views)
api.add_resource(HelloWorld, "/")
api.add_resource(HealthCheck, "/healthcheck")
api.add_resource(SendCommands, "/send_commands")
api.add_resource(GetResults, "/send_commands/<string:job_id>")