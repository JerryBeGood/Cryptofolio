from ariadne import load_schema_from_path, ObjectType, make_executable_schema
from cryptofolio.graphql.binance import resolvers as binance_resolvers
from cryptofolio.graphql.coingeko import resolvers as coingeko_resolvers

# GraphQL
# Loading schemas into string variables
binance_type_defs = load_schema_from_path('cryptofolio/graphql/binance')
coingeko_typ_defs = load_schema_from_path(
    'cryptofolio/graphql/coingeko/schema.graphql')

# Initializing types variables
query = ObjectType("Query")
mutation = ObjectType("Mutation")

# Connecting resolving methods to schema queries
query.set_field('topAssets', coingeko_resolvers.resolve_topAssets)
query.set_field('assetChartData', coingeko_resolvers.resolve_assetChartData)
query.set_field('binanceAccountInfo',
                binance_resolvers.resolve_binanceAccountInfo)
query.set_field('binanceExchangeInfo',
                binance_resolvers.resolve_binanceExchangeInfo)

mutation.set_field('binanceSPOTMarketOrder',
                   binance_resolvers.resolve_binanceSPOTMarketOrder)

# Initialization of the shcema
schema = make_executable_schema([coingeko_typ_defs, binance_type_defs],
                                [query, mutation])
