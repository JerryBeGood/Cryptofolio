from ariadne import load_schema_from_path
from ariadne.objects import ObjectType
from cryptofolio.resolvers import exchange

exchange_type_defs = load_schema_from_path(
    'cryptofolio/schema/exchange')

exchange_mutation = ObjectType('Mutation')
exchange_query = ObjectType('Query')

# Mutations
exchange_mutation.set_field('SPOTLimitOrder',
                            exchange.spot_limit_order_resolver)
exchange_mutation.set_field('SPOTMarketOrder',
                            exchange.spot_market_order_resolver)
exchange_mutation.set_field('SPOTStopLossLimitOrder',
                            exchange.spot_stop_loss_limit_order_resolver)

exchange_mutation.set_field('accountInfo',
                            exchange.account_info_resolver)

# Queries
exchange_query.set_field('closedOrders',
                         exchange.closed_orders_resolver)
exchange_query.set_field('openOrders',
                         exchange.open_orders_resolver)
exchange_query.set_field('exchangeInfo',
                         exchange.exchange_info_resolver)
