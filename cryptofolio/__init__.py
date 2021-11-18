from flask import Flask
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML

from cryptofolio.graphql_api.schema import schema
from cryptofolio.models import db
from cryptofolio.config import DevelopmentConfig

app = Flask(__name__.split('.')[0])
app.config.from_object(DevelopmentConfig)

mail = Mail()
bcrypt = Bcrypt()

db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
app.app_context().push()


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(schema,
                                   data,
                                   context_value=request,
                                   debug=crypto.app.debug)

    status_code = 200 if success else 400
    return jsonify(result), status_code
