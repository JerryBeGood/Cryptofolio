from ariadne import load_schema_from_path, ObjectType, make_executable_schema
import cryptofolio.graphql.coingeko.coingekoResolvers as coinGeko
import cryptofolio.graphql.binance.binanceResolvers as binance

# GraphQL
# Loading schema string into a variable
type_defs = load_schema_from_path("cryptofolio/graphql/")

# Initializing types variables
query = ObjectType("Query")
# TODO: What is the meaning of this line?
# TODO: And why there isn't declaration of coinChartData type and it works?
coin = ObjectType("Coin")

# Connecting resolving methods to schema queries
query.set_field('topCoins', coinGeko.resolve_topCoins)
query.set_field('coinChartData', coinGeko.resolve_coinChartData)
query.set_field('binanceAccountData', binance.resolve_binanceAccountData)

# Initialization of the shcema
schema = make_executable_schema(type_defs, query, coin)