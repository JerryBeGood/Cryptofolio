from ariadne import load_schema_from_path
from ariadne.objects import ObjectType
from cryptofolio.graphql_api.resolvers import exchanges

exchange_type_defs = load_schema_from_path(
    'cryptofolio/graphql_api/schema/exchange')

exchange_mutation = ObjectType('Mutation')

exchange_mutation.set_field('SPOTLimitOrder',
                            exchanges.spot_limit_order_resolver)
exchange_mutation.set_field('SPOTMarketOrder',
                            exchanges.spot_market_order_resolver)
exchange_mutation.set_field('SPOTStopLossLimitOrder',
                            exchanges.spot_stop_loss_limit_order_resolver)
