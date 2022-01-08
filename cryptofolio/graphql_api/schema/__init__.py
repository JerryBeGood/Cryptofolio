from ariadne import make_executable_schema
from cryptofolio.graphql_api.schema.coingeko import coingeko_typ_defs, coingeko_query
from cryptofolio.graphql_api.schema.user_account import user_account_type_defs, user_account_mutation
from cryptofolio.graphql_api.schema.exchange import exchange_type_defs, exchange_mutation, exchange_query

# Initialization of the shcema
schema = make_executable_schema(
    [coingeko_typ_defs,
     user_account_type_defs,
     exchange_type_defs],
    [coingeko_query,
     user_account_mutation,
     exchange_mutation, exchange_query])
