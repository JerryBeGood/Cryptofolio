from ariadne import load_schema_from_path
from ariadne.objects import ObjectType
import cryptofolio.graphql.binance.binance_resolvers as binance_resolvers

# Loading of schema definition
binance_type_defs = load_schema_from_path('cryptofolio/graphql/binance')

# Initialization of type variables
binance_query = ObjectType("Query")
binance_mutation = ObjectType("Mutation")

# Connection of resolvers to corresponding queries
binance_query.set_field('binanceAccountInfo',
                        binance_resolvers.resolve_binanceAccountInfo)
binance_query.set_field('binanceExchangeInfo',
                        binance_resolvers.resolve_binanceExchangeInfo)

# Connection of resolvers to corresponding mutations
binance_mutation.set_field('binanceSPOTMarketOrder',
                           binance_resolvers.resolve_binanceSPOTMarketOrder)
binance_mutation.set_field('binanceSPOTLimitOrder',
                           binance_resolvers.resolve_binanceSPOTLimiOrder)
binance_mutation.set_field(
    'binanceSPOTStopLossLimitOrder',
    binance_resolvers.resolve_binanceSPOTStopLossLimitOrder)
