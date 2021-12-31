from ariadne import load_schema_from_path
from ariadne.objects import ObjectType
from cryptofolio.graphql_api.resolvers import binance

binance_type_defs = load_schema_from_path(
    'cryptofolio/graphql_api/schema/binance')

binance_query = ObjectType("Query")

binance_query.set_field('binanceAccountInfo',
                        binance.binance_account_info_resolver)
binance_query.set_field('binanceExchangeInfo',
                        binance.binance_exchange_info_resolver)
