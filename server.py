from flask import Flask, jsonify, request
from flask_cors import CORS
from logger import logger, configure

from resources.users import *

import json, yaml, hashlib, os


### Init controller routes manager
app = Flask(__name__)

### Load app config
conf = yaml.load(open('conf/api-conf.yml'))

# Logger configuration
configure(conf['log']['level_values'][conf['log']['level']],
          conf['log']['dir'], conf['log']['filename'],
          conf['log']['max_filesize'], conf['log']['max_files'])

### Load app config into Flask WSGI running instance
app.config['CONF'] = conf
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['CORS_HEADERS'] = 'Auth-Token, Content-Type, User, Content-Length'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

url_prefix = conf['url_prefix']

try:
    # Resources loading
    user_resource = User()
except:
    logger.error("ERREUR INITIALISATION ACCES RESOURCES")
    exit()



### Root REST API endpoint: display all available registered routes
@app.route(url_prefix + "/")
def index():
    logger.info("index")

    routes_tmp = {}
    for rule in app.url_map.iter_rules():
        urlhash = hashlib.md5() 
        urlhash.update((rule.rule).encode("utf8"))
        route = {
            'url' : rule.rule,
            'methods' : (routes_tmp[urlhash.hexdigest()]['methods']).union(rule.methods) if urlhash.hexdigest() in routes_tmp else rule.methods
        }
        routes_tmp[urlhash.hexdigest()] = route

    routes = []
    for k, r in routes_tmp.items():
        route = {
            "url": r['url'],
            "methods": list(r['methods'])
        }
        routes.append(route)

    return jsonify({"routes" : routes})


################################################################################
#   TECHNICAL ROUTES
################################################################################
@app.route(url_prefix + "/heartbeat")
def hello():
    return "yo"

@app.route(url_prefix + "/conf")
def api_conf():
    return jsonify(app.config['CONF'])

################################################################################
#   USERS ROUTES
################################################################################
@app.route(url_prefix + "/users", methods=['GET'])
def get_all_users():
    users = user_resource.get_all()
    return jsonify(users)

if __name__ == "__main__":
    # Run http REST stack
    logger.info("Run api on {}:{}".format(conf['host'], conf['port']))
    app.run(host=conf['host'], port=int(conf['port']), debug=conf['log']['level'] == "DEBUG")