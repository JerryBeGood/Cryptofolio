from ariadne import make_executable_schema
from cryptofolio.graphql_api.schema.binance import binance_mutation, binance_query, binance_type_defs
from cryptofolio.graphql_api.schema.coingeko import coingeko_typ_defs, coingeko_query
from cryptofolio.graphql_api.schema.user_account import user_account_type_defs, user_account_mutation

# Initialization of the shcema
schema = make_executable_schema(
    [coingeko_typ_defs, binance_type_defs, user_account_type_defs],
    [coingeko_query, binance_query, binance_mutation, user_account_mutation])
