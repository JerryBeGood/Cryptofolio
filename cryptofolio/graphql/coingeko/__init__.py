from ariadne import load_schema_from_path, ObjectType
from cryptofolio.graphql.coingeko import coingeko_resolvers

# Loading of schema definition
coingeko_typ_defs = load_schema_from_path('cryptofolio/graphql/coingeko')

# Initialization of type variables
coingeko_query = ObjectType("Query")

# Connection of resolvers to corresponding queries
coingeko_query.set_field('topAssets', coingeko_resolvers.resolve_topAssets)
coingeko_query.set_field('assetChartData',
                         coingeko_resolvers.resolve_assetChartData)
