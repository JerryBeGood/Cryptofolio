from flask import Flask, request, jsonify
from ariadne import load_schema_from_path, ObjectType, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from GraphQL.Resolvers.coinGeko_resolvers import resolve_topCoins, resolve_coinChartData

# GraphQL
# Loading schema string into a variable
type_defs = load_schema_from_path("GraphQL/Schemas")

# Initializing types variables
query = ObjectType("Query")
# TODO: What is the meaning of this line?
# TODO: And why there isn't declaration of coinChartData type and it works?
coin = ObjectType("Coin")

# Connecting resolving methods to schema queries
query.set_field('topCoins', resolve_topCoins)
query.set_field('coinChartData', resolve_coinChartData)

# Initialization of the shcema
schema = make_executable_schema(type_defs, query, coin)

#Application
app = Flask(__name__.split('.')[0])


# GraphQL API endpoints
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
                                   debug=app.debug)

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)
