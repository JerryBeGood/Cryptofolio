from ariadne import load_schema_from_path, ObjectType
from cryptofolio.resolvers import coingeko

# Loading of schema definition
coingeko_typ_defs = load_schema_from_path(
    'cryptofolio/schema/coingeko')

# Initialization of type variables
coingeko_query = ObjectType("Query")

# Connection of resolvers to corresponding queries
coingeko_query.set_field('topAssets', coingeko.top_assets_resolver)
coingeko_query.set_field('assetChartData', coingeko.asset_chart_data_resolver)
