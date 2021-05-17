from ariadne import load_schema_from_path, ObjectType, make_executable_schema
from cryptofolio.graphql.binance import binanceResolvers, binanceQueries, binanceTypes
from cryptofolio.graphql.coingeko import coingekoQueries, coingekoResolvers, coingekoTypes

# GraphQL
# Loading schemas into string variables
allQueries = 'type Query{' + binanceQueries.binanceQueries + coingekoQueries.coingekoQueries + '}'
allTypes = binanceTypes.binanceTypes + coingekoTypes.coingekoTypes

# Initializing types variables
query = ObjectType("Query")

# Connecting resolving methods to schema queries
query.set_field('topAssets', coingekoResolvers.resolve_topAssets)
query.set_field('assetChartData', coingekoResolvers.resolve_assetChartData)
query.set_field('binanceAccountData',
                binanceResolvers.resolve_binanceAccountData)

# Initialization of the shcema
schema = make_executable_schema([allQueries, allTypes], query)