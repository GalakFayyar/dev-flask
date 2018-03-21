#!/usr/bin/python
# -*- coding: utf8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS

from commons.logger import logger, configure
from commons import configuration

from resources.users import *

import json, os


script_dir = os.path.dirname(__file__)


def _init_app():
    ### Load app config
    _conf = configuration.load()
    _url_prefix = _conf['url_prefix']

    ### Init controller routes manager
    _app = Flask(__name__)

    ### Load app config into Flask WSGI running instance
    _app.config['CONF'] = _conf
    _app.config['PROPAGATE_EXCEPTIONS'] = True

    _app.config['CORS_HEADERS'] = 'Auth-Token, Content-Type, User, Content-Length'
    cors = CORS(_app, resources={r"/*": {"origins": "*"}})

    return _app, _url_prefix, _conf

def _load_resources():
    try:
        # Resources loading
        _users_resource = User(None)
    except:
        logger.error("ERREUR INITIALISATION ACCES RESOURCES")
        exit()

    return _users_resource

################################################################################
#   INIT APP FLASK
################################################################################
app, url_prefix, conf = _init_app()
users_resource = _load_resources()

################################################################################
#   TECHNICAL ROUTES
################################################################################
@app.route(url_prefix + "/heartbeat")
def hello():
    return "bim boum"

@app.route(url_prefix + "/conf")
def api_conf():
    return jsonify(app.config['CONF'])

@app.route(url_prefix + "/users")
def users():
    users = users_resource.get_users()
    return jsonify(users)


if __name__ == "__main__":
    # Run http REST stack
    logger.info("Run api on {}:{}".format(conf['host'], conf['port']))
    app.run(host=conf['host'], port=int(conf['port']), debug=conf['log']['level'] == "DEBUG")